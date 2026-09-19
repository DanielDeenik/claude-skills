# PoC Success Signature

After running `scripts/02_poc_single_page.ps1` (F5 in ISE Script Pane), STEP 4
of its output MUST show this exact shape to confirm the pipeline works
end-to-end. If any of the **bolded** fields are missing or empty, the parser
needs adjustment per `references/parser_patterns.md`.

## Expected STEP 4 output (against EXCIK in SECURITIES)

```
=== STEP 4: Structured row (only populated fields) ===
  build_date           01/05/2026 11:59
  column               EXCIK
  dbtype               NUMBER(5)
  description          This field contains a reference to an exchange. Some securities can be quoted on several exchanges, in this case the alternative exchanges are stored in a separate table.
  dwh_views            A_EQUITIES.EXCHANGE; A_SECS.EXCHANGE; A_SECS.EXCHANGE_REF; DR_SD_SECURITIES.EXCHANGE_ID
  fk_to                EXCHANGES
  internal_width       5
  is_key               YES
  kind                 Tier2_TableField
  namespace            TableFields
  nullable             NOT NULL (partly)
  table                SECURITIES
  title                EXCIK
  url_path             https://help.simcorpcloud.com/2510/en/Content/TableFields/Table-1%20Field-190.htm
```

## Validation checklist

- [ ] `column` = `EXCIK`
- [ ] `table` = `SECURITIES`
- [ ] `dbtype` = `NUMBER(5)`
- [ ] `internal_width` = `5`
- [ ] `nullable` = `NOT NULL (partly)`
- [ ] `fk_to` = `EXCHANGES`
- [ ] `is_key` = `YES`
- [ ] `dwh_views` contains `A_EQUITIES.EXCHANGE` and 3 others, joined by `; `
- [ ] `description` non-empty, contains substring `reference to an exchange`
- [ ] `build_date` non-empty, in format `dd/mm/yyyy hh:mm`

## STEP 5 + 6 output

CSV must round-trip through Set-Content and Get-Content cleanly:

```
=== STEP 5: Write CSV ===
  Wrote C:\Users\<user>\Documents\SimCorp_Help_Structured\PoC_single_row.csv

=== STEP 6: Read CSV back ===
  namespace,url_path,title,kind,table,column,dbtype,internal_width,nullable,fk_to,domain,dwh_views,editor_list_identifier,editor_list_name,am_field_tooltip,category,is_key,access,formatter,help_topic_raw,description,build_date,source_file
  TableFields,https://help.simcorpcloud.com/2510/en/Content/TableFields/Table-1%20Field-190.htm,EXCIK,Tier2_TableField,SECURITIES,EXCIK,NUMBER(5),5,NOT NULL (partly),EXCHANGES,,A_EQUITIES.EXCHANGE; A_SECS.EXCHANGE; A_SECS.EXCHANGE_REF; DR_SD_SECURITIES.EXCHANGE_ID,,,,,YES,,,,"This field contains a reference to an exchange. Some securities can be quoted on several exchanges, in this case the alternative exchanges are stored in a separate table.",01/05/2026 11:59,raw/Table-1-Field-190.htm
```

The description prose is wrapped in `"..."` because it contains commas — CSV
escaping is working.

## If PoC fails

Stop. Do NOT proceed to the production-block paste. Diagnose per
`references/parser_patterns.md` "When patterns break" section.
