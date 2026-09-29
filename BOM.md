# Materials and hardware BOM — 2026-09-29

Current procurement/fit state. Not a final shopping list: unknown electrical ratings and fastener lengths must be resolved before ordering. Geometry files are not proof of fit.

| Item | Qty | Status / requirement |
|---|---:|---|
| Yahboom 2DOF PTZ mechanism | 1 | Owned; STEP identity and printed top-hole pattern confirmed. Pan 20 kg·cm, tilt 25 kg·cm; both marked DC 6–7.4 V. Stall current, 3.3 V signal compatibility and travel unknown |
| Donor electric water gun/pump with nozzle/button/tube | 1 | Owned. Housing + nozzle 132.25 × 32 × 24 mm; ~75 g estimate; front ~18 mm round. Elbow/hose excluded from envelope. Motor start/run current and switch topology unverified |
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
| PETG | As sliced | Carrier baseline 67.49 g including supports/brim; coupons already tested. Final shell quantities not released |
| Printed gun retaining bridge/lid | TBD | Requested, **not yet designed**. Wait for carrier fit; aim to reuse carrier |
| Thin compliant nonconductive padding | As needed | Select after fit; prevent gun rolling without crushing case. Nominal rear-cap allowance 0.5 mm, estimated main-face gap ~2 mm |
| M3 carrier-to-PTZ screws | 4 | 4 mm printed mounting crossbar; choose engagement after checking actual bracket/clearance. Do not copy long coupon-test bolts |
| M3 screws/nuts/washers for enclosure/chassis | TBD | Fit: 3.4 mm printed clearance / 5.7 mm nut AF / 2.6 mm pocket depth; lengths/counts follow final joints |
| M3 chassis rods | 4 provisional | Approximately 190 mm; verify assembled stack before cutting/buying |
| Camera M2 and Pi mounting hardware/spacers | As needed | Confirm actual holes, engagement, PCB underside and electrical isolation; camera coupon pending |
| Pi cooling and protective internal cover | 1 solution | Kit fan/heatsink expected; actual clearance/thermal result unresolved. Dedicated Active Cooler not confirmed |
| Splash barriers, drainage, seals and cable strain relief | 1 set | Not yet engineered; printed shell is not automatically waterproof |
| Base anchoring and bottle retention | 1 set | Must remain stable with ~500 g water plus bottle and moving payload |

No PCA9685 is required by default: ESP32 supplies servo PWM signals, separate regulated power supplies the servo motors. Existing firmware outside this public CAD repo uses GPIO14 pan and GPIO15 tilt; GPIO15 is a boot-strapping pin. GPIO13 pump is historical reservation only. USB serial commands, arming, calibrated travel and pump watchdog are not implemented in that baseline. See [wiring plan](docs/WIRING_PLAN.md).

Historical stock to recheck: MP1584EN buck modules (cannot boost 5 V to 6 V), KF301 relay modules and WAGO connectors. Original 14500 Li-ion cell is 3.7 V nominal / 500 mAh / 1.85 Wh; not planned as a final internal battery/charger. Never parallel it with a regulator. **User has no cable ties; none are assumed available.** No AI accelerator purchase required before benchmarking the Pi.
