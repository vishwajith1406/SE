"""Local two-studio Finance Requirements Portal, inspired by the reference flow."""
import hashlib, json, os, re, secrets, sqlite3, zipfile
from http import cookies
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from mimetypes import guess_type
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from docx_export import write_docx
from financial_engine import srs_reply, srs_sections, sdlc_report

ROOT=Path(__file__).parent; OUT=ROOT/'outputs'; OUT.mkdir(exist_ok=True); DB=ROOT/'finance_portal.db'; SESS={}
def conn():
    c=sqlite3.connect(DB); c.execute('create table if not exists users (username text primary key, password text not null)'); return c
def pw(v): return hashlib.sha256(v.encode()).hexdigest()
def page(title, body, user=None):
    nav='<a href="/platform/">Agentic Platform</a><a href="/srs">SRS Studio</a><a href="/sdlc">SDLC Studio</a>' if user else ''
    auth=f'<span>{user}</span> <a href="/logout">Sign out</a>' if user else '<a href="/login">Sign in</a> <a class="button" href="/signup">Create account</a>'
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} | FinReq AI</title><style>
    :root{{--nav:#10203b;--blue:#356fe5;--ink:#17233b;--muted:#64748b;--line:#e3e9f2;--bg:#f5f7fb;--green:#0d7b5c}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px system-ui,Segoe UI,sans-serif}}header{{background:var(--nav);color:white;padding:15px max(5vw,25px);display:flex;gap:25px;align-items:center}}header strong{{font-size:19px}}header nav{{display:flex;gap:17px;flex:1}}a{{color:#3266ca;text-decoration:none}}header a{{color:#dce9ff}}.button,button{{background:var(--blue);border:0;border-radius:7px;color:white;padding:9px 13px;font:inherit;font-weight:650;cursor:pointer}}button.secondary,.button.secondary{{background:white;color:var(--ink);border:1px solid var(--line)}}main{{max-width:1060px;margin:32px auto;padding:0 20px}}h1{{margin:0 0 7px;font-size:27px}}h2{{font-size:17px}}.sub,.help{{color:var(--muted)}}.card{{background:#fff;border:1px solid var(--line);border-radius:10px;padding:20px;margin:17px 0;box-shadow:0 1px 2px #11224409}}.grid{{display:grid;grid-template-columns:220px 1fr;gap:17px}}textarea,input{{width:100%;padding:10px;border:1px solid #d6dfed;border-radius:7px;font:inherit}}textarea{{min-height:110px}}label{{font-weight:700;font-size:12px;display:block;margin-bottom:7px}}.turn{{padding:12px;border-radius:8px;margin:9px 0;white-space:pre-wrap}}.user{{background:#eaf1ff}}.assistant{{background:#f6f8fb;border:1px solid var(--line)}}.role{{font-size:11px;font-weight:800;text-transform:uppercase;display:block;color:#526a94;margin-bottom:4px}}.actions{{display:flex;gap:9px;margin-top:10px;flex-wrap:wrap}}.notice{{background:#fff7df;color:#815a0d;border:1px solid #f2ddaa;padding:12px;border-radius:7px}}.status{{min-height:20px;color:#0b7759;margin-top:9px}}.report{{white-space:pre-wrap;line-height:1.55;background:#f8faff;padding:14px;border-radius:7px}}.error{{color:#b42338}}@media(max-width:700px){{.grid{{grid-template-columns:1fr}}header{{flex-wrap:wrap}}}}</style></head><body><header><strong>FinReq AI <small>DEMO</small></strong><nav>{nav}</nav>{auth}</header><main>{body}</main></body></html>'''

def form(title, action, fields, note=''):
    return page(title,f'<h1>{title}</h1><p class="sub">{note}</p><form class="card" method="post" action="{action}">'+''.join(f'<label>{label}<input name="{name}" type="{typ}" required></label><br>' for label,name,typ in fields)+'<button>Continue</button></form>')
def user_of(h):
    sid=cookies.SimpleCookie(h.headers.get('Cookie')).get('finreq'); return SESS.get(sid.value,{}).get('user') if sid else None
def state(user): return SESS.setdefault(next((k for k,v in SESS.items() if v.get('user')==user),secrets.token_urlsafe()), {'user':user,'srs':[],'sdlc':''})
class App(BaseHTTPRequestHandler):
  def send(self, status, content, mime='text/html; charset=utf-8', extra=None):
    data=content.encode() if isinstance(content,str) else content; self.send_response(status);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(data))); 
    if extra:
      for k,v in extra.items():self.send_header(k,v)
    self.end_headers();self.wfile.write(data)
  def redirect(self, to, cookie=None): self.send_response(303);self.send_header('Location',to);cookie and self.send_header('Set-Cookie',cookie);self.end_headers()
  def body(self): return {k:v[0] for k,v in parse_qs(self.rfile.read(int(self.headers.get('Content-Length','0'))).decode()).items()}
  def json(self, value, status=200): return self.send(status,json.dumps(value),'application/json; charset=utf-8')
  def do_GET(self):
    p=urlparse(self.path).path; user=user_of(self)
    if p == '/platform': return self.redirect('/platform/')
    if p.startswith('/platform/'):
      requested = p.removeprefix('/platform/') or 'index.html'
      allowed = {'index.html', 'app.js', 'styles.css'}
      if requested not in allowed: return self.send(404,'Not found')
      file = ROOT / requested
      return self.send(200,file.read_bytes(),guess_type(str(file))[0] or 'application/octet-stream')
    if p=='/': return self.send(200,page('Finance Requirement Intelligence','<h1>Finance Requirement Intelligence</h1><p class="sub">A full academic prototype for agentic requirement engineering and SDLC identification in finance.</p><div class="grid"><section class="card"><h2>1. Agentic Finance Platform</h2><p>Run the end-to-end workflow: informal input, structured requirements, clarification, security, compliance, risk, SDLC scoring, workflow, traceability, artefacts, audit, and evaluation.</p><a class="button" href="/platform/">Open Agentic Platform</a></section><section class="card"><h2>2. Finance SRS Studio</h2><p>Discuss a project, answer adaptive finance/security questions, and export a Word requirements specification.</p><a class="button" href="/srs">Open SRS Studio</a></section><section class="card"><h2>3. Finance SDLC Studio</h2><p>Provide a project statement or SRS evidence, review transparent SDLC reasoning, and export a Word recommendation.</p><a class="button" href="/sdlc">Open SDLC Studio</a></section></div><p class="notice">Demo intelligence is deterministic and local. Outputs are drafts requiring human business, security, and compliance review.</p>',user))
    if p=='/login': return self.send(200,form('Sign in','/login',[('Username','username','text'),('Password','password','password')],'Use a local account to keep studio histories separate.'))
    if p=='/signup': return self.send(200,form('Create account','/signup',[('Username','username','text'),('Password','password','password')],'Local-only authentication for this demo.'))
    if p=='/logout':
      c=cookies.SimpleCookie(self.headers.get('Cookie')); sid=c.get('finreq'); sid and SESS.pop(sid.value,None); return self.redirect('/', 'finreq=; Max-Age=0; Path=/')
    if not user: return self.redirect('/login')
    st=state(user)
    if p=='/srs':
      turns=''.join(f'<div class="turn {x["role"]}"><span class="role">{x["role"]}</span>{x["content"]}</div>' for x in st['srs']) or '<p class="help">Describe your financial software project to begin.</p>'
      return self.send(200,page('Finance SRS Studio',f'<h1>Finance SRS Studio</h1><p class="sub">Describe the project naturally. The local agent records evidence and asks for missing financial controls.</p><div class="grid"><aside class="card"><h2>Workspace</h2><p>Guided discovery</p><p>Structured SRS draft</p><p>Word export</p><form method="post" action="/srs/new"><button class="secondary">New project</button></form></aside><section class="card"><div>{turns}</div><form method="post" action="/srs/chat"><label>Project discussion</label><textarea name="message" placeholder="Describe your digital banking, payment, loan, insurance, or analytics project…" required></textarea><div class="actions"><button>Send</button><button formaction="/srs/report" class="secondary">Generate Finance SRS</button></div></form>{"<p><a class=button href=/srs/download>Download Finance SRS (.docx)</a></p>" if st.get("srs_file") else ""}</section></div>',user))
    if p=='/sdlc':
      report=st.get('sdlc',''); return self.send(200,page('Finance SDLC Studio',f'<h1>Finance SDLC Studio</h1><p class="sub">Provide a finance-project statement or paste relevant SRS content. The prototype exposes its decision reasoning.</p><div class="grid"><aside class="card"><h2>Workspace</h2><p>SDLC comparison</p><p>Finance risk-aware workflow</p><p>Word export</p><form method="post" action="/sdlc/new"><button class="secondary">New project</button></form></aside><section class="card"><form method="post" action="/sdlc/report"><label>Project statement or SRS evidence</label><textarea name="context" required placeholder="Paste the project statement, requirements, security criticality, compliance checkpoints, and expected requirement changes…">{st.get("sdlc_context","")}</textarea><div class="actions"><button>Generate detailed SDLC report</button></div></form>{f"<h2>Recommendation preview</h2><div class=report>{report}</div><p><a class=button href=/sdlc/download>Download SDLC report (.docx)</a></p>" if report else ""}</section></div>',user))
    return self.send(404,page('Not found','<h1>Not found</h1>',user))
  def do_POST(self):
    p=urlparse(self.path).path
    if p == '/api/extract-document':
      # The platform only extracts text from local .txt/.docx files. It never sends the file to an external LLM.
      try:
        boundary = self.headers.get('Content-Type','').split('boundary=',1)[1].encode()
        raw = self.rfile.read(int(self.headers.get('Content-Length','0')))
        part = next(x for x in raw.split(b'--'+boundary) if b'filename=' in x)
        header, data = part.split(b'\r\n\r\n',1); data = data.rsplit(b'\r\n',1)[0]
        filename = re.search(br'filename="([^"]+)"',header).group(1).decode('utf-8','ignore').lower()
        if filename.endswith('.txt'): text=data.decode('utf-8','replace')
        elif filename.endswith('.docx'):
          from io import BytesIO
          with zipfile.ZipFile(BytesIO(data)) as z: xml=z.read('word/document.xml').decode('utf-8','replace')
          text=re.sub(r'<[^>]+>',' ',xml); text=re.sub(r'\s+',' ',text)
        else: raise ValueError('Use a TXT or DOCX document.')
        if not text.strip(): raise ValueError('The document has no readable text.')
        return self.json({'text':text[:50000],'source':filename,'warning':'Local extraction only. Verify sensitive data masking before production use.'})
      except Exception as e: return self.json({'error':str(e)},400)
    data=self.body();user=user_of(self)
    if p in ('/login','/signup'):
      name=data.get('username','').strip(); password=data.get('password',''); c=conn()
      if p=='/signup':
        try:c.execute('insert into users values (?,?)',(name,pw(password)));c.commit()
        except sqlite3.IntegrityError:return self.send(400,form('Create account','/signup',[('Username','username','text'),('Password','password','password')],'<span class=error>Username already exists.</span>'))
      row=c.execute('select password from users where username=?',(name,)).fetchone();c.close()
      if not row or row[0]!=pw(password): return self.send(400,form('Sign in','/login',[('Username','username','text'),('Password','password','password')],'<span class=error>Invalid username or password.</span>'))
      sid=secrets.token_urlsafe();SESS[sid]={'user':name,'srs':[],'sdlc':''};return self.redirect('/',f'finreq={sid}; Path=/; HttpOnly; SameSite=Lax')
    if not user:return self.redirect('/login')
    st=state(user)
    if p=='/srs/new':st['srs']=[];st.pop('srs_file',None);return self.redirect('/srs')
    if p=='/srs/chat':
      msg=data.get('message','').strip();st['srs'] += [{'role':'user','content':msg},{'role':'assistant','content':srs_reply(msg,st['srs'])}];st.pop('srs_file',None);return self.redirect('/srs')
    if p=='/srs/report':
      project='Finance Software Project'; path=OUT/f'finance-srs-{secrets.token_hex(5)}.docx';write_docx(path,project+' — Software Requirements Specification',srs_sections(project,st['srs']));st['srs_file']=str(path);return self.redirect('/srs')
    if p=='/srs/download': return self.download(st.get('srs_file'),'Finance-SRS.docx')
    if p=='/sdlc/new':st['sdlc']='';st['sdlc_context']='';st.pop('sdlc_file',None);return self.redirect('/sdlc')
    if p=='/sdlc/report':
      text=data.get('context','').strip();st['sdlc_context']=text;st['sdlc']=sdlc_report('Finance Software Project',text);path=OUT/f'finance-sdlc-{secrets.token_hex(5)}.docx';write_docx(path,'Finance SDLC Recommendation',[('Detailed recommendation',st['sdlc'])]);st['sdlc_file']=str(path);return self.redirect('/sdlc')
    if p=='/sdlc/download': return self.download(st.get('sdlc_file'),'Finance-SDLC-Recommendation.docx')
    return self.send(404,'Not found')
  def download(self,path,name):
    if not path or not Path(path).is_file():return self.send(404,'Generate a report first.')
    data=Path(path).read_bytes(); return self.send(200,data,'application/vnd.openxmlformats-officedocument.wordprocessingml.document',{'Content-Disposition':f'attachment; filename="{name}"'})
  def log_message(self,*args): pass
if __name__=='__main__':
  print('Finance portal: http://127.0.0.1:8002');ThreadingHTTPServer(('127.0.0.1',8002),App).serve_forever()
