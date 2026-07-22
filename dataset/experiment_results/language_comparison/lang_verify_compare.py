"""
Verify the CN-vs-EN prompt-language experiment (results_lang/) and compare.
Same extract/unitary/fidelity logic as verify_n5_full.py. Core 21 x 3 models x BV
x n=5 x {cn,en}. Outputs a standardized CSV + prints the CN vs EN comparison.
"""
import re, os, csv, math, glob
import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator
from scipy import stats

BASE = os.path.expanduser("~/Desktop/20260324 QCV量子电路视觉生成论文")
RAW = os.path.join(BASE, "results_lang")
GT_DIR = os.path.join(BASE, "quantum-circuit-vision", "dataset", "braket_code")
dev = LocalSimulator()

def clean_ansi(s):
    s=re.sub(r'\x1b\[[\d;?]*[a-zA-Z]','',s); return re.sub(r'[\x00-\x09\x0b\x0c\x0e-\x1f]','',s)
def _trunc(code):
    lines=code.split('\n'); cut=[]
    for ln in lines:
        s=ln.strip()
        if any(ch in ln for ch in '─│┌┐└┘├┤┬┴┼╌╏━┃┓┛┗┏') or s.startswith(('T :','T  :','Credits','▸','>')): break
        cut.append(ln)
    lines=cut
    while lines:
        cand='\n'.join(lines).strip()
        try:
            compile(re.sub(r'print\(.*?\)','',cand),'<c>','exec')
            if 'Circuit()' in cand: return cand
        except SyntaxError: pass
        lines.pop()
    return None
def extract_code(raw):
    gb=re.findall(r'\x1b\[38;5;10m(.*?)(?:\x1b\[0m)',raw,re.DOTALL)
    if gb:
        parts,cap=[],False
        for b in gb:
            c=clean_ansi(b).strip()
            if not c:
                if cap: parts.append('')
                continue
            if re.match(r'^\+\s*\d+$',c): continue
            if c in ('✓',) or c.startswith('/') or c.startswith('▸'): continue
            if 'from braket' in c or 'import' in c: cap=True
            if cap:
                parts.append(c)
                if re.match(r'print\s*\(',c): break
        if parts:
            code='\n'.join(parts)
            if 'Circuit' in code and 'Circuit()' in code:
                f=_trunc(code)
                if f: return f
    t=clean_ansi(raw); t=re.sub(r'^[-+]?\s*\d+[\s,]*\d*\s*[:\|]\s?','',t,flags=re.MULTILINE)
    m=re.search(r'(from braket\.circuits import Circuit.*?)(?:\n ▸|\nCreating:|\nI will|\Z)',t,re.DOTALL)
    if m: return _trunc(m.group(1).strip())
    return None
def exec_circuit(code):
    ns={"math":math,"np":np,"numpy":np}
    exec(compile(re.sub(r'print\(.*?\)','',code),'<e>','exec'),ns)
    for v in ns.values():
        if isinstance(v,Circuit): return v
    return None
def get_unitary(c):
    n=c.qubit_count; cols=[]
    for i in range(2**n):
        p=Circuit()
        for b in range(n):
            if (i>>b)&1: p.x(b)
        full=p.add_circuit(c); full.state_vector()
        cols.append(np.array(dev.run(full,shots=0).result().values[0]))
    return np.column_stack(cols)
def fidelity(a,b):
    return 0.0 if a.shape!=b.shape else abs(np.trace(a.conj().T@b))/a.shape[0]
def load_gt(name):
    p=os.path.join(GT_DIR,name+".py")
    if not os.path.exists(p): return None
    ns={"math":math,"np":np,"numpy":np}
    exec(compile(open(p).read(),p,'exec'),ns)
    for v in ns.values():
        if isinstance(v,Circuit): return v
gt_cache={}
def gt_u(name):
    if name not in gt_cache:
        c=load_gt(name); gt_cache[name]=get_unitary(c) if c is not None else None
    return gt_cache[name]

rows=[]
for fp in sorted(glob.glob(os.path.join(RAW,"*_raw.txt"))):
    m=re.match(r'(cn|en)_(claude-[a-z]+-[\d.]+)_bv_(.+)_run(\d+)_raw\.txt',os.path.basename(fp))
    if not m: continue
    lang,model,name,run=m.group(1),m.group(2),m.group(3),int(m.group(4))
    passed=False; fid=0.0; err=""
    try:
        code=extract_code(open(fp,encoding='utf-8',errors='replace').read())
        if not code: err="extract_failed"
        else:
            gen=exec_circuit(code)
            if gen is None: err="no_circuit"
            else:
                gu=gt_u(name)
                if gu is None: err="no_gt"
                else:
                    fid=fidelity(gu,get_unitary(gen)); passed=fid>=0.99
                    if not passed: err=f"fid={fid:.3f}"
    except Exception as e:
        err=f"exec:{str(e)[:40]}"
    rows.append(dict(lang=lang,model=model,circuit=name,run=run,passed=passed,fidelity=round(fid,4),error=err))

# save standardized CSV
out=os.path.join(BASE,"lang_compare_verification.csv")
with open(out,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["lang","model","circuit","run","passed","fidelity","error"])
    w.writeheader(); w.writerows(rows)
print(f"verified {len(rows)} -> {out}\n")

import statistics as st
MODELS=["claude-opus-4.6","claude-sonnet-4.6","claude-haiku-4.5"]
SH={"claude-opus-4.6":"Opus","claude-sonnet-4.6":"Sonnet","claude-haiku-4.5":"Haiku"}
def rate(lang,model=None):
    xs=[r["passed"] for r in rows if r["lang"]==lang and (model is None or r["model"]==model)]
    return 100*sum(xs)/len(xs)
print("=== CN vs EN pass rate (BV, core n=5) ===")
print(f"  {'model':8s}  CN     EN     Δ(EN-CN)")
for mdl in MODELS:
    cn=rate("cn",mdl); en=rate("en",mdl)
    print(f"  {SH[mdl]:8s} {cn:5.1f}  {en:5.1f}  {en-cn:+.1f}pp")
print(f"  {'ALL':8s} {rate('cn'):5.1f}  {rate('en'):5.1f}  {rate('en')-rate('cn'):+.1f}pp")

# paired test at (circuit x model) level: mean pass over 5 runs, CN vs EN
pairs_cn=[]; pairs_en=[]
circs=sorted(set(r["circuit"] for r in rows))
for mdl in MODELS:
    for c in circs:
        cn=[r["passed"] for r in rows if r["lang"]=="cn" and r["model"]==mdl and r["circuit"]==c]
        en=[r["passed"] for r in rows if r["lang"]=="en" and r["model"]==mdl and r["circuit"]==c]
        if cn and en:
            pairs_cn.append(sum(cn)/len(cn)); pairs_en.append(sum(en)/len(en))
d=np.array(pairs_en)-np.array(pairs_cn)
print(f"\n=== paired test (circuit x model, N={len(d)} pairs) ===")
print(f"  mean Δ(EN-CN) = {d.mean()*100:+.1f}pp")
if d.std()>0:
    t,p=stats.ttest_rel(pairs_en,pairs_cn)
    try: w,pw=stats.wilcoxon(pairs_en,pairs_cn)
    except Exception: pw=float('nan')
    print(f"  paired t: p={p:.3f}   Wilcoxon: p={pw:.3f}")
else:
    print("  no difference (all pairs identical)")
print(f"  extract_failed: {sum(1 for r in rows if r['error']=='extract_failed')}")
