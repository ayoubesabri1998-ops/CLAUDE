// Live preview for an episode page. Active only when the URL contains "?preview"
// (the renderer never adds it). Scales the 1080x1920 stage to the window and adds
// play / scrub controls; if the page sets data-preview-audio on <body>, that audio
// is played in sync and used as the clock.
(function () {
  if (!/[?&]preview\b/.test(location.search)) return;
  const ready = () => (window.prepare ? window.prepare() : Promise.resolve());
  window.addEventListener('load', () => ready().then(start));

  function start() {
    const stage = document.getElementById('stage');
    const de = document.documentElement, body = document.body;
    de.style.cssText += ';width:100%;height:100%;overflow:hidden;background:#0b0908';
    body.style.cssText += ';width:100%;height:100%;overflow:hidden;background:#0b0908;margin:0';
    const BAR = 64;
    const fit = () => {
      const k = Math.min((innerHeight - BAR) / 1920, innerWidth / 1080);
      stage.style.transformOrigin = '0 0';
      stage.style.position = 'absolute';
      stage.style.left = ((innerWidth - 1080 * k) / 2) + 'px';
      stage.style.top = '0px';
      stage.style.scale = k;   // separate from transform, which the episode uses for camera shake
    };
    fit(); addEventListener('resize', fit);

    const src = body.dataset.previewAudio;
    const audio = src ? new Audio(src) : null;
    const bar = document.createElement('div');
    bar.style.cssText = `position:fixed;left:0;right:0;bottom:0;height:${BAR}px;display:flex;align-items:center;gap:12px;padding:0 16px;background:#16120f;color:#efe5cc;font:600 15px system-ui,sans-serif;direction:ltr;z-index:99`;
    bar.innerHTML = `<button id="pv-play" style="width:84px;height:40px;border-radius:8px;border:0;background:#b3142a;color:#fff;font:700 15px system-ui">▶ Play</button>
      <input id="pv-seek" type="range" min="0" max="${DUR}" step="0.01" value="0" style="flex:1;accent-color:#b3142a">
      <span id="pv-time" style="width:120px;text-align:right;font-variant-numeric:tabular-nums">0.00 / ${DUR.toFixed(1)}</span>`;
    body.appendChild(bar);
    const btn = bar.querySelector('#pv-play'), seek = bar.querySelector('#pv-seek'), time = bar.querySelector('#pv-time');
    let t = 0, playing = false, t0 = 0, wall0 = 0;
    const show = () => { render(t); seek.value = t; time.textContent = `${t.toFixed(2)} / ${DUR.toFixed(1)}`; };
    const tick = () => {
      if (!playing) return;
      t = audio ? audio.currentTime : t0 + (performance.now() - wall0) / 1000;
      if (t >= DUR) { t = DUR; pause(); }
      show(); requestAnimationFrame(tick);
    };
    const play = () => { if (t >= DUR) t = 0; playing = true; btn.textContent = '❚❚ Pause'; t0 = t; wall0 = performance.now();
      if (audio) { audio.currentTime = t; audio.play().catch(() => {}); } requestAnimationFrame(tick); };
    const pause = () => { playing = false; btn.textContent = '▶ Play'; if (audio) audio.pause(); };
    btn.onclick = () => (playing ? pause() : play());
    seek.oninput = () => { t = +seek.value; if (audio) audio.currentTime = t; t0 = t; wall0 = performance.now(); show(); };
    addEventListener('keydown', e => {
      if (e.code === 'Space') { e.preventDefault(); playing ? pause() : play(); }
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        t = Math.max(0, Math.min(DUR, t + (e.key === 'ArrowRight' ? 1 : -1) * (e.shiftKey ? 0.1 : 1)));
        if (audio) audio.currentTime = t; t0 = t; wall0 = performance.now(); show();
      }
    });
    show();
  }
})();
