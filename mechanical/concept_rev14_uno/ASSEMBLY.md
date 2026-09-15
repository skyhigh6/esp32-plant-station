# R14 assembly supplement and configuration list

Document ID: PLANT-WC-UNO-MOUNTS
15 Sep 2026 | Revision R14 | Status: issued for prototype review; physical acceptance open.

## Required configuration

| Item | Quantity | Revision / file |
|---|---:|---|
| Integrated tower/sump | 1 | R14 tower_sump_body_uno |
| Fascia | 1 | R13 fascia_charcoal |
| Roof | 1 | R13 top_cover_sage |
| Planter | 1 | R13 planter_sage |
| Uno mounting coupon | 1 trial piece | R14 uno_mount_fit_coupon |
| Arduino Uno board | 1 | Uno R3 standard assumed; actual variant unknown |
| Board screws | 4 | M3 candidate; head type and length to be established by trial |

Retain selected R13 knob and non-carrier accessories as required. This is a mechanical supplement to the R13 kit guide. Its carrier mounting instructions and carrier coupon do not apply to the Uno configuration. R13 firmware/wiring instructions are not Uno commissioning authority.

## Work sequence

1. Record board manufacturer, revision and measured hole registration. Print the coupon at 100% in the intended material/process. It is a rectangular board-envelope gauge, not an exact outline replica.
2. Offer the coupon to the board underside with its screw-test boss facing away. All four nominal 3.2 mm gauge holes must register without bending or forcing the board.
3. Test the chosen screw in the coupon's 2.8 mm pilot. Establish tapping or thread-forming method, screw-head clearance and retention without cracking. The coupon boss is 8 mm high, so use a short test screw; it does not reproduce the tower's 11 mm blind depth.
4. Review tower slicing, especially the horizontal standoffs, roots and internal supports. Printer, material, layer height and support strategy are not specified; record them before manufacture.
5. Inspect the printed tower: all four bosses attached, roots intact, pilots unobstructed, seating faces in one plane. Remove support without enlarging holes or damaging the wet/dry partition.
6. With power disconnected and fascia/roof removed, insert the Uno through the front opening. Components face the fascia, USB faces left, PCB underside seats at y76. Use the asymmetric pattern to confirm orientation.
7. Select screw length from actual board thickness and any washer. Engagement must stay below the 11 mm pilot depth with positive bottoming margin. Tighten only sufficiently to retain the board; no qualified torque is available.
8. Check all four supports contact the board without bowing. Inspect screw heads, underside joints, USB and power connectors, headers and wiring against the enclosure and fascia. Confirm tool access and cable insertion/removal before closing the enclosure.
9. Refit the retained R13 fascia, roof and planter. Record the acceptance results. Proceed to separate electrical commissioning only under the applicable verified Uno instructions.

## Hold points

Do not print the full tower until coupon registration and screw fit pass. Do not accept the installed board until USB/cable, component, head and wiring clearance checks pass. A failed interface requires a recorded geometry correction or an explicitly assessed routing arrangement; do not force the board or cable.

## Close-out

Record results in [ACCEPTANCE.md](ACCEPTANCE.md), retaining photographs, actual screw specification and measured clearances. CAD fit is not physical acceptance.
