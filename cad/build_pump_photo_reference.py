"""Current rounded pump shape library; use rebuild.py pump for candidates."""
import hashlib
import json
import math
from pathlib import Path

import cadquery as cq
import numpy as np
import trimesh
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

ROOT = Path(__file__).resolve().parent
P = json.loads((ROOT / "pump_photo_parameters.json").read_text())
M, E = P["measured"], P["estimated"]


def box(w, length, thick, centre):
    return cq.Workplane("XY").box(w, length, thick).val().translate(centre)


def rounded(w, length, thick, centre, radius):
    return (cq.Workplane("XY").box(w, length, thick).edges("|Z")
            .fillet(radius).val().translate(centre))


def cyl(radius, length, start, direction=(0, 0, 1)):
    return cq.Solid.makeCylinder(radius, length, cq.Vector(*start), cq.Vector(*direction))


def oval_barrel(width, thickness, start_y, length):
    # XZ plane's normal points towards -Y; negative extrusion goes rearwards.
    return (cq.Workplane("XZ", origin=(0, start_y, 0))
            .ellipse(width/2, thickness/2).extrude(-length).val())


def build_parts():
    length, width, thick = M["overall_length"], M["overall_width"], M["overall_thickness"]
    nose, front_width = E["nozzle_length"], M["front_section_width"]
    shoulder = nose + E["front_section_length"]
    core_w, core_t = E["main_core_width"], E["main_core_thickness"]
    body = oval_barrel(core_w, core_t, shoulder, length-shoulder)
    front = oval_barrel(front_width, E["front_section_thickness"], nose,
                        E["front_section_length"]+2)
    body = body.fuse(front)
    # The photos show flat broad-face lands for bosses/windows on an otherwise
    # curved casing. Keep these instead of flattening the whole cross-section.
    for sign in (-1, 1):
        body = body.fuse(rounded(E["face_land_width"], length-shoulder-6,
                        E["face_land_thickness"],
                        (0, (length+shoulder)/2,
                         sign*(core_t-E["face_land_thickness"])/2), 3))
    # A shallow split-line around the two casing halves; retain a connected core.
    band = box(width+4, length+4, .35, (0, length/2, 0))
    inside = rounded(core_w-.8, length-shoulder-.8, 2,
                     (0, (length+shoulder)/2, 0), E["main_corner_radius"]-.4)
    inside = inside.fuse(rounded(front_width-.8, E["front_section_length"]+2, 2,
                        (0, nose+(E["front_section_length"]+2)/2, 0), 1.6))
    body = body.cut(band.cut(inside))
    # Side latches set the measured maximum 32 mm width.
    for y in (shoulder+10, shoulder+43, length-20):
        for sign in (-1, 1):
            body = body.fuse(box((width-core_w)/2+.5, 9, 12,
                            (sign*(core_w/2+(width-core_w)/4-.25), y, 0)))
    # Broad rear cap lip and raised circular gearbox detail on just one face.
    cap = oval_barrel(width, thick, length-E["rear_cap_length"], E["rear_cap_length"])
    body = body.fuse(cap)
    for radius, y, height in ((E["gear_boss_radius"], E["gear_boss_y"], 1.0),
                             (3.4, E["gear_boss_y"], 1.5),
                             (4.6, E["gear_boss_y"]+14, 1.2),
                             (2.3, E["gear_boss_y"]+24, 1.5)):
        body = body.fuse(cyl(radius, height+.2, (0, y, core_t/2-.2)))
    # Opposite face has recessed screw seats, not the raised circular features.
    for y in (shoulder+5, E["gear_boss_y"]+1, E["gear_boss_y"]+14):
        body = body.cut(cyl(1.7, 1.2, (0, y, -core_t/2), (0, 0, 1)))
    body = body.cut(cyl(1.7, 1.2, (0, shoulder+5, core_t/2), (0, 0, -1)))
    # Opposed motor windows with visible metallic insert. Visual recesses only.
    wy = length-E["window_from_rear"]
    for sign in (-1, 1):
        body = body.cut(box(E["window_width"], E["window_length"], 3,
                            (0, wy, sign*(core_t/2-.5))))
    motor = box(E["window_width"]-.2, E["window_length"]-.2, core_t-2.2, (0, wy, 0))
    # Tapered yellow nozzle: separate fitting, not an organic extension.
    nozzle = cq.Solid.makeCone(1.5, 3.5, nose, cq.Vector(0, 0, 0), cq.Vector(0, 1, 0))
    nozzle = nozzle.cut(cyl(.65, nose, (0, 0, 0), (0, 1, 0)))
    # Explicit side inlet elbow plus a short straight hose stub. Full moving
    # hose route is intentionally not invented here.
    ey = E["elbow_y"]
    ex = -front_width/2-E["elbow_projection_from_front_side"]+E["elbow_outer_radius"]
    elbow = cyl(E["elbow_outer_radius"], -front_width/2-ex,
                (ex, ey, 0), (1, 0, 0))
    elbow = elbow.fuse(rounded(6, 6, 6, (ex, ey, 0), 1.0))
    elbow = elbow.fuse(cyl(E["elbow_outer_radius"], 10, (ex, ey, 0), (0, 1, 0)))
    hose = cyl(E["tube_outer_radius"], E["tube_stub_length"], (ex, ey+10, 0), (0, 1, 0))
    hose = hose.cut(cyl(E["tube_outer_radius"]-.6, E["tube_stub_length"],
                        (ex, ey+10, 0), (0, 1, 0)))
    return [
        ("pump_housing", body.clean(), "#ED650C"),
        ("pump_motor_window", motor, "#787F83"),
        ("pump_nozzle", nozzle, "#DC9C25"),
        ("pump_elbow_estimated", elbow.clean(), "#DC9C25"),
        ("pump_hose_stub_estimated", hose, "#AFCACD"),
    ]
