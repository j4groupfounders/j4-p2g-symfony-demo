"""Frozen project inventory and HTTP characterization; isolated faults, fail closed."""
import pathlib,json,subprocess,os,sys,time,re,hashlib,urllib.request,urllib.error,xml.etree.ElementTree as ET
P=pathlib.Path('.');E=P/'Evidence';E.mkdir(exist_ok=True);c=json.loads((P/'j4_config.json').read_text());n=c['name'];mutation=int(os.environ.get('J4_MUTATION','-1'));result={'mutation':mutation,'infrastructure':False}
def run(cmd,file,timeout=600):
 with (E/file).open('w') as f:r=subprocess.run('set -o pipefail; '+cmd,shell=True,executable='/bin/bash',stdout=f,stderr=subprocess.STDOUT,timeout=timeout)
 return r.returncode
def inventory():
 files=list((E/'junit').glob('*.xml')) if n=='sample-app' else [E/'junit.xml']
 assert files and all(f.exists() for f in files),'Missing XML: infrastructure, not detection'
 ids=[];skips=[];fails=[]
 for f in files:
  for t in ET.parse(f).getroot().iter('testcase'):
   ident=t.get('classname',t.get('class',''))+'::'+t.get('name','');ids.append(ident)
   if t.find('skipped') is not None:skips.append(ident)
   if t.find('failure') is not None or t.find('error') is not None:fails.append(ident)
 assert ids,'No project tests executed'
 return {'ids':sorted(ids),'skips':sorted(skips)},bool(fails)
def snapshots():
 class NoRedirect(urllib.request.HTTPRedirectHandler):
  def redirect_request(self,*a,**kw):return None
 op=urllib.request.build_opener(NoRedirect);rows=[]
 for route in c['routes']:
  try:r=op.open('http://127.0.0.1:8080'+route,timeout=20)
  except urllib.error.HTTPError as e:r=e
  b=r.read().decode('utf8','replace');assert r.code<500,(route,r.code,b[:200])
  b=re.sub(r'(name="(?:csrf-token|authenticity_token|_csrf_token)"[^>]*(?:content|value)=")[^"]+',r'\1<CSRF>',b)
  rows.append({'route':route,'status':r.code,'type':r.headers.get('Content-Type',''),'redirect':r.headers.get('Location'),'hash':hashlib.sha256(b.encode()).hexdigest(),'body':b})
 return rows
try:
 for lock in ['Gemfile.lock','composer.lock']:
  if (P/lock).exists():(E/lock).write_bytes((P/lock).read_bytes())
 if mutation>=0:
  m=json.loads((P/'j4_mutations.json').read_text())[mutation];f=P/m['file'];s=f.read_text();assert s.count(m['old'])==m.get('count',1),'Seed target drift';f.write_text(s.replace(m['old'],m['new']));result['fault']=m['name']
 if n=='sample-app':
  assert run('bundle exec rails db:test:prepare','db.log')==0,'Database setup failed'
  rc=run('bundle exec ruby -Itest j4_tests.rb','tests.log')
 else:rc=run('vendor/bin/phpunit --log-junit Evidence/junit.xml','tests.log')
 inv,detected=inventory();(E/'inventory.json').write_text(json.dumps(inv,indent=2));result.update(project_rc=rc,project_detected=detected)
 assert rc==0 or detected,'Test process failed without test failure: infrastructure'
 if (P/'j4-inventory.json').exists() and not detected:assert inv==json.loads((P/'j4-inventory.json').read_text()),'Test inventory changed'
 cmd=['bundle','exec','rails','server','-b','127.0.0.1','-p','8080'] if n=='sample-app' else ['php','-S','127.0.0.1:8080','-t','public','public/index.php']
 with (E/'server.log').open('w') as log:
  server=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT)
  try:
   ready=False
   for _ in range(60):
    if server.poll() is not None:raise RuntimeError('Server exited')
    try:urllib.request.urlopen('http://127.0.0.1:8080'+c['routes'][0],timeout=2);ready=True;break
    except Exception:time.sleep(1)
   assert ready,'Server did not boot'
   surface=snapshots();again=snapshots();(E/'surface.json').write_text(json.dumps(surface,indent=2));(E/'surface-repeat.json').write_text(json.dumps(again,indent=2));assert surface==again,'Unstable HTTP surface'
  finally:server.terminate();server.wait(timeout=20)
 expected=json.loads((P/'surface.json').read_text()) if (P/'surface.json').exists() else surface
 if (P/'j4-framework-changes.json').exists():
  for change in json.loads((P/'j4-framework-changes.json').read_text()):
   assert change['before'] in expected;expected[expected.index(change['before'])]=change['after']
 http_detected=surface!=expected;result.update(http_detected=http_detected,combined_detected=detected or http_detected)
 result['success']=(not detected and not http_detected) if mutation<0 else True
except Exception as e:result.update(infrastructure=True,error=str(e),success=False)
finally:
 (E/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));sys.exit(0 if result.get('success') else 1)
