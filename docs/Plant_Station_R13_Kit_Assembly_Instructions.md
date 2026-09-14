# Plant Station | Kit assembly instructions

R13 / Customer-format prototype edition / 14 September 2026

![](C:\Users\kevin\Documents\ChatGPT\plant\mechanical\concept_rev13\product_ai.png)

Build a compact manual-watering station with a removable planter, pump reservoir and serviceable electronics tower.

<b>Read before assembly.</b> This manual describes the current mechanical kit. Electrical connections, the power system, maximum fill level and final control labels are not released. Complete the mechanical dry build; keep power disconnected until the matching verified wiring and commissioning instructions are available.

Cover image: AI appearance illustration based on R13 CAD. LED colours, fitted components and the depicted sound grille are illustrative; actual CAD has one 4 mm sound opening. Use the CAD diagrams and dimensions for assembly.

# 1 | Check the kit and prepare

Identify the four main printed parts: <b>A</b> integrated tower / sump / battery saddle; <b>B</b> front fascia; <b>C</b> roof; <b>D</b> removable planter. Also select one shaft-matched knob. There is no separate hose clip, clip screw, battery tray or battery tray screw.

![](C:\Users\kevin\Documents\ChatGPT\plant\mechanical\concept_rev13\exploded.png)

<b>Provisional hardware allocation:</b> 12 plastic thread-forming 3 x 8 mm pan-head screws (4 carrier, 4 fascia, 4 roof); 4 M2.5 x 16 mm screws and 4 nuts for the LCD; component-supplied button/pot nuts; one suitable cable tie. Validate the screw family and engagement on a fit sample before use.

<b>Components:</b> carrier and ESP32 module, LCD/backpack, three buttons and LEDs with resistors, potentiometer, 10 mm case piezo, insulated cell holder, pump, tubing, moisture sensor and an approved insulated harness/power/driver set. Exact electrical part variants remain to be fixed.

<b>Tools:</b> matching hand screwdrivers, small spanners, callipers, side cutters for the tie, and a soft deburring tool. Work on a clean, dry tray. Do not use a powered driver.

# 2 | Inspect and trial-fit

![](C:\Users\kevin\Documents\ChatGPT\plant\mechanical\concept_rev13\internal.png)

1. Remove print debris and supports. Check the screw supports are continuous and inspect the sump floor for cracks or pinholes. Clear both planter drain holes.

2. Trial the carrier and LCD against their fit coupons before fitting them. Carrier installed centres: 57 horizontal x 60 vertical mm. LCD centres: 75 x 31 mm. Nothing should need forcing or bending.

3. Check the selected insulated holder fits the 72 x 22 mm saddle clearance. The holder rests at z12; it must not expose cell contacts to the printed base or tie.

4. Trial the planter vertically into the sump and lift it clear. The local skirt notches must clear the service riser and sensor lead. Remove the planter for the following steps.

<b>Pass:</b> no cracks, loose fragments, blocked passages, bowed boards or forced fits. Resolve a failed fit before proceeding.

# 3 | Route the pump tube and leads

![](C:\Users\kevin\Documents\ChatGPT\plant\mechanical\concept_rev13\cable_section.png)

1. With power disconnected and planter removed, trial the pump in the sump. The reserved body envelope is 38.5 x 25.5 x 43 mm; verify the actual outlet and mounting requirements.

2. Feed the tube from the common sump-side intake up the <b>10 mm bore at x123/y92</b>. The outlet is above the planter. Curve the free tube gently towards the soil, respecting its specified minimum bend radius. Keep the whole water tube outside the electronics cavity.

3. Feed the two pump wires into the separate <b>8 mm bore at x110/y92</b>, then through the crossover into the tower. Do not force moulded connectors through a passage.

4. Check for kinks and abrasion. Provide retention and strain relief matched to the real tube and cable. The removed clip is not required; outlet retention still needs a physical fit trial.

Rim height is not a fill instruction. The passages are not sealed glands. Do not add water during the electrical assembly.

# 4 | Sensor lead and battery holder

![](C:\Users\kevin\Documents\ChatGPT\plant\mechanical\concept_rev13\sensor_entry_section.png)

1. Route the sensor lead through the 8 mm side entry, centre y65/z64. Its lower edge is level with the sump rim. Use the matching local relief in the planter skirt.

2. Leave a service loop so the probe and planter can be removed without pulling the lead. Fit suitable edge protection and strain relief; arrange the external lead to shed drips away from the opening. Actual connector and bend fit need checking.

![](C:\Users\kevin\Documents\ChatGPT\plant\mechanical\concept_rev13\battery_tie_section.png)

3. Thread the tie through the 6 x 2.5 mm tunnel beneath the saddle before fitting the insulated holder. A 4.8 x 1.5 mm tie is the current fit assumption. Keep the locking head accessible.

4. Tighten only enough to retain the holder. Keep the tie clear of contacts and avoid distortion. Trim the tail. The old battery screw holes have been removed. Leave the cell out.

# 5 | Fit the fascia and carrier

![](C:\Users\kevin\Documents\ChatGPT\plant\mechanical\concept_rev13\fascia_rear.png)

1. Fit the LCD to the rear standoffs using its four screws and nuts. Trial head diameter at or below 5.5 mm. Confirm thread projection and insulation; do not bow the board.

2. Fit the three panel buttons and potentiometer with their supplied washers and nuts. Button holes are nominal 12 mm; the pot hole is 7 mm. Final third-button function and indicator labels remain provisional.

3. Dry-fit the LEDs and piezo. Use compatible adhesive sparingly around case perimeters, keeping lenses, the sound port, contacts and the piezo vibrating surface clear. Follow the adhesive cure instructions.

4. Secure the carrier to the rear bosses with its USB edge facing left. Check both actual plugs in the 28 x 20 mm side opening. Keep screw tips clear of conductors.

5. Fit the shaft-matched knob gently, with at least 0.5 mm clearance from the fascia/nut. Do not mark it in millilitres until flow has been calibrated.

# 6 | Close and inspect the dry assembly

![](C:\Users\kevin\Documents\ChatGPT\plant\mechanical\concept_rev13\assembly.png)

1. Keep all supplies disconnected. Connect only a released, identified harness; no terminal or GPIO pinout is authorised by this mechanical manual. Keep joints insulated and wires away from screw tips.

2. Offer up the fascia with a service loop and secure its four screws. Fit the roof with four screws. Hand-tighten to seated contact; no torque value has been validated.

3. Fit the planter and check the tube, pump wires and sensor lead remain free. Lift the planter through its full removal travel, supporting the body and managing the service loops.

<b>Dry acceptance:</b> screws retain without stripping; carrier/LCD do not bow; both USB plugs engage; holder is secure; tube is unkinked; both drains are open; all covers seat; planter removal does not pull or trap services.

Do not energise a kit with an unidentified battery, charger, power path or harness. Record any failed check before replacing the covers.

# 7 | Commissioning, use and care

<b>Commissioning remains open.</b> Before a powered wet test, verify the exact carrier pinout, supply levels, fuse/disconnect, cell protection, pump driver/default-OFF behaviour and installed firmware. Establish a fill mark using controlled leak, drain-back, tilt and splash tests. No fill quantity or charging procedure is approved yet.

<b>Intended control behaviour:</b> WATER requests one bounded timed dose; release does not stop an active dose. The proposed STOP control or LAMP TEST cancels it. The knob is sampled at dose start. Moisture is advisory; there is no automatic watering. These describe the review firmware, not validated delivered-kit operation; the pump is currently disabled and LCD text is not implemented.

<b>After commissioning:</b> check water and tube condition before each supervised use. Keep electronics dry. Disconnect power before lifting the planter, cleaning, or touching the pump. Empty before moving and support the entire base.

<b>Cleaning:</b> remove soil debris from both drains and pump inlet, rinse removable wet parts as compatible with their material, and dry before reassembly. Do not immerse the tower. Cleaning chemicals and water temperature limits need material qualification.

<b>Faults:</b> no flow - disconnect and inspect intake/tube/water level; leakage - disconnect, empty and inspect the wet body; intermittent power - stop and inspect the approved supply/harness; tight planter - remove debris and check cable routing, never lever against the tower.

<b>Build record:</b> serial/build ID __________  Date __________<br/>Component revisions __________  Dry checks __________<br/>Electrical acceptance __________  Leak/fill evidence __________<br/>Dose calibration __________  Inspector __________

Supplier release items still required: final BOM and harness map, verified control labels/software, maximum fill and dose range, material/care limits, product support and warranty details.