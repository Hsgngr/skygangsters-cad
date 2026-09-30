# Carrier V4 — derived from the user's pump STEP

2026-09-30. **Unpowered fit prototype; physical V4 results pending. Camera and shell mounting are not included or released.** Replaces guessed contact contours in V3/V3.1. Old artifacts are archived locally, not supplied in the public current tree.

## What changed

- Uses `pump_reference.py` / `references/water_pump/water_pump.step` at scale 1:1, not the photo or scan proxy. Original Fusion/STEP files remain unchanged.
- Extracts actual closed cross-sections from the main STEP solid at **7.5 mm and 81 mm from the rear face**, then offsets the profile outward **0.4 mm** for initial fit clearance. No guessed V or circular/elliptical cross-section. Missing physical fillets/chamfers are still missing; these remain fit prototypes.
- Two short lower saddles have the model's flat bottom and sloped sides. They terminate below the projecting seam tabs. The two different upper bridges follow the corresponding upper profiles, with extra lower clearance for seam tabs.
- Continuous low deck replaces slender posts. The bridges are separate parts printed on their sides. No long rear shell arm, and no unnecessary centre hole in the PTZ adapter.
- Front shoulder stops and two outboard rear stops limit axial sliding. Rear centre remains open (20 mm between stops); a 16 × 16 mm straight wire-clearance probe passes. Actual motor wire exit, hose, strain relief and moving loops still require physical checks.
- Retains the tested **42 × 14 mm four-hole PTZ pattern**, 3.4 mm M3 holes, 5.7 mm nut flats and 2.6 mm nut pocket depth. Adapter-to-deck front bolt row moved by 1 mm for driver access; do **not** mix the old V3 adapter with the new deck.

Gun placement maps native `(x,y,z)` to `(32+x, 66.05-z, 12.4+y)` mm relative to the PTZ top face. This centres its geometric length front-to-back over the mounting pattern, not its measured centre of mass. The nozzle points toward negative assembly Y. Source shape includes the user's modeled fittings but not the complete real hose/wire route.

## Files and print order

Published paths are relative to the repository root:

- `cad/latest/carrier_v4/assembly/carrier_v4_review.step`: complete review with user pump and purchased PTZ.
- `cad/latest/carrier_v4/assembly/`: component STEP/BREP and assembly/reference STLs. **Not the slicer folder.**
- `print/carrier/`: print-oriented STL files only.
- `previews/`: three actual CAD renders of installed, open-rear and exploded views.
- `validation/carrier_validation.json`, `validation/carrier_slicer_validation.json`: digital evidence, not proof of strength.

Rebuilds write to ignored `cad/candidates/carrier_v4/`, never over these published files.

**First: rear fit saddle + rear bridge**, about **38m40 / 11.84 g** from separate diagnostic slices. Place the saddle centre 7.5 mm forward from the gun's rear casing face; 10 mm-wide contact region spans 2.5–12.5 mm from that face. The screw ears are 14 mm long. This tests the actual rear support profile without reprinting the whole deck.

Then test **front fit saddle + front bridge**, about **37m53 / 11.63 g**. Front centre is 81 mm from the rear face (51.1 mm behind the STEP's nozzle tip); lower contact spans 76–86 mm. Match the front/rear pairs; they are not interchangeable. These bridges are **new profiles**, not the old V3 bridges.

Once both fits pass, print **PTZ adapter + gun deck**. Reuse the two tested V4 bridges; the standalone fit saddles are coupons, not extra assembly parts. Full functional assembly is four printed parts: adapter, deck, front bridge, rear bridge. Do not attach standalone coupons on top of the deck's integral saddles.

| Print file | Envelope, mm | Diagnostic estimate |
|---|---|---|
| `ptz_adapter_print.stl` | 102 × 53 × 6 | 58m18 / 24.18 g |
| `gun_deck_print.stl` | 72 × 99.05 × 14.4 | 1h09m51 / 23.73 g |
| `rear_bridge_print.stl` | 72 × 31.05 × 8 | 18m48 / 6.21 g |
| `rear_fit_saddle_print.stl` | 72 × 14 × 14.4 | 19m52 / 5.63 g |
| `front_bridge_print.stl` | 72 × 28.2 × 8 | 17m53 / 5.66 g |
| `front_fit_saddle_print.stl` | 72 × 14 × 14.4 | 20m00 / 5.97 g |

PETG, supplied orientation, MK4S HF0.4, 0.20 mm STRUCTURAL, **5 perimeters, 25% infill, 2 mm brim, supports OFF**. Every diagnostic slice has no support-material toolpaths. Nut-pocket roofs and sideways screw holes still involve short bridges; inspect layer preview and actual print. Do not rotate the upper bridges upright. Combined plate times may differ.

## Dry-fit and fasteners

Disconnect battery/power. Support the gun on the table. Lower it into each saddle without forcing it; install the corresponding bridge. The profile clearance should not be closed by bending the bridge/casing with the screws. Check contact, rocking, side clips, motor windows, hose and wires. Small gaps at unmodeled rounded corners may remain; do not demand sharp-edge/full-surface contact. Thin compliant nonconductive pads may be needed, but choose thickness only after measuring actual gaps; do not force a thick pad into the 0.4 mm nominal clearance.

- Each bridge: two M3 nuts and nominal **M3×8** screws, no extra washer thickness assumed (4 mm foot + 4 mm ear). Check actual engagement/projection.
- Deck to adapter: four M3 nuts and nominal **M3×10** screws (4 mm flange + 6 mm plate). Nuts seat under the adapter; check underside clearance.
- Adapter to PTZ: four M3 screws into the metal pattern, length **not yet specified**. Counterbore leaves 2.8 mm of plastic below the screw head. Check actual head dimensions, thread engagement and underside clearance; do not reuse long coupon bolts blindly.
- Install the PTZ adapter before the deck, since the deck covers part of the PTZ screw-access area. Deck and bridge screw-driver paths are checked with components assembled.

Full unpowered assembly checks: both bridges' feet seat, no rocking, gun does not roll, end stops limit fore/aft motion without pushing the wire exit, and removal is possible with bridges removed. CAD predicts end-stop contact after a 1 mm axial shift; this is a geometry test, not a tested load rating. No glue or strong clamp force to compensate for poor fit.

## Validation and unresolved work

Six printable parts are valid single solids and watertight, consistently wound single-component meshes. CAD checks cover actual STEP interference, part/part and PTZ interference, straight-up gun and bridge removal, driver access, rear wire probe, end-stop engagement, and nine sampled pan/tilt poses against the purchased mechanism's fixed/pan solids. All digital checks pass; see the report for the current count/results.

Those poses do **not** check the existing body/head shell or a real hose/ribbon sweep. Gun reference tessellation has a known open-edge issue, so all fit/intersection operations use STEP solids, not the reference STL. Some purchased PTZ preview triangles are degenerate; Blender drops them only for rendering. Printable meshes pass their own checks.

Source dimensions/omitted edge treatments must still be reconciled with physical hardware. No FEA, load/adhesion proof, weatherproofing, arming, electrical safety or powered-motion release. Camera fit test, compact camera bracket, independent head shell attachment and full head/body clearances remain next-stage work. The old shell geometry is not compatible merely because the carrier fits the PTZ.

## Reproduce locally

```sh
.venv/bin/python cad/rebuild.py check
.venv/bin/python cad/slice_carrier_v4.py
blender --background --python cad/render_carrier_v4.py
```

Dimensions live in `cad/carrier_v4.json`; STEP identity is pinned in `cad/pump_reference.json`. All build dependencies and purchased PTZ BReps are included. See the README for environment setup and desktop executable configuration. Rendering is CAD-based; no generated concept imagery. No hardware is operated and no print job is sent.
