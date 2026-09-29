"""Modular owl, printable engineering prototype. No hardware operation.

Current shape-function library extracted for the public handoff.
Use rebuild.py to generate unreleased candidates; no standalone entry point.
Source parameters remain editable; STEP imports do not retain this history.
"""
import argparse
import json
import math
from pathlib import Path
import cadquery as cq
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "candidates"
I, B, H, HW = [json.loads((ROOT / f).read_text()) for f in
               ("interfaces_v2.json", "body_v2.json", "head_v2.json", "hardware_parameters.json")]
if B["interface"] != I["revision"] or H["interface"] != I["revision"]:
    raise ValueError("Head/body interface revisions do not match the shared PTZ contract")
OFFSET = I["ptz_base_z"] - I["source_base_y"]
TOP = OFFSET + I["source_top_y"]
TILT = OFFSET + I["source_tilt_axis_y"]
PARTS = []

def box(x,y,z,c):
    return cq.Workplane("XY").box(x,y,z).val().translate(c)

def cyl(r,h,p,d=(0,0,1)):
    return cq.Solid.makeCylinder(r,h,cq.Vector(*p),cq.Vector(*d))

def ellipsoid(r,c):
    return cq.Workplane("XY").sphere(1).val().transformGeometry(cq.Matrix(
        [[r[0],0,0,0],[0,r[1],0,0],[0,0,r[2],0],[0,0,0,1]])).translate(c)

def loft(rings):
    return cq.Solid.makeLoft([cq.Workplane("XY",origin=(0,0,z)).ellipse(x,y).val()
                             for z,x,y in rings],ruled=True)

def hole(s,p,h=10,r=None,d=(0,0,1)):
    if r is None: r=I["m3_clearance_d"]/2
    return s.cut(cyl(r,h,p,d))

def nut(p,h=None,axis="Z",af=None):
    if h is None: h=I["m3_nut_depth"]
    if af is None: af=I["m3_nut_across_flats"]
    n=cq.Workplane("XY").polygon(6,af/math.cos(math.pi/6)).extrude(h).val()
    if axis=="Y": n=n.rotate((0,0,0),(1,0,0),-90)
    return n.translate(p)

def add(name,s,module,color="#d3b994",rotation=None,notes="",kind="print"):
    if kind=="print": s=s.clean()
    if not s.isValid(): raise ValueError(f"Invalid BRep: {name}")
    folder=OUT/module
    folder.mkdir(parents=True,exist_ok=True)
    s.exportBrep(str(folder/f"{name}.brep"))
    cq.exporters.export(s,str(folder/f"{name}.stl"),tolerance=.08,angularTolerance=.12)
    row=dict(name=name,module=module,color=color,kind=kind,notes=notes,
             group="tilt" if module=="head" else "fixed",shape=s)
    if kind=="print":
        if len(s.Solids())!=1: raise ValueError(f"{name}: {len(s.Solids())} solids, expected one")
        q=s
        if rotation: q=q.rotate((0,0,0),rotation[0],rotation[1])
        bb=q.BoundingBox()
        q=q.translate((-bb.xmin,-bb.ymin,-bb.zmin))
        dest=OUT/"print"/module
        dest.mkdir(parents=True,exist_ok=True)
        cq.exporters.export(q,str(dest/f"{name}.stl"),tolerance=.08,angularTolerance=.12)
        mesh=trimesh.load(dest/f"{name}.stl",force="mesh")
        # OCC BRep bounds include tolerances. Translate the tessellation itself
        # exactly onto Z=0 (a rigid print-orientation transform, no mesh repair).
        mesh.apply_translation(-mesh.bounds[0])
        mesh.export(dest/f"{name}.stl")
        row["mesh"]={"watertight":bool(mesh.is_watertight),"winding":bool(mesh.is_winding_consistent),
                     "components":len(mesh.split(only_watertight=False)),
                     "bounds_mm":mesh.extents.round(3).tolist(),"solid_volume_mm3":round(s.Volume(),2),
                     "on_bed":abs(float(mesh.bounds[0,2]))<.001,
                     "bed_fits":bool(np.all(mesh.extents<=np.array(I["printer_bed_mm"])-.1))}
        if not all([row["mesh"]["watertight"],row["mesh"]["winding"],row["mesh"]["components"]==1,row["mesh"]["bed_fits"]]):
            raise ValueError(f"Print validation failed {name}: {row['mesh']}")
    PARTS.append(row)
    print("OK",name,row.get("mesh",{}),flush=True)
    return s

def split_shell(s,name,module,lugs):
    # Three or more accessible M3 seam joints with ordinary captive nuts.
    for x,z in lugs:
        s=s.fuse(cyl(6,14,(x,-7,z),(0,1,0)))
    for side,label in [(-1,"front"),(1,"rear")]:
        half=s.intersect(box(500,250-I["seam_gap"]/2,600,(0,side*(125+I["seam_gap"]/4),250)))
        for x,z in lugs:
            half=hole(half,(x,-30,z),60,d=(0,1,0))
            if side>0: half=half.cut(nut((x,4.4,z),axis="Y"))
            else: half=half.cut(cyl(3.3,23 if module=="head" else 22,(x,-30,z),(0,1,0)))
        add(f"{name}_{label}",half,module,rotation=((1,0,0),-90 if side<0 else 90) if module=="head" else None,
            notes=("Head: seam face on bed; supports inside open half. " if module=="head" else "Body: upright on bottom rim, use brim; supports for bolt lugs only. ")+"M3 seam joints.")

def body():
    print("BUILD BODY",flush=True)
    # Fixed ring carries all rods; removing floor cannot release the chassis.
    ring=cq.Workplane("XY",origin=(0,0,4)).ellipse(100,85).extrude(6).val().cut(cyl(B["bottom_opening_radius"],8,(0,0,3)))
    lid=cq.Workplane("XY").ellipse(100,85).extrude(4).val()
    rb=HW["reservoir"]["diameter_mm"]/2
    lid=lid.fuse(cyl(rb+1.5,4,(0,0,4)))
    lip=cyl(rb+3.5,8,(0,0,4)).cut(cyl(rb+1.5,9,(0,0,4)))
    # Deliberate opening clearance to fixed structural ring.
    if rb+3.5 >= B["bottom_opening_radius"]-.5: raise ValueError("Bottle cradle no longer clears base opening")
    lid=lid.fuse(lip)
    for x in (-73,73):
        for y in (-45,45):
            ring=hole(ring,(x,y,3),8).cut(nut((x,y,7.4)))
            lid=hole(lid,(x,y,-1),6)
    for x,y in B["frame_posts_xy"]:
        ring=hole(ring,(x,y,3),8).cut(nut((x,y,4)))
    for x in (-87,87):
        for y in (-32,32): ring=hole(ring,(x,y,3),8)
    add("structural_base_ring",ring,"body","#638293",notes="Four chassis rods stay attached here when bottom plate is removed.")
    add("removable_bottom_bottle_tray",lid,"body","#3c4449",notes="Four M3 screws; support owl before removal. Disconnect pickup before lowering bottle. Not a certified watertight tray.")

    outer=loft(B["shell_rings_z_rx_ry"])
    inner_rings=[[z,x-B["wall_axis_offset"],y-B["wall_axis_offset"]] for z,x,y in B["shell_rings_z_rx_ry"]]
    inner=loft(inner_rings)
    shell=outer.cut(inner)
    for x in (-87,87):
        for y in (-32,32):
            shell=shell.fuse(cyl(8,8,(x,y,10)))
            shell=hole(shell,(x,y,9),10).cut(nut((x,y,15.4)))
    # Rear ventilation and fixed cable/plumbing exits. No IP rating claimed.
    for x in (-36,-24,-12,0,12,24,36):
        shell=shell.cut(box(5,50,12,(x,83,165)))
    shell=shell.cut(box(26,32,36,(-66,-15,201)))
    shell=shell.cut(box(22,24,36,(66,25,201)))
    split_shell(shell,"body_shell","body",[(-104,75),(104,75),(-85,182),(85,182)])

    # Four threaded M3 rods, not printed, clamp spacers, trays and mechanism deck.
    for level,z,h in [("lower",10,25),("middle",38,102),("upper",144,38)]:
        for idx,(x,y) in enumerate(B["frame_posts_xy"]):
            add(f"frame_spacer_{level}_{idx+1}",hole(cyl(5,h,(x,y,z)),(x,y,z-1),h+2),"body","#638293",notes="Slide over M3 threaded rod; print upright with brim.")
    for side in (-1,1):
        tray=box(34,68,3,(side*73,0,36.5))
        for y in (-38,38): tray=tray.fuse(cyl(6,3,(side*58,y,35))).fuse(box(12,12,3,(side*60,y*.85,36.5)))
        for y in (-38,38): tray=hole(tray,(side*58,y,34),5)
        for y in (-22,22): tray=tray.cut(box(26,3,5,(side*73,y,36.5)))
        add(f"controller_strap_tray_{side}",tray,"body","#638293",notes="Universal strap tray: select board before detailing hole pattern; add insulating spacers.")

    tray=box(132,94,4,(0,0,142))
    # Side corners trimmed to fit the shell; full central roof covers bottle.
    for x,y in B["frame_posts_xy"]: tray=hole(tray,(x,y,139),6)
    pi_xy=[(3.5,3.5),(3.5,52.5),(61.5,3.5),(61.5,52.5)]
    for x,y in pi_xy:
        x+=B["pi_translation"][0]; y+=B["pi_translation"][1]
        tray=tray.fuse(cyl(3.5,B["pi_standoff_height"],(x,y,144)))
        tray=hole(tray,(x,y,139),13,1.4).cut(nut((x,y,140),af=5.2,h=2.2))
    # Downward skirt surrounds bottle below the solid electronics roof.
    tray=tray.fuse(cyl(51.5,6,(0,0,134)).cut(cyl(49,7,(0,0,133))))
    add("pi_tray_wet_bay_roof",tray,"body","#638293",notes="M2.5 Pi mounting pattern 58 x 49 mm; sealed plumbing routing outside roof; not leak-certified.")
    deck=cyl(58,4,(0,0,182))
    for x,y in B["frame_posts_xy"]:
        length=math.hypot(x,y)
        arm=box(length,12,4,(length/2,0,184)).rotate((0,0,0),(0,0,1),math.degrees(math.atan2(y,x)))
        deck=deck.fuse(arm).fuse(cyl(8,4,(x,y,182)))
        deck=hole(deck,(x,y,181),6)
    for x,y in I["base_holes_xy"]: deck=hole(deck,(x,y,181),6)
    deck=deck.fuse(box(24,28,4,(-64,-15,184)))
    for y in (-22,-8): deck=hole(deck,(-66,y,181),6)
    add("ptz_base_adapter",deck,"body","#638293",notes="Official STEP base pattern; M3 bolts + nuts. Verify foot contact and screw length on actual mechanism.")
    guide=box(20,28,4,(-66,-15,188)).fuse(box(4,24,48,(-72,-15,214)))
    guide=guide.fuse(box(18,41,4,(-65,-19.5,236)))
    for y in (-22,-8): guide=hole(guide,(-66,y,185),6)
    for z in (202,228): guide=guide.cut(box(8,4,8,(-72,-15,z)))
    add("camera_ribbon_guide",guide,"body","#638293",rotation=((0,1,0),90),
        notes="Two M3 bolts to deck tab; loose soft straps only, not a sharp ribbon fold. Hand-verify flex loop before powering servos.")

def head():
    print("BUILD HEAD",flush=True)
    zc=TOP+H["centre_above_mount"]; ez=TOP+H["eye_above_mount"]; ex=H["eye_x"]
    outer=ellipsoid(H["radii"],(0,0,zc))
    inner=ellipsoid([r-H["wall_axis_offset"] for r in H["radii"]],(0,0,zc))
    # Collars must reach the curved shell around their ENTIRE circumference.
    # V2 stopped at Y=-75, leaving open crescents on the outer/top edges.
    # Extend to the head midplane; the inner ellipsoid removes surplus inside.
    front=H["front_y"]; rear=H["eye_collar_rear_y"]
    ro=H["eye_collar_outer_radius"]; ri=H["eye_collar_inner_radius"]
    face=H["eye_collar_face_thickness"]
    assert rear >= 0 and ro-ri >= 2.4 and face >= 2.0
    for x in (-ex,ex): outer=outer.fuse(cyl(ro,rear-front,(x,front,ez),(0,1,0)))
    shell=outer.cut(inner).cut(cyl(H["neck_clearance_radius"],134,(0,0,166)))
    # Hollow the eye collars behind a 2.4 mm face instead of printing solid
    # annular blocks. Retain a 3 mm radial rim and the optical/nozzle apertures.
    for x in (-ex,ex): shell=shell.cut(cyl(ri,rear-front-face+1,(x,front+face,ez),(0,1,0)))
    for x,r in [(-ex,H["camera_aperture_radius"]),(ex,H["nozzle_aperture_radius"])]:
        shell=hole(shell,(x,-120,ez),60,r,(0,1,0))
    # Integrated beak: no floating decorative solids.
    beak=cq.Workplane("XZ",origin=(0,-87,TOP+12)).polyline([(-9,6),(9,6),(0,-13)]).close().extrude(25).val()
    shell=shell.fuse(beak)
    # Rear head fastens vertically to carrier at two local interface holes.
    boss=box(32,20,8,(0,99,TOP+12)).intersect(outer)
    shell=shell.fuse(boss)
    for x in (-8,8):
        shell=hole(shell,(x,98,TOP+7),10).cut(nut((x,98,TOP+13.4)))
        # Intentional underside tool ports: a driver otherwise hits the rear
        # shell's lower curve before reaching the vertical carrier screws.
        shell=hole(shell,(x,98,200),TOP+1-200,H["rear_mount_tool_port_radius"])
    split_shell(shell,"head_shell","head",[(-109,zc),(109,zc),(0,zc+89)])

    carrier=make_head_carrier()
    add("head_payload_carrier",carrier,"head","#7297aa",notes="M3 to PTZ; M2 camera bolts/nuts, 5 mm rear standoff; straps retain adjustable gun envelope. Supports required.")


def make_head_carrier(config=None):
    """Pure carrier geometry for independent, versioned fit-test exports."""
    config=config or {}
    ez=TOP+H["eye_above_mount"]; ex=H["eye_x"]
    carrier=box(116,24,4,(0,0,TOP+2))
    for x,y in I["head_holes_xy"]: carrier=hole(carrier,(x,y,TOP-1),6)
    carrier=hole(carrier,(0,0,TOP-1),6,5)
    # Rear support plate reaches the head mounting bosses.
    rear=box(32,104,4,(0,49,TOP+6))
    carrier=carrier.fuse(rear)
    for x in (-8,8): carrier=hole(carrier,(x,98,TOP+3),6)
    # Gun cradle with side clearance, two strap slots and a rear stop.
    g=HW["gun_assembly"]
    floor=ez-g["thickness_mm"]/2-config.get("pump_bottom_padding_allowance_mm",0)
    gun_rear=H["front_y"]-H["gun_front_projection_mm"]+g["length_mm"]
    cradle_front=H["front_y"]+40
    cradle_rear=gun_rear+9
    cradle_y=(cradle_front+cradle_rear)/2
    wall=config.get("side_wall_thickness_mm",2)
    rail_offset=g["width_mm"]/2+config.get("pump_side_clearance_mm",1)+wall/2
    shelf_width=2*rail_offset+wall+2
    shelf=box(shelf_width,cradle_rear-cradle_front,4,(ex,cradle_y,floor-2))
    for x in (ex-rail_offset,ex+rail_offset):
        shelf=shelf.fuse(box(wall,cradle_rear-cradle_front-8,5,(x,cradle_y,floor+2.5)))
        for y in config.get("strap_stations_world_y_mm",[-57,-5]):
            shelf=shelf.cut(box(config.get("strap_slot_width_mm",2.5),config.get("strap_slot_length_mm",5),6,(x,y,floor-2)))
    shelf=shelf.fuse(box(shelf_width,3,5,(ex,gun_rear+config.get("pump_rear_clearance_mm",2)+1.5,floor+2.5)))
    carrier=carrier.fuse(shelf)
    for x in (ex-12,ex+12): carrier=carrier.fuse(cyl(4,floor-4-(TOP+4),(x,0,TOP+4)))
    # Camera bracket uses official 21 x 12.5 mm hole pattern, optical centre
    # 14.4 mm above PCB bottom, not the centre of its bounding rectangle.
    # Raised fork keeps a full-width FFC exit below the camera. A narrow slot
    # in the old solid stem did not account for the width of the ribbon.
    rail=box(30,81,4,(-ex,-28.5,TOP+6))
    rail=rail.fuse(box(30,12,13,(-ex,-69,TOP+10.5)))
    rail=rail.fuse(box(30,27,4,(-ex,-82.5,TOP+15)))
    bracket=box(30,3,31,(-ex,-91.5,TOP+29.5))
    carrier=carrier.fuse(rail).fuse(bracket)
    camera_bottom=ez-14.4
    for x in (-ex-10.5,-ex+10.5):
        for z in (2*ez-(camera_bottom+2),2*ez-(camera_bottom+14.5)):
            carrier=carrier.fuse(cyl(2.3,5,(x,-98,z),(0,1,0)))
            carrier=hole(carrier,(x,-100,z),13,1.15,(0,1,0))
    # Rear ribbon exit slot avoids squeezing the FPC behind the camera.
    carrier=carrier.cut(box(H["camera_ribbon_slot_width"],16,17,(-ex,-93,ez-11.1)))
    # Driver access from above, before installing payloads. The right shelf
    # otherwise partly blocks a straight driver over the PTZ mounting screws.
    for x,y in I["head_holes_xy"]:
        carrier=hole(carrier,(x,y,TOP+4),70,H["ptz_driver_clearance_radius"])
    return carrier
