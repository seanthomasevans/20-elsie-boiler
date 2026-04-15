"""
Generate 3D model of boiler closet at 20 Elsie Lane #217.
Rinnai i120CN I-Series Combi Boiler + closed-loop hydronic heating.
v14: COMBI BOILER replaces RXP199iN tankless per HVAC tech (Dubay) recommendation.
     Integrated pump, proportional valve, flat plate HX, servo DHW control.
     No external TMV, zone valve, or circulation pump needed.
     Closed CH loop (treated water) separate from DHW (potable).
     5 bottom ports: Condensate, CH Return, DHW Hot, DHW Cold, CH Supply.
     Gas on right side. 2" twin pipe PVC venting (native, no adapter).

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
# Rinnai i120CN I-Series Combi Boiler
# 18.5"W x 26.4"H x 10.9"D, 76.1 lb
# CH: 120K BTU, DHW: 199K BTU, 95.5% AFUE
# Left-biased mount, bottom at 24" AFF
# ============================================================
RW = inch(18.5)
RD = inch(10.9)
RH = inch(26.4)
RB = inch(24)          # Bottom at 24" AFF
RT = RB + RH            # Top at ~50.4" AFF (13.6" below AH)

RX0 = inch(4)            # Left edge at 4" (near gas entry)
RX1 = RX0 + RW           # ~22.5"
RY1 = CD                  # Flush with back wall
RY0 = CD - RD             # ~21.1"
RCX = (RX0 + RX1) / 2     # ~13.25"
RCY = (RY0 + RY1) / 2     # ~26.55"


# ============================================================
# Port positions — ESTIMATED for i120CN combi (5 bottom + 1 side)
# Bottom view L→R: COND, CH_RET, DHW_HOT, DHW_COLD, CH_SUP
# Exact positions TBD from installation manual. Estimates based on
# 18.5" width, internal component layout from brochure cutaway.
# Gas port on RIGHT SIDE panel (same as RXP199iN).
# ============================================================
P_COND_X   = RX0 + inch(2.5)      # Condensate drain, far left
P_CHRET_X  = RX0 + inch(5.5)      # CH Return (1" NPT), left-center
P_HOT_X    = RX0 + inch(8.5)      # DHW Hot Outlet (3/4" NPT), center-left
P_COLD_X   = RX0 + inch(11.5)     # DHW Cold Inlet (3/4" NPT), center-right
P_CHSUP_X  = RX0 + inch(14.5)     # CH Supply (1" NPT), right-center

# All bottom ports share approximate depth (center of unit)
P_Y = RCY                          # ~26.5" from front
P_Z = RB                           # Ports exit bottom at 24" AFF

# Gas port — RIGHT SIDE panel, low and near front
GAS_X = RX1                        # Flush with right side panel
GAS_Z = RB + inch(0.60)            # 0.60" above bottom edge
GAS_Y = RY0 + inch(2.83)           # 2.83" from front face

# Vent connections — TOP of unit, 2" nominal twin pipe PVC (native, no adapter)
V_EXH_X = RX0 + inch(5.91)        # Exhaust on left side of top
V_INT_X = RX0 + inch(12.59)       # Intake on right side of top
V_Y     = RCY                      # Centered depth


# ============================================================
# Pipe radii
# ============================================================
R_VENT = inch(1.0)        # 2" PVC (native, no 3" adapter needed)
R_GAS = inch(0.375)       # 3/4" CSST
R_PIPE = inch(0.375)      # 3/4" CPVC (DHW)
R_HEAT = inch(0.5)        # 1" CPVC (CH loop)
R_COND = inch(0.25)       # 1/2" condensate
R_SMALL = inch(0.3)


# ============================================================
# Manifold heights — much simpler with combi (no cross-connections)
# DHW and CH are completely separate circuits.
# ============================================================
Z_CH_S = inch(12)         # CH supply horizontal
Z_CH_R = inch(14)         # CH return horizontal
Z_COLD = inch(16)         # Cold supply horizontal (DHW)
Z_HOT  = inch(18)         # Hot outlet horizontal (DHW)
Z_FILL = inch(10)         # Fill valve height (CH loop)


# ============================================================
# Vents: 2" PVC twin pipe, UNDER air handler at 62" AFF
# Smaller pipes than RXP199iN (was 3"), more clearance in closet
# ============================================================
VENT_Z = inch(62)
VENT_Y_EXH = CD - inch(6)         # Back vent (exhaust)
VENT_Y_INT = CD - inch(18)        # Front vent (intake), 12" forward


# ============================================================
# Gas routing — enters from LEFT ceiling, routes under Rinnai
# ============================================================
GAS_CEIL_X = inch(4)
GAS_CEIL_Y = inch(10)
GAS_UNDER_Z = inch(23)            # Under Rinnai (24"), above manifold (Z_HOT=18")
SHUTOFF_Z = inch(56)


# ============================================================
# Component positions — SIMPLER: no TMV, no blend line, no zone valve
# DHW circuit: cold from floor -> unit cold inlet; unit hot outlet -> fixtures
# CH circuit: unit CH supply -> riser -> AH; AH -> riser -> unit CH return
# ============================================================
COLD_X = inch(3)           # Cold entry from floor (left of unit)
V1_X = inch(5)             # Cold shutoff valve
V2_X = inch(14)            # Hot shutoff valve
V3_X = inch(10)            # CH supply shutoff (optional)

# Risers: on walls, outside unit X range (4-22.5")
RISER_S_X = CW - inch(2)  # CH supply riser on RIGHT WALL (~34")
RISER_R_X = inch(2)        # CH return riser on LEFT WALL

# Y-depth offsets
Y_WALL = CD - inch(2)      # Main horizontals against back wall
Y_BLEND = CD - inch(4)     # Secondary runs slightly off wall

# AH connections — FRONT FACE
AH_FRONT_Y = inch(2)
AH_SX = inch(26)           # Supply connection X
AH_RX = inch(10)           # Return connection X
AH_SZ = AH_BTM + inch(4)   # Supply Z (68")
AH_RZ = AH_BTM + inch(2)   # Return Z (66")

# Floor drain — RIGHT side
FD_X = CW - inch(8)
FD_Y = inch(8)

# Outdoor branches through left wall
TAP_Z = inch(16)
TAP_Y = inch(10)
OGAS_Z = inch(60)
OGAS_Y = inch(14)


# ============================================================
# Bend radii per pipe size
# ============================================================
BEND_VENT = inch(3)        # Smaller for 2" pipe
BEND_MAIN = inch(2)
BEND_HEAT = inch(2.5)
BEND_GAS = inch(2)
BEND_COND = inch(1.5)
BEND_SMALL = inch(1.5)


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

    # Port stubs — 5 bottom ports + gas side
    stub = inch(3)
    # DHW ports (3/4" NPT)
    cyl("Port_DHW_Cold", (P_COLD_X, P_Y, RB - stub / 2), R_PIPE * 1.4, stub, M["copper_stub"])
    cyl("Port_DHW_Hot", (P_HOT_X, P_Y, RB - stub / 2), R_PIPE * 1.4, stub, M["copper_stub"])
    # CH ports (1" NPT, larger)
    cyl("Port_CH_Sup", (P_CHSUP_X, P_Y, RB - stub / 2), R_HEAT * 1.4, stub, M["copper_stub"])
    cyl("Port_CH_Ret", (P_CHRET_X, P_Y, RB - stub / 2), R_HEAT * 1.4, stub, M["copper_stub"])
    # Condensate (1/2" NPT)
    cyl("Port_Cond", (P_COND_X, P_Y, RB - stub / 2), R_COND * 2, stub, M["port"])
    # Gas (3/4" NPT, right side)
    cyl("Port_Gas", (RX1 + inch(1), GAS_Y, GAS_Z), R_GAS * 1.4, inch(2), M["port"], 'X')
    # Vent stubs (2" nominal, native)
    cyl("Port_VentExh", (V_EXH_X, V_Y, RT + inch(0.5)), R_VENT, inch(1), M["port"])
    cyl("Port_VentInt", (V_INT_X, V_Y, RT + inch(0.5)), R_VENT, inch(1), M["port"])


# ============================================================
# BUILD: Vents — 2" PVC twin pipe, native (no adapter needed)
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
# BUILD: Gas — CSST from LEFT ceiling, routes under Rinnai
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

    sharkbite_valve("GasShutoff", GAS_CEIL_X, GAS_CEIL_Y, SHUTOFF_Z, R_GAS, M, 'Z')

    sharkbite_tee("GasTee_Out", GAS_CEIL_X, GAS_CEIL_Y, OGAS_Z, R_GAS, M, 'Z', '-X')
    pipe_run("Gas_Outdoor", [
        (GAS_CEIL_X, GAS_CEIL_Y, OGAS_Z),
        (-EXT_T - inch(1), GAS_CEIL_Y, OGAS_Z),
    ], R_GAS, M["csst"], BEND_GAS)
    sharkbite_valve("GasOutShutoff", inch(1), GAS_CEIL_Y, OGAS_Z, R_GAS, M, 'X')


# ============================================================
# BUILD: DHW Cold Supply (potable, 3/4" CPVC)
# Simple: floor riser -> shutoff -> unit cold inlet
# ============================================================
def build_dhw_cold(M):
    pipe_run("DHW_Cold_Supply", [
        (COLD_X, Y_WALL, -inch(2)),
        (COLD_X, Y_WALL, Z_COLD),
        (P_COLD_X, Y_WALL, Z_COLD),
        (P_COLD_X, P_Y, Z_COLD),
        (P_COLD_X, P_Y, P_Z - inch(1)),
    ], R_PIPE, M["cpvc"], sharp=True)

    sharkbite_valve("V1_ColdShut", V1_X, Y_WALL, Z_COLD, R_PIPE, M)

    # Potable expansion tank on cold supply (Watts PLT-5, right side)
    EXP_X = inch(29)
    EXP_HORIZ_Z = inch(8)
    sharkbite_tee("ExpTee_DHW", COLD_X, Y_WALL, EXP_HORIZ_Z, R_PIPE, M, 'Z', '-Y')
    pipe_run("Exp_DHW_Run", [
        (COLD_X, Y_WALL, EXP_HORIZ_Z),
        (COLD_X, Y_BLEND, EXP_HORIZ_Z),
        (EXP_X, Y_BLEND, EXP_HORIZ_Z),
        (EXP_X, Y_BLEND, RB + inch(16)),
        (EXP_X, Y_WALL, RB + inch(16)),
    ], R_PIPE, M["cpvc"], sharp=True)
    cyl("ExpTank_DHW", (EXP_X, Y_WALL, RB + inch(16) + inch(5)),
        inch(3), inch(9), M["exp_tank"])
    cyl("ExpTank_DHW_Cap", (EXP_X, Y_WALL, RB + inch(16) + inch(0.5)),
        inch(2.8), inch(1.5), M["exp_tank"])

    # Outdoor tap branch
    sharkbite_tee("ColdTee_Tap", COLD_X, Y_WALL, TAP_Z, R_PIPE, M, 'Z', '-Y')
    pipe_run("Cold_OutdoorTap", [
        (COLD_X, Y_WALL, TAP_Z),
        (COLD_X, TAP_Y, TAP_Z),
        (-EXT_T - inch(1), TAP_Y, TAP_Z),
    ], R_PIPE, M["cpvc"], sharp=True)
    sharkbite_valve("TapShutoff", inch(2), TAP_Y, TAP_Z, R_PIPE, M, 'X')


# ============================================================
# BUILD: DHW Hot Outlet (potable, 3/4" CPVC)
# Simple: unit hot outlet -> shutoff -> fixtures (exits right wall)
# No TMV needed: servo-based temp control built into i120CN.
# ============================================================
def build_dhw_hot(M):
    dhw_out_z = Z_HOT + inch(1.5)
    pipe_run("DHW_Hot_Out", [
        (P_HOT_X, P_Y, P_Z - inch(1)),
        (P_HOT_X, P_Y, Z_HOT),
        (P_HOT_X, Y_WALL, Z_HOT),
        (CW + WALL_T + inch(1), Y_WALL, Z_HOT),
    ], R_PIPE, M["cpvc_hot"], sharp=True)

    sharkbite_valve("V2_HotShut", V2_X, Y_WALL, Z_HOT, R_PIPE, M)


# ============================================================
# BUILD: CH Supply (closed loop, 1" CPVC)
# Unit CH supply -> riser on right wall -> up to AH
# ============================================================
def build_ch_supply(M):
    pipe_run("CH_Supply", [
        (P_CHSUP_X, P_Y, P_Z - inch(1)),
        (P_CHSUP_X, P_Y, Z_CH_S),
        (P_CHSUP_X, Y_WALL, Z_CH_S),
        (RISER_S_X, Y_WALL, Z_CH_S),
        (RISER_S_X, Y_WALL, AH_SZ),
        (RISER_S_X, AH_FRONT_Y, AH_SZ),
        (AH_SX, AH_FRONT_Y, AH_SZ),
    ], R_HEAT, M["cpvc_hot"], sharp=True)


# ============================================================
# BUILD: CH Return (closed loop, 1" CPVC)
# AH return -> riser on left wall -> back to unit CH return
# ============================================================
def build_ch_return(M):
    pipe_run("CH_Return", [
        (AH_RX, AH_FRONT_Y, AH_RZ),
        (RISER_R_X, AH_FRONT_Y, AH_RZ),
        (RISER_R_X, Y_WALL, AH_RZ),
        (RISER_R_X, Y_WALL, Z_CH_R),
        (P_CHRET_X, Y_WALL, Z_CH_R),
        (P_CHRET_X, P_Y, Z_CH_R),
        (P_CHRET_X, P_Y, P_Z - inch(1)),
    ], R_HEAT, M["cpvc"], sharp=True)

    # CH expansion tank (hydronic, NOT potable) on return line
    # Watts ETX-15 or similar, on left wall
    CH_EXP_X = inch(2)
    CH_EXP_Z = inch(36)
    sharkbite_tee("ExpTee_CH", RISER_R_X, Y_WALL, Z_CH_R, R_HEAT, M, 'X', '-X')
    pipe_run("Exp_CH_Run", [
        (RISER_R_X, Y_WALL, Z_CH_R),
        (CH_EXP_X, Y_WALL, Z_CH_R),
        (CH_EXP_X, Y_WALL, CH_EXP_Z),
    ], R_HEAT, M["cpvc"], sharp=True)
    cyl("ExpTank_CH", (CH_EXP_X, Y_WALL, CH_EXP_Z + inch(5)),
        inch(3), inch(9), M["exp_tank_ch"])
    cyl("ExpTank_CH_Cap", (CH_EXP_X, Y_WALL, CH_EXP_Z + inch(0.5)),
        inch(2.8), inch(1.5), M["exp_tank_ch"])

    # Fill/purge valve on CH return (to fill closed loop)
    FILL_X = inch(5)
    sharkbite_valve("FillValve", FILL_X, Y_WALL, Z_CH_R, R_HEAT, M, 'X')


# ============================================================
# BUILD: Condensate drain (PVC)
# ============================================================
def build_condensate(M):
    NEUT_Z = inch(8)
    NEUT_X = P_COND_X

    pipe_run("Cond_Drop", [
        (P_COND_X, P_Y, P_Z - inch(1)),
        (P_COND_X, P_Y, NEUT_Z + inch(4)),
        (P_COND_X, Y_WALL, NEUT_Z + inch(4)),
    ], R_COND, M["pvc"], sharp=True)

    box("Neutralizer", NEUT_X - inch(2), NEUT_X + inch(2),
        Y_WALL - inch(1.5), Y_WALL + inch(1), NEUT_Z, NEUT_Z + inch(4), M["pvc"])

    pipe_run("Cond_ToDrain", [
        (NEUT_X, Y_WALL, NEUT_Z),
        (NEUT_X, Y_WALL, inch(0.5)),
        (FD_X, Y_WALL, inch(0.5)),
        (FD_X, FD_Y, inch(0.5)),
    ], R_COND, M["drain"], sharp=True)

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

    glb = os.path.join(out_dir, "boiler_closet.glb")
    bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB')

    n = len([o for o in bpy.data.objects if o.type == 'MESH'])
    print(f"\n{'=' * 60}")
    print(f"MODEL v14 (i120CN COMBI BOILER, closed loop CH)")
    print(f"{'=' * 60}")
    print(f"Mesh objects: {n}")
    print(f"Exported: {glb}")
    print(f"Unit: Rinnai i120CN, 18.5\"W x 26.4\"H x 10.9\"D")
    print(f"  CH: 120K BTU, DHW: 199K BTU, 95.5% AFUE")
    print(f"  Bottom at {RB/0.0254:.0f}\" AFF, top at ~{RT/0.0254:.0f}\"")
    print(f"  X range: {RX0/0.0254:.0f}\"-{RX1/0.0254:.1f}\"")
    print(f"Ports (L->R): COND={P_COND_X/0.0254:.1f} CH_RET={P_CHRET_X/0.0254:.1f} "
          f"DHW_HOT={P_HOT_X/0.0254:.1f} DHW_COLD={P_COLD_X/0.0254:.1f} "
          f"CH_SUP={P_CHSUP_X/0.0254:.1f}\"")
    print(f"Gas: Z={GAS_Z/0.0254:.1f}\", Y={GAS_Y/0.0254:.1f}\"")
    print(f"Manifold Z: CH_S={Z_CH_S/0.0254:.0f} CH_R={Z_CH_R/0.0254:.0f} "
          f"COLD={Z_COLD/0.0254:.0f} HOT={Z_HOT/0.0254:.0f}")
    print(f"Vents: 2\" PVC twin pipe at {VENT_Z/0.0254:.0f}\" AFF")
    print(f"INTEGRATED: pump, proportional valve, flat plate HX, servo DHW")
    print(f"ELIMINATED: TMV, zone valve, external pump, MCC-91-2, check valve")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
