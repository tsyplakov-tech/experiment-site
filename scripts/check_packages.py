"""Record registry release dates and one explicitly named mirror's availability."""
from pathlib import Path
from urllib.request import urlopen,Request
from datetime import datetime,timezone
import json
result={'checked_at':datetime.now(timezone.utc).isoformat(),'packages':{}}
for name in ['mkdocs','mkdocs-material','sphinx','myst-parser','pelican']:
    row={}
    for label,url in [('pypi',f'https://pypi.org/pypi/{name}/json'),('mirror',f'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/{name}/')]:
        try:
            with urlopen(Request(url,headers={'User-Agent':'ScientificSiteComparison/1.0'}),timeout=12) as response:
                row[label]={'url':url,'status':response.status}
                if label=='pypi':
                    data=json.load(response);version=data['info']['version']
                    row[label].update(version=version,release_dates=[f['upload_time_iso_8601'] for f in data['releases'].get(version,[])])
                else: row[label]['index_sample_bytes']=len(response.read(4096))
        except Exception as exc: row[label]={'url':url,'error':str(exc)}
    result['packages'][name]=row
Path('research/package-availability.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Registry checks saved')
