"""Build V4 candidates or verify them against the public prototype; no hardware I/O."""
import argparse
import hashlib
import json
from pathlib import Path
import cadquery as cq
import trimesh
import build_carrier_v4 as v4
import build_v2 as baseline
import pump_reference

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def carrier():
    v4.main()


def check():
    carrier()
    report = json.loads((REPO/'validation/carrier_validation.json').read_text())
    assert report['all_pass']
    for name, row in report['meshes'].items():
        release = REPO/'print/carrier'/f'{name}_print.stl'
        assert hashlib.sha256(release.read_bytes()).hexdigest() == row['sha256'], name
        mesh = trimesh.load(release, force='mesh')
        assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split()) == 1, name
        old = cq.Shape.importBrep(str(ROOT/'latest/carrier_v4/assembly'/f'{name}.brep'))
        new = cq.Shape.importBrep(str(v4.OUT/'assembly'/f'{name}.brep'))
        assert old.isValid() and new.isValid()
        difference = old.cut(new).Volume() + new.cut(old).Volume()
        assert difference < .05, (name, difference)
    print('PASS: six published meshes and regenerated V4 solids; digital checks only, physical fit pending.')


def pump():
    pump_reference.main()


def shells():
    baseline.OUT = ROOT/'candidates/shells'
    baseline.OUT.mkdir(parents=True, exist_ok=True)
    baseline.PARTS.clear()
    baseline.body()
    baseline.head()
    assembly = cq.Assembly(name='BASELINE_SHELLS_HELD_NOT_V4_FITTED')
    for row in baseline.PARTS:
        assembly.add(row['shape'], name=row['name'], color=cq.Color(row['color']))
    assembly.save(str(baseline.OUT/'shell_candidates.step'))
    print('Held baseline shells: redesign around V4, camera and full motion envelope before printing.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', 'carrier', 'pump', 'shells'])
    globals()[parser.parse_args().action]()
