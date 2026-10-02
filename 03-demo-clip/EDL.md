# Edit decision list: final_demo.mp4

Output: `final_demo.mp4` · 1920×1080 · 30 fps · 39.3 s.
Source: `source_capture.mp4`, a 2940×1600 capture of the prototype made with `scripts/capture.mjs`. It replaces `demo.mov`, which was not available; the shot order follows the original edit brief.
The capture was taken at about 5 fps at full resolution. All zooms and pans were rendered in post at 30 fps.

All cuts are hard cuts, except a 7-frame cross-dissolve into the end card. Captions appear 0.2 s after each cut (see `captions_en.srt` and `captions_th.srt`).

| # | Output in | Output out | Source in | Source out | Speed | Shot |
|---|---|---|---|---|---|---|
| 1 | 00:00:00.000 | 00:00:03.000 | 00:00:00.402 | 00:00:03.402 | 1× | Landing hero → push in to 'From evidence to review' |
| 2 | 00:00:03.000 | 00:00:05.500 | 00:00:05.058 | 00:00:07.558 | 1× | Demo cases: '฿300 merchant payment' card |
| 3 | 00:00:05.500 | 00:00:08.500 | 00:00:11.296 | 00:00:20.296 | 3× | Institutions: Bank A transaction feed fills (3× speed) |
| 4 | 00:00:08.500 | 00:00:15.233 | 00:00:21.056 | 00:00:29.456 | 1.25× | Our Engine: CASE-0001 opens, money-flow graph, 0.85 score + reasons |
| 5 | 00:00:15.233 | 00:00:19.633 | 00:00:31.109 | 00:00:35.509 | 1× | Institutions, Bank B only: click 'Restrict ฿300 only' → Held ฿300 |
| 6 | 00:00:19.633 | 00:00:22.533 | 00:00:35.952 | 00:00:38.852 | 1× | Merchant: ฿300 held / ฿10,000 usable |
| 7 | 00:00:22.533 | 00:00:25.533 | 00:00:39.995 | 00:00:42.995 | 1× | Merchant: evidence sent, review flow at 'Officer review' |
| 8 | 00:00:25.533 | 00:00:28.533 | 00:00:43.666 | 00:00:46.666 | 1× | Bank B officer console: click 'Release this hold' |
| 9 | 00:00:28.533 | 00:00:31.533 | 00:00:47.332 | 00:00:50.332 | 1× | Merchant: hold released, ฿10,300 usable |
| 10 | 00:00:31.533 | 00:00:34.533 | 00:00:50.830 | 00:00:53.830 | 1× | Overview: institutions, engine, merchant side by side (pull-out) |
| 11 | 00:00:34.300 | 00:00:39.300 | 00:00:56.356 | (still) | — | End card: blurred landing hero + navy 70%, ทันเงิน logo, tagline (7-frame dissolve in) |

## Crops (source pixels, 16:9, eased between keyframes)

| # | Start → end crop (x, y, width) | Zoom vs full frame |
|---|---|---|
| 1 | (48, 0, 2844) → (1230, 274, 1800) | 1.0× → 1.6× |
| 2 | (0, 520, 1850) → (60, 600, 1600) | 1.5× → 1.8× |
| 3 | (180, 300, 1520) → (300, 380, 1300) | 1.9× → 2.2× |
| 4 | (300, 0, 2200) held until the tag reads CASE-0001 → (560, 660, 1660) | 1.3× → 1.7× |
| 5 | (1300, 500, 820) → (1330, 520, 790): Bank B column only, Exchange out of frame | about 3.6× |
| 6 | (800, 300, 2100) → (880, 337, 2016) | 1.35× → 1.4× |
| 7 | (840, 230, 2040) → (883, 255, 1968) | 1.4× |
| 8 | (1320, 1075, 790) → (1340, 1090, 760): console buttons only | about 3.7× |
| 9 | (840, 290, 2040) → (883, 310, 1968) | 1.4× |
| 10 | (470, 230, 2000) → (48, 0, 2844): pull-out | 1.4× → 1.0× |

Segments 5 and 8 zoom past the 2× guide. That is the only way to keep the Exchange panel and the recommendation line out of frame. The capture is at 2× DPI, so the text stays readable, though slightly softer than in the other shots.
