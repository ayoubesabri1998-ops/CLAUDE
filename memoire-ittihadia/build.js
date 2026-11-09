#!/usr/bin/env node
// One-command build for an episode:  node build.js ep02   (or ep01)
//
//   --range 30:45    render only that time window (seconds) — quick check of an edit
//   --jobs 3         parallel render processes (default: CPU cores, max 6)
//   --audio-only     rebuild the audio mix and re-mux onto the last rendered picture
//
// Output: output/<episode>.mp4   (temporary files in output/tmp/)
const { spawn, spawnSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const ROOT = __dirname;
const EPISODES = {
  ep01: { dir: 'ep01-ben-barka', out: 'ep01-ben-barka.mp4', audio: 'bed' },
  ep02: { dir: 'ep02-bouabid', out: 'ep02-bouabid.mp4', audio: 'voice+music' },
};

const argv = process.argv.slice(2);
const epKey = argv.find(a => EPISODES[a]);
if (!epKey) { console.log('usage: node build.js ep01|ep02 [--range a:b] [--jobs n] [--audio-only]'); process.exit(1); }
const opt = k => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : null; };
const EP = EPISODES[epKey];
const epDir = path.join(ROOT, EP.dir);
const page = path.join(epDir, 'index.html');
const outDir = path.join(ROOT, 'output'), tmp = path.join(outDir, 'tmp');
fs.mkdirSync(tmp, { recursive: true });

// ---------- helpers ----------
function run(cmd, args, o = {}) {
  const r = spawnSync(cmd, args, { encoding: 'utf8', maxBuffer: 1 << 26, ...o });
  if (r.error) throw new Error(`${cmd}: ${r.error.message}`);
  if (r.status !== 0) throw new Error(`${cmd} failed:\n${(r.stderr || '').slice(-2000)}`);
  return r;
}
function findPython() {
  for (const c of ['python3', 'python', 'py']) {
    const r = spawnSync(c, ['-c', 'import numpy'], { encoding: 'utf8' });
    if (r.status === 0) return c;
  }
  throw new Error('Python with numpy not found. Install Python 3, then: pip install numpy');
}
function lufs(file, filter = '') {
  const r = run('ffmpeg', ['-hide_banner', '-nostats', '-i', file, '-af', (filter ? filter + ',' : '') + 'ebur128', '-f', 'null', '-'], {});
  const m = [...r.stderr.matchAll(/^\s+I:\s+(-?[\d.]+) LUFS/gm)].pop();
  return m ? +m[1] : null;
}
function peak(file) {
  const r = run('ffmpeg', ['-hide_banner', '-nostats', '-i', file, '-af', 'volumedetect', '-f', 'null', '-']);
  return +r.stderr.match(/max_volume: (-?[\d.]+) dB/)[1];
}
function duration(file) {
  return +run('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', file]).stdout.trim();
}
const info = JSON.parse(run('node', [path.join(ROOT, 'shared', 'render.js'), page, '--info']).stdout.trim().split('\n').pop());
const FPS = info.FPS;

// ---------- picture ----------
async function renderPicture(silent) {
  let F0 = 0, F1 = info.frames;
  const range = opt('--range');
  if (range) { const [a, b] = range.split(':').map(Number); F0 = Math.round(a * FPS); F1 = Math.min(info.frames, Math.round(b * FPS)); }
  const jobs = Math.max(1, Math.min(+(opt('--jobs') || Math.min(6, os.cpus().length)), F1 - F0));
  const step = Math.ceil((F1 - F0) / jobs);
  console.log(`▶ rendering frames ${F0}–${F1} (${((F1 - F0) / FPS).toFixed(1)} s) with ${jobs} processes…`);
  const done = new Array(jobs).fill(0), totals = [];
  const t0 = Date.now();
  const parts = await Promise.all([...Array(jobs).keys()].map(i => new Promise((res, rej) => {
    const a = F0 + i * step, b = Math.min(F1, a + step), part = path.join(tmp, `part${i}.mp4`);
    totals[i] = b - a;
    const p = spawn('node', [path.join(ROOT, 'shared', 'render.js'), page, part, '--from', String(a), '--to', String(b)]);
    p.stdout.on('data', d => {
      const m = [...String(d).matchAll(/PROGRESS (\d+)\/(\d+)/g)].pop();
      if (m) { done[i] = +m[1]; const s = done.reduce((x, y) => x + y, 0), T = totals.reduce((x, y) => x + y, 0);
        const el = (Date.now() - t0) / 1000, eta = s ? el / s * (T - s) : 0;
        process.stdout.write(`\r  ${s}/${T} frames · ${Math.round(100 * s / T)}% · ~${Math.ceil(eta / 60)} min left   `); }
    });
    p.stderr.on('data', d => process.stderr.write(d));
    p.on('close', c => (c === 0 ? res(part) : rej(new Error('render process failed'))));
  })));
  process.stdout.write('\n');
  const list = path.join(tmp, 'parts.txt');
  fs.writeFileSync(list, parts.map(p => `file '${p.replace(/'/g, "'\\''")}'`).join('\n'));
  run('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', silent]);
  return { F0, F1 };
}

// ---------- audio ----------
function buildAudio(mix) {
  const py = findPython();
  if (EP.audio === 'bed') {
    console.log('▶ generating music bed…');
    run(py, [path.join(epDir, 'make_audio.py'), mix], { cwd: epDir });
    return;
  }
  // ep02: untouched voice + licensed music (ducked under the voice) + stamp/impact effects
  const A = f => path.join(epDir, 'audio', f);
  const sfx = path.join(tmp, 'sfx.wav'), pre = path.join(tmp, 'mix_pre.wav');
  console.log('▶ generating stamp/impact effects…');
  run(py, [path.join(epDir, 'make_audio.py'), sfx, '--sfx-only', '--no-whoosh'], { cwd: epDir });
  const voice = A('voiceover_edit.flac'), music = A('music_methodus.flac');
  const DUR = info.DUR, mDur = duration(music);
  if (Math.abs(mDur - DUR) > 0.5) console.log(`  ⚠ music is ${mDur.toFixed(1)} s but the video is ${DUR.toFixed(1)} s — it will be trimmed/padded. (Ask for a new edit of the track at ${DUR.toFixed(2)} s.)`);
  const vL = lufs(voice, 'pan=stereo|c0=c0|c1=c0'), mL = lufs(music);
  const MUSIC_BELOW_VOICE = 13;   // dB — raise to make the music quieter
  const g = (vL - MUSIC_BELOW_VOICE - mL).toFixed(1);
  console.log(`▶ mixing: voice ${vL} LUFS, music ${mL} LUFS → music gain ${g} dB`);
  const fc = `[0:a]atrim=0:${DUR},apad=whole_dur=${DUR},volume=${g}dB,afade=t=in:d=0.4,afade=t=out:st=${(DUR - 3).toFixed(2)}:d=3[mu];` +
    `[1:a]volume=-5dB[fx];[2:a]adelay=500,apad,pan=stereo|c0=c0|c1=c0,asplit=2[v1][vsc];` +
    `[mu][vsc]sidechaincompress=threshold=0.012:ratio=5:attack=25:release=450[mud];[mud][fx][v1]amix=inputs=3:normalize=0:duration=first`;
  run('ffmpeg', ['-y', '-loglevel', 'error', '-i', music, '-i', sfx, '-i', voice, '-filter_complex', fc, '-c:a', 'pcm_s24le', pre]);
  const up = (-1 - peak(pre)).toFixed(1);   // plain gain only: loudest peak at -1 dBFS, no limiter
  run('ffmpeg', ['-y', '-loglevel', 'error', '-i', pre, '-af', `volume=${up}dB`, '-c:a', 'pcm_s16le', mix]);
}

// ---------- main ----------
(async () => {
  const t0 = Date.now();
  const silent = path.join(tmp, 'silent.mp4'), mix = path.join(tmp, 'mix.wav');
  let range = null;
  if (!argv.includes('--audio-only') || !fs.existsSync(silent)) range = await renderPicture(silent);
  buildAudio(mix);
  const isRange = range && (range.F0 > 0 || range.F1 < info.frames);
  const out = path.join(outDir, isRange ? EP.out.replace('.mp4', `_${(range.F0 / FPS).toFixed(0)}-${(range.F1 / FPS).toFixed(0)}s.mp4`) : EP.out);
  const audioIn = isRange ? ['-ss', String(range.F0 / FPS), '-i', mix] : ['-i', mix];
  console.log('▶ final encode…');
  run('ffmpeg', ['-y', '-loglevel', 'error', '-i', silent, ...audioIn, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow',
    '-crf', '24', '-maxrate', '6M', '-bufsize', '12M', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out]);
  // keep a copy of the full mix next to the episode so the browser preview plays the current sound
  if (!isRange) run('ffmpeg', ['-y', '-loglevel', 'error', '-i', mix, '-c:a', 'aac', '-b:a', '160k', path.join(epDir, 'audio', 'preview_mix.m4a')]);
  console.log(`✔ ${path.relative(ROOT, out)}  (${duration(out).toFixed(1)} s, ${((Date.now() - t0) / 60000).toFixed(1)} min)`);
})().catch(e => { console.error('\n✖', e.message); process.exit(1); });
