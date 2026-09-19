# 03 The offline Cash Management Template (Jason Carter, xlsm)

Read from the files of 8 and 9 September 2026. Sheet names and formulas were
read from the workbook, not assumed. Re-read them on every new file; the
desk edits this workbook by hand.

## Sheets

Visible: csh (the working sheet, A1:NQ348), Bulk Fees, dph cash bal, DJD,
TradeSummary, AVISO Tradefile Intermediary, JC ToDo. Hidden: Home, Trade
File, Bond Trade File, Treasuries Trade File, Wires, DSF Rec, Cred Pos, Cred
Trans, OptionCheck, OptionAssignment, Ref, DownloadOptionTrades, MutualFund,
FX, DistributionSummary, Credential Security Class Codes, SwitchTrades, To
Do, mf trades, Notes, E-mail Template, Sheet1, old, PM Rec Format, and a
veryHidden PB_CACHE.

## csh sheet columns (header row 2)

A Portfolio code (NWM110, NWM120, NWM140, NWM241, NWM300, NWM280, NWM250,
NWM270, NWM330, NWM510, NWM530, NWM520, MVS2024, NWM260, NWM160, NWM290;
Desjardins rows carry D471, D552, D478, D470).
B Fund Name. C Account # (custodian account, for example 504110L1).
D Credit/Debit Balance. Formula on the custodian rows:
=IFERROR(-INDEX('dph cash bal'!A:A, MATCH(csh!C3,'dph cash bal'!C:C,0)),0)
so D is the negated Debit Balance column of the dph cash bal sheet, which is
the custodian export of that morning. Desjardins rows use
=SUMIFS(DJD!X:X, DJD!B:B, csh!C16, DJD!J:J, "USD CURNCY") so they read the
DJD sheet (Desjardins position export, column X Market Value Account
Currency, filtered to the USD CURNCY line).
E Trading Summary (Settles next biz day). Array formula summing
TradeSummary!J (Net Change) for the fund class codes of the row, minus
switches in and out (columns F and G) for the equity rows, for example
NWM110 sums NWM110, NWM114, NWM116, NWM11600, NWM11604, NWM118.
F Notes. G H I Fund Flow (1) (2) (3), typed by hand. J Bulk Fee Capture:
=SUMIF('Bulk Fees'!D:D, C3, 'Bulk Fees'!E:E). K Equity Trades, typed.
L SCD TRADES, typed. M MFT Trades, typed (mutual fund and HISA trades placed
today, expected to settle next business day).
N Total Available Cash: =SUM(D3:M3) on the main rows, =SUM(D6:K6) on the
sub account rows. This is the expectation for tomorrow morning.
O Primary Contact. P Longstanding Notes. Q HISA Held in the Account (for
example DYN5006, EVF201, EVF301, TDB8153, NWI34600, PFC7701). R Target Cash.
S Potential Trade: =N3-R3. T notes on timing. U V Trading Summary override
and the shared drive paths of the source reports.

## How Jason reads it

Previous day's column N is the expected balance for this morning. Today's
column D is the actual balance this morning. The comparison is D today
against N yesterday, account by account. S is what he would trade to get
back to target R.

## Known failure modes of the file itself

1. DJD sheet empty (9 September 2026 file): the three Desjardins rows read 0
   in D, so any recon shows the full expected amount as a difference. Check
   DJD has rows before trusting those lines.
2. TradeSummary not refreshed: both the 8 and 9 September files carry the
   Period End Date 9/4/2026 summary ("Applied filters: Dates (Slicer) is
   Latest"). Column E is then the 9/4 fund flow, not the latest.
3. Hand typed K and M columns: rounded amounts (16,000,000.00 and
   9,500,000.00 on NWM110) against exact order values in SimCorp
   (15,993,924.10 for the seven NWM110 equity orders of 8 September).
4. Fund Flow columns G H I carry manual items (69,000.00 and (50,000.00) on
   NWM241 on 8 September) with no source in the file.

## Account map

The SimCorp bank account IDs follow the pattern <portfolio number> <custodian
tag> <currency> (110 AVS CAD, 120 DESJ USD). The template account numbers are
custodian account numbers. The Bulk Fees sheet ties NWM240 to 504241L1
(Nicola U.S. Equity Income Fund), which is why the template row NWM241 maps
to SimCorp NWM240_A. Every other mapping in
account_map_nicola_2026-09-09.csv rests on the opening balances of 8
September tying to the cent plus the naming. Rows that did not tie on 8
September (110 AVS CAD, 240 AVS CAD, 240 AVS USD) are mapped by naming only
and are flagged in the source column.

## Data the template has that SimCorp does not show on the same date

HISA and mutual fund trades typed in M are treated by the desk as available
next business day. In SimCorp they are orders whose payment date comes from
the fund's dealing terms and from date rolling (references/01, sections on
fund certificate cut off and rolling). On 9 September the 9,500,000.00 BNST
Corporate Tiered Investment Savings sale of NWM110 was value dated 9/10 in
the Cash Viewer while the template counted it in the 9/9 expectation.
