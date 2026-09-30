"""Compact bolt-together carrier derived from the authoritative Fusion STEP."""
import hashlib
import itertools
import json
from pathlib import Path

import cadquery as cq
import trimesh
import build_v2 as b
from geometry_checks import intersection, pose
from pump_reference import load_reference, CONFIG as SOURCE

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'candidates/carrier_v4'
C=json.loads((ROOT/'carrier_v4.json').read_text())
X=C['gun_x']; A=C['adapter_thickness']; F=C['deck_floor_thickness']


def box(w,l,h,c,r=0):
    p=cq.Workplane('XY').box(w,l,h)
    if r: p=p.edges('|Z').fillet(r)
    return p.val().translate(c)


def bore(s,x,y,z,h):
    return s.cut(b.cyl(b.I['m3_clearance_d']/2,h,(x,y,z)))


def placed(s):
    return s.rotate((0,0,0),(1,0,0),90).translate((X,MID,C['native_y_lift']))


def section_cutter(station,depth):
    sec=cq.Workplane('XY').add(NATIVE.Solids()[0]).section(station).val()
    assert len(sec.Wires())==1, 'Review multi-loop source section'
    wire=sec.Wires()[0].offset2D(C['profile_clearance'])
    assert len(wire)==1
    expanded=wire[0].translate((0,0,-depth/2))
    return placed(cq.Solid.extrudeLinear(expanded,[],cq.Vector(0,0,depth))),sec.BoundingBox()


def adapter():
    # Same tested 42 x 14 mm PTZ pattern and 102 x 53 x 6 mm base footprint.
    s=box(102,53,A,(17,-3.5,A/2),3)
    for x,y in b.I['head_holes_xy']:
        s=bore(s,x,y,-1,A+2).cut(b.cyl(3.3,4,(x,y,A-3.2)))
    for dx,y in itertools.product(C['deck_bolt_x_offsets'],C['deck_bolt_y']):
        s=bore(s,X+dx,y,-1,A+2).cut(b.nut((X+dx,y,-.01),h=b.I['m3_nut_depth']+.01))
    return s.clean()


def saddle(station):
    y=MID-station
    stock=box(40,C['saddle_depth'],C['saddle_top_z']-A,(X,y,(A+C['saddle_top_z'])/2))
    cutter,_=section_cutter(station,C['saddle_depth']+2)
    # Open vertically for drop-in insertion: stock ends below the source seam.
    stock=stock.cut(cutter)
    for dx in C['retainer_bolt_x_offsets']:
        stock=stock.fuse(box(20,14,F,(X+(26 if dx>0 else -26),y,A+F/2),2))
        stock=bore(stock,X+dx,y,A-1,F+2).cut(b.nut((X+dx,y,A-.01),h=b.I['m3_nut_depth']+.01))
    return stock.clean()


def bridge(station):
    y=MID-station
    cutter,bb=section_cutter(station,C['bridge_depth']+2)
    top=bb.ymax+C['native_y_lift']+C['profile_clearance']+C['bridge_roof_thickness']
    bottom=A+F
    s=box(50.4,C['bridge_depth'],top-bottom,(X,y,(top+bottom)/2))
    s=s.cut(cutter)
    relief_top=C['bridge_lower_relief_top_z']
    s=s.cut(box(40.4,C['bridge_depth']+4,relief_top-bottom+2,(X,y,(relief_top+bottom-2)/2)))
    for dx in C['retainer_bolt_x_offsets']:
        sign=1 if dx>0 else -1
        s=s.fuse(box(16,C['bridge_depth'],4,(X+sign*28,y,bottom+2)))
        points=[(X+sign*24,bottom+4),(X+sign*27,bottom+4),(X+sign*24,bottom+7)]
        s=s.fuse(cq.Workplane('XZ',origin=(0,y+C['bridge_depth']/2,0)).polyline(points).close().extrude(C['bridge_depth']).val())
        s=bore(s,X+dx,y,bottom-1,6)
    return s.clean()


def deck():
    lo,hi=C['deck_y_limits']
    s=box(40,hi-lo,F,(X,(lo+hi)/2,A+F/2),2)
    for station in C['saddle_native_z'].values():s=s.fuse(saddle(station))
    for dx,y in itertools.product(C['deck_bolt_x_offsets'],C['deck_bolt_y']):
        s=s.fuse(box(14,12,F,(X+(23 if dx>0 else -23),y,A+F/2),2))
        s=bore(s,X+dx,y,A-1,F+2)
    # Small side stops, NOT a full rear wall. Central 20 mm remains open.
    front=MID-C['native_front_shoulder_z']-C['end_stop_clearance']
    rear=MID+C['end_stop_clearance']
    for sign in (-1,1):
        for y in (front-1.25,rear+1.25):
            s=s.fuse(box(8,2.5,C['saddle_top_z']-A,(X+sign*14,y,(A+C['saddle_top_z'])/2)))
    return s.clean()


NATIVE=load_reference()
MID=C['gun_length_midpoint_y']+NATIVE.BoundingBox().zlen/2


def main():
    for folder in ('print','assembly'):(OUT/folder).mkdir(parents=True,exist_ok=True)
    parts={'ptz_adapter':adapter(),'gun_deck':deck()}
    for name,station in C['saddle_native_z'].items():
        parts[f'{name}_bridge']=bridge(station)
        parts[f'{name}_fit_saddle']=saddle(station)
    main_parts={k:v for k,v in parts.items() if not k.endswith('fit_saddle')}
    checks=[];meshes={};scene=[]
    def check(name,s,t):
        overlap=intersection(s,t)
        checks.append(dict(name=name,overlap_mm3=round(overlap,6),passed=overlap<.05))
        if overlap>=.05: print('COLLISION',name,overlap,flush=True)
    assembly=cq.Assembly(name='CARRIER_V4_USER_STEP_UNPOWERED_PROTOTYPE')
    for name,s in parts.items():
        assert s.isValid() and len(s.Solids())==1, name
        s.exportBrep(str(OUT/'assembly'/f'{name}.brep'))
        cq.exporters.export(s,str(OUT/'assembly'/f'{name}.step'))
        cq.exporters.export(s,str(OUT/'assembly'/f'{name}_assembly.stl'),tolerance=.05,angularTolerance=.12)
        oriented=s.rotate((0,0,0),(1,0,0),90) if name.endswith('bridge') else s
        file=OUT/'print'/f'{name}_print.stl'
        cq.exporters.export(oriented,str(file),tolerance=.05,angularTolerance=.12)
        m=trimesh.load(file,force='mesh');m.apply_translation(-m.bounds[0]);m.export(file)
        assert m.is_watertight and m.is_winding_consistent and len(m.split())==1,name
        meshes[name]=dict(extents_mm=m.extents.tolist(),sha256=hashlib.sha256(file.read_bytes()).hexdigest(),watertight=True)
        if name not in main_parts:continue
        color='#47758C' if name=='ptz_adapter' else '#C89842' if name=='gun_deck' else '#586474'
        assembly.add(s,name=name,color=cq.Color(color));scene.append(dict(name=name,file=f'assembly/{name}_assembly.stl',color=color))
    for (n,s),(k,t) in itertools.combinations(main_parts.items(),2):check(n+'_vs_'+k,s,t)
    gun=placed(NATIVE)
    for n,s in parts.items():
        check(n+'_vs_user_step',s,gun)
        # Verify straight-up insertion/removal through the saddles/stops (bridges removed).
        if not n.endswith('bridge'):
            for dz in (1,4,10,25):check(n+f'_gun_lift_{dz}',s,gun.translate((0,0,dz)))
        else:
            for dz in (1,4,10,25):check(n+f'_bridge_lift_{dz}',s.translate((0,0,dz)),gun)
    # Confirm the end stops really arrest translation, not just clear the gun.
    for dy in (-1.0,1.0):
        overlap=intersection(main_parts['gun_deck'],gun.translate((0,dy,0)))
        checks.append(dict(name=f'end_stop_arrests_y_{dy}',overlap_mm3=round(overlap,6),
                           passed=overlap>.5,expected='intentional overlap after 1 mm axial displacement'))
    for i,s in enumerate(gun.Solids(),1):
        name=f'user_pump_body_{i}'
        cq.exporters.export(s,str(OUT/'assembly'/f'{name}_reference.stl'),tolerance=.05,angularTolerance=.12)
        assembly.add(s,name=name,color=cq.Color('#ED650C'))
        scene.append(dict(name=name,file=f'assembly/{name}_reference.stl',color='#ED650C'))
    mech={n:cq.Shape.importBrep(str(ROOT/'latest/components'/f'ptz_{n}.brep')).translate((0,0,-b.TOP)) for n in ('fixed','pan','tilt')}
    for n,s in mech.items():
        assembly.add(s,name='ptz_'+n,color=cq.Color('#247D6C'))
        cq.exporters.export(s,str(OUT/'assembly'/f'ptz_{n}_reference.stl'),tolerance=.12,angularTolerance=.2)
        scene.append(dict(name='ptz_'+n,file=f'assembly/ptz_{n}_reference.stl',color='#247D6C'))
        for k,t in main_parts.items():check(k+'_vs_ptz_'+n,t,s)
    for dx,y in itertools.product(C['deck_bolt_x_offsets'],C['deck_bolt_y']):
        tool=b.cyl(3.1,45,(X+dx,y,A+F+.05))
        for n,s in main_parts.items():check(f'deck_driver_{dx}_{y}_{n}',s,tool)
    for name,station in C['saddle_native_z'].items():
        for dx in C['retainer_bolt_x_offsets']:
            tool=b.cyl(3.1,45,(X+dx,MID-station,A+F+4+.05))
            for n,s in main_parts.items():check(f'bridge_driver_{name}_{dx}_{n}',s,tool)
    # Rear wire window: conservative straight probe, not a moving harness model.
    wire=box(16,25,16,(X,MID+12.5,24))
    for n,s in main_parts.items():check(n+'_rear_wire_window',s,wire)
    payload=cq.Compound.makeCompound(list(main_parts.values())+[gun]).translate((0,0,b.TOP))
    for pan,tilt in itertools.product((-25,0,25),(-15,0,15)):
        for n in ('fixed','pan'):
            check(f'pose_{pan}_{tilt}_{n}',pose(payload,pan,tilt,'tilt'),pose(mech[n].translate((0,0,b.TOP)),pan,tilt,n))
    assembly.save(str(OUT/'assembly/carrier_v4_review.step'))
    (OUT/'scene.json').write_text(json.dumps(scene,indent=2)+'\n')
    report=dict(revision=C['revision'],source=SOURCE,parameters=C,meshes=meshes,checks=checks,
                all_pass=all(r['passed'] for r in checks),
                source_transform='rotate X +90 degrees, then translate (32,66.05,12.4) mm; no scaling',
                limitations=['Source lacks fillets/chamfers; real contact and pad preload need fit tests.',
                             'Source fittings do not establish complete real hose/wire envelopes.',
                             'No camera/head shell redesign or full body/cable sweep in this release.',
                             'No structural or powered validation; trial fit parts first.'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    assert report['all_pass'],'Review failed collision checks'
    print('PASS',len(checks),'checks',json.dumps(meshes),flush=True)


if __name__=='__main__':main()
