from pathlib import Path
import json, math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.utils import ImageReader
ROOT=Path(__file__).resolve().parents[1]; CAD=ROOT/'mechanical/concept_rev5'
OUT=ROOT/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
c=canvas.Canvas(str(OUT/'Plant_Station_R5_Illustrated_Build_Guide.pdf'),pagesize=(595.28,841.89))
c.setTitle('Plant Station R5 - Illustrated build and commissioning guide')
c.setAuthor('Kev / Plant Station project')
ink=HexColor('#263631');sage=HexColor('#80947d');grey=HexColor('#edf0eb');amber=HexColor('#8c5d16')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=10,leading=14,textColor=ink)
page_no=0

def text(t,x,y,w=507,size=10):
    st=ParagraphStyle('p',parent=style,fontSize=size,leading=size*1.4)
    p=Paragraph(t,st);_,h=p.wrap(w,800);p.drawOn(c,x,y-h);return y-h-10

def page(title,subtitle):
    global page_no
    if page_no:c.showPage()
    page_no+=1;c.setFillColor(ink);c.setFont('Helvetica-Bold',20);c.drawString(44,790,title)
    text(subtitle,44,770,size=9)
    c.setStrokeColor(sage);c.line(44,738,551,738)
    c.setFont('Helvetica',8);c.setFillColor(ink);c.drawString(44,26,'PLANT STATION | R5 | 09 September 2026 | Provisional hardware fit')
    c.drawRightString(551,26,str(page_no))

def pic(path,x,y,w,h):
    c.drawImage(str(path),x,y,width=w,height=h,preserveAspectRatio=True,anchor='c',mask='auto')

def table(rows,y,widths):
    data=[[Paragraph(str(v),ParagraphStyle('cell',parent=style,fontSize=9,leading=12)) for v in row] for row in rows]
    t=Table(data,colWidths=widths,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),grey),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),.3,sage)]));_,h=t.wrap(507,700);t.drawOn(c,44,y-h);return y-h-14

def box(label,x,y,w=130,h=48):
    c.setFillColor(grey);c.setStrokeColor(sage);c.roundRect(x,y,w,h,5,fill=1,stroke=1);text(label,x+8,y+h-9,w-16,9)

def arrow(x1,y1,x2,y2,label=None):
    c.setStrokeColor(ink);c.setLineWidth(1);c.line(x1,y1,x2,y2)
    a=math.atan2(y2-y1,x2-x1)
    for d in (-.45,.45):c.line(x2,y2,x2-6*math.cos(a+d),y2-6*math.sin(a+d))
    if label:text(label,(x1+x2)/2+4,(y1+y2)/2+12,140,8)

def code(lines,y):
    c.setFillColor(grey);c.rect(44,y-14*len(lines)-18,507,14*len(lines)+18,fill=1,stroke=0)
    c.setFillColor(ink);c.setFont('Courier',8)
    for i,line in enumerate(lines):c.drawString(53,y-15-i*14,line)
    return y-14*len(lines)-33

page('Plant Station','Illustrated build guide | Mechanical R5 / existing manual-dose firmware')
pic(CAD/'concept_reference.png',44,360,507,350)
y=text('<b>Design reference</b> - supplied concept art: sage enclosure, charcoal fascia and sump, left-hand electronics tower, removable planter and service covers.',44,350)
y=text('R5 follows that arrangement while retaining the user-measured LCD and PCB interfaces. The art is not a dimensional drawing. Camera optics, decorative vents and automatic watering shown in the art are not implemented features.',44,y)
y=text('<b>What this guide covers:</b> seven printed parts, mount clearances, assembly order, functional pinout, wiring blocks, compile/upload procedure and staged acceptance.',44,y)
text('<b>Release status:</b> CAD and mesh checks passed. Actual carrier pinout, component fit, slicing, fastener pull-out, leak testing and hardware operation remain unverified. This is a complete guide to the current prototype configuration, not a declaration of a finished working product.',44,y)

page('01 / Parts and assembly','Actual CAD exports, shown exploded; positions here are intentionally separated.')
pic(CAD/'exploded.png',44,350,507,380)
table([['Part / file stem','Purpose'],['tower_sage / fascia_charcoal','Dry housing and removable LCD/control panel'],['top_cover_sage','Removable screw-down top cover'],['sump_charcoal / planter_sage','Lower reservoir and two-drain planting insert'],['battery_tray / hose_clip','Insulated holder support and external tube retention']],340,[220,287])
text('STLs retain their common assembly coordinates. Load together without auto-arranging to inspect fit. For printing, load each part separately, orient it and place its lowest face on the build plate. Do not print the complete assembled model as a fused object.',44,120)

page('02 / Mount geometry and clearance','All dimensions in mm. LCD and carrier centres are user measured; component envelopes are assumed.')
# Front datum diagram, scaled x/z geometry.
ox,oy,k=62,390,1.8
c.setStrokeColor(sage);c.setFillColor(grey);c.roundRect(ox,oy,96*k,158*k,10,fill=1,stroke=1)
c.setFillColor(white);c.rect(ox+13*k,oy+100*k,70*k,25*k,fill=1,stroke=1)
for x,z in [(11.5,97.5),(84.5,97.5),(11.5,127.5),(84.5,127.5)]:
    c.circle(ox+x*k,oy+z*k,2.5*k,fill=0);c.circle(ox+x*k,oy+z*k,1.2*k,fill=0)
for x,z in [(18,80),(78,80),(18,135),(78,135)]:
    c.setStrokeColor(amber);c.circle(ox+x*k,oy+z*k,4*k,fill=0)
text('Front projection<br/><b>Sage:</b> LCD mounts<br/><b>Amber:</b> rear PCB mounts',267,683,275)
text('LCD aperture: 70 x 25<br/>LCD centres: 73 x 30<br/>LCD bosses: OD 5 / bore 2.4<br/>LCD stand-off: 8 behind fascia<br/><br/>PCB centres: 60 x 55<br/>PCB bosses: OD 8 / pilot 2.8<br/>PCB face: y = 76<br/>Rear cavity wall: y = 94',267,615,275)
text('Datum: x right, y rear, z up.<br/>Tower front/bottom/left = 0.<br/>Nominal assembly envelope:<br/><b>207 x 100 x 161</b>',267,440,275)
table([['Check','Nominal result'],['LCD boss / 4 mm screw head to aperture','0.415 / 0.915 minimum'],['LCD boss radial wall','1.3 around 2.4 bore'],['PCB driver access / rear stand-off','7 diameter / 18 clear to rear wall'],['Assumed PCB / LCD edge to side wall','4 / 2'],['Assumed LCD-to-PCB component gap','20.8'],['Fascia edge / sump locating-lip fit gap','0.4 nominal each']],365,[280,227])
text('LCD uses provisional M2 through-bolts, head diameter at most 4 mm, without oversized washers near the aperture. Verify actual mounting-hole size and head dimensions. The small boss-to-aperture margin makes a fascia fit coupon essential.',44,106,size=9)

page('03 / Internal layout and fasteners','Section removes the front half; actual underside components and cable connectors need measuring.')
pic(CAD/'section.png',44,355,507,370)
y=text('<b>Envelope checks used:</b> PCB 76 x 67, thickness 1.6 and 20 front projection. LCD 80 x 36, thickness 1.6 and 20 rear projection. These are explicitly assumed keep-out volumes; both clear the printed parts. Check protrusions under the PCB separately.',44,345)
y=table([['Location','Provisional fitting / check'],['4 LCD mounts','M2 through-bolts + nuts; 2.4 bore. Select length from 11 mm panel/boss stack + actual PCB + nut engagement.'],['4 PCB mounts','2.8 blind pilot, 11 depth; select screw for actual board bore. Do not bottom out or enlarge into the rear wall.'],['4 fascia / 4 top cover','3.4 clearance holes; 2.8 pilots. Top cover pilot depth 7; fascia depth 9. Test thread engagement in a coupon.'],['2 holder pads / 1 hose clip','2.8 pilot; holder pads have 5 blind depth, hose shelf 3. Measure screw protrusion before tightening.']],y,[135,372])
text('No heat-set inserts are specified in R5. Do not use earlier revision insert instructions. Printed screw retention and installation torque are untested; tighten only enough to seat, without bowing a board.',44,y,size=9)

page('04 / Mechanical build sequence','Dry fit first. Retain access to every fastener and keep the wet and dry modules separable.')
y=720
steps=[('1. Inspect and prepare','Print mount/dovetail trial sections before full parts. Slice each STL in mm; inspect layer preview for unsupported bosses, bridged holes and the hollow planter skirt. Material, printer and support settings are not yet specified.'),('2. Inspect the prints','Remove supports; verify clear bores and two unobstructed 6 mm floor drains. Check the 4 mm sump floor, seams and locating lip. Deburr mating surfaces without changing measured hole centres.'),('3. Prove hardware fit','Offer the real PCB to all four 60 x 55 mounts without force. Check screw/tool access, underside components and USB cable/strain relief. Fit the LCD to all four 73 x 30 mounts and verify aperture and screw-head clearance.'),('4. Fit dry electronics','With all power isolated, fit the insulated cell holder to its tray and secure the tray to the floor pads. Fit the PCB through the open front. Leave the cell disconnected. Driver/translator/sounder mount details await actual module dimensions; never leave them loose.'),('5. Populate the fascia','Fit the LCD to its rear bosses, then the three buttons, three LEDs and dose potentiometer. Route labelled wiring with service slack. Control cutouts are provisional: 12, 5 and 7 mm respectively. The sounder grille is only an aperture, not a finished module mount.'),('6. Join wet module','Remove planter. Raise the sump relative to the tower; engage both open-top female dovetails over the tower rails, then lower onto the stops. Do not force the 0.4 mm nominal sliding fits. This is not a positively locked carrying joint.'),('7. Fit pump and tubing','Fit a removable filtered pump using its manufacturer-approved retention. Route tube/cable through the rear 12 mm service notch outside the soil bowl. The clip bore is 7 mm nominal; measure tube OD. Keep water tubing external, with no penetration into the dry tower.'),('8. Close and inspect','Seat the planter lip, then attach fascia and top cover after wiring tests. Check cables are not pinched, outlets remain above maximum reservoir level and all service parts can be removed. Carry using support beneath both modules, not by the tower alone.')]
for title,body in steps:y=text('<b>'+title+'</b><br/>'+body,44,y)

page('05 / System block diagrams','Functional architecture; signal lines do not indicate a physical connector location.')
box('Known regulated supply',44,651,150);box('Verified board power input',231,651,140);box('ESP32 controller',411,651,140)
arrow(194,675,231,675);arrow(371,675,411,675)
box('Fused pump branch + disconnect',44,540,150);box('MOSFET driver + suppression',231,540,140);box('5 V pump / wet sump',411,540,140)
arrow(119,651,119,588);arrow(194,564,231,564);arrow(371,564,411,564);arrow(481,651,301,588,'logic only')
box('Buttons + dose pot + soil input',44,425,150);box('Manual dose controller',231,425,140);box('LEDs / LCD translator / sounder driver',411,425,140)
arrow(194,449,231,449);arrow(371,449,411,449)
text('Electrical: use a controlled common ground. Pump power is a separate load branch; it must not flow through an ESP32 GPIO or 3.3 V rail. Supply protection and wire sizes depend on measured startup current.',44,397)
box('Pump + inlet filter',44,292,145);box('Secured tube / outlet above fill level',224,292,150);box('Soil compartment',409,292,142)
arrow(189,316,224,316);arrow(374,316,409,316)
box('Lower sump',224,191,150);arrow(480,292,374,215,'two 6 mm drains');arrow(224,215,116,292,'recirculation')
text('Water: the planting cavity is 90 x 60 x 50 with exactly two floor drains. Debris screens must remain removable. Determine fill level and drain-back capacity with the actual pump installed. No level/flow sensor or dry-run protection is provided.',44,157)
text('18650 power path: unresolved. The printed tray accepts an insulated holder; it does not establish cell chemistry, charging compatibility, protection or 5 V regulation.',44,88,size=9)

page('06 / Pinout illustration','LOGICAL COMPILE-REVIEW MAP ONLY - not the SunFounder physical header pinout.')
box('Classic ESP32\nreview profile',212,373,171,308)
left=[('GPIO34','Soil analogue in'),('GPIO35','Dose pot wiper'),('GPIO32','WATER to GND'),('GPIO33','LAMP TEST to GND'),('GPIO13','STOP to GND'),('GPIO21','I2C SDA')]
right=[('GPIO25','Pump driver gate'),('GPIO26','Red LED + resistor'),('GPIO27','Blue LED + resistor'),('GPIO14','Green LED + resistor'),('GPIO23','Sounder driver'),('GPIO22','I2C SCL')]
for i,((pin,label),(pin2,label2)) in enumerate(zip(left,right)):
    yy=634-i*43
    text(label,44,yy+9,150,9);arrow(180,yy,212,yy);text(pin,220,yy+9,70,9)
    text(pin2,310,yy+9,70,9);arrow(383,yy,408,yy);text(label2,416,yy+9,136,9)
text('Numbers above are GPIO identifiers, not connector positions. SDA/SCL are bidirectional. GPIO13/14 may conflict with JTAG; camera/SD/flash/PSRAM and onboard functions may reserve these and other pins.',44,342)
y=table([['Power / signal interface','Requirement'],['3.3 V / GND','Pot ends to 3.3 V/GND; all input levels verified within 0-3.3 V.'],['LCD SDA / SCL','Use suitable bidirectional translation if backpack pulls up to 5 V.'],['Pump / sounder','External rated driver only. Pump and sounder disabled by default.'],['Actual SunFounder board','Revision, header order and every reserved net UNKNOWN. Do not wire from this illustration.']],274,[155,352])
text('Before replacing this page with a physical pinout: photograph both sides and silkscreen, record the exact board revision, obtain its schematic, identify pin 1/orientation and reconcile all 12 required GPIO functions with reserved nets.',44,y,size=9)

page('07 / Wiring details','Reference circuits are provisional until the exact component ratings and board map are closed.')
box('+5 V pump branch',44,658,160);box('Pump motor',240,658,120);box('Drain (D) / MOSFET',412,658,139)
arrow(204,682,240,682);arrow(360,682,412,682)
box('Verified GPIO',44,546,130);box('100-220 ohm series',211,546,145);box('Gate (G)',413,546,138)
arrow(174,570,211,570);arrow(356,570,413,570)
text('Flyback diode across motor: <b>cathode to +5 V</b>, anode to drain. MOSFET source to common GND. Gate pull-down: provisional 47-100 kohm to GND. Select MOSFET with specified low resistance at 3.3 V gate drive; verify actual package G/D/S order.',44,517)
y=table([['Circuit','Build / test detail'],['Buttons','Normally open switches to GND; internal pull-ups. Confirm WATER, LAMP TEST and proposed STOP labels against wiring.'],['LEDs','Separate series resistor for each LED; initial 1 kohm is provisional. Check polarity and measured current.'],['Dose potentiometer','Ends to 3.3 V and GND, wiper to ADC. Select wiper bias after measuring pot resistance; test open-wiper behaviour with pump isolated.'],['Soil sensor','Verify supply rating and measure analogue output before connecting ADC. Calibrate in this soil and pot.'],['LCD','Identify PCF8574 mapping, I2C address and pull-up rail. Use correct level translation. Firmware currently probes only; no display text routine exists.'],['Sounder / auxiliary boards','Identify active/passive type and current, then select driver and suppression as required. Secure all modules with insulating mounts after measuring their envelopes.']],445,[130,377])
text('USB access remains a provisional rear 18 x 14 opening. Actual connector position and cable approach are unverified. Keep motor wiring clear of analogue signal wiring and reserve accessible strain relief; the current CAD does not supply a fitted cable gland.',44,y,size=9)

page('08 / Firmware preparation and compile','Windows / PowerShell. Compile-only review is permitted; actual carrier wiring is still unresolved.')
y=text('1. Open PowerShell in the project root. Install Arduino CLI or use the executable bundled with Arduino IDE. Record the CLI path, ESP32 core version and board target. The package was recompiled on 09 September using core <b>2.0.17</b>.',44,718)
y=code(['$cli = "$env:LOCALAPPDATA\\Programs\\Arduino IDE\\resources\\app"', '$cli += "\\lib\\backend\\resources\\arduino-cli.exe"', '& $cli version', '& $cli core list', '& $cli board list'],y)
y=text('2. If the ESP32 core is absent, install it using Espressif\'s Boards Manager instructions [1]. Use the recorded 2.0.17 baseline to reproduce this review, or record and revalidate any different version. Do not select a generic target for the supplied carrier without checking its module and flash/PSRAM options.',44,y)
y=text('3. Compile the existing review profile. Run from the project root. This flag explicitly selects the isolated classic ESP32 review map; it does not approve that map for the SunFounder carrier.',44,y)
y=code(['$sketch = "firmware\\arduino\\PlantEsp32ManualPump"', '$flags = "-DPLANT_BOARD_PROFILE_CLASSIC_DEVKIT_WROOM32_REVIEW_ONLY"', '& $cli compile --fqbn esp32:esp32:esp32 `', '  --libraries firmware\\libraries `', '  --build-property "compiler.cpp.extra_flags=$flags" `', '  --output-dir firmware\\build\\review $sketch', 'if ($LASTEXITCODE -ne 0) { throw "Compile failed" }'],y)
y=text('<b>Recorded compile:</b> 272,957 bytes flash; 21,944 bytes global RAM. No upload was performed. Core control tests were previously recorded as passed; this turn recompiled the unchanged sketch.',44,y)
y=text('<b>Current firmware limits:</b> pump gated by PLANT_HARDWARE_ENABLE=0. Sounder is disabled unless explicitly enabled. LCD update is empty; the probe path also lacks Wire.begin initialisation. Enabling the LCD flag alone will not produce a working display.',44,y)
text('The sketch deliberately fails compilation if no explicit board profile is selected. Before operating the supplied carrier, implement and review a carrier-specific profile or prove the existing map is valid for that exact board. Even with pump disabled, the sketch configures several other GPIOs as outputs.',44,y)

page('09 / Upload and first connection','Conditional procedure for a verified target. The current SunFounder carrier has not passed this gate.')
y=720
for title,body in [('1. Release the board map','Confirm module identity, carrier revision, flash/PSRAM settings and every assigned GPIO. Update the source/profile and recompile if any differ. Do not upload the classic review binary to the unverified camera carrier.'),('2. Isolate the loads','Keep pump and battery disconnected. Use a known USB data cable and approved board USB input. Remove or isolate peripherals that conflict with programming pins according to the board documentation.'),('3. Identify the live port','Run board list before and after connecting USB. Select the newly identified port; do not reuse the historical Uno COM8 assignment. Close Serial Monitor and other applications holding the port.')]:y=text('<b>'+title+'</b><br/>'+body,44,y)
y=code(['& $cli board list', '$port = Read-Host "Verified board COM port"', '$fqbn = Read-Host "Verified target FQBN used for compilation"', '# Use ONLY binaries compiled for that verified board/profile.', '& $cli upload --port $port --fqbn $fqbn `', '  --input-dir firmware\\build\\review `', '  firmware\\arduino\\PlantEsp32ManualPump', 'if ($LASTEXITCODE -ne 0) { throw "Upload failed" }'],y)
y=text('4. Arduino CLI upload does not compile first [2]. Confirm the input directory contains the build just verified. If connection fails, check data cable, port and the exact board bootloader procedure; some ESP32 boards need BOOT held during connection [1]. Do not guess carrier switch settings.',44,y)
y=code(['& $cli monitor --port $port --config baudrate=115200'],y)
y=text('5. Expected serial banner: <b>ESP32 plant manual pump scaffold</b>, then hardware output DISABLED and LCD adapter disabled. Periodic fields: t_ms, soil_raw, pump_request, pump_applied, lamp_test, locked and dose_ms.',44,y)
text('Accept only if pump_applied remains false with the default build. With verified controls connected, exercise STOP and lamp test and inspect state changes. A successful upload proves programming only; it does not prove pin mapping, LCD operation or safe pump switching.',44,y)

page('10 / Commissioning and acceptance','Record measured results. Blank fields are intentionally unverified, not implied passes.')
y=table([['Test / stage','Acceptance criterion / record'],['CAD configuration - PASS','7 single closed positive-volume meshes; 21 pair intersections zero; mounting/access probes passed. See verification.json and STL hashes.'],['Mechanical dry fit','All mounts seat without force; screws do not bottom out; no PCB bow, component contact or pinched cables. Actual measured clearances: __________'],['Dry controls','WATER requests one timed dose; release does not cancel. STOP or LAMP TEST cancels on next loop. Held controls do not repeat; release all for 35 ms before re-arming.'],['Dose control','Pot sampled only at dose start; provisional range 0-5000 ms. Zero dose requests no output. Open-wiper behaviour verified: __________'],['Electrical bench','Verify gate LOW at reset/boot, supply rails, startup current and driver temperature with rated test load before pump. Measurements: __________'],['Wet containment','Electronics removed: leak-test sump and all relevant joints over a controlled observation period. Check drains, inlet screen, maximum fill and drain-back. Duration/result: __________'],['Wet dose calibration','With supervised pump tests, measure volume at several short durations using installed lift/tube. Repeat and record variation; reduce initial cap. Duration is not yet ml.'],['Maintenance','Clean screen/drains; inspect tube retention and cable insulation. Confirm STOP and power disconnect before each supervised session.']],720,[150,357])
y=text('<b>Unclosed release items:</b> exact board pinout; pump/holder/button/sounder/USB envelopes; screw and material selection; slicer review; waterproofing; LCD implementation; battery/charging compatibility; real-soil and delivered-volume calibration.',44,y)
y=text('<b>References checked 09 September 2026</b><br/>[1] <link href="https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html" color="#315f77">Espressif Arduino-ESP32 installation and board selection</link><br/>[2] <link href="https://docs.arduino.cc/arduino-cli/commands-reference/arduino-cli_upload" color="#315f77">Arduino CLI upload reference</link><br/>[3] <link href="https://docs.arduino.cc/arduino-cli/getting-started" color="#315f77">Arduino CLI compile, port detection and upload workflow</link>',44,y,size=9)
text('Local authority: mechanical/concept_rev5/build.py and verification.json; firmware/arduino/PlantEsp32ManualPump/PlantEsp32ManualPump.ino; docs/PROJECT_CONTROL.md. The R5 package supersedes earlier mechanical fit/insert guidance, while preserving measured dimensions and unresolved hardware questions.',44,y,size=9)
c.save();print(OUT/'Plant_Station_R5_Illustrated_Build_Guide.pdf')
