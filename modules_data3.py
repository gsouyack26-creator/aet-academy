"""AET Course modules 13-18 (Advanced)"""

MODULES_3 = [
  {
    "id": 13, "title": "Advanced PLC - Structured Text, AOIs & Fault Handling",
    "objectives": ["Write Structured Text with IF/CASE/FOR/WHILE","Create reusable Add-On Instructions (AOIs) and UDTs","Implement fault handling (major/minor faults, recovery)","Design state machines using CASE or SFC"],
    "sections": [
      {"h": "Structured Text Deep Dive", "body": "<b>Why ST?</b> Complex math, loops, conditionals are cleaner than ladder. Mix LD for discrete + ST for logic.<br><pre>IF condition THEN action;\nELSIF other THEN action2;\nELSE default;\nEND_IF;\n\nCASE state OF\n  0: (* idle *)\n  10: (* running *)\n  99: (* fault *)\nEND_CASE;\n\nFOR i := 0 TO 9 DO\n  array[i] := 0;\nEND_FOR;</pre><b>Data types:</b> BOOL, INT/DINT, REAL, STRING, arrays, structures (UDTs)."},
      {"h": "Add-On Instructions (AOIs)", "body": "<b>AOI</b> = reusable custom block with inputs, outputs, local data. Like a function.<br><b>Use cases:</b> Motor control (standardized), valve control, PID wrapper, alarm handler.<br><b>Structure:</b> Parameters (InOut/Input/Output), Local tags (hidden), Logic (LD/ST/FBD inside).<br><b>Benefits:</b> Tested once, used everywhere, version-controlled.<br><b>Siemens:</b> Function Blocks (FBs) with instance DBs."},
      {"h": "User-Defined Types (UDTs)", "body": "<pre>TYPE Motor_Data:\n  Running  : BOOL;\n  Faulted  : BOOL;\n  Speed_Cmd: REAL;\n  Speed_Fbk: REAL;\n  Amps     : REAL;\n  RunHours : DINT;\n  FaultCode: INT;\nEND_TYPE;</pre>Create: <code>Motors : ARRAY[0..19] OF Motor_Data;</code> - 20 motors, identical structure. Cleaner than 140 tags."},
      {"h": "Fault Handling", "body": "<b>Major faults (AB):</b> Halt controller - type 1 (power-up), type 4 (I/O), type 6 (instruction). Create Controller Fault Handler to catch/log/recover.<br><b>Design pattern:</b> Every AOI has .FaultCode + .Faulted. Fault routine logs to FIFO buffer. Recovery: clear fault, safe state, require operator acknowledge."},
      {"h": "State Machines", "body": "<pre>CASE Machine_State OF\n  0:  (* IDLE *) IF Start AND NOT Fault THEN State:=10; END_IF;\n  10: (* STARTING *) RunSequence(); IF Done THEN State:=20; END_IF;\n  20: (* RUNNING *) IF Stop THEN State:=30; END_IF;\n      IF Fault THEN State:=99; END_IF;\n  30: (* STOPPING *) StopSeq(); IF Stopped THEN State:=0; END_IF;\n  99: (* FAULTED *) AllOff(); IF Reset AND NOT Fault THEN State:=0; END_IF;\nEND_CASE;</pre>Explicit states, clear transitions, easy debug."}
    ],
    "lab": {"title": "Build a Motor Control AOI", "tool": "OpenPLC or CODESYS (free)", "steps": ["Create UDT Motor_Ctrl: Cmd_Start, Cmd_Stop, Running, Faulted, RunTimer, FaultCode","Create FB_Motor: inputs Start/Stop/OL_Fault/E_Stop; outputs Motor_Out/Running/Faulted","Implement ST state machine: IDLE/STARTING/RUNNING/FAULTED","Test: Start (should run); OL_Fault (should fault, output off); E_Stop (immediate off)","Reuse: instantiate 3 times for 3 motors, verify independence"]},
    "quiz": [
      {"q": "Main advantage of Add-On Instructions (AOIs)?", "options": ["Run faster","Reusable tested-once logic blocks with encapsulated data","Replace all ladder","Only work in ST"], "answer": 1, "explain": "AOIs = write once, test once, reuse everywhere with consistent behavior."},
      {"q": "FAULT state in a state machine should:", "options": ["Continue running","Turn off outputs, wait for fault clear + operator reset","Power cycle PLC","Delete program"], "answer": 1, "explain": "Fault = safe state (outputs off) + require both fault cleared AND operator acknowledge before restart."},
      {"q": "AB Major Fault Type 4 indicates:", "options": ["Math overflow","I/O communication failure","Power supply issue","Download needed"], "answer": 1, "explain": "Type 4 = I/O fault (module not responding, rack power loss, RPI timeout)."}
    ],
    "resources": [{"name":"Rockwell AOI Guide","url":"https://www.rockwellautomation.com/en-us/support/documentation/literature-library.html"},{"name":"CODESYS Function Blocks","url":"https://www.codesys.com/"},{"name":"The Automation Blog - ST","url":"https://theautomationblog.com/"}]
  },
  {
    "id": 14, "title": "IIoT & Industry 4.0",
    "objectives": ["Define IIoT, Industry 4.0, Smart Factory","Identify edge/fog/cloud architecture layers","Explain MQTT protocol for industrial data","Assess OT cybersecurity risks (IEC 62443)"],
    "sections": [
      {"h": "What Is IIoT / Industry 4.0?", "body": "<b>IIoT</b> = connecting industrial equipment to networks for data collection, analysis, optimization beyond traditional SCADA.<br><b>Industry 4.0</b> = 4th industrial revolution: cyber-physical systems, AI/ML, digital twins.<br><b>Smart Factory pillars:</b> Connectivity, Visibility, Transparency, Predictive, Adaptability.<br><b>RME context:</b> Monitron (vibration PdM), Compass dashboards, robotic fleet management."},
      {"h": "Edge-Fog-Cloud Architecture", "body": "<b>Edge:</b> Sensors/PLCs generating data. Lightweight processing on gateways (Pi, industrial PCs, Ignition Edge).<br><b>Fog/MES:</b> On-premise servers, local analytics, SCADA/historians. Works if internet drops.<br><b>Cloud:</b> AWS/Azure - big data, ML training, fleet analytics. Higher latency, massive scale.<br><b>Rule:</b> Safety-critical control stays at edge. Never put safety logic in the cloud."},
      {"h": "MQTT Protocol", "body": "<b>MQTT</b> = lightweight publish/subscribe for constrained devices.<br><b>Broker</b> (Mosquitto/HiveMQ) + <b>Publishers</b> (devices) + <b>Subscribers</b> (apps).<br><b>Topics:</b> <code>site/ACY1/conveyor/sorter1/speed</code> - hierarchical.<br><b>QoS:</b> 0 (fire-forget), 1 (at least once), 2 (exactly once).<br><b>Sparkplug B:</b> Industrial MQTT spec for SCADA (Ignition MQTT module uses it)."},
      {"h": "OT Cybersecurity (IEC 62443)", "body": "<b>Risk:</b> Connecting floor to networks exposes PLCs/drives to threats.<br><b>IEC 62443:</b> Security Levels (SL 1-4), zones/conduits, lifecycle requirements.<br><b>Practical:</b> Network segmentation (IT/OT DMZ), port security, disable unused protocols, patch carefully, physical access control, application whitelisting, PLC program backups.<br><b>Reality:</b> Many PLCs have default passwords, open Telnet. AET techs are front-line OT hygiene."}
    ],
    "lab": {"title": "MQTT Pub/Sub Demo", "tool": "Mosquitto (free) + MQTT Explorer (free)", "steps": ["Install Mosquitto broker + MQTT Explorer","Start broker on localhost:1883","Subscribe to 'factory/conveyor/#'","Publish: mosquitto_pub -t factory/conveyor/speed -m '45.2'","Observe message in Explorer","Publish 5 values simulating speed sensor every 2s","Discuss: payload format (JSON vs Sparkplug B)?"]},
    "quiz": [
      {"q": "Which layer handles real-time machine control?", "options": ["Cloud","Edge (PLC/sensor level)","Fog only","Enterprise ERP"], "answer": 1, "explain": "Time-critical control (ms response) must stay at edge. Cloud latency is unacceptable for real-time control."},
      {"q": "MQTT uses what messaging pattern?", "options": ["Request/Response","Publish/Subscribe via broker","Peer-to-peer","Polling"], "answer": 1, "explain": "MQTT = pub/sub through a broker. Publishers send to topics, subscribers receive from topics. Decoupled and lightweight."},
      {"q": "IEC 62443 addresses:", "options": ["Motor wiring","Industrial cybersecurity for automation","PLC languages","Hydraulic sizing"], "answer": 1, "explain": "IEC 62443 = THE standard for OT/industrial automation cybersecurity."}
    ],
    "resources": [{"name":"Mosquitto MQTT","url":"https://mosquitto.org/"},{"name":"MQTT Explorer","url":"https://mqtt-explorer.com/"},{"name":"ISA/IEC 62443","url":"https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards"}]
  },
  {
    "id": 15, "title": "Electrical Troubleshooting & Test Equipment",
    "objectives": ["Use DMM safely for V/I/R/continuity","Interpret megohmmeter insulation tests","Apply systematic troubleshooting (half-split, signal trace)","Use oscilloscopes for drive/signal analysis"],
    "sections": [
      {"h": "DMM Mastery", "body": "<b>Voltage (parallel):</b> AC vs DC, True RMS required for VFD outputs.<br><b>Current:</b> Clamp meter preferred (non-contact). Inrush vs running.<br><b>Resistance (de-energized!):</b> Isolate component. Motor windings balanced within 5%.<br><b>Safety:</b> CAT III/IV rated. Live-dead-live procedure. Never measure ohms on energized circuit."},
      {"h": "Megohmmeter (Insulation Resistance)", "body": "<b>Purpose:</b> Test motor/cable insulation at 500V or 1000V DC.<br><b>Motor test:</b> Disconnect leads, mega phase-to-ground. Good: >100M; Caution: 5-100M; Bad: <5M.<br><b>Rule of thumb:</b> Min = 1M per kV + 1M (480V motor: min ~2M).<br><b>PI test:</b> 10min/1min ratio. PI>2 = good; PI<1.5 = degraded."},
      {"h": "Systematic Troubleshooting", "body": "<b>Half-split:</b> Test midpoint - good=downstream, bad=upstream. Repeat. Logarithmic efficiency.<br><b>Symptom-based:</b> List causes, check most likely/easiest first.<br><b>Signal trace:</b> Follow signal source-to-destination. PLC output ON? Wire OK? Relay energized? Contact closed? Each step narrows fault.<br><b>Principle:</b> POWER -> SIGNAL -> LOAD."},
      {"h": "Oscilloscope Basics", "body": "<b>When:</b> DMM shows RMS only - useless for PWM/encoder/comm signals.<br><b>VFD output:</b> See PWM pattern. Verify 3 phases present/symmetric.<br><b>Encoders:</b> Clean square waves, 90deg quadrature, Z pulse present.<br><b>Tools:</b> Fluke ScopeMeter (CAT III rated, battery, portable)."}
    ],
    "lab": {"title": "Troubleshooting Scenarios", "tool": "Pen/paper scenarios", "steps": ["Scenario 1: Motor won't start, PLC output ON. Signal-trace from PLC output to motor terminals.","Scenario 2: VFD Ground Fault. What to disconnect, megger, isolate (motor vs cable vs drive)?","Scenario 3: Wrong speed. VFD cmd correct. Causes? (slip, wrong motor data, encoder fault, overload)","For each: most likely cause, first 3 checks, tools needed","Draw live-dead-live verification procedure"]},
    "quiz": [
      {"q": "Before measuring resistance with DMM:", "options": ["Set AC mode","De-energize and isolate the component","Use highest range only","Measure voltage on same leads"], "answer": 1, "explain": "NEVER measure ohms on energized circuits. De-energize, lock out, verify dead, THEN measure."},
      {"q": "Motor insulation 3 Megohms on 480V motor:", "options": ["Excellent","Caution - marginal, monitor/schedule replacement","Perfect per IEEE","Failed immediately"], "answer": 1, "explain": "Min = ~2M. 3M is above minimum but in caution zone (<100M). Monitor trend; if declining, plan replacement."},
      {"q": "Half-split troubleshooting:", "options": ["Replace half the parts","Test midpoint to find which half has the fault, repeat","Split the team","Run at half speed"], "answer": 1, "explain": "Each test eliminates half the circuit. Logarithmically efficient for long signal chains."}
    ],
    "resources": [{"name":"Fluke Multimeter Guides","url":"https://www.fluke.com/en-us/learn/blog/electrical"},{"name":"All About Circuits - Test Equipment","url":"https://www.allaboutcircuits.com/textbook/"},{"name":"Inst Tools - Insulation Testing","url":"https://instrumentationtools.com/"}]
  },
  {
    "id": 16, "title": "Preventive & Predictive Maintenance (Reliability)",
    "objectives": ["Differentiate reactive/preventive/predictive/prescriptive maintenance","Calculate MTBF, MTTR, availability","Interpret vibration analysis basics (FFT, bearing frequencies)","Design a PM program for automated equipment"],
    "sections": [
      {"h": "Maintenance Strategies", "body": "<b>Reactive:</b> Fix when broken. OK for non-critical only.<br><b>Preventive (PM):</b> Time/usage-based scheduled tasks. Prevents some failures.<br><b>Predictive (PdM):</b> Condition-based monitoring (vibration, temp, oil). Maintain when degradation detected. Optimal.<br><b>Prescriptive:</b> AI recommends action (Amazon Monitron example)."},
      {"h": "Key Metrics", "body": "<b>MTBF</b> = Total uptime / Failures. Higher = more reliable.<br><b>MTTR</b> = Total downtime / Repairs. Lower = faster response.<br><b>Availability</b> = MTBF / (MTBF+MTTR). Ex: 200hr/202hr = 99.0%.<br><b>OEE</b> = Availability x Performance x Quality. World-class: 85%+.<br><b>Amazon:</b> DPMO (jam rate), PM compliance, backlog aging."},
      {"h": "Vibration Analysis Basics", "body": "<b>Why:</b> Rotating equipment telegraphs failure through vibration weeks before catastrophe.<br><b>Signatures:</b> 1x RPM = imbalance; 2x = misalignment; Bearing freqs (BPFO/BPFI) = bearing degradation; 2x line freq (120Hz) = electrical issue.<br><b>ISO 10816:</b> Good (<1.8mm/s) to Danger (>11.2mm/s) for Class II machines."},
      {"h": "PM Program Design", "body": "<b>Steps:</b> 1) Asset criticality (A/B/C). 2) Failure mode analysis. 3) Task selection (predict vs prevent). 4) Schedule (balance across shifts). 5) Execute + document in CMMS. 6) Improve (extend intervals if PM finds nothing; shorten if failures occur between)."}
    ],
    "lab": {"title": "PM Program Design", "tool": "Spreadsheet or pen/paper", "steps": ["Pick 3 site assets (motor, divert, pneumatic cylinder)","List 2-3 failure modes + warning signs each","Assign strategy (reactive/PM/PdM) with justification","Define task, tools, interval for each PM","Calculate: MTBF=2000hr, MTTR=4hr, Availability=? (99.8%)","Discuss: how would vibration monitoring change MTBF/MTTR?"]},
    "quiz": [
      {"q": "1x RPM vibration on a motor indicates:", "options": ["Bearing failure","Imbalance (most common)","Electrical fault","Cavitation"], "answer": 1, "explain": "1x RPM = shaft speed frequency = rotor imbalance. Most common vibration problem. Fix by balancing."},
      {"q": "MTBF=500hr, MTTR=5hr. Availability?", "options": ["99.0%","90.0%","50.0%","95.0%"], "answer": 0, "explain": "500/(500+5) = 500/505 = 99.0%."},
      {"q": "Predictive maintenance is:", "options": ["Fix after failure","Replace on fixed schedule","Monitor condition, maintain when degradation detected","Hire more techs"], "answer": 2, "explain": "PdM = condition-based. Intervene only when trending toward failure."}
    ],
    "resources": [{"name":"Mobius Institute (vibration)","url":"https://www.mobiusinstitute.com/"},{"name":"AWS Monitron","url":"https://aws.amazon.com/monitron/"},{"name":"ISO 10816 summary","url":"https://instrumentationtools.com/"}]
  },
  {
    "id": 17, "title": "Control Panel Design & Build",
    "objectives": ["Read/create panel layouts per NFPA 79 / IEC 61439 / UL 508A","Select and size breakers, contactors, wire, enclosures","Apply wiring practices: separation, labeling, ferrules","Perform point-to-point verification and commissioning"],
    "sections": [
      {"h": "Standards", "body": "<b>NFPA 79:</b> Electrical standard for industrial machinery panels (NA). Covers enclosures, overcurrent, grounding, wire sizing, labeling.<br><b>IEC 61439:</b> International LV switchgear/controlgear assemblies.<br><b>UL 508A:</b> Industrial control panels (US listing). Defines SCCR (Short-Circuit Current Rating).<br><b>Requirements:</b> Door-disconnect interlock, SCCR calculation, grounding, ventilation, bending radius."},
      {"h": "Component Selection", "body": "<b>Enclosure:</b> NEMA 4 (watertight), NEMA 12 (dusttight), NEMA 1 (general). 20-30% spare space. RAL 7035 gray.<br><b>Main breaker:</b> Full-load + 125% continuous. Door-interlocked.<br><b>Motor circuits:</b> Breaker + contactor + overload. VFD: 1.5-2x drive FLA for inrush.<br><b>Control transformer:</b> 480V->120V. Size VA + 20% margin.<br><b>Terminal blocks:</b> DIN-rail, labeled, ferrules. Separate power/signal.<br><b>24VDC PSU:</b> For PLC I/O and sensors."},
      {"h": "Wiring Practices", "body": "<b>Separation:</b> Power and signal in SEPARATE ducts. Never mix 480V with 24VDC.<br><b>Sizing:</b> NEC ampacity. Typical: #14 for 120V control, #12 for 20A, #10-4 for motors by HP.<br><b>Labeling:</b> Every wire numbered (matches schematic). Print labels. Every TB position labeled.<br><b>Ferrules:</b> On all stranded wire to terminal blocks.<br><b>Colors (NFPA 79):</b> Black=power; White=neutral; Green/GY=ground; Red=AC control; Blue=DC."},
      {"h": "Commissioning", "body": "<b>Pre-power:</b> 1) Point-to-point verify all wires. 2) Torque check terminals. 3) Grounding continuity. 4) Megger motors (VFD disconnected!). 5) Remove debris. 6) Verify interlock.<br><b>Power-up:</b> Control circuit first (verify PLC/HMI). Then main power motors off (verify voltages). Then jog each motor individually (check rotation/current)."}
    ],
    "lab": {"title": "Panel Layout Exercise", "tool": "Graph paper or diagrams.net (free)", "steps": ["Design panel for: 1 VFD (10HP/480V), CompactLogix, 24VDC PSU, control transformer, terminal blocks","Draw DIN-rail layout: Top=disconnect+breakers, Middle=VFD+PLC+PSU, Bottom=TBs","Draw single-line power diagram","List wire sizes for each segment with justification","Create terminal block numbering scheme","List 5-item pre-power checklist"]},
    "quiz": [
      {"q": "Power and signal wiring should be:", "options": ["Same wireway for convenience","Separate wireways to prevent noise","Only signal needs ducts","Mix freely"], "answer": 1, "explain": "Separation prevents noise coupling. 480V next to 24VDC = false readings, erratic PLC, potential damage."},
      {"q": "What is SCCR?", "options": ["Standard Circuit Component Rating","Short-Circuit Current Rating - max fault current panel can withstand","Signal Cable Connector Rating","System Control Circuit Resistance"], "answer": 1, "explain": "SCCR must be >= available fault current at installation point. Required by UL 508A / NEC."},
      {"q": "First power-up sequence:", "options": ["Full power immediately","Control circuit first, then main power motors off, then jog each motor","Only if customer watches","Skip verification"], "answer": 1, "explain": "Staged power-up catches wiring errors before damage."}
    ],
    "resources": [{"name":"NFPA 79","url":"https://www.nfpa.org/codes-and-standards"},{"name":"AutomationDirect - Panel Design","url":"https://www.automationdirect.com/"},{"name":"Diagrams.net (free)","url":"https://www.diagrams.net/"}]
  },
  {
    "id": 18, "title": "Career Acceleration - Portfolio, Interviews & Certifications",
    "objectives": ["Build a technical portfolio demonstrating AET competency","Prepare for controls/automation interviews (technical + behavioral)","Create a certification roadmap by ROI","Develop a 12-month professional development plan"],
    "sections": [
      {"h": "Technical Portfolio", "body": "<b>Include:</b> PLC programs (screenshots, logic explanation), panel builds (photos, schematics), troubleshooting stories (problem/diagnosis/fix/time), automation projects (even personal OpenPLC+Pi), certs earned, training completed.<br><b>Format:</b> Physical binder + digital (GitHub Pages/PDF).<br><b>Key:</b> Show the PROCESS, not just result. Demonstrate WHY, not just WHAT."},
      {"h": "Interview Preparation", "body": "<b>Technical questions:</b> PLC scan cycle? Troubleshoot motor that won't start? NPN vs PNP? How does VFD control speed? What causes OV? Purpose of LOTO? Read this ladder - what does it do? Why 4-20mA not 0-20?<br><b>Behavioral (STAR):</b> Difficult equipment problem? Prioritize multiple machines down? Learn new technology quickly?<br><b>Amazon LPs:</b> Bias for Action, Dive Deep, Ownership, Invent & Simplify."},
      {"h": "Certification Roadmap", "body": "<b>Tier 1 (1-3 mo):</b> OSHA 10/30, MSSC CPT, NFPA 70E QEW.<br><b>Tier 2 (3-6 mo):</b> ISA CCST Level 1, SACA C-101, Rockwell cert.<br><b>Tier 3 (6-12 mo):</b> ISA CCST L2, FANUC Robot Programmer, Siemens SITRAIN, SACA C-201.<br><b>Tier 4 (expert):</b> ISA CCST L3, ISA CAP, PE license.<br><b>Best ROI:</b> ISA CCST (widest industry recognition). Vendor certs for specific shops."},
      {"h": "12-Month Plan", "body": "<pre>Mo 1-2: Modules 0-4; Start CCST study\nMo 3-4: Modules 5-8; OpenPLC home project; Start portfolio\nMo 5-6: Modules 9-12; Take CCST L1 exam; 1 vendor training\nMo 7-8: Advanced 13-17; MQTT+PLC project; Start next cert\nMo 9-10: Pursue advanced cert; Attend ISA/SACA event; Update portfolio\nMo 11-12: Apply for target role; Final portfolio polish; Plan Year 2</pre><b>Habits:</b> 30 min/day study, 1 project/month, document everything, network (ISA local, LinkedIn)."}
    ],
    "lab": {"title": "Personal Development Sprint", "tool": "Spreadsheet + this course", "steps": ["Self-assess: rate 1-5 on each of 10 AET domains","Identify bottom 3 = priority learning areas","Pick ONE certification aligned with career goal","Find 3 free resources covering your weak areas","Write 90-day plan: study, build, achieve","Block 30 min/day for AET study","Start portfolio doc with 3 past work accomplishments"]},
    "quiz": [
      {"q": "ISA CCST is valuable because:", "options": ["Cheapest","Most widely recognized control systems technician credential with 3 levels","Amazon requires it","Replaces degree"], "answer": 1, "explain": "ISA CCST = THE benchmark for automation/controls technicians. Levels I-II-III. Recognized industry-wide."},
      {"q": "Interview question 'troubleshoot a motor that won't start' tests:", "options": ["Memorization","Your systematic diagnostic approach (logical, safe, efficient)","Fix speed","Brand knowledge"], "answer": 1, "explain": "They want systematic METHOD: power -> signal -> load. Evaluating thought process + safety awareness."},
      {"q": "Portfolio should emphasize:", "options": ["Only certs","The PROCESS (how you diagnosed/designed/built)","Page quantity","Opinions"], "answer": 1, "explain": "Process > product. Show HOW you think and solve problems."}
    ],
    "resources": [{"name":"ISA CCST","url":"https://www.isa.org/certification/ccst"},{"name":"SACA","url":"https://www.saca.org/"},{"name":"Amazon Jobs - RME","url":"https://www.amazon.jobs/"},{"name":"GitHub Pages","url":"https://pages.github.com/"}]
  },
  {
    "id": 19,
    "title": "PLC Programming Languages - Ladder vs Structured Text (IEC 61131-3)",
    "objectives": [
      "Name the five IEC 61131-3 languages and when each fits",
      "Read and write core Ladder (LD) instructions: XIC, XIO, OTE, OTL/OTU, timers, counters",
      "Read and write core Structured Text (ST): assignment, comparisons, IF/CASE/FOR/WHILE",
      "Choose the right language for a task: safety/interlocks vs. math/data vs. sequencing"
    ],
    "sections": [
      {
        "h": "The IEC 61131-3 Language Family",
        "body": "The IEC 61131-3 standard defines <b>five</b> PLC programming languages. Most controllers (Rockwell Studio 5000, Siemens TIA Portal, CODESYS) let you mix them in one project.<br><br><b>1. Ladder Diagram (LD)</b> - graphical relay rungs. The default for discrete logic and the easiest to troubleshoot live.<br><b>2. Structured Text (ST)</b> - Pascal-like text. Best for math, loops, arrays, and complex decisions. Siemens calls it <b>SCL</b> (Structured Control Language).<br><b>3. Function Block Diagram (FBD)</b> - wired blocks; common for process/PID and analog signal flow.<br><b>4. Sequential Function Chart (SFC)</b> - flowchart of steps + transitions; ideal for step sequences and batch.<br><b>5. Instruction List (IL)</b> - low-level assembly-like text; <b>deprecated</b> in the 3rd edition, avoid for new work.<br><br><b>Key idea:</b> you don't pick one for the whole machine - you pick the best language per routine."
      },
      {
        "h": "Ladder Diagram (LD) Essentials",
        "body": "Ladder reads left-to-right like current flowing from a left power rail to a right rail through contacts to a coil.<br><pre>    XIC        XIO         OTE\n --| |--------|/|---------( )--\n  Start      Stop        Motor</pre><b>Core instructions:</b><br>&bull; <b>XIC</b> <code>-| |-</code> Examine If Closed (true when the bit is 1)<br>&bull; <b>XIO</b> <code>-|/|-</code> Examine If Open (true when the bit is 0)<br>&bull; <b>OTE</b> <code>-( )-</code> Output Energize (non-retentive, follows the rung)<br>&bull; <b>OTL / OTU</b> Output Latch / Unlatch (retentive set/reset)<br>&bull; <b>Timers:</b> TON (on-delay), TOF (off-delay), RTO (retentive)<br>&bull; <b>Counters:</b> CTU (up), CTD (down)<br>&bull; <b>Data:</b> MOV, ADD, CPT, comparison (EQU, GRT, LES)<br><br><b>Strength:</b> you can watch power flow highlight in real time - unmatched for live discrete troubleshooting. <b>Weakness:</b> math, loops, and array handling get sprawling and hard to read."
      },
      {
        "h": "Structured Text (ST) Essentials",
        "body": "ST is a high-level text language. Watch the two easiest gotchas: <b>:=</b> is assignment, <b>=</b> is comparison, and <b>&lt;&gt;</b> means not-equal.<br><pre>(* on-delay in ST *)\nIF Start AND NOT Stop THEN\n  Motor := TRUE;\nELSIF EStop THEN\n  Motor := FALSE;\nEND_IF;\n\nCASE State OF\n  0:      (* idle *)\n  10..20: (* running band *)\n  99:     Motor := FALSE;\nEND_CASE;\n\nFOR i := 0 TO 9 DO\n  Totals[i] := 0;\nEND_FOR;</pre><b>Constructs:</b> IF/ELSIF/ELSE, CASE (supports ranges like <code>2..4:</code>), FOR, WHILE, REPEAT...UNTIL.<br><b>Where it runs:</b> Studio 5000 supports ST on ControlLogix / CompactLogix and Micro800 (Connected Components Workbench) - <b>but not</b> on legacy MicroLogix / SLC-500. Siemens SCL runs on S7-1200/1500.<br><b>Strength:</b> compact math, loops, recipes, string/array work. <b>Weakness:</b> no live power-flow view, and an unbounded loop can blow the scan time."
      },
      {
        "h": "Choosing the Right Language",
        "body": "<table border='1' cellpadding='4' style='border-collapse:collapse'><tr><th>Task</th><th>Best language</th></tr><tr><td>Safety interlocks, permissives, E-stop logic</td><td><b>Ladder</b> (auditable, live troubleshooting)</td></tr><tr><td>Discrete motor / valve / conveyor control</td><td><b>Ladder</b> (or an AOI written in LD)</td></tr><tr><td>Math, scaling, totalizing, arrays, recipes</td><td><b>Structured Text</b></td></tr><tr><td>Analog / PID signal flow</td><td><b>FBD</b></td></tr><tr><td>Step sequences, batch, startup/shutdown</td><td><b>SFC</b> (or a CASE state machine in ST)</td></tr></table><br><b>Rule of thumb:</b> if a maintenance tech will troubleshoot it live at 2 a.m., favor ladder. If it's data-heavy engineering logic, favor ST. Interlocks and permissives should stay in ladder so the DENY condition is easy to verify."
      },
      {
        "h": "How This Shows Up at ACY1 (AWCS)",
        "body": "The Amazon Warehouse Control System (AWCS) conveyor logic is <b>ladder with AOIs</b> - one Add-On Instruction per conveyor-zone type. When troubleshooting an unfamiliar zone, <b>open the AOI definition</b> - reading the main routine alone will mislead you.<br><br>AWCS runs three Logix tasks: <b>Continuous</b> (~5 ms scan, conveyor logic), <b>Periodic</b> (50 ms, sorter decisions), and <b>Event</b> (interrupt-driven, E-stops).<br><br>A <b>watchdog fault (F0xx)</b> fires when the continuous-task scan time exceeds the watchdog setting - the controller faults and <b>all outputs de-energize</b> (conveyor stops). A classic cause is a <b>runaway FOR-DO loop</b> or an oversized data-move - exactly the kind of ST/loop mistake this module warns about. That is a strong argument for keeping loops bounded and interlocks in ladder."
      }
    ],
    "lab": {
      "title": "Translate a Rung Both Ways",
      "tool": "OpenPLC or CODESYS (free)",
      "steps": [
        "Write a seal-in (start/stop) motor rung in Ladder: XIC Start, branch OTE Motor around it, XIO Stop in series",
        "Add a TON so the motor only energizes 2 s after Start is held",
        "Now write the SAME logic in Structured Text using IF/ELSIF and a TON function block",
        "Compare: which was faster to read? Which would you rather troubleshoot live?",
        "Add a bounded FOR loop in ST to clear a 10-element array - confirm it is bounded (0 TO 9) so it cannot run away and trip the scan watchdog"
      ]
    },
    "quiz": [
      {
        "q": "How many languages does IEC 61131-3 define?",
        "options": [
          "Two",
          "Three",
          "Five",
          "Ten"
        ],
        "answer": 2,
        "explain": "Five: Ladder Diagram (LD), Structured Text (ST), Function Block Diagram (FBD), Sequential Function Chart (SFC), and Instruction List (IL, now deprecated)."
      },
      {
        "q": "In Structured Text, which operator is ASSIGNMENT (not comparison)?",
        "options": [
          ":=",
          "==",
          "=",
          "<>"
        ],
        "answer": 0,
        "explain": "ST uses := to assign and = to compare. <> means not-equal. Mixing up := and = is the classic ST beginner bug."
      },
      {
        "q": "Which Ladder instruction is true when its bit is 0 (OFF)?",
        "options": [
          "XIC -| |-",
          "XIO -|/|-",
          "OTE -( )-",
          "OTL"
        ],
        "answer": 1,
        "explain": "XIO (Examine If Open) is true when the bit is 0. XIC (Examine If Closed) is true when the bit is 1."
      },
      {
        "q": "For safety interlocks and permissives, which language is generally preferred?",
        "options": [
          "Structured Text",
          "Ladder",
          "Instruction List",
          "REPEAT loops"
        ],
        "answer": 1,
        "explain": "Ladder is auditable and shows live power flow, so verifying the DENY condition of an interlock is straightforward - the reason AWCS keeps this logic in ladder."
      },
      {
        "q": "AWCS conveyor logic is primarily written in which language, and how is zone logic packaged?",
        "options": [
          "Pure ST, one big routine",
          "Ladder with one AOI per conveyor-zone type",
          "FBD only",
          "SFC with no reuse"
        ],
        "answer": 1,
        "explain": "AWCS is ladder that uses Add-On Instructions extensively - one AOI per zone type. Always open the AOI definition when troubleshooting an unfamiliar zone."
      },
      {
        "q": "A PLC watchdog fault (F0xx) on the AWCS continuous task most likely results from:",
        "options": [
          "A blown 24 VDC fuse",
          "A runaway FOR-DO loop or oversized data move that overruns scan time",
          "An HMI reboot",
          "A network switch swap"
        ],
        "answer": 1,
        "explain": "F0xx fires when continuous-task scan time exceeds the watchdog setting - commonly a runaway FOR-DO loop or large data move. The controller faults and all outputs de-energize (conveyor stops)."
      },
      {
        "q": "Which task is best suited to Structured Text rather than Ladder?",
        "options": [
          "A single start/stop seal-in rung",
          "Totalizing throughput across a 50-element array",
          "An E-stop drop-out",
          "A guard-door permissive"
        ],
        "answer": 1,
        "explain": "Array math, totalizing, scaling, and recipes are compact in ST but sprawling in ladder. Discrete safety logic stays in ladder."
      },
      {
        "q": "Structured Text is NOT available on which controller family?",
        "options": [
          "ControlLogix",
          "CompactLogix",
          "Legacy MicroLogix / SLC-500",
          "Micro800 (CCW)"
        ],
        "answer": 2,
        "explain": "Studio 5000 supports ST on ControlLogix, CompactLogix, and Micro800 (via CCW), but legacy MicroLogix / SLC-500 do not support Structured Text."
      }
    ],
    "resources": [
      {
        "name": "IEC 61131-3 Overview (PLCopen)",
        "url": "https://plcopen.org/iec-61131-3"
      },
      {
        "name": "Rockwell Studio 5000 Logix Designer",
        "url": "https://www.rockwellautomation.com/en-us/products/software/factorytalk/designsuite/studio-5000.html"
      },
      {
        "name": "The Automation Blog - Ladder vs ST",
        "url": "https://theautomationblog.com/"
      }
    ]
  },
  {
    "id": 20,
    "title": "Material Handling & Conveyor Systems (MHE)",
    "objectives": [
      "Identify the major conveyor types and where each is used in a fulfillment center",
      "Explain 24 VDC Motor-Driven Roller (MDR) zones and Zero-Pressure Accumulation (ZPA)",
      "Describe common sortation technologies and how packages are diverted",
      "Diagnose the most common MHE faults: back-pressure, jams, belt mistracking, E-stop opens"
    ],
    "sections": [
      {
        "h": "Conveyor Types 101",
        "body": "Material Handling Equipment (MHE) is the backbone of a fulfillment center. Know the families:<br><br>&bull; <b>Belt conveyor</b> - continuous belt over a slider bed or rollers; general transport.<br>&bull; <b>Motor-Driven Roller (MDR)</b> - 24 VDC brushless rollers, grouped into zones, each zone driven by a control card. Low-voltage, quiet, energy-efficient.<br>&bull; <b>Line-shaft / belt-driven roller</b> - older mechanical roller conveyor.<br>&bull; <b>Accumulation conveyor</b> - buffers product; may be Zero-Pressure Accumulation (ZPA).<br>&bull; <b>Merge / divert</b> - combines lines or pushes product off to a lane.<br>&bull; <b>Gapper</b> - speeds up sections to create gaps between packages (e.g. the ADTA gapper's 4-stage progression ~85&rarr;115&rarr;170&rarr;200 ft/min, dynamically adjusting section speed +/-20%).<br><br>Most FC lines are a chain of these feeding a sorter."
      },
      {
        "h": "MDR Zones & Zero-Pressure Accumulation (ZPA)",
        "body": "<b>MDR</b> conveyor is divided into <b>zones</b>. Each zone has a control card (e.g. an Interroll MultiControl) driving one or more 24 VDC rollers, plus a zone photoeye + reflector.<br><br><b>ZPA</b> = <i>Zero-Pressure Accumulation</i>: each zone only releases its item when the <b>downstream zone is clear</b>, so boxes never pile up and push against each other. This protects product and creates clean gaps for downstream scanning/sortation.<br><br><b>Back-pressure fault:</b> if a downstream zone stays full and the upstream zone keeps driving, the MultiControl card triggers a <b>back-pressure timeout (typically 30 s)</b> and stops the zone. <b>Fix:</b> relieve the downstream jam FIRST, then reset the zone. If it recurs, check zone-sensor alignment and reflector cleanliness."
      },
      {
        "h": "Sortation Systems",
        "body": "A sorter diverts each package to its destination lane. Common types:<br><br>&bull; <b>Sliding-shoe sorter</b> - polyurethane shoes slide diagonally across a moving slat bed to push packages into angled lanes. PM focus: shoe wear + guide-mechanism alignment.<br>&bull; <b>Cross-belt sorter</b> - each carrier has its own little belt that runs sideways to eject at the target chute.<br>&bull; <b>Tilt-tray sorter</b> - trays tilt to drop items into chutes.<br>&bull; <b>Pop-up wheel / roller diverter</b> - wheels rise to steer a package off the main line.<br>&bull; <b>Scan-and-induct tunnel</b> - reads the barcode and commits the divert decision downstream.<br><br>Sortation depends on accurate <b>gapping and induction</b> upstream - if gaps are wrong, packages get mis-sorted or sent to reject."
      },
      {
        "h": "Common MHE Faults & Recovery",
        "body": "<b>Back-pressure timeout:</b> downstream full &rarr; upstream zone stops. Clear downstream jam, then reset zone.<br><b>Jam / package stuck:</b> a photoeye stays blocked past its timer. Clear the box, verify photoeye + reflector are clean and aligned.<br><b>Gate / divert fault:</b> a 24 VDC divert solenoid didn't actuate (package goes to reject). Check coil resistance (a 24 VDC coil should read ~50-200 &#8486;) and that supply is &gt; 22 V during actuation.<br><b>E-stop open (ADTA zone):</b> ALL e-stops (pull cords + push buttons) in the zone must be reset before it restarts. Use the HMI zone map to find the open device - <b>do not pull-test</b> e-stops to find it.<br><b>Belt mistracking:</b> covered in the mechanical section - the take-up rule matters."
      },
      {
        "h": "Belt Tracking & Take-Up (ACY1 rules)",
        "body": "Two ACY1 mechanical rules worth memorizing (from the ACY1 MHE Training Guide):<br><br><b>Belt tracking correction:</b> when a belt drifts off-center, adjust the take-up on the side <b>OPPOSITE</b> the direction of drift, in <b>small increments</b> - run and recheck before adjusting again.<br><br><b>Screw-type take-up:</b> adjust <b>both sides equally in 1/4-turn increments only</b>. Run briefly and re-check tracking after each cycle before making further corrections.<br><br>Over-tightening or chasing the belt too aggressively causes more mistracking, premature belt/bearing wear, and lacing failures. Small moves, verify, repeat."
      }
    ],
    "lab": {
      "title": "Map a ZPA Zone and Trace a Back-Pressure Fault",
      "tool": "Paper/whiteboard (or any MDR line you can observe safely)",
      "steps": [
        "Sketch 3 MDR zones in series: each with a control card, driven roller(s), photoeye + reflector",
        "Mark the ZPA rule: a zone only releases when the DOWNSTREAM zone photoeye is clear",
        "Now block the most-downstream photoeye (simulate a full/jammed exit)",
        "Trace what happens: downstream stays full -> upstream keeps arriving -> back-pressure timeout (~30 s) -> zone stops",
        "Write the correct recovery order: relieve the DOWNSTREAM jam first, THEN reset the zone (not the other way around)"
      ]
    },
    "quiz": [
      {
        "q": "What does ZPA (Zero-Pressure Accumulation) mean for an MDR conveyor?",
        "options": [
          "All zones run at zero speed",
          "Each zone releases its item only when the downstream zone is clear",
          "Zones apply constant pressure to pack boxes tightly",
          "The conveyor has no photoeyes"
        ],
        "answer": 1,
        "explain": "ZPA releases one item per zone only when the downstream zone is clear, so boxes never pile up and push against each other - creating clean gaps for scanning/sortation."
      },
      {
        "q": "A downstream MDR zone stays full and the upstream zone keeps driving. What fault fires and how do you clear it?",
        "options": [
          "Overtemp - power cycle the card",
          "Back-pressure timeout (~30 s) - relieve the downstream jam first, then reset the zone",
          "E-stop open - reset the whole line",
          "Belt slip - tighten the belt"
        ],
        "answer": 1,
        "explain": "The MultiControl card triggers a back-pressure timeout (typically 30 s). Always relieve the DOWNSTREAM jam first, then reset the zone."
      },
      {
        "q": "A belt is drifting off-center to the right. Per the ACY1 rule, you adjust the take-up on which side?",
        "options": [
          "The right side (same as drift)",
          "The side OPPOSITE the drift, in small increments",
          "Both sides one full turn",
          "Loosen the belt completely"
        ],
        "answer": 1,
        "explain": "Adjust the take-up on the side OPPOSITE the direction of drift, in small increments - run and recheck before adjusting again."
      },
      {
        "q": "Screw-type take-ups should be adjusted:",
        "options": [
          "One side only, several turns",
          "Both sides equally, in 1/4-turn increments, rechecking each cycle",
          "As tight as possible in one pass",
          "Only when the belt breaks"
        ],
        "answer": 1,
        "explain": "Adjust both sides equally in 1/4-turn increments only, running briefly and re-checking tracking after each cycle."
      },
      {
        "q": "A sliding-shoe sorter diverts packages by:",
        "options": [
          "Tilting trays",
          "Polyurethane shoes sliding diagonally across a slat bed into angled lanes",
          "Air jets",
          "Robot arms"
        ],
        "answer": 1,
        "explain": "Sliding-shoe sorters use individual polyurethane shoes that slide diagonally across a moving slat bed; shoe wear and guide-mechanism alignment are the primary PM items."
      },
      {
        "q": "A 24 VDC divert-gate solenoid won't actuate and packages go to reject. First electrical checks?",
        "options": [
          "Replace the PLC",
          "Coil resistance (~50-200 ohm) and supply voltage > 22 V during actuation",
          "Reboot the HMI",
          "Replace the belt"
        ],
        "answer": 1,
        "explain": "Check the 24 VDC coil resistance (should read ~50-200 ohm) and confirm supply is above 22 V during actuation before condemning the gate."
      },
      {
        "q": "On an ADTA zone with an 'E-stop open' fault, the correct approach is:",
        "options": [
          "Pull-test each e-stop until the zone starts",
          "Use the HMI zone map to find the open device; reset ALL e-stops in the zone before it restarts",
          "Bypass the e-stop circuit",
          "Reset only the nearest button"
        ],
        "answer": 1,
        "explain": "ADTA requires ALL e-stops in the zone to be reset; use the HMI zone map to identify the open device - do NOT pull-test e-stops to find it."
      },
      {
        "q": "The ADTA gapper's job is to:",
        "options": [
          "Sort packages by size",
          "Create gaps between packages by progressively increasing section speed",
          "Weigh packages",
          "Print labels"
        ],
        "answer": 1,
        "explain": "The gapper accelerates through a 4-stage speed progression (~85->115->170->200 ft/min), dynamically adjusting section speed to open consistent gaps for downstream scanning/sortation."
      }
    ],
    "resources": [
      {
        "name": "Interroll MultiControl / MDR",
        "url": "https://www.interroll.com/"
      },
      {
        "name": "MHI - Conveyor & Sortation Overview",
        "url": "https://www.mhi.org/"
      },
      {
        "name": "ACY1 MHE Training Guide (internal RME share)",
        "url": "https://www.mhi.org/fundamentals/conveyors"
      }
    ]
  },
  {
    "id": 21,
    "title": "Amazon Robotics & Autonomous Mobile Robots (AMR)",
    "objectives": [
      "Describe how an AR drive-unit floor works: fiducials, pods, highways, charging",
      "Name the major drive-unit models and the tools used to service them (ARTS, DUDT)",
      "Explain charge management: drive-to-charger ratios, LCRM/MDIPF",
      "Diagnose the top AR floor faults: fiducial read, wheel obstruction, No Comms, charger overcurrent"
    ],
    "sections": [
      {
        "h": "How an AR Floor Works",
        "body": "Amazon Robotics (AR) uses fleets of autonomous drive units (Kiva-lineage) that shuttle inventory <b>pods</b> to and from operator stations.<br><br>&bull; <b>Fiducials</b> - 2D barcode/QR markers laid out in a grid on the floor. Drives read them with a downward camera to know exactly where they are.<br>&bull; <b>Highways</b> - defined travel lanes; 'super highways' and 'main highways' carry the heaviest traffic, the 'pod farm' is the storage interior.<br>&bull; <b>Pods</b> - the mobile shelving a drive lifts and carries.<br>&bull; <b>Charging</b> - drives return to chargers autonomously to top up.<br><br>The whole floor is a coordinated traffic system - navigation depends on <b>clean, undamaged fiducials</b> and a <b>debris-free floor</b>."
      },
      {
        "h": "Drive-Unit Models & Service Tools",
        "body": "<b>Models:</b> the network runs many drive types - named models like <b>Hercules, Atlas, Titan, Pegasus</b>, plus legacy H, S, G, P, PL, T, TR and 'X' series. Battery chemistry varies: <b>Li-ion</b> (G/P/PL/S) and older <b>lead-acid (R)</b>. Reboot CLI commands differ by model.<br><br><b>Service software:</b><br>&bull; <b>ARTS</b> (Amazon Robotics Technician Suite) - the tech portal / floor map / diagnostics. Always verify your <b>DUDT client version matches the server version</b> before a session - a mismatch causes silent data errors.<br>&bull; <b>DUDT</b> (Drive Unit Diagnostic Tool) - includes the <b>'Wheel Wear'</b> function. Replace wheels when OD is <b>&lt; 190 mm</b> (standard drive) or <b>&lt; 195 mm</b> (H-drive). Worn wheels cause higher motor current, floor scuffing, and navigation drift."
      },
      {
        "h": "Charge Management (LCRM / MDIPF)",
        "body": "Keeping enough drives charged is a fleet-level balancing act.<br><br>&bull; <b>Drive-to-charger ratio:</b> an automatic <b>Sev-3 ticket</b> fires when the drive:charger ratio exceeds <b>26:1 for 90+ continuous minutes</b>. Recommended maximums vary by model (e.g. Hercules and Li-ion G = 25:1, Titan = 21:1, Li-ion S = 18:1).<br>&bull; <b>LCRM</b> (Low Charge Regime Manager) automatically reduces <b>MDIPF</b> (Max Drives In Play Fraction) - holding drives back in reserve for charging when average fleet charge drops below thresholds. Enabled at all FC sites for all drive types <b>except lead-acid (R)</b> drives, and NOT in LVM zones.<br><br>Translation: if too few chargers are working, the system parks drives to protect charge - throughput drops before drives die on the floor."
      },
      {
        "h": "Top AR Floor Faults & Recovery",
        "body": "&bull; <b>Error 105 - fiducial read failure:</b> smeared or damaged fiducial. Clean QR codes monthly with <b>dry microfiber, no solvents</b>; replace any fiducial with corner damage &gt; 5 mm.<br>&bull; <b>Error 206 - wheel obstruction:</b> debris fouling a drive wheel. Floor debris (cardboard, strapping, labels) is the <b>#1 cause of drive disablements during peak</b> - run hourly floor walks; clear with compressed air.<br>&bull; <b>'No Comms' in ARTS:</b> check (1) AP (access point) status on the floor map, (2) Ethernet cable to the AP, (3) VLAN assignment on the switch port. AR drives use a <b>dedicated VLAN</b> - cross-VLAN traffic causes intermittent disconnects.<br>&bull; <b>Charger 'Output Overcurrent' (LED: 3 red flashes):</b> shorted drive battery or damaged contacts. Test with a known-good drive - if the fault clears, the original drive's battery is failed; if it persists, the charger is suspect."
      },
      {
        "h": "AR Floor PM & Safety",
        "body": "<b>Floor PM tiers (RME ERS policy):</b> sortable AR floors use three cleaning tiers in APM - <b>4-week</b> (high-traffic: perimeter, super highways), <b>8-week</b> (moderate: main highways, pod-farm exterior), <b>12-week</b> (deep pod-farm interior). Fiducial inspection rides along with cleaning.<br><br><b>Safety:</b> the AR floor is a restricted, controlled space. Entry requires the site's floor-access / lockout process (vest, authorization, and the field's drives paused or the segment cleared) - <b>never</b> step onto a live AR field to grab a box or clear debris without following the site's safe-entry procedure. A moving drive carrying a loaded pod is heavy and quiet."
      }
    ],
    "lab": {
      "title": "Triage an AR Drive Disablement",
      "tool": "ARTS floor map (or a whiteboard walkthrough)",
      "steps": [
        "A drive shows disabled at a grid location. Read the error code first (105 vs 206 vs No Comms)",
        "Error 105: inspect the fiducial under the drive - clean (dry microfiber) or flag for replacement if corner damage > 5 mm",
        "Error 206: check the wheels for debris; clear it and inspect wheel OD for wear (< 190 mm standard / < 195 mm H-drive = replace)",
        "No Comms: verify the nearest AP status, its Ethernet cable, and the switch-port VLAN",
        "Before physically approaching: confirm the field/segment is paused or cleared per the site's AR floor-access procedure"
      ]
    },
    "quiz": [
      {
        "q": "How does an AR drive unit know its position on the floor?",
        "options": [
          "GPS",
          "It reads 2D barcode/QR fiducials laid out in a floor grid",
          "Ultrasonic beacons",
          "Dead reckoning only"
        ],
        "answer": 1,
        "explain": "Drives read floor fiducials (2D barcode/QR markers) with a downward camera. Smeared or damaged fiducials cause navigation errors."
      },
      {
        "q": "An AR drive throws error 105. What is the most likely cause and fix?",
        "options": [
          "Low battery - swap battery",
          "Fiducial read failure - clean the fiducial (dry microfiber) or replace if corner damage > 5 mm",
          "Motor fault - replace motor",
          "Network outage - reboot switch"
        ],
        "answer": 1,
        "explain": "Error 105 = fiducial read failure. Clean QR codes with dry microfiber (no solvents); replace any fiducial with corner damage > 5 mm."
      },
      {
        "q": "Using DUDT's Wheel Wear function, you should replace a standard drive's wheels when the OD drops below:",
        "options": [
          "150 mm",
          "190 mm",
          "220 mm",
          "250 mm"
        ],
        "answer": 1,
        "explain": "Replace standard-drive wheels below 190 mm OD (195 mm for H-drive). Worn wheels raise motor current and cause navigation drift."
      },
      {
        "q": "What does LCRM (Low Charge Regime Manager) do?",
        "options": [
          "Speeds up all drives",
          "Reduces MDIPF to hold drives in reserve for charging when fleet charge drops",
          "Disables chargers",
          "Increases pod weight limits"
        ],
        "answer": 1,
        "explain": "LCRM automatically lowers MDIPF (Max Drives In Play Fraction), parking drives in reserve to protect charge - enabled everywhere except lead-acid (R) drives and LVM zones."
      },
      {
        "q": "An automatic Sev-3 ticket fires when the drive-to-charger ratio exceeds:",
        "options": [
          "10:1 for 10 minutes",
          "26:1 for 90+ continuous minutes",
          "5:1 instantly",
          "50:1 for a full shift"
        ],
        "answer": 1,
        "explain": "A Sev-3 fires when drive:charger ratio exceeds 26:1 for 90+ continuous minutes. Recommended per-model maxes are lower (e.g. Hercules 25:1, Titan 21:1)."
      },
      {
        "q": "The #1 cause of drive disablements during peak is:",
        "options": [
          "Software bugs",
          "Floor debris (cardboard, strapping, labels) fouling wheels",
          "Operator error",
          "Charger failures"
        ],
        "answer": 1,
        "explain": "Floor debris is the top disablement cause during peak - it triggers error 206 (wheel obstruction). Run hourly floor walks and clear with compressed air."
      },
      {
        "q": "Drives show 'No Comms' in ARTS. What do you check?",
        "options": [
          "The pod weight",
          "AP status, Ethernet to the AP, and switch-port VLAN assignment",
          "The floor fiducials",
          "The charger LED"
        ],
        "answer": 1,
        "explain": "Check access-point (AP) status on the floor map, the Ethernet cable to the AP, and the VLAN on the switch port - AR drives use a dedicated VLAN."
      },
      {
        "q": "Before physically approaching a disabled drive on the AR field, you must:",
        "options": [
          "Just walk out and grab it",
          "Follow the site's AR floor-access / safe-entry procedure (field paused or segment cleared, authorization/vest)",
          "Wait for the drive to move",
          "Turn off the whole building"
        ],
        "answer": 1,
        "explain": "The AR floor is a restricted controlled space. Always follow the site's floor-access procedure - a loaded pod-carrying drive is heavy and quiet. Never enter a live field unprocedurally."
      }
    ],
    "resources": [
      {
        "name": "Amazon Robotics (overview)",
        "url": "https://www.aboutamazon.com/news/operations/amazon-robotics"
      },
      {
        "name": "Autonomous Mobile Robots - A3 Association",
        "url": "https://www.automate.org/robotics/mobile-robots"
      },
      {
        "name": "ARTS / DUDT (internal AR tech portal)",
        "url": "https://www.aboutamazon.com/news/operations/amazon-robotics"
      }
    ]
  }
]
