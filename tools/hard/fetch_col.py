import json,glob,re,time,os,urllib.request,urllib.parse
UA={"User-Agent":"Cladle-education-game (github.com/cladle/cladle)"}
def get(u):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60) as r: return json.load(r)
        except Exception as e:
            print('retry',e); time.sleep(5*(i+1))
R=[r for f in sorted(glob.glob('v*.json')) for r in json.load(open(f))['result'] if re.search('[ァ-ヶ]',r['name'])]
ids=sorted({r['taxonID'] for r in R})
os.makedirs('cls',exist_ok=True)
for i in range(0,len(ids),100):
    f=f'cls/{i}.json'
    if os.path.exists(f): continue
    q='&'.join('USAGE_ID='+x for x in ids[i:i+100])
    d=get(f'https://api.checklistbank.org/dataset/3LR/nameusage/search?{q}&limit=200')
    json.dump(d,open(f,'w')); time.sleep(1.2)
refs=sorted({r.get('referenceId') for r in R if r.get('referenceId')})
C={}
if os.path.exists('refs.json'): C=json.load(open('refs.json'))
for x in refs:
    if x in C: continue
    d=get(f'https://api.checklistbank.org/dataset/3LR/reference/{x}'); C[x]=d.get('citation') if d else None; time.sleep(1.2)
json.dump(C,open('refs.json','w'),ensure_ascii=False)
print(len(ids),len(refs))
