from PIL import Image
from pathlib import Path

p = Path(__file__).parent
names = ['lavento-navy-full-01.png', 'lavento-olive-full-01.png',
         'lavento-blue-full-01.png', 'lavento-cardigan-01.png',
         'lavento-safari-01.png', 'lavento-casual-suit-01.png']
frames = []
w, h = 480, 720
for name in names:
    im = Image.open(p / name).convert('RGB').resize((w, h), Image.Resampling.LANCZOS)
    palette = im.quantize(colors=128)
    for i in range(30):
        t = i / 29
        scale = 1 + 0.12 * t * t * (3 - 2 * t)
        cw, ch = w / scale, h / scale
        left, top = (w - cw) / 2, (h - ch) * 0.25
        frame = im.transform((w, h), Image.Transform.EXTENT,
                             (left, top, left + cw, top + ch), Image.Resampling.BICUBIC)
        frames.append(frame.quantize(palette=palette, dither=Image.Dither.NONE))
out = p / 'lavento-outfit-zoom-3sec.gif'
frames[0].save(out, save_all=True, append_images=frames[1:], duration=100,
               loop=0, optimize=False)
check = Image.open(out)
total = 0
for i in range(check.n_frames):
    check.seek(i)
    total += check.info['duration']
assert check.n_frames == 180 and total == 18000
print(f'{check.n_frames} frames, {total} ms, {out.stat().st_size} bytes')
