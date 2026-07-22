# -*- coding: utf-8 -*-
"""AET Academy Reference Library - practical quick-reference cheat sheets.
Authored HTML bodies (trusted content) rendered raw. Categories drive filter chips."""

REF_CATS = [
    ("elec",  "\u26a1 Electrical"),
    ("motor", "\U0001f504 Motors & Drives"),
    ("wire",  "\U0001f50c Wiring & Code"),
    ("sensor","\U0001f4e1 Sensors & Signals"),
    ("plc",   "\U0001f4df PLC & Logic"),
    ("pid",   "\U0001f39b\ufe0f Process & PID"),
    ("fluid", "\U0001f4a8 Fluid Power"),
    ("net",   "\U0001f310 Networks"),
    ("safety","\U0001f6e1\ufe0f Safety"),
    ("instr", "\U0001f321\ufe0f Instrumentation"),
    ("test",  "\U0001f527 Test & Troubleshooting"),
    ("conv",  "\U0001f4d0 Conversions"),
]

def T(rows, head=None):
    h = "<table class='reftab'>"
    if head:
        h += "<thead><tr>" + "".join("<th>%s</th>" % c for c in head) + "</tr></thead>"
    h += "<tbody>"
    for r in rows:
        h += "<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>"
    return h + "</tbody></table>"

REFERENCE = [
 # ---------- Electrical ----------
 {"cat":"elec","title":"Ohm's Law &amp; Power Wheel","body":
   "<p>The four core quantities relate through V, I, R, P:</p>" +
   T([["V = I &times; R","Voltage (volts)"],
      ["I = V / R","Current (amps)"],
      ["R = V / I","Resistance (ohms)"],
      ["P = V &times; I","Power (watts)"],
      ["P = I&sup2; &times; R","Power from current"],
      ["P = V&sup2; / R","Power from voltage"]], ["Formula","Solves for"]) +
   "<p class='reftip'>Tip: cover the unknown in the V-I-R triangle to find its formula.</p>"},
 {"cat":"elec","title":"Three-Phase Power","body":
   T([["Line vs Phase (Wye)","V_line = &radic;3 &times; V_phase ; I_line = I_phase"],
      ["Line vs Phase (Delta)","V_line = V_phase ; I_line = &radic;3 &times; I_phase"],
      ["Apparent power","S = &radic;3 &times; V_L &times; I_L  (VA)"],
      ["Real power","P = &radic;3 &times; V_L &times; I_L &times; PF  (W)"],
      ["&radic;3","1.732"]]) },
 {"cat":"elec","title":"Series vs Parallel Circuits","body":
   T([["Resistance","Series: R = R1+R2+... ; Parallel: 1/R = 1/R1+1/R2+..."],
      ["Current","Series: same through all ; Parallel: divides"],
      ["Voltage","Series: divides ; Parallel: same across all"],
      ["Two parallel R","R = (R1&times;R2)/(R1+R2)"]]) },
 {"cat":"elec","title":"Voltage Drop (rule of thumb)","body":
   "<p>Keep branch-circuit drop under 3%, total under 5% (NEC recommendation).</p>" +
   T([["Single phase","VD = (2 &times; K &times; I &times; L) / CM"],
      ["Three phase","VD = (1.732 &times; K &times; I &times; L) / CM"],
      ["K (copper)","12.9 &nbsp; K (aluminum) 21.2"],
      ["L","one-way length in feet ; CM = circular mils of conductor"]]) },
 {"cat":"elec","title":"AC vs DC &amp; RMS","body":
   T([["RMS","V_rms = V_peak / &radic;2 = V_peak &times; 0.707"],
      ["Peak","V_peak = V_rms &times; 1.414"],
      ["Peak-to-peak","V_pp = 2 &times; V_peak"],
      ["US line","120 V_rms = ~170 V_peak ; 60 Hz"]]) },

 # ---------- Motors & Drives ----------
 {"cat":"motor","title":"Synchronous Speed &amp; Slip","body":
   T([["Sync speed","Ns = (120 &times; f) / poles  (RPM)"],
      ["60 Hz, 2-pole","3600 RPM ; 4-pole 1800 ; 6-pole 1200 ; 8-pole 900"],
      ["Slip","% slip = (Ns - Nrotor) / Ns &times; 100"],
      ["Typical slip","2-5% at full load for standard induction motors"]]) },
 {"cat":"motor","title":"HP, kW &amp; Motor Current","body":
   T([["HP to kW","kW = HP &times; 0.746"],
      ["kW to HP","HP = kW / 0.746"],
      ["3-phase FLA (approx)","I = (HP &times; 746) / (1.732 &times; V &times; PF &times; eff)"],
      ["Rule of thumb 460V 3ph","~1.25 A per HP"],
      ["Rule of thumb 230V 3ph","~2.5 A per HP"]]) },
 {"cat":"motor","title":"VFD V/Hz &amp; Basics","body":
   T([["Constant torque","Maintain V/Hz ratio (e.g. 460V/60Hz = 7.67)"],
      ["Above base speed","Constant HP, field weakening, torque falls"],
      ["Carrier freq","Higher = quieter motor, more drive heat"],
      ["Accel/Decel","Ramp times limit current &amp; mechanical shock"],
      ["Braking","DB resistor or regen for fast decel of high inertia"]]) },
 {"cat":"motor","title":"Wye vs Delta Motor Connections","body":
   T([["Wye (star)","Lower starting current, ~58% of delta voltage per winding"],
      ["Delta","Full voltage/torque, higher current"],
      ["Wye-Delta start","Start in wye (reduced), switch to delta at speed"],
      ["Dual-voltage 9-lead","Series = high V (e.g. 460) ; Parallel = low V (230)"]]) },

 # ---------- Wiring & Code ----------
 {"cat":"wire","title":"Copper Wire Ampacity (60/75/90C, approx)","body":
   T([["14 AWG","15 / 20 / 25 A"],
      ["12 AWG","20 / 25 / 30 A"],
      ["10 AWG","30 / 35 / 40 A"],
      ["8 AWG","40 / 50 / 55 A"],
      ["6 AWG","55 / 65 / 75 A"],
      ["Note","NEC 310.16, derate for temp/fill. Always verify against code."]], ["AWG","Ampacity"]) },
 {"cat":"wire","title":"US Conductor Color Codes","body":
   T([["120/208/240V","Black, Red, Blue (phases)"],
      ["277/480V","Brown, Orange, Yellow (phases)"],
      ["Neutral","White (120/240) or Gray (277/480)"],
      ["Ground","Green, green/yellow, or bare"],
      ["DC","Red = +, Black = - (common convention)"]]) },
 {"cat":"wire","title":"Grounding vs Bonding","body":
   T([["Grounding","Connection to earth; reference &amp; lightning/surge path"],
      ["Bonding","Joining metal parts to create a low-impedance fault path"],
      ["EGC","Equipment grounding conductor carries fault current to trip breaker"],
      ["Why","A properly bonded fault path lets overcurrent devices open fast"]]) },
 {"cat":"wire","title":"Control Panel Wire Practices","body":
   "<ul class='reflist'><li>Separate power and signal wiring; cross at 90&deg;</li>" +
   "<li>Use ferrules on stranded conductors into terminals</li>" +
   "<li>Wire duct fill max ~60%; leave slack for service</li>" +
   "<li>Label both ends of every conductor</li>" +
   "<li>Shielded cable: ground shield at ONE end only (usually panel)</li></ul>"},

 # ---------- Sensors & Signals ----------
 {"cat":"sensor","title":"4-20 mA Scaling","body":
   "<p>Convert a 4-20 mA loop to engineering units:</p>" +
   T([["EU","= ((mA - 4) / 16) &times; (span) + min"],
      ["mA","= ((EU - min) / span) &times; 16 + 4"],
      ["% signal","= ((mA - 4) / 16) &times; 100"],
      ["Why 4 mA zero","Live zero detects broken wire (0 mA = fault)"]]) },
 {"cat":"sensor","title":"Signal Types","body":
   T([["4-20 mA","Analog, noise-immune, live-zero, most common"],
      ["0-10 V","Analog, simple, sensitive to voltage drop/noise"],
      ["Discrete","On/off, 24 VDC typical in industrial"],
      ["PWM / freq","Duty cycle or pulse rate (flow, encoders)"],
      ["Digital bus","IO-Link, HART, fieldbus - carries data + diagnostics"]]) },
 {"cat":"sensor","title":"Sinking (NPN) vs Sourcing (PNP)","body":
   T([["PNP (sourcing)","Switches +V to the load; load to common. Common in NA/EU"],
      ["NPN (sinking)","Switches load to ground/common; +V to load"],
      ["Input card","Match sensor type: sourcing sensor needs sinking input"],
      ["Memory aid","PNP = Positive switched, Pushes current to input"]]) },
 {"cat":"sensor","title":"Common Sensor Technologies","body":
   T([["Inductive","Metal targets, short range, rugged"],
      ["Capacitive","Any material incl liquids/powders"],
      ["Photoelectric","Through-beam, retro, diffuse; long range"],
      ["Ultrasonic","Distance, works on clear/shiny targets"],
      ["Proximity vs photo","Prox = near metal; photo = light-based, longer"]]) },

 # ---------- PLC & Logic ----------
 {"cat":"plc","title":"Ladder Logic Cheat-Sheet","body":
   "<p><b>Read a rung left-to-right:</b> power starts at the left rail and must find a continuous path through the contacts to energize the coil (output) on the right rail.</p>"
   + T([["&#8739;&#8739; XIC (NO)","Examine-If-Closed / normally-open contact. Passes power when its bit is <b>TRUE</b> (device actuated)."],
        ["&#8815; XIO (NC)","Examine-If-Open / normally-closed contact. Passes power when its bit is <b>FALSE</b>. Used for Stop PBs, E-stops, overloads."],
        ["( ) OTE","Output energize coil. ON only while the rung is true."],
        ["TON","On-delay timer. Times up while the rung is true; sets a Done (DN) bit at preset. Resets when the rung goes false."],
        ["CTU","Count-up counter. Adds 1 on each false&rarr;true (rising) edge; sets DN at preset. Needs a separate reset rung."]], ["Instruction","What it does"])
   + "<p><b>Series = AND, parallel = OR.</b> Contacts in a row must <i>all</i> pass (AND). Contacts stacked in branches give an <i>either/or</i> path (OR).</p>"
   + "<p><b>Seal-in (3-wire) pattern:</b> a momentary Start contact is OR&rsquo;d with a contact off the coil&rsquo;s own bit; once the coil energizes, its own contact &lsquo;seals&rsquo; power around Start. A series NC Stop (and NC overload) drops it:</p>"
   + "<pre class='ladascii'>  |  Start   Stop   OL          |\n  +--] [--+--]/[---]/[---( Motor )\n  |        |                    |\n  +-]Motor[+                    |</pre>"
   + "<p><b>Troubleshoot a dead output:</b> 1) Put the rung in its should-run state. 2) Trace power left-to-right to the <u>first contact that is open</u> &mdash; that is your suspect. 3) A contact with no field device you can toggle (tripped OL, blown fuse) is a field fault, not an HMI/logic fix. 4) If the rung looks true but the machine ignores a button, suspect a <b>wrong address / crossed wire</b> &mdash; toggle the input and confirm the contact actually changes.</p>"
   + "<p style='color:var(--txt2);font-size:.9rem'>&#128161; Practice all of this live in <b>Lab Simulators &rarr; PLC Ladder Logic</b> (seal-in, TON, CTU, safety interlock, 3 fault challenges, and a build-your-own sandbox).</p>" },
 {"cat":"plc","title":"Common PLC Data Types","body":
   T([["BOOL","1 bit, TRUE/FALSE"],
      ["INT","16-bit signed (-32768..32767)"],
      ["DINT","32-bit signed integer"],
      ["REAL","32-bit floating point"],
      ["WORD/DWORD","16/32-bit unsigned bit collections"],
      ["STRING","Character array"]], ["Type","Description"]) },
 {"cat":"plc","title":"Number Systems","body":
   T([["Decimal 10","Binary 1010, Hex A, BCD 0001 0000"],
      ["Decimal 255","Binary 1111 1111, Hex FF"],
      ["Hex digits","0-9 then A-F (10-15)"],
      ["BCD","Each decimal digit = 4 bits; used by thumbwheels/displays"],
      ["Nibble/Byte/Word","4 / 8 / 16 bits"]]) },
 {"cat":"plc","title":"PLC Scan Cycle","body":
   "<ol class='reflist'><li>Read inputs (input image table)</li>" +
   "<li>Execute program logic top-to-bottom</li>" +
   "<li>Update outputs (output image table)</li>" +
   "<li>Housekeeping / comms / diagnostics</li></ol>" +
   "<p class='reftip'>Scan time typically 1-20 ms. Outputs only change at end of scan.</p>"},
 {"cat":"plc","title":"IEC 61131-3 Languages","body":
   T([["LD","Ladder Diagram - relay-style, most common"],
      ["FBD","Function Block Diagram - graphical blocks"],
      ["ST","Structured Text - Pascal-like text"],
      ["SFC","Sequential Function Chart - step/transition"],
      ["IL","Instruction List - assembly-like (deprecated)"]]) },
 {"cat":"plc","title":"Boolean Logic Truth Table","body":
   T([["AND","1 only if ALL inputs 1 (series contacts)"],
      ["OR","1 if ANY input 1 (parallel contacts)"],
      ["NOT","Inverts (normally-closed contact)"],
      ["XOR","1 if inputs differ"],
      ["Seal-in","Output OR'd with its own contact to latch"]], ["Gate","Behavior"]) },

 # ---------- Process & PID ----------
 {"cat":"pid","title":"PID Terms","body":
   T([["P (Proportional)","Reacts to present error; too high = oscillation"],
      ["I (Integral)","Eliminates steady-state offset; too high = overshoot/instability"],
      ["D (Derivative)","Reacts to rate of change; dampens; sensitive to noise"],
      ["Output","= P&times;error + I&times;&int;error + D&times;(d error/dt)"]]) },
 {"cat":"pid","title":"PID Tuning Effects","body":
   T([["Increase P","Faster response, more overshoot, may oscillate"],
      ["Increase I","Removes offset faster, more overshoot, slower stability"],
      ["Increase D","Less overshoot, dampens, amplifies noise"],
      ["Start point","Tune P first, add I to remove offset, D last if needed"]], ["Change","Effect"]) },

 # ---------- Fluid Power ----------
 {"cat":"fluid","title":"Cylinder Force &amp; Speed","body":
   T([["Force","F = P &times; A  (pressure &times; piston area)"],
      ["Area","A = &pi; &times; r&sup2;  (bore radius)"],
      ["Speed","v = Q / A  (flow / area)"],
      ["Rod side","Effective area reduced by rod = faster, less force on retract"]]) },
 {"cat":"fluid","title":"Pneumatics vs Hydraulics","body":
   T([["Medium","Air (compressible) vs oil (incompressible)"],
      ["Pressure","Pneumatic ~60-120 psi ; hydraulic 1000-5000+ psi"],
      ["Force","Hydraulic = much higher force, precise"],
      ["Speed","Pneumatic = fast, springy; hydraulic = smooth, controlled"],
      ["Clean","Air exhausts to atmosphere; oil contained/filtered"]]) },

 # ---------- Networks ----------
 {"cat":"net","title":"Industrial Protocol Comparison","body":
   T([["EtherNet/IP","CIP over Ethernet; Rockwell ecosystem"],
      ["PROFINET","Ethernet; Siemens ecosystem"],
      ["Modbus TCP/RTU","Simple, open, register-based; legacy-friendly"],
      ["EtherCAT","Very fast motion/servo; distributed clocks"],
      ["IO-Link","Point-to-point smart-sensor layer (not a bus)"]], ["Protocol","Notes"]) },
 {"cat":"net","title":"IP Addressing Basics","body":
   T([["Private ranges","10.x.x.x ; 172.16-31.x.x ; 192.168.x.x"],
      ["/24 subnet","255.255.255.0 = 254 usable hosts"],
      ["Same subnet","Devices must share network portion to talk directly"],
      ["Gateway","Route off-subnet traffic; DNS resolves names"]]) },

 # ---------- Safety ----------
 {"cat":"safety","title":"Stop Categories (IEC 60204-1)","body":
   T([["Category 0","Immediate removal of power (uncontrolled stop)"],
      ["Category 1","Controlled stop, then remove power"],
      ["Category 2","Controlled stop, power maintained"],
      ["E-stop","Usually Cat 0 or Cat 1"]], ["Category","Definition"]) },
 {"cat":"safety","title":"SIL vs Performance Level (PL)","body":
   T([["SIL (IEC 61508/62061)","SIL 1-3 in machinery; higher = lower failure prob"],
      ["PL (ISO 13849)","PL a-e; PL e is highest"],
      ["Rough map","PL c &asymp; SIL 1 ; PL d &asymp; SIL 2 ; PL e &asymp; SIL 3"],
      ["Determined by","Severity, frequency/exposure, possibility of avoidance"]]) },
 {"cat":"safety","title":"LOTO Steps (energy control)","body":
   "<ol class='reflist'><li>Prepare / notify affected employees</li>" +
   "<li>Shut down equipment normally</li><li>Isolate ALL energy sources</li>" +
   "<li>Apply locks and tags (each worker their own lock)</li>" +
   "<li>Release/block stored energy (springs, hydraulics, capacitors)</li>" +
   "<li>Verify zero energy (try-to-start / test)</li></ol>"},
 {"cat":"safety","title":"Safeguarding Devices","body":
   T([["Light curtain","Presence sensing, no physical barrier; response-time critical"],
      ["Safety mat","Detects operator standing in zone"],
      ["Interlock switch","Guard-position monitoring; use redundant/coded for high PL"],
      ["Two-hand control","Both hands occupied, away from hazard"],
      ["Safety relay/PLC","Monitors devices, provides safe stop"]]) },

 # ---------- Instrumentation ----------
 {"cat":"instr","title":"Thermocouple Types","body":
   T([["Type K","Ni-Cr / Ni-Al ; -200 to 1260C ; most common, general"],
      ["Type J","Iron / Constantan ; 0 to 750C"],
      ["Type T","Copper / Constantan ; -200 to 350C ; low temp"],
      ["Type E","High output ; -200 to 900C"],
      ["Cold junction","Reference compensation required for accuracy"]], ["Type","Details"]) },
 {"cat":"instr","title":"RTD (Pt100)","body":
   T([["Pt100","100 &Omega; at 0C ; ~0.385 &Omega;/C"],
      ["Accuracy","More accurate/stable than thermocouple, narrower range"],
      ["Wiring","3-wire common (compensates lead resistance); 4-wire best"],
      ["Range","~ -200 to 600C"]]) },
 {"cat":"instr","title":"Pressure &amp; Temp Conversions","body":
   T([["1 bar","14.5 psi = 100 kPa"],
      ["1 atm","14.7 psi = 1.013 bar"],
      ["C to F","F = C &times; 9/5 + 32"],
      ["F to C","C = (F - 32) &times; 5/9"],
      ["Gauge vs absolute","PSIA = PSIG + ~14.7 (atmospheric)"]]) },

 # ---------- Test & Troubleshooting ----------
 {"cat":"test","title":"Multimeter Functions","body":
   T([["Voltage","Measure IN PARALLEL across the component; power on"],
      ["Current","Measure IN SERIES (break the circuit); mind fuse rating"],
      ["Resistance/continuity","Power OFF, component isolated"],
      ["Diode test","Forward ~0.5-0.7V drop, reverse OL"],
      ["Safety","Verify meter on known live source before/after (prove-test-prove)"]]) },
 {"cat":"test","title":"Meggers &amp; Clamp Meters","body":
   T([["Megohmmeter","Insulation resistance at 500/1000V; motor windings-to-ground"],
      ["Good insulation","Typically hundreds of M&Omega;+ ; trend over time"],
      ["Clamp meter","Measure current without breaking circuit (CT)"],
      ["Inrush","Use clamp inrush mode for motor start current"]]) },
 {"cat":"test","title":"Systematic Troubleshooting","body":
   "<ol class='reflist'><li>Define the problem &amp; what changed</li>" +
   "<li>Gather info (indicators, faults, history)</li>" +
   "<li>Identify probable causes; split the system (half-split)</li>" +
   "<li>Test the most likely / easiest to check first</li>" +
   "<li>Repair, then verify the fix AND root cause</li>" +
   "<li>Document for the next tech</li></ol>"},
 {"cat":"test","title":"Common Motor Faults","body":
   T([["Won't start, hums","Single-phasing, locked rotor, low voltage, cap fault"],
      ["Trips overload","Overloaded, high ambient, bearing drag, unbalanced V"],
      ["Runs hot","Overload, poor ventilation, voltage imbalance, harmonics"],
      ["Bearing noise","Lubrication, misalignment, VFD shaft currents (use grounding ring)"]]) },

 # ---------- Conversions ----------
 {"cat":"conv","title":"SI Prefixes","body":
   T([["k (kilo)","10^3"],["M (mega)","10^6"],["G (giga)","10^9"],
      ["m (milli)","10^-3"],["u (micro)","10^-6"],["n (nano)","10^-9"]], ["Prefix","Multiplier"]) },
 {"cat":"conv","title":"Handy Constants &amp; Conversions","body":
   T([["1 HP","746 W"],["&radic;3","1.732"],["1 inch","25.4 mm"],
      ["1 gallon","3.785 L"],["1 lb","0.454 kg"],["1 Nm","0.738 ft-lb"]]) },
]
