import re, json, sys, glob
DDL=[f"{sys.argv[1]}", f"{sys.argv[2]}"]
FK=sys.argv[3]; CAT=sys.argv[4]; OUT=sys.argv[5]
tables={}   # name -> {desc, columns:{col:{type,comment}}, rows}
# ---- parse DDL (columns + types) ----
for fn in DDL:
    lines=open(fn,encoding="utf-8",errors="replace").read().splitlines()
    i=0; cur=None
    while i<len(lines):
        ln=lines[i]
        m=re.search(r'CREATE TABLE "SCDAT"\."([A-Z0-9_$]+)"',ln)
        if m:
            cur=m.group(1); tables.setdefault(cur,{"desc":"","columns":{},"rows":None})
            # advance to opening paren line then read columns
            j=i+1
            # find first '(' 
            while j<len(lines) and '(' not in lines[j] and 'CREATE TABLE' not in lines[j]:
                j+=1
            # now read column lines until a line that starts with ')' (closing)
            depth=0; started=False
            k=j
            while k<len(lines):
                l=lines[k]
                cm=re.match(r'\s*"([A-Z0-9_$#]+)"\s+(.+?),?\s*$', l)
                if cm and 'CONSTRAINT' not in l:
                    col=cm.group(1); typ=cm.group(2).rstrip(',').strip()
                    if col not in tables[cur]["columns"]:
                        tables[cur]["columns"][col]={"type":typ,"comment":""}
                if re.match(r'\s*\)\s*',l) and (started or '(' in lines[j]):
                    break
                if '(' in l: started=True
                k+=1
            i=k; cur=None; continue
        i+=1
# ---- comments ----
for fn in DDL:
    txt=open(fn,encoding="utf-8",errors="replace").read()
    for m in re.finditer(r'COMMENT ON TABLE "SCDAT"\."([A-Z0-9_$]+)"\s+IS \'(.*?)\';',txt,re.S):
        t=m.group(1); d=m.group(2).split('\n')[0].strip()
        if t in tables and d: tables[t]["desc"]=d
    for m in re.finditer(r'COMMENT ON COLUMN "SCDAT"\."([A-Z0-9_$]+)"\."([A-Z0-9_$#]+)"\s+IS \'(.*?)\';',txt,re.S):
        t,c,d=m.group(1),m.group(2),m.group(3).split('\n')[0].strip()
        if t in tables and c in tables[t]["columns"]: tables[t]["columns"][c]["comment"]=d
# ---- row counts ----
for m in re.finditer(r"values \('([A-Z0-9_$]+)',(\d+),",open(CAT,encoding="utf-8",errors="replace").read()):
    if m.group(1) in tables: tables[m.group(1)]["rows"]=int(m.group(2))
    else: tables.setdefault(m.group(1),{"desc":"","columns":{},"rows":int(m.group(2))})
# ---- FK edges ----
fks=[]
for m in re.finditer(r"values \('([^']*)','([^']*)','([^']*)','([^']*)','([^']*)'\)",open(FK,encoding="utf-8",errors="replace").read()):
    fks.append({"ct":m.group(1),"cc":m.group(2),"pt":m.group(3),"pc":m.group(4),"fk":m.group(5)})
index={"tables":tables,"fks":fks}
json.dump(index,open(OUT,"w"))
ncol=sum(len(t["columns"]) for t in tables.values())
print("tables:",len(tables),"| columns:",ncol,"| fk edges:",len(fks))
# spot checks
for t in ["TRANSMAIN","SECURITIES","PRICES","PRICEPROFS","PRICEDEFS","PRIKEYDEFS","PRIKEYSERVICES","AIASSETS","SECTYPES","SEGGEN"]:
    tt=tables.get(t)
    print(f"  {t:16s} present={bool(tt)} cols={len(tt['columns']) if tt else 0} rows={tt['rows'] if tt else None} desc={tt['desc'][:30] if tt else ''}")
