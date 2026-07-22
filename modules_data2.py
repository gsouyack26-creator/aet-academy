"""AET Course modules 6-12"""

MODULES_2 = [
  {
    "id": 6, "title": "Fluid Power - Pneumatics & Hydraulics",
    "objectives": ["Read ISO 1219 fluid-power symbols","Design pneumatic circuits with DCVs and cylinders","Apply Pascal's law for hydraulic force/speed","Troubleshoot fluid-power faults"],
    "sections": [
      {"h": "Pneumatics", "body": "<b>Supply:</b> Compressor - receiver - FRL (Filter/Regulator/Lubricator) - valve - actuator.<br><b>DCVs:</b> 3/2, 5/2, 5/3 (ports/positions). Actuation: solenoid, pilot, spring-return.<br><b>5/2 valve:</b> Controls double-acting cylinder. <b>Flow control:</b> Meter-out preferred (smooth motion via back-pressure)."},
      {"h": "Hydraulics", "body": "<b>Pascal's Law:</b> F = P x A.<br><i>Example:</i> 2000 PSI, 3in bore: A=pi(1.5^2)=7.07in2. F=14,137 lbs.<br><b>Components:</b> Reservoir - Pump - Relief valve - DCV - Actuator - Filter - return.<br><b>Speed:</b> v = Q/A. <b>Differences from pneumatics:</b> incompressible, much higher forces, needs return lines, heat management."},
      {"h": "Symbols & Circuits", "body": "ISO 1219: squares=valve positions, arrows=flow, T=blocked, triangles=actuators (filled=hydraulic, empty=pneumatic).<br><b>Common circuits:</b> Extend/retract, speed control (meter-out), sequencing, regenerative (hydraulic fast-extend)."},
      {"h": "Troubleshooting", "body": "<b>Pneumatic:</b> No motion=check supply/FRL/solenoid. Slow=flow restriction/leaks. Erratic=moisture/worn spool.<br><b>Hydraulic:</b> No motion=low fluid/pump fail/relief stuck. Slow=internal leak/high temp. Noisy pump=cavitation. Overheating=relief cracking/blocked cooler."}
    ],
    "lab": {"title": "Design Pick-and-Place Circuit", "tool": "Pen/paper (ISO 1219 schematic)", "steps": ["Design 2-cylinder circuit: A(vertical lift) + B(horizontal extend)","Sequence: B extend - A extend(grip) - B retract - A retract(place)","Draw ISO 1219 schematic with FRL, 2x 5/2 valves, 2 cylinders, 4 limit switches","Add meter-out flow controls","Write PLC sequence (4 steps + transitions)"]},
    "quiz": [
      {"q": "Hydraulic cylinder, 4in bore, 1500 PSI. Extend force?", "options": ["6000 lbs","18,850 lbs","4712 lbs","1500 lbs"], "answer": 1, "explain": "A = pi(2^2) = 12.57in2. F = 1500 x 12.57 = 18,850 lbs."},
      {"q": "Why meter-OUT preferred in pneumatics?", "options": ["Saves air","Smoother motion via back-pressure","Cheaper","More force"], "answer": 1, "explain": "Back-pressure on exhaust controls piston speed smoothly. Meter-in causes jerky motion."},
      {"q": "5/2 valve means:", "options": ["5 PSI, 2 gal","5 ports, 2 positions","5 cylinders, 2 valves","Size 5 type 2"], "answer": 1, "explain": "5 ports (P,A,B,EA,EB) and 2 positions."}
    ],
    "resources": [{"name":"Festo Didactic","url":"https://www.festo.com/us/en/e/technical-education"},{"name":"LibreTexts - Fluid Power","url":"https://eng.libretexts.org/"},{"name":"SMC Pneumatics","url":"https://www.smcusa.com/"}]
  },
  {
    "id": 7, "title": "HMI / SCADA Systems",
    "objectives": ["Design effective HMI screens (ISA-101 principles)","Configure tags linking HMI to PLC data","Implement alarm management (ISA-18.2)","Set up trending/data logging"],
    "sections": [
      {"h": "HMI vs SCADA", "body": "<b>HMI:</b> Local operator panel at machine (PanelView, Comfort Panel, PC-based).<br><b>SCADA:</b> Plant-wide, aggregates multiple PLCs, historian, dashboards, remote. Examples: FactoryTalk View SE, WinCC, Ignition, Wonderware.<br><b>Modern trend:</b> Web-based (Ignition Perspective, AVEVA) - HTML5 clients."},
      {"h": "Screen Design (ISA-101)", "body": "<b>Hierarchy:</b> L1 Overview - L2 Area - L3 Detail - L4 Diagnostic.<br><b>Principles:</b> Gray background, color for STATE only (green=run, red=fault, yellow=warn), minimal animation, 3-click max depth, 40x40px touch targets."},
      {"h": "Tags", "body": "Tags = named data points linking HMI to PLC. Types: Analog (INT/REAL), Discrete (BOOL), String. HMI polls PLC via protocol (EtherNet/IP, OPC-UA, Modbus TCP)."},
      {"h": "Alarms (ISA-18.2)", "body": "<b>States:</b> Normal - Unacknowledged - Acknowledged - RTN (clear).<br><b>Priorities:</b> 1=Critical, 2=High, 3=Medium, 4=Low.<br><b>Target:</b> <=10 alarms/hr normal; <=2 standing. <b>Shelving:</b> Temp suppress nuisance alarm (time-limited, audited)."}
    ],
    "lab": {"title": "Build an HMI Screen", "tool": "FUXA (free, open-source) or pen/paper", "steps": ["Install FUXA (free, open-source web SCADA/HMI) - or sketch the screen on paper","Create pump station: 1 pump, level + pressure transmitters","Build detail screen: pump status, Start/Stop, level bar, pressure numeric","Add 3 alarms: High Level (P2), Low Level (P3), Pump Fault (P1)","Add trend chart (level + pressure, 30 min)"]},
    "quiz": [
      {"q": "Recommended HMI background color?", "options": ["Bright blue","Black","Gray (neutral)","White"], "answer": 2, "explain": "Gray reduces fatigue, makes status colors stand out."},
      {"q": "ISA-18.2 target alarm rate?", "options": ["100/hr","10/hr during normal operation","1/day","Unlimited"], "answer": 1, "explain": "<=10 alarms/hr normal; higher = alarm fatigue."},
      {"q": "HMI tags vs PLC tags?", "options": ["Same thing","HMI tags reference PLC tags via comm protocol","HMI has no tags","PLC tags are motor-only"], "answer": 1, "explain": "HMI tags are linked copies that poll PLC data via protocol."}
    ],
    "resources": [{"name":"FUXA - open-source SCADA/HMI","url":"https://github.com/frangoteam/FUXA"},{"name":"RealPars - HMI/SCADA","url":"https://www.realpars.com/"},{"name":"ISA Standards","url":"https://www.isa.org/standards-and-publications"}]
  },
  {
    "id": 8, "title": "Industrial Networks & Fieldbus",
    "objectives": ["Compare device/control/enterprise network levels","Configure Ethernet/IP communication","Explain OPC-UA and IIoT role","Troubleshoot network issues"],
    "sections": [
      {"h": "Network Levels", "body": "<b>Device:</b> Sensor/actuator to controller (IO-Link, AS-i, DeviceNet).<br><b>Control:</b> PLC-PLC, PLC-HMI, PLC-drives (EtherNet/IP, PROFINET, Modbus TCP, EtherCAT).<br><b>Enterprise:</b> Plant to business (standard TCP/IP, OPC-UA bridge)."},
      {"h": "Ethernet/IP", "body": "CIP over standard Ethernet. <b>Implicit:</b> cyclic I/O (deterministic, RPI-based). <b>Explicit:</b> request/response (parameter reads). <b>Setup:</b> Static IPs, add to I/O tree, set RPI. <b>Topology:</b> Star (switches), DLR (ring for AB)."},
      {"h": "OPC-UA", "body": "Vendor-neutral, platform-independent, secure. Server (PLC/gateway) - Client (HMI/SCADA/MES/cloud). Replaces OPC-DA (COM/DCOM Windows-only). THE IIoT backbone. Encrypted, authenticated, cross-platform."},
      {"h": "Troubleshooting", "body": "<b>Tools:</b> Ping, ARP, Wireshark, switch LEDs.<br><b>Issues:</b> Duplicate IP, wrong subnet, bad cable (CRC errors), switch loop (broadcast storm), RPI too fast.<br><b>Best practices:</b> Separate control from enterprise (VLAN), managed switches, document IPs, label cables."}
    ],
    "lab": {"title": "IP Address Planning", "tool": "Pen/paper + optional Wireshark", "steps": ["Design IP scheme: PLC=.10, HMI=.11, VFD=.20, Remote IO=.30, Gateway=.100 on 192.168.1.0/24","Document in table: Device, IP, Subnet, Function","Discuss: why NOT DHCP for control devices?","Optional: capture traffic with Wireshark, filter for CIP packets"]},
    "quiz": [
      {"q": "RPI in EtherNet/IP controls:", "options": ["Cable type","How often I/O data is exchanged (ms)","Voltage level","Routing priority"], "answer": 1, "explain": "RPI = Requested Packet Interval (ms between cyclic exchanges)."},
      {"q": "OPC-UA replaced OPC-DA mainly because:", "options": ["Faster","Vendor-neutral, cross-platform, secure (no COM/DCOM)","Less bandwidth","Microsoft required it"], "answer": 1, "explain": "No COM/DCOM dependency; works on Linux/embedded; encrypted."},
      {"q": "Can't ping new VFD. First step?", "options": ["Replace VFD","Check IP/subnet and physical link LED","Reboot PLC","Call vendor"], "answer": 1, "explain": "Check physical layer and IP config first."}
    ],
    "resources": [{"name":"OPC Foundation","url":"https://opcfoundation.org/"},{"name":"Wireshark","url":"https://www.wireshark.org/"},{"name":"RealPars - Networking","url":"https://www.realpars.com/"}]
  },
  {
    "id": 9, "title": "Robotics & Motion Control",
    "objectives": ["Identify robot types and applications","Explain coordinate frames and motion types","Program basic pick-and-place operations","Apply robot safety standards (ISO 10218, R15.06)"],
    "sections": [
      {"h": "Robot Types", "body": "<b>6-axis Articulated:</b> Most versatile (welding, palletizing, tending).<br><b>SCARA:</b> 4-axis, fast horizontal assembly.<br><b>Delta:</b> Very fast pick-and-place, light payload.<br><b>Cartesian/Gantry:</b> Linear axes, large CNC/palletizing.<br><b>Cobot:</b> Shared workspace, force-limited."},
      {"h": "Frames & Motion", "body": "<b>World/Base/Tool(TCP)/User frames.</b><br><b>Joint:</b> Each axis shortest path (fastest, curved).<br><b>Linear:</b> TCP straight line (predictable).<br><b>Circular:</b> TCP traces arc (3 points)."},
      {"h": "Programming", "body": "Teach pendant: jog to position, record points, write program.<br><b>FANUC example:</b><br><pre>1: J P[1] 100% FINE\n2: L P[2] 500mm/sec CNT50\n3: L P[3] 100mm/sec FINE\n4: RO[1]=ON (gripper)\n5: L P[2] 500mm/sec CNT50\n6: J P[4] 100% CNT100\n7: L P[5] 100mm/sec FINE\n8: RO[1]=OFF</pre>FINE=stop at point, CNT=continuous."},
      {"h": "Safety", "body": "<b>ISO 10218-1/-2:</b> Robot/system safety requirements.<br><b>ANSI/RIA R15.06:</b> US integrator standard; risk assessment required.<br><b>ISO/TS 15066:</b> Cobot force/pressure limits.<br><b>Safeguarding:</b> Fencing, light curtains, safety scanners, interlocked gates.<br><b>Teach mode:</b> 250mm/sec max speed."}
    ],
    "lab": {"title": "Pick-and-Place Flowchart", "tool": "Pen/paper (flowchart)", "steps": ["Draw top-down layout: robot center, pick left, place right","Define 5 positions: Home, Pick_Approach, Pick, Place_Approach, Place","Write pseudocode program with J/L moves, gripper, waits","Identify where FINE vs CNT and explain why","List 3 safeguarding measures"]},
    "quiz": [
      {"q": "Straight-line TCP motion type?", "options": ["Joint","Linear","Circular","Random"], "answer": 1, "explain": "Linear moves TCP in a straight line."},
      {"q": "Max TCP speed in teach mode (R15.06)?", "options": ["1000mm/s","250mm/s","500mm/s","No limit"], "answer": 1, "explain": "250mm/sec max for human safety during programming."},
      {"q": "Align with angled conveyor using which frame?", "options": ["World","Base","Tool","User"], "answer": 3, "explain": "User frame aligns to a fixture/conveyor."}
    ],
    "resources": [{"name":"FANUC eLearning","url":"https://www.fanucamerica.com/support/training"},{"name":"RealPars - Robotics","url":"https://www.realpars.com/"},{"name":"RIA Safety","url":"https://www.robotics.org/"}]
  },
  {
    "id": 10, "title": "Process Control & PID",
    "objectives": ["Distinguish open-loop from closed-loop control","Explain P, I, D terms and effects","Tune a PID loop systematically","Read P&ID diagrams (ISA-5.1)"],
    "sections": [
      {"h": "Feedback Control", "body": "<b>Open loop:</b> No measurement feedback (hope it works).<br><b>Closed loop:</b> Measure PV, compare to SP, calculate error (E=SP-PV), output correction (CV). Continuously adjusts.<br><i>Example:</i> Level control: transmitter(PV) - PID controller - control valve(CV)."},
      {"h": "PID Terms", "body": "<b>P:</b> Output proportional to error. Fast but leaves offset.<br><b>I:</b> Output proportional to accumulated error. Eliminates offset but can oscillate (windup).<br><b>D:</b> Output proportional to rate of change. Reduces overshoot but amplifies noise.<br><b>Combined:</b> CV = Kp*E + Ki*integral(E) + Kd*dE/dt. Most loops use PI (D=0 for noisy processes)."},
      {"h": "Tuning", "body": "<b>Manual:</b> Set I=D=0. Increase Kp until oscillation (ultimate gain Ku, period Tu).<br>Set Kp=0.45*Ku, Ti=Tu/1.2 (Z-N PI formula).<br><b>Metrics:</b> Rise time, overshoot, settling time, steady-state error.<br><b>Anti-windup:</b> Limit integral when output saturated."},
      {"h": "P&ID (ISA-5.1)", "body": "<b>Tag format:</b> 1st letter = measured variable (T=temp, P=pressure, F=flow, L=level). Following = function (I=indicator, C=controller, T=transmitter, V=valve).<br><i>Examples:</i> FIC-101 = Flow Indicating Controller. LT-205 = Level Transmitter.<br><b>Symbols:</b> Circle=field, circle+line=panel, square=DCS/PLC."}
    ],
    "lab": {"title": "PID Simulation", "tool": "Free online PID simulator", "steps": ["Set first-order process (time const ~10s, dead time ~2s)","P-only: observe offset after SP step","Add I: observe offset eliminated","Increase Kp until oscillation, note Ku","Back off to 60% Ku, adjust Ki for <20% overshoot","Try small Kd, observe effect","Document final Kp, Ki, Kd"]},
    "quiz": [
      {"q": "Integral (I) term eliminates:", "options": ["Overshoot","Oscillation","Steady-state error (offset)","Noise"], "answer": 2, "explain": "I accumulates error to drive it to zero."},
      {"q": "P&ID tag TT-304 means:", "options": ["Temperature Transmitter loop 304","Total Throughput","Test Terminal","Timer Trigger"], "answer": 0, "explain": "T=Temp, T=Transmitter, 304=loop number."},
      {"q": "Loop oscillating steadily - what to do?", "options": ["Increase Kp","Decrease Kp","Increase Ki","Add dead time"], "answer": 1, "explain": "Oscillation = too much gain. Reduce Kp to stabilize."}
    ],
    "resources": [{"name":"MIT OCW - Control Systems","url":"https://ocw.mit.edu/"},{"name":"Control.com - PID","url":"https://control.com/"},{"name":"RealPars - PID","url":"https://www.realpars.com/"}]
  },
  {
    "id": 11, "title": "Machine Safety & Functional Safety",
    "objectives": ["Conduct basic risk assessment (severity x probability x avoidance)","Select safeguarding methods based on risk","Interpret ISO 13849-1 PL and Categories","Apply OSHA LOTO and NFPA 70E"],
    "sections": [
      {"h": "Risk Assessment", "body": "<b>ISO 12100 method:</b> Identify hazards (mechanical/electrical/thermal) - Estimate risk: S1/S2 (severity) x F1/F2 (frequency) x P1/P2 (avoidance) - Determine PLr from risk graph - Implement safeguards (eliminate > engineer > admin)."},
      {"h": "Safeguarding", "body": "<b>Hard guards:</b> Fixed barriers (first choice).<br><b>Interlocked guards:</b> Guard + safety switch; stops machine when opened.<br><b>Presence-sensing:</b> Light curtains (Type 4/Cat 4), safety scanners, safety mats.<br><b>E-stop:</b> Cat 0 or 1 stop. <b>Safety PLCs:</b> GuardLogix, PILZ PNOZ, Siemens F-CPU."},
      {"h": "ISO 13849-1", "body": "<b>Performance Level:</b> a (lowest) to e (highest PFHd).<br><b>Categories:</b> B (basic), 1 (well-tried), 2 (self-test), 3 (single-fault tolerant), 4 (single-fault tolerant + high diagnostic).<br><b>Typical:</b> PL e/Cat 4 = highest risk (robot cells). PL c/Cat 2 = moderate risk."},
      {"h": "LOTO & Arc Flash", "body": "<b>OSHA 1910.147 LOTO:</b> Notify - Shutdown - Isolate - Lock/Tag - Verify zero energy.<br><b>Stored energy:</b> Pneumatic pressure, hydraulic accumulators, springs, capacitors (VFD DC bus!).<br><b>NFPA 70E:</b> Arc-flash boundaries, PPE categories (cal/cm2). De-energize whenever possible."}
    ],
    "lab": {"title": "Risk Assessment Exercise", "tool": "Pen/paper scenario", "steps": ["Scenario: conveyor pinch point, operators reach in during operation","Identify hazards: crush/pinch, entanglement","Risk: S2 + F2 + P2 = PLr e","Select safeguards: interlocked guard + light curtain (Cat 4/PL e)","Write LOTO procedure: identify ALL energy sources, isolation points, verification"]},
    "quiz": [
      {"q": "S2+F2+P2 on risk graph = PLr?", "options": ["PL a","PL c","PL d","PL e"], "answer": 3, "explain": "Highest risk path = PLr e."},
      {"q": "After lockout, you MUST:", "options": ["Start maintenance","Verify zero energy (try start, check stored energy)","Only tag it","Wait 30 min"], "answer": 1, "explain": "Verification is mandatory - try start, check caps/pressure/springs."},
      {"q": "ISO 13849 Category 3 means:", "options": ["No safety needed","Single fault does NOT cause loss of safety function","Basic principles only","Software-only"], "answer": 1, "explain": "Cat 3 = single-fault tolerant via redundancy + diagnostics."}
    ],
    "resources": [{"name":"OSHA 1910.147","url":"https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147"},{"name":"NFPA 70E/79","url":"https://www.nfpa.org/codes-and-standards"},{"name":"PILZ Safety Knowledge","url":"https://www.pilz.com/en-US/knowledge"},{"name":"Rockwell GuardLogix","url":"https://www.rockwellautomation.com/en-us/support/documentation/literature-library.html"}]
  },
  {
    "id": 12, "title": "Capstone - System Integration & Career Paths",
    "objectives": ["Integrate all AET domains into a complete cell design","Develop a commissioning checklist","Map personal skill gaps to learning goals","Identify certification/degree pathways"],
    "sections": [
      {"h": "Integration Mindset", "body": "Real systems integrate ALL domains: Electrical + PLC + HMI + Network + Drives + Sensors + Fluid Power + Robotics + Safety.<br><b>Your job:</b> Understand interconnections. Troubleshoot ACROSS domain boundaries - the fault may be network, not PLC; mechanical, not electrical."},
      {"h": "Commissioning", "body": "<b>Pre-power:</b> Verify wiring vs drawings, check torque, megger motors, verify grounding, inspect pneumatic/hydraulic lines.<br><b>Power-on (no motion):</b> Control power only. Check PLC I/O mapping. Verify HMI comms. Ping devices.<br><b>Motion (jog):</b> Jog each axis. Verify direction. Check sensors. Test safety (E-stop, curtain, gate).<br><b>Auto:</b> Step-by-step sequence. Verify cycle time. Load product. Production run. Document settings."},
      {"h": "Career Paths", "body": "<b>Entry (AAS/certs):</b> Maintenance Tech, Automation Tech, Robotics Tech, Instrumentation Tech.<br><b>Growth (experience + BS/certs):</b> Automation Engineer (Amazon L4-L5 AE), Controls Engineer, System Integrator, Reliability Engineer, Engineering Manager.<br><b>Certifications:</b> ISA CCST L1-L3, SACA C-101/C-201, FANUC, Rockwell/Siemens, NFPA 70E QEW."},
      {"h": "Personal Development Plan", "body": "Rate yourself 1-5 on each of 10 domains. Identify bottom 3 = priority growth areas.<br><b>Action plan:</b> Domain - Current level - Target level - Resources (from this course) - Practice method - Validation (cert/project/peer review). Revisit quarterly."}
    ],
    "lab": {"title": "Design Complete Automated Cell", "tool": "Paper/whiteboard", "steps": ["Design palletizing cell: robot picks boxes from conveyor, stacks on pallet (4x3x3 layers)","Draw layout: conveyor(VFD), photoeye, robot(vacuum gripper), pallet station, safety fencing + gate + light curtain","List components by domain: Electrical, PLC I/O list, Sensors, Network IPs, Safety devices+PL","Write high-level sequence: wait-detect-pick-place-count-layer-full-signal","Create 10-item commissioning checklist","Identify which domains this touches (all 10!)"]},
    "quiz": [
      {"q": "Before applying power to a new machine:", "options": ["Run auto to check errors","Verify wiring point-to-point, check torque, megger motors, verify grounding","Just turn it on","Program PLC first"], "answer": 1, "explain": "Pre-power checks prevent catastrophic damage."},
      {"q": "HMI shows 'I/O Comm Loss' on gripper valve. First check:", "options": ["Replace robot","Network connection to remote I/O module (cable, LED, IP)","Recalibrate valve","Reprogram robot"], "answer": 1, "explain": "Comm loss = network issue. Check physical, then link, then IP."},
      {"q": "ISA CCST has how many levels?", "options": ["1","2","3","5"], "answer": 2, "explain": "ISA CCST: Level I (entry), II (experienced), III (expert)."}
    ],
    "resources": [{"name":"ISA CCST","url":"https://www.isa.org/certification"},{"name":"SACA","url":"https://www.saca.org/"},{"name":"ABET Programs","url":"https://www.abet.org/accreditation/find-programs/"},{"name":"Amazon Jobs - RME","url":"https://www.amazon.jobs/"}]
  }
]
