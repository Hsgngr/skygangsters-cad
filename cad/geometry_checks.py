"""Independent BRep interference, extraction-path, mesh and cable-budget audit."""
import itertools
import json
import math
from functools import lru_cache
from pathlib import Path
import cadquery as cq
import numpy as np
import trimesh
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from build_v2 import ROOT, OUT, I, B, H, HW, TOP, TILT, cyl

@lru_cache(maxsize=2048)
def bounds(s):
    b=Bnd_Box(); BRepBndLib.Add_s(s.wrapped,b)
    return b.Get()

def intersection(a,b):
    ba,bb=bounds(a),bounds(b)
    if any(ba[c+3]<=bb[c]+.001 or bb[c+3]<=ba[c]+.001 for c in range(3)):
        return 0.
    # Reject a detailed purchased assembly using its enclosing solid first.
    # This is conservative and avoids expensive face-pair searches when the
    # complete electronics bounding box is entirely inside a hollow shell.
    if len(b.Solids())>10:
        sizes=[bb[k+3]-bb[k] for k in range(3)]
        enclosing=cq.Workplane("XY").box(*sizes).val().translate(tuple((bb[k]+bb[k+3])/2 for k in range(3)))
        if not a.intersect(enclosing).Solids(): return 0.
    return sum(s.Volume() for s in a.intersect(b).Solids())

def pose(s,yaw,pitch,group):
    if group=="tilt": s=s.rotate((0,0,TILT),(1,0,TILT),pitch)
    if group in ("pan","tilt"): s=s.rotate((0,0,0),(0,0,1),yaw)
    return s

def point(p,yaw,pitch):
    a,b=math.radians(yaw),math.radians(pitch)
    x,y,z=p; z-=TILT
    y,z=y*math.cos(b)-z*math.sin(b),y*math.sin(b)+z*math.cos(b)
    return np.array((x*math.cos(a)-y*math.sin(a),x*math.sin(a)+y*math.cos(a),z+TILT))
