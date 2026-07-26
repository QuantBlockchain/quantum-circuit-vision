"""
Verify GPT cross-vendor experiment (results_gpt/) and compare.
core 21 x {gpt-5.6-sol,terra,luna} x {bv,tv} x {cn,en} x n=5 = 1260.
Same extract/unitary/fidelity pipeline. Compares to current-model Claude EN-BV
(from lang_compare_verification.csv) for a clean same-period cross-vendor contrast.
"""
import re, os, csv, math, glob
import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator
from scipy import stats

BASE = os.path.expanduser("~/Desktop/20260324 QCV量子电路视觉生成论文")
RAW = os.path.join(BASE, "results_gpt")
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
def unwrap_main(code):
    # strip markdown fences and lift circuit-building code out of def main(): wrappers
    code=re.sub(r'```[a-zA-Z]*','',code)
    lines=code.split('\n'); out=[]; indent=None; in_def=False
    for ln in lines:
        if re.match(r'[ \t]*def\s+\w+\s*\(',ln): in_def=True; indent=None; continue
        if in_def:
            if not ln.strip(): out.append(''); continue
            cur=len(ln)-len(ln.lstrip())
            if indent is None: indent=cur
            if cur<indent: in_def=False; out.append(ln); continue
            body=ln[indent:]
            if body.strip().startswith(('return','main(')): continue
            out.append(body)
        else:
            out.append(ln)
    return '\n'.join(out)

def exec_circuit(code):
    code=unwrap_main(code)
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
def fidelity(a,b): return 0.0 if a.shape!=b.shape else abs(np.trace(a.conj().T@b))/a.shape[0]
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
    m=re.match(r'(cn|en)_(gpt-5\.6-[a-z]+)_(bv|tv)_(.+)_run(\d+)_raw\.txt',os.path.basename(fp))
    if not m: continue
    lang,model,mode,name,run=m.groups()
    passed=False; fid=0.0
    try:
        code=extract_code(open(fp,encoding='utf-8',errors='replace').read())
        if code:
            gen=exec_circuit(code)
            if gen is not None:
                gu=gt_u(name)
                if gu is not None:
                    fid=fidelity(gu,get_unitary(gen)); passed=fid>=0.99
    except Exception: pass
    rows.append(dict(lang=lang,model=model,mode=mode,circuit=name,run=int(run),passed=passed,fidelity=round(fid,4)))

out=os.path.join(BASE,"results_gpt_verification.csv")
with open(out,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["lang","model","mode","circuit","run","passed","fidelity"]); w.writeheader(); w.writerows(rows)
print(f"verified {len(rows)} -> results_gpt_verification.csv\n")

GPT=["gpt-5.6-sol","gpt-5.6-terra","gpt-5.6-luna"]
SG={"gpt-5.6-sol":"Sol","gpt-5.6-terra":"Terra","gpt-5.6-luna":"Luna"}
def rate(rs): return 100*sum(r["passed"] for r in rs)/len(rs) if rs else float('nan')
def sub(lang=None,model=None,mode=None):
    return [r for r in rows if (lang is None or r["lang"]==lang) and (model is None or r["model"]==model) and (mode is None or r["mode"]==mode)]

print("=== GPT pass rate (%) by model x mode x lang ===")
print(f"  {'model':7s} | BV-cn BV-en | TV-cn TV-en")
for m in GPT:
    print(f"  {SG[m]:7s} | {rate(sub('cn',m,'bv')):5.1f} {rate(sub('en',m,'bv')):5.1f} | {rate(sub('cn',m,'tv')):5.1f} {rate(sub('en',m,'tv')):5.1f}")

print("\n=== GPT: CoT effect (BV vs TV, EN) ===")
for m in GPT:
    bv=rate(sub('en',m,'bv')); tv=rate(sub('en',m,'tv')); print(f"  {SG[m]:7s} BV {bv:.1f}  TV {tv:.1f}  Δ(TV-BV) {tv-bv:+.1f}pp")
print("=== GPT: language effect (EN vs CN, BV) ===")
for m in GPT:
    cn=rate(sub('cn',m,'bv')); en=rate(sub('en',m,'bv')); print(f"  {SG[m]:7s} CN {cn:.1f}  EN {en:.1f}  Δ(EN-CN) {en-cn:+.1f}pp")

# cross-vendor: GPT vs Claude, EN BV, current model (Claude from lang csv)
claude_csv=os.path.join(BASE,"lang_compare_verification.csv")
if os.path.exists(claude_csv):
    cr=list(csv.DictReader(open(claude_csv)))
    def crate(model): 
        xs=[c["passed"]=="True" for c in cr if c["lang"]=="en" and c["model"]==model]
        return 100*sum(xs)/len(xs) if xs else float('nan')
    print("\n=== Cross-vendor (EN, BV, core n=5, current model) ===")
    print("  GPT:   Sol {:.1f}  Terra {:.1f}  Luna {:.1f}".format(rate(sub('en','gpt-5.6-sol','bv')),rate(sub('en','gpt-5.6-terra','bv')),rate(sub('en','gpt-5.6-luna','bv'))))
    print("  Claude: Opus {:.1f}  Sonnet {:.1f}  Haiku {:.1f}".format(crate('claude-opus-4.6'),crate('claude-sonnet-4.6'),crate('claude-haiku-4.5')))

# difficulty gradient (GPT, EN BV) by prefix
def tier(n): return 'basic' if n.startswith('demo') else 'intermediate' if n.startswith('inter') else 'advanced'
print("\n=== GPT difficulty gradient (EN BV, all 3 GPT pooled) ===")
for t in ['basic','intermediate','advanced']:
    rs=[r for r in sub('en',None,'bv') if tier(r['circuit'])==t]; print(f"  {t:12s} {rate(rs):.1f}%")
