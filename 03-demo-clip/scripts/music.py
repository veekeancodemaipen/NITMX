"""Original synthesized soundtrack + SFX for the demo clip, synced to timeline.json cues."""
import json, sys
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 44100
tl = json.load(open('timeline.json'))
DUR = tl['end'] + 0.5
N = int(DUR * SR)
rng = np.random.default_rng(7)
t_all = np.arange(N) / SR

def lp(x, fc, order=2): return sosfilt(butter(order, fc, 'low', fs=SR, output='sos'), x)
def hp(x, fc, order=2): return sosfilt(butter(order, fc, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def midi(n): return 440 * 2 ** ((n - 69) / 12)
def add(buf, sig, start):
    i = int(start * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(sig)); buf[i:j] += sig[: j - i]

BPM = 104
beat = 60 / BPM
bar = 4 * beat
# vi - IV - I - V in C major (Am F C G), voiced around middle C
CHORDS = [(57, [57, 60, 64, 69]), (53, [53, 57, 60, 65]), (48, [55, 60, 64, 67]), (55, [55, 59, 62, 67])]

intro_end = next(c['t'] for c in tl['cues'] if c['type'] == 'whoosh')  # title card ends
outro_t = next(c['t'] for c in tl['cues'] if c['type'] == 'outro')

pad = np.zeros(N); arp = np.zeros(N); bass = np.zeros(N); drums = np.zeros(N)

def supersaw(f, n, det=(-0.12, -0.05, 0, 0.05, 0.12)):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for d in det:
        ff = f * 2 ** (d / 12)
        out += 2 * ((t * ff + rng.random()) % 1) - 1
    return out / len(det)

def env_adsr(n, a, r):
    e = np.ones(n); ai = int(a * SR); ri = int(r * SR)
    e[:ai] = np.linspace(0, 1, ai); e[-ri:] *= np.linspace(1, 0, ri)
    return e

nbars = int(np.ceil(DUR / bar)) + 1
for b in range(nbars):
    root, notes = CHORDS[b % 4]
    st = b * bar
    n = int((bar + 0.6) * SR)
    # pad
    s = sum(supersaw(midi(x), n) for x in notes) / len(notes)
    add(pad, s * env_adsr(n, 0.5, 0.8), st)
    # bass: root on 8ths with a pumping envelope
    for k in range(8):
        bn = int(beat / 2 * SR); tt = np.arange(bn) / SR
        f = midi(root - 12)
        sig = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)
        add(bass, sig * np.exp(-tt * 5) * (0.8 if k % 2 else 1.0), st + k * beat / 2)
    # arp: 16ths over chord tones an octave up
    pattern = [0, 1, 2, 3, 2, 1, 3, 2]
    for k in range(16):
        f = midi(notes[pattern[k % 8]] + 12)
        an = int(0.35 * SR); tt = np.arange(an) / SR
        tri = 2 * np.abs(2 * ((tt * f) % 1) - 1) - 1
        sig = (0.7 * tri + 0.3 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt * 14)
        add(arp, sig * (1.0 if k % 4 == 0 else 0.7), st + k * beat / 4)
    # drums
    for k in range(4):
        tb = st + k * beat
        kn = int(0.35 * SR); tt = np.arange(kn) / SR
        ph = 2 * np.pi * np.cumsum(45 + 110 * np.exp(-tt * 30)) / SR
        add(drums, np.sin(ph) * np.exp(-tt * 9) * 1.0, tb)
        hn = int(0.06 * SR); tt = np.arange(hn) / SR
        add(drums, hp(rng.standard_normal(hn), 7000) * np.exp(-tt * 70) * 0.35, tb + beat / 2)
        if k in (1, 3):
            cn = int(0.2 * SR); tt = np.arange(cn) / SR
            add(drums, bp(rng.standard_normal(cn), 900, 3500) * np.exp(-tt * 22) * 0.45, tb)

pad = lp(pad, 1800) * 0.32
arp = lp(arp, 5000) * 0.13
bass = lp(bass, 400) * 0.30
drums = drums * 0.42

# arrangement: intro = pad only; arp after title; drums+bass once the demo plays; drop drums for outro
def ramp(t, a, b): return np.clip((t - a) / max(b - a, 1e-3), 0, 1)
play_t = next(c['t'] for c in tl['cues'] if c['type'] == 'play')
m_arp = ramp(t_all, intro_end - 1.0, intro_end + 1.0)
m_bass = ramp(t_all, intro_end, intro_end + 2) * 0.6 + ramp(t_all, play_t - 0.5, play_t + 0.5) * 0.4
m_drum = ramp(t_all, play_t - beat, play_t) * (1 - ramp(t_all, outro_t - 0.2, outro_t + 0.6))
music = pad + arp * m_arp + bass * m_bass * (1 - 0.6 * ramp(t_all, outro_t, outro_t + 1)) + drums * m_drum
# fade in/out
music *= ramp(t_all, 0, 1.5) * (1 - ramp(t_all, DUR - 3.5, DUR - 0.2))

# ---- SFX ----
sfx = np.zeros(N)
def whoosh(d=0.7):
    n = int(d * SR); tt = np.arange(n) / SR
    noise = rng.standard_normal(n)
    out = np.zeros(n); seg = 512
    for i in range(0, n, seg):  # sweeping band
        c = 300 + 5000 * np.sin(np.pi * i / n) ** 2
        chunk = noise[max(0, i - 2048): i + seg]
        out[i:i + seg] = bp(chunk, c * 0.6, min(c * 1.6, 18000))[-len(out[i:i + seg]):]
    return out * np.sin(np.pi * tt / d) ** 2 * 0.35
def click():
    n = int(0.03 * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2200 * tt) * 0.5 + hp(rng.standard_normal(n), 3000) * 0.4) * np.exp(-tt * 260) * 0.5
def ping(base=1318.5):
    n = int(1.2 * SR); tt = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * base * m * tt) * np.exp(-tt * dcy) for m, a, dcy in [(1, 1, 4), (2, .4, 6), (3, .2, 9), (4.2, .1, 12)])
    s2 = sum(a * np.sin(2 * np.pi * base * 1.5 * m * tt) * np.exp(-tt * dcy) for m, a, dcy in [(1, .7, 4), (2, .25, 7)])
    out = s.copy(); out[int(0.09 * SR):] += s2[: n - int(0.09 * SR)]
    return out * 0.11
def riser_impact(d=2.0):
    n = int(d * SR); tt = np.arange(n) / SR
    r = hp(rng.standard_normal(n), 1500) * (tt / d) ** 2 * 0.12
    ni = int(1.6 * SR); ti = np.arange(ni) / SR
    imp = (np.sin(2 * np.pi * np.cumsum(40 + 80 * np.exp(-ti * 12)) / SR) * np.exp(-ti * 3) * 0.6
           + lp(rng.standard_normal(ni), 2500) * np.exp(-ti * 5) * 0.25)
    return r, imp
def chord_chime(notes):
    out = np.zeros(int(3.5 * SR))
    for i, x in enumerate(notes):
        p = ping(midi(x)) * 1.3
        out[int(i * 0.12 * SR): int(i * 0.12 * SR) + len(p)] += p[: len(out) - int(i * 0.12 * SR)]
    return out

for c in tl['cues']:
    t = c['t']
    if c['type'] == 'whoosh': add(sfx, whoosh(), max(0, t - 0.15))
    elif c['type'] == 'click': add(sfx, click(), t)
    elif c['type'] == 'ping': add(sfx, ping(), t + 0.05)
    elif c['type'] == 'play': add(sfx, chord_chime([69, 72, 76]) * 0.8, t + 0.1)
    elif c['type'] == 'intro':
        add(sfx, chord_chime([60, 64, 67, 72]), 0.5)
    elif c['type'] == 'outro':
        r, imp = riser_impact()
        add(sfx, r, t - 2.0); add(sfx, imp, t)
        add(sfx, chord_chime([57, 60, 64, 69, 72]), t + 0.3)

# duck music under SFX a little
env = np.abs(sfx); env = lp(env, 8, 1); duck = 1 - np.clip(env * 2.5, 0, 0.35)
mix = music * duck + sfx
# stereo: slight width on pad/arp via delay
L = mix + 0.08 * np.roll(arp * m_arp, int(0.011 * SR))
R = mix + 0.08 * np.roll(pad, int(0.017 * SR))
st = np.stack([L, R], 1)
st = np.tanh(st * 1.1) / np.tanh(1.1)
st = st / np.max(np.abs(st)) * 0.89
wavfile.write('soundtrack.wav', SR, (st * 32767).astype(np.int16))
print('wrote soundtrack.wav', DUR)
