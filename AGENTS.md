# CAD handoff instructions

Read README.md, BOM.md and Devlog.md first. This is a CAD-only public repository.

- Keep private paths, credentials, network configuration, photos, datasets and company material out.
- Current carrier is V4, derived from the pinned user STEP. V2.2 failed physically; V3 profiles did not fit. Do not recreate superseded carriers.
- User approved gun right offset 32 mm with length midpoint centred front-to-back; left side is reserved for camera. Do not silently centre it laterally or claim centre-of-mass balance.
- Await physical V4 rear/front fit-test results. No cable ties are assumed available. Bridges are bolted.
- Camera mount and shell attachments are not part of V4. Baseline head/body shells remain held and need integration/redesign.
- Use cad/rebuild.py; candidates go to ignored cad/candidates/. Do not overwrite released artifacts implicitly.
- Recheck CAD, mesh, support-free orientation, fastener/tool access and physical fit after changes. Keep digital evidence distinct from strength/cable-sweep/powered approval.
- Update BOM, devlog, print guide, validation and inventory when intentionally publishing changes. Stage reviewed files before refreshing inventory.
- Preserve shared PTZ datums and modular head/body access.
- Do not operate hardware, flash firmware or modify the Pi. Electrical design is unresolved.
- Keep older work outside the public current tree. Do not import private history to fill missing information.
