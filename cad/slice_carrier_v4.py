"""Support-free diagnostic slices for STEP-derived V4 carrier; no printer jobs."""
import json
import tempfile
from pathlib import Path
import slicer_support as s

OUT=Path(__file__).resolve().parent/'candidates/carrier_v4'
s.TMP=Path(tempfile.mkdtemp(prefix='carrier-v4-slices-'))
s.PROFILES=['--printer-profile','Original Prusa MK4S HF0.4 nozzle',
            '--print-profile','0.20mm STRUCTURAL @MK4S 0.4','--material-profile','Generic PETG @MK4S HF0.4',
            '--no-support-material','--no-support-material-auto','--brim-width','2','--skirts','0',
            '--perimeters','5','--fill-density','25%','--threads','2','--no-binary-gcode']
audit=json.loads((OUT/'validation.json').read_text())
assert audit['all_pass']
results=[]
for name in audit['meshes']:
    row=s.run(OUT/'print'/f'{name}_print.stl')
    assert row['sha256']==audit['meshes'][name]['sha256']
    code=(s.TMP/f'{name}_print.gcode').read_text()
    row['has_support_toolpaths']=';TYPE:Support material' in code
    assert row['pass_check'] and not row['has_support_toolpaths'],name
    results.append(row)
(OUT/'slicer_validation.json').write_text(json.dumps(dict(profiles=s.PROFILES,parts=results,all_pass=True,
    scope='Diagnostic only; trial rear saddle/bridge first. No automatic full carrier or powered release.'),indent=2)+'\n')
