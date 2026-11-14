from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

p = Path(__file__).parent
items = [
    ('navy-full', '네이비 재킷', '단정하고 품격 있는 클래식 스타일'),
    ('olive-full', '올리브 재킷', '자연스럽고 편안한 데일리 스타일'),
    ('blue-full', '라이트 블루 재킷', '밝고 산뜻한 스마트 캐주얼'),
    ('cardigan', '카디건과 청바지', '따뜻하고 여유로운 주말 스타일'),
    ('safari', '사파리 재킷', '가볍고 활동적인 외출 스타일'),
    ('casual-suit', '그레이 수트', '격식과 편안함을 갖춘 모임 스타일'),
]
title = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 24)
body = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 20)
w, h, footer = 480, 720, 106
frames = []
for stem, heading, caption in items:
    source = Image.open(p / f'lavento-{stem}-01.png').convert('RGB').resize((w, h), Image.Resampling.LANCZOS)
    for i in range(30):
        t = i / 29
        scale = 1 + .12 * t * t * (3 - 2 * t)
        cw, ch = w / scale, h / scale
        left, top = (w-cw)/2, (h-ch)*.25
        photo = source.transform((w, h), Image.Transform.EXTENT, (left, top, left+cw, top+ch), Image.Resampling.BICUBIC)
        canvas = Image.new('RGB', (w, h+footer), '#faf7f1')
        canvas.paste(photo, (0, 0))
        draw = ImageDraw.Draw(canvas)
        draw.text((w/2, h+14), heading, font=title, fill='#292b28', anchor='mt')
        draw.text((w/2, h+54), caption, font=body, fill='#575950', anchor='mt')
        if i == 0:
            canvas.save(p / f'lavento-{stem}-captioned.png')
            palette = canvas.quantize(colors=128)
        frames.append(canvas.quantize(palette=palette, dither=Image.Dither.NONE))
out = p / 'lavento-outfit-zoom-captioned.gif'
frames[0].save(out, save_all=True, append_images=frames[1:], duration=100, loop=0, optimize=False)
check = Image.open(out)
duration = 0
for i in range(check.n_frames):
    check.seek(i)
    duration += check.info['duration']
assert check.n_frames == 180 and duration == 18000
print(f'Validated: {check.n_frames} frames, {duration} ms, {check.size}')
