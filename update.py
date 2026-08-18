import html
import json
import urllib.request
import xml.etree.ElementTree as ET

FEED = 'https://www.goodreads.com/review/list_rss/15832103?shelf=currently-reading'
req = urllib.request.Request(FEED, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=30) as response:
    root = ET.fromstring(response.read())

item = root.find('./channel/item')
if item is None:
    data = {'title':'','author':'','cover':'','url':''}
else:
    def text(name):
        node = item.find(name)
        return (node.text or '').strip() if node is not None else ''
    data = {
        'title': text('title'),
        'author': text('author_name'),
        'cover': text('book_large_image_url') or text('book_image_url'),
        'url': text('link')
    }

with open('current-reading.json','w',encoding='utf-8') as f:
    json.dump(data,f,ensure_ascii=False,indent=2)

print(json.dumps(data,ensure_ascii=False))
