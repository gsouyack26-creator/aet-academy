"""AET Course module data — imported by build_course.py"""

MODULES = [
  {
    "id": 0, "title": "Introduction to Automation Engineering Technology",
    "objectives": ["Define AET and its role in modern manufacturing/logistics","Identify the 10 core technical domains of automation","Describe how automated systems integrate sensors, controllers, actuators, and networks","Map AET career paths and credentials (AAS, BSET, certs)"],
    "sections": [
      {"h": "What Is AET?", "body": "Automation Engineering Technology is the applied discipline of designing, installing, programming, operating, and maintaining automated industrial systems. It combines electrical/electronics, mechanical, computer-control, and systems-integration skills.<br><br>At Amazon fulfillment centers (like ACY1), AET skills are used daily by RME technicians maintaining conveyors, sorters, drives, PLCs, robotics cells, and safety systems."},
      {"h": "The Automation Pyramid", "body": "Industrial automation is modeled as a hierarchy:<br><b>Level 0</b> - Physical Process (motors, actuators, sensors)<br><b>Level 1</b> - Direct Control (PLCs, safety controllers)<br><b>Level 2</b> - Supervisory (HMI, SCADA)<br><b>Level 3</b> - Manufacturing Operations (MES, historians)<br><b>Level 4</b> - Enterprise (ERP, business systems)<br><br>AET technicians primarily work at Levels 0-2."},
      {"h": "The 10 Core Domains", "body": "<ol><li>Electrical Fundamentals & Motor-Control Wiring</li><li>PLCs (IEC 61131-3)</li><li>HMI / SCADA</li><li>Industrial Networks & Fieldbus</li><li>Motors, VFDs & Drives</li><li>Sensors & Instrumentation</li><li>Fluid Power (Pneumatics & Hydraulics)</li><li>Robotics & Motion Control</li><li>Process Control & PID</li><li>Machine Safety / Functional Safety</li></ol>"},
      {"h": "Career Paths", "body": "<b>Credentials:</b> AAS (2yr) - entry; Stackable certs (15-30 cr); BSET (4yr) - advanced.<br><b>Certifications:</b> ISA CCST, SACA C-101/C-201, FANUC Robot cert, Rockwell/Siemens vendor certs, NCCER Instrumentation.<br><b>At Amazon RME:</b> L4 Automation Engineer, Mechatronics & Robotics Technician, Senior AE (L5+)."}
    ],
    "lab": {"title": "Explore the Automation Pyramid", "tool": "Paper/whiteboard", "steps": ["Draw the 5-level automation pyramid","List 2-3 real devices from your site per level","Star areas where you want to grow"]},
    "quiz": [
      {"q": "What does AET stand for?", "options": ["Automated Electrical Testing","Automation Engineering Technology","Advanced Electronics Troubleshooting","Applied Energy Transmission"], "answer": 1, "explain": "AET = Automation Engineering Technology."},
      {"q": "At which levels do AET technicians primarily work?", "options": ["Levels 3-4","Levels 0-2 (Process/Control/Supervisory)","Level 4 only","Level 5 (Cloud)"], "answer": 1, "explain": "AET techs work at Levels 0-2."},
      {"q": "Most common 2-year AET entry credential?", "options": ["BSET","AAS (Associate of Applied Science)","MBA","PhD"], "answer": 1, "explain": "The AAS is the standard 2-year entry credential."}
    ],
    "resources": [{"name":"RealPars","url":"https://www.realpars.com/"},{"name":"ISA","url":"https://www.isa.org/"},{"name":"SACA","url":"https://www.saca.org/"}]
  },
  {
    "id": 1, "title": "Electrical Fundamentals & Motor-Control Wiring",
    "objectives": ["Apply Ohm's law and Kirchhoff's laws to DC circuits","Calculate RMS voltage/current in single/three-phase AC","Read industrial motor-control schematics (ladder diagrams)","Wire a 3-wire start/stop motor control circuit"],
    "sections": [
      {"h": "DC Fundamentals", "body": "<b>Ohm's Law:</b> V = I x R. <b>Power:</b> P = V x I.<br><b>KVL:</b> Voltage drops around a loop = 0. <b>KCL:</b> Currents in = currents out.<br><b>Series:</b> R_total = R1+R2+R3 (current same, voltage divides).<br><b>Parallel:</b> 1/R_total = 1/R1+1/R2 (voltage same, current divides).<br><i>Example:</i> 24V, R1=100, R2=200 series: I=80mA, V_R1=8V, V_R2=16V."},
      {"h": "AC Fundamentals", "body": "<b>RMS:</b> V_rms = V_peak / sqrt(2). 120V outlet = 170V peak.<br><b>Three-phase:</b> V_line = V_phase x sqrt(3). 480V/277V, 208V/120V.<br><b>Power factor:</b> PF = cos(theta). Motors = lagging PF < 1."},
      {"h": "Motor Control Circuits", "body": "<b>Power circuit:</b> L1/L2/L3 - disconnect - fuses - contactor(M) - OL - motor.<br><b>Control circuit:</b> 120V control transformer - Stop(NC) - Start(NO) - M coil - M aux(seal-in).<br><b>3-wire control:</b> Start momentarily energizes M; M aux seals in. Stop breaks seal. OL NC contact protects."},
      {"h": "Reading Schematics", "body": "Ladder diagrams: two vertical rails, horizontal rungs. Devices: M=starter, OL=overload, CR=relay, PB=pushbutton, LS=limit switch, SOL=solenoid, PL=pilot light."}
    ],
    "lab": {"title": "Start/Stop Circuit", "tool": "PLCfiddle or pen/paper", "steps": ["Draw 3-wire start/stop with Stop(NC), Start(NO), M coil, M aux, OL(NC)","Trace current when Start pressed","Trace when Stop pressed","Add a pilot light for 'running'"]},
    "quiz": [
      {"q": "480V 3-phase: what is phase voltage?", "options": ["480V","277V","208V","120V"], "answer": 1, "explain": "V_phase = 480/sqrt(3) = 277V."},
      {"q": "What seals in the motor coil after releasing Start?", "options": ["Overload relay","M auxiliary contact (parallel with Start)","Disconnect","Gravity"], "answer": 1, "explain": "M aux contact seals in the coil."},
      {"q": "What does NC overload contact do?", "options": ["Starts motor","Speed control","Opens to de-energize coil on overload","Adds braking"], "answer": 2, "explain": "OL NC opens on overload, breaking coil circuit."}
    ],
    "resources": [{"name":"All About Circuits - DC","url":"https://www.allaboutcircuits.com/textbook/direct-current/"},{"name":"All About Circuits - AC","url":"https://www.allaboutcircuits.com/textbook/alternating-current/"},{"name":"Khan Academy EE","url":"https://www.khanacademy.org/science/electrical-engineering"}]
  },
  {
    "id": 2, "title": "PLC Fundamentals",
    "objectives": ["Explain the PLC scan cycle","Identify I/O types (discrete/analog, sinking/sourcing)","Write basic ladder logic: XIC, XIO, OTE, OTL, OTU","Describe IEC 61131-3 languages (LD, FBD, ST, SFC)"],
    "sections": [
      {"h": "What Is a PLC?", "body": "A <b>Programmable Logic Controller</b> reads inputs, executes a user program, and controls outputs in real time. Components: CPU, Power Supply, I/O Modules, Comm ports. Replaces hardwired relay logic with software."},
      {"h": "The Scan Cycle", "body": "Every PLC repeats: <ol><li><b>Input Scan</b> - read all inputs to image table</li><li><b>Program Scan</b> - execute logic top-to-bottom using input image</li><li><b>Output Scan</b> - write output image to physical outputs</li><li><b>Housekeeping</b> - comms, diagnostics, watchdog</li></ol>Typical scan: 5-50ms."},
      {"h": "Addressing", "body": "<b>Allen-Bradley Logix:</b> Tag-based names.<br><b>Siemens S7:</b> I0.0, Q0.0, M0.0, DB1.DBX0.0.<br><b>Legacy AB SLC:</b> I:1/0, O:0/0, B3:0/0.<br><b>Discrete:</b> 24VDC; NPN(sinking) vs PNP(sourcing).<br><b>Analog:</b> 4-20mA or 0-10V, 12-16 bit."},
      {"h": "Basic Ladder Instructions", "body": "<b>XIC</b> (Examine Closed) - TRUE when bit=1<br><b>XIO</b> (Examine Open) - TRUE when bit=0<br><b>OTE</b> (Output Energize) - ON when rung true<br><b>OTL/OTU</b> - Latch/Unlatch (retentive)<br><b>Branches</b> - parallel=OR, series=AND"},
      {"h": "IEC 61131-3 Languages", "body": "<b>LD</b> - Ladder (graphical, relay-style)<br><b>FBD</b> - Function Block (graphical blocks)<br><b>ST</b> - Structured Text (Pascal-like)<br><b>SFC</b> - Sequential Function Chart (state machine)<br>Most programs MIX: LD for discrete, ST for math, SFC for sequences."}
    ],
    "lab": {"title": "Build Start/Stop in Ladder", "tool": "OpenPLC Editor (free)", "steps": ["Create BOOL vars: Start_PB, Stop_PB, Motor_Run, Seal","Write ladder: (Start OR Seal) AND NOT Stop -> Seal; Seal -> Motor_Run","Simulate and verify","Add TON timer: 5s delay before Conveyor_Ready energizes"]},
    "quiz": [
      {"q": "When does the PLC read physical inputs?", "options": ["Program scan","Output scan","Input scan (beginning)","Housekeeping"], "answer": 2, "explain": "Inputs read at start of each scan."},
      {"q": "XIO is TRUE when bit is:", "options": ["1 (ON)","0 (OFF)","Floating","Pulsing"], "answer": 1, "explain": "XIO = TRUE when bit is 0 (OFF)."},
      {"q": "Which IEC 61131-3 language is text-based like Pascal?", "options": ["Ladder","FBD","Structured Text","SFC"], "answer": 2, "explain": "Structured Text is the text-based language."}
    ],
    "resources": [{"name":"OpenPLC Project","url":"https://openplcproject.com/"},{"name":"PLCfiddle","url":"https://plcfiddle.com/"},{"name":"RealPars - PLC Basics","url":"https://www.realpars.com/"}]
  },
  {
    "id": 3, "title": "PLC Programming II - Timers, Counters & Data",
    "objectives": ["Program TON, TOF, RTO timers","Program CTU/CTD counters","Use comparison and math instructions","Organize programs with subroutines/tasks"],
    "sections": [
      {"h": "Timers", "body": "<b>TON:</b> Accumulates while input TRUE; DN sets when ACC>=PRE; resets when input FALSE.<br><b>TOF:</b> DN ON immediately; counts after input FALSE; DN drops when ACC>=PRE.<br><b>RTO:</b> Like TON but retentive - needs explicit RES to clear.<br>Time base: PRE in ms (AB) or TIME type (Siemens T#5s)."},
      {"h": "Counters", "body": "<b>CTU:</b> Increments on false-to-true transition. DN when ACC>=PRE.<br><b>CTD:</b> Decrements. DN when ACC<=0.<br>Applications: batch counting, part counting, shift production tracking."},
      {"h": "Comparison & Math", "body": "<b>Compare:</b> EQU, NEQ, GRT, GEQ, LES, LEQ.<br><b>Math:</b> ADD, SUB, MUL, DIV, MOD, SQR.<br><b>Move:</b> MOV, COP, FLL.<br><i>Scaling example:</i> PSI = ((Raw - 6553) x 100) / 26214."},
      {"h": "Program Organization", "body": "<b>AB Logix:</b> MainTask/MainRoutine calls subroutines via JSR. Separate routines for Inputs, Sequence, Outputs, Alarms, HMI.<br><b>Tasks:</b> Continuous, Periodic (fixed interval), Event (triggered).<br><b>Siemens:</b> OB1, FCs, FBs with instance DBs, global DBs."}
    ],
    "lab": {"title": "Traffic Light Sequencer", "tool": "OpenPLC or CODESYS (free)", "steps": ["Create outputs: Red, Yellow, Green","Use 3 TON timers: Green=10s, Yellow=3s, Red=10s","Build sequence cycling through all states","Add CTU counting cycles; at 10 set Maintenance_Due","Add RES on Reset_PB"]},
    "quiz": [
      {"q": "TON PRE=3000ms, input TRUE for 2s then FALSE. Final ACC?", "options": ["3000","2000","0","5000"], "answer": 2, "explain": "TON resets ACC to 0 when input goes FALSE."},
      {"q": "Which timer retains ACC when input drops?", "options": ["TON","TOF","RTO","CTU"], "answer": 2, "explain": "RTO is retentive - keeps ACC, needs separate RES."},
      {"q": "Scale raw 6553-32767 to 0-100:", "options": ["EU = Raw x 100","EU = ((Raw-6553) x 100) / 26214","EU = Raw / 327.67","EU = Raw - 6553"], "answer": 1, "explain": "Subtract offset, multiply by EU span, divide by raw span."}
    ],
    "resources": [{"name":"RealPars - Timers","url":"https://www.realpars.com/"},{"name":"CODESYS","url":"https://www.codesys.com/"},{"name":"The Automation Blog","url":"https://theautomationblog.com/"}]
  },
  {
    "id": 4, "title": "Sensors & Instrumentation",
    "objectives": ["Select sensor types for various measurement needs","Wire NPN/PNP sensors to PLC inputs","Interpret 4-20 mA signals and scale to engineering units","Configure encoder feedback"],
    "sections": [
      {"h": "Discrete Sensors", "body": "<b>Inductive:</b> Metal only, 2-30mm range.<br><b>Capacitive:</b> Any material, shorter range.<br><b>Photoelectric:</b> Through-beam (longest range), Retroreflective, Diffuse (shortest).<br><b>Ultrasonic:</b> Any material, distance measurement.<br><b>NPN vs PNP:</b> NPN=sinking (switch to 0V), PNP=sourcing (switch to +V). Match to PLC input type."},
      {"h": "Analog Instruments", "body": "<b>4-20 mA:</b> 4mA=zero (live zero - 0mA = wire break fault). Immune to wire resistance.<br><b>Temperature:</b> RTD (Pt100, accurate), Thermocouple (J/K/T, wide range), Thermistor.<br><b>Pressure:</b> Gauge/absolute/differential, diaphragm/strain gauge.<br><b>Flow:</b> Magnetic, Coriolis, Vortex, DP.<br><b>Level:</b> Ultrasonic, Radar, Capacitance, Float."},
      {"h": "Encoders", "body": "<b>Incremental:</b> A/B (quadrature for direction), Z (index). Effective counts = PPR x 4.<br><b>Absolute:</b> Unique position code, no homing needed. SSI, BiSS output.<br>Applications: conveyor tracking, motor speed (RPM = pulses/time x 60/PPR)."},
      {"h": "Scaling & Calibration", "body": "EU = ((Raw - Raw_Low) / (Raw_High - Raw_Low)) x (EU_High - EU_Low) + EU_Low<br><b>Calibration:</b> Apply known reference, verify mA output, adjust zero (4mA) and span (20mA)."}
    ],
    "lab": {"title": "Sensor Wiring & Scaling", "tool": "Pen/paper + calculator", "steps": ["Draw PNP sensor wiring to 24VDC sinking PLC input","Draw 2-wire 4-20mA transmitter to analog input","Calculate: raw 19660 (range 6553-32767), 0-100 PSI = ? (Answer: 50 PSI)","Encoder 1024 PPR with x4 decoding = ? counts/rev (4096)"]},
    "quiz": [
      {"q": "4-20 mA reads 0 mA. What does this mean?", "options": ["Zero process value","Full scale","Wire break / transmitter failure","Normal at 0%"], "answer": 2, "explain": "4mA = live zero. 0mA = broken loop."},
      {"q": "PNP sensor switches which voltage when active?", "options": ["+V (supply)","0V (ground)","AC line","4-20 mA"], "answer": 0, "explain": "PNP = sourcing = connects output to +V."},
      {"q": "500 PPR encoder with x4 decoding:", "options": ["500","1000","2000","4000"], "answer": 2, "explain": "500 x 4 = 2000 counts/rev."}
    ],
    "resources": [{"name":"Inst Tools","url":"https://instrumentationtools.com/"},{"name":"AutomationDirect","url":"https://www.automationdirect.com/"},{"name":"RealPars - Sensors","url":"https://www.realpars.com/"}]
  },
  {
    "id": 5, "title": "Motors, VFDs & Drives",
    "objectives": ["Read motor nameplates (HP, FLA, RPM, SF, insulation, frame)","Explain VFD operation (rectifier-DC bus-inverter, V/Hz)","Configure essential VFD parameters","Diagnose common VFD faults (OC, OV, UV, OL, GF, OH)"],
    "sections": [
      {"h": "AC Induction Motors", "body": "Stator creates rotating field; rotor dragged by induction (always slower = slip).<br><b>Sync speed:</b> n = 120 x f / P. 60Hz 4-pole = 1800RPM sync, ~1750 actual.<br><b>Nameplate:</b> HP, FLA, RPM, Voltage, SF (1.15 typ), Insulation (F=155C), NEMA frame, Enclosure (TEFC/ODP)."},
      {"h": "VFD Principles", "body": "<b>Sections:</b> Rectifier (AC-DC, 6-pulse diode) - DC Bus (capacitors, ~650VDC for 480V) - Inverter (IGBT switching, variable V and f).<br><b>V/Hz:</b> Constant ratio maintains flux/torque. 460V/60Hz = 7.67V/Hz. At 30Hz output ~230V.<br><b>Vector control:</b> Independently controls flux and torque for better dynamics."},
      {"h": "Key Parameters", "body": "Motor data (V, FLA, HP, RPM, Hz). Accel/Decel time. Current limit (150% 60s, 200% 3s). Control mode (V/Hz, Sensorless Vector, Closed-loop Vector). Braking (coast, DC injection, dynamic braking resistor, regen)."},
      {"h": "Common Faults", "body": "<b>OC:</b> Overcurrent - short/ground/jam/fast accel.<br><b>OV:</b> Overvoltage - fast decel/regen/supply spike.<br><b>UV:</b> Undervoltage - power sag/blown phase fuse.<br><b>OL:</b> Overload (I2t) - sustained overload/poor ventilation.<br><b>GF:</b> Ground fault - damaged insulation/wet motor.<br><b>OH:</b> Overtemp - blocked fan/high ambient/carrier freq too high."}
    ],
    "lab": {"title": "VFD Parameter Worksheet", "tool": "Any VFD manual PDF (free from vendor)", "steps": ["Download PowerFlex 525 Quick Start Guide","Find motor nameplate params (P031-P034)","Find Accel/Decel (P036-P037)","Find Speed Reference Source options","Find Overcurrent fault code and troubleshooting steps"]},
    "quiz": [
      {"q": "4-pole motor at 45Hz, sync speed?", "options": ["1350 RPM","900 RPM","1800 RPM","2700 RPM"], "answer": 0, "explain": "120 x 45 / 4 = 1350 RPM."},
      {"q": "OV fault most often caused by:", "options": ["Low supply voltage","Decel too fast (regen to bus)","Shorted winding","High ambient temp"], "answer": 1, "explain": "Fast decel pumps energy back to DC bus, spiking voltage."},
      {"q": "Why maintain constant V/Hz?", "options": ["Save energy","Maintain motor flux (torque capability)","Reduce harmonics","OSHA requirement"], "answer": 1, "explain": "Constant V/Hz = constant flux = rated torque at any speed."}
    ],
    "resources": [{"name":"Rockwell Literature Library","url":"https://www.rockwellautomation.com/en-us/support/documentation/literature-library.html"},{"name":"RealPars - VFDs","url":"https://www.realpars.com/"},{"name":"Siemens SIOS","url":"https://support.industry.siemens.com/"}]
  }
]
