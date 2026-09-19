#!/usr/bin/env python3
"""Ad-hoc schema lookup against schema_index.json — replaces guessing / the Fields picker.
Usage:
  resolve.py table  <TABLE>        show a table: description, rows, every column + type + comment
  resolve.py column <TOKEN>        find columns whose name OR comment matches TOKEN (which tables)
  resolve.py fk     <TABLE>        all FK edges out of and into TABLE (real join keys)
  resolve.py find   <KEYWORD>      tables whose description matches KEYWORD
"""
import json,sys,re
IDX=json.load(open("schema_index.json")); T=IDX["tables"]; FKS=IDX["fks"]
cmd=sys.argv[1]; arg=sys.argv[2]
if cmd=="table":
    t=arg.upper()
    if t not in T: 
        print("NOT FOUND. did you mean:", [x for x in T if arg.upper() in x][:10]); sys.exit()
    print(f"{t} — {T[t]['desc']} (rows={T[t]['rows']}, {len(T[t]['columns'])} cols)")
    for c,v in T[t]["columns"].items(): print(f"  {c:24s} {v['type']:18s} {v['comment']}")
elif cmd=="column":
    tok=arg.lower()
    for t,v in T.items():
        for c,cv in v["columns"].items():
            if tok in c.lower() or tok in cv["comment"].lower():
                print(f"  {t}.{c}  [{cv['type']}]  {cv['comment']}")
elif cmd=="fk":
    t=arg.upper()
    print(f"OUT of {t} (this table's join keys to parents):")
    for f in FKS:
        if f["ct"]==t: print(f"  {f['ct']}.{f['cc']} -> {f['pt']}.{f['pc']}  ({f['fk']})")
    print(f"INTO {t} (children that join to it):")
    for f in FKS:
        if f["pt"]==t: print(f"  {f['ct']}.{f['cc']} -> {f['pt']}.{f['pc']}  ({f['fk']})")
elif cmd=="find":
    for t,v in T.items():
        if arg.lower() in v["desc"].lower(): print(f"  {t:24s} {v['desc']} (rows={v['rows']})")
