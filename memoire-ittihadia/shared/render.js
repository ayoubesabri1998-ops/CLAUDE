// Renders an episode page (index.html) frame by frame to a silent MP4.
//
//   node shared/render.js <episode>/index.html out.mp4 [--from F --to T]
//   node shared/render.js <episode>/index.html --stills 2,30.5,60 [outDir]
//   node shared/render.js <episode>/index.html --info        (prints DUR/FPS/frames as JSON)
//
// The page must expose: prepare() (async), render(t), DUR, FPS.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const { pathToFileURL } = require('url');

(async () => {
  const args = process.argv.slice(2);
  const pagePath = path.resolve(args[0] || 'index.html');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await page.goto(pathToFileURL(pagePath).href);
  await page.evaluate(() => prepare());
  const { DUR, FPS } = await page.evaluate(() => ({ DUR, FPS }));
  const N = Math.round(DUR * FPS);

  if (args.includes('--info')) {
    console.log(JSON.stringify({ DUR, FPS, frames: N }));
    await browser.close(); return;
  }

  const si = args.indexOf('--stills');
  if (si >= 0) {
    const outDir = args[si + 2] || '.';
    for (const t of args[si + 1].split(',').map(Number)) {
      await page.evaluate(t => render(t), t);
      const p = path.join(outDir, `still_${t}.png`);
      await page.screenshot({ path: p });
      console.log('saved', p);
    }
    await browser.close(); return;
  }

  const out = args[1] || 'silent.mp4';
  const fi = args.indexOf('--from'), ti = args.indexOf('--to');
  const F0 = fi >= 0 ? +args[fi + 1] : 0, F1 = ti >= 0 ? Math.min(N, +args[ti + 1]) : N;
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out],
    { stdio: ['pipe', 'ignore', 'inherit'] });
  for (let f = F0; f < F1; f++) {
    await page.evaluate(t => render(t), f / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if ((f - F0) % 60 === 0) process.stdout.write(`PROGRESS ${f - F0}/${F1 - F0}\n`);
  }
  process.stdout.write(`PROGRESS ${F1 - F0}/${F1 - F0}\n`);
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
})();
