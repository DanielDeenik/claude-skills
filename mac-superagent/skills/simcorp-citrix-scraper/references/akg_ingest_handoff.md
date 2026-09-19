# AKG / LightRAG Ingest Hand-off (Mac side)

After the Citrix extraction zip lands on your Mac, this is the canonical
ingest path into the persistent RAG knowledge graph.

## 1. Unpack to AKG data root

Per memory `project_akg_persistent_rag` + `feedback_run_from_github`, AKG
runs from `~/Documents/GitHub/akg` with venv 3.12. Ingest source dirs live
under `data/lightrag-active/`.

```bash
cd ~/Documents/GitHub/akg

# Unpack to a versioned subfolder (don't overwrite older runs)
RUN_TAG="simcorp_help_2510_$(date +%Y%m%d)"
mkdir -p data/lightrag-active/$RUN_TAG
unzip ~/Downloads/SimCorp_Help_Structured*.zip -d data/lightrag-active/$RUN_TAG/

# Sanity check
ls -lh data/lightrag-active/$RUN_TAG/
wc -l data/lightrag-active/$RUN_TAG/SimCorp_Help_Structured.csv
```

## 2. Merge with `db2.sql` field dictionary

The CSV from Citrix has help-portal narrative; merging with the offline
`SimCorp_DB_Field_Dictionary.csv` adds DDL precision.

```bash
cd ~/Documents/GitHub/akg
source .venv/bin/activate
python -c "
import pandas as pd, sys
help_path = sys.argv[1]
db_path   = '$HOME/Library/Mobile Documents/com~apple~CloudDocs/01 Work \& Business/a. Consulting - SimCorp/_SimCorp_Help_Extraction/SimCorp_DB_Field_Dictionary.csv'
out_path  = sys.argv[2]
help_df = pd.read_csv(help_path)
db_df   = pd.read_csv(db_path)
merged  = help_df.merge(
    db_df,
    left_on=['table','column'],
    right_on=['table_name','column_name'],
    how='left',
    suffixes=('_help','_db')
)
merged.to_csv(out_path, index=False)
print(f'Merged: {len(merged):,} rows × {len(merged.columns)} cols → {out_path}')
" \
data/lightrag-active/$RUN_TAG/SimCorp_Help_Structured.csv \
data/lightrag-active/$RUN_TAG/SimCorp_Help_Merged.csv
```

## 3. Trigger ingest

Per memory `project_akg_lightrag_contract`, the ingest contract requires:
- `entity_types` in `addon_params`
- `llm_model_max_async` + `embedding_func_max_async` (split from old `max_async`)

```bash
cd ~/Documents/GitHub/akg
source .venv/bin/activate
bin/akg ingest --source $RUN_TAG --workspace simcorp_help
```

Or wait for the daily `akg-rag-daily-ingest` cron at 02:00 (per memory
`feedback_reuse_existing_tasks` — don't create new scheduled tasks; the
existing slot covers this).

## 4. Verify ingest

```bash
bin/akg query --workspace simcorp_help "What does EXCIK represent in SECURITIES?"
```

Expected response should cite the description from the extracted CSV plus the
column comment from `db2.sql`, fused.

## 5. Update Notion

Per memory `project_notion_pipeline`, the Wiki should reference the new
corpus version. Push an entry to §18 sub-page noting:
- Run date
- Row count
- Portal version (2510)
- Source CSV path

## File layout after successful ingest

```
~/Documents/GitHub/akg/data/lightrag-active/simcorp_help_2510_20260515/
├── SimCorp_Help_Structured.csv         (Citrix scrape output)
├── SimCorp_Help_Merged.csv             (joined with db2.sql)
├── raw/                                (per-page .htm files)
├── _checkpoint.txt
└── _errors.log
```

And LightRAG state at `~/Documents/GitHub/akg/data/lightrag/` with the
indexed entities/relations/chunks queryable via the simcorp-super-agent skill.
