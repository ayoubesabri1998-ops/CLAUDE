"""Placeholder music bed for episode 02 (same sound design as episode 01):
dark drone, whoosh + boom on scene cuts, a big hit on the name reveal with the
drone ducking just before it, stamp thuds, typewriter ticks. Generated from
scratch, royalty-free."""
import numpy as np, wave, sys, re, json, os

# The composition's time-warp table: [real time, internal time]. Every event below is
# written in internal time and mapped to real time, so audio follows any retiming.
_html = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'), encoding='utf-8').read()
WARP = json.loads(re.search(r'const WARP = (\[.*?\]);', _html).group(1))
def rt(ti):
    """internal time -> real time"""
    for (r0, i0), (r1, i1) in zip(WARP, WARP[1:]):
        if ti <= i1: return r0 + (r1 - r0) * max(0.0, (ti - i0) / (i1 - i0))
    return WARP[-1][0]

SR, DUR = 48000, float(WARP[-1][0])
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(11)

def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR); y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y

def fade(n, a, r):
    e = np.ones(n); a = int(a * SR); r = int(r * SR)
    e[:a] = np.linspace(0, 1, a); e[n - r:] = np.linspace(1, 0, r); return e

L = np.zeros(N); R = np.zeros(N)

# drone (D minor-ish pad with slow beating)
lfo = 0.6 + 0.4 * np.sin(2 * np.pi * t / 9)
for f, a, det in [(73.42, .30, .15), (110.0, .16, .2), (146.83, .10, .3), (174.61, .06, .25), (220.0, .035, .4)]:
    L += a * lfo * np.sin(2 * np.pi * (f - det) * t + .3 * np.sin(2 * np.pi * .1 * t))
    R += a * lfo * np.sin(2 * np.pi * (f + det) * t)
air = np.repeat(lowpass(rng.standard_normal(N // 8), 300), 8)[:N] * .5
L += air * .25; R += np.roll(air, 2400) * .25
env = fade(N, 1.5, 3.5)
# tension before the name: drone sinks to near-silence, then slams back on the hit
env *= 1 - .85 * np.clip((t - rt(17.0)) / (rt(18.6) - rt(17.0)), 0, 1) * (t < rt(18.6))
L *= env; R *= env
if '--sfx-only' in sys.argv:   # music track replaces the drone; keep impacts, stamps, ticks
    L[:] = 0; R[:] = 0

def boom(at, gain=1.0):
    n = int(2.5 * SR); tt = np.arange(n) / SR
    f = 38 + 70 * np.exp(-tt * 9)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.2)
    s = (s + rng.standard_normal(n) * np.exp(-tt * 60) * .3) * gain
    i = int(at * SR); m = min(n, N - i)
    L[i:i + m] += s[:m]; R[i:i + m] += s[:m]

def whoosh(end, length=.7, gain=.35):
    n = int(length * SR); tt = np.linspace(0, 1, n)
    x = lowpass(rng.standard_normal(n), 1800) * (tt ** 2.5) * gain * 3
    i = int((end - length) * SR)
    L[i:i + n] += x * np.linspace(.4, 1, n); R[i:i + n] += x * np.linspace(1, .4, n)

def tick(at, gain=.12, freq=2400):
    n = int(.03 * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * tt) * np.exp(-tt * 300) * gain
    i = int(at * SR); L[i:i + n] += s; R[i:i + n] += s

boom(0.0, .8)
whoosh(rt(4.2), .5); boom(rt(4.2), .7)                    # coin tears
for c in [12, 21, 29, 36, 64, 75, 82, 88, 98, 108, 118, 123]:
    whoosh(rt(c)); boom(rt(c), .9)
whoosh(rt(18.6), 1.4, .5); boom(rt(18.6), 1.7); boom(rt(18.6) + .02, .6)  # the name
for s_ in [1.9, 5.8, 15.0, 16.4, 19.6, 22.6, 33.8, 77.6, 85.2]:
    boom(rt(s_ + .2), .55)                               # stamps
boom(rt(94.6), 1.1)                                      # government dismissed
boom(rt(108.6), 1.2)                                     # 1981 arrest
for k in range(34): tick(rt(82.9 + 3.1 * k / 34) + rng.uniform(-.02, .02), .1, 1800 + rng.uniform(0, 900))  # typewriter
for w in [40.0, 47.0, 52.6, 56.8, 60.8]: tick(rt(w + .3), .2)  # "why?" strips
for k in range(10): tick(rt(118.2 + 1.8 * (k / 10) ** .7), .08, 3200)  # coin spin
whoosh(rt(120.6), 1.0, .45); boom(rt(120.6), 1.4)        # the name, last time

def verb(x):
    y = x.copy()
    for d, g in [(1601, .35), (2399, .3), (3203, .25), (4801, .2)]:
        z = np.zeros_like(x); z[d:] = x[:-d] * g; y += z
    return y
L, R = verb(L), verb(R)
mx = max(np.abs(L).max(), np.abs(R).max())
L, R = L / mx * .6, R / mx * .6
pcm = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(next((x for x in sys.argv[1:] if not x.startswith('--')), 'bed.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok')
