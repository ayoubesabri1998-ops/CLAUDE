"""Build a 2.5D parallax shot in Blender from a photo and its depth map, then render it.

Run headless (no Blender window needed):
  blender -b -P blender_parallax.py -- --image plate.png --depth plate_depth.png --move dolly

Or paste into Blender's Scripting tab, or send it through Blender MCP (execute_blender_code)
after setting ARGS at the bottom of this file. Inside an open Blender it adds a new scene and
never touches your current one.

Depth convention: white = near, black = far (Depth Anything style). Add --invert for the opposite.
Moves: dolly, dolly_out, orbit, crane, truck, dolly_zoom (the "vertigo" look).
The image is enlarged just enough that the move never shows its edges.
Output: a PNG sequence plus a .blend copy, so you can tweak the shot in Blender.
Turn the PNGs into a ProRes file for AE / Resolve with:
  ffmpeg -framerate 30 -i shot_%04d.png -c:v prores_ks -profile:v 3 -pix_fmt yuv422p10le shot.mov
"""
import argparse
import math
import os
import sys

import bpy  # import before bmesh / mathutils: they only exist once bpy is loaded
import bmesh
from mathutils import Vector

MOVES = ("dolly", "dolly_out", "orbit", "crane", "truck", "dolly_zoom")


def parse(argv):
    ap = argparse.ArgumentParser(prog="blender_parallax.py")
    ap.add_argument("--image", required=True, help="photo or frame (PNG/JPG/EXR)")
    ap.add_argument("--depth", required=True, help="depth map, same framing as the image (16-bit PNG or EXR best)")
    ap.add_argument("--out", default=None, help="output prefix, e.g. renders/shot_  (default: next to the image)")
    ap.add_argument("--move", choices=MOVES, default="dolly")
    ap.add_argument("--amount", type=float, default=0.15, help="size of the move, 0.05 subtle to 0.3 strong")
    ap.add_argument("--strength", type=float, default=0.25, help="depth relief; lower it if edges smear")
    ap.add_argument("--pivot", type=float, default=0.5, help="depth value that stays in place (0 far .. 1 near)")
    ap.add_argument("--invert", action="store_true", help="use when the depth map is black = near")
    ap.add_argument("--seconds", type=float, default=4.0)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--lens", type=float, default=35.0, help="camera focal length in mm")
    ap.add_argument("--overscan", type=float, default=1.02, help="minimum enlargement; raised automatically for the move")
    ap.add_argument("--grid", type=int, default=400, help="mesh detail across the width")
    ap.add_argument("--smooth", type=int, default=2, help="geometry smoothing passes; softens tearing at depth edges")
    ap.add_argument("--max-width", type=int, default=1920)
    ap.add_argument("--linear", action="store_true", help="constant speed instead of ease in / ease out")
    ap.add_argument("--dof", type=float, default=0.0, help="f-stop for depth of field on the subject (0 = off)")
    ap.add_argument("--motion-blur", action="store_true")
    ap.add_argument("--engine", choices=("cycles", "eevee", "workbench"), default="cycles")
    ap.add_argument("--samples", type=int, default=16)
    ap.add_argument("--gpu", action="store_true", help="render Cycles on an NVIDIA GPU (OptiX or CUDA)")
    ap.add_argument("--no-render", action="store_true", help="only build and save the .blend")
    return ap.parse_args(argv)


def new_scene():
    """Headless: start from an empty file. Inside an open Blender: add a new scene, never touch the user's."""
    if bpy.app.background:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        return bpy.context.scene
    scene = bpy.data.scenes.new("TAWLIF Parallax")
    if bpy.context.window is not None:
        bpy.context.window.scene = scene
    return scene


def load_image(path, colorspace):
    img = bpy.data.images.load(os.path.abspath(path), check_existing=True)
    img.colorspace_settings.name = colorspace
    return img


def camera_path(move, amt, d0):
    """Return f(s) -> (camera position, lens multiplier) for s in 0..1. The camera always looks at the origin."""
    if move == "dolly":
        return lambda s: (Vector((0, 0, d0 * (1 - amt * s))), 1.0)
    if move == "dolly_out":
        return lambda s: (Vector((0, 0, d0 * (1 - amt * (1 - s)))), 1.0)
    if move == "orbit":
        ang = math.radians(amt * 60)

        def orbit(s):
            t = -ang + 2 * ang * s
            return Vector((d0 * math.sin(t), 0, d0 * math.cos(t))), 1.0
        return orbit
    if move == "crane":
        return lambda s: (Vector((0, amt * d0 * (s - 0.5), d0)), 1.0)
    if move == "truck":
        return lambda s: (Vector((amt * d0 * (s - 0.5), 0, d0)), 1.0)
    # dolly_zoom: move in while widening the lens so the subject keeps its size
    return lambda s: (Vector((0, 0, d0 * (1 - 2 * amt * s))), 1 - 2 * amt * s)


def needed_overscan(path, aspect, tan_half, z_far):
    """How much the image must be enlarged so no frame of the move sees past its edges."""
    worst = 1.0
    up_world = Vector((0, 1, 0))
    for i in range(41):
        pos, lens_mult = path(i / 40)
        th = tan_half / lens_mult
        tv = th / aspect
        fwd = (-pos).normalized()
        right = fwd.cross(up_world).normalized()
        up = right.cross(fwd)
        for sx in (-1, 1):
            for sy in (-1, 1):
                d = fwd + right * (th * sx) + up * (tv * sy)
                if d.z >= 0:
                    return 4.0
                hit = pos + d * ((z_far - pos.z) / d.z)
                worst = max(worst, abs(hit.x) / (aspect / 2), abs(hit.y) / 0.5)
    return worst


def make_plane(scene, width, height, grid):
    xs = max(2, grid)
    ys = max(2, int(round(grid * height / width)))
    mesh = bpy.data.meshes.new("ParallaxPlane")
    bm = bmesh.new()
    bm.loops.layers.uv.new("UVMap")  # create_grid only writes UVs into an existing UV layer
    bmesh.ops.create_grid(bm, x_segments=xs, y_segments=ys, size=0.5, calc_uvs=True)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new("ParallaxPlane", mesh)
    obj.scale = (width, height, 1.0)
    scene.collection.objects.link(obj)
    return obj


def make_material(plate):
    mat = bpy.data.materials.new("Plate")
    if bpy.app.version < (5, 0, 0):
        mat.use_nodes = True  # always on from Blender 5.0
    nt = mat.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = plate
    tex.extension = "EXTEND"
    emit = nt.nodes.new("ShaderNodeEmission")
    emit.inputs["Strength"].default_value = 1.0
    nt.links.new(tex.outputs["Color"], emit.inputs["Color"])
    nt.links.new(emit.outputs["Emission"], out.inputs["Surface"])
    nt.nodes.active = tex
    return mat


def set_engine(scene, a):
    if a.engine == "cycles":
        scene.render.engine = "CYCLES"
        scene.cycles.samples = a.samples
        scene.cycles.use_denoising = False
        if a.gpu:
            try:
                prefs = bpy.context.preferences.addons["cycles"].preferences
                for kind in ("OPTIX", "CUDA"):
                    try:
                        prefs.compute_device_type = kind
                        break
                    except TypeError:
                        continue
                prefs.get_devices()
                for d in prefs.devices:
                    d.use = True
                scene.cycles.device = "GPU"
            except Exception as e:  # noqa: BLE001 - fall back to CPU
                print("GPU not available, rendering on CPU:", e)
    elif a.engine == "eevee":
        for name in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
            try:
                scene.render.engine = name
                break
            except TypeError:
                continue
    else:
        scene.render.engine = "BLENDER_WORKBENCH"
        scene.display.shading.light = "FLAT"
        scene.display.shading.color_type = "TEXTURE"


def main(argv):
    a = parse(argv)
    scene = new_scene()
    plate = load_image(a.image, "sRGB")
    depth = load_image(a.depth, "Non-Color")
    w_px, h_px = plate.size
    if not w_px or not h_px:
        raise SystemExit(f"Could not read image: {a.image}")

    aspect = w_px / h_px
    sensor = 36.0
    tan_half = sensor / 2.0 / a.lens
    d0 = (aspect / 2.0) / tan_half  # camera distance that frames the image exactly
    path = camera_path(a.move, a.amount, d0)
    z_far = -a.pivot * a.strength  # the farthest the displaced surface can sit behind the plane
    over = max(a.overscan, needed_overscan(path, aspect, tan_half, z_far) * 1.02)
    print(f"Image enlarged {over:.2f}x so the {a.move} never shows its edges")

    plane = make_plane(scene, aspect * over, over, a.grid)
    plane.data.materials.append(make_material(plate))

    tex = bpy.data.textures.new("Depth", type="IMAGE")
    tex.image = depth
    tex.extension = "EXTEND"
    disp = plane.modifiers.new("Depth", "DISPLACE")
    disp.texture = tex
    disp.texture_coords = "UV"
    disp.direction = "NORMAL"
    disp.strength = -a.strength if a.invert else a.strength
    disp.mid_level = (1.0 - a.pivot) if a.invert else a.pivot
    if a.smooth > 0:
        sm = plane.modifiers.new("Soften", "SMOOTH")
        sm.factor = 0.5
        sm.iterations = a.smooth

    target = bpy.data.objects.new("Target", None)
    target.rotation_euler = (-math.pi / 2, 0, 0)  # its Z axis points to world +Y: the camera's "up"
    scene.collection.objects.link(target)
    cam_data = bpy.data.cameras.new("Camera")
    cam_data.lens = a.lens
    cam_data.sensor_width = sensor
    cam_data.sensor_fit = "HORIZONTAL"
    cam = bpy.data.objects.new("Camera", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    track = cam.constraints.new("TRACK_TO")
    track.target = target
    track.track_axis = "TRACK_NEGATIVE_Z"
    track.up_axis = "UP_Y"
    track.use_target_z = True  # keep the image upright; world Z is the viewing axis here
    if a.dof > 0:
        cam_data.dof.use_dof = True
        cam_data.dof.focus_object = target
        cam_data.dof.aperture_fstop = a.dof

    frames = max(2, int(round(a.seconds * a.fps)))
    scene.frame_start, scene.frame_end = 1, frames
    scene.render.fps = a.fps
    scale = min(1.0, a.max_width / w_px)
    scene.render.resolution_x = int(round(w_px * scale / 2)) * 2
    scene.render.resolution_y = int(round(h_px * scale / 2)) * 2
    scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.render.use_motion_blur = a.motion_blur
    set_engine(scene, a)

    edit_prefs = bpy.context.preferences.edit
    old_interp = edit_prefs.keyframe_new_interpolation_type
    edit_prefs.keyframe_new_interpolation_type = "LINEAR" if a.linear else "BEZIER"
    if a.move == "orbit":
        # A real arc: the camera sits on a pivot at the image centre and the pivot turns.
        pivot = bpy.data.objects.new("OrbitPivot", None)
        scene.collection.objects.link(pivot)
        cam.parent = pivot
        cam.location = (0, 0, d0)
        ang = math.radians(a.amount * 60)
        for frame, rot in ((1, -ang), (frames, ang)):
            pivot.rotation_euler = (0, rot, 0)
            pivot.keyframe_insert("rotation_euler", frame=frame)
    else:
        for frame, s in ((1, 0.0), (frames, 1.0)):
            pos, lens_mult = path(s)
            cam.location = pos
            cam.keyframe_insert("location", frame=frame)
            if a.move == "dolly_zoom":
                cam_data.lens = a.lens * lens_mult
                cam_data.keyframe_insert("lens", frame=frame)
    edit_prefs.keyframe_new_interpolation_type = old_interp

    base = os.path.splitext(os.path.abspath(a.image))[0]
    out = os.path.abspath(a.out) if a.out else base + f"_{a.move}_"
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    scene.render.filepath = out
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"

    blend_path = (out.rstrip("_") or out) + ".blend"
    bpy.ops.wm.save_as_mainfile(filepath=blend_path, copy=True)
    print(f"Saved scene: {blend_path}")
    if not a.no_render:
        bpy.ops.render.render(animation=True, scene=scene.name)
        print(f"Rendered {frames} frames to {out}####.png")


# When pasted into Blender's Scripting tab or sent through Blender MCP, set ARGS here, e.g.
# ARGS = ["--image", "C:/shots/plate.png", "--depth", "C:/shots/plate_depth.png", "--move", "orbit"]
ARGS = None

if __name__ == "__main__":
    if "--" in sys.argv:
        main(sys.argv[sys.argv.index("--") + 1:])
    elif ARGS:
        main(ARGS)
    else:
        print(__doc__)
