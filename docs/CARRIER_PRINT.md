# Carrier V2.2 — PETG dry-fit print

> **Withdrawn 2026-09-30:** this print broke at both pump-bed posts and the rear arm during support removal. Do not follow the historical print recommendation below. See the README for current V3 small-fit-test status and software handoff; V3 files are not yet bundled here.

2026-09-29. **Print this carrier only; head shells and body are not released.** This replaces the older carrier for the next physical fit test, not the whole V2.1 assembly.

**Latest physical status:** this carrier is printing. The user has no straps/cable ties and prefers a printed retaining bridge/lid. Wait for completion and inspect gun seating before designing it; no retainer exists yet. Strap instructions below describe the original retention option, not a requirement to purchase ties or a claim that the gun is already secured.

## Files

- **Print:** `../print/carrier/head_payload_carrier_v2_2.stl` — millimetres, already oriented and on the bed.
- Fusion part: `../cad/latest/carrier_local.step` — local Z=0 at the PTZ top mounting face.
- Fit reference: `../cad/latest/head_current_review.step` — current head shells, carrier, camera and photo-derived pump; purchased references are NOT print parts.
- Preview: `../previews/11_carrier_only.png`; installed view: `../previews/05_head_payload_access.png`.
- Original carrier validation and diagnostic slice evidence: `../validation/`. Source hashes refer to the original local release, before packaging; see README.

Do not print the `*_world.stl`: it is a render/assembly-coordinate reference, not the bed-oriented deliverable. Do not use the previous carrier from the old ZIP.

## What changed

- Uses measured pump envelope **132.25 × 32 × 24 mm**, retaining the approved 15 mm forward projection.
- Open cradle has **36 mm between side walls** (2 mm allowance each side) and a revised rear stop 3 mm behind the measured pump rear. It is not a fitted negative of the estimated rounded model.
- Nominal 0.5 mm allowance under the rear cap, roughly 2 mm under the photo-estimated flat main-case lands. Use suitable thin compliant padding/shims; exact contact and nozzle height need physical confirmation.
- Four 2.5 × 5 mm slots serve two retaining straps, at world Y=-68 and -42 mm, clear of the photo-estimated motor window and front elbow. Check actual latches, holes and moving parts before tightening straps.
- PETG-tested **3.4 mm M3 clearance holes**. The shared 5.7 mm nut-pocket choice remains recorded; the carrier itself does not introduce new captive nut pockets.
- PTZ top hole centres and camera mount are unchanged. Extra side clearance also avoids a zero-thickness tangency between a cradle wall and the screwdriver-access cut.

## Slice / print

Use PETG and the same actual printer/nozzle calibration as the successful PETG coupon. Existing diagnostic profile: **Original Prusa MK4S HF0.4 nozzle / 0.20 mm STRUCTURAL / Generic PETG**.

- Keep imported orientation; footprint **121 × 199 mm**, height **45 mm**.
- Four perimeters, 20% infill, 2 mm brim.
- Supports enabled, automatic placement, **Snug** style (not organic/tree for this checked baseline). Inspect support under raised platforms, camera bracket and strap-slot bridges, and ensure removal access.
- Estimated **2 h 55 min / 67.49 g PETG**, including supports/brim; your profile/material may differ. No printer-ready G-code is provided or sent to the printer.

Slicer completed without reported errors or repairs. The mesh is a single watertight, consistently wound component. Thirty-four CAD checks and nine sampled pan/tilt poses pass, including camera-region regression, measured pump envelope, photo-model elbow/stub, neutral purchased PTZ clearance, tool/ribbon access and sampled shell-removal paths. These are digital checks, not strength, flex-loop or waterproofing certification. ±25° pan / ±15° tilt samples do not authorize powered travel.

## After printing

1. Remove supports/brim carefully; clear screw holes and strap slots without enlarging them unnecessarily. Check flat seating and layer integrity.
2. With **servos and pump disconnected**, mount the bare carrier using correctly sized M3 screws. The mounting crossbar is 4 mm thick; choose engagement based on the actual bracket, not the long test screws. Verify no bottoming or underside interference. Stop if tightening is needed to flatten the part.
3. Dry-fit the real pump. Use light straps and compliant padding so it cannot roll or slide; do not squeeze the casing, tube, latches or moving parts. Check nozzle projection, elbow access, hose bend and rear wire exit. Expect to adjust padding because the detailed contour is photo-estimated.
4. Camera coupon remains first when the camera arrives. If it fits, install the camera gently and check access to the ribbon latch and the full cable width; do not clamp the PCB on components or force holes to align.
5. Send top/side photos with the pump mounted, plus any screw, strap or hose interference. A dry-fit pass precedes either shell print. No water or powered-motion testing is required for this stage.
