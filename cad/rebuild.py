"""Rebuild unreleased candidates or verify the published carrier; no hardware I/O."""
import argparse
import hashlib
import json
from pathlib import Path
import cadquery as cq
import numpy as np
import trimesh
import build_v2 as b
import build_pump_photo_reference as p
from geometry_checks import intersection, pose

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent
OUT=ROOT/'candidates'
CONFIG=json.loads((ROOT/'carrier_v2_2.json').read_text())

def saved(name):
    return cq.Shape.importBrep(str(ROOT/'latest/components'/f'{name}.brep'))

def check():
    new=b.make_head_carrier(CONFIG).clean()
    old=saved('head_payload_carrier')
    assert new.isValid() and len(new.Solids())==1
    difference=new.cut(old).Volume()+old.cut(new).Volume()
    assert difference<.05, f'Carrier changed: {difference} mm3; candidate not released'
    release=REPO/'print/carrier/head_payload_carrier_v2_2.stl'
    report=json.loads((REPO/'validation/carrier_validation.json').read_text())
    assert hashlib.sha256(release.read_bytes()).hexdigest()==report['stl_sha256']
    mesh=trimesh.load(release,force='mesh')
    assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1
    assert np.allclose(mesh.extents,[121,199,45],atol=.02)
    rows=json.loads((ROOT/'latest/manifest.json').read_text())
    pump=[r['name'] for r in rows if r['name'].startswith('pump_') and r['name']!='pump_interface']
    for name in ['head_shell_front','head_shell_rear','camera_module3','ptz_tilt']+pump:
        overlap=intersection(new,saved(name))
        assert overlap<.05,(name,overlap)
    moving=cq.Compound.makeCompound([new]+[saved(n) for n in pump])
    targets=[r for r in rows if r['group'] in ('fixed','pan')]
    for pan in (-25,0,25):
        for tilt in (-15,0,15):
            transformed=pose(moving,pan,tilt,'tilt')
            for row in targets:
                overlap=intersection(transformed,pose(saved(row['name']),pan,tilt,row['group']))
                assert overlap<.05,(pan,tilt,row['name'],overlap)
    print('PASS: carrier geometry unchanged, released STL hash/mesh, neutral clearances, nine sampled poses')
    print('This is not full assembly, physical fit, cable-sweep or powered-motion approval.')

def carrier():
    OUT.mkdir(exist_ok=True)
    shape=b.make_head_carrier(CONFIG).clean()
    assert shape.isValid() and len(shape.Solids())==1
    local=shape.translate((0,0,-b.TOP))
    cq.exporters.export(local,str(OUT/'carrier_candidate.step'))
    cq.exporters.export(local,str(OUT/'carrier_candidate.stl'),tolerance=.08,angularTolerance=.12)
    mesh=trimesh.load(OUT/'carrier_candidate.stl',force='mesh')
    mesh.apply_translation(-mesh.bounds[0]);mesh.export(OUT/'carrier_candidate.stl')
    assert mesh.is_watertight and mesh.is_winding_consistent
    print('Unreleased carrier candidate: recheck, re-slice and physically fit before approval')

def pump():
    OUT.mkdir(exist_ok=True)
    asm=cq.Assembly(name='PUMP_REFERENCE_CANDIDATE_NOT_PRINT_PART')
    for name,shape,color in p.build_parts():
        assert shape.isValid()
        asm.add(shape,name=name,color=cq.Color(color))
    asm.save(str(OUT/'pump_candidate.step'))
    print('Estimated purchased-part proxy only; not a printable motor/pump')

def shells():
    OUT.mkdir(exist_ok=True)
    b.OUT=OUT/'shells';b.OUT.mkdir(exist_ok=True)
    b.PARTS.clear()
    original=b.make_head_carrier
    b.make_head_carrier=lambda config=None:original(CONFIG if config is None else config)
    b.body();b.head()
    asm=cq.Assembly(name='SHELL_CANDIDATES_NOT_RELEASED')
    for row in b.PARTS:asm.add(row['shape'],name=row['name'],color=cq.Color(row['color']))
    asm.save(str(OUT/'shell_candidates.step'))
    print('Unreleased shell candidates; purchased references are NOT rebuilt or refitted')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['check','carrier','pump','shells'])
    args=parser.parse_args()
    globals()[args.action]()
