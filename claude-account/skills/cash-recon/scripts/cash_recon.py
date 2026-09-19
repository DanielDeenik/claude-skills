#!/usr/bin/env python3
"""cash_recon.py

Reconcile the offline Cash Management Template (csh sheet) against a SimCorp
Asset Manager Cash Viewer export, one row per mapped bank account.

Inputs (all paths are arguments, nothing is hard coded):
  --expected   template workbook whose column "Total Available Cash" is the
               expectation for the recon date (the previous day's file)
  --actual     template workbook whose column "Credit/Debit Balance" is the
               custodian balance on the recon date (today's file)
  --viewer     Cash Viewer export (Sheet1: Security ID, Cash balance <date>,
               Cash movement <date> columns; portfolio rows, currency rows,
               account rows)
  --map        CSV with columns template_account, simcorp_account, portfolio,
               currency, source  (one row per bank account to compare)
  --date       recon value date as M/D/YYYY, must be a column date in --viewer
  --out        output xlsx (one sheet, Recon)

Output columns: template account, SimCorp account, portfolio, currency,
expected (col N of --expected), actual (col D of --actual), actual less
expected, SimCorp balance on --date, SimCorp less actual, note.
A second block lists every bare currency row (cash position with no bank
account) found in the viewer export with its non zero movements, because
those are the orders that did not receive a bank account.
"""
import argparse, csv, datetime as dt, re, sys
import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

CCY = re.compile(r"^[A-Z]{3}$")


def read_template(path, sheet, wanted):
    ws = openpyxl.load_workbook(path, data_only=True)[sheet]
    hdr = {}
    for row in ws.iter_rows(min_row=1, max_row=5):
        for c in row:
            if isinstance(c.value, str) and c.value.strip() in wanted:
                hdr[c.value.strip()] = c.column
        if len(hdr) == len(wanted):
            break
    missing = [w for w in wanted if w not in hdr]
    if missing:
        sys.exit(f"{path}: header(s) not found on rows 1 to 5: {missing}")
    acct_col = hdr["Account #"]
    out = {}
    for r in range(1, ws.max_row + 1):
        a = ws.cell(r, acct_col).value
        if a is None:
            continue
        key = str(a).strip()
        out[key] = {w: ws.cell(r, hdr[w]).value for w in wanted}
    return out


def read_viewer(path):
    ws = openpyxl.load_workbook(path, data_only=True).active
    dates = []  # (column, date)
    for c in range(1, ws.max_column + 1):
        h = ws.cell(1, c).value
        if isinstance(h, str) and (h.startswith("Cash balance") or h.startswith("Cash movement")):
            m = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", h)
            if m:
                dates.append((c, dt.datetime.strptime(m.group(1), "%m/%d/%Y").date()))
    if not dates:
        sys.exit(f"{path}: no Cash balance or Cash movement date columns on row 1")
    rows = []  # dict(portfolio, currency, account, kind, balances{date: cumulative})
    pf = ccy = None
    for r in range(2, ws.max_row + 1):
        a, b = ws.cell(r, 1).value, ws.cell(r, 2).value
        if a is None and b is None:
            continue
        if a is not None and b is None:
            if CCY.match(str(a).strip()):
                ccy = str(a).strip(); kind = "currency"; label = ccy
            else:
                pf = str(a).strip(); ccy = None; kind = "portfolio"; label = pf
        else:
            label = str(b).strip()
            kind = "cash_account" if CCY.match(label) else "bank_account"
        cum, bal = 0.0, {}
        for c, d in dates:
            v = ws.cell(r, c).value
            cum += float(v) if isinstance(v, (int, float)) else 0.0
            bal[d] = round(cum, 2)
        rows.append(dict(portfolio=pf, currency=ccy, label=label, kind=kind, balances=bal))
    return rows, [d for _, d in dates]


def style(ws):
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = ws.dimensions
    for c in ws[1]:
        c.font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="000000")
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.font = Font(name="Calibri", size=14)
            if isinstance(c.value, (int, float)):
                c.number_format = "#,##0.00;(#,##0.00)"
    for i in range(1, ws.max_column + 1):
        ws.column_dimensions[get_column_letter(i)].width = 24


def main():
    ap = argparse.ArgumentParser()
    for k in ("expected", "actual", "viewer", "map", "date", "out"):
        ap.add_argument("--" + k, required=True)
    ap.add_argument("--sheet", default="csh")
    a = ap.parse_args()
    recon_date = dt.datetime.strptime(a.date, "%m/%d/%Y").date()
    wanted = ["Account #", "Credit/Debit Balance", "Total Available Cash"]
    exp = read_template(a.expected, a.sheet, wanted)
    act = read_template(a.actual, a.sheet, wanted)
    viewer, dates = read_viewer(a.viewer)
    if recon_date not in dates:
        sys.exit(f"{a.date} is not a column in the viewer export; columns: {[d.strftime('%m/%d/%Y') for d in dates]}")
    by_acct = {r["label"]: r for r in viewer if r["kind"] == "bank_account"}
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Recon"
    ws.append(["Template account", "SimCorp account", "Portfolio", "Currency",
               "Expected", "Actual", "Actual less expected",
               f"SimCorp balance {a.date}", "SimCorp less actual", "Note"])
    with open(a.map, newline="") as fh:
        for m in csv.DictReader(fh):
            t, s = m["template_account"].strip(), m["simcorp_account"].strip()
            e = exp.get(t, {}).get("Total Available Cash")
            v = act.get(t, {}).get("Credit/Debit Balance")
            sc = by_acct.get(s, {}).get("balances", {}).get(recon_date)
            note = []
            if t not in exp: note.append("template account not in expected file")
            if t not in act: note.append("template account not in actual file")
            if s not in by_acct: note.append("SimCorp account not in viewer export")
            if isinstance(v, (int, float)) and v == 0 and isinstance(e, (int, float)) and e != 0:
                note.append("actual reads 0, check the feeding sheet (DJD or dph cash bal) is populated")
            d1 = round(v - e, 2) if isinstance(v, (int, float)) and isinstance(e, (int, float)) else None
            d2 = round(sc - v, 2) if isinstance(sc, (int, float)) and isinstance(v, (int, float)) else None
            ws.append([t, s, m.get("portfolio", ""), m.get("currency", ""), e, v, d1, sc, d2, "; ".join(note)])
    ws.append([])
    ws.append(["Cash account row (no bank account)", "Portfolio", "Currency", "Value date", "Movement"])
    for r in viewer:
        if r["kind"] != "cash_account":
            continue
        prev = 0.0
        for d in dates:
            mv = round(r["balances"][d] - prev, 2); prev = r["balances"][d]
            if mv != 0:
                ws.append([r["label"], r["portfolio"], r["currency"], d.strftime("%m/%d/%Y"), mv])
    style(ws)
    wb.save(a.out)
    print(f"written {a.out}")


if __name__ == "__main__":
    main()
