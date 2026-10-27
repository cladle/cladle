import re,html,json,sys
from html.parser import HTMLParser
t=open(sys.argv[1],encoding='utf-8').read()
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.stack=[]; s.rank=None; s.cur=None; s.field=None; s.out=[]; s.ulr=[]
    def handle_starttag(s,tag,a):
        a=dict(a); c=a.get('class','')
        if tag=='ul':
            m=re.search(r'rank_(\w+)',c); s.ulr.append(m.group(1) if m else None)
        elif tag=='div' and c=='taxon':
            r=s.ulr[-1] if s.ulr else None
            s.cur={'rank':r,'ja':'','sci':'','depth':len(s.ulr)}; s.out.append(s.cur)
        elif tag=='span' and s.cur is not None:
            if c.startswith('wamei'): s.field='ja'
            elif c.startswith('sciname') and 'author' not in c: s.field='sci'
            else: s.field=None
            if 'provisional' in c or 'undescribed' in c: s.cur['flag']=c
    def handle_endtag(s,tag):
        if tag=='ul': s.ulr.pop()
        elif tag=='span': s.field=None
        elif tag=='div': s.cur=None
    def handle_data(s,d):
        if s.cur is not None and s.field: s.cur[s.field]+=d
p=P(); p.feed(t)
for x in p.out: x['ja']=x['ja'].strip(); x['sci']=' '.join(x['sci'].split())
json.dump(p.out,open('herp.json','w'),ensure_ascii=False,indent=0)
import collections
print(collections.Counter(x['rank'] for x in p.out))
for x in p.out:
    if x['rank'] not in ('species','subspecies','genus'): print('  '*x['depth'],x['rank'],x['ja'],x['sci'],x.get('flag',''))
