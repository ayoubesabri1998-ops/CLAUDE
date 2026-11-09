"""Voiceover edit for episode 02.

1. noise reduction (profile = the silent lead-in before the first word)
2. speech islands found by an energy VAD on the denoised signal
3. retakes / dead air removed (ranges found from the word-level transcript)
4. pauses re-timed: tight inside sentences, a breath between paragraphs
5. writes the edited (un-processed) voice + a JSON map raw->edited time,
   and the scene anchors used to re-time the video (WARP)

usage: python3 vo_edit.py raw.wav words.json outdir
"""
import json, sys, wave
import numpy as np
import noisereduce as nr

src, words_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
RAW_OUT = '--processed' not in sys.argv   # default: cut the ORIGINAL audio, untouched
w = wave.open(src); SR = w.getframerate(); nch = w.getnchannels(); sw = w.getsampwidth()
raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.uint8)
if sw == 3:  # 24-bit PCM
    b = raw.reshape(-1, 3); x = (b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8) | (b[:, 2].astype(np.int32) << 16))
    x = np.where(x >= 1 << 23, x - (1 << 24), x).astype(np.float32) / (1 << 23)
else:
    x = np.frombuffer(raw.tobytes(), np.int16).astype(np.float32) / 32768
if nch > 1: x = x.reshape(-1, nch).mean(1)
W = [wd for s in json.load(open(words_path, encoding='utf-8')) for wd in s['words']]
FIRST_WORD = W[0]['s']

# ---- 1. noise reduction --------------------------------------------------------
noise = x[int(.5 * SR):int((FIRST_WORD - .3) * SR)]
y = nr.reduce_noise(y=x, sr=SR, y_noise=noise, stationary=True, prop_decrease=.92, n_fft=2048)
y = y.astype(np.float32)

# ---- 2. VAD -----------------------------------------------------------------------
hop = int(.01 * SR)
fr = y[:len(y) // hop * hop].reshape(-1, hop)
db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
floor = np.median(db[int(.5 / .01):int((FIRST_WORD - .3) / .01)])
speech_peak = np.percentile(db, 97)
thr = max(floor + 30, speech_peak - 22)   # word cores
on = db > thr
# hangover: close gaps < 220 ms, drop blips < 80 ms
isl, i, n = [], 0, len(on)
while i < n:
    if on[i]:
        j = i
        while j < n and on[j]: j += 1
        isl.append([i, j]); i = j
    else: i += 1
merged = []
for a, b in isl:
    if merged and a - merged[-1][1] < 22: merged[-1][1] = b
    else: merged.append([a, b])
# hysteresis: grow each island outward while there is still sound above the floor,
# so soft word endings (e.g. the tail of «الفلوس», «بوعبيد») are not clipped
low = max(floor + 18, speech_peak - 62)
grown = []
for a, b in merged:
    if b - a < 8: continue
    k = 0   # backward: bridge dips up to 80 ms, at most 250 ms
    while a > 8 and db[a - 8:a].max() > low and k < 25: a -= 1; k += 1
    k = 0   # forward: bridge dips up to 120 ms (soft final consonants), at most 550 ms
    while b < n - 12 and db[b:b + 12].max() > low and k < 55: b += 1; k += 1
    if grown and a <= grown[-1][1] + 2: grown[-1][1] = max(grown[-1][1], b)
    else: grown.append([a, b])
islands = [[a * .01, b * .01] for a, b in grown]

# ---- 3. remove dead air + retakes (raw seconds, from the transcript) ----------------
REMOVE = [(0, FIRST_WORD - .25),       # lead-in
          (131.40, 136.40),            # stumbled first take of "ولكن الإصلاحات ما وقفوش…"
          (151.50, 155.00),            # aborted first take of "وفنفس الحكومة تأسس الصندوق…"
          (185.30, 212.90),            # 2 aborted takes of "ومن بعد واصل عبد الرحيم بوعبيد…"
          (221.50, 227.20),            # «قبل ما يتولى قيادة الاتحاد الاشتراكي سنة 1975» — wrong connector, cut per feedback
          (226.00, 231.60),            # aborted first take of "وفعام 1981 تعتقل بسبب…"
          (243.28, 251.20),            # aborted first take of the quote
          (W[-1]['e'] + .25, 1e9)]     # anything after the last word
def removed(t): return any(a <= t < b for a, b in REMOVE)
keep = [[a, b] for a, b in islands if not removed((a + b) / 2)]
# drop breaths / mouth noises: short and quiet islands
def peak_db(a, b): return db[int(a / .01):int(b / .01)].max()
keep = [[a, b] for a, b in keep if not (b - a < .35 and peak_db(a, b) < speech_peak - 18)]
PRE, POST = .05, .12
keep = [[max(0, a - PRE), min(len(y) / SR, b + POST)] for a, b in keep]
_m = []
for a, b in keep:                      # padded neighbours that touch become one segment
    if _m and a <= _m[-1][1]: _m[-1][1] = max(_m[-1][1], b)
    else: _m.append([a, b])
keep = _m

# ---- 4. re-time pauses ----------------------------------------------------------------
def wstart(token, near, tol=4):
    c = [wd for wd in W if token in wd['w'] and abs(wd['s'] - near) < tol]
    return min(c, key=lambda wd: abs(wd['s'] - near))
PARAGRAPHS = [35.24, 45.92, 66.62, 78.66, 131.66, 165.36, 212.98, 232.5, 259.04]   # raw starts of paragraph openers
NAME1 = wstart('عبد', 44.9)['s']
def new_gap(g, nxt_start, prev_end):
    if any(prev_end - .2 <= p <= nxt_start + .3 for p in PARAGRAPHS): return .48
    if abs(nxt_start - NAME1) < .35: return .32          # tiny suspense before the name
    if g < .15: return g
    return float(np.clip(g * .4, .10, .24))
# room tone from the quietest 2 s of the lead-in, used to fill the tightened gaps
src_sig = x if RAW_OUT else y
_h = int(.1 * SR); lead = src_sig[int(.5 * SR):int((FIRST_WORD - .4) * SR)]
_e = np.array([np.sqrt((lead[i:i + 2 * SR] ** 2).mean()) for i in range(0, len(lead) - 2 * SR, _h)])
_i = int(_e.argmin()) * _h; ROOM = lead[_i:_i + 2 * SR].copy()
def room(nsamp):
    reps = int(np.ceil(nsamp / len(ROOM))) + 1
    r = np.tile(ROOM, reps)[:nsamp].copy() if RAW_OUT else np.zeros(nsamp, np.float32)
    return r
edit, segs, t = [], [], 0.0
fade = int(.015 * SR)
for k, (a, b) in enumerate(keep):
    if k:
        g = new_gap(a - keep[k - 1][1], a + PRE, keep[k - 1][1] - POST)
        edit.append(room(int(g * SR))); t += g
    seg = src_sig[int(a * SR):int(b * SR)].copy()
    if RAW_OUT:   # crossfade speech <-> room tone instead of fading to digital silence
        rt = room(fade)
        seg[:fade] = seg[:fade] * np.linspace(0, 1, fade) + rt * np.linspace(1, 0, fade)
        seg[-fade:] = seg[-fade:] * np.linspace(1, 0, fade) + rt * np.linspace(0, 1, fade)
    else:
        seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    segs.append({'raw': [a, b], 'edit': [t, t + (b - a)]})
    edit.append(seg); t += b - a
vo = np.concatenate(edit)

def raw2edit(tr):
    for s in segs:
        if tr <= s['raw'][1]:
            return s['edit'][0] + max(0.0, tr - s['raw'][0])
    return segs[-1]['edit'][1]

# ---- 5. anchors for the video (internal composition time <- edited voice time) -------------
A = lambda tok, near: raw2edit(wstart(tok, near)['s'])
anchors = [
    ('stamp', 1.9, A('قبل', 15.3)), ('problem', 4.2, A('حتى', 19.3)), ('istiqlal', 8.0, A('يعني', 28.5)),
    ('flous', 9.9, A('ولكن', 30.0)), ('choc', 12, A('واللي', 35.3)), ('c1', 14.0, A('خابر', 38.5)),
    ('c2', 15.4, A('رجل', 40.2)), ('bal', 17.0, A('بل', 41.6)), ('name1', 18.6, raw2edit(NAME1)),
    ('paradox', 21, A('تزاد', 46)), ('notfin', 25.3, A('متخصص', 59)), ('fahem', 26.9, A('ولكن', 61.0)),
    ('vision', 29, A('لم', 66.7)), ('minister', 32.4, A('نائب', 72)), ('gov', 33.8, A('حكومة', 75.8)),
    ('y1959', 36, A('وفي', 78.7)), ('bam', 38.3, A('30', 85.5)), ('dirham', 44.3, A('وفي', 100.9)),
    ('cdg', 51.0, A('وفي', 109.5)), ('bnde', 55.3, A('والبنك', 117.7)), ('bmce', 59.3, A('والبنك', 122.4)),
    ('industry', 64, raw2edit(137.88)), ('samir', 66.6, A('سامير', 142)), ('somaca', 68.0, A('سومكة', 144.5)),
    ('build', 69.6, A('يبدأ', 147.5)), ('jobs', 71.6, A('فرص', 149.5)),
    ('cnss', 75, A('وفي', 150.9)), ('plan', 82, A('وتوجد', 162.5)),
    ('synth', 88, A('رجل', 165.4)), ('vision2', 91.6, A('صدفة', 173)), ('y1960', 94.4, A('تفات', 176.5)),
    ('legacy', 95.8, A('ولكن', 178)), ('struggle', 98, A('ومن', 213)), ('unfp', 100.0, A('وساهم', 217.5)),
    ('y1981', 108, A('وفي', 226.3)), ('position', 109.4, raw2edit(236.0)),
    ('court', 110.9, A('وقال', 238.8)), ('quote', 111.6, A('ربي', 251.3)),
    ('callback', 118, A('والمرة', 259.1)), ('remember', 119.4, A('تذكر', 263)), ('name2', 120.6, A('عبد', 264.8)),
]
vo_end = len(vo) / SR
json.dump({'sr': SR, 'duration': vo_end, 'segments': segs, 'anchors': anchors, 'thr_db': float(thr), 'floor_db': float(floor)},
          open(f'{out}/edit_map.json', 'w'), ensure_ascii=False, indent=1)
pcm = (np.clip(vo, -1, 1) * 32767).astype(np.int16)   # no gain, no processing
with wave.open(f'{out}/vo_edit.wav', 'wb') as o:
    o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes(pcm.tobytes())
print(f'raw {len(x) / SR:.1f}s -> edited {vo_end:.1f}s · islands kept {len(keep)} · VAD thr {thr:.1f} dB (floor {floor:.1f})')
for name, ti, te in anchors: print(f'  {name:9s} internal {ti:6.1f}  ->  voice {te:6.2f}')
