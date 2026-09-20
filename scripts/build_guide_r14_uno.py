"""Build the controlled R14 Uno assembly manual using repository evidence."""
from pathlib import Path
import hashlib
import json
import shutil
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pdf/Plant_Station_R14_Uno_Assembly_Manual.pdf'
REF = ROOT / 'docs/r14_uno_reference'
REPO = 'https://github.com/skyhigh6/esp32-plant-station'
BASE = REPO + '/blob/main/'
NAVY = colors.HexColor('#163345')
TEAL = colors.HexColor('#167d8d')
PALE = colors.HexColor('#eef4f6')
INK = colors.HexColor('#263845')
WIRE = {'red':'#bf2834','black':'#263238','orange':'#bc6200','blue':'#2469b2',
        'yellow':'#947200','green':'#23824b','violet':'#7d4da0','white':'#667581','brown':'#805337','grey':'#65727d'}
STYLE = ParagraphStyle('body',fontName='Helvetica',fontSize=10,leading=14,textColor=INK)
SMALL = ParagraphStyle('small',parent=STYLE,fontSize=8.4,leading=11.5)
HEAD = ParagraphStyle('head',parent=STYLE,fontName='Helvetica-Bold',fontSize=13,leading=17,textColor=NAVY)
W,H = 595.28,841.89
story=[]

def p(text): return ('p',text)
def h(text): return ('h',text)
def note(text): return ('note',text)
def pic(path,height,caption): return ('pic',path,height,caption)
def table(headers,rows,widths): return ('table',headers,rows,widths)
def diagram(kind,height): return ('diagram',kind,height)
def page(title,*items): story.append((title,items))
def link(label,path): return f'<link href="{BASE+path}" color="#167d8d">{label}</link>'

page('R14 UNO | Assembly manual',
 p('PLANT STATION / PLANT-AM-R14-UNO / Issue A / 20 September 2026'),
 pic('mechanical/concept_rev14_uno/preview.png',320,'R14 tower and Uno mounting geometry. Actual CAD view; electronics omitted.'),
 h('Mechanical assembly, wiring and commissioning'),
 p('A workshop manual for junior engineers assembling one Arduino Uno R3 plant station. Includes the complete mechanical sequence, component schedule, numbered harness drawings and test records.'),
 note('<b>Build status:</b> mechanical prototype and motor-disabled bench electronics. This finished manual does not certify a finished watering appliance. Actual fit, pump power/driver selection and wet acceptance remain open.'),
 p('Geometry: R14 tower with retained R13 fascia, roof and planter. Mechanical documentation baseline: R14-D2. Electrical reference: saved PlantUno bench v2 source.'),
 p(f'<b>Files and updates:</b> <link href="{REPO}" color="#167d8d">{REPO}</link>'))

page('01 | Read first and obtain the files',
 table(['Pages','Use'],[['3-4','BOM and incoming inspection'],['5-9','Incoming inspection, fit trials and mechanical assembly'],['10-14','Uno orientation, wiring diagrams and wire schedule'],['15','Future pump circuit - design hold'],['16-17','Firmware and dry commissioning'],['18-19','Wet acceptance, care and build record'],['20','Evidence, sources and revision control']],[65,450]),
 h('Download the controlled configuration'),
 p('Open the repository above, choose <b>Code &gt; Download ZIP</b>, extract it, and record the commit from the repository history. Do not print every STL in the repository; older revisions remain for traceability.'),
 p(link('R14 tower, coupon and STEP files','mechanical/concept_rev14_uno/README.md')+'<br/>'+link('Retained R13 parts','mechanical/concept_rev13/README.md')+'<br/>'+link('Complete mechanical review archive','Plant_Station_R14_Uno_Review.zip')+'<br/>'+link('This assembly manual','output/pdf/Plant_Station_R14_Uno_Assembly_Manual.pdf')+'<br/>'+link('Bench firmware snapshot used by this manual','docs/r14_uno_reference/PlantUno/PlantUno.ino')),
 note('<b>Excluded:</b> the purchased panel USB-C breakout is not fitted or wired. Adding it later requires a separate enclosure/print and electrical revision. The Uno\'s existing onboard USB socket remains the bench programming/power connection.'),
 p('<b>Terms:</b> confirmed = supported by inspected files or test evidence; reported = user record; proposed = selected here but not physically qualified; unknown = inspect or measure before use. A drawing connection applies only after the component matches its stated type.'))

page('02 | BOM - printed parts and fasteners',
 table(['ID / qty','Part / source','Specification and disposition'],[
 ['M01 / 1','R14 tower_sump_body_uno.stl','Integrated tower, sump and holder saddle; 207 x 100 x 158 mm.'],
 ['M02 / 1','R13 fascia_charcoal.stl','LCD, three nominal 12 mm buttons, 7 mm pot bore.'],
 ['M03 / 1','R13 top_cover_sage.stl','Retained roof; assembled height approximately 161 mm.'],
 ['M04 / 1','R13 planter_sage.stl','Retained planter, two drains and service reliefs.'],
 ['M05 / 1','R13 selected knob STL','Choose round or D shaft after measurement; print one variant.'],
 ['T01 / 1','R14 uno_mount_fit_coupon.stl','Mandatory board registration and pilot trial.'],
 ['T02 / as needed','R13 fit coupons','LCD, button, knob, piezo/LED and upper boss coupons. Do not use carrier coupon for Uno.'],
 ['F01 / 4','Uno screws','M3 candidate; length/head/thread process selected by trial. Pilot 2.8 mm x 11 mm deep.'],
 ['F02 / 8','Fascia + roof screws','4 each; 3 x 8 mm plastic thread-forming is provisional. Verify actual engagement.'],
 ['F03 / 4 sets','LCD screws and nuts','M2.5 x 16 mm provisional; head <=5.5 mm. Verify stack and thread projection.'],
 ['F04 / 4 sets','Component nuts/washers','Three buttons and one potentiometer; supplied matching hardware.'],
 ['F05 / 1','Holder cable tie, optional','4.8 x 1.5 mm provisional; tunnel 6 x 2.5 mm. No cell fitted.'],
 ],[62,175,278]),
 p('<b>Purchased hardware evidence:</b> Photo 2 shows an M2/M2.5/M3 button-head screw, Nyloc nut and washer listing, plus a 2.2-6.0 mm plastic self-tapping screw listing. The selected sizes, lengths and quantities are not visible. Sort and measure the delivered parts; listing ranges are not fit specifications.'),
 note('Machine screws and plastic thread-forming screws are different systems. Do not force an M3 machine screw into an unqualified printed pilot. A Nyloc nut is not used behind a blind tower boss. No separate battery-tray or hose-clip screws are required.'))

page('03 | BOM - electronics and consumables',
 table(['ID / qty','Component','Build requirement / evidence'],[
 ['U1 / 1','Arduino Uno R3','Classic 5 V ATmega328P; actual clone/board markings to record. Not Uno R4.'],
 ['DS1 / 1','16 x 2 I2C LCD','Existing QAPASS/PCF8574 assumed; verify labels and 5 V rating. Saved v2 LCD test passed.'],
 ['SEN1 / 1','Capacitive soil probe','Existing v1.2 reported; verify 3.3 V operation and pin order.'],
 ['RV1 / 1','Linear potentiometer','10 kOhm proposed if purchasing; verify actual resistance, shaft and terminals.'],
 ['SW1-3 / 3','Illuminated panel switches','Photos show red, green and yellow ring listings. Diameter, momentary/latching option and ring voltage unknown.'],
 ['LED1-3 / 3','Low-current indicator LEDs','Reference circuit: red lockout, blue dose, green ready. Separate LEDs unless ring ratings are verified.'],
 ['R1-3 / 3','1 kOhm resistors','One per bare LED; 0.25 W adequate for this circuit.'],
 ['PS1 / 1','Uno USB data/power lead','Match actual onboard socket. Dry bench supply only; no external 5 V injection.'],
 ['P1 / 1','DC pump','3.3 V reported; actual label, current, outlet and envelope to verify. Leave disconnected.'],
 ['DRV1 / 1 set','Pump driver and supply','Not selected; MOSFET, diode, gate resistors, fused regulated supply and disconnect required. See p15.'],
 ['BZ1 / 1','10 mm case sounder','Type/current/height unconfirmed; no connection in this issue.'],
 ['BAT1 / optional','18650 holder/power system','Mechanical provision only. Cell, charger/protection and power path not released.'],
 ['C01 / as needed','Harness and wet-side items','Insulated wire, labels, connectors, heatshrink, edge protection, strain relief, measured tubing, drain screens; compatible sealing material if needed.'],
 ],[67,155,293]),
 p('Use approximately 0.2-0.35 mm2 flexible insulated wire for short low-current bench signal runs. Motor wire, supply rating and fuse depend on measured current. Label both ends of every wire; colours alone are insufficient.'),
 note('Bought does not mean electrically identified. Do not connect the unknown illuminated rings, sounder, cell or motor to an Uno pin. The USB-C panel module is deliberately omitted from this BOM.'))

page('04 | Incoming inspection and tools',
 h('Tools and preparation'),
 p('Use callipers, a multimeter with continuity and DC-voltage ranges, hand screwdrivers, small spanners, cutters, wire stripper, suitable crimp/solder tools and heatshrink. Keep the bench dry. Disconnect USB and all supplies before handling wiring. Use a current-limited supply for future motor characterisation.'),
 table(['Check','Method','Pass / action'],[
 ['Switch action','Meter on unpowered contact pair; operate and release.','Normally open at rest; closed only while pressed. Latching switches do not meet the current interface.'],
 ['Switch contacts vs ring','Use supplier terminal drawing and meter; identify COM/NO/NC and LED +/-.','Record labels. Use COM/NO only; insulate NC. Do not identify lamp wires by colour alone.'],
 ['Ring rating','Read selected order details, markings or matching supplier data.','Record voltage, current, polarity and any internal resistor. Leave isolated until known.'],
 ['Panel fit','Measure barrel, nut, rear projection and pot bushing.','Trial coupon and fascia without forcing; nominal button bore 12 mm.'],
 ['Fasteners','Measure diameter/under-head length; identify thread family.','Trial on coupon. Record engagement and positive bottoming clearance.'],
 ['LCD and probe','Read module labels, supply ratings and connector order.','Follow labels, not the apparent order in a generic diagram.'],
 ['Board and cables','Record board revision; inspect underside and plug envelope.','All four Uno holes register; USB insertion and service access verified.'],
 ],[98,192,225]),
 note('Hold point HP1: do not print the complete tower until the Uno coupon and screw-fit trials pass. Do not energise any unidentified module. Record failures rather than modifying parts until they appear to fit.'))

page('05 | Fit and mount the Arduino Uno',
 pic('mechanical/concept_rev14_uno/mount_section.png',245,'R14 exported-mesh mount sections. Nominal dimensions; print fit remains to be checked.'),
 p('<b>1.</b> Print the Uno coupon at 100% scale in the intended process. Offer it to the PCB underside with its screw-test boss facing away. All four 3.2 mm gauge holes must register without board bending.'),
 p('<b>2.</b> Trial screw/thread preparation in the 2.8 mm coupon pilot. Its boss is 8 mm high: use a short trial screw. It does not reproduce the tower\'s 11 mm blind depth.'),
 p('<b>3.</b> Inspect the full tower print: roots sound, support removed, pilots clear, seating faces coplanar and wet/dry divider undamaged. Record printer, material, scale, orientation, layer height and supports.'),
 p('<b>4.</b> Insert the Uno through the front with fascia and roof removed. Components face the fascia; USB faces left. PCB underside seats at y76; rear wall y94 gives 18 mm nominal rear clearance.'),
 p('<b>5.</b> Fit four qualified screws. Engagement = under-head length minus measured PCB/washer stack. Keep engagement below 11 mm with positive bottoming margin. Hand-tighten; no torque is qualified. Check all supports contact without bowing.'),
 note('HP2: check screw heads, solder joints, headers, USB/power plugs and cable removal with the fascia in place. The retained side aperture was designed for the earlier carrier; direct Uno USB access is not established by the mount geometry.'))

page('06 | Assemble the wet-side routes',
 pic('mechanical/concept_rev13/cable_section.png',270,'Retained R13 service-riser geometry; unchanged by the R14 mount revision.'),
 p('<b>6.</b> Inspect sump floor and walls for cracks/pinholes. Remove print debris and clear both planter drains. Trial the pump, leaving it electrically disconnected. The CAD reference envelope is 38.5 x 25.5 x 43 mm; it is not the measured 3.3 V pump.'),
 p('<b>7.</b> Feed the water tube through the 10 mm bore at x123/y92. Keep the tube outside the electronics cavity. Actual tube OD, connector size, bend radius and outlet retention must be checked; the old separate hose clip is not used.'),
 p('<b>8.</b> Route the two isolated pump leads through the separate 8 mm bore at x110/y92 and the crossover into the tower. Keep leads free from abrasion and moving/removed parts. Insulate both ends pending driver selection.'),
 p('<b>9.</b> Trial the planter through its full insertion/removal travel. Fit removable debris guards without blocking the two drains. Provide enough slack to service the pump and planter without pulling connections.'),
 note('No water during electrical assembly. The sump rim at z60 is not a fill mark. Printed passages are not sealed glands; no maximum fill volume has been qualified.'))

page('07 | Sensor route and fascia components',
 pic('mechanical/concept_rev13/sensor_entry_section.png',205,'Retained sensor entry: diameter 8 mm, centre y65/z64; lower edge z60.'),
 p('<b>10.</b> Route the probe lead through the sensor entry and matching planter relief. Add suitable edge protection and strain relief. Leave a service loop; keep the probe electronics above the wetting/soil limit for the actual sensor.'),
 p('<b>11.</b> Mount the LCD on the fascia rear: reference centres 75 x 31 mm, aperture 71.4 x 24.6 mm. Trial four M2.5 screws/nuts; avoid board bow and conductor contact. Verify backpack depth and access to the contrast trimmer.'),
 p('<b>12.</b> Fit the identified momentary buttons and potentiometer using supplied nuts/washers. Match actual parts to the 12 mm and 7 mm nominal bores. Fit the selected knob with at least 0.5 mm axial clearance.'),
 p('<b>13.</b> For the existing firmware, label WATER and LAMP TEST. The third switch is SPARE / NOT ACTIVE; do not label it STOP while USE_STOP=false. Switch colour does not establish its function.'),
 p('<b>14.</b> Fit separate reference LEDs or retain ring wires insulated pending identification. Red=lockout, blue=dose request and green=ready are the software meanings. Yellow purchased ring is not an automatic electrical substitute for blue.'),
 note('Keep the unidentified sounder disconnected. If fitting an empty insulated holder, route a tie through the 6 x 2.5 mm saddle tunnel before installing it; leave the cell out. Battery operation is outside this issue.'))

page('08 | Harness installation and closure',
 pic('mechanical/concept_rev13/fascia_rear.png',220,'Retained fascia CAD. Component bodies and harness must be checked on the actual build.'),
 p('<b>15.</b> Build the harness on the bench using pages 10-14. Number both ends W01 onward and label components U1, DS1, SEN1, RV1 and SW1/SW2. Use insulated distribution terminals for shared 5 V, 3.3 V and ground; do not stuff multiple bare ends into an Uno socket.'),
 p('<b>16.</b> Verify each wire against the schedule with power off. Confirm no crossed supply rails, no uninsulated joints, correct LED polarity/resistors and correct COM/NO switch contacts. Tug-test terminations gently.'),
 p('<b>17.</b> Complete dry bench commissioning with the assembly open. Then disconnect power, arrange service loops and retain the harness away from screw tips, wet openings and sharp edges.'),
 p('<b>18.</b> Offer up the fascia and fit four qualified screws. Refit the roof with four screws. Hand-tighten only. Ensure cables cannot be pinched between mating faces.'),
 p('<b>19.</b> Fit and remove the planter again. Check both drains, tube bend, sensor lead, pump leads, USB access and cover seating. Photograph the internal routing before final closure.'),
 note('HP3: all dry mechanical and electrical checks must pass before closing the assembly. Power remains USB bench power; no motor, external supply, battery or panel USB-C connection is included.'))

page('09 | Uno R3 orientation and terminal map',
 diagram('board',345),
 p('Simplified top view with the onboard USB socket at the left. Header order is shown for orientation; spacing and board outline are schematic. Verify the printed pin labels on the actual Uno/clone before connecting.'),
 table(['Terminal','Connection'],[['5V / GND','LCD and pot supply / common return'],['3.3V / A0 / A1','Probe supply / probe output / pot wiper'],['A4 / A5','LCD SDA / SCL; not digital D4 / D5'],['D2 / D3','WATER / LAMP TEST normally-open contacts'],['D5 / D6 / D7','Red / blue / green reference LED via individual 1 kOhm resistor'],['D4 / D8 / D9','Unused STOP / sounder reserve / motor reserve; leave disconnected']],[115,400]),
 p('The dedicated SDA/SCL header duplicates A4/A5; use one connection set. D0/D1 remain free for USB serial. Use the Uno\'s onboard USB connector for this bench configuration. See official pinout source S1 on p20.'))

page('10 | Wiring drawing E01 - LCD and analogue',
 diagram('analogue',335),
 h('Read the drawing'),
 p('Each horizontal line is one physical wire. Wire ID is the primary identifier; colour is secondary. Separate GND wires join at a common insulated ground distribution point connected to Uno GND. Component terminal positions are functional, not a claim about connector order.'),
 p('<b>LCD:</b> VCC=5 V, GND=ground, SDA=A4, SCL=A5. Check the backpack labels. Adjust contrast only after successful I2C initialisation. No ESP32 level shifter is used in this 5 V Uno/5 V backpack arrangement.'),
 p('<b>Probe:</b> verify the actual module works at 3.3 V. VCC=3.3 V, GND=ground, AOUT=A0. Keep its output within the Uno input range and never connect an unknown 5 V output to the 3.3 V supply terminal.'),
 p('<b>Pot:</b> outer terminals to 5 V/GND, wiper to A1. Identify the wiper with a meter. Swap only the two outer leads if clockwise decreases the setting. This prototype has no validated open-wiper fail-low circuit.'),
 note('Orange is 3.3 V; red is 5 V. Never bridge these rails. The probe is the only proposed 3.3 V load; measure its current and check the actual board capacity before energising.'))

page('11 | Wiring drawing E02 - controls and LEDs',
 diagram('controls',320),
 p('<b>Switch detail:</b> W11 goes to SW1 COM and W12 returns SW1 NO to GND; W13/W14 do the same for SW2. COM and NO may be interchanged electrically. A four/five-terminal illuminated switch has a separate lamp circuit: do not bridge it to the contact pair.'),
 p('<b>LED detail:</b> D5/D6/D7 each feeds its own 1 kOhm resistor, then the LED anode (+). Each cathode (-) returns to GND. The resistor may physically sit at either end of its series branch; never omit it for a bare LED.'),
 p('At 5 V, 1 kOhm limits each bare-LED branch to less than 5 mA, even before LED forward voltage is considered. This is a low-current indication circuit; brightness is not yet qualified.'),
 note('<b>Purchased rings:</b> keep isolated until their rated voltage/current and internal resistor are known. A 12 V ring is not powered from 5 V, and an unknown ring is not driven directly by GPIO. If the rings need a driver, issue a revised drawing. The red/green/yellow purchases do not establish the red/blue/green reference LED circuit.'),
 p('SW3 and its lamp remain spare. LAMP TEST cancels the simulated dose; a three-press gesture also enters diagnostics. There is no active dedicated STOP button in the supplied bench snapshot.'))

page('12 | Wire schedule - power and analogue',
 table(['Wire / colour','From','To','Check'],[
 ['W01 / red','U1 5V via +5V terminal','DS1 VCC','5 V-rated LCD only'],['W02 / black','Ground terminal','DS1 GND','Common ground'],
 ['W03 / blue','U1 A4','DS1 SDA','Not D4'],['W04 / yellow','U1 A5','DS1 SCL','Not D5'],
 ['W05 / orange','U1 3.3V','SEN1 VCC','Module rating verified'],['W06 / black','Ground terminal','SEN1 GND','Verify module label'],
 ['W07 / green','SEN1 AOUT','U1 A0','Analogue output'],['W08 / red','+5V terminal','RV1 high outer','Check direction'],
 ['W09 / black','Ground terminal','RV1 low outer','Check direction'],['W10 / violet','RV1 wiper','U1 A1','Variable 0-5 V'],
 ['W21 / red','U1 5V','+5V distribution terminal','Feeds W01 and W08'],['W22 / black','U1 GND','Ground distribution terminal','Feeds all return wires'],
 ],[102,135,146,132]),
 h('Harness conventions'),
 p('E01/E02 show logical nets. W21 and W22 are the physical feeder wires to the shared distribution terminals. Each branch has its own numbered conductor. Do not put a component in series with another component\'s ground return.'),
 p('Fit a removable connector where servicing requires it, with matching labels on both halves. Record connector pin order in the build record; no connector family or cavity assignment is implied here. Keep sensor signal and I2C runs short and separated from future motor-current wiring.'),
 note('Before USB connection, disconnect unknown modules and check for wiring shorts with the meter. Electronic circuits can show changing resistance while capacitors charge; investigate a persistent near-zero supply-to-ground reading. Do not use resistance/continuity mode on a powered circuit.'))

page('13 | Wire schedule - controls and indicators',
 table(['Wire / colour','From','To','Function'],[
 ['W11 / white','U1 D2','SW1 COM','WATER input'],['W12 / black','SW1 NO','Ground terminal','WATER return'],
 ['W13 / grey','U1 D3','SW2 COM','LAMP input'],['W14 / black','SW2 NO','Ground terminal','LAMP return'],
 ['W15 / red','U1 D5','R1 1 kOhm -> LED1 anode','Red lockout'],['W16 / black','LED1 cathode','Ground terminal','LED1 return'],
 ['W17 / blue','U1 D6','R2 1 kOhm -> LED2 anode','Blue dose request'],['W18 / black','LED2 cathode','Ground terminal','LED2 return'],
 ['W19 / green','U1 D7','R3 1 kOhm -> LED3 anode','Green ready'],['W20 / black','LED3 cathode','Ground terminal','LED3 return'],
 ],[102,134,166,113]),
 p('Each W15/W17/W19 identifier covers its wired series branch to the resistor. Mount the resistor adjacent to the LED and sleeve the resistor-to-anode joint; label the branch ends. Each LED return remains separately numbered.'),
 table(['Reserved terminal','Issue A disposition'],[['D4','No wire; USE_STOP=false. SW3 is spare, not a safety stop.'],['D8','No wire; unidentified sounder left disconnected.'],['D9','No wire in the bench harness; MOTOR_ENABLED=false keeps output LOW.'],['VIN / barrel / external 5V','No external supply connection in this build.'],['Panel USB-C / cell','Excluded. No connection to any supply rail.']],[145,370]),
 note('White/grey wire must still carry its W-number because colour discrimination is not an acceptance method. Supplier lead colours do not override the verified terminal identity. Keep spare leads individually insulated.'))

page('14 | Future pump driver - design hold',
 diagram('pump',280),
 p('E03 is a complete circuit concept, not an instruction to energise the present pump. The pump is reported as 3.3 V, but its actual identity, startup/stall current and duty limits are unknown. Select parts only after those measurements and matching datasheets are available.'),
 table(['Future ID','Connection / selection criterion'],[['W30 brown','D9 -> 100-220 Ohm gate resistor -> Q1 gate.'],['W31 black','Uno GND -> motor supply GND / Q1 source; shared reference.'],['W32 red','Regulated 3.3 V supply + -> fuse/disconnect -> motor +.'],['W33 black','Motor - -> Q1 drain. Motor return must not flow through an Uno header.'],['Q1 / RPD','Logic-level N-MOSFET specified at 4.5/5 V gate drive, adequate current/thermal rating; 47-100 kOhm gate-to-source pull-down.'],['D1','Flyback diode: cathode/band to motor +, anode to drain; rated for actual current and supply.']],[98,417]),
 note('Do not power the motor from Uno 3.3V, 5V or GPIO. Keep MOTOR_ENABLED=false until the driver, regulated supply, fuse, disconnect, default-OFF behaviour and flow tests have passed. USB-powered Uno and the separate motor supply share GND only; do not join positive rails.'),
 p('An independent power disconnect is required. Software timeout cannot stop a shorted MOSFET or guarantee recovery from a processor hang. Battery/charging design remains a separate configuration decision.'))

page('15 | Firmware installation and operation',
 p('The manual carries a frozen copy of the existing local bench v2 source in <b>docs/r14_uno_reference/PlantUno/</b>. It includes PlantUno.ino, PlantController.h and PlantView.h. No firmware behaviour was changed for this manual; source SHA-256 values are recorded in the adjacent evidence manifest.'),
 p('<b>20.</b> Keep all three files in the PlantUno folder. Install Arduino IDE/CLI and the Arduino AVR Boards package. Select Arduino Uno / ATmega328P and the detected port, not Uno R4. Install <b>hd44780 by Bill Perry</b> using Library Manager; it is not bundled here.'),
 p('<b>21.</b> With only the identified dry bench harness connected, compile and upload through the onboard USB socket. Disconnect the motor and all future supplies. Open serial at 115200 baud. Expect PlantUno bench v2 and LCD initialisation status=0.'),
 p('<font face="Courier" size="8">arduino-cli compile --fqbn arduino:avr:uno<br/>  docs/r14_uno_reference/PlantUno</font><br/>CLI command shown wrapped; enter it as one line. Choose the actual port explicitly for upload.'),
 table(['Control / indication','Bench v2 behaviour'],[['WATER','One simulated 0-5000 ms dose per press; knob sampled at start. Releasing WATER does not cancel. No automatic watering.'],['LAMP TEST','Cancels dose and illuminates reference LEDs. Release required before re-arm.'],['Triple LAMP','Three debounced presses within 1.2 s toggle VIEW; repeat to leave. WATER inhibited in VIEW.'],['VIEW display','Probe raw/relative moisture, pot raw/percent and WATER/LAMP states.'],['Normal display','Relative moisture, Ready MOTOR OFF, TEST dose, LAMP TEST or release instruction.'],['Moisture calibration','Dry=447, settled wet=221; clamped relative index. Not volumetric water content. Recalibrate for changed soil/probe.']],[120,395]),
 note('Default: USE_STOP=false; MOTOR_ENABLED=false. Do not enable the motor simply by changing the constant. Historical v1 LCD fault evidence is superseded only for the saved v2 bench run, not for your newly assembled unit.'))

page('16 | Dry commissioning - record every result',
 table(['Test','Method','Acceptance'],[
 ['E01','Power off; inspect every wire against schedule.','No crossed rails; all joints insulated; unknown modules isolated.'],
 ['E02','Uno + LCD first; power via onboard USB.','Stable supply; serial starts normally; LCD status=0 and steady readable text.'],
 ['E03','Remove power; add probe. Repower and observe VIEW.','Raw reading changes plausibly with probe condition. Record dry/wet values; protect electronics from water.'],
 ['E04','Remove power; add pot. Repower; sweep fully.','Raw approximately 0-1023, monotonic; clockwise increases. Record actual endpoints.'],
 ['E05','Add switches/LEDs with power off, then test.','Released WATER/LAMP=0; pressed=1. Lamp test lights all three reference indicators.'],
 ['E06','Set pot midrange, press WATER, keep held.','Single simulated dose; no repeat while held. Release/repress required.'],
 ['E07','Start simulated dose, then press LAMP.','Request cancels; release lockout clears after stable release.'],
 ['E08','Triple LAMP; attempt WATER; exit VIEW.','VIEW toggles; no dose in VIEW; release required on exit.'],
 ['E09','Measure D9 to GND during boot, WATER and LAMP.','LOW throughout normal bench tests; no motor connected.'],
 ['E10','Close after disconnecting; check routing and access.','No pinch/strain; all covers seat; planter removable; USB accessible.'],
 ],[45,225,245]),
 h('Fault isolation'),
 p('<b>LCD fault:</b> power off, verify GND/5V/A4/A5 and backpack labels. A contrast adjustment cannot repair an I2C bus fault. For resets/flashing backlight, inspect supply and watch for repeated startup messages.<br/><b>Input always pressed:</b> check COM/NO and latching variant.<br/><b>LED dark:</b> check polarity, resistor and correct pin.<br/><b>Pot/probe erratic:</b> check ground, wiper/output contact and connector identity.'),
 note('HP4: save the serial log, measured rail values, wire check and photographs. Any failure stays open until corrected and retested. Prior bench evidence does not accept the installed harness.'))

page('17 | Wet acceptance, operation and care',
 h('Proceed only after the pump design hold is closed'),
 p('<b>22.</b> Establish the actual pump rating, driver/supply/fuse selection, electrical isolation/strain relief, default-OFF tests and a controlled test procedure. Reassess switch functions and a clear stop/disconnect method before enabling delivery.'),
 p('<b>23.</b> Leak-test the wet assembly with electronics removed or positively isolated. Use a catch tray and inspect all seams, riser routes and sensor entry. No fill volume is prescribed: determine and record a limit below unsealed entries, allowing for drain-back, splash and handling.'),
 p('<b>24.</b> Check both drains and pump inlet remain clear with the chosen soil/guards. Verify that stopped flow does not siphon water into the planter or electronics. Correct the outlet arrangement if siphoning occurs.'),
 p('<b>25.</b> Under supervision, calibrate volume versus run time at the installed lift and tube route using a measured vessel. Record repeatability and the selected maximum dose. Do not label the knob in millilitres from elapsed time alone.'),
 p('<b>26.</b> Record wet-test results and reviewer disposition. Until complete, operate only in motor-disabled dry bench mode. No unattended-operation claim is made.'),
 h('Routine use after acceptance'),
 p('Check water level, intake, tube security and dry electronics before each supervised use. There is no reservoir-level interlock; prevent dry running by inspection and the pump\'s rated limits. Moisture indication is advisory. Repeated WATER presses can overwater.'),
 h('Cleaning and service'),
 p('Disconnect all power before lifting the planter or touching wiring/pump. Empty before moving; support the entire base. Clear both drains and intake screens. Clean only with materials and temperatures compatible with the actual print/coating. Never immerse the electronics tower.'),
 note('Leakage, unexpected pump running, hot wiring or repeated resets: disconnect power, contain/empty water, record the defect and investigate. A software stop is not electrical isolation.'))

page('18 | Build and acceptance record',
 p('Complete for each physical assembly. Attach photographs, serial logs, measurements and any non-conformance record. A blank entry is not a pass.'),
 table(['Record','Value / evidence reference'],[
 ['Build ID / date / engineer','________________________________________________'],['Git commit / manual issue','________________________________________________'],['Printer / material / slicer / job','________________________________________________'],['Board / LCD / probe variants','________________________________________________'],['Switch size / action / lamp rating','________________________________________________'],['Fasteners / thread process','________________________________________________'],['Coupon / screw-fit evidence','________________________________________________'],['PCB engagement / bottoming margin','________________________________________________'],['USB / component minimum gaps','________________________________________________'],['Harness / connector revision','________________________________________________'],['Measured 5 V / 3.3 V rails','________________________________________________'],['Dry tests E01-E10 / evidence','________________________________________________'],['Firmware source hash / upload log','________________________________________________'],['Pump / driver / supply / fuse','________________________________________________'],['Leak / fill / siphon / flow evidence','________________________________________________'],['Open defects / restrictions','________________________________________________'],['Disposition / reviewer / date','________________________________________________'],
 ],[220,295]),
 p('<b>Current disposition at issue:</b> geometry digitally checked; actual fit and installed tests open. Pump, sounder, battery and illuminated-ring integration not electrically released. Panel USB-C excluded.'),
 p('Any geometry or electrical change needs updated drawings, source identity and relevant repeated tests. Retain the original record; add a dated correction with the reason and affected part/wire/test IDs.'))

page('19 | Evidence, sources and revision control',
 table(['Ref','Basis / limit'],[
 ['E1','R14 verification.json and independent_mesh_check.json: digital CAD/STEP and mesh evidence; no physical qualification. Independent mesh check rerun 20 Sep 2026, PASS.'],
 ['E2','R13 retained geometry and kit drawings: tube/wire routes, fascia, planter and holder saddle. Carrier mounting instructions superseded by R14.'],
 ['E3','PlantUno bench v2 source and 15 Sep 2026 serial log: LCD status=0, lcd=OK, motor=OFF over saved five-second readback. Does not prove full commissioning.'],
 ['E4','User purchase screenshots supplied 20 Sep 2026: red/green/yellow ring-switch listings, mixed machine hardware and plastic screw listings. Selected variants not visible. Screenshots not reproduced or published.'],
 ['S1','Arduino Uno R3 official pinout and board documentation, checked 20 Sep 2026. Used to cross-check labels, 5 V logic and duplicate SDA/SCL.'],
 ['S2','Bill Perry / duinoWitchery hd44780 library documentation, checked 20 Sep 2026. Install separately; library licence GPL-3.0.'],
 ],[35,480]),
 p('<link href="https://docs.arduino.cc/resources/pinouts/A000066-full-pinout.pdf" color="#167d8d">S1: Official Arduino Uno R3 full pinout</link><br/><link href="https://docs.arduino.cc/hardware/uno-rev3/" color="#167d8d">S1: Arduino Uno R3 board documentation</link><br/><link href="https://github.com/duinoWitchery/hd44780" color="#167d8d">S2: hd44780 library source and documentation</link>'),
 p(link('R14 acceptance register','mechanical/concept_rev14_uno/ACCEPTANCE.md')+'<br/>'+link('Source snapshot and evidence hashes','docs/r14_uno_reference/evidence_manifest.json')),
 h('Issue history'),
 p('<b>Issue A, 20 September 2026:</b> complete Uno assembly manual; R14/R13 configuration consolidated, wire colours/numbers assigned, purchased-part inspection added, bench v2 evidence reconciled. Original functional wiring diagrams created for this manual; diagrams are not photographs or exact component pin-layout drawings.'),
 note('The manual is complete for the documented configuration. Open engineering decisions are explicit because no defensible voltage rating, purchased variant, pump current, physical fit or wet acceptance can be inferred from a listing image or a CAD pass.'))

def text(c,x,y,s,size=9,color=INK,bold=False):
 c.setFillColor(color); c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x,y,s)

def box(c,x,y,w,h,label,fill=PALE):
 c.setFillColor(fill);c.setStrokeColor(TEAL);c.roundRect(x,y,w,h,5,fill=1,stroke=1)
 text(c,x+9,y+h-18,label,10,NAVY,True)

def wire(c,x1,x2,y,label,colour):
 c.setStrokeColor(colors.HexColor(WIRE[colour]));c.setLineWidth(1.8);c.line(x1,y,x2,y)
 c.setFillColor(colors.HexColor(WIRE[colour]));c.circle(x1,y,2,fill=1,stroke=0);c.circle(x2,y,2,fill=1,stroke=0)
 text(c,x1+8,y+5,label,8,INK)

def draw_diagram(c,kind,x,y,w,height):
 if kind=='board':
  bx,by=x+30,y+75;bw=455;bh=195
  box(c,bx,by,bw,bh,'UNO R3 / ATmega328P',colors.HexColor('#d7edef'))
  box(c,bx-20,by+95,58,42,'USB',colors.HexColor('#e6e7e8'))
  box(c,bx-10,by+18,60,34,'DC IN',colors.HexColor('#e6e7e8'))
  box(c,bx+155,by+68,180,42,'ATmega328P',colors.HexColor('#ccd3d6'))
  top=['SCL','SDA','AREF','GND','13','12','11','10','9','8','7','6','5','4','3','2','1','0']
  bottom=['NC','IOREF','RESET','3.3V','5V','GND','GND','VIN','A0','A1','A2','A3','A4','A5']
  for labels,yy,step,start,up in [(top,by+bh-6,22,bx+51,True),(bottom,by+7,27,bx+65,False)]:
   for i,label in enumerate(labels):
    xx=start+i*step;c.setFillColor(NAVY);c.rect(xx-3,yy-3,6,6,fill=1,stroke=0)
    c.saveState();c.translate(xx,yy+(13 if up else -13));c.rotate(90 if up else -90);text(c,0,0,label,8);c.restoreState()
  text(c,x+30,y+12,'READ BOARD LABELS: not to scale; top view, USB left.',9,NAVY,True)
 elif kind in ['analogue','controls']:
  if kind=='analogue':
   rows=[('5V','W01 red','VCC / DS1 LCD','red'),('GND','W02 black','GND / DS1 LCD','black'),('A4','W03 blue','SDA / DS1 LCD','blue'),('A5','W04 yellow','SCL / DS1 LCD','yellow'),('3.3V','W05 orange','VCC / SEN1 probe','orange'),('GND','W06 black','GND / SEN1 probe','black'),('A0','W07 green','AOUT / SEN1 probe','green'),('5V','W08 red','High outer / RV1 pot','red'),('GND','W09 black','Low outer / RV1 pot','black'),('A1','W10 violet','Wiper / RV1 pot','violet')]
  else:
   rows=[('D2','W11 white','SW1 COM / WATER','white'),('GND','W12 black','SW1 NO / WATER','black'),('D3','W13 grey','SW2 COM / LAMP','grey'),('GND','W14 black','SW2 NO / LAMP','black'),('D5','W15 red','R1 1k -> LED1 + red','red'),('GND','W16 black','LED1 -','black'),('D6','W17 blue','R2 1k -> LED2 + blue','blue'),('GND','W18 black','LED2 -','black'),('D7','W19 green','R3 1k -> LED3 + green','green'),('GND','W20 black','LED3 -','black')]
  box(c,x,y+7,95,height-14,'U1 UNO R3');box(c,x+300,y+7,215,height-14,'COMPONENT TERMINALS')
  step=(height-56)/len(rows)
  for i,(pin,label,dest,col) in enumerate(rows):
   yy=y+height-48-i*step;text(c,x+15,yy-3,pin,9,NAVY,True)
   wire(c,x+95,x+300,yy,label,col);text(c,x+309,yy-3,dest,8.5)
 else:
  # Functional circuit with explicit connections; dot junctions only.
  box(c,x+5,y+187,155,53,'3.3 V MOTOR SUPPLY')
  box(c,x+345,y+155,155,77,'P1 MOTOR')
  box(c,x+345,y+55,155,70,'')
  text(c,x+350,y+134,'Q1 N-MOSFET',10,NAVY,True)
  text(c,x+355,y+197,'+');text(c,x+355,y+167,'-')
  text(c,x+355,y+110,'DRAIN');text(c,x+355,y+91,'GATE');text(c,x+355,y+72,'SOURCE')
  wire(c,x+160,x+345,y+207,'W32 red / fuse + disconnect','red')
  c.setStrokeColor(INK);c.line(x+335,y+170,x+335,y+113);c.line(x+305,y+170,x+345,y+170);c.line(x+335,y+113,x+345,y+113)
  c.line(x+305,y+207,x+305,y+195);c.line(x+305,y+181,x+305,y+170)
  c.setFillColor(colors.white);c.rect(x+299,y+181,12,14,fill=1,stroke=1)
  c.setLineWidth(2);c.line(x+299,y+193,x+311,y+193);c.setLineWidth(1)
  text(c,x+215,y+184,'D1 / band up',8)
  text(c,x+192,y+151,'W33 motor - to drain',8)
  box(c,x+5,y+71,114,49,'UNO D9')
  wire(c,x+119,x+345,y+94,'W30 / 100-220 Ohm','brown')
  c.setFillColor(colors.white);c.setStrokeColor(INK);c.rect(x+166,y+90,27,8,fill=1,stroke=1)
  c.setStrokeColor(INK);c.line(x+275,y+94,x+275,y+32);c.line(x+85,y+32,x+460,y+32);c.line(x+460,y+32,x+460,y+55)
  c.line(x+60,y+71,x+60,y+32);c.line(x+60,y+32,x+85,y+32)
  text(c,x+18,y+76,'GND',8)
  c.line(x+5,y+195,x-8,y+195);c.line(x-8,y+195,x-8,y+32);c.line(x-8,y+32,x+60,y+32)
  text(c,x+14,y+192,'GND',8)
  c.setFillColor(colors.white);c.rect(x+270,y+43,10,29,fill=1,stroke=1);text(c,x+167,y+50,'RPD 47-100k',8)
  text(c,x+10,y+17,'W31 black: Uno GND + supply GND + source common',8,NAVY,True)
  text(c,x+10,y+257,'D1 FLYBACK: across motor + and drain',10,NAVY,True)
  # Separate diode annotation tied to exact nodes, avoiding ambiguous crossings.
  text(c,x+10,y+244,'Cathode (band) -> motor +; anode -> motor - / drain',9)
  text(c,x+10,y+137,'Concept only - NOT FITTED',9,TEAL,True)

def build():
 OUT.parent.mkdir(parents=True,exist_ok=True)
 c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle('Plant Station R14 Uno - Complete Assembly Manual');c.setAuthor('Plant Station Engineering')
 for n,(title,items) in enumerate(story,1):
  c.setFillColor(NAVY);c.rect(0,H-105,W,105,fill=1,stroke=0)
  text(c,40,H-34,'PLANT STATION     /     ENGINEERING ASSEMBLY SERIES',9,colors.white,True)
  text(c,40,H-72,title,21,colors.white,True)
  yy=H-124
  for item in items:
   kind=item[0]
   if kind in ['p','h','note']:
    st=HEAD if kind=='h' else STYLE
    para=Paragraph(item[1],st);pad=10 if kind=='note' else 0
    _,hh=para.wrap(515-pad*2,700)
    if kind=='note':
     c.setFillColor(PALE);c.roundRect(40,yy-hh-20,515,hh+20,4,fill=1,stroke=0)
    para.drawOn(c,40+pad,yy-hh-pad);yy-=hh+pad*2+10
   elif kind=='pic':
    path=ROOT/item[1];iw,ih=ImageReader(str(path)).getSize();scale=min(515/iw,item[2]/ih)
    dw,dh=iw*scale,ih*scale;c.drawImage(str(path),40+(515-dw)/2,yy-dh,dw,dh,mask='auto');yy-=dh+5
    para=Paragraph(item[3],SMALL);_,hh=para.wrap(515,80);para.drawOn(c,40,yy-hh);yy-=hh+13
   elif kind=='table':
    data=[[Paragraph(escape(str(t)),SMALL) for t in row] for row in [item[1]]+item[2]]
    t=Table(data,colWidths=item[3]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#d5e6eb')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),1,TEAL)]))
    _,hh=t.wrap(515,700);t.drawOn(c,40,yy-hh);yy-=hh+12
   elif kind=='diagram':
    draw_diagram(c,item[1],40,yy-item[2],515,item[2]);yy-=item[2]+12
   if yy<53: raise RuntimeError(f'Page {n} overflow at {yy:.1f}: {title}')
  c.setStrokeColor(TEAL);c.setLineWidth(.6);c.line(40,43,555,43)
  text(c,40,28,'PLANT-AM-R14-UNO  |  Issue A  |  20 Sep 2026',8)
  c.drawRightString(555,28,f'{n:02d} / {len(story):02d}')
  c.bookmarkPage(f'p{n}');c.addOutlineEntry(title,f'p{n}',0);c.showPage()
 c.save()
 # Markdown companion preserves the authored instructions and schedule.
 md=[]
 for title,items in story:
  md.append('# '+title)
  for it in items:
   if it[0] in ['p','h','note']:md.append(it[1])
   elif it[0]=='pic':md.append(f'![{it[3]}](../{it[1]})')
   elif it[0]=='table':md.append('\n'.join([' | '.join(it[1]),' | '.join(['---']*len(it[1]))]+[' | '.join(r) for r in it[2]]))
   elif it[0]=='diagram':md.append('See vector wiring drawing in PDF: '+it[1])
 (ROOT/'docs/Plant_Station_R14_Uno_Assembly_Manual.md').write_text('\n\n'.join(md),encoding='utf-8',newline='\n')
 print(f'Created {OUT}: {len(story)} pages')

if __name__=='__main__':
 build()
