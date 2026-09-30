# Materials and hardware BOM — 2026-09-30

Current procurement/fit state. Not a final shopping list: unknown electrical ratings and fastener lengths must be resolved before ordering. Geometry files are not proof of fit.

**Current carrier: V4, derived from the user's STEP.** Rear and front fit tests are pending. This public pack includes all six prototype print files; print the small fit pairs before adapter/deck. Head/body shells and camera mount remain held. See the print guide for placement and screw engagement checks.

| Item | Qty | Status / requirement |
|---|---:|---|
| Yahboom 2DOF PTZ mechanism | 1 | Owned; STEP identity and printed top-hole pattern confirmed. Pan 20 kg·cm, tilt 25 kg·cm; both marked DC 6–7.4 V. Stall current, 3.3 V signal compatibility and travel unknown |
| Donor electric water gun/pump with nozzle/button/tube | 1 | Owned. Authoritative user STEP main casing/nozzle envelope 132.1 × 34 × 25.4 mm; physical body reported 29 mm, projecting features 32 mm. STEP/physical differences and omitted edge treatments need fit testing. Mass ~75 g estimate; motor current/switch topology unverified |
| Raspberry Pi 5, 8 GB | 1 | Received, OS Lite 64-bit/SSH working, packages updated; no actuator connection |
| Pi kit official 27 W USB-C supply | 1 | Use for Pi bench operation; independent from unapproved common-supply conversion |
| 32 GB microSD | 1 | In use, ~24 GB free after installation; not the originally advertised 128 GB kit storage |
| Raspberry Pi Camera Module 3 Standard | 1 | Ordered/expected; physical fit coupon still pending |
| 300 mm 15-pin Standard → 22-pin Mini CSI cable | 1 | Ordered; confirm receipt and real flex route, slack and strain relief |
| ESP32 DevKit V1 / ESP-WROOM-32, micro-USB | 1 | Owned/identified. 30 pins, four mounting holes; actual outline, hole pattern and height need measurement |
| YU0510 5 V / 10 A external adapter | 1 | Owned, centre-positive, indoor-only; barrel/screw-terminal attachment ratings unverified. **Not direct servo power** |
| Regulated 6 V servo supply/conversion | 1 branch | Unselected. Existing 5 V adapter would require a suitable BOOST; current/transient budget must include both servos |
| Regulated pump supply, nominal 3.7 V target | 1 branch | Unselected pending motor verification; do not feed from 5 or 6 V directly |
| 3.3 V-compatible motor-rated fail-OFF switching stage | 1 | Relay OR MOSFET, not both by default; suppress motor transients. Existing KF301 low-trigger relay stock is a candidate only |
| Fuses, holders, rated DC inlet/distribution and actuator disconnect | 1 set | Not selected/fitted; ratings follow current budget and wire/connector limits |
| Controller power interface | 1 | Pi USB to ESP32 micro-USB proposed. No simultaneous USB + VIN without verified board power-path support |
| Pi USB-C input interface for single-adapter scheme | 1 if used | Not selected; current capacity/voltage and USB-C negotiation not established by adapter's 10 A label |
| 500 ml bottle/cap | 1 | Not selected; CAD placeholder Ø90 × 110 mm total. Update to actual bottle before holder design |
| Pickup tube, cap barb/seal, make-up-air vent, tube retention | 1 set | Size to real tube/bottle; check priming/suction lift and leak isolation |
| PETG V4 rear fit pair | 1 saddle + 1 bridge | Diagnostic total 11.84 g; ~38m40; physical fit pending |
| PETG V4 front fit pair | 1 saddle + 1 bridge | Diagnostic total 11.63 g; ~37m53; physical fit pending |
| PETG V4 adapter + deck | 1 each | Diagnostic total 47.91 g; print after both fit pairs pass; reuse V4 bridges, not standalone saddles |
| Printed V4 retaining bridges | 2 distinct | Front/rear profiles differ; do not swap or reuse V3 parts |
| M3 bridge fasteners | 4 screws + 4 nuts | Nominal M3×8 with 4 mm foot + 4 mm ear, no extra washer allowance; verify engagement |
| M3 deck-to-adapter fasteners | 4 screws + 4 nuts | Nominal M3×10, 4 mm flange + 6 mm adapter; verify underside clearance |
| Thin compliant nonconductive padding | If needed | Select only after measured fit; nominal CAD profile clearance 0.4 mm, not a prescribed pad thickness |
| M3 carrier-to-PTZ screws | 4 | Length unresolved. 6 mm adapter counterbored to leave 2.8 mm below screw head; verify actual head, bracket engagement and underside clearance |
| M3 screws/nuts/washers for enclosure/chassis | TBD | Fit: 3.4 mm printed clearance / 5.7 mm nut AF / 2.6 mm pocket depth; lengths/counts follow final joints |
| M3 chassis rods | 4 provisional | Approximately 190 mm; verify assembled stack before cutting/buying |
| Camera M2 and Pi mounting hardware/spacers | As needed | Confirm actual holes, engagement, PCB underside and electrical isolation; camera coupon pending |
| Pi cooling and protective internal cover | 1 solution | Kit fan/heatsink expected; actual clearance/thermal result unresolved. Dedicated Active Cooler not confirmed |
| Splash barriers, drainage, seals and cable strain relief | 1 set | Not yet engineered; printed shell is not automatically waterproof |
| Base anchoring and bottle retention | 1 set | Must remain stable with ~500 g water plus bottle and moving payload |

No PCA9685 is required by default: ESP32 supplies servo PWM signals, separate regulated power supplies the servo motors. Existing firmware outside this public CAD repo uses GPIO14 pan and GPIO15 tilt; GPIO15 is a boot-strapping pin. GPIO13 pump is historical reservation only. USB serial commands, arming, calibrated travel and pump watchdog are not implemented in that baseline. See [wiring plan](docs/WIRING_PLAN.md).

Historical stock to recheck: MP1584EN buck modules (cannot boost 5 V to 6 V), KF301 relay modules and WAGO connectors. Original 14500 Li-ion cell is 3.7 V nominal / 500 mAh / 1.85 Wh; not planned as a final internal battery/charger. Never parallel it with a regulator. **User has no cable ties; none are assumed available.** No AI accelerator purchase required before benchmarking the Pi.
