"""Load and inspect the authoritative user-modeled pump without modifying it.

New holder work should import load_reference() instead of the photo proxy.
Source axes are native Fusion axes; no implicit scaling or assembly placement.
"""
import hashlib
import json
from pathlib import Path

import cadquery as cq
import trimesh

ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT/'pump_reference.json').read_text())


def load_reference():
    source = ROOT/CONFIG['authoritative_source']
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != CONFIG['source_step_sha256']:
        raise ValueError('Pump STEP changed: inspect new geometry and explicitly update reference metadata.')
    shape = cq.importers.importStep(str(source)).val()
    assert shape.isValid() and shape.Solids(), 'Invalid pump source geometry'
    assert all(s.isValid() and s.Volume()>0 for s in shape.Solids())
    return shape


def main():
    shape = load_reference()
    out = ROOT/'candidates/pump_user_reference'
    out.mkdir(parents=True,exist_ok=True)
    box = shape.BoundingBox()
    bounds = {a: [getattr(box,a+'min'),getattr(box,a+'max')] for a in 'xyz'}
    solids = []
    for i,part in enumerate(shape.Solids(),1):
        file = out/f'pump_body_{i}_reference.stl'
        cq.exporters.export(part,str(file),tolerance=.05,angularTolerance=.12)
        mesh = trimesh.load(file,force='mesh')
        solids.append(dict(name=f'pump_body_{i}',valid=True,volume_mm3=part.Volume(),
                           watertight=bool(mesh.is_watertight),
                           winding_consistent=bool(mesh.is_winding_consistent),
                           reference_stl=file.name))
    shape.exportBrep(str(out/'pump_user_reference_native.brep'))
    report = dict(source=CONFIG,valid=True,solid_count=len(solids),
                  native_bounds_mm=bounds,native_extents_xyz_mm=[box.xlen,box.ylen,box.zlen],
                  parts=solids,print_release=False,
                  limitations=['User omitted chamfers/fillets.',
                               'STL tessellation may have open edges even for valid CAD solids; inspect per-part flags. Use STEP/BREP for geometry, not these preview meshes for manufacturing.',
                               'Full measured contact profile, cable/hose routing and source-to-carrier placement not verified.',
                               'V4 uses this source; physical holder fit remains pending.'])
    (out/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
