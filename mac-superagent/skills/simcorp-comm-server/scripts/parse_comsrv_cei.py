#!/usr/bin/env python3
"""Parse SimCorp Dimension Communication Server CEI exports into the catalogue tables
used by the simcorp-comm-server skill.

Nothing is hardcoded: every value printed comes from the CEI files you point it at.
Run it after any fresh export so reference 06 can be regenerated rather than hand-typed.

Usage:
    python3 parse_comsrv_cei.py <folder-with-cei-files> [--json out.json]

Recognised exports (matched on the CEI [Content] table name, not the file name):
    tCOMSRVSETUPS     Communication Server Setups
    tCOMSRVPARSETS    Communication Server Parameter Sets
    tPFDDIRECTORIES   Protected File Directories
    tCSCONFMSGTYPES   Configurable Message Types
    tREFFILENAMES     Reference File Names
"""
import sys, os, json, argparse, glob


def read_blocks(path):
    """A CEI file is [Section] headers followed by ' key=value' lines."""
    blocks, cur = {}, None
    with open(path, encoding="utf-8-sig", errors="replace") as fh:
        for line in fh:
            s = line.rstrip("\n")
            t = s.strip()
            if t.startswith("[") and t.endswith("]"):
                cur = t[1:-1]
                blocks[cur] = []
            elif cur is not None:
                blocks[cur].append(s)
    return blocks


def kv(line):
    t = line.strip()
    if "=" not in t:
        return None, None
    k, v = t.split("=", 1)
    return k, v


def config_header(blocks):
    out = {}
    for line in blocks.get("Config", []):
        k, v = kv(line)
        if k:
            out[k] = v
    return out


def parse_setups(blocks):
    setups = {}
    for name, lines in blocks.items():
        if not name.startswith("tCOMSRVSETUPS_"):
            continue
        sid = name[len("tCOMSRVSETUPS_"):]
        rec = {"id": sid, "header": {}, "params": [], "msgtypes": [], "configs": []}
        cur = None
        for line in lines:
            t = line.strip()
            if t.startswith("tCOMSRVSETUPCNFPARS="):
                cur = {}; rec["params"].append(cur); continue
            if t.startswith("tCOMSRVSETUPMSGTYPES="):
                cur = {}; rec["msgtypes"].append(cur); continue
            if t.startswith("tCOMSRVSETUPCONFIGS="):
                cur = {}; rec["configs"].append(cur); continue
            k, v = kv(line)
            if k:
                (cur if cur is not None else rec["header"])[k] = v
        setups[sid] = rec
    return setups


def parse_parsets(blocks):
    sets_ = {}
    for name, lines in blocks.items():
        if not name.startswith("tCOMSRVPARSETS_"):
            continue
        pid = name[len("tCOMSRVPARSETS_"):]
        rec = {"id": pid, "header": {}, "setups": []}
        cur = None
        for line in lines:
            t = line.strip()
            if t.startswith("tCOMSRVPARSETSSUB="):
                cur = {}; rec["setups"].append(cur); continue
            k, v = kv(line)
            if k:
                (cur if cur is not None else rec["header"])[k] = v
        sets_[pid] = rec
    return sets_


def parse_simple(blocks, prefix, keep):
    out = {}
    for name, lines in blocks.items():
        if not name.startswith(prefix):
            continue
        rec = {}
        for line in lines:
            k, v = kv(line)
            if k in keep:
                rec[k] = v
        out[name[len(prefix):]] = rec
    return out


def load_folder(folder):
    data = {"setups": {}, "parsets": {}, "pfd": {}, "msgtypes": {}, "reffiles": {},
            "provenance": {}}
    for path in sorted(glob.glob(os.path.join(folder, "*.cei"))):
        b = read_blocks(path)
        hdr = config_header(b)
        if hdr and not data["provenance"]:
            data["provenance"] = {k: hdr.get(k) for k in
                                  ("version", "svcpack", "track", "state", "custid",
                                   "custname", "userid", "utctime")}
        data["setups"].update(parse_setups(b))
        data["parsets"].update(parse_parsets(b))
        data["pfd"].update(parse_simple(
            b, "tPFDDIRECTORIES_", {"pPFDDIR", "pPFDBASEDIR", "pPFDSTATUS", "pPFDDESC"}))
        data["msgtypes"].update(parse_simple(
            b, "tCSCONFMSGTYPES_", {"pCSCONFMSG", "pCSCONFMSGNAME", "pCSMSGTYPE"}))
        data["reffiles"].update(parse_simple(
            b, "tREFFILENAMES_", {"pREFFILE", "pREFFILENAME", "pOPENMODE", "pCREATEDIR"}))
    return data


def report(d):
    p = d["provenance"]
    print("PROVENANCE:", ", ".join(f"{k}={v}" for k, v in p.items() if v))
    print(f"\nSETUPS ({len(d['setups'])})")
    for sid, r in sorted(d["setups"].items()):
        h = r["header"]
        print(f"\n== {sid} | {h.get('pCSSETUPNAME','')}")
        print(f"   owner={h.get('pCSOWNER','')} parallel={h.get('pCSPARALLEL','')} "
              f"pkg={h.get('pIFCPKGNO','')}")
        mt = "; ".join(
            f"{m.get('pCSMSGTYPE','')}"
            + (f"/{m['pCSCONFMSGIK-pCSCONFMSG']}" if m.get('pCSCONFMSGIK-pCSCONFMSG') else "")
            + ("" if str(m.get('pCSACTIVE','')).startswith('1') else " [INACTIVE]")
            for m in r["msgtypes"]) or "(none)"
        print("   msgtypes:", mt)
        cf = "; ".join(
            f"{c.get('pFILENAME','')}@{c.get('pPFDDIRIK-pPFDDIR','')}"
            + ("" if str(c.get('pCSACTIVE','')).startswith('1') else " [INACTIVE]")
            for c in r["configs"]) or "(none)"
        print("   configs :", cf)
        for prm in r["params"]:
            print(f"   param   : {prm.get('pCSCNFPAR','')} = {prm.get('pCSTEXT','')}")

    print(f"\nPARAMETER SETS ({len(d['parsets'])})")
    referenced = set()
    for pid, r in sorted(d["parsets"].items()):
        h = r["header"]
        print(f"  {pid:18} {h.get('pCSTYPE',''):22} log_mode={h.get('pCSLOGMODE',''):22}"
              f" log_dir={h.get('pCSLOGDIR-pREFFILE','')}")
        for s in r["setups"]:
            sid = s.get("pCSSETUPIK-pCSSETUP", "")
            referenced.add(sid)
            print(f"      -> {sid:18} active={s.get('pCSACTIVE','')}")

    print(f"\nPROTECTED FILE DIRECTORIES ({len(d['pfd'])})")
    for k, r in sorted(d["pfd"].items()):
        print(f"  {r.get('pPFDBASEDIR','')} {r.get('pPFDDIR','')} status={r.get('pPFDSTATUS','')}")

    print(f"\nCONFIGURABLE MESSAGE TYPES ({len(d['msgtypes'])})")
    for k, r in sorted(d["msgtypes"].items()):
        print(f"  {r.get('pCSCONFMSG','')} | {r.get('pCSCONFMSGNAME','')} | type={r.get('pCSMSGTYPE','')}")

    print(f"\nREFERENCE FILE NAMES ({len(d['reffiles'])})")
    for k, r in sorted(d["reffiles"].items()):
        print(f"  {r.get('pREFFILE','')} | {r.get('pREFFILENAME','')}")

    known = set(d["setups"])
    print("\nCONSISTENCY")
    print("  referenced by a parameter set but NOT in this export:",
          sorted(referenced - known) or "none")
    print("  exported but in NO parameter set:", sorted(known - referenced) or "none")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", help="folder containing the *.cei exports")
    ap.add_argument("--json", help="also write the parsed structure as JSON")
    a = ap.parse_args()
    if not os.path.isdir(a.folder):
        sys.exit(f"not a folder: {a.folder}")
    data = load_folder(a.folder)
    if not data["setups"] and not data["parsets"]:
        sys.exit("no Communication Server objects found in that folder")
    report(data)
    if a.json:
        with open(a.json, "w") as fh:
            json.dump(data, fh, indent=1)
        print(f"\nwrote {a.json}")
