"""Edits the source capture into the ทันเงิน product demo (1920×1080, 30 fps).

Stage 1 (`python3 edit.py plan`): writes edit_segments.json (captions) for render_text.mjs.
Stage 2 (`python3 edit.py render`): renders video frames to ffmpeg, plus SRTs, EDL and audio cues.
Source times are anchored to the marks logged by capture.mjs. Rects are source pixels (2940×1600) as [x, y, w]; height is always w*9/16 (16:9, never letterboxed).
"""
import bisect, json, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter

FPS, OW, OH = 30, 1920, 1080
SW, SH = 2940, 1600
cap = json.load(open('capture.json'))
FR = cap['frames']; TS = [f['t'] for f in FR]
M = {m['name']: m['t'] for m in cap['marks']}
CLICKS = [c for c in cap['clicks'] if 'player-main' not in c['sel'] and 'Restart' not in c['sel']]  # only on-screen officer/merchant clicks

# (src_in, src_out, speed, keyframes [(u, [x,y,w])], EN, TH, label)
SEGMENTS = [
    (M['hero'] + 0.1, M['hero'] + 3.1, 1.0, [(0, [48, 0, 2844]), (1, [1230, 274, 1800])],
     "Scam money moves from bank to crypto in minutes.",
     "เงินจากมิจฉาชีพไหลจากธนาคารสู่คริปโตในไม่กี่นาที", "Landing hero → push in to 'From evidence to review'"),
    (M['cases'] + 0.21, M['cases'] + 2.71, 1.0, [(0, [0, 520, 1850]), (1, [60, 600, 1600])],
     "Banks see baht. Exchanges see crypto. Nobody sees the whole path.",
     "ธนาคารเห็นเงินบาท ศูนย์ซื้อขายเห็นคริปโต ไม่มีใครเห็นเส้นทางทั้งหมด", "Demo cases: '฿300 merchant payment' card"),
    (M['inst_play'] + 0.4, M['inst_play'] + 9.4, 3.0, [(0, [180, 300, 1520]), (1, [300, 380, 1300])],
     "A victim's ฿50,000 is split across mule accounts within minutes.",
     "เงิน ฿50,000 ของผู้เสียหายถูกแตกไปหลายบัญชีม้าภายในไม่กี่นาที", "Institutions: Bank A transaction feed fills (3× speed)"),
    (M['engine'] + 0.55, M['engine'] + 8.95, 1.25, [(0, [300, 0, 2200]), (0.64, [300, 0, 2200]), (0.84, [515, 644, 1700]), (1, [560, 660, 1660])],
     "ทันเงิน links bank, exchange and chain into one explainable case.",
     "ทันเงินเชื่อมธนาคาร ศูนย์ซื้อขาย และบล็อกเชนเป็นเคสเดียวที่อธิบายได้", "Our Engine: CASE-0001 opens, money-flow graph, 0.85 score + reasons"),
    (M['restrict'] + 0.09, M['restrict'] + 4.49, 1.0, [(0, [1300, 500, 820]), (1, [1330, 520, 790])],
     "The officer holds only the suspicious ฿300, not the whole account.",
     "เจ้าหน้าที่พักเฉพาะยอด ฿300 ที่น่าสงสัย ไม่ใช่ทั้งบัญชี", "Institutions, Bank B only: click 'Restrict ฿300 only' → Held ฿300"),
    (M['merchant_held'] + 0.2, M['merchant_held'] + 3.1, 1.0, [(0, [800, 300, 2100]), (1, [880, 337, 2016])],
     "The shop keeps ฿10,000 to keep trading.",
     "ร้านค้ายังใช้เงิน ฿10,000 ค้าขายต่อได้", "Merchant: ฿300 held / ฿10,000 usable"),
    (M['evidence_sent'] + 0.49, M['evidence_sent'] + 3.49, 1.0, [(0, [840, 230, 2040]), (1, [883, 255, 1968])],
     "The shop sends evidence from its banking app.",
     "ร้านค้าส่งหลักฐานผ่านแอปธนาคาร", "Merchant: evidence sent, review flow at 'Officer review'"),
    (M['console'] + 0.32, M['console'] + 3.32, 1.0, [(0, [1320, 1075, 790]), (1, [1340, 1090, 760])],
     "A bank officer reviews and decides. Humans stay in control.",
     "เจ้าหน้าที่ธนาคารทบทวนและตัดสินใจ มนุษย์ยังเป็นผู้ควบคุม", "Bank B officer console: click 'Release this hold'"),
    (M['released'] + 0.31, M['released'] + 3.31, 1.0, [(0, [840, 290, 2040]), (1, [883, 310, 1968])],
     "Released. The full ฿10,300 is usable again.",
     "ปลดการพักยอดแล้ว ใช้เงินได้ครบ ฿10,300", "Merchant: hold released, ฿10,300 usable"),
    (M['overview'] + 0.3, M['overview'] + 3.3, 1.0, [(0, [470, 230, 2000]), (1, [48, 0, 2844])],
     "Every party sees one shared, explainable case.",
     "ทุกฝ่ายเห็นเคสเดียวกันที่อธิบายได้", "Overview: institutions, engine, merchant side by side (pull-out)"),
]
END_DUR, XFADE = 5.0, 7  # end card seconds, cross-dissolve frames into the end card

def ease(u): return 4 * u ** 3 if u < .5 else 1 - (-2 * u + 2) ** 3 / 2

def rect_at(kf, u):
    for (u0, r0), (u1, r1) in zip(kf, kf[1:]):
        if u <= u1:
            k = ease(0 if u1 == u0 else (u - u0) / (u1 - u0))
            x, y, w = [a + (b - a) * k for a, b in zip(r0, r1)]
            break
    else:
        x, y, w = kf[-1][1]
    h = w * 9 / 16
    x = min(max(x, 0), SW - w); y = min(max(y, 0), SH - h)
    return x, y, w, h

def frame_at(t):
    return FR[max(0, bisect.bisect_right(TS, t) - 1)]['name']

def fmt(t, sep=','):
    ms = round(t * 1000); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}{sep}{ms % 1000:03d}"

# Output timeline: segments butt-joined with hard cuts; the end card dissolves in over the last XFADE frames.
timeline, t = [], 0.0
for s in SEGMENTS:
    n = round((s[1] - s[0]) / s[2] * FPS)
    timeline.append((t, n)); t += n / FPS
end_start = t - XFADE / FPS
TOTAL = end_start + END_DUR

if sys.argv[1] == 'plan':
    Image.open('hero_end.png').crop((0, 150, SW, 1400)).save('hero_bg.png')  # dark hero band only, for the end card
    json.dump([{'en': s[4], 'th': s[5]} for s in SEGMENTS], open('edit_segments.json', 'w'), ensure_ascii=False, indent=1)
    print('total', round(TOTAL, 2)); sys.exit()

caps = [Image.open(f'overlays/cap_{i}.png').convert('RGBA') for i in range(len(SEGMENTS))]
end_bg = Image.open('overlays/end_bg.png').convert('RGBA'); end_fg = Image.open('overlays/end_fg.png').convert('RGBA')
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{OW}x{OH}', '-r', str(FPS),
                       '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', 'video_only.mp4'],
                      stdin=subprocess.PIPE)
cache = {}
def src_img(name):
    if name not in cache:
        cache.clear(); cache[name] = Image.open(name).convert('RGB')
    return cache[name]

def click_ring(img, s_t, x, y, w):
    """Soft highlight on a click: an expanding, fading ring for 0.6s from the click time."""
    for c in CLICKS:
        dt = s_t - c['t']
        if 0 <= dt <= 0.6:
            sx, sy = (c['x'] - x) * OW / w, (c['y'] - y) * OW / w
            k = dt / 0.6; r = 18 + 46 * k; a = int(170 * (1 - k))
            ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
            d.ellipse([sx - 22, sy - 22, sx + 22, sy + 22], fill=(74, 159, 245, int(70 * (1 - k))))
            d.ellipse([sx - r, sy - r, sx + r, sy + r], outline=(74, 159, 245, a), width=5)
            img = Image.alpha_composite(img, ov)
    return img

cues, srt_en, srt_th, edl = [], [], [], []
last_frame = None
for i, (s, (o_start, n)) in enumerate(zip(SEGMENTS, timeline)):
    src_in, src_out, speed, kf, en, th, label = s
    for c in CLICKS:
        if src_in <= c['t'] <= src_out: cues.append({'type': 'click', 't': o_start + (c['t'] - src_in) / speed})
    c_in, c_out = o_start + 0.2, o_start + n / FPS - (XFADE / FPS if i == len(SEGMENTS) - 1 else 0)
    srt_en.append((c_in, c_out, en)); srt_th.append((c_in, c_out, th))
    edl.append((i + 1, o_start, o_start + n / FPS, src_in, src_out, speed, label))
    for k in range(n):
        u = k / max(n - 1, 1); s_t = src_in + k / FPS * speed
        x, y, w, h = rect_at(kf, u)
        img = src_img(frame_at(s_t)).crop((round(x), round(y), round(x + w), round(y + h))).resize((OW, OH), Image.LANCZOS).convert('RGBA')
        img = click_ring(img, s_t, x, y, w)
        ct = k / FPS - 0.2
        if ct >= 0:
            a = min(1, ct / 0.2)
            layer = caps[i] if a >= 1 else Image.blend(Image.new('RGBA', caps[i].size, (0, 0, 0, 0)), caps[i], a)
            img = Image.alpha_composite(img, layer)
        # dissolve into the end card over the final XFADE frames of the last segment
        if i == len(SEGMENTS) - 1 and k >= n - XFADE:
            img = Image.blend(img, end_bg, (k - (n - XFADE) + 1) / (XFADE + 1))
        ff.stdin.write(img.convert('RGB').tobytes())

# End card: background holds, logo/tagline fade + rise in over 0.6s.
n_end = round(END_DUR * FPS) - XFADE
for k in range(n_end):
    tt = k / FPS; a = min(1, max(0, (tt - 0.15) / 0.6)); e = ease(a)
    img = end_bg.copy()
    fg = end_fg.copy()
    if a < 1:
        fg.putalpha(fg.getchannel('A').point(lambda v: int(v * e)))
    img.alpha_composite(fg, (0, round(18 * (1 - e))))
    ff.stdin.write(img.convert('RGB').tobytes())
ff.stdin.close(); ff.wait()

total = timeline[-1][0] + timeline[-1][1] / FPS + n_end / FPS
cues.append({'type': 'endcard', 't': end_start})
json.dump({'cues': cues, 'end': total, 'segments': [o for o, _ in timeline]}, open('out_cues.json', 'w'), indent=1)

def write_srt(path, rows):
    with open(path, 'w') as f:
        for j, (a, b, txt) in enumerate(rows, 1): f.write(f"{j}\n{fmt(a)} --> {fmt(b)}\n{txt}\n\n")
end_lines_en = 'Stop the mule money — not the innocent merchant.'
end_lines_th = 'หยุดเงินม้า ไม่ใช่หยุดร้านค้าบริสุทธิ์'
write_srt('captions_en.srt', srt_en + [(end_start + 0.5, total, end_lines_en)])
write_srt('captions_th.srt', srt_th + [(end_start + 0.5, total, end_lines_th)])
with open('edl.md', 'w') as f:
    f.write('| # | Output in | Output out | Source in | Source out | Speed | Shot |\n|---|---|---|---|---|---|---|\n')
    for j, oi, oo, si, so, sp, lb in edl:
        f.write(f'| {j} | {fmt(oi, ".")} | {fmt(oo, ".")} | {fmt(si, ".")} | {fmt(so, ".")} | {sp:g}× | {lb} |\n')
    f.write(f'| 11 | {fmt(end_start, ".")} | {fmt(total, ".")} | {fmt(cap["marks"][-1]["t"], ".")} | (still) | — | End card: blurred landing hero + navy 70%, ทันเงิน logo, tagline ({XFADE}-frame dissolve in) |\n')
print('total', round(total, 2), 'clicks', [round(c['t'], 2) for c in cues if c['type'] == 'click'])
