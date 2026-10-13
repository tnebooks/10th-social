"""Build Hugo resource data without changing any textbook Markdown."""
from pathlib import Path
import hashlib,json,re,urllib.parse

ROOT=Path(__file__).resolve().parents[1]
CATALOGUES={'en':'.textbook-agent/english-review-20261013/published-resource-catalog.json','ta':'.textbook-agent/resource-review-20261012/published-resource-catalog.json'}
SIMULATIONS={
 'climate-and-natural-vegetation-of-india':{'kind':'climate','topic':'topic-2-1','pages':{'en':150,'ta':159}},
 'gross-domestic-product-and-its-growth-an-introduction':{'kind':'gdp','topic':'topic-1-1','pages':{'en':299,'ta':316}},
 'government-and-taxes':{'kind':'gst','topic':'topic-4-3','pages':{'en':330,'ta':349}},
}
result={}
for lang,catalogue_path in CATALOGUES.items():
 catalogue=json.loads((ROOT/catalogue_path).read_text());result[lang]={}
 for lesson in catalogue['lessons']:
  slug=lesson['slug'];path=ROOT/('content.'+lang)/'docs'/slug/'_index.md';text=path.read_text()
  source=text.split('<!-- supplemental-resources:start -->')[0]
  heading=re.search(r'^###\s+(?:REFERENCE BOOKS|மேற்கோள் நூல்கள்|ேமற்ேகாள் நூல்கள்)\s*$',source,re.M)
  assert heading,(lang,slug,'missing bibliography heading')
  block=re.split(r'^#{1,6}\s+',source[heading.end():],maxsplit=1,flags=re.M)[0]
  books=[]
  for line in block.splitlines():
   if line.startswith(('!','<','{{')):continue
   numbered=re.match(r'^(\d+)\.\s+(.*)',line)
   if numbered:books.append({'number':numbered[1],'text':numbered[2]})
   elif line.strip() and books:books[-1]['text']+=' '+line.strip()
  assert books,(lang,slug,'empty printed bibliography')
  topics=[]
  for topic in lesson['topics']:
   assert f'id="{topic["anchor"]}"' in source,(lang,slug,topic['anchor'])
   topics.append({k:topic[k] for k in ['number','title','anchor','video_url','interactive_url']})
  references=[]
  for check in lesson['source_checks']:
   original=check.get('original_url') or check.get('printed_url')
   assert original,(lang,slug,check)
   parsed=urllib.parse.urlsplit(original)
   target=original if parsed.scheme in ['http','https'] and parsed.netloc and not re.search(r'\s',original) else None
   alternatives=check.get('alternatives',[])+([check['alternative']] if check.get('alternative') else [])
   references.append({'label':original,'url':target,'checked_date':check.get('checked_date'),'status':check['status'],'alternatives':alternatives})
  for item in lesson['videos']+lesson['interactive']:
   parsed=urllib.parse.urlsplit(item['url']);assert parsed.scheme=='https' and parsed.netloc,(lang,slug,item['url'])
  record={'title':re.search(r'^title:\s*(.+)',text,re.M)[1].strip('"\''), 'source_pages':lesson['source_pdf_pages'],'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'books':books,'videos':lesson['videos'],'activities':lesson['interactive'],'topics':topics,'source_checks':lesson['source_checks'],'references':references,'teacher_approval':False}
  if lesson.get('english_medium_catalogue'):record['video_catalogue']=lesson['english_medium_catalogue']
  if slug in SIMULATIONS:
   spec=SIMULATIONS[slug];page=spec['pages'][lang]
   record['simulation']={'kind':spec['kind'],'source_page':page,'source_item_id':f'p{page}-{ "equation" if spec["kind"]=="gdp" else "text"}-1','source_topic':spec['topic']}
  result[lang][slug]=record
(ROOT/'data').mkdir(exist_ok=True)
(ROOT/'data/lesson_resources.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'lessons':sum(len(x) for x in result.values()),'videos':sum(len(l['videos']) for x in result.values() for l in x.values()),'topic_activities':sum(len(l['topics']) for x in result.values() for l in x.values()),'simulations':sum('simulation' in l for x in result.values() for l in x.values())}))
