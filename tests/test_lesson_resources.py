"""Check the rendered lesson resource contract in both languages."""
from pathlib import Path
from html.parser import HTMLParser
import json, os, unittest

ROOT=Path(__file__).resolve().parents[1]
BUILD=Path(os.environ.get('TEXTBOOK_BUILD','/private/tmp/10th-social-resource-build'))

class Panels(HTMLParser):
    def __init__(self):
        super().__init__();self.stack=[];self.references=[];self.books=[];self.videos=[];self.activity_links=[];self.topics=[];self.activity=False;self.simulations=[];self.statuses=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs); scope={v for _,v in self.stack if v}
        if attrs.get('id'):scope.add(attrs['id'])
        if tag=='a' and 'referencepanel' in scope:self.references.append(attrs.get('href'))
        if attrs.get('data-original-check-status'):self.statuses.append(attrs['data-original-check-status'])
        if 'lesson-book-reference' in attrs.get('class','').split():self.books.append(attrs)
        if attrs.get('data-lesson-video-url'):self.videos.append(attrs['data-lesson-video-url'])
        if tag=='a' and attrs.get('data-external-activity'):self.activity_links.append(attrs['href'])
        if tag=='option' and 'lesson-topic-select' in scope:self.topics.append(attrs.get('value'))
        if attrs.get('id')=='lesson-activities':self.activity=True
        if attrs.get('data-simulation'):self.simulations.append(attrs['data-simulation'])
        if tag not in ['img','br','hr','meta','link','input','source','wbr']:self.stack.append((tag,attrs.get('id')))
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:self.stack=self.stack[:i];break

class LessonResourceTests(unittest.TestCase):
    def test_all_lessons_have_real_resource_panels_and_local_activities(self):
        failures=[];counts={'lessons':0,'videos':0,'topics':0}
        for lang,path in [('en','.textbook-agent/english-review-20261013/published-resource-catalog.json'),('ta','.textbook-agent/resource-review-20261012/published-resource-catalog.json')]:
            catalogue=json.loads((ROOT/path).read_text())
            for lesson in catalogue['lessons']:
                slug=lesson['slug'];html=BUILD/('ta' if lang=='ta' else '')/'docs'/slug/'index.html'
                if not html.exists():failures.append(f'{lang}/{slug}: no rendered page');continue
                p=Panels();p.feed(html.read_text());counts['lessons']+=1;counts['videos']+=len(p.videos);counts['topics']+=len(p.topics)
                source=f'/10th-social/{"ta/" if lang=="ta" else ""}docs/{slug}/source/'
                if source not in p.references:failures.append(f'{lang}/{slug}: original source missing from References panel')
                if not p.books:failures.append(f'{lang}/{slug}: printed bibliography missing from Books panel')
                if p.statuses != [r['status'] for r in lesson['source_checks']]:failures.append(f'{lang}/{slug}: recorded reference statuses missing')
                if not all(p.references):failures.append(f'{lang}/{slug}: empty reference URL')
                if not {v['url'] for v in lesson['videos']} <= set(p.videos):failures.append(f'{lang}/{slug}: Videos panel missing catalogue videos')
                if not p.activity or set(p.topics)!={t['anchor'] for t in lesson['topics']}:failures.append(f'{lang}/{slug}: local topic activity missing')
                if not {x['url'] for x in lesson['interactive']} <= set(p.activity_links):failures.append(f'{lang}/{slug}: external activity links missing')
                kind={'climate-and-natural-vegetation-of-india':'climate','gross-domestic-product-and-its-growth-an-introduction':'gdp','government-and-taxes':'gst'}.get(slug)
                if kind and kind not in p.simulations:failures.append(f'{lang}/{slug}: {kind} simulation missing')
        self.assertEqual([],failures,f'{len(failures)} resource failures; first failures: {failures[:8]}')
        self.assertEqual(54,counts['lessons']);self.assertEqual(360,counts['topics']);self.assertEqual(372,counts['videos'])

    def test_source_galleries_do_not_get_lesson_only_controls(self):
        for lang in ['en','ta']:
            for folder in (ROOT/('content.'+lang)/'docs').iterdir():
                if not folder.is_dir():continue
                html=BUILD/('ta' if lang=='ta' else '')/'docs'/folder.name/'source/index.html'
                p=Panels();p.feed(html.read_text())
                self.assertFalse(p.activity,str(html))

if __name__=='__main__':unittest.main()
