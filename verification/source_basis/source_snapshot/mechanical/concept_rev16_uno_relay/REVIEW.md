# R16 Uno relay mount — design review

27 September 2026. Units: mm. Baseline: R15 Uno prototype body. R15 files and checks remain the issued comparison set.

## Requested change

Add mounts for the actual pump relay module below the Arduino Uno, inside the dry tower. An R16 prototype body, retained R15 lid and four-boss trial coupon have been exported. Physical fit is still open.

## Supplied part reference

- User-supplied listing: https://www.amazon.co.uk/dp/B0CSJQZ89V (ASIN B0CSJQZ89V).
- The supplied photographs show the delivered red PCB with a Songle SRD-05VDC-SL-C relay, four mounting holes and a screw terminal block at each end. Both photographs show the component side; the underside is still unseen.
- A [seller listing for the apparent module](https://ibspot.com/us/products/gtiwung-pack-of-10-one-channel-relay-module-5-v-1-channel-relay-board-with-optocoupler-isolation-high-level-trigger-relay-module-low-level-trigger-expansion-board-relay-switch-module-for-arduino) gives 50 × 26 × 18.5 overall, Ø3.1 holes and 44.5 × 20.5 hole-centre pitch. The 50 × 26 PCB size is consistent with the ruler photographs. Hole pitch, PCB thickness and height remain nominal until checked on the physical board.
- The user intends to use the same screws as for the Uno. The screw shown earlier by a ruler does not establish a reliable major diameter or head size; the 2.8 mm pilot remains a coupon trial.

## Options considered

| Layout | Benefit | Limit |
| --- | --- | --- |
| Vertical board below Uno | Short horizontal reach to side walls | The nominal 50 mm board would consume almost all of the 51 mm gap between battery saddle and Uno; no useful end clearance. |
| Horizontal board on rear dry wall | 26 mm high, front screw access, 12 mm nominal gap above battery and 13 mm below Uno | Wire bends at the two end terminals require a physical trial. **Selected for R16.** |
| Side-wall mount | Frees rear wall | Obstructs service access and risks the existing left-side connector aperture. |

## R16 nominal placement

- PCB x21–71, z33–59, underside seating at y76; populated face toward the removable fascia.
- Hole centres `(23.75,35.75)`, `(23.75,56.25)`, `(68.25,35.75)`, `(68.25,56.25)` in x/z.
- Contacts face right, toward the sump and pump cable route; DC+/DC-/IN1 face left. This is a routing choice for trial, not an electrical wiring approval.
- Four tapered rear-wall bosses: Ø8.5 at the seating tip, Ø10 at the root, 19 mm projection, Ø2.8 × 11 mm blind pilot. The same screw is intended as the R15 Uno bosses.
- Nominal side spaces to the inner shell walls: 15 mm at the logic terminal end, 19 mm at the contact terminal end. The stated component height gives a nominal frontmost y55.9; the fascia's *assumed* button rear limit is y39, leaving 16.9 mm in that direction. Actual terminal/wire bend and button hardware need assembly trial.
- No new penetration is made through the wet/dry wall.

## Current CAD space

- Uno board envelope: x13.71–82.29, z72.00–125.34; underside seating plane y76. Its lower edge is z72.
- Integrated battery saddle occupies approximately x12–84, y30–60 and rises to z21. The gap between its top and the nominal Uno lower edge is 51 mm before clearances.
- Rear dry-wall inner face is near y94. Both the Uno and R16 relay bosses project to y76; the relay seat and same-screw choice remain subject to physical fit.
- Fascia controls occupy the front of the tower. Their rearward envelopes and wire bends are not established by this space calculation.
- The R15 pump riser relief is in the wet-side sump. Relay mounts must remain in the dry tower and preserve the wet/dry partition.

## Evidence still needed from the relay

1. Underside photograph beside a ruler, with solder tails visible around all four holes.
2. Measured mounting-hole diameter and pitch, PCB thickness, rear solder projection and assembled component height.
3. Confirm the existing Uno screws pass through all four relay holes and their heads clear the adjacent terminal blocks/PCB parts.
4. Check actual print material/orientation and whether the Ø2.8 pilot accepts the screws without splitting.
5. Trial the contact and logic wire entries, bend radii, screwdriver access and relay removal with the Uno, controls and fascia present.

## Design and acceptance intent

- Preserve the R15 Uno bosses, roof and pump-clearance changes while modifying only the dry-tower mount region needed for the relay.
- Use the measured asymmetric mounting pattern if present. Avoid forcing the PCB, contacting solder joints or obscuring terminals.
- Leave accessible service loops, a reachable disconnect, and separation between relay contact/pump wiring and sensor/LCD wiring.
- Check board insertion/removal with the Uno, fascia and battery saddle in place. Check wall continuity and digital intersections before a physical fit coupon and full-body print.
- The relay module's electrical rating, reset state and pump-power path are governed by the current Uno relay wiring review; CAD fit does not close those checks.

## Digital verification and release status

- R16 `build.py` reports PASS after CAD solid validation, STEP readback, mesh export and named interference checks, but this CAD runtime returns exit code 1 during shutdown. That is **not** a clean build result.
- The independent `check_exports.py` exits 0: all three R16 STLs are closed, consistently wound single components with positive volume, two-face edges and no degenerate facets. Sections confirm all four relay pilots and tapered boss diameters on the body and fit coupon. The R16 lid has the same bounds and volume as the retained R15 lid.
- Digital PCB/nominal component envelopes do not intersect the R16 body; all body changes lie in the named dry-side relay-mount region. These checks do not prove physical insertion, screw retention, wire fit or electrical suitability.
- Recommended next print: the four-boss relay mount trial coupon. Mount the actual board with the actual screws, then approve or revise the full-body R16 STL. The R15 Uno screw, lid head and pump trials remain separate open gates.
