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
      {"h": "State Machines", "body": "<pre>CASE Machine_State OF\n  0:  (* IDLE *) IF Start AND NOT Fault THEN State:=10; END_IF;\n  10: (* STARTING *) RunSequence(); IF Done THEN State:=20; END_IF;\n  20: (* RUNNING *) IF Stop THEN State:=30; END_IF;\n      IF Fault THEN State:=99; END_IF;\n  30: (* STOPPING *) StopSeq(); IF Stopped THEN State:=0; END_IF;\n  99: (* FAULTED *) AllOff(); IF Reset AND NOT Fault THEN State:=0; END_IF;\nEND_CASE;</pre>Explicit states, clear transitions, easy debug."},
      {"h": "IEC Timers, Counters & Edge Detection in ST", "body": "In Structured Text you do not get inline TON boxes - you <b>declare a function-block instance</b> and call it every scan. The call updates the block's outputs:<br><pre>VAR\n  StartDly : TON;\n  PartCtr  : CTU;\n  BtnEdge  : R_TRIG;\nEND_VAR\n\n// On-delay: motor runs 2 s after Enable\nStartDly(IN := Enable, PT := T#2s);\nMotor := StartDly.Q;\n\n// One-shot the pushbutton, then count\nBtnEdge(CLK := Cycle_PB);\nPartCtr(CU := BtnEdge.Q, RESET := ShiftReset, PV := 500);\nFull := PartCtr.Q;   // .CV holds the running count</pre><b>Key outputs:</b> TON/TOF/TP expose <code>.Q</code> (bool) and <code>.ET</code> (elapsed TIME). Counters expose <code>.Q</code> and <code>.CV</code> (current value).<br><br><b>Why R_TRIG matters:</b> if you feed <code>CU := Cycle_PB</code> directly and the operator holds the button, the counter would increment <b>every scan</b>. <b>R_TRIG</b> converts the level into a single one-scan rising pulse so you count once per press. <b>F_TRIG</b> does the same on release.<br><br><b>Instance = memory:</b> each declared instance keeps its own state between scans. Never share one instance for two jobs, and never conditionally skip its call inside an IF that can go false mid-cycle - a timer only advances on the scans where you actually call it."},
      {"h": "Arrays, Loops & Data Processing in ST", "body": "ST shines where ladder struggles: iterating over data. Declare arrays with an index range and loop with <b>FOR</b>:<br><pre>VAR\n  Temps : ARRAY[0..9] OF REAL;\n  i     : INT;\n  Total : REAL;\n  Hi    : REAL;\nEND_VAR\n\nTotal := 0;  Hi := Temps[0];\nFOR i := 0 TO 9 DO\n  Total := Total + Temps[i];\n  IF Temps[i] &gt; Hi THEN  Hi := Temps[i];  END_IF;\nEND_FOR;\nAvg := Total / 10.0;</pre><b>Loop rules that keep the scan safe:</b><br>&bull; Always loop over a <b>fixed, bounded</b> range - never a range that a runtime value can blow up. A runaway FOR can overrun the scan watchdog and fault the processor.<br>&bull; Respect array bounds. Reading <code>Temps[10]</code> on a <code>[0..9]</code> array is an <b>out-of-bounds</b> fault (or silent corruption on some platforms). Guard the index: <code>IF i &gt;= 0 AND i &lt;= 9 THEN ...</code>.<br><br><b>FIFO / shift register</b> (shift samples down, newest at the top):<br><pre>FOR i := 9 TO 1 BY -1 DO\n  Buf[i] := Buf[i-1];\nEND_FOR;\nBuf[0] := NewSample;</pre><b>WHILE</b> and <b>REPEAT</b> exist too, but prefer bounded FOR loops in scan-based code. Use loops for recipe tables, alarm scans, checksum/CRC, and moving averages - jobs that would be dozens of near-identical rungs in ladder."},
      {"h": "Writing Robust, Scan-Safe ST", "body": "Powerful text logic is also easy to write dangerously. Rules for code that survives production:<br><br><b>1. Guard every divide.</b> <code>x / y</code> with <code>y = 0</code> faults the processor. Always <code>IF y &lt;&gt; 0 THEN ... ELSE handle;</code>.<br><b>2. Keep loops bounded.</b> No unbounded WHILE on a live signal. Every loop must have a fixed maximum iteration count so the scan cannot run away.<br><b>3. Know INPUT vs OUTPUT vs IN_OUT parameters.</b> In AOIs/functions, <b>INPUT</b> is copied in (a snapshot), <b>OUTPUT</b> is copied out, and <b>IN_OUT</b> passes by reference - the block edits your live tag directly. Use IN_OUT for large UDTs (no copy cost) but know you are mutating the caller's data.<br><b>4. Latch faults deliberately.</b> A momentary fault should <b>seal in</b> until an operator resets it - do not let it self-clear the instant the condition passes, or you will chase ghosts:<br><pre>IF FaultCond THEN  Faulted := TRUE;  END_IF;\nIF ResetBtn AND NOT FaultCond THEN  Faulted := FALSE;  END_IF;</pre><b>5. Initialize before use.</b> Sums, max/min accumulators, and indexes must be seeded each pass or they carry stale data.<br><b>6. Comment the intent, not the syntax.</b> <code>// jam if photoeye blocked &gt; 3 s</code> beats <code>// set jam true</code>. The next tech (maybe you at 3 AM) needs the <b>why</b>.<br><b>7. Avoid double-writing an output</b> from two places - same trap as ladder double-coils; the last write each scan wins.<br><br>Robust ST reads almost like the process description it implements: bounded, guarded, clearly latched, and commented for the person who has to troubleshoot it live."}
    ],
    "lab": {"title": "Build a Motor Control AOI", "tool": "OpenPLC or CODESYS (free)", "steps": ["Create UDT Motor_Ctrl: Cmd_Start, Cmd_Stop, Running, Faulted, RunTimer, FaultCode","Create FB_Motor: inputs Start/Stop/OL_Fault/E_Stop; outputs Motor_Out/Running/Faulted","Implement ST state machine: IDLE/STARTING/RUNNING/FAULTED","Test: Start (should run); OL_Fault (should fault, output off); E_Stop (immediate off)","Reuse: instantiate 3 times for 3 motors, verify independence"]},
    "quiz": [
      {"q": "Main advantage of Add-On Instructions (AOIs)?", "options": ["Run faster","Reusable tested-once logic blocks with encapsulated data","Replace all ladder","Only work in ST"], "answer": 1, "explain": "AOIs = write once, test once, reuse everywhere with consistent behavior."},
      {"q": "FAULT state in a state machine should:", "options": ["Continue running","Turn off outputs, wait for fault clear + operator reset","Power cycle PLC","Delete program"], "answer": 1, "explain": "Fault = safe state (outputs off) + require both fault cleared AND operator acknowledge before restart."},
      {"q": "AB Major Fault Type 4 indicates:", "options": ["Math overflow","I/O communication failure","Power supply issue","Download needed"], "answer": 1, "explain": "Type 4 = I/O fault (module not responding, rack power loss, RPI timeout)."},
      {"q": "In ST, why feed a pushbutton through an R_TRIG before a CTU counter?", "options": ["It makes the button respond faster", "R_TRIG converts the held level into a single one-scan pulse so you count once per press, not every scan", "R_TRIG debounces electrical noise on the input", "It is required syntax for all counters"], "answer": 1, "explain": "Without an edge trigger, a held button increments the counter every scan. R_TRIG gives one rising-edge pulse per press."},
      {"q": "A TON function-block instance in ST exposes which two outputs?", "options": [".DN and .ACC", ".Q (done) and .ET (elapsed time)", ".EN and .PRE", ".CV and .RESET"], "answer": 1, "explain": "IEC timers output .Q (the done bit) and .ET (elapsed TIME). .CV/.Q are for counters; .ACC/.PRE/.DN are the Studio 5000 ladder-tag names."},
      {"q": "Which timer HOLDS its accumulated time through a rung/power loss and needs a RES to clear?", "options": ["TON (on-delay)", "TOF (off-delay)", "RTO (retentive on-delay)", "TP (pulse)"], "answer": 2, "explain": "RTO accumulates true-time and retains it until a RES instruction zeroes it - ideal for total runtime / maintenance-hour tracking."},
      {"q": "What is the danger of an unbounded WHILE loop driven by a live signal in scan-based ST?", "options": ["It uses too much memory", "It can overrun the scan watchdog and fault the processor", "It runs slower than a FOR loop", "Nothing, it is perfectly safe"], "answer": 1, "explain": "A loop that never exits within one scan trips the watchdog timer and faults the controller. Keep every loop bounded to a fixed max iteration count."},
      {"q": "Reading Temps[10] on an array declared ARRAY[0..9] OF REAL will:", "options": ["Return 0 safely", "Cause an out-of-bounds fault or silent corruption depending on platform", "Automatically resize the array", "Wrap around to Temps[0]"], "answer": 1, "explain": "Index 10 is outside 0..9. Always guard the index (IF i >= 0 AND i <= 9) before accessing the element."},
      {"q": "For passing a large UDT into an AOI/function without a copy cost, which parameter type is best?", "options": ["INPUT (copied in)", "OUTPUT (copied out)", "IN_OUT (passed by reference)", "A local VAR"], "answer": 2, "explain": "IN_OUT passes by reference - no copy, and the block edits your live tag directly. Use it for large structures, knowing you are mutating the caller's data."}
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
      {"h": "Oscilloscope Basics", "body": "<b>When:</b> DMM shows RMS only - useless for PWM/encoder/comm signals.<br><b>VFD output:</b> See PWM pattern. Verify 3 phases present/symmetric.<br><b>Encoders:</b> Clean square waves, 90deg quadrature, Z pulse present.<br><b>Tools:</b> Fluke ScopeMeter (CAT III rated, battery, portable)."},
      {"h": "Systematic Troubleshooting Methodology: Symptom to Cause to Verified Repair", "body": "<b>Step 1 - Define the symptom exactly:</b> A conveyor E-stop is tripped versus a drive fault versus a motor that simply will not start are three different problems. Collect PLC fault codes, HMI messages, and operator observations before touching hardware.<br><b>Step 2 - Identify probable causes:</b> List every cause that could produce the symptom, then rank by probability and ease of test. On an ACY1 induction belt line, a no-run condition is 60% likely to be a control circuit issue (E-stop, safety relay, interlock) before it is a power-circuit issue.<br><b>Step 3 - Half-split:</b> Divide the circuit at its midpoint. If power is present at the mid-point, the fault is downstream; if absent, upstream. Two tests eliminate half the circuit each iteration.<br><b>Step 4 - Change one variable at a time:</b> Swapping a contactor <i>and</i> a relay simultaneously makes root cause unknown if the machine runs. Replace one component, test, then continue.<br><b>Step 5 - Verify the repair:</b> Run the system through a full duty cycle, not just a jog. Confirm no secondary faults. Log the repair in SIM-T with root cause, corrective action, and parts consumed. Documentation prevents repeat failures and feeds PM improvement."},
      {"h": "Digital Multimeter In Depth: Connections, Modes, and Input Impedance", "body": "<b>Voltage (parallel connection):</b> Always connect meter leads in parallel with the load or source - never in series. Autoranging meters like the Fluke 87V start at the highest range and step down; manually range when speed matters.<br><b>Current (series - danger):</b> To measure current the circuit <i>must be broken</i> and the meter inserted in series. The 10 A fused input is not protected on all meters; exceeding it blows the internal fuse silently. Use a clamp meter instead on ACY1 conveyor motors (&gt;5 A typical).<br><b>Resistance and continuity:</b> De-energize and discharge the circuit first. Residual capacitor charge &gt;50 V can damage a meter on ohms mode. Continuity beep confirms &lt;30 ohms on most meters.<br><b>Diode test mode:</b> Forward voltage of a good silicon diode reads 0.5-0.7 V; a shorted diode reads near 0; open diode reads OL.<br><b>Input impedance:</b> A 10 M&ohm; input impedance meter can display 30-50 VAC &quot;ghost voltages&quot; on unloaded conductors capacitively coupled to adjacent live wires - a low-impedance mode (LoZ, ~3 k&ohm;) bleeds the charge and reads near zero, confirming the conductor is truly dead.<br><b>True-RMS:</b> VFD outputs are non-sinusoidal; an average-responding meter reads 5-15% low. Fluke 87V or 289 with true-RMS accurately measures distorted waveforms on ACY1 drive outputs."},
      {"h": "Clamp Meter: Non-Contact Current, Inrush, and Load Imbalance", "body": "<b>Operating principle:</b> A split-core Hall-effect or current-transformer clamp measures the magnetic field around a single conductor. The conductor must be isolated - clamp around <i>one</i> wire only. Clamping around a two-conductor cable reads near zero because currents cancel.<br><b>Inrush measurement:</b> DOL motor starting inrush reaches 6-8x full-load amps (FLA) for the first 5-8 cycles (83-133 ms at 60 Hz). A clamp with peak-hold or inrush function (e.g., Fluke 376 FC) captures the peak without the display averaging it away. Persistent inrush &gt;10x FLA suggests a shorted winding or locked rotor.<br><b>Min/Max function:</b> Records the minimum and maximum readings over a time window. Use it unattended across a shift to catch intermittent overloads on ACY1 sortation induction belts that only spike during jam conditions.<br><b>Load imbalance:</b> Measure each phase leg of a three-phase motor feed individually. NEMA MG-1 allows a maximum voltage imbalance of 1%; a 2% voltage imbalance produces roughly 8% current imbalance and 12% additional heating. If one leg reads &gt;10% above average current, trace back to the panel for a high-resistance contact or loose lug on that phase."},
      {"h": "Insulation Resistance Testing (Megger): Procedure, Limits, and Restrictions", "body": "<b>Purpose:</b> Measures the resistance of insulation between conductors and ground using a DC voltage source high enough to stress the insulation. A standard ohmmeter (9 V) cannot reveal insulation weakness that only appears above 100 V.<br><b>Test voltages by motor rating:</b> 120/240 VAC motors &rarr; 500 VDC test; 480 VAC motors &rarr; 1000 VDC test; cables and switchgear &rarr; 500-2500 VDC depending on rated voltage. IEEE Std 43-2013 is the governing standard for motor insulation testing.<br><b>Minimum acceptable resistance:</b> IEEE 43 minimum = 1 M&ohm; per kV of rated voltage + 1 M&ohm;. For a 480 V (0.48 kV) motor: 0.48 + 1 = <b>1.48 M&ohm; minimum</b>. Values below this indicate moisture, contamination, or insulation breakdown.<br><b>Polarization Index (PI):</b> PI = (10-minute reading) / (1-minute reading). Good insulation PI &ge; 2.0; marginal 1.0-2.0; failed &lt;1.0. A PI below 2 on an ACY1 conveyor drive motor warrants further investigation before return to service.<br><b>NEVER megger:</b> Electronics, VFDs, PLCs, capacitors (discharge first), or any solid-state device. The high DC voltage destroys MOSFETs and IGBTs. Disconnect drive output terminals before meggering the motor cable."},
      {"h": "Meter Safety and CAT Ratings: Choosing the Right Tool for the Energy Level", "body": "<b>IEC 61010-1 Category ratings</b> define the transient overvoltage a meter can survive without arcing to the user:<br><ol><li><b>CAT II (600-1000 V):</b> Receptacle outlets, single-phase loads. Acceptable for 120/240 VAC panel branch circuits.</li><li><b>CAT III (600-1000 V):</b> Fixed building wiring, three-phase distribution panels, MCC bus. Required for ACY1 480 VAC motor control center work.</li><li><b>CAT IV (600-1000 V):</b> Service entrance, utility transformers, outdoor conductors. Highest protection.</li></ol><b>Higher CAT = safer</b> at the same voltage. A CAT II 1000 V meter used at a CAT III location has inadequate protection against fast transients (&gt;6000 V microsecond spikes).<br><b>Fused leads:</b> Always verify lead fuse integrity before use. Test by connecting leads to a known voltage - if the current jack fuse is blown the meter reads voltage but current mode reads OL.<br><b>PPE:</b> Per NFPA 70E, use arc-rated PPE when working on exposed energized conductors. ACY1 MCCs are typically PPE Category 2 (minimum 8 cal/cm&sup2; arc-rated clothing, face shield, hearing protection).<br><b>Live-Dead-Live:</b> Verify meter function on a known live source, then test the target circuit, then re-verify the meter on the known source. A dead meter gives a false dead reading - the leading cause of contact injuries during electrical work."},
      {"h": "Voltage-Drop Testing: Finding High-Resistance Connections a Continuity Check Misses", "body": "<b>Why continuity fails:</b> A loose lug or pitted contact may read 0.1-2 ohms - low enough to pass a continuity beep, but under 20 A load that same 1 ohm connection dissipates 400 W (P = I&sup2;R = 20&sup2; &times; 1) and creates a 20 V drop. The circuit appears wired correctly when de-energized but fails or trips under load.<br><b>Procedure:</b> With the circuit <i>energized and under load</i>, place meter leads across the suspected connection (both sides of a closed contactor, both ends of a wire lug, across a terminal strip connection). A healthy bolted connection should drop &lt;100 mV at rated current. A breaker pole should drop &lt;50 mV. A value &gt;200 mV indicates a high-resistance joint.<br><b>ACY1 example:</b> A 24 VDC control relay that pulls in on the bench but fails to hold in the field may have a 5 V drop across the PLC output terminal. Measuring from the PLC output terminal to the relay coil terminal under load reveals the drop; tracing the wire shows a corroded terminal block ferrule.<br><b>Temperature correlation:</b> Per NEC Table 310.16, a 3 AWG copper conductor at 75&deg;C ampacity is 100 A. A high-resistance connection running at elevated temperature accelerates insulation degradation in adjacent wires - early thermal imaging catches it before a fault occurs."},
      {"h": "Thermal Imaging: Detecting Loose Lugs, Overloaded Conductors, and Failing Bearings", "body": "<b>Physics:</b> All objects above absolute zero emit infrared radiation. An IR camera (FLIR E60, Ti400, etc.) converts emitted IR to a temperature map. Emissivity must be set correctly: painted metal &asymp;0.95, bare copper &asymp;0.03-0.07 (poor emitter - use electrical tape marker).<br><b>Delta-T decision thresholds (NETA MTS-2019, Table 1):</b><br><ol><li>&Delta;T 1-10&deg;C above ambient: Possible deficiency, monitor.</li><li>&Delta;T 11-20&deg;C: Investigate and plan repair.</li><li>&Delta;T 21-40&deg;C: Schedule prompt repair.</li><li>&Delta;T &gt;40&deg;C: Repair immediately - imminent failure risk.</li></ol><b>MCC lug inspection:</b> Scan ACY1 MCC panels with doors open under &ge;40% load. A hot lug at &Delta;T &gt;20&deg;C above adjacent phases indicates a loose connection - torque to manufacturer spec (typically 50-250 in-lb for 350 kcmil lugs).<br><b>Bearing condition:</b> A bearing in early-stage failure generates friction heat; healthy bearing &Delta;T vs. ambient is typically &lt;20&deg;C. A bearing at &Delta;T &gt;40&deg;C above its motor end-bell is failing. On ACY1 belt conveyor head-pulley drive motors, thermal scan replaces scheduled touch-checks and enables condition-based replacement before catastrophic failure."},
      {"h": "Reading and Tracing from Electrical Prints: Wire Numbers, Rungs, and Cross-References", "body": "<b>Ladder diagram structure:</b> Each horizontal line is a <i>rung</i>. Left vertical rail is L1 (hot); right rail is L2/N (neutral) or the return. Rungs are numbered top to bottom; columns are numbered left to right. A contact labeled <b>CR1-3</b> means Coil CR1, contact number 3 on that coil.<br><b>Wire numbers:</b> Each wire has a unique number (e.g., 1014, 2033). The same number appears wherever that conductor is connected. Trace wire 1014 from the PLC output module, through terminal strip TS-2 pin 14, to relay coil K7. Wire numbers are the thread through a complex print.<br><b>Cross-references:</b> When coil CR1 is energized, normally-open contact CR1 appears elsewhere. Print editors add a grid reference (e.g., &quot;CR1 /14&quot; = contact on sheet 1, rung 14) adjacent to the coil symbol. Always follow cross-references before assuming a circuit is open - a contact may be on a different sheet.<br><b>Wire-number conventions:</b> A common industrial scheme on Allen-Bradley AutoCAD Electrical prints uses four-digit wire numbers whose first digit encodes the voltage level - for example 1xxx = 480 VAC, 2xxx = 120 VAC control, 4xxx = 24 VDC. Where a facility follows a scheme like this you can predict the voltage on a wire before touching it - a good safety habit. Numbering conventions vary by integrator, so always confirm the legend on the print title/notes sheet first."},
      {"h": "The Five Fault Types: Open, Short, Ground, High-Resistance, and Intermittent", "body": "<b>1. Open circuit:</b> A complete break in the path. Current = 0. Voltage appears across the open (full source voltage). Confirmed by: voltmeter reads source voltage across suspected break; ohmmeter reads OL when de-energized.<br><b>2. Short circuit:</b> Unintended low-resistance path, usually phase-to-phase. Current spikes; overcurrent protection trips. Confirmed by: ohmmeter reads near 0 ohms between conductors that should be isolated; megger reads &lt;0.1 M&ohm;.<br><b>3. Ground fault:</b> Phase conductor contacts equipment ground or earth. Trips GFCI, ground-fault relay, or blows fuse depending on impedance. On a 480 V ungrounded system at ACY1, a single ground fault may not trip protection - a second ground fault on a different phase creates a phase-to-phase fault through earth. Confirmed by: megger phase-to-ground reading &lt;1 M&ohm;.<br><b>4. High-resistance connection:</b> Partial contact - current flows but with excessive voltage drop and heat. Does not trip overcurrent protection. Confirmed by: voltage-drop test &gt;200 mV across a connection under load; IR camera shows hot spot.<br><b>5. Intermittent fault:</b> Appears and disappears with vibration, temperature, or load. Hardest to find. Techniques: min/max clamp meter, PLC fault log timestamps vs. production events, thermal scan under load, wiggle-test wiring while monitoring continuity."},
      {"h": "Structured No-Run Troubleshooting: ACY1 Belt Conveyor Starter Circuit from Prints to Repair", "body": "<b>Symptom:</b> Belt conveyor BC-047 will not start. PLC output for RUN is commanded ON; motor contactor does not energize. No VFD fault active.<br><b>Step 1 - Print review:</b> Locate conveyor starter circuit on print sheet E-07. Identify power path: PLC output card O:3/2 &rarr; wire 2114 &rarr; terminal TS-4/22 &rarr; E-stop string &rarr; safety relay SR-1 &rarr; wire 2117 &rarr; contactor coil M1 &rarr; neutral 2001.<br><b>Step 2 - Half-split at safety relay SR-1 output (midpoint):</b> With PLC commanding RUN, measure 120 VAC at SR-1 output terminal. Reads 0 V. Fault is upstream of SR-1.<br><b>Step 3 - Measure PLC output terminal:</b> Reads 120 VAC - PLC output energized. Measure at TS-4/22 after the E-stop string. Reads 0 V. Fault is in the E-stop string between the PLC output and TS-4/22.<br><b>Step 4 - Walk the E-stop string:</b> Three E-stops in series on wire 2114 &rarr; 2115 &rarr; 2116. Measure each junction. Voltage disappears between E-stop ES-3 pin A1 and A2. ES-3 is at the north tail-pulley guard.<br><b>Step 5 - Inspect ES-3:</b> Guard door E-stop actuator visually reset but internal contact spring fatigued - contact resistance 4.7 k&ohm; (should be &lt;1 ohm). Confirm with voltage-drop test: 118 V drops across ES-3 contacts under 5 mA coil circuit load.<br><b>Step 6 - Repair and verify:</b> Replace ES-3 with matching Telemecanique XCSPA701 actuator. Verify 0 V drop across new contact. Conveyor starts. Log in SIM-T, update PM task to include contact resistance check on all E-stop actuators annually."}
    ],
    "lab": {"title": "Troubleshooting Scenarios", "tool": "Pen/paper scenarios", "steps": ["Scenario 1: Motor won't start, PLC output ON. Signal-trace from PLC output to motor terminals.","Scenario 2: VFD Ground Fault. What to disconnect, megger, isolate (motor vs cable vs drive)?","Scenario 3: Wrong speed. VFD cmd correct. Causes? (slip, wrong motor data, encoder fault, overload)","For each: most likely cause, first 3 checks, tools needed","Draw live-dead-live verification procedure"]},
    "quiz": [
      {"q": "Before measuring resistance with DMM:", "options": ["Set AC mode","De-energize and isolate the component","Use highest range only","Measure voltage on same leads"], "answer": 1, "explain": "NEVER measure ohms on energized circuits. De-energize, lock out, verify dead, THEN measure."},
      {"q": "Motor insulation 3 Megohms on 480V motor:", "options": ["Excellent","Caution - marginal, monitor/schedule replacement","Perfect per IEEE","Failed immediately"], "answer": 1, "explain": "Min = ~2M. 3M is above minimum but in caution zone (<100M). Monitor trend; if declining, plan replacement."},
      {"q": "Half-split troubleshooting:", "options": ["Replace half the parts","Test midpoint to find which half has the fault, repeat","Split the team","Run at half speed"], "answer": 1, "explain": "Each test eliminates half the circuit. Logarithmically efficient for long signal chains."},
      {"q": "During the half-split troubleshooting method applied to a 10-rung control circuit ladder, your first measurement should be at approximately which rung?", "options": ["Rung 1 (source end)", "Rung 5 (midpoint)", "Rung 10 (load end)", "The most accessible rung regardless of position"], "answer": 1, "explain": "The half-split method divides the circuit at its midpoint first. This eliminates half the circuit with one measurement. Testing from one end takes up to 10 measurements to find a single fault; half-split finds it in log2(10) approximately 4 measurements."},
      {"q": "You measure 45 VAC on an unloaded conductor you believe is de-energized. What is the most likely cause and the correct tool setting to confirm?", "options": ["A real 45 V source; use VAC range to confirm", "Ghost voltage from capacitive coupling; switch meter to LoZ (low-impedance) mode", "Inductive kick from a nearby relay; use a clamp meter instead", "Meter fuse is blown; replace the fuse"], "answer": 1, "explain": "A 10 Mohm input impedance meter can display ghost voltages (typically 10-60 VAC) on de-energized conductors capacitively coupled to adjacent live wires. Low-impedance mode (approx 3 kohm) bleeds the capacitive charge and reads near zero if the conductor is truly dead."},
      {"q": "A 480 VAC conveyor drive motor megger test at 1000 VDC returns a 1-minute reading of 0.9 Mohm. Per IEEE Std 43-2013, this motor should be:", "options": ["Returned to service; 0.9 Mohm exceeds the 0.5 Mohm minimum", "Tagged out; it fails the 1 Mohm-per-kV+1 rule (minimum 1.48 Mohm for 480 V)", "Tested again at 500 VDC; 1000 VDC is too high for 480 V motors", "Accepted if Polarization Index exceeds 4.0"], "answer": 1, "explain": "IEEE 43-2013 minimum = 1 Mohm per kV of rated voltage + 1 Mohm. For a 480 V (0.48 kV) motor: 0.48 + 1 = 1.48 Mohm minimum. A reading of 0.9 Mohm falls below this threshold regardless of PI, indicating insulation degradation."},
      {"q": "When using a clamp meter to check three-phase load balance on a conveyor motor, Phases A, B, and C read 18 A, 18 A, and 26 A respectively. What does this indicate?", "options": ["Normal variation; all phases within 50% is acceptable per NEMA MG-1", "Phase C has a high-resistance connection upstream; trace back to the panel", "The motor has an open winding on Phase C", "The clamp is positioned incorrectly; re-clamp around all three conductors"], "answer": 1, "explain": "Phase C draws 44% more current than the average (20.7 A), which far exceeds the roughly 10% tolerance for load imbalance. An open or high-resistance connection on the Phase C feed causes lower voltage on that phase, increasing current drawn. An open winding would show near-zero current, not elevated current. Re-clamping around all three conductors would cancel and read near zero."},
      {"q": "You are working on an energized 480 VAC MCC in ACY1. Which CAT rating is the minimum acceptable for your digital multimeter?", "options": ["CAT I 600 V", "CAT II 600 V", "CAT III 600 V", "CAT IV 300 V"], "answer": 2, "explain": "IEC 61010-1 CAT III covers fixed building wiring and motor control centers at 480 VAC three-phase distribution. CAT II is for branch-circuit outlets. CAT I is for electronic equipment only. CAT IV 300 V has lower absolute voltage rating than needed. CAT III 600 V or 1000 V is correct for MCC work."},
      {"q": "A voltage-drop test across a closed contactor main contact under full motor load reads 480 mV. What does this indicate?", "options": ["Normal; less than 500 mV is acceptable for contactors", "High resistance in the contact; healthy contacts should drop less than 100 mV", "The contactor is de-energized; a closed contact cannot have voltage across it", "Meter leads are connected backwards; reverse polarity"], "answer": 1, "explain": "A healthy bolted contactor main contact should drop less than 100 mV at rated current. A 480 mV drop indicates contact pitting or loose contact pressure, creating a high-resistance joint that generates heat and could lead to arc damage or nuisance trips. This fault would not be caught by a continuity check when de-energized."},
      {"q": "Per NETA MTS-2019 Table 1, a thermal scan of ACY1 MCC lugs shows Phase B at 62 deg C and Phases A and C at 38 deg C (ambient 25 deg C). Delta-T for Phase B above adjacent phases is approximately 24 deg C. What action is required?", "options": ["No action; less than 40 deg C delta-T is acceptable", "Monitor; possible deficiency but within normal range", "Schedule prompt repair within the next maintenance window", "Immediate repair; greater than 40 deg C delta-T indicates imminent failure"], "answer": 2, "explain": "NETA MTS-2019 Table 1 delta-T thresholds: 1-10 deg C = monitor; 11-20 deg C = investigate; 21-40 deg C = schedule prompt repair; greater than 40 deg C = repair immediately. A 24 deg C delta-T falls in the 21-40 deg C band, requiring scheduled prompt repair."},
      {"q": "On an ACY1 Allen-Bradley AutoCAD Electrical print, wire number 4033 is encountered. Without seeing the circuit, what voltage level does this wire carry by the ACY1 wire-numbering convention?", "options": ["480 VAC", "120 VAC control", "24 VDC", "Signal/analog level"], "answer": 2, "explain": "ACY1 wire-numbering convention assigns the first digit to voltage level: 1xxx = 480 VAC, 2xxx = 120 VAC control, 4xxx = 24 VDC. Wire 4033 begins with 4, indicating 24 VDC. This allows technicians to predict the voltage on any wire before contact, a critical safety practice."},
      {"q": "A 480 VAC ungrounded delta system in ACY1 has a single phase-to-ground fault on Phase A. What is the immediate danger?", "options": ["Immediate trip of the main breaker due to ground fault current", "No immediate danger; single fault may not trip protection, but a second fault on another phase creates a phase-to-phase fault through ground", "Voltage on Phases B and C drops to zero", "Motor insulation breaks down immediately on all connected equipment"], "answer": 1, "explain": "On an ungrounded delta system, a single phase-to-ground fault may not provide sufficient current to trip protective devices. The real hazard is the second ground fault: if Phase A is grounded and Phase C then faults to ground, a near-phase-to-phase voltage appears across the fault path through earth, causing high fault current and potential equipment damage."},
      {"q": "The Polarization Index (PI) for a 480 V conveyor motor returns 10-minute reading of 120 Mohm and 1-minute reading of 110 Mohm. PI = 1.09. How should this result be interpreted?", "options": ["Excellent insulation; PI above 1.0 is acceptable", "Marginal insulation; PI between 1.0 and 2.0 warrants further investigation", "Failed insulation; PI below 2.0 means the motor must be rewound immediately", "Invalid test; PI cannot be calculated from a 1-minute and 10-minute reading"], "answer": 1, "explain": "IEEE 43-2013 PI classification: PI greater than or equal to 2.0 = good; PI 1.0-2.0 = marginal (investigate further); PI less than 1.0 = failed. A PI of 1.09 is marginal - the insulation resistance is not increasing significantly over time, suggesting moisture or contamination. The motor should be investigated but does not require immediate rewinding."},
      {"q": "During the Live-Dead-Live verification procedure, after testing a suspected dead circuit you re-test the meter on a known live source and get no reading. What must you conclude?", "options": ["The target circuit is confirmed dead", "The meter failed between measurements; the dead reading on the target circuit is unreliable", "The known live source has also de-energized", "The meter fuse is intact; proceed with work on the circuit"], "answer": 1, "explain": "Live-Dead-Live requires the meter to function correctly on a known source before AND after testing the target. If the meter fails the post-test live check, it means the meter malfunctioned (blown fuse, failed lead, dropped meter) at some point during the test. The dead reading on the target cannot be trusted. A failed post-test is the scenario that prevents contact with an energized conductor."},
      {"q": "In the ACY1 BC-047 troubleshooting example, voltage was present at the PLC output terminal but absent at terminal TS-4/22. The E-stop string runs between these two points with three E-stops in series. Using half-split, which E-stop should be measured first?", "options": ["ES-1 (first in series from the PLC output)", "ES-2 (midpoint of the three-E-stop string)", "ES-3 (last before TS-4/22)", "All three simultaneously by measuring phase-to-neutral"], "answer": 1, "explain": "With three E-stops in series (ES-1, ES-2, ES-3), the midpoint is between ES-1 and ES-2. Measuring the junction between ES-1 and ES-2 first eliminates half the string: if voltage is present, fault is downstream (ES-2 or ES-3); if absent, fault is at ES-1. This finds the fault in 2 measurements instead of up to 3 sequential measurements from one end."}
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
      {"h": "PM Program Design", "body": "<b>Steps:</b> 1) Asset criticality (A/B/C). 2) Failure mode analysis. 3) Task selection (predict vs prevent). 4) Schedule (balance across shifts). 5) Execute + document in CMMS. 6) Improve (extend intervals if PM finds nothing; shorten if failures occur between)."},
      {"h": "The Maintenance Strategy Spectrum", "body": "<b>Reactive (Run-to-Failure, RTF):</b> No planned action; repair after breakdown. Acceptable only for non-critical, easily replaced assets with no safety or throughput impact (e.g., a spare light fixture). Cost is low upfront but high when failure causes line stoppage.<br><br><b>Preventive (PM):</b> Time- or usage-based tasks performed on a fixed schedule regardless of condition (e.g., replace conveyor belt every 12 months, lubricate bearings every 500 hr). Prevents wear-out failures but risks over-maintenance and introduces infant-mortality risk from unnecessary disassembly.<br><br><b>Predictive (PdM):</b> Condition-based monitoring (vibration, IR, oil, ultrasonic, MCA) detects degradation before failure. Task is triggered only when a threshold is crossed, maximizing run time and minimizing unnecessary downtime.<br><br><b>Reliability-Centered Maintenance (RCM):</b> Structured process (SAE JA1011) that selects the best strategy for each failure mode based on consequence and detectability. Output is a justified mix of RTF, PM, PdM, and redesign. ACY1 uses RCM logic when building EAM/APM task lists for critical MHE assets."},
      {"h": "The Bathtub Curve and Failure Patterns", "body": "The classical bathtub curve plots failure rate vs. time in three zones:<br><ol><li><b>Infant Mortality (burn-in):</b> High early failure rate caused by manufacturing defects, improper installation, or inadequate break-in lubrication. Example: a newly installed VFD output IGBT may fail within the first 72 hr of operation if a gate-driver defect exists.</li><li><b>Useful Life (constant hazard):</b> Random, low, relatively flat failure rate. Most failures here are extrinsic (overload, contamination, operator error) rather than age-driven. <b>Statistical key:</b> electronic components overwhelmingly occupy this zone; scheduling replacement by age does NOT reduce their failure rate.</li><li><b>Wear-Out:</b> Rising failure rate driven by fatigue, corrosion, or cumulative degradation. Mechanical components (bearings, belts, gears) do wear out; replacement at or before this onset is justified.</li></ol>Nowlan &amp; Heap (1978, United Airlines) found only ~11% of equipment items show classic wear-out patterns. The remaining 89% fail randomly or with infant-mortality profiles, underpinning the shift from fixed-interval PM to condition-based PdM for electronic and complex assemblies."},
      {"h": "The P-F Curve and P-F Interval", "body": "The P-F (Potential Failure to Functional Failure) curve describes how asset condition degrades from first detectable anomaly (point P) to complete loss of function (point F). The <b>P-F interval</b> is the time window between P and F; PdM must sample at intervals &lt; P-F/2 to ensure detection before failure.<br><br>Example for an ACY1 sorter drive bearing: ultrasonic pen detects early sub-surface fatigue at P (~8 weeks before failure); vibration spectrum shows high-frequency bearing defect frequency at ~5 weeks; audible noise appears at ~2 weeks; functional failure (seizure, line stop) at F. By detecting at P, the team gains 8 weeks of lead time for planned replacement during a scheduled window, avoiding a $15,000+ emergency outage cost.<br><br>Selecting the right PdM technology depends on where in the P-F curve you want to detect: ultrasound and oil analysis detect earliest; vibration is mid-curve; temperature and visual are late-curve. Combining technologies extends the detection window and reduces risk of missing a fast-developing failure mode."},
      {"h": "Vibration Analysis - FFT and Characteristic Frequencies", "body": "Vibration analysis is the primary PdM tool for ACY1 rotating equipment. A transducer (accelerometer, ICP type, sensitivity ~100 mV/g) mounts on the bearing housing. The <b>FFT (Fast Fourier Transform)</b> converts a time-domain waveform into a frequency spectrum, revealing discrete fault frequencies:<br><br><b>Imbalance:</b> Dominant 1x running speed (1x RPM). Phase is steady; single-plane correction reduces it &gt;80%.<br><b>Misalignment:</b> Elevated 1x and 2x RPM; angular misalignment also shows axial vibration. Laser alignment to within 0.05 mm/100 mm eliminates it.<br><b>Bearing defect frequencies</b> (BPFO, BPFI, BSF, FTF) calculated from bearing geometry and shaft speed, typically 3x-20x RPM. BPFO (outer race) = (N/2) x RPM x (1 - d/D x cos&alpha;).<br><b>Looseness:</b> Sub-harmonics (0.5x, 0.33x) and high harmonics; classic truncated waveform.<br><br>ISO 10816-3 provides velocity severity bands: &lt;2.3 mm/s RMS = Good; 2.3-4.5 = Satisfactory; 4.5-11.2 = Unsatisfactory; &gt;11.2 = Unacceptable for Group 1 machines (&gt;15 kW, &gt;600 RPM)."},
      {"h": "Infrared Thermography - Electrical and Mechanical Applications", "body": "Infrared (IR) cameras detect surface temperature anomalies without contact. NFPA 70B and IEEE Std 145-1983 guide electrical thermography programs. All IR scans of electrical panels must be performed under <b>minimum 40% load</b>; scanning under light load misses real hot spots.<br><br><b>Electrical applications:</b> Loose or oxidized connections develop elevated resistance; by P = I&sup2;R, current flow produces heat. A 3-phase motor starter with one loose lug shows a thermal delta-T vs. a reference phase. NETA severity:<br>&bull; Delta-T 1-10&deg;C: monitor<br>&bull; Delta-T 11-20&deg;C: repair within 30 days<br>&bull; Delta-T &gt;20&deg;C: immediate action<br><br><b>Mechanical applications:</b> Overloaded or failing bearings on conveyor head pulleys and sorter drives show temperature rise 15-40&deg;C above ambient before audible noise develops. Misaligned couplings generate friction heat, visible as a hot stripe across the coupling gap. An ACY1 sorter induction motor coupling running at +35&deg;C above ambient indicates imminent failure requiring a planned shutdown within one shift."},
      {"h": "Oil Analysis and Ultrasonic Inspection", "body": "<b>Oil Analysis:</b> Wear-metal spectroscopy (ICP-OES) identifies elements released by component wear: Fe (gears, shafts), Cu (bronze bushings), Al (housings), Pb/Sn (babbitt bearings). Trending increasing Fe ppm in a gearbox sample over 3 consecutive intervals signals abnormal gear wear before vibration changes. Key additional tests: viscosity (ISO grade verification), water content (&lt;0.1% acceptable), particle count (ISO 4406 cleanliness code), and acid number (AN) for oxidation.<br><br><b>Airborne Ultrasound (40 kHz):</b> Detects compressed-air leaks (a 1/16-in orifice at 100 psi wastes ~25 CFM), steam trap failure (open bypass), and electrical arcing/corona in switchgear without opening panels. Structure-borne ultrasound via a contact probe detects early bearing fatigue as a rise in dBuV readings (ASTM standard instrument response). For grease replenishment, listening with ultrasound while slowly adding grease prevents over-lubrication: noise level drops then rises when fully lubricated - stop at the drop point. Over-greasing is a top bearing-failure cause at ACY1."},
      {"h": "Motor Circuit Analysis (MCA) and Insulation Testing", "body": "<b>Megger (insulation resistance, IR test):</b> Apply 500 V DC (motors &lt;1 kV) or 1000 V DC (motors 1-5 kV) between winding and ground per IEEE Std 43-2013. Minimum acceptable IR = [(kV + 1) M&Omega;] or 100 M&Omega; minimum for motors &gt;1 kV. <b>Polarization Index (PI)</b> = IR at 10 min / IR at 1 min; PI &lt;2.0 indicates contaminated or deteriorated insulation (rewind threshold). Trend IR over time; a 50% drop from baseline warrants investigation.<br><br><b>Motor Circuit Analysis (MCA):</b> Tests at de-energized state: measures winding resistance (balance within 1%), inductance balance, capacitance, impedance, and insulation-to-ground. An ACY1 460 V, 15 hp conveyor drive motor with inductance imbalance &gt;5% between phases indicates a developing winding turn-to-turn fault. MCA is trended over time (months to years); a 20% degradation in any parameter from baseline triggers investigation. Unlike megger alone, MCA can detect early inter-turn shorts before insulation-ground failure develops."},
      {"h": "PM Task Development and Interval Optimization", "body": "PM task development follows a structured process: (1) <b>Identify failure modes</b> for each asset (FMEA); (2) <b>Determine task type</b>: on-condition (PdM), scheduled discard/replacement, scheduled restoration, or failure-finding; (3) <b>Set interval</b> using manufacturer data, historical MTBF, P-F interval, or reliability engineering. Interval sources in order of preference: P-F interval analysis, historical failure data (Weibull fit), OEM recommendation.<br><br><b>Interval basis:</b> Fixed-time (calendar), fixed-cycle (belt conveyor feet traveled, motor starts), or condition trigger. ACY1 uses EAM to track both calendar and meter-based triggers.<br><br><b>Over-maintenance risk:</b> Unnecessarily frequent PM introduces infant mortality (assembly errors), uses labor, and consumes parts budget. Example: replacing a healthy V-belt on a 90-day schedule when its P-F interval is 6 months wastes 3 replacement cycles per year. PM optimization (PMO) reviews each task: if no failure has been prevented in 3 years, extend interval or convert to PdM. The goal is the <b>minimum PM that sustains reliability</b>, not maximum wrench time."},
      {"h": "Reliability KPIs - MTBF, MTTR, Availability, and OEE", "body": "<b>MTBF</b> (Mean Time Between Failures) = Total uptime / Number of failures. A conveyor segment runs 7,000 hr/yr with 4 unplanned stops: MTBF = 1,750 hr.<br><b>MTTR</b> (Mean Time To Repair) = Total repair time / Number of repairs. Four repairs totaling 8 hr: MTTR = 2 hr.<br><br><b>Availability:</b><br><pre>A = MTBF / (MTBF + MTTR)\nA = 1750 / (1750 + 2) = 99.89%</pre><br><b>OEE</b> (Overall Equipment Effectiveness) = Availability x Performance x Quality.<br><pre>A = 0.92, P = 0.95, Q = 0.99\nOEE = 0.92 x 0.95 x 0.99 = 0.865 = 86.5%</pre>World-class OEE is &ge;85%. ACY1 sorter OEE below 80% triggers a reliability review in APM. MTTR is most directly improved by parts availability, procedure clarity, and technician training. MTBF improvement requires root-cause elimination (redesign, PdM, better lubrication)."},
      {"h": "CMMS/EAM, Asset Criticality, and PM Compliance at ACY1", "body": "ACY1 uses <b>EAM (Enterprise Asset Management)</b> as the CMMS and <b>APM (Asset Performance Management)</b> for predictive analytics and condition monitoring trend data. <b>Work-order flow:</b> PM trigger (schedule or condition) &rarr; WO created in EAM &rarr; planner assigns labor/parts &rarr; tech executes &rarr; findings recorded &rarr; WO closed with actual hours and failure codes. Failure coding (using AIMMS taxonomy: object, problem, cause) enables MTBF trending and bad-actor analysis.<br><br><b>Asset Criticality Ranking:</b> Each asset scored on safety impact, throughput impact, redundancy, and mean downtime cost. Score drives PM frequency and PdM investment. ACY1 sorter drives and induction motors are typically Criticality A (highest); roller conveyor segments may be B or C depending on bypass capability.<br><br><b>PM compliance</b> metric = WOs completed on time / WOs scheduled x 100%. ACY1 RME target is &ge;90%. Compliance below 80% indicates resourcing or planning issues and correlates with higher reactive-maintenance rates. APM dashboards surface PM compliance, open defects, and condition-alert counts daily for RME leadership review."}
    ],
    "lab": {"title": "PM Program Design", "tool": "Spreadsheet or pen/paper", "steps": ["Pick 3 site assets (motor, divert, pneumatic cylinder)","List 2-3 failure modes + warning signs each","Assign strategy (reactive/PM/PdM) with justification","Define task, tools, interval for each PM","Calculate: MTBF=2000hr, MTTR=4hr, Availability=? (99.8%)","Discuss: how would vibration monitoring change MTBF/MTTR?"]},
    "quiz": [
      {"q": "1x RPM vibration on a motor indicates:", "options": ["Bearing failure","Imbalance (most common)","Electrical fault","Cavitation"], "answer": 1, "explain": "1x RPM = shaft speed frequency = rotor imbalance. Most common vibration problem. Fix by balancing."},
      {"q": "MTBF=500hr, MTTR=5hr. Availability?", "options": ["99.0%","90.0%","50.0%","95.0%"], "answer": 0, "explain": "500/(500+5) = 500/505 = 99.0%."},
      {"q": "Predictive maintenance is:", "options": ["Fix after failure","Replace on fixed schedule","Monitor condition, maintain when degradation detected","Hire more techs"], "answer": 2, "explain": "PdM = condition-based. Intervene only when trending toward failure."},
      {"q": "Which maintenance strategy should be applied to a non-critical spare indicator lamp that has a readily available replacement and no safety consequence upon failure?", "options": ["Reliability-centered maintenance (RCM) analysis", "Scheduled preventive replacement every 90 days", "Predictive monitoring via infrared thermography", "Run-to-failure (reactive)"], "answer": 3, "explain": "Run-to-failure is appropriate when failure has no safety impact, no significant throughput consequence, and the item is cheap and easily replaced. Applying PdM or scheduled PM to such an item wastes resources."},
      {"q": "According to Nowlan and Heap's landmark reliability study, approximately what percentage of equipment failure modes exhibit the classic age-related wear-out pattern (rising failure rate with time)?", "options": ["About 11%", "About 40%", "About 68%", "About 89%"], "answer": 0, "explain": "Nowlan and Heap found only ~11% of items show classic wear-out (bathtub curve right limb). The majority fail randomly or with infant-mortality profiles, justifying condition-based over age-based strategies for most components."},
      {"q": "The P-F interval on a sorter drive bearing is determined to be 6 weeks. To ensure detection before functional failure, the PdM inspection interval should be no greater than:", "options": ["6 weeks", "4 weeks", "3 weeks", "1 week"], "answer": 2, "explain": "The sampling interval must be less than P-F/2 to guarantee at least one detection opportunity between point P and point F. P-F/2 = 6/2 = 3 weeks, so inspections every 3 weeks or less are required."},
      {"q": "An FFT vibration spectrum for a 1760 RPM conveyor gearbox output shaft shows a dominant spike at 1x RPM with a steady phase reading. The most likely fault is:", "options": ["Bearing outer-race defect (BPFO)", "Mechanical looseness with sub-harmonics", "Mass imbalance", "Angular misalignment"], "answer": 2, "explain": "Dominant 1x RPM with steady phase is the classic signature of mass imbalance. Misalignment typically shows elevated 2x and axial components; looseness shows sub-harmonics; bearing defects appear at calculated defect frequencies (typically 3x-20x RPM)."},
      {"q": "ISO 10816-3 classifies vibration velocity above which RMS value as 'Unacceptable' for Group 1 rotating machines (>15 kW, >600 RPM)?", "options": ["2.3 mm/s", "4.5 mm/s", "7.1 mm/s", "11.2 mm/s"], "answer": 3, "explain": "ISO 10816-3 Group 1 severity bands: <2.3 Good, 2.3-4.5 Satisfactory, 4.5-11.2 Unsatisfactory, >11.2 Unacceptable. The >11.2 mm/s zone requires immediate corrective action."},
      {"q": "An IR scan of an ACY1 MCC bucket reveals a delta-T of 25 degrees C between one motor starter lug and the reference phase lug under full load. Per NETA severity guidelines, this requires:", "options": ["No action; monitor at next annual survey", "Repair within 30 days", "Repair within 90 days at next planned outage", "Immediate action - remove from service or repair before next shift"], "answer": 3, "explain": "NETA thermography severity: delta-T 1-10 deg C = monitor; 11-20 = repair within 30 days; >20 deg C = immediate action. A 25 deg C delta-T on a current-carrying connection poses fire and failure risk requiring immediate correction."},
      {"q": "When performing structure-borne ultrasound-guided lubrication on a conveyor head-pulley bearing, the technician should stop adding grease when:", "options": ["The grease gun reaches 10 strokes regardless of sound", "The ultrasound noise level drops and then begins to rise again - stop at the minimum (drop point)", "The bearing housing temperature drops by 5 deg C", "Grease begins to purge from the relief fitting"], "answer": 1, "explain": "Ultrasound-guided lubrication: dBuV level drops as fresh grease coats starved contact surfaces, then rises as the cavity fills and over-pressure develops. Stopping at the minimum noise level prevents over-greasing, the leading cause of bearing failure."},
      {"q": "Per IEEE Std 43-2013, the minimum acceptable insulation resistance for a 460 V (0.46 kV) motor winding tested at 500 V DC is:", "options": ["1 M-ohm", "5 M-ohm", "100 M-ohm", "1000 M-ohm"], "answer": 0, "explain": "IEEE 43-2013 minimum IR = (kV + 1) M-ohm = (0.46 + 1) = ~1.5 M-ohm, rounded to 1 M-ohm minimum. However, for motors >1 kV, 100 M-ohm is the minimum. A 460 V motor minimum is approximately 1 M-ohm by this formula."},
      {"q": "A Motor Circuit Analysis (MCA) test on a 460 V conveyor motor shows inductance values of 12.1 mH, 12.0 mH, and 15.4 mH across the three phases. What does this indicate?", "options": ["Normal - all values are within 5% balance", "Possible turn-to-turn winding fault on the high-inductance phase; imbalance exceeds 5% limit", "Open circuit on one phase; measurement is too high", "Capacitive imbalance from a failed power-factor correction capacitor"], "answer": 1, "explain": "MCA inductance balance limit is within 5% between phases. The third phase at 15.4 mH vs ~12.0 mH average shows ~28% deviation, strongly indicating a developing inter-turn short or winding fault requiring further investigation."},
      {"q": "A conveyor belt segment logs 4 unplanned stoppages totaling 10 hours of repair time over a 6,000-hour operating year. What is the calculated Availability (A)?", "options": ["A = 99.83%", "A = 98.33%", "A = 93.33%", "A = 99.00%"], "answer": 0, "explain": "MTBF = 6000 hr / 4 failures = 1500 hr. MTTR = 10 hr / 4 repairs = 2.5 hr. A = MTBF / (MTBF + MTTR) = 1500 / (1500 + 2.5) = 1500 / 1502.5 = 99.83%."},
      {"q": "An ACY1 sorter line has Availability = 0.91, Performance = 0.94, and Quality = 0.98. What is the OEE, and does it meet world-class threshold?", "options": ["OEE = 83.8%; below world-class threshold of 85%", "OEE = 91.0%; meets world-class threshold", "OEE = 94.0%; meets world-class threshold", "OEE = 78.2%; far below world-class threshold"], "answer": 0, "explain": "OEE = 0.91 x 0.94 x 0.98 = 0.838 = 83.8%. World-class OEE benchmark is >=85%, so 83.8% is below threshold and would trigger a reliability review in ACY1's APM system."},
      {"q": "ACY1 RME's target for PM compliance (work orders completed on time vs. scheduled) is at least 90%. If compliance falls below 80%, the most direct consequence tracked in EAM/APM metrics is:", "options": ["Increased MTBF for critical assets", "Higher reactive (unplanned) maintenance rate and increased downtime", "Reduced spare-parts consumption", "Improved OEE through fewer planned interruptions"], "answer": 1, "explain": "PM compliance below 80% means scheduled maintenance tasks are being skipped or delayed. This allows preventable failures to develop, directly increasing unplanned (reactive) maintenance events, downtime, and MTTR. EAM data correlates low PM compliance with higher reactive-WO rates."}
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
      },
      {"h": "Ladder Scan & Rung Anatomy", "body": "A PLC does not run ladder like a program that jumps around - it executes a fixed <b>scan cycle</b> over and over:<br><pre>1. Read all physical INPUTS -&gt; input image table\n2. Solve rungs TOP to BOTTOM, LEFT to RIGHT\n3. Write output image table -&gt; physical OUTPUTS\n4. Housekeeping / comms, then repeat</pre>Everything a rung reads comes from the image table captured at step 1, and outputs only hit the field at step 3. A typical scan is 1-10 ms.<br><br><b>Rung anatomy:</b> a rung is a set of <b>input conditions</b> (contacts) on the left that must form a true path to the <b>output</b> (coil/instruction) on the right.<br><pre>    Start   Stop         Motor\n --| |----|/|-----+-----( )--\n   Motor          |\n --| |------------+   (parallel branch = OR)</pre><b>Series contacts = AND</b> (all must be true). <b>Parallel branches = OR</b> (any path true energizes the coil).<br><br><b>Seal-in (latching) circuit:</b> the <code>Motor</code> contact in parallel with <code>Start</code> is the classic <b>seal-in</b>. Press Start, the coil energizes, its own contact closes and keeps the rung true after you release Start. <code>Stop</code> (an XIO / normally-closed contact) breaks the seal. This is the most common motor-control pattern in the plant.<br><br><b>Scan-order gotcha:</b> if you write to a bit on rung 10 and read it on rung 5, rung 5 uses <b>last scan's</b> value - it is one scan stale. Order matters. Writing the same output coil on two rungs is the classic <b>double-coil</b> bug: only the last one solved wins.<br><br><b>Edge (one-shot) instructions</b> fire for exactly one scan on a transition:<br>&bull; <b>ONS / OSR</b> - one-shot rising (fires when the preceding logic goes false-&gt;true)<br>&bull; <b>OSF</b> - one-shot falling (fires on true-&gt;false)<br>Use a one-shot to trigger a single action per button press (increment a counter, latch a fault, send one message) instead of re-firing every scan the button is held."},
      {"h": "Ladder Timers & Counters in Depth", "body": "Timers and counters are <b>function-block-style instructions</b> with a memory structure. In Studio 5000 a TON tag has three status bits and two values:<br>&bull; <b>.EN</b> (Enable) - true while the rung feeding the timer is true<br>&bull; <b>.TT</b> (Timing) - true while actively counting up (EN true AND not done)<br>&bull; <b>.DN</b> (Done) - true when <code>.ACC &gt;= .PRE</code><br>&bull; <b>.PRE</b> (Preset, ms) - the target; <b>.ACC</b> (Accumulator, ms) - elapsed time<br><br><b>Timer types:</b><br>&bull; <b>TON</b> (On-Delay) - starts timing when rung goes true; <code>.DN</code> after PRE. Rung false resets <code>.ACC</code> to 0 immediately. Use for start delays, jam-qualify windows, warmups.<br>&bull; <b>TOF</b> (Off-Delay) - <code>.DN</code> goes true the instant the rung is true and stays true for PRE ms <b>after</b> the rung goes false. Use for run-on fans, lube pulses, keeping a light on briefly.<br>&bull; <b>RTO</b> (Retentive On) - accumulates true-time and <b>holds .ACC through power/rung loss</b>. Only a <b>RES</b> instruction clears it. Use for total runtime / maintenance-hour tracking.<br>&bull; <b>RES</b> - resets a timer or counter (.ACC=0, status bits off).<br><br><b>Counters:</b><br>&bull; <b>CTU</b> counts up on each false-&gt;true of its rung; <code>.DN</code> when <code>.ACC &gt;= .PRE</code>. Counts <b>rising edges</b>, so it inherently one-shots.<br>&bull; <b>CTD</b> counts down. <b>CTU + CTD sharing one tag</b> makes a bidirectional counter (parts in vs parts out).<br>&bull; A counter keeps counting past PRE - use <code>.DN</code> to act, then <b>RES</b> to zero it.<br><br><b>Cascading for long times:</b> to time hours from a millisecond timer, let one TON's <code>.DN</code> both reset itself (via a rung) and clock a CTU. When the timer rolls every 60 s, the counter tallies minutes - a classic way to build long, low-resolution timers."},
      {"h": "Structured Text Operators & IEC Function Blocks", "body": "ST is a high-level text language. Know the <b>operator precedence</b> (highest first) so you parenthesize correctly:<br><pre>()          parentheses\nNOT, -      unary\n**          exponent\n*  /  MOD   multiply/divide/modulo\n+  -        add/subtract\n&lt; &lt;= &gt; &gt;=   comparison\n=  &lt;&gt;        equal / not-equal\nAND / &amp;     logical and\nXOR\nOR          (lowest)</pre>Note <b>=</b> is a comparison in ST; <b>:=</b> is assignment. <b>&lt;&gt;</b> means not-equal.<br><br><b>IEC timers/counters are function blocks you instantiate</b>, not inline instructions. Declare an instance, then call it with named parameters:<br><pre>VAR\n  JamTmr : TON;   // declare instance\nEND_VAR\n\nJamTmr(IN := Photoeye_Blocked, PT := T#3s);\nIF JamTmr.Q THEN  Jam := TRUE;  END_IF;</pre>&bull; <b>TON</b>(IN, PT) -&gt; outputs <b>.Q</b> (done) and <b>.ET</b> (elapsed time). <b>TOF</b> and <b>TP</b> (pulse) work the same way.<br>&bull; <b>CTU</b>(CU, RESET, PV) -&gt; <b>.Q</b>, <b>.CV</b> (current value). CTD, CTUD similar.<br><br><b>Edge detection blocks:</b> <b>R_TRIG</b>(CLK) gives a one-scan <b>.Q</b> pulse on a rising edge; <b>F_TRIG</b> on a falling edge - the ST equivalent of ONS.<br><br><b>Bistables (latches):</b> <b>SR</b> is set-dominant (S1 wins if both active); <b>RS</b> is reset-dominant (R1 wins) - use RS for safety latches so reset always wins.<br><br><b>Time literals</b> use the <b>T#</b> prefix: <code>T#500ms</code>, <code>T#3s</code>, <code>T#1m30s</code>, <code>T#2h</code>. <b>STRING</b> functions include <code>LEN</code>, <code>LEFT</code>, <code>RIGHT</code>, <code>MID</code>, <code>CONCAT</code>, <code>FIND</code> for building labels and parsing barcodes."},
      {"h": "Structured Text Pattern Cookbook", "body": "A handful of ST patterns cover most real controls tasks. Keep these in your back pocket:<br><br><b>1. Linear scaling (raw counts -&gt; engineering units):</b><br><pre>// 4-20 mA sensor, raw 6242..31208 -&gt; 0..100 PSI\nPSI := (RawIn - 6242) * 100.0 / (31208 - 6242);</pre><b>2. Clamp / limit a value:</b><br><pre>Speed := LIMIT(0, Cmd, 100);   // MIN=0, MAX=100\n// or explicitly:\nIF Speed &gt; 100 THEN Speed := 100;\nELSIF Speed &lt; 0 THEN Speed := 0; END_IF;</pre><b>3. Hysteresis (deadband) - stops relay chatter:</b><br><pre>IF Temp &gt;= 80.0 THEN  Fan := TRUE;\nELSIF Temp &lt;= 70.0 THEN  Fan := FALSE; END_IF;\n// between 70 and 80 the output HOLDS its last state</pre><b>4. Debounce with a timer (reject glitches):</b><br><pre>DebTmr(IN := RawInput, PT := T#50ms);\nStableInput := DebTmr.Q;</pre><b>5. Safe divide (never divide by zero):</b><br><pre>IF Divisor &lt;&gt; 0 THEN  Result := Total / Divisor;\nELSE  Result := 0;  Fault := TRUE;  END_IF;</pre><b>6. Moving average (simple smoothing):</b><br><pre>Sum := Sum - Buf[Idx] + NewSample;\nBuf[Idx] := NewSample;\nIdx := (Idx + 1) MOD N;\nAvg := Sum / N;</pre><b>7. State-machine skeleton</b> (see the State Machines module for the full pattern) - a CASE on a State enum with one branch per step and explicit transitions. These seven patterns show up across scaling analog signals, protecting divides, cleaning noisy inputs, and sequencing - the daily bread of ST at ACY1."}
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
      },
      {"q": "In a ladder seal-in (latch) rung, what keeps the motor coil energized after the Start button is released?", "options": ["A retentive timer", "The Motor contact wired in parallel with Start holds the rung true", "The Stop button", "The scan cycle automatically re-energizes it"], "answer": 1, "explain": "The output's own contact placed in parallel with the momentary Start forms the seal-in; it maintains the true path until a series Stop (XIO) breaks it."},
      {"q": "Writing to the same output coil on two different rungs (a 'double-coil') causes what?", "options": ["Both rungs energize the output", "A compile error every time", "Only the LAST rung solved each scan controls the output; the earlier one is effectively ignored", "The output toggles rapidly"], "answer": 2, "explain": "Because rungs solve top-to-bottom and outputs write once per scan, the last coil solved wins - the classic double-coil bug that hides intermittent behavior."},
      {"q": "For a Studio 5000 TON timer, which pair correctly names the elapsed value and the done bit?", "options": [".ET and .Q", ".ACC (accumulator) and .DN (done)", ".CV and .PT", ".PRE and .EN"], "answer": 1, "explain": "In ladder/Studio 5000 the timer tag uses .ACC for elapsed ms and .DN for done. (In IEC Structured Text the same block instead exposes .ET and .Q.)"},
      {"q": "In Structured Text, how do you use a TON on-delay timer?", "options": ["Drop a TON box on a rung", "Declare a TON instance, then call it each scan with named params (IN, PT) and read .Q/.ET", "Write TON = TRUE in a loop", "Timers are not available in ST"], "answer": 1, "explain": "IEC timers are function blocks: declare an instance (JamTmr : TON;), call JamTmr(IN:=cond, PT:=T#3s) every scan, then read JamTmr.Q and JamTmr.ET."}
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
