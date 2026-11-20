"""Reproducible clean-output and one-file-change builds (three repetitions)."""
from pathlib import Path
import subprocess,sys,time,shutil,json,statistics,platform,importlib.metadata
R=Path(__file__).resolve().parents[1]/'research'
out=R/'output'; out.mkdir(exist_ok=True)
commands={
 'mkdocs': [sys.executable,'-m','mkdocs','build','-f',str(R/'mkdocs/mkdocs.yml')],
 'sphinx': [sys.executable,'-m','sphinx','-b','html',str(R/'sphinx/docs'),str(out/'sphinx')],
 'pelican':[sys.executable,'-m','pelican','content','-s','pelicanconf.py','-o',str(out/'pelican')],
}
results={}
for name,cmd in commands.items():
    timings={'cold':[],'incremental':[]}
    for i in range(3):
        target=out/name
        if target.exists(): shutil.rmtree(target)
        for mode in timings:
            src=R/name/('content/stress.md' if name=='pelican' else 'docs/index.md')
            original=src.read_text(encoding='utf-8')
            if mode=='incremental': src.write_text(original+'\n<!-- incremental edit -->\n',encoding='utf-8')
            t=time.perf_counter()
            p=subprocess.run(cmd,cwd=R/name,capture_output=True)
            elapsed=time.perf_counter()-t
            (R/f'{name}-{mode}.log').write_bytes(p.stdout+p.stderr)
            if mode=='incremental': src.write_text(original,encoding='utf-8')
            if p.returncode: raise RuntimeError(f'{name}: see build log')
            timings[mode].append(round(elapsed,4))
    results[name]={**timings,'cold_median':statistics.median(timings['cold']),'incremental_median':statistics.median(timings['incremental']),'html_bytes':(out/name/'index.html').stat().st_size,'site_bytes':sum(p.stat().st_size for p in (out/name).rglob('*') if p.is_file())}
results['_environment']={'platform':platform.platform(),'python':sys.version,'versions':{p:importlib.metadata.version(p) for p in ['mkdocs','mkdocs-material','sphinx','myst-parser','pelican','plotly','matplotlib']},'method':'clean output, warm OS/package cache; incremental edits one page, fresh CLI process; excludes prepare_research.py'}
(R/'build-metrics.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
