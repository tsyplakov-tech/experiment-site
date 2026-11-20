from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]/'research'
b=json.loads((R/'build-metrics.json').read_text(encoding='utf-8'))
a=json.loads((R/'browser-metrics.json').read_text(encoding='utf-8'))
lines=['# P2. Измеренные результаты','', 'Единица КБ = 1000 байт. Время — медиана трёх запусков. Подробный протокол и ограничения — в [REPORT.md](REPORT.md).','', '| Генератор | Чистая сборка, с | Повторная после правки, с | HTML, КБ | Ресурсы страницы desktop, КБ | Каталог сборки, КБ | Внешние запросы desktop/mobile | Lighthouse P/A/BP/SEO | Mobile 390px |','|---|---:|---:|---:|---:|---:|---|---|---|']
for name in ['mkdocs','sphinx','pelican']:
    v=b[name]; d=a[name]['desktop']; m=a[name]['mobile']; c=m['checks']; lh=a[name].get('lighthouse',{})
    score='/'.join(str(round(lh[k]*100)) if isinstance(lh.get(k),(int,float)) else 'N/A' for k in ['performance','accessibility','best-practices','seo'])
    mobile='OK' if c['documentWidth']<=c['width'] and not c['brokenImages'] and not c.get('mathErrors') and not m['errors'] else 'Проблемы — см. JSON'
    lines.append(f"| {name} | {v['cold_median']:.3f} | {v['incremental_median']:.3f} | {v['html_bytes']/1000:.1f} | {d['resource_bytes']/1000:.1f} | {v['site_bytes']/1000:.1f} | {d['external_requests']}/{m['external_requests']} | {score} | {mobile}; grid {c['columns']} |")
lines+=['','P/A/BP/SEO: производительность, доступность, лучшие практики, поисковая оптимизация. Lighthouse не проверяет научную корректность. Mobile OK означает отсутствие горизонтального переполнения документа, ошибок JS/MathJax и сломанных изображений; визуальный просмотр дополняет эту проверку.','', '## Скриншоты','']
for name in ['mkdocs','sphinx','pelican']:
    lines += [f'### {name}', '', f'![Desktop {name}](screenshots/{name}-desktop.png)', '', f'![Mobile {name}](screenshots/{name}-mobile.png)', '']
(R/'MEASUREMENTS.md').write_text('\n'.join(lines),encoding='utf-8')
print('\n'.join(lines[:10]))
