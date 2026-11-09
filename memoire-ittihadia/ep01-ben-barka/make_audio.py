"""Synthesizes a placeholder music bed (dark drone + hits on scene cuts).
Original, royalty-free: generated from scratch. Replace with licensed music if you like."""
import numpy as np, wave, sys

SR, DUR = 48000, 42.0
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)

def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR); y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):  # one-pole (fine for short buffers)
        acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y

def fade(n, a, r):
    e = np.ones(n); a = int(a * SR); r = int(r * SR)
    e[:a] = np.linspace(0, 1, a); e[n - r:] = np.linspace(1, 0, r); return e

L = np.zeros(N); R = np.zeros(N)

# 1) drone: D minor-ish pad, slow beating, swells
lfo = 0.6 + 0.4 * np.sin(2 * np.pi * t / 9)
for f, a, det in [(73.42, .30, .15), (110.0, .16, .2), (146.83, .10, .3), (174.61, .06, .25), (220.0, .035, .4)]:
    L += a * lfo * np.sin(2 * np.pi * (f - det) * t + .3 * np.sin(2 * np.pi * .1 * t))
    R += a * lfo * np.sin(2 * np.pi * (f + det) * t)
air = rng.standard_normal(N // 8)
air = np.repeat(lowpass(air, 300), 8)[:N] * .5
L += air * .25; R += np.roll(air, 2400) * .25
env = fade(N, 1.5, 3.0)
# duck the drone during the abduction moment, swell back for the counter
env *= 1 - .5 * np.clip((t - 28.8) / .4, 0, 1) * np.clip((31.8 - t) / .6, 0, 1)
L *= env; R *= env

# 2) impacts on scene cuts
def boom(at, gain=1.0):
    n = int(2.5 * SR); tt = np.arange(n) / SR
    f = 38 + 70 * np.exp(-tt * 9)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.2)
    click = rng.standard_normal(n) * np.exp(-tt * 60) * .3
    s = (s + click) * gain
    i = int(at * SR); m = min(n, N - i)
    L[i:i + m] += s[:m]; R[i:i + m] += s[:m]

def whoosh(end, length=.7, gain=.35):
    n = int(length * SR); tt = np.linspace(0, 1, n)
    x = lowpass(rng.standard_normal(n), 1800) * (tt ** 2.5) * gain * 3
    i = int((end - length) * SR)
    L[i:i + n] += x * np.linspace(.4, 1, n); R[i:i + n] += x * np.linspace(1, .4, n)

def tick(at, gain=.12):
    n = int(.03 * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 300) * gain
    i = int(at * SR); L[i:i + n] += s; R[i:i + n] += s

boom(0.0, .8)
for c in [4.5, 10.0, 19.0, 25.0, 32.0, 37.0]:
    whoosh(c); boom(c, .9)
boom(29.2, 1.3)                                       # stamp slam
for k in range(18): tick(.5 + k * .08)                # date digits rolling
for a in [11.0, 12.8, 14.6, 16.4]: tick(a, .25)       # timeline dots
for k in range(30): tick(32.4 + 2.0 * (k / 30) ** 2, .1)  # counter

# 3) simple reverb (feedback delays) + master
def verb(x):
    y = x.copy()
    for d, g in [(1601, .35), (2399, .3), (3203, .25), (4801, .2)]:
        z = np.zeros_like(x); z[d:] = x[:-d] * g; y += z
    return y
L, R = verb(L), verb(R)
mx = max(np.abs(L).max(), np.abs(R).max())
L, R = L / mx * .6, R / mx * .6
pcm = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'bed.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok')
