import json,re,sys,difflib
IDX=json.load(open(sys.argv[1]))
T=IDX["tables"]; FKS=IDX["fks"]
# indexes
COLS_BY_TABLE={t:set(v["columns"]) for t,v in T.items()}
TABLES_BY_COL={}
for t,v in T.items():
    for c in v["columns"]: TABLES_BY_COL.setdefault(c,set()).add(t)
FK_SET=set((f["ct"],f["cc"],f["pt"],f["pc"]) for f in FKS)
FK_BY_CHILD={}
for f in FKS: FK_BY_CHILD.setdefault((f["ct"],f["cc"]),[]).append((f["pt"],f["pc"]))

def norm_field(raw):
    cands=[raw.upper(), re.sub(r'^[a-z]+','',raw).upper(), re.sub(r'^[a-z]','',raw).upper()]
    seen=[]; 
    for c in cands:
        if c and c not in seen: seen.append(c)
    return seen

def resolve_table(raw):
    u=raw.upper()
    if u in T: return u,"exact"
    # description / name search
    cands=[t for t in T if u in t]  # substring in name
    if not cands:
        # search descriptions
        cands=[t for t,v in T.items() if raw.lower() in v["desc"].lower()][:8]
    close=difflib.get_close_matches(u,list(T),n=5,cutoff=0.6)
    cands=list(dict.fromkeys(cands+close))[:8]
    return None,cands

def check_field(table,raw):
    if table not in T: return ("TABLE_MISSING",None,[])
    cols=COLS_BY_TABLE[table]
    for c in norm_field(raw):
        if c in cols: return ("OK",c,[])
    # where does it live?
    elsewhere=[]
    for c in norm_field(raw):
        if c in TABLES_BY_COL: elsewhere=sorted(TABLES_BY_COL[c])[:6]; break
    return ("FIELD_NOT_ON_TABLE",None,elsewhere)

def check_join(ct,cc,pt,pc):
    ct,pt=ct.upper(),pt.upper()
    for cn in norm_field(cc):
        for pn in norm_field(pc):
            if (ct,cn,pt,pn) in FK_SET: return ("VERIFIED_FK",f"{ct}.{cn}->{pt}.{pn}")
    # child col has *some* FK?
    for cn in norm_field(cc):
        if (ct,cn) in FK_BY_CHILD:
            tgts=FK_BY_CHILD[(ct,cn)]
            return ("FK_TO_OTHER",f"{ct}.{cn} FKs to {tgts[:3]}")
    # IK naming heuristic
    for cn in norm_field(cc):
        if cn.endswith("IK") and pt in T and cn in COLS_BY_TABLE.get(pt,()):
            return ("IK_MATCH",f"{ct}.{cn} matches {pt}.{cn} by IK name (no declared FK)")
    return ("UNVERIFIED","no FK edge and no IK match")

def rows(t): 
    return T[t]["rows"] if t in T else None

design=json.load(open(sys.argv[2]))
print("# DEX Design Validation Report —",design["name"])
print("Schema: 5,781 tables / 84,020 cols / 19,749 FK edges (SCDAT 25.10 dump)\n")
for e in design["extractions"]:
    print("="*70); print(f"{e['id']} — {e['title']}")
    for tb in e["tables"]:
        rt,info=resolve_table(tb)
        if rt:
            r=rows(rt); d=T[rt]["desc"]
            print(f"  [TABLE OK]   {tb:16s} -> {rt}  ({len(COLS_BY_TABLE[rt])} cols, rows={r})  {d}")
            if r==0: print(f"               ^ EMPTY-RESULT RISK: 0 rows in this dump")
        else:
            print(f"  [TABLE ????] {tb:16s} NOT FOUND. candidates: {info}")
    for (tb,fld) in e.get("fields",[]):
        rt,_=resolve_table(tb)
        if not rt: 
            print(f"  [FIELD skip] {tb}.{fld} (table unresolved)"); continue
        st,real,elsewhere=check_field(rt,fld)
        if st=="OK": print(f"  [FIELD OK]   {rt}.{fld} -> {real}")
        else: print(f"  [FIELD BAD]  {rt}.{fld} NOT on {rt}. lives on: {elsewhere or 'unknown'}")
    for j in e.get("joins",[]):
        st,info=check_join(*j)
        tag={"VERIFIED_FK":"JOIN OK  ","FK_TO_OTHER":"JOIN WARN","IK_MATCH":"JOIN ~ok ","UNVERIFIED":"JOIN ????"}[st]
        print(f"  [{tag}] {j[0]}.{j[1]} = {j[2]}.{j[3]}  :: {st} :: {info}")
    for blk in e.get("blocked",[]):
        print(f"  [BLOCKED]    {blk}")
