"""
Generate 3D model of boiler closet at 20 Elsie Lane #217.
Rinnai i120CN I-Series Combi Boiler + closed-loop hydronic heating.
v14.1: Routing fixes per Sean's feedback:
  - Cold water entry from LEFT WALL (under light switch), not floor
  - CH expansion tank (red) moved to RIGHT SIDE of unit
  - 90-degree SharkBite elbows at every right-angle pipe turn
  - Fill valve repositioned, no longer clustered with expansion tee
  - Gas outdoor branch lowered below transformer (was intersecting)
  - Manifold tight against back wall, cold supply runs on left wall

Run: blender --background --python generate_boiler_v14_i120cn.py

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
# Rinnai i120CN I-Series Combi Boiler
# 18.5"W x 26.4"H x 10.9"D, 76.1 lb
# CH: 120K BTU, DHW: 199K BTU, 95.5% AFUE
# Left-biased mount, bottom at 24" AFF
# ============================================================
RW = inch(18.5)
RD = inch(10.9)
RH = inch(26.4)
RB = inch(24)          # Bottom at 24" AFF
RT = RB + RH            # Top at ~50.4" AFF
RX0 = inch(4)            # Left edge at 4"
RX1 = RX0 + RW           # ~22.5"
RY1 = CD                  # Flush with back wall
RY0 = CD - RD             # ~21.1"
RCX = (RX0 + RX1) / 2     # ~13.25"
RCY = (RY0 + RY1) / 2     # ~26.55"


# ============================================================
# Port positions -- ESTIMATED for i120CN combi (5 bottom + 1 side)
# Bottom view L->R: COND, CH_RET, DHW_HOT, DHW_COLD, CH_SUP
# ============================================================
P_COND_X   = RX0 + inch(2.5)
P_CHRET_X  = RX0 + inch(5.5)
P_HOT_X    = RX0 + inch(8.5)
P_COLD_X   = RX0 + inch(11.5)
P_CHSUP_X  = RX0 + inch(14.5)

P_Y = RCY
P_Z = RB

# Gas port -- RIGHT SIDE panel
GAS_Z = RB + inch(0.60)
GAS_Y = RY0 + inch(2.83)

# Vent connections -- TOP of unit, 2" nominal twin pipe PVC (native)
V_EXH_X = RX0 + inch(5.91)
V_INT_X = RX0 + inch(12.59)
V_Y     = RCY


# ============================================================
# Pipe radii
# ============================================================
R_VENT = inch(1.0)        # 2" PVC (native)
R_GAS = inch(0.375)       # 3/4" CSST
R_PIPE = inch(0.375)      # 3/4" CPVC (DHW)
R_HEAT = inch(0.5)        # 1" CPVC (CH loop)
R_COND = inch(0.25)       # 1/2" condensate


# ============================================================
# Manifold heights -- DHW and CH are completely separate circuits
# ============================================================
Z_CH_S = inch(12)         # CH supply horizontal
Z_CH_R = inch(14)         # CH return horizontal
Z_COLD = inch(16)         # Cold supply horizontal (DHW)
Z_HOT  = inch(18)         # Hot outlet horizontal (DHW)


# ============================================================
# Vents: 2" PVC twin pipe, UNDER air handler at 62" AFF
# ============================================================
VENT_Z = inch(62)
VENT_Y_EXH = CD - inch(6)
VENT_Y_INT = CD - inch(18)


# ============================================================
# Cold water entry -- LEFT WALL, under light switch
# Existing PEX through wall, ball valve, copper stub.
# SharkBite onto copper, CPVC begins.
# ============================================================
COLD_ENTRY_Y = inch(12)        # Centered with light switch Y
COLD_ENTRY_Z = inch(42)        # Under light switch (46-50")
COLD_DROP_X  = inch(2)         # Vertical drop, 2" from left wall

TAP_Z = inch(30)               # Outdoor tap tee height on vertical drop


# ============================================================
# DHW expansion tank (potable, BLUE) -- RIGHT SIDE
# ============================================================
EXP_DHW_TEE_X  = inch(8)       # Tee on back wall cold horizontal
EXP_DHW_X      = inch(29)      # Tank X position (right of unit)
EXP_DHW_CONN_Z = inch(36)      # Tank bottom connection Z


# ============================================================
# Gas routing
# ============================================================
GAS_CEIL_X  = inch(4)
GAS_CEIL_Y  = inch(10)
GAS_UNDER_Z = inch(23)         # Under Rinnai (24"), above manifold
SHUTOFF_Z   = inch(68)         # Gas shutoff (above transformer 54-60")
OGAS_Z      = inch(52)         # Outdoor gas branch (below transformer)


# ============================================================
# CH circuit routing
# ============================================================
RISER_S_X = CW - inch(2)       # CH supply riser, right wall (~34")
RISER_R_X = inch(2)            # CH return riser, left wall

# CH expansion tank (hydronic, RED) -- RIGHT SIDE, on CH supply line
CH_EXP_X      = inch(26)       # Tank X position
CH_EXP_CONN_Z = inch(24)       # Tank bottom connection Z

# Fill valve on CH return (separated from expansion tank)
FILL_X = inch(6)

# Y-depth offsets
Y_WALL = CD - inch(2)          # Main horizontals against back wall

# AH connections -- FRONT FACE
AH_FRONT_Y = inch(2)
AH_SX = inch(26)               # Supply connection X
AH_RX = inch(10)               # Return connection X
AH_SZ = AH_BTM + inch(4)       # Supply Z (68")
AH_RZ = AH_BTM + inch(2)       # Return Z (66")

# DHW hot shutoff
V2_X = inch(20)

# Floor drain -- RIGHT side
FD_X = CW - inch(8)
FD_Y = inch(8)


# ============================================================
# Bend radii (for smooth flexible routing only)
# ============================================================
BEND_GAS = inch(2)


# ============================================================
# Materials
# ============================================================
PALETTE = {
    "wall_ext":     ((0.75, 0.72, 0.68), 0.85, 0.0),
    "wall_int":     ((0.88, 0.86, 0.83), 0.80, 0.0),
    "floor":        ((0.55, 0.52, 0.48), 0.90, 0.0),
    "ceiling":      ((0.90, 0.88, 0.85), 0.80, 0.0),
    "air_handler":  ((0.72, 0.68, 0.62), 0.55, 0.15),
    "rinnai":       ((0.85, 0.87, 0.90), 0.35, 0.30),
    "rinnai_face":  ((0.20, 0.25, 0.35), 0.40, 0.10),
    "display":      ((0.12, 0.30, 0.70), 0.25, 0.10),
    "cpvc":         ((0.88, 0.82, 0.72), 0.50, 0.0),
    "cpvc_hot":     ((0.85, 0.78, 0.68), 0.50, 0.0),
    "sharkbite":    ((0.78, 0.67, 0.25), 0.22, 0.90),
    "csst":         ((0.82, 0.72, 0.12), 0.28, 0.75),
    "pvc":          ((0.93, 0.92, 0.90), 0.45, 0.0),
    "cast_iron":    ((0.12, 0.11, 0.13), 0.55, 0.65),
    "copper_stub":  ((0.72, 0.45, 0.20), 0.25, 0.95),
    "valve_handle": ((0.15, 0.40, 0.75), 0.60, 0.0),
    "exp_tank":     ((0.15, 0.35, 0.65), 0.45, 0.20),
    "exp_tank_ch":  ((0.65, 0.15, 0.15), 0.45, 0.20),
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


# ============================================================
# Component helpers
# ============================================================
def sharkbite_tee(name, x, y, z, pipe_r, M, main_axis='X', branch_dir='Z'):
    body_r = pipe_r * 1.8
    main_len = pipe_r * 7
    branch_len = pipe_r * 5
    cyl(name, (x, y, z), body_r, main_len, M["sharkbite"], main_axis)
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
    body_r = pipe_r * 2.0
    body_len = pipe_r * 6
    cyl(name, (x, y, z), body_r, body_len, M["sharkbite"], axis)
    cyl(name + "_ball", (x, y, z), body_r * 1.15, body_len * 0.35, M["sharkbite"], axis)
    hl = pipe_r * 5
    hw = pipe_r * 0.8
    ht = pipe_r * 0.35
    if axis in ('X', 'Y'):
        box(name + "_h",
            x - hw, x + hw, y - ht, y + ht,
            z + body_r * 0.7, z + body_r * 0.7 + hl, M["valve_handle"])
    else:
        box(name + "_h",
            x + body_r * 0.7, x + body_r * 0.7 + hl,
            y - ht, y + ht, z - hw, z + hw, M["valve_handle"])


def pipe_with_elbows(base_name, waypoints, pipe_r, pipe_mat, elbow_mat, sharp=True):
    """Pipe run with 90-degree elbow fittings at each right-angle turn.
    Elbows are brass SharkBite push-to-connect (or PVC for condensate).
    Each elbow gets a unique mesh name for the viewer packing list."""
    pipe_run(base_name, waypoints, pipe_r, pipe_mat, sharp=sharp)
    er = pipe_r * 1.7
    el = pipe_r * 3.5
    for i in range(1, len(waypoints) - 1):
        p0 = Vector(waypoints[i - 1])
        p1 = Vector(waypoints[i])
        p2 = Vector(waypoints[i + 1])
        d_in = (p1 - p0).normalized()
        d_out = (p2 - p1).normalized()
        dot = abs(d_in.dot(d_out))
        if dot < 0.15:  # ~90 degree turn (cos 90 = 0)
            cross = d_in.cross(d_out)
            ax, ay, az = abs(cross.x), abs(cross.y), abs(cross.z)
            if ax >= ay and ax >= az:
                axis = 'X'
            elif ay >= az:
                axis = 'Y'
            else:
                axis = 'Z'
            cyl(f"{base_name}_E{i}", tuple(p1), er, el, elbow_mat, axis)


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
# BUILD: Air handler (64-80" AFF)
# ============================================================
def build_air_handler(M):
    box("AirHandler", inch(1), CW - inch(1), inch(2), CD - inch(1),
        AH_BTM, CH - inch(1), M["air_handler"])
    box("SupplyDuct", inch(12), inch(22), inch(8), inch(18),
        CH - inch(1), CH + inch(4), M["duct"])


# ============================================================
# BUILD: Rinnai i120CN Combi Boiler
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

    # Port stubs -- 5 bottom ports + gas side
    stub = inch(3)
    cyl("Port_DHW_Cold", (P_COLD_X, P_Y, RB - stub / 2), R_PIPE * 1.4, stub, M["copper_stub"])
    cyl("Port_DHW_Hot", (P_HOT_X, P_Y, RB - stub / 2), R_PIPE * 1.4, stub, M["copper_stub"])
    cyl("Port_CH_Sup", (P_CHSUP_X, P_Y, RB - stub / 2), R_HEAT * 1.4, stub, M["copper_stub"])
    cyl("Port_CH_Ret", (P_CHRET_X, P_Y, RB - stub / 2), R_HEAT * 1.4, stub, M["copper_stub"])
    cyl("Port_Cond", (P_COND_X, P_Y, RB - stub / 2), R_COND * 2, stub, M["port"])
    cyl("Port_Gas", (RX1 + inch(1), GAS_Y, GAS_Z), R_GAS * 1.4, inch(2), M["port"], 'X')
    cyl("Port_VentExh", (V_EXH_X, V_Y, RT + inch(0.5)), R_VENT, inch(1), M["port"])
    cyl("Port_VentInt", (V_INT_X, V_Y, RT + inch(0.5)), R_VENT, inch(1), M["port"])


# ============================================================
# BUILD: Vents -- 2" PVC twin pipe, native (no adapter needed)
# ============================================================
def build_vents(M):
    pipe_run("VentExh_Run", [
        (V_EXH_X, V_Y, RT + inch(1)),
        (V_EXH_X, V_Y, VENT_Z),
        (V_EXH_X, VENT_Y_EXH, VENT_Z),
        (-EXT_T - inch(1), VENT_Y_EXH, VENT_Z),
    ], R_VENT, M["pvc"], sharp=True)

    cyl("VentExh_Elb1", (V_EXH_X, V_Y, VENT_Z),
        R_VENT * 1.3, R_VENT * 2, M["pvc"])
    cyl("VentExh_Elb2", (V_EXH_X, VENT_Y_EXH, VENT_Z),
        R_VENT * 1.3, R_VENT * 2, M["pvc"], 'X')
    cyl("VentExh_Cap", (-EXT_T - inch(2), VENT_Y_EXH, VENT_Z),
        R_VENT + inch(0.5), inch(2), M["pvc"], 'X')

    pipe_run("VentInt_Run", [
        (V_INT_X, V_Y, RT + inch(1)),
        (V_INT_X, V_Y, VENT_Z),
        (V_INT_X, VENT_Y_INT, VENT_Z),
        (-EXT_T - inch(1), VENT_Y_INT, VENT_Z),
    ], R_VENT, M["pvc"], sharp=True)

    cyl("VentInt_Elb1", (V_INT_X, V_Y, VENT_Z),
        R_VENT * 1.3, R_VENT * 2, M["pvc"])
    cyl("VentInt_Elb2", (V_INT_X, VENT_Y_INT, VENT_Z),
        R_VENT * 1.3, R_VENT * 2, M["pvc"], 'X')
    cyl("VentInt_Cap", (-EXT_T - inch(2), VENT_Y_INT, VENT_Z),
        R_VENT + inch(0.5), inch(2), M["pvc"], 'X')


# ============================================================
# BUILD: Gas -- CSST from LEFT ceiling, routes under Rinnai
# Flexible CSST uses smooth bends, no elbows needed.
# Outdoor branch lowered to Z=52" to clear transformer (54-60").
# ============================================================
def build_gas(M):
    pipe_run("Gas_Line", [
        (GAS_CEIL_X, GAS_CEIL_Y, CH + inch(2)),
        (GAS_CEIL_X, GAS_CEIL_Y, GAS_UNDER_Z),
        (GAS_CEIL_X, Y_WALL, GAS_UNDER_Z),
        (RX1 + inch(2), Y_WALL, GAS_UNDER_Z),
        (RX1 + inch(2), GAS_Y, GAS_UNDER_Z),
        (RX1 + inch(2), GAS_Y, GAS_Z),
    ], R_GAS, M["csst"], BEND_GAS)

    # Shutoff valve on vertical drop (above transformer)
    sharkbite_valve("GasShutoff", GAS_CEIL_X, GAS_CEIL_Y, SHUTOFF_Z, R_GAS, M, 'Z')

    # Outdoor gas branch -- right angle through left wall at Z=52"
    sharkbite_tee("GasTee_Out", GAS_CEIL_X, GAS_CEIL_Y, OGAS_Z, R_GAS, M, 'Z', '-X')
    pipe_run("Gas_Outdoor", [
        (GAS_CEIL_X, GAS_CEIL_Y, OGAS_Z),
        (-EXT_T - inch(1), GAS_CEIL_Y, OGAS_Z),
    ], R_GAS, M["csst"], BEND_GAS)
    sharkbite_valve("GasOutShutoff", inch(1), GAS_CEIL_Y, OGAS_Z, R_GAS, M, 'X')


# ============================================================
# BUILD: DHW Cold Supply (potable, 3/4" CPVC)
# Entry from LEFT WALL under light switch. Existing PEX + ball valve.
# Down left wall, along left wall to back corner, along back wall
# to cold port. Outdoor tap tee on vertical drop. DHW expansion
# tank tee on back wall horizontal.
# ============================================================
def build_dhw_cold(M):
    # Through-wall PEX stub (existing pipe from basement supply)
    pipe_run("DHW_Cold_Entry", [
        (-EXT_T - inch(1), COLD_ENTRY_Y, COLD_ENTRY_Z),
        (COLD_DROP_X + inch(1), COLD_ENTRY_Y, COLD_ENTRY_Z),
    ], R_PIPE * 1.2, M["cpvc"])

    # Existing ball valve at wall entry [REUSE]
    sharkbite_valve("V1_ColdShut", inch(1), COLD_ENTRY_Y, COLD_ENTRY_Z, R_PIPE, M, 'X')

    # 90-degree elbow: horizontal entry turns to vertical drop
    cyl("DHW_Cold_Entry_Elb", (COLD_DROP_X, COLD_ENTRY_Y, COLD_ENTRY_Z),
        R_PIPE * 1.7, R_PIPE * 3.5, M["sharkbite"], 'Y')

    # Main cold supply: vertical drop on left wall, then back wall to port
    # 4 elbows: at Z_COLD turn, left-back corner, port X turn, port Z turn
    pipe_with_elbows("DHW_Cold_Supply", [
        (COLD_DROP_X, COLD_ENTRY_Y, COLD_ENTRY_Z),    # start (after entry elbow)
        (COLD_DROP_X, COLD_ENTRY_Y, Z_COLD),           # bottom of vertical drop
        (COLD_DROP_X, Y_WALL, Z_COLD),                  # along left wall to back corner
        (P_COLD_X, Y_WALL, Z_COLD),                     # along back wall to port X
        (P_COLD_X, P_Y, Z_COLD),                        # jog to port depth
        (P_COLD_X, P_Y, P_Z - inch(1)),                 # up to port
    ], R_PIPE, M["cpvc"], M["sharkbite"])

    # Outdoor tap tee on vertical drop at Z=30"
    sharkbite_tee("ColdTee_Tap", COLD_DROP_X, COLD_ENTRY_Y, TAP_Z, R_PIPE, M, 'Z', '-X')
    pipe_run("Cold_OutdoorTap", [
        (COLD_DROP_X, COLD_ENTRY_Y, TAP_Z),
        (-EXT_T - inch(1), COLD_ENTRY_Y, TAP_Z),
    ], R_PIPE, M["cpvc"], sharp=True)
    sharkbite_valve("TapShutoff", inch(1), COLD_ENTRY_Y, TAP_Z, R_PIPE, M, 'X')

    # DHW expansion tank (potable, BLUE) -- tee on back wall horizontal
    sharkbite_tee("ExpTee_DHW", EXP_DHW_TEE_X, Y_WALL, Z_COLD, R_PIPE, M, 'X', 'Z')
    # Branch: along back wall right, then up to tank. 1 elbow at turn.
    pipe_with_elbows("Exp_DHW_Run", [
        (EXP_DHW_TEE_X, Y_WALL, Z_COLD),               # from tee
        (EXP_DHW_X, Y_WALL, Z_COLD),                    # along back wall right
        (EXP_DHW_X, Y_WALL, EXP_DHW_CONN_Z),            # up to tank
    ], R_PIPE, M["cpvc"], M["sharkbite"])

    # Tank: Watts PLT-5, 2.1 gal, potable-rated, blue
    cyl("ExpTank_DHW", (EXP_DHW_X, Y_WALL, EXP_DHW_CONN_Z + inch(5.5)),
        inch(3.5), inch(10), M["exp_tank"])
    cyl("ExpTank_DHW_Cap", (EXP_DHW_X, Y_WALL, EXP_DHW_CONN_Z + inch(0.5)),
        inch(3.2), inch(1.5), M["exp_tank"])


# ============================================================
# BUILD: DHW Hot Outlet (potable, 3/4" CPVC)
# Unit hot outlet -> shutoff -> fixtures (exits right wall).
# No TMV needed: servo-based temp control built into i120CN.
# ============================================================
def build_dhw_hot(M):
    # 2 elbows: at Z_HOT turn, at back wall turn
    pipe_with_elbows("DHW_Hot_Out", [
        (P_HOT_X, P_Y, P_Z - inch(1)),                  # from port
        (P_HOT_X, P_Y, Z_HOT),                           # drop to manifold
        (P_HOT_X, Y_WALL, Z_HOT),                        # to back wall
        (CW + WALL_T + inch(1), Y_WALL, Z_HOT),          # exit right wall
    ], R_PIPE, M["cpvc_hot"], M["sharkbite"])

    sharkbite_valve("V2_HotShut", V2_X, Y_WALL, Z_HOT, R_PIPE, M)


# ============================================================
# BUILD: CH Supply (closed loop, 1" CPVC)
# Unit CH supply port -> back wall -> right wall riser -> up to AH.
# CH expansion tank (hydronic, RED) branches off back wall horizontal.
# ============================================================
def build_ch_supply(M):
    # 5 elbows on main run
    pipe_with_elbows("CH_Supply", [
        (P_CHSUP_X, P_Y, P_Z - inch(1)),                # from port
        (P_CHSUP_X, P_Y, Z_CH_S),                        # drop to manifold
        (P_CHSUP_X, Y_WALL, Z_CH_S),                     # to back wall
        (RISER_S_X, Y_WALL, Z_CH_S),                      # along back wall right
        (RISER_S_X, Y_WALL, AH_SZ),                       # up right wall riser
        (RISER_S_X, AH_FRONT_Y, AH_SZ),                   # forward to AH front
        (AH_SX, AH_FRONT_Y, AH_SZ),                       # to AH supply stub
    ], R_HEAT, M["cpvc_hot"], M["sharkbite"])

    # CH expansion tank (hydronic, RED) -- tee on back wall at X=26"
    # Branch goes straight up from tee to tank. No additional elbows.
    sharkbite_tee("ExpTee_CH", CH_EXP_X, Y_WALL, Z_CH_S, R_HEAT, M, 'X', 'Z')
    pipe_run("Exp_CH_Run", [
        (CH_EXP_X, Y_WALL, Z_CH_S),                      # from tee
        (CH_EXP_X, Y_WALL, CH_EXP_CONN_Z),                # straight up to tank
    ], R_HEAT, M["cpvc"], sharp=True)

    # Tank: Watts ETX-15, 2.1 gal, hydronic-rated, red
    cyl("ExpTank_CH", (CH_EXP_X, Y_WALL, CH_EXP_CONN_Z + inch(5.5)),
        inch(3.5), inch(10), M["exp_tank_ch"])
    cyl("ExpTank_CH_Cap", (CH_EXP_X, Y_WALL, CH_EXP_CONN_Z + inch(0.5)),
        inch(3.2), inch(1.5), M["exp_tank_ch"])


# ============================================================
# BUILD: CH Return (closed loop, 1" CPVC)
# AH return -> left wall riser down -> back wall -> unit CH return.
# Fill valve on back wall horizontal (separated from expansion tank).
# ============================================================
def build_ch_return(M):
    # 5 elbows on main run
    pipe_with_elbows("CH_Return", [
        (AH_RX, AH_FRONT_Y, AH_RZ),                      # from AH return stub
        (RISER_R_X, AH_FRONT_Y, AH_RZ),                   # along AH front to left
        (RISER_R_X, Y_WALL, AH_RZ),                        # back to wall
        (RISER_R_X, Y_WALL, Z_CH_R),                        # down left wall
        (P_CHRET_X, Y_WALL, Z_CH_R),                        # along back wall to port
        (P_CHRET_X, P_Y, Z_CH_R),                           # to port depth
        (P_CHRET_X, P_Y, P_Z - inch(1)),                    # up to port
    ], R_HEAT, M["cpvc"], M["sharkbite"])

    # Fill/purge valve on CH return back wall horizontal
    # Opens to charge closed loop from potable supply. Close after filling.
    sharkbite_valve("FillValve", FILL_X, Y_WALL, Z_CH_R, R_HEAT, M, 'X')


# ============================================================
# BUILD: Condensate drain (PVC)
# ============================================================
def build_condensate(M):
    NEUT_Z = inch(8)
    NEUT_X = P_COND_X

    # Drop from port to neutralizer -- 1 PVC elbow at turn
    pipe_with_elbows("Cond_Drop", [
        (P_COND_X, P_Y, P_Z - inch(1)),
        (P_COND_X, P_Y, NEUT_Z + inch(4)),
        (P_COND_X, Y_WALL, NEUT_Z + inch(4)),
    ], R_COND, M["pvc"], M["pvc"])

    box("Neutralizer", NEUT_X - inch(2), NEUT_X + inch(2),
        Y_WALL - inch(1.5), Y_WALL + inch(1), NEUT_Z, NEUT_Z + inch(4), M["pvc"])

    # From neutralizer to floor drain -- 2 PVC elbows
    pipe_with_elbows("Cond_ToDrain", [
        (NEUT_X, Y_WALL, NEUT_Z),
        (NEUT_X, Y_WALL, inch(0.5)),
        (FD_X, Y_WALL, inch(0.5)),
        (FD_X, FD_Y, inch(0.5)),
    ], R_COND, M["drain"], M["pvc"])

    box("DrainChannel", NEUT_X - inch(1), FD_X + inch(1),
        Y_WALL - inch(1), Y_WALL + inch(0.5), -inch(0.3), inch(0.3), M["drain"])


# ============================================================
# BUILD: Electrical
# ============================================================
def build_electrical(M):
    box("ElecSwitch", -inch(0.3), inch(0.3), inch(10), inch(14),
        inch(46), inch(50), M["panel"])
    box("ElecXfmr", -inch(0.3), inch(2.5), inch(10), inch(14),
        inch(54), inch(60), M["panel"])
    box("ElecOutlet", -inch(0.3), inch(0.3), inch(18), inch(22),
        inch(46), inch(50), M["panel"])


# ============================================================
# BUILD: Floor drain
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
    build_dhw_cold(M)
    build_dhw_hot(M)
    build_ch_supply(M)
    build_ch_return(M)
    build_condensate(M)
    build_electrical(M)
    build_floor_drain(M)

    setup_cameras()
    setup_lighting()

    glb = os.path.join(out_dir, "boiler_closet_v14_i120cn.glb")
    bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB')

    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    n = len(meshes)
    n_elbows = len([o for o in meshes if '_E' in o.name and any(c.isdigit() for c in o.name.split('_E')[-1])])
    n_elbows += len([o for o in meshes if 'Entry_Elb' in o.name])  # manual entry elbow
    n_vent_elb = len([o for o in meshes if 'Vent' in o.name and 'Elb' in o.name])

    print(f"\n{'=' * 60}")
    print(f"MODEL v14.1 (i120CN COMBI, routing fixes)")
    print(f"{'=' * 60}")
    print(f"Mesh objects: {n}")
    print(f"Exported: {glb}")
    print(f"Unit: Rinnai i120CN, 18.5\"W x 26.4\"H x 10.9\"D")
    print(f"  CH: 120K BTU, DHW: 199K BTU, 95.5% AFUE")
    print(f"  Bottom at {RB/0.0254:.0f}\" AFF, top at ~{RT/0.0254:.0f}\"")
    print(f"  X range: {RX0/0.0254:.0f}\"-{RX1/0.0254:.1f}\"")
    print(f"Cold entry: LEFT WALL at Y={COLD_ENTRY_Y/0.0254:.0f}\", Z={COLD_ENTRY_Z/0.0254:.0f}\"")
    print(f"Manifold Z: CH_S={Z_CH_S/0.0254:.0f} CH_R={Z_CH_R/0.0254:.0f} "
          f"COLD={Z_COLD/0.0254:.0f} HOT={Z_HOT/0.0254:.0f}")
    print(f"Expansion tanks: DHW(blue) X={EXP_DHW_X/0.0254:.0f}\", "
          f"CH(red) X={CH_EXP_X/0.0254:.0f}\" -- both RIGHT of unit")
    print(f"90-degree elbows: {n_elbows} pipe + {n_vent_elb} vent = {n_elbows + n_vent_elb} total")
    print(f"Gas outdoor branch: Z={OGAS_Z/0.0254:.0f}\" (below transformer 54-60\")")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
