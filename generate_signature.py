import io
import json
import urllib.request
from PIL import Image, ImageDraw, ImageFont

with open('current-reading.json', encoding='utf-8') as f:
    book = json.load(f)

W, H = 640, 124
img = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(img)

REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
LABEL = ImageFont.truetype(REG, 10)
TITLE = ImageFont.truetype(BOLD, 16)
AUTHOR = ImageFont.truetype(REG, 12)

# Subtle vertical divider keeps the widget clean in an email signature.
d.line((72, 18, 72, 106), fill=(220, 220, 220), width=1)

cover = None
if book.get('cover'):
    try:
        req = urllib.request.Request(book['cover'], headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as r:
            cover = Image.open(io.BytesIO(r.read())).convert('RGB')
            cover.thumbnail((54, 82), Image.Resampling.LANCZOS)
    except Exception as e:
        print('Cover download failed:', e)

if cover:
    x = 8 + (54 - cover.width) // 2
    y = (H - cover.height) // 2
    img.paste(cover, (x, y))
else:
    d.rounded_rectangle((8, 21, 62, 103), radius=3, outline=(210, 210, 210), width=1)

d.text((94, 18), 'CURRENTLY READING', font=LABEL, fill=(105, 105, 105))

def ellipsize(text, font, max_width):
    text = text or ''
    if d.textbbox((0, 0), text, font=font)[2] <= max_width:
        return text
    while text and d.textbbox((0, 0), text + '…', font=font)[2] > max_width:
        text = text[:-1]
    return text + '…'

title = ellipsize(book.get('title'), TITLE, W - 104)
author = ellipsize('by ' + (book.get('author') or ''), AUTHOR, W - 104)
d.text((94, 39), title, font=TITLE, fill=(35, 35, 35))
d.text((94, 66), author, font=AUTHOR, fill=(105, 105, 105))

# Small Goodreads-style prompt without relying on JavaScript.
d.text((94, 91), 'My Goodreads • Currently Reading', font=LABEL, fill=(145, 145, 145))

img.save('currently-reading.png', 'PNG', optimize=True)
print('Generated polished currently-reading.png')
