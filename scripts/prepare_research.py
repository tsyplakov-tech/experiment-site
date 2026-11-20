"""Generate three equivalent scientific stress pages from shared data."""
from pathlib import Path
import shutil, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.offline import get_plotlyjs
from pybtex.database import parse_file
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

ROOT = Path(__file__).resolve().parents[1]
R = ROOT/'research'
def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

bib = '''@book{taylor1997,
author = {Taylor, John R.},
title = {An Introduction to Error Analysis},
year = {1997},
publisher = {University Science Books}
}
'''
write(R/'shared/references.bib', bib)
entry = parse_file(R/'shared/references.bib').entries['taylor1997']
reference = f"Taylor, John R. ({entry.fields['year']}). {entry.fields['title']}. {entry.fields['publisher']}."
x = [1,2,3,4,5]; y = [1.1,1.9,3.2,3.9,5.1]
write(R/'shared/data.csv', 'x,y\n'+''.join(f'{a},{b}\n' for a,b in zip(x,y)))
plt.figure(figsize=(6,3)); plt.plot(x,y,'o-',label='Наблюдения'); plt.xlabel('x'); plt.ylabel('y'); plt.grid(); plt.tight_layout()
(R/'shared').mkdir(exist_ok=True)
plt.savefig(R/'shared/static.png',dpi=140); plt.close()
fig = go.Figure(go.Scatter(x=x,y=y,mode='lines+markers'))
fig.update_layout(title='Интерактивные наблюдения',autosize=True,height=320,margin=dict(l=40,r=20,t=50,b=40))
plot = fig.to_html(full_html=False,include_plotlyjs=False,div_id='experiment-plot',config={'responsive':True,'displaylogo':False})
css = '''img{max-width:100%;height:auto} .experiment-columns{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;align-items:center} table{border-collapse:collapse;width:100%}td,th{border:1px solid #8796a5;padding:.5rem}caption{font-weight:bold;padding:.5rem}.plotly-graph-div{max-width:100%} .highlight{overflow:auto} @media(max-width:700px){.experiment-columns{grid-template-columns:1fr}} @media print{nav,.sphinxsidebar{display:none}.experiment-columns{display:block}}'''+HtmlFormatter().get_style_defs('.highlight')
code = 'import numpy as np\ny = np.array([1.1, 1.9, 3.2, 3.9, 5.1])\nmean = y.mean()\nprint(mean)\n'
table = '''<table id="results-table"><caption>Таблица 1. Результаты измерений</caption><thead><tr><th rowspan="2" scope="col">Серия</th><th colspan="2" scope="colgroup">Отклик</th></tr><tr><th scope="col">Среднее</th><th scope="col">Погрешность</th></tr></thead><tbody><tr><th scope="row">A</th><td>3.04</td><td>0.10</td></tr><tr><th scope="row">B</th><td>3.00</td><td>0.12</td></tr></tbody></table>'''
for name in ['mkdocs','sphinx','pelican']:
    src = R/name/('content' if name=='pelican' else 'docs')
    assets = src/('assets' if name!='sphinx' else '_static')
    assets.mkdir(parents=True,exist_ok=True)
    shutil.copy(R/'shared/static.png',assets/'static.png')
    write(assets/'plotly.min.js',get_plotlyjs())
    write(assets/'experiment.css',css)
    mj=R/'tools/node_modules/mathjax/es5'
    if mj.exists(): shutil.copytree(mj,assets/'mathjax',dirs_exist_ok=True)
    shutil.copy(R/'shared/references.bib',src/'references.bib')
    a = '_static' if name=='sphinx' else 'assets'
    body = f'''# Погрешность измерений: стресс-тест

## Методика {{#method}}

Пять наблюдений одной серии. Оценка среднего описана в [Taylor, 1997](#ref-taylor1997). Методика повторяется в разделе [Результаты](#results). Погрешность здесь иллюстративная[^note].

<div id="eq-mean">\\[\\begin{{equation}}\\bar{{y}}=\\frac{{1}}{{n}}\\sum_{{i=1}}^n y_i \\label{{eq:mean}}\\end{{equation}}\\]</div>

Среднее вычисляется по уравнению \\(\\eqref{{eq:mean}}\\).

## Результаты {{#results}}

{table}

<div class="experiment-columns"><div><h3>Интерпретация</h3><p>Рост отклика близок к линейному. Статический график справа построен matplotlib по тем же пяти точкам, что и интерактивный график ниже.</p></div><figure><img src="{a}/static.png" alt="График пяти измерений: отклик линейно растёт"><figcaption>Рисунок 1. Наблюдения</figcaption></figure></div>

<script src="{a}/plotly.min.js"></script>
{plot}

## Вычисление

{highlight(code,PythonLexer(),HtmlFormatter(linenos='table'))}

[^note]: Это учебный пример, а не оценка точности прибора.

## Литература

<div id="ref-taylor1997">{reference}</div>
'''
    if name=='sphinx':
        body=body.replace('## Методика {#method}','(method)=\n## Методика').replace('## Результаты {#results}','(results)=\n## Результаты')
        body=body.replace('[Taylor, 1997](#ref-taylor1997)','{cite:p}`taylor1997`')
        start=body.index('<div id="eq-mean">'); end=body.index('## Результаты') if '## Результаты' in body else 0
        body=body[:start]+'''```{math}
:label: eq-mean
\\bar{y}=\\frac{1}{n}\\sum_{i=1}^n y_i
```

Среднее вычисляется по уравнению {eq}`eq-mean`.

(results)=
'''+body[end:]
        body=body[:body.index('<div id="ref-taylor1997">')]+'''```{bibliography}
```
'''
    else:
        body=body.replace('## Методика {#method}','<h2 id="method">Методика</h2>').replace('## Результаты {#results}','<h2 id="results">Результаты</h2>')
    if name=='pelican': body='Title: Погрешность измерений: стресс-тест\nDate: 2026-11-20\nSlug: stress\n\n'+body
    write(src/('stress.md' if name=='pelican' else 'index.md'),body)

write(R/'mkdocs/mkdocs.yml','''site_name: Научный стресс-тест
docs_dir: docs
site_dir: ../../research/output/mkdocs
theme:
  name: material
  language: ru
  font: false
plugins:
  - search:
      lang: [ru]
markdown_extensions:
  - footnotes
  - md_in_html
extra_css: [assets/experiment.css]
extra_javascript:
  - assets/math-config.js
  - assets/mathjax/tex-mml-chtml.js
''')
mathconfig="window.MathJax={tex:{tags:'ams',inlineMath:[['\\\\(','\\\\)']]}};"
write(R/'mkdocs/docs/assets/math-config.js',mathconfig)
write(R/'pelican/content/assets/math-config.js',mathconfig)
write(R/'sphinx/docs/conf.py', '''project='Научный стресс-тест'
extensions=['myst_parser','sphinx.ext.mathjax','sphinx_design','sphinxcontrib.bibtex']
language='ru'
html_theme='alabaster'
html_static_path=['_static']
html_css_files=['experiment.css']
html_js_files=[]
mathjax_path='mathjax/tex-mml-chtml.js'
bibtex_bibfiles=['references.bib']
bibtex_default_style='plain'
numfig=True
exclude_patterns=[]
''')
write(R/'pelican/pelicanconf.py', '''AUTHOR='Исследователь'
SITENAME='Научный стресс-тест'
SITEURL=''
TIMEZONE='Europe/Moscow'
DEFAULT_LANG='ru'
PATH='content'
THEME='theme'
STATIC_PATHS=['assets']
ARTICLE_URL='index.html'
ARTICLE_SAVE_AS='index.html'
INDEX_SAVE_AS='listing.html'
FEED_ALL_ATOM=None
CATEGORY_FEED_ATOM=None
TRANSLATION_FEED_ATOM=None
AUTHOR_FEED_ATOM=None
AUTHOR_FEED_RSS=None
MARKDOWN={'extensions':['markdown.extensions.extra','markdown.extensions.codehilite'], 'output_format':'html5'}
''')
write(R/'pelican/theme/templates/article.html','''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{{ article.title }}</title><link rel="stylesheet" href="assets/experiment.css"><style>body{font:18px/1.65 system-ui;margin:auto;padding:24px;max-width:1000px;color:#203044}h1,h2{line-height:1.2}</style><script src="assets/math-config.js"></script><script defer src="assets/mathjax/tex-mml-chtml.js"></script></head><body><main>{{ article.content }}</main></body></html>''')
for template in ['index','archives','categories','tags','authors','author','category','tag','period_archives']:
    write(R/f'pelican/theme/templates/{template}.html','<!doctype html><html lang="ru"><title>Стресс-тест</title><a href="index.html">Стресс-тест</a></html>')
print('Sources generated')
