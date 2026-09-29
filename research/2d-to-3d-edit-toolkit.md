# 2D→3D Edit Toolkit

_29 September 2026 · deep research on GitHub and the web_

Open-source tools, Claude skills and MCP servers that add 2D→3D, motion design, VFX and SFX power to an After Effects or DaVinci Resolve workflow. Every entry was checked against its GitHub page or official docs, and every license was read with monetized channels in mind.

## Start here

This report answers one question: which free tools on GitHub make an After Effects or DaVinci Resolve editor stronger at motion design, VFX, SFX and 2D→3D, and how do you connect them to Claude Code?

If you add only nine things, add these:

| Job | Add this | Why |
|---|---|---|
| Let Claude build 3D scenes | **[Blender MCP](https://github.com/ahujasid/blender-mcp)** + Blender | Free 3D hub. Claude builds parallax rigs, 3D titles, camera moves and image-to-3D props. |
| Let Claude work inside Resolve | **[davinci-resolve-mcp](https://github.com/samuelgursky/davinci-resolve-mcp)** (or Resolve 21.1 Studio's own AI-assistant connection) | Timeline, color and Fusion 3D nodes (Camera3D, ImagePlane3D, Text+) by prompt. |
| Let Claude work inside After Effects | **[mcp-aftereffects](https://github.com/kumoproductions/mcp-aftereffects)** (safe) or **[after-effects-mcp](https://github.com/Dakkshin/after-effects-mcp)** (more power) | 3D layers, cameras, keyframes and expressions by prompt. |
| Depth maps and 3D parallax | **[ComfyUI](https://github.com/comfyanonymous/ComfyUI)** + **[Video Depth Anything](https://github.com/DepthAnything/Video-Depth-Anything)** Small + **[Depthflow nodes](https://github.com/akatz-ai/ComfyUI-Depthflow-Nodes)** | Flicker-free depth passes and the “3D Zoom” look, commercially safe. |
| Motion graphics written as code | **[HyperFrames](https://github.com/heygen-com/hyperframes)** or **[Remotion skills](https://github.com/remotion-dev/skills)** + **[GSAP](https://github.com/greensock/gsap-skills)** + **[motion-design skill](https://github.com/LottieFiles/motion-design-skill)** | Claude is strongest when it writes code; these render it to MP4. |
| A real 3D model from a picture | **[TRELLIS.2](https://github.com/microsoft/TRELLIS.2)** | One image → textured GLB for AE's Advanced 3D or Blender. MIT. |
| AI camera moves | **[WanGP](https://github.com/deepbeepmeep/Wan2GP)** with **[ReCamMaster](https://github.com/KlingAIResearch/ReCamMaster)** | Re-shoot a flat clip as an orbit or push-in on a consumer GPU. |
| Sound effects in sync | **[HunyuanVideo-Foley](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley)** + **[Stable Audio 3](https://github.com/Stability-AI/stable-audio-3)** + **[beat_this](https://github.com/CPJKU/beat_this)** | Whooshes and hits that match the picture, plus beat markers. |
| Roto and keying | **[Sammie-Roto 2](https://github.com/Zarxrax/Sammie-Roto-2)** / **[Samosa](https://github.com/tenetmotion/Samosa)** (AE) + **[CorridorKey](https://github.com/nikopueringer/CorridorKey)** | Click-to-roto players and clean green-screen keys. |

> Monetized YouTube, TikTok or Instagram counts as **commercial use**. Many AI models are non-commercial even when their code is free. The catalog marks every license.

## Pick by goal

| Goal | Free pick | Runs on | License |
|---|---|---|---|
| 3D parallax from a photo or frame | ComfyUI-Depthflow-Nodes + Depth Anything V2 Small | Any OpenGL GPU | Commercial OK |
| Depth pass for lens blur, fog and parallax | Video Depth Anything Small → EXR | NVIDIA, about 7 GB | Commercial OK (Small only) |
| 3D title or logo with a camera move | AE Advanced 3D (26.x) or Fusion Text3D; Blender for more | Your editor | — |
| Real 3D object from a picture | TRELLIS.2 → GLB → AE or Blender | 24 GB (GGUF ≈8 GB), or Mac port | MIT |
| AI orbit or push-in on a clip | ReCamMaster in WanGP | Consumer NVIDIA | MIT |
| Camera move from a still | Wan 2.2 Fun Camera Control (ComfyUI template) | 24 GB | Apache-2.0 |
| Stick 3D text to real footage | AE 3D Camera Tracker, or Blender tracker + exporter | CPU | Free |
| Rebuild a place in 3D and fly through it | Brush → SuperSplat | Any GPU or browser | Apache / MIT |
| Copy a player's move onto a 3D character | SAM 3D Body + fbxify → Blender / Mixamo | NVIDIA | Commercial OK |
| Turn the whole montage into VR 3D | iw3 | 4–8 GB NVIDIA | MIT |
| Rotoscope a player | Sammie-Roto 2, Samosa (AE) or SAM 3 | NVIDIA or CPU | Check models |
| Green-screen key | CorridorKey (EZ GUI or Resolve OFX) | 6–8 GB | Renders OK for paid work |
| Remove an object | MiniMax-Remover or VACE | 6 GB+ | Check / Apache |
| Smooth slow motion | Flowframes (RIFE) | Any GPU | GPL |
| Upscale | SeedVR2 or Video2X | 8 GB+ / any GPU | Apache / AGPL |
| Sound effects that match the picture | HunyuanVideo-Foley | Under 8 GB in fp8 | Commercial OK, not EU/UK/South Korea |
| Your own whoosh and impact bank | Stable Audio 3 Small-SFX | CPU | Free under $1M revenue |
| Beat and downbeat markers | beat_this → AE .jsx or Resolve EDL | CPU | MIT |
| VFX elements with alpha (fire, smoke, energy) | Wan-Alpha, or Blender Mantaflow → EXR | GPU | MIT / GPL |
| Captions | AutoSubs (AE and Resolve) | CPU or GPU | MIT |

## Claude skills and MCP servers

**Skills** are instruction folders (SKILL.md) that teach Claude a job. **MCP servers** are remote controls that let Claude operate an app. You install both inside your project folder, so they travel with it.

### Skills for motion design

Run these in your project folder. `-a claude-code` copies the skills into `.claude/skills/`, which works well on Windows. The `skills` tool needs Node.js 22.20 or newer.

```bash
npx skills add heygen-com/hyperframes -a claude-code
npx skills add remotion-dev/skills -a claude-code
npx skills add https://github.com/greensock/gsap-skills -a claude-code
npx skills add LottieFiles/motion-design-skill -a claude-code
```

- **HyperFrames** (Apache-2.0, needs Node.js 22+ and FFmpeg) and **Remotion** render code to MP4. Remotion needs a company license above 3 employees.
- **ElevenLabs skills** (`npx skills add elevenlabs/skills`) include a sound-effects skill, but the API is paid and its free tier is non-commercial.
- **auto-editor** (`npx skills add WyattBlue/auto-editor`) cuts silence and dead air, once the auto-editor program is installed.
- **anthropics/skills** includes skill-creator, which helps you package your own workflows as skills.

### MCP servers for your apps

```bash
# Blender: the package was renamed to mcp-for-blender (Sep 2026). Needs uv.
claude mcp add blender -e DISABLE_TELEMETRY=true -- uvx mcp-for-blender
uvx mcp-for-blender install-addon
# then in Blender: Preferences › Add-ons › enable "Interface: MCP for Blender", N panel › Start MCP Server

# After Effects 2024–2026 (Node.js 24+). In AE turn on
# Preferences › Scripting & Expressions › "Allow Scripts to Write Files and Access Network"
claude mcp add aftereffects -- npx -y @kumoproductions/mcp-aftereffects

# DaVinci Resolve: the installer configures Claude Code for you
npx davinci-resolve-mcp setup

# ComfyUI (local). Point COMFY_BIN at comfy.exe inside your ComfyUI Python environment
pip install comfy-mcp "comfy-cli>=1.14.0"
claude mcp add comfy-mcp -e COMFY_BIN=C:\path\to\venv\Scripts\comfy.exe -- comfy-mcp

# FFmpeg toolbox (needs FFmpeg and Python 3.11+)
claude mcp add kinocut -- uvx --from kinocut kino
```

| App | Notes |
|---|---|
| Blender | Blender's own developers also publish an official Blender connector for Claude (blender.org/lab/mcp-server, Blender 5.1+). It is a different add-on from mcp-for-blender; don't mix the two. |
| DaVinci Resolve | Resolve Studio gives direct control. Resolve 21.1 moved Python scripting to Studio, so the free-version bridge only works up to 21.0.x. Blackmagic says Resolve 21.1 connects to Claude and Claude Code directly; press reports it as Studio-only, under File › Setup AI Assistants. |
| After Effects | For more power, [after-effects-mcp](https://github.com/Dakkshin/after-effects-mcp) adds a bridge panel and can run any ExtendScript. |
| Premiere Pro | [Adobe Premiere Pro MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP): 283 timeline operations through a CEP panel. |
| ComfyUI | No GPU? Use Comfy Cloud: `claude mcp add --transport http comfy-cloud https://cloud.comfy.org/mcp` (paid credits). |

### What Claude can and cannot do

- **Can:** write AE scripts and expressions, build Fusion and Blender scenes, run depth and 3D models through ComfyUI, batch FFmpeg jobs, place beat markers, and render code-built motion graphics.
- **Cannot:** watch your video. Give it frames, contact sheets or screenshots. It also cannot judge feel and pacing; you still choose which hits land on the beat.
- **Be careful:** Blender, AE and Resolve bridges run code on your PC. Back up projects first and use read-only modes where they exist.

## After Effects

After Effects now has real 3D built in. You may not need Element 3D for many shots.

| Version | 3D feature |
|---|---|
| 24.1 | Advanced 3D renderer, GLB import, HDRI environment lights |
| 24.5 | Animated GLB, shadow catchers, depth data for Fog 3D and Depth Matte |
| 25.2 | FBX import with animation, cameras and lights; video as environment light |
| 26.0 | Parametric meshes (cube, sphere, torus…), Substance materials, 8 shadow lights |
| 26.2 | Substance height displacement, Object Matte (AI roto) |
| 26.3 | Depth of field in Advanced 3D |

### Free 2D→3D recipe in After Effects

1. Make a depth map with Video Depth Anything Small (16-bit PNG or EXR). For a quick preview inside AE, use DepthGen or TheAnimeScripter.
2. Fast 2.5D: in a 16-bpc comp, use Displacement Map plus Camera Lens Blur with the depth layer as the blur map. Tick “Invert Blur Map”, because near objects are white.
3. Real 3D: in Blender, displace a subdivided plane with the depth map, map the photo on it, and export GLB. Import it into AE with the Advanced 3D renderer.
4. Add 3D text, parametric meshes or a TRELLIS.2 logo GLB.
5. Animate a two-node camera, or use 3D Camera Tracker on video plates. Cameras made in Blender come in through the exporter's .jsx.
6. Light it with a Poly Haven HDRI and turn on shadows.
7. Advanced 3D has no motion blur, so precompose and add CC Force Motion Blur.
8. Render with the Render Queue or `aerender`.

**Watch out:** Bodymovin exports gradients in grayscale from AE 26.0. CEP panels keep working until at least late 2028; Adobe moves to UXP after that.

## DaVinci Resolve and Fusion

The free version is powerful, but several key tools need **Studio**:

| Needs Studio | Works in Free |
|---|---|
| Camera Tracker, Magic Mask, Depth Map, Relight, all built-in AI tools | Fusion 3D: Text3D, Shape3D, Extrude3D, ImagePlane3D, Displace3D, Camera3D, Renderer3D |
| DCTL | FBX, OBJ and Alembic import; particles; Depth Blur and Fog |
| Python scripting (from 21.1) and external scripting | Lua scripts from the Scripts menu (sandboxed) |
| The built-in AI assistant connection (21.1) | Krokodove nodes (built into Fusion 21) |

On Resolve Free 21.1, Claude can still help: it writes Fusion `.setting` files (plain text node trees) that you paste into Fusion.

### Free 2D→3D recipe in Fusion

1. Export the shot and make a depth sequence with Video Depth Anything: `python run.py --input_video shot.mov --output_dir depth --encoder vits --save_exr`
2. Load the depth as a second MediaIn. Blur it 2–4 px and erode it slightly to soften edges.
3. MediaIn1 → ImagePlane3D (subdivision 200–500) → Displace3D, with the depth as the displacement input (Luminance, scale about 0.1–0.3).
4. Add a Camera3D and keyframe a short dolly with a slight orbit. Too much motion stretches the image.
5. Add Text3D with extrusion and bevel, and place it between foreground and background.
6. Merge3D → Renderer3D (Z pass on) → Depth Blur or Fog → MediaOut.
7. For stronger parallax, cut out the subject and fill the background on separate planes.
8. To match real camera motion on Free, solve the camera in Blender and import it as FBX or with the Blender → Fusion exporter.

**Watch out:** install Reactor packages with Reactor Standalone on Free 19.1+. Avoid GitHub repos offering “cracked Studio”; they follow a malware pattern.

## 2D→3D recipes

### Parallax shot from one frame or photo

1. Export the frame and upscale it 2× (Real-ESRGAN or SeedVR2).
2. Cut out the subject: `rembg i -m birefnet-general in.png fg.png`, or SAM 3 in ComfyUI.
3. Fill the background behind the subject (dilate the mask 15–30 px first).
4. Make a depth map with Depth Anything V2 Small.
5. Animate: ComfyUI Depthflow nodes (Dolly or Zoom, low intensity, 3–5 s), or layered planes in AE, Fusion or Blender for full control.
6. Render at 60 fps to ProRes or PNG, then add motion blur and grain in the editor.

### AI orbit or push-in from a short clip

1. Pick a single-take shot of at least 81 frames, subject centered, little motion blur.
2. Run ReCamMaster in WanGP. Choose an arc for an orbit, or zoom/pan. Try several seeds.
3. Upscale with SeedVR2, then interpolate from 15/16 fps to 30/60 fps with RIFE.
4. If faces, jersey numbers or logos drift, mask the original back in.

### Player or character → animated 3D character

1. Grab a sharp full-body frame and remove the background.
2. Make the mesh with TRELLIS.2 (or StdGEN for anime characters).
3. In Blender: fix scale, decimate to 20–50k faces, rig with Mixamo or UniRig.
4. Get the motion with SAM 3D Body + fbxify (FBX on a Mixamo skeleton).
5. Apply the motion to the rig, clean foot sliding, render with transparency, and composite in AE or Resolve. AE can also import the animated FBX directly.

### Rebuild a place in 3D and fly a new camera through it

1. Film a static scene while moving the camera (not tripod pans), fast shutter, locked exposure.
2. Extract sharp frames: `ffmpeg -i clip.mp4 -vf fps=3 -q:v 2 frames/%04d.jpg`
3. Solve cameras in COLMAP (or VGGT-1B-Commercial for speed).
4. Train a splat in Brush (any GPU) or LichtFeld Studio (NVIDIA).
5. Clean it and animate the camera in SuperSplat, then render. Or use the KIRI add-on in Blender, or the KIRI plugin in AE.

### Finished montage → VR or 3D

1. Export a clean master without captions.
2. Open iw3's GUI and pick a commercial-safe depth model (Any_V3_Mono or VDA_S).
3. Turn on scene detection and flicker reduction. Output Full SBS for Quest, VR180 for YouTube or anaglyph for red-cyan glasses.

## SFX and VFX recipes

### Synced whooshes, impacts and beat markers

1. Convert the edit to constant frame rate and 48 kHz: `ffmpeg -i edit.mp4 -fps_mode cfr -r 24 -ar 48000 edit_cfr.mp4`
2. Separate the drum stem with `audio-separator song.wav`.
3. Detect beats and downbeats with beat_this; find cut times with PySceneDetect.
4. Generate designed whooshes and hits with Stable Audio 3, and shot-matched Foley with HunyuanVideo-Foley (per shot, not the whole edit).
5. Place each whoosh so its peak lands 2–3 frames before the cut, and each impact on the nearest kick.
6. Write markers: a .jsx for After Effects, an EDL for Resolve (remember Resolve timelines start at 01:00:00:00).

### A VFX shot

1. Isolate the subject: CorridorKey for green screen, Samosa in AE or SAM 3 for everything else. Export EXR with alpha.
2. Clean the plate with VACE or MiniMax-Remover.
3. Relight with IC-Light or Light-A-Video, or add a quick rim light with comfyui-relight.
4. Add an element: a Wan-Alpha clip, or a Blender Mantaflow fire/smoke render.
5. Composite in 32-bit linear in AE, or with Merge in Fusion. Match premultiplied and straight alpha correctly.
6. Run video-to-sound on the final shot and layer your designed hits on top.

## Tool catalog

Every tool the research turned up, with its license, hardware and last update. Use the filters to find what fits your PC and your channel.

### Claude skills

Agent Skills (SKILL.md folders) you install into Claude Code so it knows how to do a job.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [Remotion Agent Skills](https://github.com/remotion-dev/skills) | Official skills that teach Claude to build videos in React with Remotion: best practices (including 3D through three.js), rendering and captions. | Code-built titles, lower thirds, kinetic type and 3D intros from a prompt. | npx skills add remotion-dev/skills | Node.js, no GPU | Check license (Skills license not stated; Remotion needs a company license above 3 employees) | ★ 4.8k · Sep 2026 |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | HeyGen's HTML-to-MP4 renderer with 21 skills for motion graphics, music-to-video and audio-reactive visuals, using GSAP, Lottie and Three.js. | Motion-design templates and kinetic typography written as HTML, rendered frame-exact. | npx skills add heygen-com/hyperframes | Node.js 22+ and FFmpeg; no GPU | Commercial use OK (Apache-2.0) | ★ 54k · Sep 2026 |
| [GSAP skills](https://github.com/greensock/gsap-skills) | Official GreenSock skills for animation timing, easing and timelines. | Smooth, professional easing in HTML- or Remotion-based motion graphics. | npx skills add https://github.com/greensock/gsap-skills | No GPU | Commercial use OK (MIT) | ★ 15.8k |
| [LottieFiles motion-design-skill](https://github.com/LottieFiles/motion-design-skill) | Official skill with motion-design principles: timing, easing, anticipation, follow-through. | Makes any animation Claude builds feel designed, not mechanical. | npx skills add LottieFiles/motion-design-skill | No GPU | Commercial use OK (MIT) | ★ 1.8k |
| [Three.js skills](https://github.com/CloudAI-X/threejs-skills) | Skills for building Three.js 3D scenes: lights, materials, cameras, particles. | 3D logos, particle intros and camera flights written in code. | npx skills add CloudAI-X/threejs-skills | No GPU needed to write; GPU helps rendering | Commercial use OK (MIT) | ★ 3.4k |
| [R3F skills](https://github.com/EnzeD/r3f-skills) | React Three Fiber skills, tested against three r185. | 3D scenes inside Remotion through @remotion/three. | npx skills add EnzeD/r3f-skills | No GPU | Check license (See repo) | ★ 121 |
| [adobe-agent-skills](https://github.com/aedev-tools/adobe-agent-skills) | Skills that write and run After Effects ExtendScript. | Let Claude build AE comps, 3D layers, cameras and expressions. | npx skills add aedev-tools/adobe-agent-skills | After Effects; macOS only | Commercial use OK (Apache-2.0) | ★ 103 |
| [ae-agent-skills](https://github.com/yumehiko/ae-agent-skills) | Agent skills for scripting After Effects. | Small AE automations: layer setup, renaming, keyframes. | npx ae-agent-skills install | After Effects | Check license (See repo) | ★ 33 |
| [blender-game-skills (image-to-3d)](https://github.com/majidmanzarpour/blender-game-skills) | Turns a reference image into a rigged 3D model with headless Blender. | Quick 3D props or characters to animate in a 3D shot. | npx skills add majidmanzarpour/blender-game-skills --skill blender-image-to-3d | Blender | Commercial use OK (MIT) | ★ 114 |
| [blender-skills (camera moves)](https://github.com/kevinbadi/blender-skills) | Turntable, dolly and crane camera moves; renders ProRes 4444 with alpha. | Product-style 3D shots ready to drop onto your timeline. | Skills; needs Blender MCP and a Meshy API key | Blender | Check license (See repo; Meshy is paid) | ★ 131 |
| [cc-blender-skill](https://github.com/RobLe3/cc-blender-skill) | 30 Claude Code skills for Blender 5.1. | General Blender scene building and rendering by prompt. | Copy into .claude/skills | Blender 5.1+ | Check license (See repo) | ★ 77 |
| [claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) | FFmpeg, Remotion and MoviePy skills in one kit. | Batch cuts, conversions, proxies and code-driven edits. | Claude Code skills | No GPU | Check license (See repo) | ★ 2.2k |
| [ElevenLabs skills](https://github.com/elevenlabs/skills) | Official sound-effects, music and voice skills. | Generate whooshes, hits, risers and ambiences from a text prompt. | npx skills add elevenlabs/skills | Paid API key | Paid (ElevenLabs API is paid) |  |
| [Anthropic skills (skill-creator)](https://github.com/anthropics/skills) | Anthropic's official skills repo, including skill-creator for packaging and testing your own skills. | Turn your own TAWLIF workflows into clean, reusable skills. | /plugin marketplace add anthropics/skills | No GPU | Check license (Per skill; mostly Apache-2.0) |  |

### MCP servers

Connectors that let Claude drive an app: Blender, Resolve, After Effects, Premiere, ComfyUI, FFmpeg.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [MCP for Blender (mcp-for-blender)](https://github.com/ahujasid/blender-mcp) | Lets Claude build and edit Blender scenes, run Python, grab Poly Haven HDRIs and models, take viewport screenshots and generate 3D models (Hunyuan3D, Rodin). The package was renamed from blender-mcp to mcp-for-blender in Sep 2026. | Depth-displaced parallax rigs, 3D titles, image-to-3D props and camera moves by prompt. | claude mcp add blender uvx mcp-for-blender · uvx mcp-for-blender install-addon | Blender 3.0+, any OS | Commercial use OK (MIT; telemetry on by default) | ★ 29.6k · Sep 2026 |
| [Blender Lab MCP (official)](https://projects.blender.org/lab/blender_mcp) | The Blender developers' own MCP server behind Claude's official Blender connector (announced by Anthropic, Apr 2026): runs Python, takes screenshots, inspects .blend files and searches the Blender manual and API. | Well-documented Blender automation for Blender 5.1+. | Install from blender.org/lab/mcp-server; Claude Desktop: Connectors › Blender | Blender 5.1+ | Commercial use OK (GPL-3.0-or-later) | Sep 2026 |
| [DaVinci Resolve 21.1 built-in MCP (unverified)](https://www.blackmagicdesign.com/products/davinciresolve) | Resolve 21.1 (Sep 2026) connects to AI assistants such as Claude and Claude Code. Press reports it as Studio-only, set up under File › Setup AI Assistants. | Let Claude edit timelines, grade and build Fusion comps inside Resolve. | Built into Resolve Studio | Resolve Studio ($295) | Paid (Paid (Studio)) | Sep 2026 |
| [davinci-resolve-mcp](https://github.com/samuelgursky/davinci-resolve-mcp) | The most complete community Resolve MCP: timeline, media pool, color (nodes, CDL, LUTs), render queue, and Fusion comps with Camera3D, ImagePlane3D, Renderer3D and Text+. | Build Fusion 3D titles and 2.5D parallax comps by prompt. | npx davinci-resolve-mcp setup | Resolve 18.5+; Studio for direct control; Free only via a bridge up to 21.0.x | Commercial use OK (MIT) | ★ 3.2k · Sep 2026 |
| [after-effects-mcp](https://github.com/Dakkshin/after-effects-mcp) | Creates comps; text, shape, solid, null and camera layers; 3D switches, keyframes, expressions, masks and track mattes; runs any ExtendScript. | AE 3D layers, camera moves and expression rigs by prompt. | Node server + AE bridge panel | After Effects 2022+, Windows/macOS | Commercial use OK (MIT) | ★ 675 · Apr 2026 |
| [mcp-aftereffects](https://github.com/kumoproductions/mcp-aftereffects) | Safer After Effects MCP: undo-grouped edits, read-only mode, code eval off by default, single-frame render previews. | Everyday AE automation with guard rails. | claude mcp add aftereffects -- npx -y @kumoproductions/mcp-aftereffects | AE 2024–2026, Node.js 24+ | Commercial use OK (MIT) | ★ 78 |
| [Adobe Premiere Pro MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP) | 283 Premiere operations: sequences, trims, transitions, effects, keyframes, color, audio ducking, captions and export. | Rough cuts and repetitive timeline work in Premiere. | npm package + CEP panel | Premiere 2020+, Windows/macOS | Commercial use OK (MIT) | ★ 628 · Sep 2026 |
| [Comfy MCP (official)](https://github.com/Comfy-Org/comfy-mcp) | Drives a local ComfyUI or Comfy Cloud: finds models and nodes, builds, validates and runs workflows. | Run depth, image-to-3D (TRELLIS.2) and video models straight from Claude. | pip install comfy-mcp + claude mcp add | Local NVIDIA GPU, or Comfy Cloud (paid) | Commercial use OK (AGPL-3.0 or commercial) | ★ 241 · Aug 2026 |
| [kinocut (FFmpeg MCP)](https://github.com/KyaniteLabs/kinocut) | FFmpeg editing MCP with 201 tools for cutting, captions and quality checks, with guard rails. | Batch exports, conversions, proxies and frame grabs. | claude mcp add kinocut -- uvx --from kinocut kino | FFmpeg on PATH, Python 3.11+ | Commercial use OK (Apache-2.0) | ★ 177 · Sep 2026 |
| [VectCutAPI (CapCut)](https://github.com/sun-guannan/VectCutAPI) | Builds CapCut / JianYing drafts over HTTP or MCP; includes a Claude skill. | Automate CapCut edits and templates. | HTTP / MCP server | Auto export on Windows only | Commercial use OK (Apache-2.0) | ★ 2.3k · Sep 2026 |
| [Cinema 4D MCP](https://github.com/ttiimmaacc/cinema4d-mcp) | Controls Cinema 4D, including MoGraph cloners and effectors. | 3D motion design if you use C4D. | MCP server + C4D plugin | Cinema 4D (paid) | Commercial use OK (MIT) | ★ 128 |
| [fxhoudinimcp](https://github.com/healkeiser/fxhoudinimcp) | 215 Houdini tools, including Pyro, RBD and FLIP setups. | Fire, smoke and destruction simulations by prompt. | claude mcp add --scope user fxhoudini -- <python> -m fxhoudinimcp | Houdini license | Commercial use OK (MIT) | ★ 260 |
| [open-fusion-mcp](https://github.com/legionsound/open-fusion-mcp) | Experimental Fusion MCP with skills: one-call 3D scene builder and a render-and-check loop. | Try only as an experiment (v0.1). | MCP server + skills | macOS, Resolve Studio 21.1 | Check license (See repo) | ★ 0 |

### After Effects

Free scripts, extensions, developer tools and 3D workflows for After Effects.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [Duik Ángela](https://github.com/RxLaboratory/Duik) | The standard free rigging kit for After Effects: IK, bones, controllers, auto-rig and animation tools. | Character and mechanical rigs for motion design. | ScriptUI panel (not affected by the CEP shutdown) | AE 2021+ | Commercial use OK (GPL-3.0) | ★ 405 · Feb 2026 |
| [TheAnimeScripter](https://github.com/NevermindNilas/TheAnimeScripter) | AE panel for depth maps (including DA3 video depth), segmentation, RIFE interpolation, upscaling and dedup. | Depth passes, slow-mo and mattes without leaving After Effects. | AE panel (Adobe edition Windows-only) | NVIDIA recommended | Commercial use OK (AGPL-3.0; pick commercial-safe models) | ★ 329 · Sep 2026 |
| [AutoSubs](https://github.com/tmoroney/auto-subs) | Local Whisper transcription that turns speech into AE text layers or Resolve subtitles. | Animated captions for edits and shorts. | Desktop app + AE/Resolve integration | CPU or GPU | Commercial use OK (MIT) | ★ 4.3k · Sep 2026 |
| [DepthGen](https://github.com/palf-gh/DepthGen) | Native AE effect that makes a depth map with ONNX (CUDA, DirectML, CoreML or CPU). | Quick in-AE depth for lens blur and parallax previews (frame by frame, may flicker). | AE effect plugin | Windows or Mac; any GPU or CPU | Commercial use OK (MIT) | ★ 7 · 2026 |
| [Blender → AE exporter (.jsx)](https://extensions.blender.org/add-ons/io-export-after-effects/) | Exports Blender cameras, lights, empties, image planes and tracking markers to a .jsx you run in AE. | Build or track a camera in Blender, then use it in AE. | Blender extension | Blender 4.2+ | Commercial use OK (GPL) |  |
| [after-effects-to-blender-export](https://github.com/adroitwhiz/after-effects-to-blender-export) | Sends AE cameras and layers (for example from the 3D Camera Tracker) to Blender. | Track in AE, then add real 3D objects in Blender. | AE script + Blender add-on | — | Check license (See repo) | ★ 243 · Jan 2026 |
| [Rebound](https://github.com/meszmate/rebound) | 59 tools: curve editor, physical springs, align and array, Figma/AI/PSD to native layers. | Free easing and layout panel for motion design. | CEP panel | AE 2019+ | Commercial use OK (MIT) | ★ 21 · Aug 2026 |
| [momentum.js](https://github.com/barium3/momentumjs) | p5.js-style code that becomes native AE shapes and text, or GPU bitmaps. | Generative motion graphics written in code. | AE script | AE 2025 recommended | Commercial use OK (MIT) | ★ 171 · Sep 2026 |
| [nexrender](https://github.com/inlife/nexrender) | Data-driven template rendering on top of aerender. | Render dozens of versions of one template (names, scores, colors). | CLI / server | AE installed | Commercial use OK (MIT) | ★ 1.9k · Jun 2026 |
| [Lottie / Bodymovin](https://github.com/airbnb/lottie-web) | Exports AE animations to Lottie JSON for web and apps. AE 26.0 exports gradients in grayscale (open bug). | Animated icons and overlays for web and apps. | CEP extension | — | Commercial use OK (MIT) | ★ 32.1k · Nov 2024 |
| [ISF4AE](https://github.com/baku89/ISF4AE) | Runs GLSL/ISF shaders as AE effects. | Custom glitch, distortion and generative effects. | AE effect plugin | Tested on CC 2023, Apple silicon | Commercial use OK (MIT) | ★ 322 · Aug 2024 |
| [AE Scripting Guide](https://github.com/docsforadobe/after-effects-scripting-guide) | Community scripting reference, updated for AE 26.5, including 3D model layers and parametric meshes. | The reference Claude should follow when writing AE scripts. | Docs site | — | Commercial use OK (Docs) | ★ 180 · Sep 2026 |
| [Types-for-Adobe](https://github.com/docsforadobe/Types-for-Adobe) | TypeScript types for AE scripting (up to 26.0). | Fewer mistakes when Claude writes ExtendScript. | npm types | — | Commercial use OK (MIT) | ★ 644 · May 2026 |
| [Bolt CEP](https://github.com/hyperbrew/bolt-cep) | Modern framework for building AE/Premiere panels with Vite, TypeScript and React/Svelte/Vue. | Build your own TAWLIF panel inside AE. | Developer framework | — | Commercial use OK (MIT) | ★ 511 · Jun 2026 |
| [after-effects-command-ids](https://github.com/hyperbrew/after-effects-command-ids) | Menu command IDs for each AE version, for app.executeCommand(). | Let scripts trigger AE menu commands reliably. | Reference | — | Commercial use OK (MIT) | ★ 90 · Apr 2026 |

### Resolve & Fusion

Free Fuses, macros, DCTLs, scripting tools and 3D workflows for DaVinci Resolve and Fusion.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [Reactor](https://gitlab.com/WeSuckLess/Reactor) | The WeSuckLess package manager: about 500 free Fuses, macros, glows and scripts for Fusion. | Install free motion-graphics tools and effects into Fusion. | Drag the installer .lua into the Fusion Console | In-app window needs Studio since 19.1 | Check license (Per package) | ★ 88 · Sep 2026 |
| [Reactor Standalone](https://github.com/Kartaverse/Reactor-Standalone) | Desktop app that installs Reactor packages from outside Resolve. | Get Reactor packages on Resolve Free 19.1 and later. | Desktop app (Win/Mac/Linux) | Resolve Free or Studio | Commercial use OK (LGPL-2.1) | ★ 106 · Sep 2026 |
| [Krokodove (built into Fusion 21) (unverified)](https://komkomdoorn.com/krokodove) | 100+ vector, generator, modifier and 3D nodes, now shipped inside Fusion 21; 21.1 adds HeightFieldCreate3D, TubeCreate3D and more. | Depth displacement, extrusions and motion-graphics shapes in the free version. | Built into Fusion | Resolve 21+ | Commercial use OK (Free, bundled) | Sep 2026 |
| [Shaderfuse](https://github.com/nmbr73/Shaderfuse) | Shadertoy shaders converted to Fuses (95 shaders, 63 Windows-only). | Animated backgrounds, tunnels and glitch looks (non-monetized). | Reactor package | Windows NVIDIA or Apple silicon | Non-commercial only (Shaders mostly CC BY-NC-SA) | ★ 79 · Sep 2026 |
| [Vonk Ultra](https://github.com/Kartaverse/VonkUltra) | No-code data nodes (text, JSON, arrays, matrices) for data-driven Fusion graphics. | Scoreboards, stat counters and generative layouts from data. | Reactor packages | Resolve Free or Studio | Commercial use OK (GPL-3.0) | ★ 12 · Jul 2026 |
| [Fusion expressions library](https://github.com/mrJohnHolt/davinci-resolve-fusion-expressions) | Copy-paste Lua expressions for time, text, masks and easing, plus VS Code snippets and .drfx packs. | Faster expression-driven animation in Fusion. | Snippets | Resolve Free | Check license (None stated) | ★ 2 |
| [pysion](https://github.com/brunocbreis/pysion) | Writes Fusion .setting text from Python, ready to paste into Fusion; no scripting API needed. | Lets Claude generate Fusion node trees that also work on Resolve Free. | Python library | Any | Commercial use OK (MIT) | ★ 26 · Sep 2023 |
| [utility-dctls](https://github.com/thatcherfreeman/utility-dctls) | 100+ DCTLs (halation, film grain, film curve, halftone, radial blur, lens distortion) plus Fuses that work in Free. | Film looks and texture on the Color page. | DCTL (Studio) · Fuses (Free) | DCTL needs Studio | Commercial use OK (MIT) | ★ 426 · Sep 2026 |
| [Demystify-Color DCTLs](https://github.com/Demystify-Color/DCTLs) | Color models, contrast and creative-look DCTLs. | Stylized grades for edits. | DCTL | Studio | Commercial use OK (MIT) | ★ 163 · May 2026 |
| [ntsc-rs](https://github.com/valadaptive/ntsc-rs) | Accurate VHS / NTSC analog look as an OFX plugin and a standalone app. | Retro VHS edits. | OFX plugin · app | Any | Commercial use OK (MIT / Apache-2.0) | ★ 2.6k · Sep 2026 |
| [Gyroflow plugins](https://github.com/gyroflow/gyroflow-plugins) | Stabilization from camera gyro data, as OFX for Resolve (Free and Studio). | Smooth action-cam and phone footage. | OFX plugin | Any GPU | Commercial use OK (GPL-3.0) | ★ 127 · Aug 2025 |
| [Blender → Fusion camera exporter](https://gist.github.com/p2or/5560c142fcb14716c6ac490a1d9bfb6e) | Writes a Fusion .comp with an animated Camera3D and the tracking point cloud from Blender. | Free substitute for Fusion's Studio-only Camera Tracker. | Blender script | Blender 4.x support unverified | Commercial use OK (GPL-2.0+) | Jan 2024 |
| [CorridorKey-Runtime (OFX)](https://github.com/alexandremendoncaalvaro/CorridorKey-Runtime) | OFX plugin for Corridor Digital's AI green-screen keyer in Resolve 20+, Fusion and Nuke. | Neural keys on the Resolve timeline. | OFX plugin | Windows RTX 30+ or Apple silicon | Check license (CC BY-NC-SA (renders usable commercially)) | ★ 754 · Jun 2026 |
| [RemObj-Fuse](https://github.com/Akascape/RemObj-Fuse) | LaMa object removal inside Fusion, frame by frame. | Clean plates on locked-off shots. | Fusion Fuse | CPU or GPU | Commercial use OK (MIT) | ★ 20 |
| [ComfyUI-SecondUnit](https://github.com/lumosai8/ComfyUI-SecondUnit) | ComfyUI nodes that pull frames, audio and subtitles from Resolve and send results back to the media pool or timeline. | Round-trip AI processing with Resolve Studio. | ComfyUI nodes | Resolve Studio | Commercial use OK (MIT) | ★ 5 |
| [pybmd](https://github.com/WheheoHu/pybmd) | Python wrapper for the Resolve scripting API, tracking 18.6 to 21.1. | Cleaner Resolve Studio scripts written by Claude. | Python library | Resolve Studio for Python on 21.1 | Commercial use OK (LGPL-3.0) | ★ 35 |
| [Resolve scripting docs mirror](https://gist.github.com/X-Raym/2f2bf453fc481b9cca624d7ca0e19de8) | Mirror of the official scripting README with version-to-version diffs (up to 21.0.4). | The reference Claude should follow when scripting Resolve. | Docs | — | Commercial use OK (Docs) | Jul 2026 |
| [awesome-davinci-resolve](https://github.com/Greenysmac/awesome-davinci-resolve) | Curated list of about 244 Resolve resources. | Browse more free tools. | List | — | Commercial use OK (—) | Sep 2026 |

### Depth maps

Models that turn an image or clip into a depth map, the base of most 2D→3D effects.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [Video Depth Anything](https://github.com/DepthAnything/Video-Depth-Anything) | Flicker-free depth for videos of any length; relative and metric models plus a streaming mode. | A clean depth pass per clip (EXR) for lens blur, fog, grading by depth and 2.5D moves. | CLI · HF Space · ComfyUI node | Small ≈7 GB · Large ≈24 GB | Check license (Small: Apache-2.0 · Base/Large: non-commercial) | ★ 2.2k · Oct 2025 |
| [Depth Anything 3](https://github.com/ByteDance-Seed/Depth-Anything-3) | Depth, camera poses and 3D Gaussians from one image or many frames; streaming mode for long videos under 12 GB. | The sharpest commercial-safe depth for stills and frames; point clouds for fake camera moves. | Gradio · CLI · ComfyUI · Blender add-on | Under 12 GB (streaming); less for Small | Check license (Small/Base/Mono-Large/Metric-Large: Apache-2.0 · Large/Giant: non-commercial) | ★ 6.4k · Jul 2026 |
| [Depth Anything V2](https://github.com/DepthAnything/Depth-Anything-V2) | Fast single-image depth, built into almost every tool (ComfyUI, Core ML on Mac, TensorRT). | Quick depth for stills, thumbnails and anime panels. | CLI · ComfyUI · HF Space · Core ML | Runs on modest GPUs and Apple silicon | Check license (Small: Apache-2.0 · Base/Large: non-commercial) | ★ 8.9k · Mar 2026 |
| [Distill-Any-Depth](https://github.com/Westlake-AGI-Lab/Distill-Any-Depth) | Depth Anything-style models where every size, even Large, is MIT. | High-quality depth for monetized work without license worries. | CLI · HF Space · built into iw3 | Consumer NVIDIA GPU | Commercial use OK (MIT) | ★ 693 · Apr 2025 |
| [DepthCrafter](https://github.com/Tencent/DepthCrafter) | Very detailed, stable video depth from a video diffusion model. | Hero shots where edge detail matters, for non-monetized work. | CLI/Gradio · ComfyUI · HF Space | 9–26 GB, about 2 fps on an A100 | Non-commercial only (Non-commercial) | ★ 1.6k · Nov 2025 |
| [MoGe-2 / MoGe-3](https://github.com/microsoft/MoGe) | Metric depth, point map, normals and field of view from one image; exports GLB and PLY. | Turn a still into a 3D point cloud or mesh for Blender. | Gradio · CLI · HF Space | NVIDIA; macOS not supported | Check license (Code and MoGe-2 weights MIT; MoGe-3 weights unverified) | ★ 3.0k · Aug 2026 |
| [Marigold v1.1](https://github.com/prs-eth/Marigold) | Diffusion depth and surface normals, with an official Colab. | Clean, detailed stills depth; normals for relighting. | diffusers · HF Space · Colab | Mid-range NVIDIA or Colab | Commercial use OK (Code Apache-2.0 · weights OpenRAIL++-M (use rules apply)) | ★ 3.2k · Sep 2026 |
| [Marigold V2](https://github.com/huawei-bayerlab/marigold-v2) | New (Sep 2026) LoRA on Qwen-Image-Edit: very sharp hair and fur, depth behind glass. | Stills where hair and fine edges must stay clean. | CLI | 17 GB at 1024² · 29 GB at 2048² | Commercial use OK (Apache-2.0) | ★ 865 · Sep 2026 |
| [Pixel-Perfect Depth](https://github.com/gangweix/pixel-perfect-depth) | Diffusion depth with clean edges and no flying pixels; video model since Jan 2026. | Depth for parallax without halos around the subject. | CLI · HF Space | NVIDIA | Commercial use OK (Apache-2.0) | ★ 1.1k · Jan 2026 |
| [RollingDepth](https://github.com/prs-eth/RollingDepth) | Video depth built on Marigold, with low-VRAM flags. | Consistent video depth when Video Depth Anything struggles. | CLI · HF Space | Low-VRAM mode available | Commercial use OK (Code Apache-2.0 · weights OpenRAIL++-M) | ★ 611 · Mar 2025 |
| [Apple Depth Pro](https://github.com/apple/ml-depth-pro) | Sharp metric depth plus focal length in about 0.3 s. | Fast, sharp depth for stills. | CLI | NVIDIA or Apple silicon | Check license (Unclear: README permissive, model card research-only) | ★ 5.7k · 2024 |
| [ComfyUI Video Depth Anything](https://github.com/yuvraj108c/ComfyUI-Video-Depth-Anything) | Runs Video Depth Anything inside ComfyUI. | Batch depth passes for many clips without coding. | ComfyUI node | About 7 GB+ | Check license (Node Apache-2.0; model license separate) | Jan 2026 |
| [ComfyUI-HQ-Image-Save](https://github.com/spacepxl/ComfyUI-HQ-Image-Save) | Saves 16/32-bit EXR and PNG from ComfyUI; the default save node is 8-bit. | Banding-free depth passes for blur, fog and displacement. | ComfyUI node | No extra GPU | Check license (See repo) |  |
| [DA3-blender](https://github.com/xy-gao/DA3-blender) | Runs Depth Anything 3 inside Blender to make point clouds or meshes from images. | Build a 3D set from a frame directly in Blender. | Blender add-on | 4 GB+; Windows | Check license (See repo) | ★ 159 |

### Parallax & 3D photo

Turn one photo or frame into a moving 3D parallax shot.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [DepthFlow](https://github.com/BrokenSource/DepthFlow) | Ray-marched parallax video from one image: the CapCut “3D Zoom” look, with seamless loops. v1.0 dropped the web UI; v0.9.1 still has it. | Anime panels, car photos and thumbnails into 3D parallax shots. | Python / CLI (v1.0) · web UI (v0.9.1) | Any OpenGL GPU; 8K on an RTX 3060-class card | Commercial use OK (AGPL-3.0, commercial use encouraged) | ★ 1.5k · Aug 2026 |
| [ComfyUI-Depthflow-Nodes](https://github.com/akatz-ai/ComfyUI-Depthflow-Nodes) | DepthFlow in ComfyUI with Zoom, Dolly, Circle, Orbital and other presets, plus depth of field and vignette. | The easiest free match for Depth Scanner or CapCut 3D Zoom. | ComfyUI Manager | Any OpenGL GPU + a depth node | Commercial use OK (AGPL-3.0 (pinned to DepthFlow 0.9.1)) | ★ 365 · Feb 2026 |
| [Parallax Maker](https://github.com/provos/parallax-maker) | Splits a photo into depth cards with SAM, inpaints the gaps and exports glTF for a Blender or Unreal camera. | Pro layered parallax with a real 3D camera. | Web UI | GPU recommended | Commercial use OK (AGPL-3.0) | ★ 105 · Sep 2026 |
| [DepthMap script](https://github.com/thygate/stable-diffusion-webui-depthmap-script) | GUI for depth maps plus the 3D-photo inpainting mesh; outputs circle or dolly-zoom videos and stereo. | 3D photo videos with the gaps filled in. | Standalone Gradio or A1111 extension | GPU, or slow on CPU | Commercial use OK (MIT; switch the default depth model to V2-Small for paid work) | ★ 1.9k · Aug 2024 |
| [Apple SHARP](https://github.com/apple/ml-sharp) | One photo to a 3D Gaussian splat in under a second; renders camera-move videos. | High-quality 3D photo moves for personal projects. | CLI · Pinokio GUI | Prediction on CUDA/MPS/CPU; rendering CUDA | Non-commercial only (Apple research license, non-commercial) | ★ 8.9k · Dec 2025 |
| [3d-ken-burns](https://github.com/sniklaus/3d-ken-burns) | Automatic 3D Ken Burns zoom with inpainting. | Documentary-style photo push-ins (non-monetized). | CLI · local web UI | NVIDIA CUDA | Non-commercial only (CC BY-NC-SA 4.0) | ★ 1.6k · Jun 2026 |

### AI camera moves

AI models that re-shoot a clip or a still with a new camera path: orbit, dolly, crane.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [Wan 2.2 Fun Camera Control](https://github.com/aigc-apps/VideoX-Fun) | Image-to-video with pan, tilt, zoom and combined camera presets (81 frames at 16 fps). | A real camera move from a single frame or poster. | Official ComfyUI template · Gradio | 24 GB for A14B fp8; smaller 5B variant | Commercial use OK (Apache-2.0) | ★ 2.3k · 2026 |
| [ReCamMaster](https://github.com/KlingAIResearch/ReCamMaster) | Re-shoots an existing clip along 10 camera paths: pan, tilt, zoom, translate, arc and orbit. | Turn a flat sports or anime shot into an orbit or push-in. | CLI · WanVideoWrapper · WanGP | Consumer GPU class (Wan2.1-1.3B) | Commercial use OK (MIT (+ Wan Apache-2.0)) | ★ 1.9k · Nov 2025 |
| [WanGP](https://github.com/deepbeepmeep/Wan2GP) | One-click Gradio app that bundles ReCamMaster, Vista4D, VACE, LTX and Hunyuan video models, with low-VRAM modes. | Run AI camera moves without ComfyUI. | Gradio app · Pinokio | Some models from 6 GB | Commercial use OK (Community license: you may sell outputs, not the app) | ★ 9.7k · Sep 2026 |
| [ComfyUI-WanVideoWrapper](https://github.com/kijai/ComfyUI-WanVideoWrapper) | ComfyUI nodes for Wan video models: ReCamMaster, Uni3C, VACE, MiniMax-Remover and more. | The main ComfyUI route to AI camera moves and video edits. | ComfyUI nodes | 12–24 GB+ depending on model | Commercial use OK (Apache-2.0) | ★ 6.7k · May 2026 |
| [Uni3C](https://github.com/ewrfcas/Uni3C) | Copies a reference clip's camera move onto a still (Wan-14B control). | Match the camera move of a shot you like. | CLI · WanVideoWrapper | 24 GB min in ComfyUI, 48 GB recommended | Commercial use OK (Apache-2.0) | ★ 571 · Aug 2025 |
| [LTX-2 camera LoRAs](https://github.com/Lightricks/LTX-2) | Dolly in/out/left/right, jib up/down and static camera LoRAs; a community IC-LoRA copies a reference camera path. | Fast camera-controlled shots for edits. | ComfyUI-LTXVideo | Official 32 GB+; low-VRAM loaders exist | Commercial use OK (LTX Community License: free under $10M/yr revenue) | ★ 9.6k · Aug 2026 |
| [Vista4D](https://github.com/Eyeline-Labs/Vista4D) | 4D point-cloud re-shoot for bigger camera moves; can duplicate or remove subjects. | Big orbit moves on a rented GPU. | CLI · Viser camera UI · WanGP | High (Wan2.1-14B) | Check license (Code Apache-2.0; weights license not stated) | ★ 600 · Apr 2026 |
| [Stable Virtual Camera](https://github.com/Stability-AI/stable-virtual-camera) | 1+ images to 14 preset camera paths (360°, spiral, dolly-zoom), up to about 1000 frames; static scenes only. | Long orbit shots of still scenes (non-monetized). | Gradio | Large NVIDIA; Windows needs WSL | Non-commercial only (Non-commercial, outputs included) | ★ 1.7k · Jun 2025 |
| [GEN3C](https://github.com/nv-tlabs/GEN3C) | 3D-cache camera control from an image or video, with a trajectory editor. | Precise camera paths on a rented GPU. | GUI trajectory editor · CLI | About 43 GB with offload | Commercial use OK (Code Apache-2.0 · NVIDIA Open Model License) | ★ 1.4k · Jun 2026 |
| [TrajectoryCrafter](https://github.com/TrajectoryCrafter/TrajectoryCrafter) | Six-degrees-of-freedom camera redirect for a phone or monocular clip. | Research-grade camera redirects. | Gradio · HF Space | 28 GB+ | Non-commercial only (Depends on DepthCrafter (research-only)) | ★ 880 · Dec 2025 |
| [ComfyUI-qwenmultiangle](https://github.com/jtydhr88/ComfyUI-qwenmultiangle) | Re-angles a still (orbit, elevation, distance) with Qwen-Image-Edit and a multi-angle LoRA, using a 3D viewport node. | Make new-angle keyframes, then animate between them with Wan first/last frame. | ComfyUI node | Claimed 4 GB with offload | Commercial use OK (Apache-2.0 / MIT) | ★ 1.4k |

### Image → 3D models

Make a textured 3D model (GLB) from one image, then use it in Blender or AE's 3D.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [TRELLIS.2](https://github.com/microsoft/TRELLIS.2) | 4B model: one image to a GLB with PBR textures. Best open quality for cars, props, logos and stylized figures. | A real 3D car, trophy or logo for AE's Advanced 3D or Blender. | Gradio · HF Space · ComfyUI-Trellis2 · Pinokio · Mac port | Official 24 GB NVIDIA; GGUF builds claim 6–8 GB | Commercial use OK (MIT (nvdiffrast has separate terms)) | ★ 11.4k · Dec 2025 |
| [ComfyUI-Trellis2](https://github.com/visualbruno/ComfyUI-Trellis2) | TRELLIS.2 and Pixal3D inside ComfyUI, with a Windows install guide. | Image-to-3D without the command line. | ComfyUI node | High VRAM; GGUF fork for less | Check license (See repo; model is MIT) | ★ 848 |
| [trellis-mac](https://github.com/shivampkumar/trellis-mac) | TRELLIS.2 port for Apple silicon (about 5 min per model on an M4 Pro). | Image-to-3D on a Mac. | CLI | Mac with 24 GB+ RAM | Check license (See repo) | ★ 488 |
| [Pixal3D](https://github.com/TencentARC/Pixal3D) | Built on TRELLIS.2; stays closer to the input image and accepts several views. | 3D models that match your reference more faithfully. | Gradio · HF Space · ComfyUI · Pinokio | Low-VRAM mode | Commercial use OK (MIT) | ★ 2.4k · Sep 2026 |
| [Hunyuan3D 2.0 / 2.1](https://github.com/Tencent-Hunyuan/Hunyuan3D-2) | Image to mesh and texture (2.1 adds PBR), with an official Blender add-on. | Textured props and characters with a Blender workflow. | Gradio · Blender add-on · ComfyUI · Pinokio | 2.0: 6 GB shape, 16 GB with texture | Check license (Tencent license: not valid in EU, UK, South Korea) | ★ 15k · mid-2025 |
| [SAM 3D Objects](https://github.com/facebookresearch/sam-3d-objects) | Click an object in a busy real photo to get a 3D splat or mesh with its pose. | Pull a real object out of a photo into 3D. | Notebooks · Meta web demo · ComfyUI wrapper | 32 GB official; 24 GB in ComfyUI | Commercial use OK (SAM License (commercial OK, some uses banned)) | ★ 7.5k · 2026 |
| [TripoSR](https://github.com/VAST-AI-Research/TripoSR) | Rough textured mesh in under half a second. | Fast placeholder 3D objects. | Gradio · HF Space | About 6 GB | Commercial use OK (MIT) | ★ 7.0k · 2024 |
| [Stable Fast 3D / SPAR3D](https://github.com/Stability-AI/stable-fast-3d) | Fast GLB with UV textures. | Quick props with clean UVs. | Gradio · ComfyUI | 6 / 10.5 GB | Check license (Stability Community License: free under $1M revenue) | ★ 1.8k · 2025 |
| [StdGEN](https://github.com/hyz317/StdGEN) | Anime character image to a layered 3D character (body, clothes, hair) that is easy to rig. | 3D versions of anime characters for AMV-style 3D shots. | HF Space · web UI | NVIDIA | Commercial use OK (Apache-2.0) | ★ 394 · Mar 2025 |
| [UniRig / SkinTokens](https://github.com/VAST-AI-Research/UniRig) | Auto-rigs any generated mesh and exports FBX or GLB. | Make a generated character ready for motion capture. | CLI (SkinTokens also Gradio) | 8–14 GB | Commercial use OK (MIT) | ★ 1.8k |

### 3D scenes & splats

Rebuild a real place in 3D from video (Gaussian splats) and fly a new camera through it.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [Brush](https://github.com/ArthurBrussee/brush) | Trains and views Gaussian splats from COLMAP or nerfstudio folders; one app for Windows, Mac, Linux and the browser. | Rebuild a location in 3D on any GPU, including AMD and Mac. | Single-file GUI app | Any WebGPU GPU | Commercial use OK (Apache-2.0) | ★ 5.1k · Sep 2025 |
| [LichtFeld Studio](https://github.com/MrNeRF/LichtFeld-Studio) | Fast splat trainer and editor; exports PLY, SOG, SPZ and HTML. | Quick, high-quality splats on NVIDIA cards. | GUI (Windows/Linux) | NVIDIA GTX 16 / RTX 20 or newer | Commercial use OK (GPL-3.0) | ★ 3.8k · Jun 2026 |
| [SuperSplat](https://github.com/playcanvas/supersplat) | Browser editor to crop and clean splats and keyframe a camera on a timeline, then render MP4 (portrait too). | Fly-through shots of a rebuilt scene, even on a phone or laptop. | Browser app | Any device | Commercial use OK (MIT) | ★ 10.3k · Sep 2026 |
| [KIRI 3DGS Render (Blender)](https://github.com/Kiri-Innovation/3dgs-render-blender-addon) | Blender add-on to import, edit, relight and animate splats alongside normal meshes. | Mix splat scenes with 3D text and objects in Blender. | Blender add-on | Blender 5.1–5.2 | Commercial use OK (GPL-2.0) | ★ 1.2k · Aug 2026 |
| [KIRI Gaussian Splatting for After Effects](https://github.com/Kiri-Innovation/Gaussian-Splatting-plugin-by-KIRI-Engine) | Renders PLY splats through AE cameras, with recolor, dissolve and displace effects. | Splat scenes directly inside After Effects. | AE plugin | AE 2025+, Windows/macOS | Commercial use OK (MIT) | ★ 28 · Jul 2026 |
| [OpenSplat](https://github.com/pierotofy/OpenSplat) | Splat trainer that runs on CPU, CUDA, ROCm or Metal. | Splats on AMD or Mac from the command line. | CLI | CPU, NVIDIA, AMD or Apple | Commercial use OK (AGPL-3.0) | ★ 2.2k |
| [nerfstudio](https://github.com/nerfstudio-project/nerfstudio) | Framework that turns a video into a camera solve and a splat (splatfacto). | One command from phone video to splat. | CLI + web viewer | NVIDIA | Commercial use OK (Apache-2.0) | ★ 12k · Nov 2024 |
| [VGGT (Commercial checkpoint)](https://github.com/facebookresearch/vggt) | Cameras and points from many frames in seconds; exports COLMAP. Use the VGGT-1B-Commercial weights for paid work. | Fast camera solves for splats and 3D compositing. | CLI · Gradio · Blender add-on (vggt-blender) | NVIDIA | Check license (Original weights non-commercial; Commercial checkpoint OK) | ★ 14.4k · May 2026 |
| [Matrix-3D](https://github.com/SkyworkAI/Matrix-3D) | One image to a panorama video, then to an explorable 3D splat world. | Build a 3D world from a single poster or frame. | Gradio | 12 GB low-VRAM mode | Commercial use OK (MIT) | ★ 833 · Sep 2025 |
| [FlashWorld](https://github.com/imlixinyang/FlashWorld) | One image to a 3D splat scene in seconds. | Fast 3D sets from a still. | HF Space · CLI | 24 GB with offload | Commercial use OK (Apache-2.0) | ★ 858 · Feb 2026 |
| [HY-World 2.0](https://github.com/Tencent-Hunyuan/HY-World-2.0) | Text, image or video to a 3D world (mesh or splats). | Large explorable 3D environments. | CLI | High VRAM | Check license (Tencent license: not valid in EU, UK, South Korea) | ★ 2.7k · May 2026 |

### Camera tracking

Solve the camera of real footage so 3D text and objects stick to it.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [COLMAP 4.2](https://github.com/colmap/colmap) | The standard structure-from-motion solver, with GUI; now includes the GLOMAP global mapper, learned matching and masks. | Solve the camera of real footage for splats or 3D compositing. | GUI + CLI; Windows binaries | CPU or GPU; AMD via ROCm | Commercial use OK (BSD) | ★ 12.8k · Sep 2026 |
| [Photogrammetry Importer (Blender)](https://github.com/SBCV/Blender-Addon-Photogrammetry-Importer) | Imports COLMAP, Meshroom or Metashape results into Blender as an animated camera, points and background plates. | Put 3D text and objects into real footage in Blender. | Blender add-on | Blender 5.0.2+ | Commercial use OK (MIT) | ★ 1.4k |
| [ViPE](https://github.com/nv-tlabs/vipe) | Lens data, camera poses and metric depth from any video, including wide-angle, 360° and shots with moving people. | Camera solves for sports footage with moving players. | CLI | NVIDIA | Check license (Apache-2.0 (UniK3D part non-commercial)) | ★ 2.1k · Jun 2026 |

### Motion capture

Copy a person's movement from a normal video onto a 3D character.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [SAM 3D Body](https://github.com/facebookresearch/sam-3d-body) | Full-body 3D pose including hands and feet from video frames, on Meta's MHR rig (ships FBX). | Copy a player's celebration or a dancer's move onto a 3D character, commercially. | CLI · ComfyUI-SAM3DBody · fbxify wrapper | NVIDIA | Commercial use OK (SAM License (commercial OK)) | ★ 3.6k · Nov 2025 |
| [sam-3d-body-fbxify](https://github.com/segfaultExpress/sam-3d-body-fbxify) | Video in, smoothed FBX out, retargeted to Mixamo or Unity rigs, with a Gradio UI. | The easiest commercial-safe video-to-FBX route. | Gradio | NVIDIA | Check license (See repo; model under SAM License) | ★ 28 |
| [GVHMR](https://github.com/zju3dv/GVHMR) | World-space human motion from video, even with a moving camera; Colab and HF Space. | The most proven video mocap, for non-monetized work. | CLI · Colab · HF Space · ComfyUI-Video2MotionCapture | NVIDIA | Non-commercial only (Research / non-profit only, plus SMPL-X) | ★ 2.0k · Mar 2025 |
| [FreeMoCap](https://github.com/freemocap/freemocap) | GUI markerless motion capture, best with 2+ webcams; Blender export; runs on CPU. | Record your own moves as 3D animation. | GUI app | CPU OK; works on Mac | Commercial use OK (AGPL-3.0) | ★ 10.4k · Sep 2026 |

### Stereo 3D & VR

Convert a finished edit to side-by-side 3D, VR180 or Vision Pro spatial video.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [iw3 (nunif)](https://github.com/nagadomi/nunif) | Converts images and videos to SBS, top-bottom, VR180 or anaglyph 3D, with flicker reduction and scene detection. | Turn a finished montage into 3D for Quest, YouTube VR180 or red-cyan glasses. | Windows GUI · CLI · one-click package | 4–8 GB NVIDIA; --low-vram | Commercial use OK (MIT; pick a commercial-safe depth model) | ★ 3.5k · Sep 2026 |
| [StereoCrafter / StereoCrafter2](https://github.com/TencentARC/StereoCrafter) | Depth warp plus diffusion inpainting for the cleanest stereo edges; v2 uses Wan2.1-VACE-14B. | Highest-quality stereo for personal projects. | CLI (GUI fork: enoky/StereoCrafter) | 16 GB+, or 4 GB with offload and 48 GB RAM | Non-commercial only (Non-commercial) | ★ 526 · May 2026 |
| [VisionDepth3D](https://github.com/VisionDepth/VisionDepth3D) | Polished Windows app: many depth models, SBS/VR180/anaglyph, RIFE and upscaling; AMD and Intel through DirectML. No longer open source. | All-in-one converter if you accept a paid license. | Windows GUI | NVIDIA, AMD or Intel | Paid (Proprietary; free tier 3 min/1080p/watermark; Pro $59.99) | ★ 335 · Sep 2026 |
| [Depth Surge 3D](https://github.com/Tok/depth-surge-3d) | Web-UI converter using DA3 or Video Depth Anything; SBS or over-under up to 8K with upscaling. | Simple alternative to iw3. | Web UI | RTX 4070-class: 2–4 s per frame | Commercial use OK (MIT) | ★ 50 · 2026 |
| [Spatial Metadata](https://github.com/Kartaverse/Spatial-Metadata) | GUI for the free spatial CLI: turns SBS video into Apple Vision Pro spatial video (MV-HEVC). | Publish your 3D montage for Vision Pro. | macOS GUI | Apple silicon Mac | Commercial use OK (LGPL) | Oct 2025 |
| [StereoPilot](https://github.com/KlingTeam/StereoPilot) | Research model that makes stereo video without a depth map (Wan2.1-1.3B). | Experiments on a rented GPU. | CLI | About 23 GB | Commercial use OK (MIT) | ★ 117 · Dec 2025 |

### Roto & cleanup

Masks, mattes, green-screen keys and object removal.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [Sammie-Roto 2](https://github.com/Zarxrax/Sammie-Roto-2) | Desktop roto app: SAM2 masks, MatAnyone mattes and MiniMax-Remover object removal. | Click-to-roto players and objects, then export mattes to AE or Resolve. | GUI (Win/Linux/macOS) · Pinokio | NVIDIA; AMD preliminary; CPU | Check license (GPL-3.0; MatAnyone models non-commercial) | ★ 390 · Sep 2026 |
| [SAM 3 / 3.1](https://github.com/facebookresearch/sam3) | Track objects by text prompt (“player in red jersey”); native in ComfyUI. | Fast masks for isolating subjects across a whole clip. | ComfyUI · notebooks | CUDA 12.6+; gated weights | Commercial use OK (SAM License (commercial OK)) | ★ 11.8k · Mar 2026 |
| [SAM 2](https://github.com/facebookresearch/sam2) | Click-to-track video masks. | Rotoscoping for parallax layers and effects. | Notebooks · web demo · ComfyUI | CUDA; WSL on Windows | Commercial use OK (Apache-2.0) | ★ 19.9k · Dec 2024 |
| [CorridorKey](https://github.com/nikopueringer/CorridorKey) | Neural green-screen keyer by Corridor Digital, with a community GUI and a Resolve OFX plugin. | Clean keys on hair and motion blur. | CLI · community GUI · Resolve OFX | 6–8 GB; M1+ Mac | Check license (CC BY-NC-SA, but outputs may be used commercially) | ★ 14.7k · 2026 |
| [BiRefNet](https://github.com/ZhengPeng7/BiRefNet) | High-resolution cutouts of stills and frames, including a matting model. | Clean subject cutouts for posters and parallax. | HF · ComfyUI | About 3.5 GB | Commercial use OK (MIT) | ★ 4.2k · Sep 2025 |
| [rembg](https://github.com/danielgatis/rembg) | Batch background removal; use -m birefnet-general for paid work. | Cut out hundreds of frames or photos at once. | CLI · Gradio | CPU, CUDA or ROCm | Check license (MIT; default bria model needs a paid license) | ★ 24.9k · Sep 2026 |
| [MatAnyone 2](https://github.com/pq-yang/MatAnyone2) | Hair-level human matte from a first-frame mask. | Soft mattes for glow and depth effects (non-monetized). | Gradio · HF Space · CLI | NVIDIA | Non-commercial only (Non-commercial (S-Lab)) | ★ 887 · Mar 2026 |
| [MiniMax-Remover](https://github.com/zibojia/MiniMax-Remover) | Fast Wan-based video object remover (6 steps). | Remove logos, people or wires from a clip. | Gradio · ComfyUI | 6 GB+ in ComfyUI | Check license (Not stated) | ★ 608 · 2025 |
| [VACE](https://github.com/ali-vilab/VACE) | Wan-based masked inpaint, outpaint and extend for video. | Clean plates, extended frames and replaced objects. | ComfyUI | 1.3B or 14B models | Commercial use OK (Apache-2.0) | ★ 4.0k · May 2025 |
| [ProPainter](https://github.com/sczhou/ProPainter) | Video object removal and outpainting. | Object removal for personal projects. | CLI · Gradio | 8 GB (low res) to 25 GB (720p) | Non-commercial only (Non-commercial (S-Lab)) | ★ 7.0k · 2023 |

### Slow-mo & upscale

Frame interpolation for smooth slow motion, and AI upscaling.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [Flowframes](https://github.com/n00mkrad/flowframes) | Drag-and-drop RIFE interpolation for 60 fps and slow motion. | Smooth slow-mo for edits, one click. | Windows GUI | Any GPU (Vulkan) | Commercial use OK (GPL-3.0) | ★ 2.1k · May 2026 |
| [Practical-RIFE](https://github.com/hzwer/Practical-RIFE) | The RIFE models inside most interpolation apps. | Scriptable frame interpolation. | CLI · Colab | CUDA | Commercial use OK (MIT) | ★ 1.0k · Oct 2024 |
| [ComfyUI-Frame-Interpolation](https://github.com/Fannovel16/ComfyUI-Frame-Interpolation) | RIFE, FILM and AMT interpolation nodes for ComfyUI. | Smooth AI-generated clips from 16 fps to 60 fps. | ComfyUI nodes | NVIDIA | Commercial use OK (MIT) | ★ 1.1k |
| [SeedVR2 (ComfyUI)](https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler) | One-step diffusion video upscale and restore that stays stable over time. | Upscale old or AI clips cleanly to 4K. | ComfyUI · CLI | 8 GB (GGUF) to 24 GB; Mac and AMD | Commercial use OK (Apache-2.0) | ★ 2.9k · Dec 2025 |
| [Video2X](https://github.com/k4yt3x/video2x) | Real-ESRGAN, Real-CUGAN and Anime4K upscaling plus RIFE, in a desktop app. | Anime and low-res footage upscaling. | Windows GUI · Linux AppImage | Any GPU (Vulkan) | Commercial use OK (AGPL-3.0) | ★ 21.9k · Jan 2025 |
| [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) | Classic GAN upscaler with an anime model; portable executables. | Upscale frames before depth or parallax. | Portable executables | Any GPU | Commercial use OK (BSD-3) | ★ 36.9k · 2022 |

### VFX & simulation

Relighting, element generation, particles, fire and smoke.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [Samosa (AE roto panel)](https://github.com/tenetmotion/Samosa) | After Effects panel: SAM 2.1/3.1 tracking, MatAnyone2 and VideoMaMa mattes, MiniMax object removal; auto-imports EXR. | AI roto and cleanup without leaving AE. | AE panel (AE 2021+) | Windows NVIDIA/CPU, Mac MPS | Check license (GPL-3.0; some models non-commercial) | ★ 5 · 2026 |
| [EZ-CorridorKey](https://github.com/edenaion/EZ-CorridorKey) | GUI for CorridorKey with a job queue and EXR/ProRes export; makes the alpha hints automatically. | Green-screen keys on hair and motion blur, one click. | GUI app | 8 GB (12 GB recommended) | Check license (CorridorKey terms: keying for paid work OK; some hint models NC) | ★ 4.2k · Aug 2026 |
| [corridorkey_ofx](https://github.com/gitcapoom/corridorkey_ofx) | CorridorKey as an OFX plugin inside Resolve 20 (free and Studio). | Neural keying directly on the Resolve timeline. | Resolve OFX plugin | Windows + NVIDIA only | Check license (CorridorKey terms) | ★ 22 · Aug 2026 |
| [Rembg-Fuse](https://github.com/Akascape/Rembg-Fuse) | Background removal inside Fusion (BiRefNet, SAM, BEN2). | Cut out subjects in Resolve's free version. | Fusion Fuse (Resolve 18+ free) | CPU or CUDA | Commercial use OK (MIT) | ★ 218 |
| [AE-ComfyUI Panels](https://github.com/ckonteos80/Adobe-After-Effects-ComfyUI-Panels) | Sends an AE layer through a ComfyUI workflow and back (stills only). | Run depth, relight or style workflows on a frame from inside AE. | AE ScriptUI panel | Needs a ComfyUI install | Commercial use OK (MIT) | ★ 10 |
| [IC-Light](https://github.com/lllyasviel/IC-Light) | Relights single frames or thumbnails from a prompt or a light direction. | Dramatic thumbnail and poster lighting; swap its background remover for BiRefNet. | Gradio · ComfyUI node | About 8 GB | Check license (Apache-2.0; bundled RMBG-1.4 is non-commercial) | ★ 8.5k · 2025 |
| [Light-A-Video](https://github.com/bcmi/Light-A-Video) | Relights video clips without training (IC-Light + Wan2.1). | Match a subject's light to a new background. | CLI · ComfyUI port | NVIDIA | Commercial use OK (Apache-2.0) | ★ 525 · 2025 |
| [comfyui-relight](https://github.com/EnragedAntelope/comfyui-relight) | Model-free key and rim lights that work on video batches. | Quick rim light on a cut-out subject. | ComfyUI node | Any | Commercial use OK (MIT) | ★ 107 |
| [Wan-Alpha](https://github.com/WeChatCV/Wan-Alpha) | Text to video with a real alpha channel: fire, smoke, glow and energy elements. | Generate VFX elements that drop straight into AE or Fusion. | CLI | 14B-class GPU | Commercial use OK (MIT) | ★ 419 · Dec 2025 |
| [Blender FLIP Fluids](https://github.com/rlguy/Blender-FLIP-Fluids) | High-quality liquid simulation for Blender. | Splashes and liquid logo reveals. | Blender add-on | CPU | Paid (Source GPL/MIT; packaged add-on is paid) | ★ 2.0k |
| [Molecular Plus](https://github.com/u3dreal/molecular-plus) | Particle collisions and debris for Blender. | Debris, sand and particle impacts. | Blender add-on | CPU | Commercial use OK (GPL-3.0) | ★ 413 |
| [Segment-Anything-for-Nuke](https://github.com/rafaelperez/Segment-Anything-for-Nuke) | SAM inside Nuke, plus the same author's ViTMatte, Depth Anything and RIFE nodes. | AI roto and depth in Nuke. | Nuke gizmo | 4–8 GB | Commercial use OK (MIT) |  |

### SFX & beat sync

AI sound effects synced to picture, beat detection and stem separation.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [HunyuanVideo-Foley](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley) | Video (plus optional text) to 48 kHz Foley. The strongest open video-to-sound model. | Hits, whooshes and ambience that match each shot. | CLI · Gradio · ComfyUI (phazei node) | Under 8 GB in fp8; 12–20 GB full | Check license (Tencent license: commercial OK, not valid in EU, UK, South Korea) | ★ 1.1k · Sep 2025 |
| [Stable Audio 3](https://github.com/Stability-AI/stable-audio-3) | Small-SFX model: text to sound effects up to 120 s, 44.1 kHz stereo; runs on CPU. Built into ComfyUI. | Your own bank of whooshes, risers and sub-impacts. | Gradio · CLI · ComfyUI | Small on CPU (~2.4 GB); Medium 5–6.5 GB GPU | Commercial use OK (Stability Community License: free under $1M/yr revenue) | ★ 776 · May 2026 |
| [MOSS-SoundEffect v2.0](https://github.com/OpenMOSS/MOSS-TTS) | Text to sound effects at 48 kHz, up to 30 s. | Apache-licensed alternative for designed SFX. | Python · Gradio · community ComfyUI | GPU | Commercial use OK (Apache-2.0 (weights reported Apache)) | ★ 4.1k · May 2026 |
| [MMAudio](https://github.com/hkchengrex/MMAudio) | Fast video/text to 44.1 kHz audio, 8 s clips; the standard baseline. | Quick synced sound for personal projects. | CLI · Gradio · kijai ComfyUI node · Pinokio | About 6 GB | Non-commercial only (Code MIT; weights non-commercial) | ★ 2.3k · Mar 2025 |
| [audio.cpp](https://github.com/0xShug0/audio.cpp) | Runs ControlFoley, Stable Audio 3, HTDemucs and BS-RoFormer without Python. | Fast local audio AI on CUDA, Metal, Vulkan, ROCm or CPU. | CLI | Any GPU or CPU | Check license (Apache-2.0 (model licenses vary)) | ★ 3.2k · Sep 2026 |
| [beat_this](https://github.com/CPJKU/beat_this) | The most accurate open beat and downbeat tracker. | Beat and downbeat markers for cutting a montage to music. | CLI · Python · Colab | CPU is fine | Commercial use OK (MIT (code and weights)) | ★ 402 · Apr 2026 |
| [python-audio-separator](https://github.com/nomadkaraoke/python-audio-separator) | Ultimate Vocal Remover models (RoFormer, MDX, Demucs) from the command line; gives a drum stem. | Cut on the kick and snare only. | CLI | CUDA, MPS, DirectML or CPU | Commercial use OK (MIT) | ★ 1.4k · Aug 2026 |
| [Ultimate Vocal Remover GUI](https://github.com/Anjok07/ultimatevocalremovergui) | Desktop app for separating vocals, drums and other stems. | Stems without the command line. | GUI app | 6 GB+ GPU or CPU | Commercial use OK (MIT) | ★ 26.4k · Sep 2023 |
| [all-in-one (allin1)](https://github.com/mir-aidj/all-in-one) | BPM, beats, downbeats and song sections (intro, chorus, drop) as JSON. | Find the drop and plan the edit's big moments. | CLI | GPU helps | Commercial use OK (MIT) | ★ 853 · Oct 2023 |
| [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | Finds the cut times in a rendered edit. | Place a whoosh at every cut automatically. | CLI · Python | CPU | Commercial use OK (BSD-3) | ★ 5.2k · Jul 2026 |
| [OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) | Writes markers and cuts as .otio or FCP XML for Resolve, Premiere and others. | Send beat markers into any editor. | Python library | CPU | Commercial use OK (Apache-2.0) | ★ 2.0k |
| [MusiCue](https://github.com/cedarconnor/MusiCue) | Drum hits and song sections to AE .jsx, Resolve/Premiere marker CSV, FCPXML and EDL. | Beat markers in AE, Resolve and Premiere in one step. | CLI | CPU | Commercial use OK (MIT) | ★ 4 · 2026 |
| [freesound-mcp-server](https://github.com/johnkimdw/freesound-mcp-server) | Lets Claude search Freesound and returns each sound's license. | Find license-checked real sound effects by prompt. | MCP server | Free Freesound API key | Commercial use OK (MIT) | ★ 8 |

### Open-source apps

Free editors and motion-graphics apps you can script.

| Tool | What it does | Use it for | Interface | Hardware | License | Stars · updated |
|---|---|---|---|---|---|---|
| [Blender](https://github.com/blender/blender) | Free 3D suite with a video editor, compositor, camera tracker, simulations and full Python. | The 2D→3D hub: depth displacement, tracking, 3D text, particles, rendering. | Desktop app | Any modern GPU | Commercial use OK (GPL (your renders are yours)) | Jul 2026 (5.2 LTS) |
| [FFmpeg](https://github.com/FFmpeg/FFmpeg) | The command-line engine behind almost every video tool. | Frame grabs, proxies, ProRes 4444, EXR sequences, loudness. | CLI | CPU (GPU encoding optional) | Commercial use OK (LGPL/GPL) |  |
| [Remotion](https://github.com/remotion-dev/remotion) | Make videos with React code; 3D through @remotion/three. | Template-driven motion graphics that Claude writes well. | Node.js framework | CPU render | Check license (Free for individuals and up to 3 employees; paid above) | ★ 61k · Sep 2026 |
| [Friction](https://github.com/friction2d/friction) | Open-source vector motion-graphics app with JavaScript expressions. | Free After Effects-style 2D motion design. | Desktop app | Any | Commercial use OK (GPL-3.0) | Dec 2025 (1.0 RC) |
| [Natron](https://github.com/NatronGitHub/Natron) | Open-source node compositor (Nuke-style) with Python; last stable release 2022. | Free EXR compositing, if you accept an old app. | Desktop app | Any | Commercial use OK (GPL-2.0) | ★ 5.6k · 2022 (stalled) |
| [auto-editor](https://github.com/WyattBlue/auto-editor) | Cuts silence or motionless parts and exports timelines for Premiere, Resolve and FCP; has an agent skill. | Fast first assembly of long footage. | CLI · npx skills add WyattBlue/auto-editor | CPU | Commercial use OK (Unlicense) | ★ 5.4k · Sep 2026 |
| [ComfyUI](https://github.com/comfyanonymous/ComfyUI) | Node-based app that runs almost every AI model in this report: depth, 3D, video, sound. | One place to run depth passes, AI camera moves, Foley and upscaling. | Desktop app / web UI | NVIDIA best; AMD and Mac partial | Commercial use OK (GPL-3.0) |  |


## Your hardware

| Your PC | What runs well |
|---|---|
| No NVIDIA GPU, Mac or laptop | Blender, SuperSplat, Brush, Flowframes, Video2X, Depth Anything V2 (Core ML), Stable Audio 3 Small, beat_this, AutoSubs, all skills and MCP servers. Use Hugging Face Spaces or Colab for the rest. |
| NVIDIA 8 GB | Video Depth Anything Small, DepthFlow, iw3, RIFE, SeedVR2 (GGUF), HunyuanVideo-Foley (fp8), MMAudio, CorridorKey, WanGP small models |
| NVIDIA 12–16 GB | DepthCrafter at low res, Hunyuan3D 2.0 with texture, SAM 3, most ComfyUI video workflows |
| NVIDIA 24 GB | TRELLIS.2, Wan 2.2 camera control (fp8), Uni3C in ComfyUI, VDA Large (personal work only) |
| Rent a 48–80 GB GPU | Vista4D, EX-4D, GEN3C, Lyra, Stable Virtual Camera at full size |

## Licenses

- **Non-commercial (not for monetized videos):** DepthCrafter, StereoCrafter, Depth Anything V2 Base/Large, Video Depth Anything Base/Large, DA3 Large/Giant, Stable Virtual Camera (outputs too), Apple SHARP, ProPainter, MatAnyone, GIMM-VFI, MMAudio weights, GVHMR, Shadertoy Fuses.
- **Territory limits:** Tencent Hunyuan models (Hunyuan3D, HunyuanVideo-Foley, HY-World) are not licensed in the EU, UK or South Korea.
- **Revenue caps:** Stability AI models are free under $1M a year; LTX-2 under $10M. Remotion needs a company license from 4 people.
- **Safe for paid work:** Depth Anything V2/Video Depth Anything **Small**, DA3 Small/Base/Mono-Large, Distill-Any-Depth, TRELLIS.2, iw3, DepthFlow, Brush, SuperSplat, COLMAP, SAM 2/3, SAM 3D Body, beat_this, Blender, FFmpeg.
- **Rule of thumb:** the model's license applies even when the app around it is MIT or GPL. Check the model card, not just the repo.

## How this was researched

Seven research tracks ran in parallel on 29 September 2026: depth and stereo; parallax and AI camera moves; real 3D from 2D; Claude skills and MCP servers; the After Effects ecosystem; the Resolve and Fusion ecosystem; and VFX plus sound effects. Each tool was checked on its GitHub page or official docs. Some sites (Hugging Face, Adobe, Blackmagic, blender.org) were blocked from the research sandbox; facts that come only from press or search results are marked “Not verified at source” in the catalog.

Stay safe: install only from official repos. Fake paid copies of DepthFlow, lookalike “SAM 3D” sites and “cracked Resolve Studio” repos exist.

---

Research date: 29 September 2026. Star counts and dates are approximate and change quickly. Entries marked “Not verified at source” come from press or search results only.License labels are a guide, not legal advice. A monetized YouTube, TikTok or Instagram channel counts as commercial use. The license of the model you run applies even when the app around it is MIT or GPL.
