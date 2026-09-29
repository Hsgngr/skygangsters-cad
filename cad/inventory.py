"""Hash the git-index file allowlist; --write refreshes the handoff inventory."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--write',action='store_true')
args=parser.parse_args()
paths=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
paths=sorted(p for p in paths if p and p!='SHA256SUMS.json')
for p in paths:
    assert not any(v in Path(p).parts for v in ('old_work','candidates','__pycache__','.ssh'))
    assert (ROOT/p).stat().st_size<100*1024**2,p
hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
target=ROOT/'SHA256SUMS.json'
if args.write:target.write_text(json.dumps(hashes,indent=2)+'\n')
else:assert hashes==json.loads(target.read_text()),'Inventory differs; review changes before regenerating'
print('Inventory OK:',len(hashes),'files plus SHA256SUMS.json')
