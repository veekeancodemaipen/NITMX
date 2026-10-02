"""Original light instrumental (~100 BPM) for the ทันเงิน demo, building into the end card, plus subtle clicks.
Reads out_cues.json from edit.py; the end-card cut is placed on a bar downbeat."""
import json
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 44100
cu = json.load(open('out_cues.json'))
DUR = cu['end']; N = int(DUR * SR); t_all = np.arange(N) / SR
end_t = next(c['t'] for c in cu['cues'] if c['type'] == 'endcard')
seg = cu['segments']
rng = np.random.default_rng(11)
def lp(x, fc): return sosfilt(butter(2, fc, 'low', fs=SR, output='sos'), x)
def hp(x, fc): return sosfilt(butter(2, fc, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def midi(n): return 440 * 2 ** ((n - 69) / 12)
def add(buf, sig, start):
    i = int(round(start * SR))
    if i < 0: sig, i = sig[-i:], 0
    if i >= len(buf): return
    j = min(len(buf), i + len(sig)); buf[i:j] += sig[: j - i]
def ramp(a, b): return np.clip((t_all - a) / max(b - a, 1e-3), 0, 1)

BPM = 100; beat = 60 / BPM; bar = 4 * beat
phase = (end_t % bar)  # first downbeat time so that a downbeat lands exactly on the end card
# I – V – vi – IV in D major, warm and optimistic
CH = [(50, [62, 66, 69, 74]), (45, [61, 64, 69, 73]), (47, [62, 66, 71, 74]), (43, [62, 67, 71, 74])]
pad, arp, bass, kick, hat, clap = (np.zeros(N) for _ in range(6))
def saw(f, n):
    t = np.arange(n) / SR
    return sum(2 * ((t * f * 2 ** (d / 12) + rng.random()) % 1) - 1 for d in (-.1, 0, .1)) / 3
b0 = -int(np.ceil(phase / bar)) - 1
for b in range(b0, int(DUR / bar) + 2):
    st = phase + b * bar
    root, notes = CH[b % 4]
    n = int((bar + .8) * SR); e = np.minimum(1, np.arange(n) / (.6 * SR)) * np.minimum(1, (n - np.arange(n)) / (.8 * SR))
    add(pad, sum(saw(midi(x), n) for x in notes) / 4 * e, st)
    for k in range(8):  # bass 8ths
        m = int(beat / 2 * SR); tt = np.arange(m) / SR
        add(bass, (np.sin(2 * np.pi * midi(root - 12) * tt) + .25 * np.sin(4 * np.pi * midi(root - 12) * tt)) * np.exp(-tt * 4), st + k * beat / 2)
    for k in range(8):  # gentle 8th-note pluck arp
        f = midi(notes[[0, 2, 1, 3, 2, 1, 3, 2][k]] + 12); m = int(.5 * SR); tt = np.arange(m) / SR
        add(arp, (np.sin(2 * np.pi * f * tt) + .3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 7), st + k * beat / 2)
    for k in range(4):
        tb = st + k * beat; m = int(.3 * SR); tt = np.arange(m) / SR
        add(kick, np.sin(2 * np.pi * np.cumsum(48 + 100 * np.exp(-tt * 32)) / SR) * np.exp(-tt * 10), tb)
        m = int(.05 * SR); tt = np.arange(m) / SR
        add(hat, hp(rng.standard_normal(m), 8000) * np.exp(-tt * 80), tb + beat / 2)
        if k in (1, 3):
            m = int(.18 * SR); tt = np.arange(m) / SR
            add(clap, bp(rng.standard_normal(m), 1000, 4000) * np.exp(-tt * 24), tb)

open_f = 900 + 2600 * ramp(seg[2], end_t)  # pad filter slowly opens across the demo: the "build"
padf = np.zeros(N); blk = 4096
for i in range(0, N, blk):  # block-wise time-varying low-pass
    c = float(open_f[min(i + blk // 2, N - 1)])
    s = max(0, i - 2048); padf[i:i + blk] = lp(pad[s:i + blk], c)[i - s:]
drums_in = ramp(seg[2] - .2, seg[2] + .3)
drums_out = 1 - ramp(end_t - .05, end_t + .25)
music = (padf * .30
         + lp(arp, 4500) * .10 * (0.6 + 0.4 * ramp(seg[2], end_t))
         + lp(bass, 350) * .28 * ramp(seg[1] - .3, seg[1] + .3) * (1 - .5 * ramp(end_t, end_t + 1.5))
         + kick * .40 * drums_in * drums_out
         + hat * .14 * drums_in * drums_out * (0.6 + 0.6 * ramp(seg[5], end_t))
         + clap * .22 * ramp(seg[7] - .2, seg[7] + .2) * drums_out)
music *= ramp(0, .6) * (1 - ramp(DUR - 1.6, DUR - .05))

sfx = np.zeros(N)
def chime(notes, amp=.09):
    out = np.zeros(int(4 * SR))
    for i, x in enumerate(notes):
        m = int(3.2 * SR); tt = np.arange(m) / SR; f = midi(x)
        s = sum(a * np.sin(2 * np.pi * f * h * tt) * np.exp(-tt * d) for h, a, d in [(1, 1, 1.6), (2, .35, 3), (3, .15, 5)])
        o = int(i * .07 * SR); out[o:o + m] += s[: len(out) - o] * amp
    return out
for c in cu['cues']:
    if c['type'] == 'click':
        m = int(.035 * SR); tt = np.arange(m) / SR
        add(sfx, (np.sin(2 * np.pi * 1800 * tt) * .5 + hp(rng.standard_normal(m), 2500) * .4) * np.exp(-tt * 220) * .22, c['t'])
# end card: soft swell into a low impact + chord chime on the downbeat
m = int(1.2 * SR); tt = np.arange(m) / SR
add(sfx, hp(rng.standard_normal(m), 1200) * (tt / 1.2) ** 3 * .08, end_t - 1.2)
m = int(1.8 * SR); tt = np.arange(m) / SR
add(sfx, np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-tt * 10)) / SR) * np.exp(-tt * 2.6) * .5, end_t)
add(sfx, chime([62, 66, 69, 74, 78]), end_t + .02)

mix = music + sfx
L = mix + .06 * np.roll(lp(arp, 4500), int(.013 * SR)); R = mix + .06 * np.roll(padf, int(.019 * SR))
st = np.tanh(np.stack([L, R], 1) * 1.15) / np.tanh(1.15)
st = st / np.max(np.abs(st)) * .89
wavfile.write('soundtrack.wav', SR, (st * 32767).astype(np.int16))
print('ok', round(DUR, 2), 'end card', round(end_t, 2), 'phase', round(phase, 3))
