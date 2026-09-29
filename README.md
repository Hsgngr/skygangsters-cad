# Skygangsters — current owl CAD

Public CAD-only handoff, 29 September 2026. One current snapshot, not the original project's git history. Start here when continuing work with another assistant.

## Current status

- **Carrier V2.2 is currently printing in PETG.** It is cleared only for an unpowered physical fit test, not powered motion or water operation. No physical carrier result yet.
- Current head/body shells remain **on hold**. Their latest geometry is included, but no shell print files are offered as a released print pack.
- The pump is the latest rounded photo-derived reference: measured housing/nozzle 132.25 × 32 × 24 mm, approximately 75 g; nominal 18 mm round front. Elbow/hose and local details are estimated.
- PETG coupon: middle option selected, 3.4 mm M3 clearance / 5.7 mm nut pocket across flats. Confirm nut does not spin when gently tightened. PTZ four-hole coupon passes: finger installation, no rocking/warp. Camera coupon still pending.
- User has **no cable ties** and requests a printed removable retaining bridge/lid. **WAIT for carrier print and real-gun dry fit before designing it.** Try to reuse the printed carrier. No retainer has been designed yet.
- Pi 5 received, Raspberry Pi OS Lite 64-bit installed; Wi-Fi/SSH key login verified and OS packages updated. No reboot performed after updates. No camera/application/actuator setup done. Credentials/network identity are deliberately excluded.

## Open or print

| File | Purpose |
|---|---|
| [Current assembly](cad/latest/owl_current_review.step) | Fusion/importable review: latest retained shells/body + V2.2 carrier + rounded pump |
| [Head assembly](cad/latest/head_current_review.step) | Same current head, local mounting plane Z=0 |
| [Carrier STL](print/carrier/head_payload_carrier_v2_2.stl) | Only released large part: PETG unpowered dry-fit print |
| [Carrier print guide](docs/CARRIER_PRINT.md) | Orientation, Snug supports, assembly checks |
| [BOM](BOM.md) | Hardware/materials, procurement and open decisions |
| [Devlog](Devlog.md) | Concise CAD-relevant decisions and evidence |
| [Wiring plan](docs/WIRING_PLAN.md) | Proposed topology, not an energized wiring release |

![Current carrier](previews/11_carrier_only.png)

STL print units are mm; leave the supplied carrier orientation unchanged. Baseline: MK4S HF 0.4, PETG, 0.20 mm, four perimeters, 20% infill, 2 mm brim, automatic **Snug** supports; diagnostic estimate 2h55m / 67.49 g. STEP assembly coordinates are not bed orientations. Purchased electronics, PTZ and pump references must not be printed.

## Editable CAD and reproducibility

`cad/latest/components/` contains one current world-space BRep per component; `manifest.json` identifies print/reference/reserve parts. Current body and shells retain their prior revision because they have not changed; superseded carriers, rectangular pumps, scans and concepts are not included.

`cad/build_v2.py` contains the current body/head shape functions, `cad/build_pump_photo_reference.py` the rounded pump shape functions. Historical full-build/export entry points have been removed for the handoff. JSON files beside them are editable dimensions. Some procurement/status metadata in these original engineering parameters is historical; **this README and BOM are authoritative for current status**. Changing dimensions is not physical validation.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python cad/rebuild.py check
.venv/bin/python cad/rebuild.py carrier
.venv/bin/python cad/rebuild.py pump
```

`check` compares regenerated carrier geometry with the published BRep, checks the released mesh/hash and rechecks carrier clearances. `carrier` and `pump` write **unreleased candidates** into ignored `cad/candidates/`; they do not overwrite published files. Use `shells` only for deliberate head/body redevelopment. Purchased reference geometry is a saved snapshot and is not automatically resized/repositioned when parameters change. Revalidate and re-slice before approving any changed print.

Original carrier audit reports in `validation/` preserve the 34 checks and nine sampled poses from the local release. Their source hashes identify the original scripts before this packaging refactor, not the extracted source modules here. The exported carrier STL is byte-identical to that release. The combined review assembly is a packaging update, not new full-assembly clearance or print certification. `SHA256SUMS.json` inventories the initial handoff (regenerate after future edits).

## Next work / constraints

1. Wait for print. Inspect flat mounting and screw engagement with power disconnected; do not use bolts to flatten a warped part.
2. Seat real pump, photograph top/side, measure clearance above and around casing. Design a removable padded retaining bridge around measured contact points; avoid hose/elbow, motor vents/windows, latches, wires and moving features. Do not assume existing strap slots support a screw-clamp load.
3. Test camera coupon before installing the PCB. Then verify carrier/payload fit, cable access, head-shell removal and motion clearance before any shell print.
4. Measure ESP32 DevKit V1 board, underside pins, four hole centres and micro-USB plug clearance. Left body `controller` reserve is only 32 × 58 × 18 mm; not a proven board fit. Right `pump_interface` is likewise a placeholder, not a selected driver.
5. Bottle remains parametric nominal 500 ml: provisional 90 mm diameter × 110 mm height, not a verified bottle. Water stays low in the fixed body; removable bottom is for servicing, not removal of the structural chassis.
6. Engineer wet/dry separation, fixed rear power inlet, Pi protection/cooling, fuses/regulators, hose and ribbon service loops. Head/body remain independent modules referenced to the purchased PTZ.
7. No powered actuator tests until rated supplies, current budget, signal compatibility, travel limits, deliberate arming, pump timeout and fail-OFF behavior are established. Use only low-pressure humane deterrence; exclude people, pets and unsafe spray areas.

The unused partially covered Ø10 mm crossbar hole remains in the already-printing carrier. It is not a mounting screw or finished cable passage; consider removing in a future revision, not silently changing this released STL. Cosmetic eyebrows/wings are deferred.

## Sources and publishing scope

- Purchased Yahboom PTZ geometry is derived from [YahboomTechnology/2DOF-PTZ](https://github.com/YahboomTechnology/2DOF-PTZ), commit `77a32cbb338fb1bf03d1c98dba7d7cf1c637fdc2`, `5.3D Model file/2DOF PTZ.STEP`. No explicit redistribution license was identified; no project license is asserted over manufacturer geometry.
- Pi reference derives from Raspberry Pi's official Pi 5 STEP; retained major solids only. See [manufacturer drawings](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#schematics-and-mechanical-drawings) and included [MIT notice](THIRD_PARTY_RASPBERRY_PI_LICENSE.txt).
- Camera proxy uses the [Module 3 Standard mechanical drawing](https://datasheets.raspberrypi.com/camera/camera-module-3-standard-mechanical-drawing.pdf). It is inverted about its optical axis for ribbon access; image rotation will be needed.
- No original photos/scans, recordings, software firmware, model datasets/weights, secrets, private Obsidian notes, network configuration or old git history are included. No new blanket open-source license has been chosen.
- Older local work lives outside this public snapshot in the original workspace's ignored `old_work/`. Do not add it here or copy private project data into this repo. Use company tools only as permitted by your employer; a public repo does not override those rules.
