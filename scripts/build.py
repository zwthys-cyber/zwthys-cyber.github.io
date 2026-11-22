"""Build the static catalog on GitHub; no third-party dependencies."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json, os, shutil, urllib.request, urllib.error

OWNER = 'zwthys-cyber'
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / '_site'
TOKEN = os.environ.get('GITHUB_TOKEN', '')

def api(path):
    headers={'Accept':'application/vnd.github+json','User-Agent':'zwthys-project-center'}
    if TOKEN: headers['Authorization']='Bearer '+TOKEN
    request=urllib.request.Request('https://api.github.com/'+path,headers=headers)
    try:
        with urllib.request.urlopen(request,timeout=20) as response:return json.load(response)
    except urllib.error.HTTPError as error:
        if error.code==404:return None
        raise

def category(name):
    if name in ['ccpocket','TethrX','con-terminal','ghostty']:return 'ai'
    if name in ['Xiaote','TeslaBLEKeyKit','teslamate','Tesla-UI-prototype','teslamate-chinese-dashboards']:return 'tesla'
    if name in ['DouyinAntiRecall','qq-anti-recall-ios','ipa-decrypt-lab','Telegram-iOS','WQFiles','ios26-gestalt-check','x-creator-studio-zh','AirCard-iOS']:return 'ios'
    return 'network'

def project(repo):
    result={'name':repo['name'],'description':repo.get('description') or '', 'url':repo['html_url'],'language':repo.get('language'),'fork':repo['fork'],'updated_at':repo['updated_at'],'category':category(repo['name']),'release':None}
    try:
        release=api('repos/'+OWNER+'/'+repo['name']+'/releases/latest')
        if release:
            assets=[{'name':a['name'],'url':a['browser_download_url'],'size':a['size']} for a in release.get('assets',[]) if a.get('state')=='uploaded']
            result['release']={'tag':release['tag_name'],'url':release['html_url'],'published_at':release['published_at'],'assets':assets}
    except (urllib.error.URLError,TimeoutError):
        print('Release metadata unavailable for '+repo['name']+'; preserving source link.')
    return result

repos=api('users/'+OWNER+'/repos?per_page=100&sort=updated')
assert isinstance(repos,list),'Repository catalog request failed'
repos=[r for r in repos if not r.get('private') and r['name'] not in [OWNER+'.github.io','.github']]
with ThreadPoolExecutor(max_workers=4) as pool:projects=list(pool.map(project,repos))
assert len(projects)>1,'Expected a multi-project catalog'
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir()
for name in ['index.html','styles.css','app.js','favicon.svg']:shutil.copy2(ROOT/name,OUT/name)
(OUT/'.nojekyll').touch()
(OUT/'data').mkdir()
(OUT/'data/projects.json').write_text(json.dumps({'updated_at':datetime.now(timezone.utc).isoformat(),'projects':projects},ensure_ascii=False,indent=2)+'\n')
print('Built public catalog: '+str(len(projects))+' projects, '+str(sum(bool(p['release'] and p['release']['assets']) for p in projects))+' projects with release assets.')
