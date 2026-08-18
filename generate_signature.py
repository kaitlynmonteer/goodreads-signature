import io
import json
import urllib.request
from PIL import Image, ImageDraw, ImageFont

with open('current-reading.json', encoding='utf-8') as f:
    book = json.load(f)

W, H = 560, 100
img = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(img)

# Use fonts available on the GitHub Actions Ubuntu runner.
REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
SMALL = ImageFont.truetype(REG, 11)
TITLE = ImageFont.truetype(BOLD, 15)
AUTHOR = ImageFont.truetype(REG, 12)

cover = None
if book.get('cover'):
    try:
        req = urllib.request.Request(book['cover'], headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as r:
            cover = Image.open(io.BytesIO(r.read())).convert('RGB')
            cover.thumbnail((54, 78), Image.Resampling.LANCZOS)
    except Exception as e:
        print('Cover download failed:', e)

if cover:
    x = (54 - cover.width) // 2
    y = (78 - cover.height) // 2
    img.paste(cover, (x, y))

text_x = 70
d.text((text_x, 12), 'CURRENTLY READING', font=SMALL, fill=(110, 110, 110))

def ellipsize(text, font, max_width):
    text = text or ''
    if d.textbbox((0, 0), text, font=font)[2] <= max_width:
        return text
    while text and d.textbbox((0, 0), text + '…', font=font)[2] > max_width:
        text = text[:-1]
    return text + '…'

title = ellipsize(book.get('title'), TITLE, W - text_x - 10)
author = ellipsize('by ' + (book.get('author') or ''), AUTHOR, W - text_x - 10)
d.text((text_x, 31), title, font=TITLE, fill=(35, 35, 35))
d.text((text_x, 56), author, font=AUTHOR, fill=(100, 100, 100))

img.save('currently-reading.png', 'PNG', optimize=True)
print('Generated currently-reading.png')
