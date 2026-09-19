# Output CSV Schema — 23 columns

The structured output CSV at `Documents\SimCorp_Help_Structured\SimCorp_Help_Structured.csv`
matches the schema defined in `CITRIX_RUNBOOK_full_corpus.md`. Each row
represents one page from `help.simcorpcloud.com/2510/en/`.

## Column reference

| # | Column | Type | Populated for | Source / regex |
|---|--------|------|---------------|----------------|
| 1 | `namespace` | string | All | URL path segment after `/Content/` |
| 2 | `url_path` | string | All | Full URL |
| 3 | `title` | string | All | `<title>` element |
| 4 | `kind` | enum | All | Derived from URL: `Table_Summary`, `Tier2_TableField`, `Tier1_Field`, `Form`, `View`, `Formula`, `Command`, `ReleaseNote`, `Main_Narrative` |
| 5 | `table` | string | Tier2, Table_Summary | `Database (field \| table) X` H1 capture |
| 6 | `column` | string | Tier2 | `Database field X in table Y` first capture |
| 7 | `dbtype` | string | Tier2 | `Database type: X` capture |
| 8 | `internal_width` | int | Tier2 | `Internal max. width ... : N` capture |
| 9 | `nullable` | enum | Tier2 | `NOT NULL (always)` \| `NOT NULL (partly)` |
| 10 | `fk_to` | string | Tier2 | `internal key reference to X` capture |
| 11 | `domain` | string | Table_Summary, Tier2 | `Table Group: X` (Table_Summary) or `of domain X` (Tier2) |
| 12 | `dwh_views` | string | Tier2 | `Found in view(s):` block; joined by `; ` |
| 13 | `editor_list_identifier` | string | Tier1 | EditorList identifier — pending Tier-1 JS-render solution |
| 14 | `editor_list_name` | string | Tier1 | EditorList short name — pending |
| 15 | `am_field_tooltip` | string | Tier1 | AM tooltip — pending |
| 16 | `category` | string | Table_Summary | `Sub-Table Group: X` capture |
| 17 | `is_key` | enum | Tier2 | `YES` if `internal key reference` matched |
| 18 | `access` | enum | Tier1 | `Input` \| `Output` \| `Both` \| `Read-only` — pending |
| 19 | `formatter` | string | Tier1 | Format type description — pending |
| 20 | `help_topic_raw` | string | Tier2 | `General help for the Table X` → `Table:X` |
| 21 | `description` | string | All | Prose block from `Description` section or first paragraphs |
| 22 | `build_date` | string | All | `Build: <date> at <time>` capture |
| 23 | `source_file` | string | All | Relative path to saved raw `.htm` under `raw/` |

## Population matrix (which fields per kind)

| Kind | Populated columns |
|------|-------------------|
| `Tier2_TableField` | namespace, url_path, title, kind, **table, column, dbtype, internal_width, nullable, fk_to, dwh_views, description, build_date**, source_file, (sometimes is_key, domain, help_topic_raw) |
| `Table_Summary` | namespace, url_path, title, kind, **table, domain (Table Group), category (Sub-Table Group), description, build_date**, source_file |
| `Tier1_Field` | namespace, url_path, title, kind, source_file (rest pending Tier-1 JS-render solution) |
| `Form` / `View` / `Formula` / `Command` / `ReleaseNote` / `Main_Narrative` | namespace, url_path, title, kind, description, build_date, source_file |

## CSV escaping

Values containing commas, quotes, or newlines are wrapped in double quotes;
inner quotes doubled per CSV standard:

```csv
TableFields,https://.../Field-190.htm,EXCIK,Tier2_TableField,SECURITIES,EXCIK,NUMBER(5),5,NOT NULL (partly),EXCHANGES,,A_EQUITIES.EXCHANGE; A_SECS.EXCHANGE,,,,,,YES,,,,"This field contains a reference to an exchange. Some securities can be quoted on several exchanges, in this case the alternative exchanges are stored in a separate table.",01/05/2026 11:59,raw/Table-1-Field-190.htm
```

## Joining with `db2.sql` dictionary

The 49,198-row `SimCorp_DB_Field_Dictionary.csv` joins on `(table_name, column_name)`:

```python
import pandas as pd
help_df = pd.read_csv('SimCorp_Help_Structured.csv')
db_df   = pd.read_csv('SimCorp_DB_Field_Dictionary.csv')
merged = help_df.merge(
    db_df,
    left_on=['table','column'],
    right_on=['table_name','column_name'],
    how='left',
    suffixes=('_help','_db')
)
```

The merged frame has both help-portal narrative (description, dwh_views,
fk_to) and DDL precision (data_type, length, nullable, table_comment,
column_comment).
