"""Static checks: internal links + anchors, one h1, heading order, img alt, unique titles/descriptions."""
import os, re, glob, io
from html.parser import HTMLParser
SITE=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'site')
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links=[]; s.ids=set(); s.heads=[]; s.imgs=[]; s.title=''; s.desc=''; s._t=False; s.base=None
    def handle_starttag(s,t,a):
        a=dict(a)
        if 'id' in a: s.ids.add(a['id'])
        if t=='a' and 'href' in a: s.links.append(a['href'])
        if t in('link','script','img'):
            v=a.get('href') or a.get('src')
            if v: s.links.append(v)
        if re.fullmatch(r'h[1-6]',t): s.heads.append(int(t[1]))
        if t=='img': s.imgs.append(a)
        if t=='title': s._t=True
        if t=='base': s.base=a.get('href')
        if t=='meta' and a.get('name')=='description': s.desc=a.get('content','')
    def handle_data(s,d):
        if s._t: s.title+=d
    def handle_endtag(s,t):
        if t=='title': s._t=False
pages={}
for f in glob.glob(os.path.join(SITE,'**','*.html'),recursive=True):
    p=P(); p.feed(io.open(f,encoding='utf-8').read()); pages[os.path.normpath(f)]=p
bad=0; titles={}; descs={}
for f,p in pages.items():
    rel=os.path.relpath(f,SITE)
    for l in p.links:
        if re.match(r'(https?:|tel:|mailto:)',l): continue
        path,_,frag=l.partition('#'); path=path.split('?')[0]
        base=SITE if p.base=='/' else os.path.dirname(f)
        target=os.path.normpath(os.path.join(base,path)) if path else f
        if not os.path.exists(target): print('BROKEN',rel,'->',l); bad+=1; continue
        if frag and target.endswith('.html') and frag not in pages[target].ids: print('MISSING ANCHOR',rel,'->',l); bad+=1
    if p.heads.count(1)!=1: print('H1 COUNT',rel,p.heads.count(1)); bad+=1
    prev=0
    for h in p.heads:
        if h>prev+1: print('HEADING SKIP',rel,prev,'->',h); bad+=1
        prev=h
    for i in p.imgs:
        if 'alt' not in i: print('NO ALT',rel,i.get('src')); bad+=1
        if 'width' not in i or 'height' not in i: print('NO SIZE',rel,i.get('src')); bad+=1
    titles.setdefault(p.title,[]).append(rel); descs.setdefault(p.desc,[]).append(rel)
    if len(p.title)>65: print('LONG TITLE',rel,len(p.title))
    if not 70<=len(p.desc)<=165: print('DESC LENGTH',rel,len(p.desc))
for k,v in list(titles.items())+list(descs.items()):
    if len(v)>1: print('DUPLICATE',k,v); bad+=1
print(len(pages),'pages checked,',bad,'problems')
