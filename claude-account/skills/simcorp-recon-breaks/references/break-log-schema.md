# Break log schema and reporting

The break log is the working record for a reconciliation date. Its left hand columns are the
analyst's, its right hand columns are the SimCorp export. Never rename, add or drop a column
without agreement, and never reorder the exported block, because the export is pasted in whole.

## Analyst columns

| Column | Content |
|---|---|
| Priority | P1, P2 or P3 from the priority rule |
| Classification code | One code from the taxonomy |
| Disposition code | One code from D1 to D8 |
| Owner | The role or team accountable for the fix, never an individual name on a shared deliverable |
| Raised date | The date a counterparty or configuration fix was raised |
| Resolved | Yes or No |
| Notes | The four part comment: what was reviewed, the cause, the remediation, the outcome |
| Target run | The reconciliation date on which this break is expected to clear |

## Exported columns from Results Monitor

These are the fields the current exports carry. Take them from the export rather than typing
them, so the log and SimCorp never disagree.

| Field | Why it matters |
|---|---|
| Reconciliation status | The system verdict. Never overwrite it in the log |
| Source | Which book the row came from, SimCorp or the external party |
| Reconciliation date | The date the run reconciles |
| Matching index | Groups the two sides of the same break. Sort by it or you will read one side alone |
| Break ID | Tracks the same break across dates. Emptied once the record matches |
| Break date | The first date the record failed to match. Drives the age |
| Number of days | The age, in business days when a Bank holidays setting is configured and calendar days when it is not |
| Rolled over date | The earliest date on which the record could not be matched |
| Last match date | The most recent date the record did match, where the setup stores it |
| Classification ID | The classification held in SimCorp. Must equal the log |
| Free comment | The comment held in SimCorp. Must equal the log |
| Line ID | Which reconciliation line produced the record |
| Fund or portfolio identifier | The reconciled fund, and the counterparty fund identifier where the setup carries one |
| Security identifier and name | Both sides, since a difference between them is itself a finding |
| Instrument type | A blank or wrong value is a finding, not a detail |
| Quantity, price and market value | In local and base currency where the setup carries both |
| Currency | Quotation currency and, for cash lines, the account currency |
| Account | External account number, sub account and real bank account for cash lines |
| Deactivated | Whether the external record has been removed from future runs |
| Partial re execution | Whether the result came from a partial re run rather than a full one |

## Deviation detail

Deviation details are shown in Results Monitor grouped by matching index, in absolute and
percentage terms with a grand total. How each figure is calculated depends on the field type
configured in the reconciliation rule, so read the field type before interpreting a percentage.
Percentages are calculated as the absolute deviation divided by the first source value. Fields
with no rule defined show as unique or multiple rather than as a deviation.

## Reporting cuts

Report four cuts per run, in this order.

1. Status totals: automatic match, derived match, manual match, match levels 1 through 4,
   deviation and no match, against the previous run.
2. Classification totals by code, with the movement against the previous run. This is the cut
   that says what to fix.
3. Open value: the absolute value of unmatched and deviating breaks, split by priority.
4. Ageing: the oldest open break, the count beyond the agreed age limit, and any break whose
   age is rising with an unchanged classification.

Row counts alone are not a report. A run with fewer rows and the same repeating classification
codes has not improved.
