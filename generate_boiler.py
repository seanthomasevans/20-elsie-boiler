"""
Generate 3D model of boiler closet at 20 Elsie Lane #217.
Rinnai RXP199iN tankless + open-loop hydronic heating.
v11: Sharp 90° SharkBite elbows everywhere. All manifold pipes against back wall.
Expansion tank centered between Rinnai left edge and left wall (X=2").
Condensate fully connected. Floor cleared. AH edge-to-edge.

Run: blender --background --python generate_boiler.py

Coordinate system: X = width (left to right), Y = depth (front to back), Z = height.
Origin = front-left-floor corner of closet interior.
Left wall = exterior (vents, outdoor tap, outdoor gas exit here).
"""
import bpy
import bmesh
import math
import os
from mathutils import Vector


# ============================================================
# Unit conversion
# ============================================================
def inch(v):
    return v * 0.0254


# ============================================================
# Closet
# ============================================================
CW = inch(36)
CD = inch(32)
CH = inch(80)
WALL_T = inch(4)
EXT_T = inch(6)
AH_BTM = inch(64)


# ============================================================
# Rinnai RXP199iN — shifted LEFT and DOWN per Sean's direction
# Left bias puts it closer to gas entry; lower mount gives vent clearance
# ============================================================
RW = inch(18.5)
RD = inch(11.41)
RH = inch(30.11)
RB = inch(24)        # Bottom at 24" AFF (was 32")
RT = RB + RH          # Top at ~54.11" AFF (10" below AH)

RX0 = inch(4)          # Left edge at 4" (was ~8.75", shifted left ~4")
RX1 = RX0 + RW         # ~22.5"
RY1 = CD                # Flush with back wall
RY0 = CD - RD           # ~20.59"
RCX = (RX0 + RX1) / 2   # ~13.25"
RCY = (RY0 + RY1) / 2   # ~26.3"


# ============================================================
# Port positions (per Figure 3, relative to Rinnai body)
# ============================================================
P_COLD_X = RCX - inch(2.55)   # ~15.7"
P_HOT_X = RCX                  # ~18"
P_COND_X = RCX + inch(2.55)   # ~20.55"
P_Y = RCY
P_Z = RB                       # Ports exit bottom at 32"

GAS_X = RX1                    # Gas port on RIGHT side
GAS_Y = RCY
GAS_Z = RB + inch(2.83)        # ~34.83"

V_EXH_X = RX0 + inch(5.91)    # Exhaust on left side of top
V_INT_X = RX0 + inch(15.97)   # Intake on right side of top


# ============================================================
# Pipe radii
# ============================================================
R_VENT = inch(1.5)
R_GAS = inch(0.375)
R_PIPE = inch(0.375)     # 3/4" CPVC
R_HEAT = inch(0.5)       # 1" CPVC
R_COND = inch(0.19)
R_SMALL = inch(0.3)


# ============================================================
# Manifold heights — staggered to prevent intersections
# All below Rinnai bottom (24"). Each level separated by 2-3".
# ============================================================
Z_HEAT_S = inch(12)      # Heating supply (lowest)
Z_HEAT_R = inch(14)      # Heating return
Z_MANIFOLD = inch(16)    # Main cold + hot horizontal runs
Z_BLEND = inch(19)       # Cold blend to TMV (crosses over manifold)
Z_DHW = inch(21)         # DHW / TMV height


# ============================================================
# Vents: UNDER the air handler, not inside it
# Rinnai top now at ~54", AH bottom at 64". Vents run at 62" under AH.
# Vents a bit closer to opening per Sean's direction.
# ============================================================
VENT_Z = inch(62)                 # Vent horizontal run at 62" (under AH at 64")
VENT_Y_EXH = CD - inch(6)        # Back vent (exhaust), slightly off back wall
VENT_Y_INT = CD - inch(18)       # Front vent (intake), 12" forward of exhaust


# ============================================================
# Gas routing — enters from LEFT ceiling, routes under Rinnai
# ============================================================
GAS_CEIL_X = inch(4)              # Left side of closet
GAS_CEIL_Y = inch(10)             # Near closet opening (was near back wall)
GAS_UNDER_Z = inch(20)            # Routes under Rinnai (bottom now at 24")
SHUTOFF_Z = inch(56)              # Gas shutoff on left-side drop


# ============================================================
# Component positions along manifold (X axis)
# Rinnai shifted left: cold port ~10.7", hot port ~13.25", cond ~15.8"
# Cold manifold: X=3" to X=10" (left side, under cold port)
# Hot manifold: X=13" to X=28" (right side, under hot port)
# No X overlap = no intersection at same height
# ============================================================
COLD_X = inch(3)           # Cold entry from floor (left of Rinnai)
V1_X = inch(5)             # Cold shutoff
T1_X = inch(8)             # Cold tee (return merge + blend branch)
V2_X = inch(16)            # Hot shutoff (clear of condensate at X≈15.8")
T2_X = inch(19)            # Hot tee (DHW + heating branch)
ZV_X = inch(22)            # Zone valve (on heating supply)
TMV_X = inch(26)           # TMV

# Risers: on walls, outside Rinnai X range (4-22.5")
RISER_S_X = CW - inch(2)  # Supply riser on RIGHT WALL (~34")
RISER_R_X = inch(2)        # Return riser on LEFT WALL
CP_X = inch(4)             # Circ pump (on return line, near left wall)
CV_X = inch(6)             # Check valve (on return line)

# Y-depth offsets — everything against the walls
Y_WALL = CD - inch(2)     # Main manifold horizontals against back wall
Y_RISER = Y_WALL           # Heating risers also against back wall
Y_BLEND = CD - inch(4)    # Cold blend line slightly off wall (avoids crossing verticals)

# AH connections — FRONT FACE (Y=2", since AH extends to Y=2")
AH_FRONT_Y = inch(2)
AH_SX = inch(26)           # Supply connection X on AH front
AH_RX = inch(10)           # Return connection X on AH front
AH_SZ = AH_BTM + inch(4)   # Supply Z on front (68")
AH_RZ = AH_BTM + inch(2)   # Return Z on front (66")

# Floor drain — RIGHT side per photos
FD_X = CW - inch(8)         # Right side (~28")
FD_Y = inch(8)

# Outdoor branches through left wall
TAP_Z = inch(16)            # Outdoor tap at manifold height (was 24, now manifold is 16)
TAP_Y = inch(10)
OGAS_Z = inch(60)           # Outdoor gas below AH (64"), above Rinnai top (54")
OGAS_Y = inch(14)           # Near front, clear of equipment


# ============================================================
# Bend radii per pipe size
# ============================================================
BEND_VENT = inch(4.5)
BEND_MAIN = inch(2)
BEND_HEAT = inch(2.5)
BEND_GAS = inch(2)
BEND_COND = inch(1.5)
BEND_SMALL = inch(1.5)


# ============================================================
# Materials: CPVC + SharkBite + PVC + CSST + Cast Iron
# ============================================================
PALETTE = {
    # Structure
    "wall_ext":     ((0.75, 0.72, 0.68), 0.85, 0.0),
    "wall_int":     ((0.88, 0.86, 0.83), 0.80, 0.0),
    "floor":        ((0.55, 0.52, 0.48), 0.90, 0.0),
    "ceiling":      ((0.90, 0.88, 0.85), 0.80, 0.0),
    # Equipment
    "air_handler":  ((0.72, 0.68, 0.62), 0.55, 0.15),
    "rinnai":       ((0.85, 0.87, 0.90), 0.35, 0.30),
    "rinnai_face":  ((0.20, 0.25, 0.35), 0.40, 0.10),
    "display":      ((0.12, 0.30, 0.70), 0.25, 0.10),
    # Plumbing materials
    "cpvc":         ((0.88, 0.82, 0.72), 0.50, 0.0),
    "cpvc_hot":     ((0.85, 0.78, 0.68), 0.50, 0.0),
    "sharkbite":    ((0.78, 0.67, 0.25), 0.22, 0.90),
    "csst":         ((0.82, 0.72, 0.12), 0.28, 0.75),
    "pvc":          ((0.93, 0.92, 0.90), 0.45, 0.0),
    "cast_iron":    ((0.12, 0.11, 0.13), 0.55, 0.65),
    "copper_stub":  ((0.72, 0.45, 0.20), 0.25, 0.95),
    # Components
    "valve_handle": ((0.15, 0.40, 0.75), 0.60, 0.0),
    "zv_actuator":  ((0.35, 0.35, 0.38), 0.50, 0.10),
    "exp_tank":     ((0.15, 0.35, 0.65), 0.45, 0.20),
    "panel":        ((0.32, 0.34, 0.38), 0.45, 0.25),
    "controller":   ((0.80, 0.75, 0.65), 0.50, 0.0),
    "duct":         ((0.68, 0.66, 0.62), 0.50, 0.20),
    "drain":        ((0.25, 0.25, 0.25), 0.55, 0.40),
    "port":         ((0.50, 0.52, 0.55), 0.35, 0.50),
    "bracket":      ((0.40, 0.40, 0.42), 0.55, 0.30),
}


# ============================================================
# Scene setup
# ============================================================
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for db in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras,
               bpy.data.lights, bpy.data.curves):
        for item in list(db):
            if item.users == 0:
                db.remove(item)


def setup_world():
    scene = bpy.context.scene
    world = bpy.data.worlds.new("W")
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs[0].default_value = (0.82, 0.85, 0.90, 1.0)
    bg.inputs[1].default_value = 0.7
    nt.links.new(bg.outputs[0], out.inputs[0])


def make_mat(name, color, roughness, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return mat


def build_mats():
    m = {}
    for k, (c, r, met) in PALETTE.items():
        m[k] = make_mat(k, c, r, metallic=met)
    return m


# ============================================================
# Geometry helpers
# ============================================================
def _deselect_all():
    try:
        bpy.ops.object.select_all(action='DESELECT')
    except Exception:
        pass


def box(name, x0, x1, y0, y1, z0, z1, mat):
    bm = bmesh.new()
    v = [
        bm.verts.new((x0, y0, z0)), bm.verts.new((x1, y0, z0)),
        bm.verts.new((x1, y1, z0)), bm.verts.new((x0, y1, z0)),
        bm.verts.new((x0, y0, z1)), bm.verts.new((x1, y0, z1)),
        bm.verts.new((x1, y1, z1)), bm.verts.new((x0, y1, z1)),
    ]
    for f in [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]:
        try:
            bm.faces.new([v[i] for i in f])
        except Exception:
            pass
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def cyl(name, center, radius, depth, mat, axis='Z'):
    _deselect_all()
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=24, radius=radius, depth=depth, location=center
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.data.name = name
    if axis == 'X':
        obj.rotation_euler = (0, math.radians(90), 0)
    elif axis == 'Y':
        obj.rotation_euler = (math.radians(90), 0, 0)
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj


# ============================================================
# Pipe routing with smooth quadratic bezier bends
# ============================================================
def _smooth_path(waypoints, bend_r, arc_segs=8):
    pts = [Vector(p) for p in waypoints]
    if len(pts) < 3:
        return [tuple(p) for p in pts]
    result = [tuple(pts[0])]
    for i in range(1, len(pts) - 1):
        p_prev, p_curr, p_next = pts[i-1], pts[i], pts[i+1]
        d_in = p_curr - p_prev
        d_out = p_next - p_curr
        if d_in.length < 1e-6 or d_out.length < 1e-6:
            result.append(tuple(p_curr))
            continue
        d_in_n = d_in.normalized()
        d_out_n = d_out.normalized()
        if d_in_n.dot(d_out_n) > 0.995:
            result.append(tuple(p_curr))
            continue
        r = min(bend_r, d_in.length * 0.45, d_out.length * 0.45)
        p0 = p_curr - d_in_n * r
        p2 = p_curr + d_out_n * r
        for j in range(arc_segs + 1):
            t = j / arc_segs
            p = (1-t)**2 * p0 + 2*(1-t)*t * p_curr + t**2 * p2
            result.append(tuple(p))
    result.append(tuple(pts[-1]))
    return result


def pipe_run(name, waypoints, radius, mat, bend_r=None, bevel_res=6, sharp=False):
    if sharp:
        smooth = [tuple(w) for w in waypoints]
    elif bend_r is None:
        bend_r = radius * 6
        smooth = _smooth_path(waypoints, bend_r)
    else:
        smooth = _smooth_path(waypoints, bend_r)
    _deselect_all()
    curve = bpy.data.curves.new(name + '_c', 'CURVE')
    curve.dimensions = '3D'
    curve.bevel_depth = radius
    curve.bevel_resolution = bevel_res
    curve.fill_mode = 'FULL'
    try:
        curve.use_fill_caps = True
    except AttributeError:
        pass
    spline = curve.splines.new('POLY')
    spline.points.add(len(smooth) - 1)
    for i, (x, y, z) in enumerate(smooth):
        spline.points[i].co = (x, y, z, 1.0)
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    obj.data.name = name
    obj.data.materials.append(mat)
    return obj


# ============================================================
# Component helpers — proper SharkBite fitting geometry
# ============================================================
def sharkbite_tee(name, x, y, z, pipe_r, M, main_axis='X', branch_dir='Z'):
    """SharkBite push-to-connect tee: T-shaped brass body with branch."""
    body_r = pipe_r * 1.8
    main_len = pipe_r * 7
    branch_len = pipe_r * 5

    # Main inline body
    cyl(name, (x, y, z), body_r, main_len, M["sharkbite"], main_axis)

    # Branch stub perpendicular to main
    if branch_dir == 'Z':
        bpos = (x, y, z + body_r + branch_len / 2)
        baxis = 'Z'
    elif branch_dir == '-Z':
        bpos = (x, y, z - body_r - branch_len / 2)
        baxis = 'Z'
    elif branch_dir == 'Y':
        bpos = (x, y + body_r + branch_len / 2, z)
        baxis = 'Y'
    elif branch_dir == '-Y':
        bpos = (x, y - body_r - branch_len / 2, z)
        baxis = 'Y'
    elif branch_dir == 'X':
        bpos = (x + body_r + branch_len / 2, y, z)
        baxis = 'X'
    elif branch_dir == '-X':
        bpos = (x - body_r - branch_len / 2, y, z)
        baxis = 'X'
    else:
        bpos = (x, y, z + body_r + branch_len / 2)
        baxis = 'Z'

    cyl(name + "_br", bpos, body_r * 0.85, branch_len, M["sharkbite"], baxis)


def sharkbite_valve(name, x, y, z, pipe_r, M, axis='X'):
    """SharkBite ball valve: brass body with ball housing bulge + lever handle."""
    body_r = pipe_r * 2.0
    body_len = pipe_r * 6

    # Main body
    cyl(name, (x, y, z), body_r, body_len, M["sharkbite"], axis)

    # Ball housing (slightly wider center bulge)
    cyl(name + "_ball", (x, y, z), body_r * 1.15, body_len * 0.35, M["sharkbite"], axis)

    # Flat lever handle (box, not cylinder)
    hl = pipe_r * 5
    hw = pipe_r * 0.8
    ht = pipe_r * 0.35
    if axis in ('X', 'Y'):
        box(name + "_h",
            x - hw, x + hw,
            y - ht, y + ht,
            z + body_r * 0.7, z + body_r * 0.7 + hl,
            M["valve_handle"])
    else:
        box(name + "_h",
            x + body_r * 0.7, x + body_r * 0.7 + hl,
            y - ht, y + ht,
            z - hw, z + hw,
            M["valve_handle"])


# ============================================================
# BUILD: Closet shell
# ============================================================
def build_closet(M):
    box("Floor", -EXT_T, CW + WALL_T, -inch(1), CD + WALL_T, -inch(2), 0, M["floor"])
    box("Ceiling", -EXT_T, CW + WALL_T, -inch(1), CD + WALL_T, CH, CH + inch(1.5), M["ceiling"])
    box("WallLeft", -EXT_T, 0, -inch(1), CD + WALL_T, 0, CH, M["wall_ext"])
    box("WallRight", CW, CW + WALL_T, -inch(1), CD + WALL_T, 0, CH, M["wall_int"])
    box("WallBack", 0, CW, CD, CD + WALL_T, 0, CH, M["wall_int"])


# ============================================================
# BUILD: Air handler (64-80" AFF, connections on FRONT FACE)
# ============================================================
def build_air_handler(M):
    # AH goes edge to edge (nearly full closet width), back to front
    box("AirHandler", inch(1), CW - inch(1), inch(2), CD - inch(1),
        AH_BTM, CH - inch(1), M["air_handler"])
    box("SupplyDuct", inch(12), inch(22), inch(8), inch(18),
        CH - inch(1), CH + inch(4), M["duct"])
    # No stubs modeled — pipes connect directly to AH bottom face


# ============================================================
# BUILD: Rinnai RXP199iN
# ============================================================
def build_rinnai(M):
    box("Rinnai", RX0, RX1, RY0, RY1, RB, RT, M["rinnai"])
    box("RinnaiFace", RX0 + inch(0.5), RX1 - inch(0.5), RY0 - inch(0.1), RY0,
        RB + inch(2), RT - inch(2), M["rinnai_face"])
    box("RinnaiDisplay", RX0 + inch(5), RX1 - inch(5), RY0 - inch(0.15), RY0 - inch(0.05),
        RT - inch(5), RT - inch(3), M["display"])
    box("MountBracketTop", RX0 + inch(2), RX1 - inch(2), RY1, RY1 + inch(0.5),
        RT - inch(3), RT - inch(1), M["bracket"])
    box("MountBracketBot", RX0 + inch(2), RX1 - inch(2), RY1, RY1 + inch(0.5),
        RB + inch(1), RB + inch(3), M["bracket"])

    # Port stubs (copper at threads for SharkBite transition)
    stub = inch(3)
    cyl("Port_Cold", (P_COLD_X, P_Y, RB - stub / 2), R_PIPE * 1.4, stub, M["copper_stub"])
    cyl("Port_Hot", (P_HOT_X, P_Y, RB - stub / 2), R_PIPE * 1.4, stub, M["copper_stub"])
    cyl("Port_Cond", (P_COND_X, P_Y, RB - stub / 2), R_COND * 2, stub, M["port"])
    cyl("Port_Gas", (RX1 + inch(1), GAS_Y, GAS_Z), R_GAS * 1.4, inch(2), M["port"], 'X')
    cyl("Port_VentExh", (V_EXH_X, P_Y, RT + inch(1)), R_VENT, inch(2), M["port"])
    cyl("Port_VentInt", (V_INT_X, P_Y, RT + inch(1)), R_VENT, inch(2), M["port"])

    box("MCC912", RX1 + inch(1), RX1 + inch(7), RY0, RY0 + inch(1.5),
        RT - inch(5), RT - inch(2), M["controller"])


# ============================================================
# BUILD: Vents — UNDER the air handler at 62" AFF
# ============================================================
def build_vents(M):
    # Exhaust (back vent = out): rises from top, sharp 90° PVC elbows at each turn
    # Segments: vertical rise, 90° elbow, depth run, 90° elbow, horizontal to wall
    pipe_run("VentExh_Run", [
        (V_EXH_X, P_Y, RT + inch(1)),
        (V_EXH_X, P_Y, VENT_Z),
        (V_EXH_X, VENT_Y_EXH, VENT_Z),
        (-EXT_T - inch(1), VENT_Y_EXH, VENT_Z),
    ], R_VENT, M["pvc"], sharp=True)

    # PVC elbows at each turn (visual markers)
    cyl("VentExh_Elb1", (V_EXH_X, P_Y, VENT_Z),
        R_VENT * 1.3, R_VENT * 2, M["pvc"])
    cyl("VentExh_Elb2", (V_EXH_X, VENT_Y_EXH, VENT_Z),
        R_VENT * 1.3, R_VENT * 2, M["pvc"], 'X')

    cyl("VentExh_Cap", (-EXT_T - inch(2), VENT_Y_EXH, VENT_Z),
        R_VENT + inch(0.5), inch(2), M["pvc"], 'X')

    # Intake (front vent = in): 12" forward of exhaust, sharp 90° elbows
    pipe_run("VentInt_Run", [
        (V_INT_X, P_Y, RT + inch(1)),
        (V_INT_X, P_Y, VENT_Z),
        (V_INT_X, VENT_Y_INT, VENT_Z),
        (-EXT_T - inch(1), VENT_Y_INT, VENT_Z),
    ], R_VENT, M["pvc"], sharp=True)

    # PVC elbows at each turn
    cyl("VentInt_Elb1", (V_INT_X, P_Y, VENT_Z),
        R_VENT * 1.3, R_VENT * 2, M["pvc"])
    cyl("VentInt_Elb2", (V_INT_X, VENT_Y_INT, VENT_Z),
        R_VENT * 1.3, R_VENT * 2, M["pvc"], 'X')

    cyl("VentInt_Cap", (-EXT_T - inch(2), VENT_Y_INT, VENT_Z),
        R_VENT + inch(0.5), inch(2), M["pvc"], 'X')


# ============================================================
# BUILD: Gas — CSST from LEFT ceiling, routes under Rinnai
# ============================================================
def build_gas(M):
    # CSST drops from LEFT ceiling near front (Y=10"), steps back to back wall,
    # runs horizontal under Rinnai to right-side gas port
    pipe_run("Gas_Line", [
        (GAS_CEIL_X, GAS_CEIL_Y, CH + inch(2)),      # From ceiling
        (GAS_CEIL_X, GAS_CEIL_Y, GAS_UNDER_Z),        # Drop to under-Rinnai height
        (GAS_CEIL_X, GAS_Y, GAS_UNDER_Z),             # Step back to Rinnai depth
        (RX1 + inch(2), GAS_Y, GAS_UNDER_Z),          # Run right under Rinnai
        (RX1 + inch(2), GAS_Y, GAS_Z),                # Rise to gas port
    ], R_GAS, M["csst"], BEND_GAS)

    # Gas shutoff on the left-side vertical drop
    sharkbite_valve("GasShutoff", GAS_CEIL_X, GAS_CEIL_Y, SHUTOFF_Z, R_GAS, M, 'Z')

    # Outdoor gas tee + branch through left wall (above electrical at Z=72")
    sharkbite_tee("GasTee_Out", GAS_CEIL_X, GAS_CEIL_Y, OGAS_Z, R_GAS, M, 'Z', '-X')
    pipe_run("Gas_Outdoor", [
        (GAS_CEIL_X, GAS_CEIL_Y, OGAS_Z),
        (-EXT_T - inch(1), GAS_CEIL_Y, OGAS_Z),
    ], R_GAS, M["csst"], BEND_GAS)

    sharkbite_valve("GasOutShutoff", inch(1), GAS_CEIL_Y, OGAS_Z, R_GAS, M, 'X')


# ============================================================
# BUILD: Cold supply (CPVC, from floor, outdoor tap branch)
# ============================================================
def build_cold_supply(M):
    # Cold riser from floor against back wall, horizontal to port, up to port
    # Sharp 90° elbows (SharkBite) at each turn
    pipe_run("Cold_Supply", [
        (COLD_X, Y_WALL, -inch(2)),
        (COLD_X, Y_WALL, Z_MANIFOLD),
        (P_COLD_X, Y_WALL, Z_MANIFOLD),
        (P_COLD_X, P_Y, Z_MANIFOLD),
        (P_COLD_X, P_Y, P_Z - inch(1)),
    ], R_PIPE, M["cpvc"], sharp=True)

    # V1 cold isolation valve — on wall
    sharkbite_valve("V1", V1_X, Y_WALL, Z_MANIFOLD, R_PIPE, M)

    # T1 cold tee (return merge + blend branch) — on wall
    sharkbite_tee("T1", T1_X, Y_WALL, Z_MANIFOLD, R_PIPE, M, 'X', 'Z')

    # Drain valve (wall-mounted, drains to channel)
    DV_Z = Z_MANIFOLD - inch(4)
    pipe_run("DrainValve_Drop", [
        (V1_X, Y_WALL, Z_MANIFOLD - inch(2)),
        (V1_X, Y_WALL, DV_Z),
    ], R_COND, M["cpvc"], sharp=True)
    sharkbite_valve("DrainValve", V1_X, Y_WALL, DV_Z, R_COND, M, 'Z')

    # Cold blend line from T1 up and over to TMV — against wall with sharp 90s
    pipe_run("ColdBlend_Run", [
        (T1_X, Y_WALL, Z_MANIFOLD),
        (T1_X, Y_WALL, Z_BLEND),
        (T1_X, Y_BLEND, Z_BLEND),
        (TMV_X, Y_BLEND, Z_BLEND),
        (TMV_X, Y_BLEND, Z_DHW),
        (TMV_X, Y_WALL, Z_DHW),
    ], R_SMALL, M["cpvc"], sharp=True)

    # Outdoor tap branch (tee off cold riser, through left wall)
    sharkbite_tee("ColdTee_Tap", COLD_X, Y_WALL, TAP_Z, R_PIPE, M, 'Z', '-Y')
    pipe_run("Cold_OutdoorTap", [
        (COLD_X, Y_WALL, TAP_Z),
        (COLD_X, TAP_Y, TAP_Z),
        (-EXT_T - inch(1), TAP_Y, TAP_Z),
    ], R_PIPE, M["cpvc"], sharp=True)
    sharkbite_valve("TapShutoff", inch(2), TAP_Y, TAP_Z, R_PIPE, M, 'X')


# ============================================================
# BUILD: Hot water out (CPVC)
# ============================================================
def build_hot_out(M):
    # Hot drops from port to wall, runs right along wall to T2. Sharp 90s.
    pipe_run("Hot_FromPort", [
        (P_HOT_X, P_Y, P_Z - inch(1)),
        (P_HOT_X, P_Y, Z_MANIFOLD),
        (P_HOT_X, Y_WALL, Z_MANIFOLD),
        (T2_X, Y_WALL, Z_MANIFOLD),
    ], R_PIPE, M["cpvc_hot"], sharp=True)

    sharkbite_valve("V2", V2_X, Y_WALL, Z_MANIFOLD, R_PIPE, M)
    sharkbite_tee("T2", T2_X, Y_WALL, Z_MANIFOLD, R_PIPE, M, 'X', '-Z')


# ============================================================
# BUILD: TMV and DHW (CPVC)
# ============================================================
def build_tmv_dhw(M):
    # Hot from T2 to TMV — routes along back wall with sharp 90° SharkBite elbows
    pipe_run("Hot_ToTMV", [
        (T2_X, Y_WALL, Z_MANIFOLD),
        (T2_X, Y_WALL, Z_BLEND),
        (TMV_X, Y_WALL, Z_BLEND),
        (TMV_X, Y_WALL, Z_DHW),
    ], R_PIPE, M["cpvc_hot"], sharp=True)

    # TMV body (SharkBite brass, larger cylinder) — on back wall
    cyl("TMV", (TMV_X, Y_WALL, Z_DHW + inch(1.5)), inch(1.8), inch(3.5), M["sharkbite"])

    # DHW out to fixtures (exits right wall) — from back wall
    dhw_z = Z_DHW + inch(1.5)
    pipe_run("DHW_Out", [
        (TMV_X + inch(2), Y_WALL, dhw_z),
        (CW + WALL_T + inch(1), Y_WALL, dhw_z),
    ], R_PIPE, M["cpvc_hot"], sharp=True)


# ============================================================
# BUILD: Heating supply (CPVC, T2 to zone valve to riser to AH)
# Riser at X=29" avoids Rinnai body (X=8.75-27.25")
# ============================================================
def build_heat_supply(M):
    # Supply: T2 drops to heat level, runs right along back wall to riser,
    # up right wall to AH height, then forward + left to AH front face connection
    pipe_run("HS_Run", [
        (T2_X, Y_WALL, Z_MANIFOLD),
        (T2_X, Y_WALL, Z_HEAT_S),
        (RISER_S_X, Y_WALL, Z_HEAT_S),
        (RISER_S_X, Y_WALL, AH_SZ),
        (RISER_S_X, AH_FRONT_Y, AH_SZ),
        (AH_SX, AH_FRONT_Y, AH_SZ),
    ], R_HEAT, M["cpvc_hot"], sharp=True)

    # Zone valve on heating supply horizontal — against back wall
    cyl("ZoneValve", (ZV_X, Y_WALL, Z_HEAT_S), inch(1.5), inch(3.5), M["sharkbite"], 'X')
    box("ZV_Actuator", ZV_X - inch(1), ZV_X + inch(1), Y_WALL - inch(1), Y_WALL + inch(1),
        Z_HEAT_S + inch(1.5), Z_HEAT_S + inch(4), M["zv_actuator"])

    # Expansion tank wall-mounted on RIGHT side, centered between Rinnai right
    # edge (X=22.5") and right wall (X=36"), so X≈29". Near top of Rinnai.
    EXP_X = inch(29)
    EXP_WALL_Z = RB + inch(20)    # Upper Rinnai height (~44" AFF, top at 54")
    # Tee off supply riser to feed expansion tank
    sharkbite_tee("ExpTee", RISER_S_X, Y_WALL, RB + inch(16), R_HEAT, M, 'Z', '-X')
    pipe_run("Exp_Run", [
        (RISER_S_X, Y_WALL, RB + inch(16)),
        (EXP_X, Y_WALL, RB + inch(16)),
    ], R_PIPE, M["cpvc"], sharp=True)

    # Tank hangs vertically on back wall, right side
    cyl("ExpTank", (EXP_X, Y_WALL, EXP_WALL_Z - inch(4)),
        inch(3), inch(9), M["exp_tank"])
    cyl("ExpTank_Cap", (EXP_X, Y_WALL, EXP_WALL_Z - inch(8.5)),
        inch(2.8), inch(1.5), M["exp_tank"])


# ============================================================
# BUILD: Heating return (CPVC, AH to circ pump to T1)
# Riser at X=7" avoids Rinnai body (X=8.75-27.25")
# ============================================================
def build_heat_return(M):
    # Return: from AH front face, back along left wall riser, down to manifold
    # Route: AH front → left to riser X → back to wall → down → along wall to T1
    pipe_run("HR_Run", [
        (AH_RX, AH_FRONT_Y, AH_RZ),
        (RISER_R_X, AH_FRONT_Y, AH_RZ),
        (RISER_R_X, Y_WALL, AH_RZ),
        (RISER_R_X, Y_WALL, Z_HEAT_R),
        (T1_X, Y_WALL, Z_HEAT_R),
        (T1_X, Y_WALL, Z_MANIFOLD),
    ], R_HEAT, M["cpvc"], sharp=True)

    # Circ pump (cast iron body + motor) — on return line against back wall
    cyl("CircPump", (CP_X, Y_WALL, Z_HEAT_R), inch(1.3), inch(3.5), M["cast_iron"], 'X')
    cyl("CircPump_Motor", (CP_X, Y_WALL, Z_HEAT_R + inch(2.5)),
        inch(1.2), inch(2.5), M["cast_iron"])

    # Check valve — on return line against back wall
    cyl("CheckValve", (CV_X, Y_WALL, Z_HEAT_R), inch(1.2), inch(3), M["sharkbite"], 'X')
    cyl("CV_Arrow", (CV_X, Y_WALL, Z_HEAT_R + inch(1.5)), inch(0.4), inch(0.8), M["sharkbite"])


# ============================================================
# BUILD: Condensate drain (PVC)
# ============================================================
def build_condensate(M):
    # Condensate drops from port, routes to wall-mounted neutralizer on back wall
    # Sharp 90° elbows, fully connected from port to drain
    NEUT_Z = RB + inch(2)    # Just above Rinnai bottom, on back wall
    NEUT_X = P_COND_X

    # Drop from condensate port to neutralizer inlet (top of neutralizer box)
    pipe_run("Cond_Drop", [
        (P_COND_X, P_Y, P_Z - inch(1)),
        (P_COND_X, P_Y, NEUT_Z + inch(4)),
        (P_COND_X, Y_WALL, NEUT_Z + inch(4)),
    ], R_COND, M["pvc"], sharp=True)

    # Neutralizer wall-mounted on back wall
    box("Neutralizer", NEUT_X - inch(2), NEUT_X + inch(2),
        Y_WALL - inch(1.5), Y_WALL + inch(1), NEUT_Z, NEUT_Z + inch(4), M["pvc"])

    # Drain line from neutralizer bottom, down wall to floor channel, to floor drain
    pipe_run("Cond_ToDrain", [
        (NEUT_X, Y_WALL, NEUT_Z),
        (NEUT_X, Y_WALL, inch(0.5)),
        (FD_X, Y_WALL, inch(0.5)),
        (FD_X, FD_Y, inch(0.5)),
    ], R_COND, M["drain"], sharp=True)

    # Floor channel strip (shallow trough for drainage, keeps floor clear)
    box("DrainChannel", NEUT_X - inch(1), FD_X + inch(1),
        Y_WALL - inch(1), Y_WALL + inch(0.5), -inch(0.3), inch(0.3), M["drain"])


# ============================================================
# BUILD: Electrical (LEFT/exterior wall)
# Just a switch, 24V transformer, and 120V outlet. Not a full panel.
# ============================================================
def build_electrical(M):
    # Light switch (small rectangular box on wall)
    box("ElecSwitch", -inch(0.3), inch(0.3), inch(10), inch(14),
        inch(46), inch(50), M["panel"])
    # 24V transformer (small box, powers zone valve + Rinnai controls)
    box("ElecXfmr", -inch(0.3), inch(2.5), inch(10), inch(14),
        inch(54), inch(60), M["panel"])
    # 120V outlet (Rinnai blower + electronics plug in here)
    box("ElecOutlet", -inch(0.3), inch(0.3), inch(18), inch(22),
        inch(46), inch(50), M["panel"])


# ============================================================
# BUILD: Floor drain (RIGHT side per photos)
# ============================================================
def build_floor_drain(M):
    cyl("FloorDrain", (FD_X, FD_Y, inch(0.1)), inch(2), inch(0.5), M["drain"])
    box("Drain_X", FD_X - inch(1.5), FD_X + inch(1.5),
        FD_Y - inch(0.1), FD_Y + inch(0.1), inch(0.2), inch(0.4), M["drain"])
    box("Drain_Y", FD_X - inch(0.1), FD_X + inch(0.1),
        FD_Y - inch(1.5), FD_Y + inch(1.5), inch(0.2), inch(0.4), M["drain"])


# ============================================================
# Camera and lighting
# ============================================================
def setup_cameras():
    cam = bpy.data.cameras.new("Cam")
    cam.lens = 20
    obj = bpy.data.objects.new("Cam", cam)
    bpy.context.collection.objects.link(obj)
    obj.location = (CW * 0.6, -CW * 1.6, CH * 0.55)
    obj.rotation_euler = (math.radians(72), 0, math.radians(8))
    bpy.context.scene.camera = obj


def setup_lighting():
    for nm, tp, energy, sz, loc, rot in [
        ("Key", 'AREA', 300, 2.5, (CW, -CW * 0.7, CH * 0.8), (55, 15, 0)),
        ("Fill", 'AREA', 150, 2.0, (-inch(20), -CW * 0.4, CH * 0.6), (60, -20, 0)),
        ("Top", 'AREA', 100, 1.5, (CW / 2, CD / 2, CH + inch(30)), (0, 0, 0)),
    ]:
        light = bpy.data.lights.new(nm, tp)
        light.energy = energy
        if hasattr(light, 'size'):
            light.size = sz
        obj = bpy.data.objects.new(nm, light)
        bpy.context.collection.objects.link(obj)
        obj.location = loc
        obj.rotation_euler = tuple(math.radians(r) for r in rot)
    pt = bpy.data.lights.new("Interior", 'POINT')
    pt.energy = 50
    obj = bpy.data.objects.new("Interior", pt)
    bpy.context.collection.objects.link(obj)
    obj.location = (CW / 2, CD / 3, CH * 0.4)


# ============================================================
# Main
# ============================================================
def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    clear_scene()
    setup_world()
    M = build_mats()

    build_closet(M)
    build_air_handler(M)
    build_rinnai(M)
    build_vents(M)
    build_gas(M)
    build_cold_supply(M)
    build_hot_out(M)
    build_tmv_dhw(M)
    build_heat_supply(M)
    build_heat_return(M)
    build_condensate(M)
    build_electrical(M)
    build_floor_drain(M)

    setup_cameras()
    setup_lighting()

    glb = os.path.join(out_dir, "boiler_closet.glb")
    bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB')

    n = len([o for o in bpy.data.objects if o.type == 'MESH'])
    print(f"\n{'=' * 60}")
    print(f"MODEL v11 (sharp 90s, all pipes on back wall, exp tank left-centered)")
    print(f"{'=' * 60}")
    print(f"Mesh objects: {n}")
    print(f"Exported: {glb}")
    print(f"Rinnai: {RB/0.0254:.0f}\" AFF, top ~{RT/0.0254:.0f}\", left-biased X={RX0/0.0254:.0f}\"-{RX1/0.0254:.1f}\"")
    print(f"Vents: {VENT_Z/0.0254:.0f}\" AFF UNDER air handler")
    print(f"Gas: from LEFT ceiling near front (Y={GAS_CEIL_Y/0.0254:.0f}\"), under Rinnai")
    print(f"Manifold: Z heights ({Z_HEAT_S/0.0254:.0f}/{Z_HEAT_R/0.0254:.0f}/{Z_MANIFOLD/0.0254:.0f}/{Z_BLEND/0.0254:.0f}/{Z_DHW/0.0254:.0f}\")")
    print(f"Y-depth: P_Y={P_Y/0.0254:.1f}\", Y_RISER={Y_RISER/0.0254:.1f}\", Y_BLEND={Y_BLEND/0.0254:.1f}\"")
    print(f"Risers: X={RISER_R_X/0.0254:.0f}\" (return), X={RISER_S_X/0.0254:.0f}\" (supply)")
    print(f"Electrical: switch + 24V xfmr + 120V outlet (not full panel)")
    print(f"Gas outdoor: Z={OGAS_Z/0.0254:.0f}\" (above electrical)")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
