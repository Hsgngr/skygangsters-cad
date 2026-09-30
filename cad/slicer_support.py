"""Portable diagnostic slicer helper. Never sends jobs to a printer."""
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess

SLICER = os.environ.get('PRUSA_SLICER') or shutil.which('prusa-slicer') or shutil.which('PrusaSlicer')
if not SLICER:
    mac = Path('/Applications/PrusaSlicer.app/Contents/MacOS/PrusaSlicer')
    if mac.is_file():
        SLICER = str(mac)
PROFILES = []
TMP = None  # Caller creates a fresh temporary directory.


def run(path):
    if not SLICER:
        raise RuntimeError('Set PRUSA_SLICER to the installed PrusaSlicer executable.')
    output = TMP / (path.stem + '.gcode')
    log = TMP / (path.stem + '.log')
    result = subprocess.run([SLICER, *PROFILES, '--export-gcode', '--output', str(output), str(path)], capture_output=True, text=True)
    content = result.stdout + result.stderr
    log.write_text(content)
    errors = [line for line in content.splitlines() if re.search(r'error|outside.*print|non.manifold|repair', line, re.I)]
    errors = [line.replace(str(path), path.name).replace(str(TMP), '<temporary>').replace(str(Path.home()), '<home>') for line in errors]
    metadata = {}
    if output.exists():
        with output.open('rb') as handle:
            handle.seek(max(0, output.stat().st_size - 90000))
            tail = handle.read().decode('utf-8', errors='replace')
        for line in tail.splitlines():
            if line.startswith(('; estimated printing time', '; filament used [g]', '; filament used [mm]')):
                key, _, value = line[2:].partition('=')
                metadata[key.strip()] = value.strip()
    ok = result.returncode == 0 and output.exists() and output.stat().st_size > 1000 and not errors
    print('SLICED', path.stem, ok, metadata, flush=True)
    return dict(name=path.stem, sha256=hashlib.sha256(path.read_bytes()).hexdigest(), exit_code=result.returncode, pass_check=ok, errors=errors, metadata=metadata, log=log.name)
