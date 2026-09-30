# CAD handoff instructions

Read README.md, BOM.md and Devlog.md first. This is a CAD-only public snapshot, not the original robotics/vision repository.

- Keep secrets, private notes/photos, network configuration, datasets/weights and company material out of this public repo.
- V2.2 failed during PETG support removal and is withdrawn. The original workspace now has a compact V3 gun cradle/adapter and retaining bridges; those sources/artifacts are NOT yet packaged here. See README toolchain/transfer notes before continuing on another laptop. No cable ties are available.
- Await physical fit of the local V3 saddle coupon plus one bridge. Do not reprint V2.2; camera coupon and head/body shells remain held. Do not equate digital checks with physical print, strength, cable-sweep or powered-operation approval.
- Keep head/body modular about the shared PTZ datums. Keep dimensions parametric. Avoid gratuitous cosmetic changes until fit is established.
- Use cad/rebuild.py; candidates go to ignored cad/candidates/. Never overwrite a released STL without explicit intent, tests and updated status.
- Validate CAD solids, mesh manifoldness, clearances, print orientation, support removal, real hardware fit and safe screw engagement. Re-slice changed parts. Update BOM/devlog and manifest/hashes with releases.
- Do not energize hardware, flash firmware, modify the Pi or assume physical access from this repo. Source firmware is not included; wiring notes are proposals with unresolved electrical gates.
- Older work is deliberately absent. Do not fetch/copy old private project history to fill gaps. Ask for missing physical measurements.
