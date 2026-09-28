# R15 Uno mechanical change review

27 September 2026. Units: mm. R14 is the printed baseline. R15 is a prototype geometry issue with physical fit trials pending.

## 1. Current state

| Feature | R14 geometry | Physical finding |
|---|---|---|
| Uno mounts | Four 6.0 outside-diameter bosses with 2.8 blind pilots, 11 deep from the board seat | Operator reports splitting during screw insertion. New Photo 2 shows deformed/split printed bosses; loose filament is excluded from the defect assessment. Screw dimensions and print material remain unmeasured. |
| Roof | 3.0 thick; four 3.4 through-holes, without head recesses | Operator requests a thicker roof and flush screw heads. New Photo 1 shows a screw against a ruler, but does not establish that the same screw is used for the lid or a precise head diameter. |
| Pump/tube route | Provisional 10.0 tube bore at x123/y92; wet-side service relief x106.5–130, y83–94, z18–52 | The earlier installed-pump photo and new Photo 3 show the outlet and connected tube. New Photo 4 identifies the lower riser ledge as the requested clearance area. |

The R14 tower/sump is one printed body. The R13 fascia and planter are retained unless an interface check identifies another change.

## 2. Constraints and unknowns

- Preserve the asymmetric Uno mounting centres, board seating plane and fascia interface.
- Keep the tube and pump on the wet side of the partition; retain a continuous dry-side wall and serviceable pump-lead route.
- Maintain lid screw engagement and tool access after changing lid thickness and head pockets.
- Record actual screw type, major diameter, head diameter and height, length, material, print orientation and the location of the split. A 2.8 pilot does not establish a qualified thread-forming fit.
- The ruler photos support approximate hardware scale, but are not calliper measurements of the screw head, tube or installed clearance. Verify those dimensions during fit trials.
- The R14 vertical passages and nominal 10.0 tube bore are retained; Photo 4 points to the ledge below them.

## 3. Options and recommendation

| Feature | Option | Trade-off |
|---|---|---|
| Uno bosses | Increase wall thickness along the screw engagement length; add a gradual root taper and full-depth trial coupon | Retains the simple four-screw assembly. Pilot and boss sizes must be selected against the actual screw and printed material. A taper alone does not cure splitting at the free end. |
| Uno bosses | Heat-set inserts or captive nuts | Better repeated service, but needs insert/nut dimensions, installation access and a larger local envelope. |
| Roof | Increase thickness and add four head pockets sized to the selected fastener | Gives flush heads; pocket depth must leave a continuous load-bearing floor and enough material at the outer edge. |
| Pump route | Rotate or shift the pump with the tube attached | May avoid a geometry change but can obstruct planter insertion or create a tight tube bend. |
| Pump route | Extend the existing wet-side relief down to the sump floor | Directly removes the ledge identified in Photo 4, while retaining the rear wall and dry-side web. The real tube still needs a fit trial. |

Selected R15 prototype: four 8.5 mm tip / 10.0 mm root tapered bosses, retaining 2.8 mm x 11 mm pilots; 5.5 mm roof with 6.6 mm x 2.5 mm head pockets; lower the wet-side relief from z18 to z4 and extend its right edge from x130 to x132. The sump floor remains 4 mm and the relief stops at y94, leaving a nominal 6 mm rear band and at least 12.5 mm of dry-side web. Existing tube/wire bores reduce the local rear-wall thickness. The altered roof projects 1.5 mm beyond the tower sides to retain material around the pockets. See README.md for files and trial order.

## 4. Acceptance criteria

1. A full-length boss coupon printed in the intended material and boss orientation takes the selected screw without splitting, excessive board load, bottoming or loss of retention. Trial both 2.8 and 3.0 mm pilots; the exported body uses 2.8 mm until the trial supports a change.
2. All four Uno mounting holes register and seat without forcing the board. Inspect solder joints and nearby components against the enlarged bosses and screw heads.
3. Lid screws fit with heads flush or below the outer face, without breaking through the remaining floor or side edge. Lid seats against the unchanged body interface.
4. Pump and connected tube can be installed and removed without force or kinking, first against the local route trial and then in the complete body. The tube remains in the wet route; the dry-side partition remains continuous. Inspect and test the printed body for leakage before wet operation.
5. R15 STEP and STL exports are single valid solids with closed, consistently wound, positive-volume meshes. Critical sections, assembled clearances and the changed-volume regions pass digital checks against R14; printed fit and leak tests remain open.

## 5. Remaining physical evidence

- Screw type and calliper dimensions; printer material, orientation and layer settings; repeatable screw trial result in the matching R15 coupon.
- Confirmation whether the pictured screw is used for the roof, and actual lid head diameter/height and engagement.
- Pump/tube fit result in the local route trial and full body, followed by a controlled wet-side leak check.

Digital geometry is complete for a prototype print trial. Physical acceptance and the correct pilot/head fit remain open.
