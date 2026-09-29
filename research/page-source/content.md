## Start here {#start data-nav="Start here"}

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

## Pick by goal {#goals data-nav="By goal"}

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

## Claude skills and MCP servers {#skills data-nav="Skills & MCP"}

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

## After Effects {#ae data-nav="After Effects"}

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

## DaVinci Resolve and Fusion {#resolve data-nav="Resolve & Fusion"}

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

## 2D→3D recipes {#recipes data-nav="2D→3D recipes"}

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

## SFX and VFX recipes {#sfx data-nav="SFX & VFX"}

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

## Tool catalog {#catalog data-nav="Catalog"}

Every tool the research turned up, with its license, hardware and last update. Use the filters to find what fits your PC and your channel.

@@CATALOG@@

## Your hardware {#hardware data-nav="Hardware"}

| Your PC | What runs well |
|---|---|
| No NVIDIA GPU, Mac or laptop | Blender, SuperSplat, Brush, Flowframes, Video2X, Depth Anything V2 (Core ML), Stable Audio 3 Small, beat_this, AutoSubs, all skills and MCP servers. Use Hugging Face Spaces or Colab for the rest. |
| NVIDIA 8 GB | Video Depth Anything Small, DepthFlow, iw3, RIFE, SeedVR2 (GGUF), HunyuanVideo-Foley (fp8), MMAudio, CorridorKey, WanGP small models |
| NVIDIA 12–16 GB | DepthCrafter at low res, Hunyuan3D 2.0 with texture, SAM 3, most ComfyUI video workflows |
| NVIDIA 24 GB | TRELLIS.2, Wan 2.2 camera control (fp8), Uni3C in ComfyUI, VDA Large (personal work only) |
| Rent a 48–80 GB GPU | Vista4D, EX-4D, GEN3C, Lyra, Stable Virtual Camera at full size |

## Licenses {#licenses data-nav="Licenses"}

- **Non-commercial (not for monetized videos):** DepthCrafter, StereoCrafter, Depth Anything V2 Base/Large, Video Depth Anything Base/Large, DA3 Large/Giant, Stable Virtual Camera (outputs too), Apple SHARP, ProPainter, MatAnyone, GIMM-VFI, MMAudio weights, GVHMR, Shadertoy Fuses.
- **Territory limits:** Tencent Hunyuan models (Hunyuan3D, HunyuanVideo-Foley, HY-World) are not licensed in the EU, UK or South Korea.
- **Revenue caps:** Stability AI models are free under $1M a year; LTX-2 under $10M. Remotion needs a company license from 4 people.
- **Safe for paid work:** Depth Anything V2/Video Depth Anything **Small**, DA3 Small/Base/Mono-Large, Distill-Any-Depth, TRELLIS.2, iw3, DepthFlow, Brush, SuperSplat, COLMAP, SAM 2/3, SAM 3D Body, beat_this, Blender, FFmpeg.
- **Rule of thumb:** the model's license applies even when the app around it is MIT or GPL. Check the model card, not just the repo.

## How this was researched {#method data-nav="Method"}

Seven research tracks ran in parallel on 29 September 2026: depth and stereo; parallax and AI camera moves; real 3D from 2D; Claude skills and MCP servers; the After Effects ecosystem; the Resolve and Fusion ecosystem; and VFX plus sound effects. Each tool was checked on its GitHub page or official docs. Some sites (Hugging Face, Adobe, Blackmagic, blender.org) were blocked from the research sandbox; facts that come only from press or search results are marked “Not verified at source” in the catalog.

Stay safe: install only from official repos. Fake paid copies of DepthFlow, lookalike “SAM 3D” sites and “cracked Resolve Studio” repos exist.
