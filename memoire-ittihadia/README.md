# ذاكرة اتحادية · مشروع الفيديوهات (نسخة محلية)

مشروع موشن غرافيك بأسلوب القصاصات الورقية، كل حلقة صفحة HTML تُصيَّر إلى فيديو عمودي 1080×1920.

| الحلقة | المجلد | الفيديو النهائي الحالي |
|---|---|---|
| 01 · المهدي بن بركة | `ep01-ben-barka/` | `ep01-ben-barka/ben-barka-demo.mp4` |
| 02 · عبد الرحيم بوعبيد | `ep02-bouabid/` | `ep02-bouabid/bouabid-ep02.mp4` |

---

## 1. التثبيت (مرة واحدة فقط)

ثبّت هذه البرامج الثلاثة:

| البرنامج | Windows | Mac |
|---|---|---|
| **Node.js** (نسخة 18 أو أحدث) | من nodejs.org | `brew install node` |
| **FFmpeg** | `winget install Gyan.FFmpeg` | `brew install ffmpeg` |
| **Python 3** + numpy | من python.org ثم `pip install numpy` | `brew install python` ثم `pip3 install numpy` |

بعد ذلك، افتح الطرفية (Terminal أو PowerShell) داخل مجلد المشروع ونفّذ:

```bash
npm install
npm run setup
```

الأمر الأول يثبّت Playwright، والثاني يحمّل متصفح Chromium الذي يُصيِّر الإطارات.

---

## 2. المعاينة المباشرة (بدون تصيير)

افتح ملف الحلقة في Chrome، وأضف `?preview` إلى آخر العنوان:

```
file:///.../memoire-ittihadia/ep02-bouabid/index.html?preview
```

يظهر شريط تحكم فيه: زر **Play** مع الصوت متزامن، وشريط زمني تسحبه لأي لحظة.
- **مفتاح المسافة:** تشغيل وإيقاف.
- **السهمان ← →:** ثانية للأمام أو للخلف، ومع Shift عُشر ثانية.

بعد أي تعديل في `index.html`، اضغط F5 فترى النتيجة فوراً.

---

## 3. التصيير

| الأمر | ماذا يفعل |
|---|---|
| `node build.js ep02` | يصيّر الحلقة كاملة، ويركّب الصوت، ويكتب `output/ep02-bouabid.mp4` |
| `node build.js ep02 --range 60:75` | يصيّر من الثانية 60 إلى 75 فقط، وهو أسرع طريقة لتجربة تعديل |
| `node build.js ep02 --audio-only` | يعيد مزج الصوت فقط ويركّبه على آخر صورة مصيَّرة، في ثوانٍ |
| `node build.js ep01` | الحلقة 01 |

التصيير يستعمل كل أنوية المعالج. مدته تقريباً 10–20 دقيقة للحلقة 02 حسب الجهاز، ويظهر الوقت المتبقي أثناء العمل. يمكن تحديد عدد العمليات بـ`--jobs 2`.

---

## 4. أين أعدّل ماذا؟ (الحلقة 02)

| أريد أن أغيّر… | المكان |
|---|---|
| **نص على الشاشة** | `ep02-bouabid/index.html`: ابحث عن النص نفسه (مثلاً «خبير اقتصادي») وغيّره |
| **حجم خط أو موضع عنصر** | في `<style>` داخل `index.html`، كل عنصر له `id` (مثلاً `#s3n2{top:820px}`) |
| **صورة** | ضع الصورة الجديدة في `ep02-bouabid/assets/` بنفس الاسم، أو غيّر المسار في `index.html` |
| **متى يظهر عنصر** | في الجزء `window.render` من `index.html`، مثلاً `drop('u1', t, 100.0, …)`. الرقم هو وقت الظهور على «الخط الزمني الداخلي» |
| **مزامنة الصوت** | الجدول `const WARP = [[الوقت الحقيقي, الوقت الداخلي], …]` في `index.html`. كل سطر يربط لحظة من الصوت بمشهد. لتأخير عنصر نصف ثانية، زد رقمه الأول 0.5 |
| **مستوى الموسيقى** | `build.js`: السطر `MUSIC_BELOW_VOICE = 13`. رقم أكبر يعني موسيقى أخفض |
| **المؤثرات (أختام، ضربات)** | `ep02-bouabid/make_audio.py` |
| **الألوان** | في أول `<style>`: `--red`, `--cream`, `--ink`… |

**أدوات الحركة الجاهزة** (كلها في `index.html`):
- `drop(id, t, وقت, ميلان)`: ورقة تسقط على اللوح.
- `slide(id, t, وقت, ميلان, اتجاه)`: ورقة تنزلق من الجانب.
- `slam(id, t, وقت, ميلان)`: ختم يُضرب.
- `draw(id, نسبة)`: خيط أحمر أو دائرة تُرسم.

---

## 5. الصوت

| الملف | المحتوى |
|---|---|
| `ep02-bouabid/audio/voiceover_edit.flac` | صوتك الأصلي بعد القص فقط، بدون أي معالجة |
| `ep02-bouabid/audio/music_methodus.flac` | الموسيقى «Methodus»، نسخة مقطوعة على مدة الفيديو (راجع `MUSIC.md`) |
| `ep02-bouabid/audio/words.json` | تفريغ التسجيل الأصلي كلمة بكلمة مع التوقيت |
| `ep02-bouabid/audio/preview_mix.m4a` | المزيج النهائي، تستعمله المعاينة، ويتحدّث تلقائياً بعد كل تصيير كامل |

**إعادة قص الصوت من التسجيل الأصلي:** ضع تسجيلك الأصلي في `ep02-bouabid/audio/raw.wav` (WAV)، ثم:

```bash
pip install noisereduce
python ep02-bouabid/vo_edit.py ep02-bouabid/audio/raw.wav ep02-bouabid/audio/words.json ep02-bouabid/audio
```

- المقاطع المحذوفة (المحاولات المكررة) محددة في `vo_edit.py`، في القائمة `REMOVE`.
- النتيجة `audio/vo_edit.wav`، والجدول الجديد للمزامنة `audio/edit_map.json`.

**إذا تغيّرت مدة الفيديو:** اطلب من Epidemic Sound نسخة جديدة من المقطوعة بالمدة الجديدة، وضعها مكان `music_methodus.flac`. يُنبّهك `build.js` إذا كانت المدتان مختلفتين.

---

## 6. هيكل المشروع

```
memoire-ittihadia/
├── build.js              ← أمر التصيير الواحد
├── package.json
├── shared/
│   ├── render.js         ← يصيّر صفحة HTML إطاراً بإطار (Playwright + FFmpeg)
│   ├── preview.js        ← المعاينة المباشرة (?preview)
│   └── fonts/            ← الخطوط (رِم كوفي، القاهرة، أميري، Special Elite)
├── ep01-ben-barka/
│   ├── index.html        ← الحلقة 01
│   └── make_audio.py     ← موسيقى ومؤثرات مولّدة
└── ep02-bouabid/
    ├── index.html        ← الحلقة 02 (المشاهد + جدول المزامنة WARP)
    ├── assets/           ← الصور الحقيقية والشعارات والدرهم
    ├── audio/            ← الصوت والموسيقى
    ├── make_audio.py     ← المؤثرات
    ├── vo_edit.py        ← قص الفويس أوفر
    ├── teleprompter.html ← نص القراءة للتسجيل
    └── VOICEOVER_DARIJA.txt
```

النتائج تُكتب في `output/`، والملفات المؤقتة في `output/tmp/`. يمكن حذف هذا المجلد في أي وقت.
