"""Copy the measured research results into the main documentation site."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'research'
dest = ROOT / 'docs/research'
assets = ROOT / 'docs/assets/experiment'
dest.mkdir(parents=True, exist_ok=True)
assets.mkdir(parents=True, exist_ok=True)

report = (source/'REPORT.md').read_text(encoding='utf-8')
report = report.replace('(MEASUREMENTS.md)', '(measurements.md)')
report = report.replace('<urlopen error _ssl.c:993: The handshake operation timed out>', 'TLS handshake timeout (доступность не подтверждена)')
(dest/'comparison.md').write_text(report, encoding='utf-8')
measurements = (source/'MEASUREMENTS.md').read_text(encoding='utf-8').replace('(REPORT.md)', '(comparison.md)')
(dest/'measurements.md').write_text(measurements, encoding='utf-8')
shutil.copytree(source/'screenshots', dest/'screenshots', dirs_exist_ok=True)

stress = (source/'mkdocs/docs/index.md').read_text(encoding='utf-8')
# Raw HTML URLs are not rewritten by MkDocs; stress is served at research/stress/.
stress = stress.replace('assets/', '../../assets/experiment/')
(dest/'stress.md').write_text(stress, encoding='utf-8')
for name in ['static.png', 'plotly.min.js', 'experiment.css', 'math-config.js']:
    shutil.copy2(source/'mkdocs/docs/assets'/name, assets/name)
# The tested formulas require the combined MathJax bundle and CHTML webfonts.
mj = source/'tools/node_modules/mathjax/es5'
(assets/'mathjax').mkdir(exist_ok=True)
shutil.copy2(mj/'tex-mml-chtml.js', assets/'mathjax/tex-mml-chtml.js')
shutil.copytree(mj/'output/chtml/fonts/woff-v2', assets/'mathjax/output/chtml/fonts/woff-v2', dirs_exist_ok=True)

downloads = dest/'data'
downloads.mkdir(exist_ok=True)
for name in ['build-metrics.json','browser-metrics.json','package-availability.json','requirements.txt']:
    shutil.copy2(source/name, downloads/name)
for name in ['data.csv','references.bib']:
    shutil.copy2(source/'shared'/name, downloads/name)
for generator in ['mkdocs','sphinx','pelican']:
    shutil.copy2(source/generator/'lighthouse.json', downloads/f'lighthouse-{generator}.json')
print('Research pages, screenshots and measured evidence copied into docs/')
