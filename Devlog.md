# CAD handoff devlog

Curated project-only record. Older geometry versions, original private devlog, photos and credentials are deliberately not published.

## 2026-09-29 — current handoff

- Created one current CAD snapshot: latest retained modular shells/body, current V2.2 carrier and rounded photo-derived pump. Excluded earlier carriers, concepts, block/scan pump models and old whole-assembly exports. Combined assembly is a review aid, not a full print release.
- Carrier printing started in PETG; fit result pending. User has no cable ties and prefers a printed lid/retaining bridge. Wait for carrier completion and physical gun seating before designing the retainer; aim to avoid another full carrier print.
- Identified a redundant Ø10 mm cut partly covered by the rear support at the PTZ crossbar. Four M3 mounting holes secure the carrier; centre cut has no confirmed function. Keep already-printing artifact unchanged; consider removing later.
- ESP32 confirmed plain DevKit V1 with ESP-WROOM-32, micro-USB and 30 pins, not ESP32-CAM. Body left controller reserve is not yet a board-specific mount. No firmware changed.
- Pi 5 received; OS Lite 64-bit installed, Wi-Fi and SSH public-key login verified. Eight OS packages updated, no outstanding upgrades/package-audit issues; no reboot after update. No camera or actuator setup. Network identity and all credentials omitted from this public handoff.

## 2026-09-29 — carrier release and coupon evidence

- PETG middle M3 coupon selected: 3.4 mm screw clearance / 5.7 mm nut AF. Left does not fit; right too slack; middle inserts very easily. Need anti-rotation check under gentle tightening. Supersedes earlier PLA judgement.
- PETG PTZ pattern passes by user report: finger installation, no rocking/warping. Camera fit coupon not yet tested.
- V2.2 carrier open cradle: 36 mm between walls for 32 mm housing, 0.5 mm nominal rear-cap pad allowance, 3 mm rear clearance, two strap stations through four 2.5 × 5 mm slots. Main-case contour and padding remain approximate.
- During development, 1.5 mm side allowance caused a zero-thickness wall/driver-cut tangency; 2 mm fixed it. Released single-solid, watertight mesh: 121 × 199 × 45 mm. 34 carrier CAD checks and nine sampled poses passed. Exact released STL preserved here.
- Diagnostic PETG slice passed: MK4S HF0.4 / 0.20 mm STRUCTURAL, four perimeters, 20% infill, 2 mm brim, automatic Snug supports, 2h55m31s / 67.49 g. Physical strength, full cable/hose sweep, weatherproofing and loaded operation remain unverified.

## Retained design decisions

- Independent head/body modules use purchased PTZ reference datums. Top bolt pattern 42 × 14 mm. Fixed lower body contains Pi, controller and nominal 500 ml reservoir; bottom bottle-access tray removable independently of structural chassis.
- Pump housing/nozzle measured 132.25 × 32 × 24 mm excluding elbow/hose; estimated mass 75 g. User photos justify oval main casing and nominal 18 mm circular barrel. Feature stations, elbow and nozzle axis are estimates, not calibrated photogrammetry. Keep 15 mm nozzle projection rather than enlarging the head.
- Camera Module 3 Standard is the initial camera. No accelerator selected. Camera proxy rotated around optical axis to route ribbon downward; camera mount and ribbon latch access require physical testing.
- 300 mm camera cable, provisional ±25° pan / ±15° tilt routing budget; these are not approved servo commands. No slip ring or continuous pan assumed.
- Servo labels: pan 20 kg·cm, tilt 25 kg·cm, both 6–7.4 V. Owned adapter 5 V / 10 A cannot power them directly. One external supply preferred but conversion/current sizing unselected. Pump original battery 3.7 V nominal; switch/motor must not be driven from GPIO.
- Existing source firmware in private working repo has Wi-Fi control and GPIO14/15 servo outputs, but immediate centre-on-start and uncalibrated range; pump control/watchdog absent. No powered motion authorized by CAD clearance tests.
- Engineering/fit first: defer cosmetic eyebrows, wings and shell beautification. Head/body shells remain on hold until physical payload fit, retention, connector access and motion/service clearances are resolved.
