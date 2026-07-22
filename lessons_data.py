# -*- coding: utf-8 -*-
# DEEP lecture expansions. Keyed DEEP[module_id][heading_substring] = extra_html
# build_academy.py appends this to any section whose heading contains the key.
# Written as real teaching prose (the "why", an analogy, a worked example) to turn
# terse reference-cards into actual lectures.

DEEP = {}

DEEP[0] = {
 "What Is AET": (
  "<p class='lec'>Think of a modern fulfillment center as a living body. The <b>conveyors, sorters, and robots</b> are the muscles; the <b>sensors</b> are the nerve endings; the <b>PLCs</b> are the spinal reflexes; and the <b>SCADA / warehouse-control system</b> is the brain. Automation Engineering Technology is the discipline that keeps that whole nervous system healthy - designing it, wiring it, programming it, and above all <b>troubleshooting it when it stops.</b></p>"
  "<p class='lec'>AET is deliberately a <i>blend</i>. A pure electrician knows wiring but not ladder logic; a pure programmer knows code but not why a motor overload trips. The AET technician lives in the overlap: enough electrical theory to take a meter reading and trust it, enough controls knowledge to read the PLC that commanded the output, and enough mechanical sense to know whether the fault is really electrical at all. That breadth is exactly why AET techs are the people a site calls at 3 a.m. when a line is down.</p>"
  "<p class='lec'><b>Why it matters to you:</b> every skill in this academy ladders up to one payoff - cutting <b>downtime</b>. A minute of stopped conveyor is lost throughput. The faster and more confidently you can trace a problem across the electrical/controls/mechanical boundary, the more valuable you are.</p>"
 ),
 "Automation Pyramid": (
  "<p class='lec'>The pyramid is not academic trivia - it is a <b>troubleshooting map.</b> When something misbehaves, you locate the symptom on a level and then decide whether to look <i>down</i> (is the field device / wiring bad?) or <i>up</i> (is the logic or the operator command wrong?). A jam that clears when you cycle power is usually Level 0-1 (a sensor or output). A part that routes to the wrong chute with every device testing good is usually Level 2-4 (logic or data).</p>"
  "<p class='lec'>Information flows <b>up</b> as measurements and status; commands flow <b>down</b> as setpoints and outputs. Each level talks to its neighbors on a slower, more abstract timescale: Level 1 scans in milliseconds, Level 4 plans in minutes or hours. Learning where a problem lives on the pyramid is half of solving it.</p>"
 ),
 "10 Core Domains": (
  "<p class='lec'>Do not be intimidated by ten domains - they are not ten separate careers, they are ten <b>views of the same machine.</b> When you diagnose a stopped VFD-driven belt, you touch electrical (the 480 V feed), motors/drives (the VFD fault code), sensors (the photo-eye that said &#39;jam&#39;), PLCs (the logic that stopped it), and networks (the message that told SCADA). This academy walks each domain in isolation so that, on the floor, you can weave them together fast.</p>"
 ),
 "Career Paths": (
  "<p class='lec'>The honest map: an <b>AAS</b> or a strong stack of certs gets you in the door as a maintenance / controls technician. Field experience plus certs (ISA CCST, SACA, an OEM robot cert) moves you to senior tech or controls specialist. A <b>BSET</b> or proven project record opens automation engineer, integrator, and reliability-engineering roles. Nobody skips the floor time - the best controls engineers are the ones who spent years with a meter in their hand.</p>"
 ),
}

DEEP[1] = {
 "DC Fundamentals": (
  "<p class='lec'><b>Ohm&#39;s Law is the single most-used equation of your career</b>, so build intuition, not just memorization. Voltage is <i>pressure</i>, current is <i>flow</i>, resistance is <i>restriction</i>. Water in a pipe: raise the pressure (V) and more flows (I); pinch the pipe (raise R) and less flows. V = I x R ties the three together, and P = V x I tells you the heat.</p>"
  "<p class='lec'><b>Worked example:</b> a 24 V sensor draws 50 mA. Its effective resistance is R = V/I = 24 / 0.05 = 480 &Omega;, and it dissipates P = V x I = 24 x 0.05 = 1.2 W. If you measure 24 V present but 0 mA flowing, the load is open (broken wire, blown internal fuse). If you measure 0 V across a load that should be on, the voltage is being dropped <i>somewhere upstream</i> - a loose terminal, a tripped protector. That upstream/downstream reasoning is the heart of electrical troubleshooting.</p>"
  "<p class='lec'>Series circuits share one current and split the voltage; parallel circuits share one voltage and split the current. A string of series contacts (E-stop, gate switch, then coil) is a safety chain - open any one and the whole rung dies, which is exactly what you want for a stop function.</p>"
 ),
 "AC Fundamentals": (
  "<p class='lec'>AC matters because the grid and every big motor run on it. The catch: an AC value is always <i>moving</i>, so we quote <b>RMS</b> - the equivalent DC that would do the same heating work. A &#39;120 V&#39; outlet actually peaks near 170 V; a &#39;480 V&#39; feed peaks near 679 V. Your meter shows RMS, but insulation must survive the peak - which is why voltage ratings look generous.</p>"
  "<p class='lec'><b>Three-phase</b> is the workhorse of industry because three staggered sine waves deliver smooth, constant power to a motor and let it start itself with no extra parts. The line-to-line voltage is &radic;3 (about 1.73) times the line-to-neutral: that is why a 277 V lighting circuit and a 480 V motor circuit live in the same panel. <b>Power factor</b> (cos of the phase angle) measures how much of your current actually does work versus just sloshing back and forth magnetizing motor iron - low PF means you pay for current you never turn into torque.</p>"
 ),
 "Motor Control Circuits": (
  "<p class='lec'>The classic <b>start/stop with seal-in</b> is the &#39;hello world&#39; of motor control, and you will see it thousands of times. Split it in two: the <b>power circuit</b> (fat wires, full line voltage, disconnect - fuses - contactor - overload - motor) and the <b>control circuit</b> (thin wires, usually 120 V, the logic that decides <i>when</i> the contactor closes).</p>"
  "<p class='lec'><b>How the seal-in works:</b> press <b>Start</b> (NO) and current reaches the M coil; the contactor pulls in, and its auxiliary NO contact - wired in parallel with the Start button - closes and keeps the coil energized after you release Start. Press <b>Stop</b> (NC) and you break that hold, the coil drops, everything opens. The overload (OL) contact sits in the same rung so a thermal trip also drops the motor. Learn to read this rung in your sleep - almost every complex control scheme is this idea repeated and interlocked.</p>"
 ),
 "Reading Schematics": (
  "<p class='lec'>A ladder diagram is read like a book: <b>top rung to bottom, left rail to right.</b> The left rail is your source (hot), the right rail is the return (neutral/common); every rung is one complete path. Inputs (contacts) live on the left, the output (a coil, light, or solenoid) lives at the right end. If power can travel an unbroken path of closed contacts from left rail to the output, that output turns on - that is the entire logic of the drawing.</p>"
  "<p class='lec'>Memorize the shorthand because it is universal: <b>M</b> starter, <b>OL</b> overload, <b>CR</b> control relay, <b>PB</b> pushbutton, <b>LS</b> limit switch, <b>SOL</b> solenoid, <b>PL</b> pilot light. Cross-reference numbers in the margin point you to where a relay&#39;s <i>other</i> contacts appear on other rungs - following those references is how you trace an interlock across a big print.</p>"
 ),
}

DEEP[2] = {
 "What Is a PLC": (
  "<p class='lec'>Before PLCs, control logic was a wall of hard-wired relays - to change a machine&#39;s behavior you rewired it, which was slow, error-prone, and impossible to document well. The <b>PLC</b> replaced that wall with software: the same rungs now live in memory, and a change is a download, not a rewiring. That is the whole reason the device exists.</p>"
  "<p class='lec'>Physically a PLC is a rugged industrial computer: a <b>CPU</b> that runs your program, a <b>power supply</b>, <b>I/O modules</b> that convert real-world 24 V / 120 V / 4-20 mA signals into bits and back, and <b>comm ports</b> to talk to HMIs, drives, and other PLCs. It is built to survive heat, vibration, and electrical noise for decades - which is why you will maintain 20-year-old PLCs that still run flawlessly.</p>"
 ),
 "Scan Cycle": (
  "<p class='lec'>The scan cycle is the single most important PLC concept, because it explains behavior that confuses beginners. The PLC does <b>not</b> react to the world continuously - it takes a fast snapshot. Every scan it (1) copies all physical inputs into an <b>input image table</b>, (2) executes your whole program top-to-bottom using <i>that frozen snapshot</i>, then (3) writes the results to the <b>output image</b> and out to the physical outputs. Then it repeats, typically every few milliseconds.</p>"
  "<p class='lec'><b>Why you must know this:</b> because the program uses the snapshot, if the same bit is written on two rungs, the <i>last</i> rung wins for that scan (&#39;last-state-wins&#39;). An input that pulses faster than one scan can be missed entirely. And an output physically changes only at the end of the scan, not the instant its rung goes true. Scan time also sets your real-time limit - a heavy program that scans slowly can miss fast events.</p>"
 ),
 "Addressing": (
  "<p class='lec'>Addressing is just the PLC&#39;s filing system for &#39;where does this signal live in memory.&#39; Modern Allen-Bradley Logix uses friendly <b>tag names</b> (Conveyor_Run, Photoeye_1) - self-documenting and the current best practice. Older and Siemens systems use <b>physical addresses</b>: Siemens I0.0 = input byte 0 bit 0, Q0.0 = output, M = memory bit, DB = data block. Legacy AB SLC used I:1/0 style.</p>"
  "<p class='lec'><b>On the floor this matters for wiring:</b> a <b>sinking (NPN)</b> sensor switches the negative side and sources current from the input card; a <b>sourcing (PNP)</b> sensor switches positive. Mismatch the sensor type to the input card&#39;s expectation and the input never reads - a very common &#39;the sensor is good but the PLC won&#39;t see it&#39; call. Most industrial DC I/O is 24 VDC.</p>"
 ),
 "Basic Ladder Instructions": (
  "<p class='lec'>Ladder&#39;s power is that it looks like the relay schematics electricians already knew. But the names trip people up, so anchor them: <b>XIC (Examine If Closed)</b> is true when its bit is 1 - draw it as a normally-open contact. <b>XIO (Examine If Open)</b> is true when its bit is 0 - a normally-closed contact. <b>OTE</b> energizes an output while the rung is true.</p>"
  "<p class='lec'>The trap for newcomers: <b>XIC / XIO describe how the instruction reads the bit, not the wiring of the field device.</b> A physical normally-closed stop button that is wired to be TRUE when un-pressed is examined with an XIC in the program. Get comfortable separating &#39;what the field device does&#39; from &#39;how the instruction tests the bit.&#39; <b>OTL/OTU</b> latch and unlatch - they hold their state even when the rung goes false, so they need a matching unlatch somewhere or they stay stuck.</p>"
 ),
 "IEC 61131-3": (
  "<p class='lec'>IEC 61131-3 is the standard that keeps you from having to relearn everything for each brand. It defines five languages so you can pick the right tool: <b>Ladder (LD)</b> for relay-style discrete logic and easy troubleshooting; <b>Function Block (FBD)</b> for signal-flow and process/PID; <b>Structured Text (ST)</b>, a Pascal-like text language, for math, loops, and complex decisions; <b>Sequential Function Chart (SFC)</b> for step-by-step processes; and Instruction List (now deprecated).</p>"
  "<p class='lec'>Real programs mix them: a batching machine might use SFC for the overall sequence, ladder for the interlocks, and ST for the recipe math. Ladder still dominates maintenance work because it is the easiest to watch live and see exactly which contact is blocking a rung.</p>"
 ),
}


DEEP[3] = {
 "Timers": (
  "<p class='lec'>Timers turn &#39;how long&#39; into logic, and almost every real machine needs them - a motor that must run 3 seconds after the light comes on, a valve that must stay open exactly 500 ms. The <b>TON (Timer On-Delay)</b> is the one you will use most: while its rung is true it accumulates time (ACC) toward your preset (PRE); when ACC reaches PRE the <b>Done (DN)</b> bit turns on. Drop the rung and it resets to zero.</p>"
  "<p class='lec'><b>TOF (off-delay)</b> is the mirror - it keeps its output on for a set time <i>after</i> the rung goes false (think of a fan that runs a while after you shut the machine). <b>RTO (retentive)</b> remembers its accumulated time across power cycles until you explicitly reset it - useful for tracking total runtime. Watch the timebase and units; a preset of 3000 on a 1 ms timer is 3 seconds, not 3000.</p>"
 ),
 "Counters": (
  "<p class='lec'>Counters answer &#39;how many.&#39; A <b>CTU (count up)</b> increments its accumulator on each <b>false-to-true transition</b> of its rung - that edge-detection is key: it counts events, not the whole time the input is held. When ACC reaches preset, the done bit fires (say, 24 items counted, divert the tote). A <b>CTD</b> counts down; pair them to track parts in a buffer.</p>"
  "<p class='lec'>The classic bug: forgetting to <b>reset</b> the counter, so it counts forever and never re-triggers cleanly, or wiring the count input to a signal that stays on so it only ever counts once. Counters and timers together build almost every sequencing job on the floor.</p>"
 ),
 "Comparison": (
  "<p class='lec'>Comparison and math instructions let the PLC make decisions from analog values and arithmetic. <b>EQU, NEQ, GRT, LES, GEQ, LEQ</b> compare two values and drive a rung true/false - &#39;if tank level GRT 80%, close the fill valve.&#39; Math blocks (<b>ADD, SUB, MUL, DIV, MOV, CPT</b>) do the arithmetic, often to scale a raw analog count into engineering units.</p>"
  "<p class='lec'>Two cautions from the field: watch <b>integer vs floating-point</b> - 5/2 in integer math is 2, not 2.5, which silently corrupts a calculation. And guard against <b>divide-by-zero</b>, which can fault the processor and stop the machine. Small math mistakes cause big, confusing behavior downstream.</p>"
 ),
 "Program Organization": (
  "<p class='lec'>A one-file spaghetti program is unmaintainable. Modern controllers organize code into <b>routines / program blocks</b> called from a main routine, often grouped by machine area or function (Conveyor_1, Palletizer, Faults). Structure makes a program readable to the next tech - and that next tech is often you at 3 a.m.</p>"
  "<p class='lec'>Good practice: a dedicated fault-handling routine, consistent tag naming, and comments on every non-obvious rung. The goal is that someone who has never seen the machine can open the program, find the area, and follow the logic. Disorganized code is a hidden downtime cost.</p>"
 ),
}

DEEP[4] = {
 "Discrete Sensors": (
  "<p class='lec'>Discrete sensors answer a yes/no question - is something there? They are the eyes and touch of the machine. <b>Inductive proximity</b> detects only metal at short range (great for gears, cams, metal targets); <b>capacitive</b> detects almost anything including liquids and plastics; <b>photoelectric</b> uses a light beam (through-beam, retro-reflective, or diffuse) for longer range; <b>ultrasonic</b> uses sound for clear/shiny targets that fool light.</p>"
  "<p class='lec'>Wiring them is where techs get stuck: match <b>PNP (sourcing)</b> or <b>NPN (sinking)</b> to your PLC input, and choose <b>NO vs NC</b> for fail-safe behavior. On a safety-related sense you often want NC so a broken wire reads the same as &#39;blocked&#39; and fails safe. Range, target material, and ambient light/dust all decide which technology survives on that spot on the line.</p>"
 ),
 "Analog Instruments": (
  "<p class='lec'>When you need a <i>value</i>, not a yes/no - temperature, pressure, level, flow - you use an analog instrument. The dominant signal is the <b>4-20 mA current loop</b>, and there is a beautiful reason it beats 0-10 V: because it is a <i>current</i> loop, wire resistance and voltage drop do not change the reading, so it runs long distances through a noisy plant without error.</p>"
  "<p class='lec'>The other gift of 4-20 mA is <b>live zero</b>: a healthy &#39;empty&#39; reads 4 mA, so <b>0 mA means a broken wire or dead transmitter</b> - the fault is unmistakable, unlike 0-10 V where zero could mean &#39;empty&#39; or &#39;dead.&#39; RTDs and thermocouples measure temperature (PT100 RTDs are accurate and stable; thermocouples read very high temps). Knowing the signal type tells you how to meter it.</p>"
 ),
 "Encoders": (
  "<p class='lec'>Encoders turn rotation or travel into countable pulses, giving the PLC precise <b>position, speed, and direction.</b> An <b>incremental</b> encoder outputs A and B pulse trains 90&deg; out of phase (quadrature) - the phase order tells direction, the pulse rate tells speed, and a Z channel marks one-per-rev for homing. Count the edges and you know how far a conveyor moved.</p>"
  "<p class='lec'>An <b>absolute</b> encoder reports its exact angle even after a power loss - no re-homing needed - which matters on axes that must not lose their place. Encoders drive everything from conveyor tracking (so the PLC knows which package is over which diverter) to servo positioning. Resolution (pulses per revolution) sets how fine you can measure.</p>"
 ),
 "Scaling": (
  "<p class='lec'>The PLC does not see &#39;72.5 psi&#39; - it sees a raw integer from the analog card (say 0-32767 for 4-20 mA). <b>Scaling</b> is the linear map from raw counts to engineering units, and getting it right is a core skill. The formula is a straight line: EU = (raw - raw_min) / (raw_max - raw_min) x (EU_max - EU_min) + EU_min.</p>"
  "<p class='lec'><b>Worked example:</b> a 0-100 psi transmitter on a 4-20 mA card scaled 0-32767. A raw of 16384 (mid-scale) maps to 50 psi. <b>Calibration</b> then trims out real-world error: apply a known input, compare the reading, and adjust zero and span until they agree. A miscalibrated loop reads plausible-but-wrong numbers - the most dangerous kind of fault because nobody questions it.</p>"
 ),
}

DEEP[5] = {
 "AC Induction Motors": (
  "<p class='lec'>The three-phase induction motor is the most common machine in any plant because it is brutally simple and reliable: no brushes, no commutator, just a wound stator and a rotor. The three-phase supply creates a <b>rotating magnetic field</b> in the stator; that field induces current in the rotor bars, and the induced current makes the rotor chase the field. The rotor always runs slightly slower than the field - that gap is <b>slip</b>, and without it no torque is produced.</p>"
  "<p class='lec'>Synchronous speed = 120 x frequency / poles. A 4-pole motor on 60 Hz syncs at 1800 RPM and runs loaded near 1750 - that 50 RPM is the slip. The <b>nameplate</b> is your bible: voltage, full-load amps (FLA), horsepower, service factor, and insulation class all drive your protection settings and troubleshooting baselines.</p>"
 ),
 "VFD Principles": (
  "<p class='lec'>A Variable Frequency Drive controls motor speed by changing the <b>frequency</b> delivered to the motor - since speed follows frequency, lower Hz means slower RPM. Inside, the VFD does three steps: <b>rectify</b> the incoming AC to a DC bus, smooth it on the bus capacitors, then <b>invert</b> it back to AC at whatever frequency and voltage it wants using fast-switching IGBTs and PWM.</p>"
  "<p class='lec'>The critical rule is <b>constant Volts-per-Hertz</b>: to keep magnetic flux (and torque) steady, the drive lowers voltage in proportion to frequency. A 480 V / 60 Hz motor wants about 8 V per Hz, so at 30 Hz it gets ~240 V. Beyond why speed control saves huge energy on fans and pumps, VFDs give soft starts (no across-the-line inrush) and precise ramping - which is why they are everywhere on modern conveyors.</p>"
 ),
 "Key Parameters": (
  "<p class='lec'>A VFD is a small computer, and its behavior lives in <b>parameters</b> you must be able to read and set. The essentials: motor nameplate data (FLA, HP, base frequency, base voltage) so the drive protects the motor; <b>accel/decel ramp times</b>; <b>min/max frequency</b> limits; the <b>control source</b> (keypad, terminal, network); and the current limit / overload settings.</p>"
  "<p class='lec'>Set the nameplate parameters wrong and everything downstream misbehaves - nuisance trips, weak torque, or no protection at all. Always record the original parameters before you change anything, and know how to restore defaults. Many drives support an autotune that measures the motor and fills these in.</p>"
 ),
 "Common Faults": (
  "<p class='lec'>VFDs announce their problems with <b>fault codes</b>, and learning the top few saves hours. <b>Overcurrent (OC)</b>: mechanical jam, too-fast accel, or a shorted output. <b>Overvoltage (OV)</b>: usually the DC bus pumped up by a fast decel on a high-inertia load - fix it by extending decel time or adding a brake resistor. <b>Undervoltage</b>: sagging supply or lost phase. <b>Overtemp</b>: blocked cooling, failed fan, or clogged heatsink.</p>"
  "<p class='lec'><b>Ground fault</b> points to insulation breakdown in the motor or cable. The pattern to internalize: a fault that trips on <i>accel</i> is usually load/mechanical or ramp-time; a fault on <i>decel</i> is usually bus overvoltage; a fault at <i>steady state</i> is usually thermal or supply. Read the code, note when it trips, and you have already narrowed the cause.</p>"
 ),
}

DEEP[6] = {
 "Pneumatics": (
  "<p class='lec'>Pneumatics uses compressed air to do work - fast, clean, cheap, and forgiving, which is why grippers, diverters, blow-offs, and clamps across a facility are air-driven. A directional-control <b>valve</b> (often a solenoid-operated 5/2 or 5/3) routes air to a <b>cylinder</b> to extend or retract it. Air is compressible, so pneumatic motion is springy and not precisely positionable - great for point-to-point, poor for holding an exact spot.</p>"
  "<p class='lec'>The unsung hero is <b>air preparation</b>: the FRL (Filter-Regulator-Lubricator). The filter removes water and dirt, the regulator sets pressure, and where needed the lubricator adds a fine oil mist. Most pneumatic &#39;equipment&#39; faults are really air-quality or pressure faults - a sticky cylinder is often just a clogged filter or a drifting regulator.</p>"
 ),
 "Hydraulics": (
  "<p class='lec'>Hydraulics trades air for oil, and because liquid is nearly <b>incompressible</b> it delivers enormous, precisely-controllable force - think balers, presses, and heavy lifts. Pascal&#39;s principle is the whole game: pressure applied to a confined fluid acts equally everywhere, so a small pump pressure across a large cylinder area becomes a huge force (Force = Pressure x Area).</p>"
  "<p class='lec'>A system needs a <b>pump</b> (makes flow), a <b>relief valve</b> (caps pressure so nothing bursts), directional and flow-control valves, an actuator, and a reservoir. Cleanliness is everything - most hydraulic failures trace to contaminated or degraded oil chewing up close-tolerance valves and pumps. And respect the pressures: hydraulic injection injuries are a serious safety hazard.</p>"
 ),
 "Symbols": (
  "<p class='lec'>Fluid-power schematics are their own language, and once you can read the symbols a circuit tells you its whole story. A valve is a box of <b>envelopes</b> - each envelope is one position (state), showing the flow paths as arrows; the number of ports and positions names it (a 5/2 has five ports, two positions). Actuators, springs, and solenoids on the ends show how the valve is shifted.</p>"
  "<p class='lec'>Lines, cylinders, pumps, filters, and accumulators each have a standard glyph. The skill is tracing the active flow path in a given valve position - which port connects to which - because that tells you where the air or oil <i>should</i> be going, so you can meter/measure and find where it actually stops.</p>"
 ),
 "Troubleshooting": (
  "<p class='lec'>Fluid-power troubleshooting rewards a systematic pressure-and-flow mindset. Start upstream: is supply pressure present and correct at the gauge? Then follow the circuit toward the actuator, checking that each valve shifts (listen and feel for the solenoid, verify its coil is energized) and that pressure appears where the active path says it should.</p>"
  "<p class='lec'>Common culprits: a de-energized or failed <b>solenoid coil</b> (meter it - a controls problem masquerading as mechanical), a stuck or contaminated valve spool, an <b>air/oil leak</b> bleeding off pressure, a misadjusted regulator or relief valve, and worn cylinder seals. The recurring lesson from Module 1 applies here too: many &#39;mechanical&#39; faults are really the electrical signal that never reached the solenoid.</p>"
 ),
}


DEEP[7] = {
 "HMI vs SCADA": (
  "<p class='lec'>An <b>HMI (Human-Machine Interface)</b> is the local touchscreen on or near one machine - it shows that machine&#39;s state and lets the operator run it. <b>SCADA (Supervisory Control And Data Acquisition)</b> is the plant-wide layer above it: it collects data from many PLCs/HMIs, gives a control-room the big picture, logs history, and manages alarms across the whole site.</p>"
  "<p class='lec'>Think of it as scale. The HMI answers &#39;how is this sorter doing right now?&#39; SCADA answers &#39;how is the whole building flowing, and what trended wrong over the last shift?&#39; SCADA does not usually do the fast real-time control - the PLCs still do that - it <i>supervises</i>, records, and presents. Knowing which layer owns a piece of behavior tells you where to look when a display is wrong versus when the machine itself is wrong.</p>"
 ),
 "Screen Design": (
  "<p class='lec'>Good HMI design is a safety and productivity issue, not decoration. The modern standard <b>ISA-101</b> pushes <b>high-performance graphics</b>: a calm gray background, muted colors for normal state, and <b>bright color reserved for abnormal conditions</b> so a problem jumps out. A screen drowning in rainbow gauges hides the one thing that matters.</p>"
  "<p class='lec'>Design for the operator under stress: consistent layout and navigation, clear hierarchy (overview to detail), analog trends and deviation indicators instead of raw numbers, and no decorative 3-D or animation that adds cognitive load. The test of a screen is simple - can a tired operator spot the abnormal state in one glance? That is the whole goal.</p>"
 ),
 "Tags": (
  "<p class='lec'>A <b>tag</b> is the named link between an HMI/SCADA object and a real value in a PLC - press a button on the screen and it writes a tag; a value changes in the PLC and the bound tag updates the display. Tags are how the picture stays live. They can be direct (bound to a PLC address) or internal (calculated/local to the HMI).</p>"
  "<p class='lec'>Two things bite technicians: the <b>update / poll rate</b> (a slow rate makes the screen lag reality, a too-fast rate loads the network), and <b>data-type / address mismatches</b> that make a tag read garbage or fail to connect. When a screen value is frozen or wrong but the machine is fine, suspect the tag binding, the comm path, or the update rate before you suspect the PLC.</p>"
 ),
 "Alarms": (
  "<p class='lec'>Alarms exist to tell an operator to <b>act now</b> - and the number-one failure mode is the <b>alarm flood</b>, where a trip sets off hundreds of alarms and the operator cannot find the real cause. The standard <b>ISA-18.2</b> defines the alarm lifecycle and rationalization to fix exactly this: every alarm must be actionable, prioritized, and have a defined response.</p>"
  "<p class='lec'>Practical principles: prioritize by consequence and urgency (not everything is &#39;critical&#39;), suppress the downstream alarms that a root trip inevitably causes, use deadbands and delays to stop chattering, and require acknowledgment. A well-designed alarm system is measured by how quiet it is when things are normal and how clearly it points at the true cause when they are not.</p>"
 ),
}

DEEP[8] = {
 "Network Levels": (
  "<p class='lec'>Plant networks are layered to match the automation pyramid. At the bottom, fast, deterministic <b>fieldbus / device-level</b> networks (EtherNet/IP, PROFINET, DeviceNet, IO-Link) connect PLCs to sensors, drives, and I/O - here timing is everything, a message must arrive within a guaranteed window. Above that sits the <b>control/supervisory</b> level (PLC-to-SCADA), and above that the <b>enterprise IT</b> level.</p>"
  "<p class='lec'>The key distinction is <b>OT vs IT</b>: operational-technology networks value determinism and uptime over raw speed and are kept segmented from the business network for both performance and security. A firewall / DMZ between OT and IT is standard. Understanding the levels tells you which network a problem lives on and who owns it.</p>"
 ),
 "Ethernet": (
  "<p class='lec'>Industrial Ethernet reuses standard Ethernet hardware but adds protocols that make it deterministic enough for control. <b>EtherNet/IP</b> (Allen-Bradley) runs the CIP protocol over TCP/UDP; <b>PROFINET</b> is the Siemens equivalent. They deliver cyclic I/O data on a tight schedule while still allowing normal TCP traffic for programming and HMI.</p>"
  "<p class='lec'>The bread-and-butter troubleshooting facts: every device needs a valid, unique <b>IP address and subnet</b>; a duplicate IP silently breaks two devices; link lights and managed-switch diagnostics are your fastest clues; and cable/connector faults (especially in high-vibration areas) cause intermittent dropouts that look like &#39;software&#39; problems. Ping and the switch port stats are your first tools.</p>"
 ),
 "OPC": (
  "<p class='lec'>Different brands of PLC, SCADA, and software historically could not talk to each other. <b>OPC</b> is the universal translator that fixed that - a standard so any compliant client can read/write any compliant server&#39;s data regardless of vendor. Classic OPC (DA) relied on Windows COM; the modern <b>OPC-UA</b> is platform-independent, secure (built-in authentication and encryption), and models data with rich structure.</p>"
  "<p class='lec'>OPC-UA is central to IIoT because it bridges the OT world to databases, dashboards, and cloud analytics without custom drivers for every device. When you see data flowing from a mix of PLC brands into one dashboard, an OPC-UA server is usually the glue in the middle.</p>"
 ),
 "Troubleshooting": (
  "<p class='lec'>Network troubleshooting is layered - work from the physical up. First the <b>physical layer</b>: link lights, cable, connectors, correct port. Then <b>addressing</b>: correct and unique IP, right subnet mask and gateway; use ping to prove reachability. Then <b>the protocol/config</b>: right EtherNet/IP or PROFINET setup, matching data sizes, no duplicate node.</p>"
  "<p class='lec'>Managed switches are gold - their port statistics show error counts, collisions, and which link is flapping. Intermittent faults in a plant are usually physical (vibration-loosened connectors, cable damage, EMI from nearby VFDs) rather than logical. Isolate methodically: prove the physical path, prove addressing, then look at configuration - do not jump to blaming the program.</p>"
 ),
}

DEEP[9] = {
 "Robot Types": (
  "<p class='lec'>Industrial robots come in families suited to different jobs. A <b>6-axis articulated</b> arm is the flexible generalist - six joints give it human-arm reach and orientation for welding, material handling, and complex paths. <b>SCARA</b> robots are fast and rigid in the horizontal plane, ideal for pick-and-place and assembly. <b>Delta</b> robots use parallel linkages for blistering-fast lightweight picking. <b>Cartesian / gantry</b> robots move in straight X-Y-Z lines for large, simple travel.</p>"
  "<p class='lec'>A separate and important class is the <b>AMR / AGV</b> - the mobile robots that move totes and pods across a fulfillment center. And <b>collaborative robots (cobots)</b> are built with force-limiting to work safely near people. Matching robot type to task (speed, payload, reach, precision) is the first design decision - and it shapes how you maintain and troubleshoot each.</p>"
 ),
 "Frames": (
  "<p class='lec'>A robot lives in <b>coordinate frames</b>, and understanding them is essential to programming and recovery. The <b>base frame</b> is fixed to the robot&#39;s foot; the <b>tool frame (TCP - tool center point)</b> is at the working tip of whatever the robot holds; a <b>user/work frame</b> aligns to a fixture or conveyor. Teach the tool and work frames accurately and your programmed points stay correct even if you swap grippers or shift a fixture.</p>"
  "<p class='lec'>Motion types matter too: <b>joint moves</b> get from A to B fastest (each axis moves independently, the tool path is unpredictable), while <b>linear moves</b> drive the TCP in a straight line for process work. Speed, acceleration, and <b>singularities</b> (poses where the math breaks down and an axis tries to spin infinitely fast) are the practical constraints you plan around.</p>"
 ),
 "Programming": (
  "<p class='lec'>Most robots are programmed by <b>teaching</b> - you jog the arm to real positions with a teach pendant and record those points, then string them into a motion program with logic, I/O handshakes, and speeds. This is intuitive and precise for the actual cell. <b>Offline programming</b> in simulation software builds the path on a computer model and downloads it, saving downtime for complex jobs.</p>"
  "<p class='lec'>The program is more than motion - it coordinates with the world through <b>I/O handshaking</b> (wait for &#39;part present,&#39; signal &#39;pick done&#39;), gripper control, and error recovery. Each major brand (FANUC, ABB, KUKA, Yaskawa) has its own language and pendant, but the concepts - frames, points, moves, I/O - transfer directly.</p>"
 ),
 "Safety": (
  "<p class='lec'>Robots are powerful and fast, so <b>safety is not optional</b> - a moving industrial arm can kill. Traditional cells are guarded: fences, interlocked gates that stop the robot if opened, light curtains and area scanners that detect intrusion, and E-stops within reach. The safeguarding must bring the robot to a safe stop before a person can reach the hazard.</p>"
  "<p class='lec'>Standards <b>ISO 10218</b> and <b>ISO/TS 15066</b> (for collaborative operation) define the requirements. Cobots achieve safety through <b>power-and-force limiting</b> - they sense contact and stop - but even a cobot needs a risk assessment because a sharp tool or heavy part changes the hazard. Never defeat an interlock, and always follow LOTO before entering a robot envelope for maintenance.</p>"
 ),
}

DEEP[10] = {
 "Feedback Control": (
  "<p class='lec'>Feedback control is how a machine holds a value steady against disturbances. The loop is a cycle: measure the <b>process variable (PV)</b>, compare it to the <b>setpoint (SP)</b> to get the <b>error</b>, and command an output (<b>CV</b>) that drives the error toward zero. A home thermostat is the everyday version - measure temperature, compare to the dial, turn the furnace on or off.</p>"
  "<p class='lec'>The contrast is <b>open-loop</b> control, which commands an output with no measurement of the result (a toaster runs a fixed time regardless of how done the bread is). Closed-loop is self-correcting; open-loop is blind. Nearly every process value that must stay on target - temperature, pressure, flow, level, speed - uses closed-loop feedback, and the workhorse algorithm is PID.</p>"
 ),
 "PID Terms": (
  "<p class='lec'>PID blends three responses to error. <b>Proportional (P)</b> reacts to the <i>present</i> error - bigger error, bigger push; alone it is fast but leaves a steady offset. <b>Integral (I)</b> reacts to the <i>accumulated past</i> error - it keeps nudging until the offset is gone, eliminating steady-state error but risking overshoot. <b>Derivative (D)</b> reacts to the <i>rate of change</i> - it anticipates and damps, smoothing overshoot but amplifying noise.</p>"
  "<p class='lec'>The intuition: P is the muscle, I is the patience, D is the caution. Most real loops run P and I (PI) because D is touchy with noisy signals. Tune too much P and it oscillates; too much I and it overshoots and hunts; too much D and it gets jittery. Understanding what each term <i>physically</i> does is what lets you fix a loop that is oscillating or sluggish.</p>"
 ),
 "Tuning": (
  "<p class='lec'>Tuning sets the P, I, and D gains so the loop is fast but stable. A practical manual method: start with I and D off, raise P until the loop just begins to oscillate, then back it off; add just enough I to remove the remaining offset without inducing hunting; add D only if you need to tame overshoot on a clean signal. Classic recipes like Ziegler-Nichols give starting numbers.</p>"
  "<p class='lec'>Read the response like a diagnosis: slow to reach setpoint = too little P or I (sluggish); overshoots and oscillates = too much gain or integral; jittery output = too much derivative or a noisy PV. Many modern controllers offer <b>auto-tune</b> that bumps the process and calculates gains - a great starting point you then refine by watching real behavior.</p>"
 ),
 "P&ID": (
  "<p class='lec'>A <b>P&amp;ID (Piping and Instrumentation Diagram)</b> is the master schematic of a process - it shows every vessel, pipe, valve, and instrument and how they connect. Instruments are shown as <b>balloons</b> whose <b>ISA-5.1</b> tag encodes their job: the first letter is the measured variable (<b>F</b>low, <b>L</b>evel, <b>P</b>ressure, <b>T</b>emperature) and following letters are the function (<b>I</b>ndicate, <b>C</b>ontrol, <b>T</b>ransmit).</p>"
  "<p class='lec'>So a balloon marked <b>FIC</b> is a Flow Indicating Controller; <b>LT</b> is a Level Transmitter; <b>PSH</b> is a Pressure Switch High. The line type in the balloon and connecting lines tells you if it is field-mounted or on a panel, and whether the signal is electric, pneumatic, or software. Reading a P&amp;ID is how you understand a process you have never seen - it is the map for the whole control scheme.</p>"
 ),
}

DEEP[11] = {
 "Risk Assessment": (
  "<p class='lec'>Machine safety starts with a <b>risk assessment</b> - you cannot safeguard a hazard you have not identified. The method: identify each hazard (crush, shear, electrical, thermal, entanglement), estimate the risk from its <b>severity</b>, <b>frequency of exposure</b>, and <b>possibility of avoidance</b>, then reduce it until acceptable. This is a documented, repeatable process, not a gut feeling.</p>"
  "<p class='lec'>Risk reduction follows a strict <b>hierarchy of controls</b>: first try to <b>eliminate or design out</b> the hazard, then use <b>engineering controls / guarding</b>, then <b>administrative controls</b> (procedures, training), and only last <b>PPE</b>. Higher-level controls are more reliable because they do not depend on a person remembering to do something. Every safeguard you add should trace back to a hazard the assessment found.</p>"
 ),
 "Safeguarding": (
  "<p class='lec'>Safeguarding is the physical layer that keeps people out of harm. <b>Fixed guards</b> (bolted barriers) are simplest and most reliable when access is not needed. <b>Interlocked movable guards</b> - a gate whose switch stops the machine when opened - allow access while forcing a stop. <b>Presence-sensing devices</b> (light curtains, area scanners, safety mats) stop the machine when a person enters a zone without a physical barrier.</p>"
  "<p class='lec'>Choose based on how often people need access and how fast the hazard stops. A guard must not be easy to defeat, and any interlock must be rated for safety (see ISO 13849). The recurring rule: the safeguard has to act before a person can reach the moving part - which means you also account for stopping time and approach speed when you place a light curtain.</p>"
 ),
 "ISO 13849": (
  "<p class='lec'><b>ISO 13849-1</b> is the standard for the reliability of safety-related control systems - it answers &#39;how trustworthy must this safety function be, and does my design meet it?&#39; The target is a <b>Performance Level (PL, a through e)</b>, set by the risk assessment: higher risk demands a higher PL. Your actual circuit achieves a PL based on its architecture (<b>Category B, 1-4</b>), component reliability (MTTFd), and diagnostic coverage.</p>"
  "<p class='lec'>The practical takeaway: a high-risk hazard cannot be protected by a single ordinary switch - it needs redundancy and self-checking (dual channels, monitored, so a single failure does not disable the safety function). This is why safety relays and safety PLCs exist and why you never wire a safety function through a standard relay. Match the achieved PL to the required PL, or the safeguard is not compliant.</p>"
 ),
 "LOTO": (
  "<p class='lec'><b>Lockout/Tagout (LOTO)</b> is the procedure that protects <i>you</i> during maintenance - it guarantees no energy can start the machine while your hands are inside. The steps: notify, shut down, isolate every energy source (electrical, pneumatic, hydraulic, gravity, stored/spring), <b>lock and tag</b> each isolation with your own lock, dissipate stored energy, and <b>verify zero energy</b> by trying to start it. One worker, one lock, one key - never trust someone else&#39;s lock for your life.</p>"
  "<p class='lec'><b>Arc flash</b> is the other electrical killer: a fault can release an explosive blast of heat and pressure. Respect the boundaries, wear the rated PPE (arc-rated clothing, face shield, gloves) for the incident-energy category, and treat every energized panel as dangerous until proven dead. The safest energized work is the work you de-energized first.</p>"
 ),
}

DEEP[12] = {
 "Integration Mindset": (
  "<p class='lec'>The capstone lesson is that real machines are <b>systems</b>, and faults love to hide in the seams between domains. A package mis-routes: is it the photo-eye (sensor), the diverter solenoid (pneumatic/electrical), the tracking logic (PLC), the encoder count (feedback), or a dropped network message (comm)? The integration mindset is refusing to assume - you follow the signal chain across every domain until the evidence points at one link.</p>"
  "<p class='lec'>This is why the AET curriculum spans so many topics: on the floor they are never separate. The best troubleshooters mentally trace &#39;where does this signal come from, what commands it, and where does it go&#39; across electrical, controls, mechanical, and network boundaries in one continuous thought. That fluency across the seams is the difference between a parts-swapper and a technician.</p>"
 ),
 "Commissioning": (
  "<p class='lec'>Commissioning is the disciplined process of proving a system works before it goes into production - and doing it in the right order saves enormous grief. Work bottom-up: <b>verify wiring and power</b> first, then <b>check each I/O point</b> (force an output, confirm the device moves; actuate an input, confirm the PLC sees it), then test individual functions, then integrated sequences, and finally full-rate production.</p>"
  "<p class='lec'>The golden rule: <b>never energize or run a sequence until the layer beneath it is proven.</b> A rushed commissioning that skips point-to-point I/O checks pays for it later with baffling intermittent faults. Document as you go - the commissioning records become the baseline you troubleshoot against for the life of the machine.</p>"
 ),
 "Career Paths": (
  "<p class='lec'>By now you have seen the whole landscape, so make it personal. The reliable growth path is <b>depth plus proof</b>: get genuinely good at troubleshooting one area (say drives or PLCs), earn a recognized cert that proves it, and take on the harder calls until people route the tough ones to you. Breadth across domains is what turns a technician into a controls specialist or engineer.</p>"
  "<p class='lec'>Value yourself by the downtime you prevent and the problems only you can solve, not by hours logged. Keep a record of the significant faults you have cracked - that story is your real resume and, later, your interview material.</p>"
 ),
 "Personal Development Plan": (
  "<p class='lec'>A development plan turns &#39;I should learn more&#39; into action. Pick one target skill and one target credential for the next 6-12 months, name the concrete resources (a course, a manual, a lab kit), and schedule practice - even 30 minutes of ladder logic or a datasheet a day compounds fast. Tie each skill to a real problem at your site so learning has an immediate payoff.</p>"
  "<p class='lec'>Review and adjust quarterly. The technicians who advance are not the ones with the most raw talent - they are the ones who kept a steady, deliberate learning habit while everyone else waited for training to be handed to them. Use this academy&#39;s tracks and the Reference Library as your running toolkit.</p>"
 ),
}


DEEP[13] = {
 "Structured Text": (
  "<p class='lec'><b>Structured Text (ST)</b> is the Pascal-like text language of IEC 61131-3, and it shines exactly where ladder gets ugly: math, loops, string handling, and complex decisions. An IF/ELSIF/CASE tree that would sprawl across twenty rungs is a few readable lines of ST. FOR and WHILE loops process arrays; functions return computed values.</p>"
  "<p class='lec'>The trade-off is visibility - you cannot watch power flow through ST the way you watch a ladder rung light up, so it is harder to troubleshoot live and easier to hide a bug. Best practice mixes languages: ladder for discrete interlocks you must watch, ST for the algorithms. Beware loops that could run unbounded within one scan and blow your scan time - keep iteration counts sane.</p>"
 ),
 "Add-On Instructions": (
  "<p class='lec'><b>Add-On Instructions (AOIs)</b> let you package a block of logic into a reusable, custom instruction - write and test a &#39;Conveyor&#39; or &#39;ValveControl&#39; block once, then drop it in as many times as you need. It is encapsulation for PLC code: the internal logic is protected and consistent, and a fix to the definition propagates to every instance.</p>"
  "<p class='lec'>The payoff is huge on large projects - twenty identical conveyors become twenty instances of one tested AOI instead of twenty hand-copied (and subtly different) copies. AOIs improve reliability, shrink the program, and make maintenance sane. The Siemens equivalent concept is the reusable function block (FB) with its instance data.</p>"
 ),
 "User-Defined Types": (
  "<p class='lec'><b>User-Defined Types (UDTs)</b> let you bundle related tags into one structured data type - a &#39;Motor&#39; UDT might contain .Run, .Speed, .Fault, .Hours. Create one Motor tag and you get all its members organized together, and an array of Motor UDTs models a whole line cleanly.</p>"
  "<p class='lec'>UDTs make code self-documenting and consistent: every motor in the plant has the same structure, so logic and HMI bindings become uniform and reusable. They pair naturally with AOIs - the AOI operates on a UDT. This structured approach is the difference between an amateur tag list and a professional, maintainable program.</p>"
 ),
 "Fault Handling": (
  "<p class='lec'>Professional programs plan for failure. Controllers have <b>fault routines</b> that catch runtime errors (array index out of range, divide-by-zero, bad indirect address) so the processor can respond gracefully instead of faulting to a dead stop. A <b>major fault</b> halts the CPU; a well-designed program traps recoverable ones and logs them.</p>"
  "<p class='lec'>Beyond CPU faults, build explicit <b>machine fault handling</b>: detect abnormal conditions (jam, over-temp, lost feedback), latch a clear fault code, drive the machine to a safe state, and surface a meaningful message to the HMI. Good fault handling is what turns a cryptic dead machine into &#39;Fault 214: Zone 3 photo-eye blocked&#39; - which is the difference between minutes and hours of downtime.</p>"
 ),
 "State Machines": (
  "<p class='lec'>A <b>state machine</b> is the cleanest way to program any sequential process - the machine is always in exactly one defined <b>state</b> (Idle, Starting, Running, Stopping, Faulted), and it moves between states only on defined <b>transitions</b>. Each state has clear entry actions and exit conditions, so behavior is predictable and easy to follow.</p>"
  "<p class='lec'>Contrast this with a tangle of interlocked timers and latches where nobody can say what the machine will do next - the classic unmaintainable program. A state machine (often implemented in ST with a CASE statement, or graphically in SFC) makes the sequence explicit, easy to extend, and easy to troubleshoot because you can always ask &#39;what state am I in and why won&#39;t I transition?&#39;</p>"
 ),
}

DEEP[14] = {
 "What Is IIoT": (
  "<p class='lec'>The <b>Industrial Internet of Things (IIoT)</b> is the extension of the automation pyramid upward and outward - connecting machines, sensors, and controllers so their data flows to analytics, dashboards, and cloud systems. <b>Industry 4.0</b> is the broader vision: smart, connected, data-driven factories where decisions are made on real-time information across the whole operation.</p>"
  "<p class='lec'>The practical payoff is <b>predictive maintenance</b> and optimization - instead of fixing a bearing after it fails, you watch its vibration trend and replace it on your schedule. For an RME technician this is not hype: it is why more sensors, edge devices, and data historians keep appearing on equipment, and why controls knowledge now overlaps with data and networking skills.</p>"
 ),
 "Edge-Fog-Cloud": (
  "<p class='lec'>IIoT data is processed at three tiers, and putting work at the right tier is the whole design art. The <b>edge</b> (on or beside the machine) handles fast, local decisions and filters raw data - you do not ship every millisecond of vibration to the cloud. The <b>fog</b> (site/gateway level) aggregates and does mid-level analytics. The <b>cloud</b> stores history and runs heavy analytics and machine learning across many sites.</p>"
  "<p class='lec'>The guiding rule: keep latency-critical and high-volume processing at the edge, push long-term storage and cross-site intelligence to the cloud. Edge computing also keeps the line running if the internet drops, and cuts bandwidth cost. Understanding this hierarchy tells you where a given piece of logic or data actually lives when you troubleshoot an IIoT system.</p>"
 ),
 "MQTT": (
  "<p class='lec'><b>MQTT</b> is the lightweight messaging protocol that dominates IIoT because it is efficient and elegant. It uses <b>publish/subscribe</b>: devices publish data to named <b>topics</b> on a central <b>broker</b>, and any client that cares subscribes to those topics. Publishers and subscribers never need to know about each other - the broker decouples them, so you add new consumers of data without touching the source.</p>"
  "<p class='lec'>Its tiny overhead suits thousands of sensors on constrained networks, and features like QoS levels and retained messages make it reliable. In industrial use, <b>Sparkplug B</b> adds a standard topic structure and state awareness on top of MQTT. Contrast it with request/response polling (like Modbus or OPC-UA read) - MQTT&#39;s report-by-exception model scales far better for many devices.</p>"
 ),
 "OT Cybersecurity": (
  "<p class='lec'>Connecting machines to networks creates attack surface, and in OT a breach can stop production or endanger people - so security is now part of the job. <b>IEC 62443</b> is the governing standard. Its cornerstone concept is <b>zones and conduits</b>: group assets into security zones and tightly control the conduits (connections) between them, especially between the OT network and IT/internet.</p>"
  "<p class='lec'>Practical defenses: network segmentation and firewalls (the OT/IT DMZ), <b>least privilege</b> access, patching where feasible, disabling unused ports/services, and monitoring for anomalies. The mindset shift for technicians: never plug an unknown USB or laptop into a control network, treat remote-access carefully, and understand that the same connectivity that enables IIoT is what you must defend. <b>Defense in depth</b> - many layers - is the strategy.</p>"
 ),
}

DEEP[15] = {
 "DMM Mastery": (
  "<p class='lec'>The digital multimeter is your primary sense on the floor, and mastery means knowing not just how to read it but how to <i>trust</i> it. Voltage is measured <b>across</b> a component (in parallel); current is measured <b>through</b> the circuit (in series, meter in the path). Resistance and continuity must be done <b>de-energized</b> - measuring resistance on a live circuit gives garbage and can damage the meter.</p>"
  "<p class='lec'>Core techniques: check for voltage first to confirm a circuit is dead before touching it (safety), use continuity to find open wires and blown fuses, and use the <b>voltage-drop method</b> to find high-resistance connections a resistance test misses under load. Know your meter&#39;s CAT rating for the voltage you are in, verify it on a known source before and after (the &#39;live-dead-live&#39; check), and respect that a meter is only as good as your lead placement and range selection.</p>"
 ),
 "Megohmmeter": (
  "<p class='lec'>A regular ohmmeter tests continuity at low voltage; a <b>megohmmeter (megger)</b> tests <b>insulation</b> by applying a high DC voltage (250-1000 V+) and measuring leakage in the megohm-to-gigohm range. It is how you catch a motor or cable whose insulation is breaking down <i>before</i> it faults to ground and takes out a drive.</p>"
  "<p class='lec'>Critical rules: the equipment must be de-energized, isolated, and discharged first, and disconnect sensitive electronics that the high voltage would destroy. Test winding-to-ground and compare against a baseline and the one-megohm-per-kV rule of thumb. A trend of falling insulation resistance over months is a classic predictive-maintenance win - you schedule the motor swap instead of suffering the failure.</p>"
 ),
 "Systematic Troubleshooting": (
  "<p class='lec'>The single trait that separates great troubleshooters from parts-swappers is <b>method</b>, not knowledge. A repeatable process: (1) define the problem precisely - what exactly is and is not working; (2) gather information - what changed, error codes, when it started; (3) form a hypothesis about the most likely cause; (4) test that hypothesis with one measurement; (5) fix and verify; (6) document.</p>"
  "<p class='lec'>Two powerful tactics: <b>divide and conquer</b> - test at the middle of a chain to instantly halve the suspect area (is the signal good here? then the fault is downstream) - and <b>question what changed</b>, because most faults follow a change. Resist the urge to shotgun parts; it is expensive, it masks the real cause, and it can create new faults. Slow is smooth, smooth is fast.</p>"
 ),
 "Oscilloscope": (
  "<p class='lec'>Where a DMM gives you one number, an <b>oscilloscope</b> shows you the signal&#39;s <i>shape over time</i> - and some faults only reveal themselves as a shape. Encoder pulse trains, PWM drive outputs, communication waveforms, sensor glitches, and intermittent noise are invisible to a meter but obvious on a scope.</p>"
  "<p class='lec'>The two controls that matter: <b>timebase</b> (horizontal, seconds per division - sets how much time you see) and <b>volts-per-division</b> (vertical, sets the amplitude scale). <b>Triggering</b> is the skill that makes a scope useful - it tells the scope when to start drawing so a repeating or one-shot event stands still on screen instead of racing by. Reach for a scope when you suspect timing, noise, or signal-integrity problems that a steady voltage reading cannot explain.</p>"
 ),
}

DEEP[16] = {
 "Maintenance Strategies": (
  "<p class='lec'>There is a spectrum of maintenance philosophies, and mature sites blend them. <b>Reactive (run-to-failure)</b> - fix it when it breaks - is cheapest up front but causes unplanned downtime and collateral damage; it is acceptable only for cheap, non-critical parts. <b>Preventive (PM)</b> - service on a time or cycle schedule - prevents many failures but can waste life on parts that were still fine.</p>"
  "<p class='lec'><b>Predictive (PdM)</b> uses condition monitoring (vibration, thermography, oil analysis, insulation trends) to fix things <i>just before</i> they fail - the sweet spot for critical equipment. <b>Reliability-Centered Maintenance (RCM)</b> is the strategy layer that decides, per asset, which of these to use based on criticality and failure modes. The goal is not maximum maintenance - it is the right maintenance on the right asset at the right time.</p>"
 ),
 "Key Metrics": (
  "<p class='lec'>You cannot improve what you do not measure, and a few metrics run the reliability world. <b>MTBF (Mean Time Between Failures)</b> tracks how reliable an asset is - rising MTBF means your maintenance is working. <b>MTTR (Mean Time To Repair)</b> tracks how fast you recover - lowering MTTR is about spares, access, and skill. <b>Availability</b> combines them: uptime / (uptime + downtime).</p>"
  "<p class='lec'><b>OEE (Overall Equipment Effectiveness)</b> multiplies Availability x Performance x Quality into one number that exposes hidden losses. And in the fulfillment world you will live with <b>DPMO</b> (defects per million opportunities) as a jam/fault rate. The point of metrics is to aim effort - they turn &#39;the sorter feels unreliable&#39; into a number you can attack and prove you improved.</p>"
 ),
 "Vibration Analysis": (
  "<p class='lec'>Rotating machines tell you what is wrong through <b>vibration</b>, if you know how to listen. Every fault has a signature frequency: <b>imbalance</b> shows up at 1x running speed, <b>misalignment</b> at 1x and 2x (often axial), <b>looseness</b> as many harmonics, and <b>bearing defects</b> as characteristic high frequencies (BPFO, BPFI) that appear early - long before the bearing gets audibly bad.</p>"
  "<p class='lec'>The tool is spectrum analysis: an accelerometer&#39;s signal is transformed (FFT) from a messy time waveform into a frequency spectrum where each peak points at a specific problem. This is the heart of predictive maintenance on motors, gearboxes, and fans - a monthly trend catches the failing bearing while you can still plan the swap, instead of it seizing on shift.</p>"
 ),
 "PM Program Design": (
  "<p class='lec'>Designing a PM program is about spending maintenance effort where it pays. Start by <b>ranking assets by criticality</b> (what does it cost the operation if this fails?), then for the critical ones identify likely failure modes and choose the maintenance strategy that addresses each. Build PM tasks that are specific, measurable, and actually tied to a failure mode - not &#39;inspect motor&#39; but &#39;check winding temperature, measure vibration, verify mounting torque.&#39;</p>"
  "<p class='lec'>Set intervals from real failure data and manufacturer guidance, then <b>refine using your metrics</b> - if a PM interval is too long you see failures between PMs; too short and you waste labor. A good program is a living thing: review MTBF and failure records and adjust. The CMMS/EAM system is where all this lives, schedules, and gets tracked.</p>"
 ),
}

DEEP[17] = {
 "Standards": (
  "<p class='lec'>A control panel is not wired to taste - it follows codes so it is safe, inspectable, and maintainable by the next person. In North America, <b>UL 508A</b> governs industrial control panel construction and <b>NFPA 79</b> covers the electrical standard for industrial machinery; <b>NEC</b> covers the installation. In much of the world <b>IEC 60204-1</b> is the equivalent. These dictate wire sizing, protection, grounding, spacing, and labeling.</p>"
  "<p class='lec'>Why you care as a technician: a code-compliant panel is documented, has proper short-circuit protection and a known <b>SCCR (short-circuit current rating)</b>, uses consistent wire colors and numbering, and is grounded correctly - which makes it dramatically faster and safer to troubleshoot. When you modify a panel, you are responsible for keeping it compliant.</p>"
 ),
 "Component Selection": (
  "<p class='lec'>Right-sizing components is where safety and reliability are designed in. Overcurrent protection (breakers, fuses) must protect the wire and be coordinated so the nearest device trips first (selectivity). Contactors and overloads are sized to the motor&#39;s FLA and duty. The <b>control transformer</b> is sized to the inrush VA of everything it powers. Wire gauge is chosen for the ampacity and voltage drop over the run.</p>"
  "<p class='lec'>Do not forget the environment: enclosure <b>NEMA/IP rating</b> for dust and washdown, thermal management (a packed panel overheats and derates components), and the panel&#39;s overall SCCR must exceed the available fault current at its location. Undersized or mismatched components cause the nuisance trips and premature failures you will otherwise chase forever.</p>"
 ),
 "Wiring Practices": (
  "<p class='lec'>Neat wiring is not vanity - it is troubleshootability and reliability. Route power and low-level signal wiring <b>separately</b> to avoid coupling VFD and motor noise into sensor and comm circuits (a top cause of phantom faults). Use wire duct, keep bends gentle, land wires on proper terminals with the right ferrules, and torque connections to spec - loose terminals are the number-one cause of intermittent, heat-generating faults.</p>"
  "<p class='lec'>Above all, <b>label everything</b> and keep the wire numbers matching the drawing. Ground and bond correctly, and use shielded cable grounded at one end for analog and comm signals. A panel wired to good practice can be traced with a print and a meter; a rat&#39;s nest costs hours every time it faults.</p>"
 ),
 "Commissioning": (
  "<p class='lec'>Panel commissioning is the safety-critical checkout before power-up, done in strict order. <b>Before energizing:</b> verify wiring against the drawings, check every ground/bond, meter for shorts and correct isolation, confirm component ratings, and make sure nothing is left loose or shorting. Then energize the control power first and verify voltages before bringing up the power circuits.</p>"
  "<p class='lec'>Then <b>point-to-point I/O checks</b> (force each output, actuate each input), function tests, and finally integrated operation - the same bottom-up discipline as system commissioning. Rushing straight to &#39;run&#39; on an unchecked panel risks a fault that damages equipment or people. A methodical commissioning is cheap insurance against an expensive, dangerous surprise.</p>"
 ),
}

DEEP[18] = {
 "Technical Portfolio": (
  "<p class='lec'>Your real resume is not a list of job titles - it is the <b>problems you have solved.</b> Keep a running portfolio: significant faults you cracked (and how), projects you built or improved, tools and scripts you made, certifications earned, and the equipment/brands you know. Capture the &#39;before, action, result&#39; for each - especially anything you can quantify (downtime cut, DPMO reduced, a recurring fault eliminated).</p>"
  "<p class='lec'>This does two things: it makes interviews easy because you have concrete stories ready, and it makes <i>you</i> aware of your own growth. Update it right after you solve something notable, while the details are fresh. A technician who can walk into a review and show a documented track record of solved problems stands far above one who just says &#39;I fix things.&#39;</p>"
 ),
 "Interview Preparation": (
  "<p class='lec'>Technical interviews for controls/maintenance roles test two things: fundamentals and how you <b>think through a problem.</b> Expect to explain Ohm&#39;s law, the PLC scan cycle, how a VFD works, how you would troubleshoot a specific down machine, and safety/LOTO. Prepare by being able to teach each core concept simply - if you can explain it to a new hire, you understand it.</p>"
  "<p class='lec'>For the &#39;walk me through how you would fix X&#39; questions, use your systematic method out loud: define the problem, gather info, hypothesize, test at the middle, verify. Bring your portfolio stories using a simple structure (situation, what you did, result). And prepare questions of your own about their equipment and reliability culture - it shows you think like a professional.</p>"
 ),
 "Certification Roadmap": (
  "<p class='lec'>Certifications prove your skills to people who have not seen you work, and a sensible order builds on itself. Foundational: <b>SACA</b> (modern automation, C-101/C-201) and <b>ISA CCST</b> (control systems technician, levels I-III) validate broad fundamentals. Then <b>vendor certs</b> where you specialize - Rockwell/Allen-Bradley, Siemens, or an OEM <b>FANUC robot</b> cert - carry real weight because employers run that gear.</p>"
  "<p class='lec'>Add safety credentials as relevant. Do not chase certs for their own sake - pick the one that matches the equipment at your site or the role you want next, so the studying doubles as job skill. Pair each cert with hands-on practice; a cert plus demonstrated ability is unbeatable, a cert alone is thin.</p>"
 ),
 "12-Month Plan": (
  "<p class='lec'>Turn everything in this academy into a concrete year. A workable template: <b>Quarter 1</b> - lock down fundamentals (electrical, PLC basics) and start your portfolio. <b>Q2</b> - go deep on one specialty that matters at your site (drives, or a PLC platform) and begin a foundational cert. <b>Q3</b> - earn that cert, take on harder troubleshooting calls deliberately. <b>Q4</b> - add a specialty/vendor cert and review your growth.</p>"
  "<p class='lec'>Make it specific and reviewable: name the resources, block the time (consistency beats intensity - a little daily), and tie each goal to a real problem or piece of equipment. Revisit the plan quarterly and adjust. The technicians who advance are simply the ones who ran a deliberate plan while others drifted - use the tracks and Reference Library here as your engine.</p>"
 ),
}


# Key Takeaways per module - the 4-5 must-remember points, rendered as a
# "Recap - Lock It In" phase after the quiz. build attaches m["takeaways"].
TAKEAWAYS = {
 0: ["AET is the blend of electrical, controls, and mechanical skill that keeps a facility running",
     "The automation pyramid is a troubleshooting map: locate the symptom, then look up or down",
     "The ten domains are ten views of the same machine, not ten separate careers",
     "Everything ladders up to one payoff: cutting downtime"],
 1: ["Ohm&#39;s Law (V=IxR) and P=VxI are your most-used tools - build intuition, not just recall",
     "AC meters read RMS; insulation must survive the higher peak voltage",
     "Three-phase line voltage is &radic;3 x phase voltage (480/277, 208/120)",
     "The start/stop seal-in rung is the pattern behind most control logic - know it cold",
     "Read ladders top-to-bottom, left rail to right; an unbroken closed path turns the output on"],
 2: ["A PLC replaced walls of relays with software you can change by download, not rewiring",
     "The scan cycle (read inputs, run program on the snapshot, write outputs) explains most beginner confusion",
     "Same bit written twice = last rung wins; a pulse faster than one scan can be missed",
     "XIC/XIO describe how the instruction reads the bit, not the field device wiring",
     "Match sensor type (PNP/NPN) to the input card or the PLC never sees the signal"],
 3: ["TON accumulates while true and sets Done at preset; TOF delays the off; RTO retains across power",
     "Counters trigger on false-to-true edges - they count events, not held time",
     "Watch integer vs float math (5/2=2) and guard against divide-by-zero",
     "Organize code into routines by area/function - the next tech to read it is often you at 3 a.m."],
 4: ["Discrete sensors answer yes/no; analog instruments give a value",
     "4-20 mA beats 0-10 V: immune to wire drop, and 0 mA = broken wire (live zero)",
     "Encoders turn motion into counts for position, speed, and direction",
     "Scaling is a linear map from raw counts to engineering units; calibration trims real-world error",
     "A miscalibrated loop reads plausible-but-wrong - the most dangerous fault"],
 5: ["Induction motors need slip to make torque; sync speed = 120xf/poles",
     "A VFD rectifies to DC then inverts to a chosen frequency to set motor speed",
     "Constant Volts-per-Hz keeps torque steady as speed changes",
     "Fault on accel = load/ramp; on decel = bus overvoltage; at steady state = thermal/supply",
     "The nameplate drives your protection settings and troubleshooting baselines"],
 6: ["Pneumatics = fast/cheap/springy (air compresses); hydraulics = huge precise force (oil doesn&#39;t)",
     "The FRL and clean fluid prevent most fluid-power faults",
     "Read valve envelopes: ports and positions name the valve and show the flow path",
     "Trace pressure and flow from supply toward the actuator to find where it stops",
     "Many &#39;mechanical&#39; faults are really the electrical signal that never reached the solenoid"],
 7: ["HMI = local one-machine view; SCADA = plant-wide supervision, logging, and alarms",
     "ISA-101: calm gray normal, bright color only for abnormal - so problems jump out",
     "Tags link the screen to PLC values; frozen/wrong values usually mean binding or poll-rate, not the PLC",
     "ISA-18.2 fights alarm floods: every alarm must be actionable and prioritized"],
 8: ["Networks are layered OT (deterministic, segmented) vs IT (business) - keep them separated",
     "EtherNet/IP and PROFINET add determinism to standard Ethernet; every device needs a unique IP",
     "OPC-UA is the vendor-neutral, secure translator that feeds IIoT dashboards",
     "Troubleshoot bottom-up: physical layer, then addressing (ping), then configuration",
     "Plant intermittents are usually physical (vibration, EMI from VFDs), not software"],
 9: ["Match robot type to task: articulated=flexible, SCARA/Delta=fast pick, Cartesian=simple travel, AMR=mobile",
     "Frames (base, tool/TCP, user) keep programmed points correct across gripper/fixture changes",
     "Joint moves are fastest; linear moves keep the TCP straight for process work",
     "Robots can kill - never defeat an interlock, always LOTO before entering the envelope (ISO 10218/15066)"],
 10:["Closed-loop measures and self-corrects (PV vs SP); open-loop is blind",
     "P reacts to present error, I to accumulated past error, D to rate of change",
     "Sluggish=more P/I; overshoot/oscillate=too much gain/I; jittery=too much D",
     "Auto-tune gives a starting point; refine by watching the real response",
     "A P&amp;ID balloon tag (ISA-5.1) encodes the variable + function: FIC, LT, PSH"],
 11:["Risk assessment first - you can&#39;t safeguard a hazard you haven&#39;t identified",
     "Hierarchy of controls: eliminate &gt; engineer/guard &gt; administrative &gt; PPE",
     "Choose safeguarding by access need: fixed guard, interlocked gate, or presence sensing",
     "ISO 13849 sets required Performance Level; high-risk needs redundant, monitored circuits",
     "LOTO: your own lock, verify zero energy; respect arc flash - de-energize when you can"],
 12:["Real machines are systems; faults hide in the seams between domains",
     "Trace &#39;where does this signal come from, what commands it, where does it go&#39; across every domain",
     "Commission bottom-up: wiring, then I/O point checks, then functions, then full rate - never skip ahead",
     "Grow by depth + proof: master an area, earn the matching cert, take the hard calls",
     "Keep a record of the faults you cracked - it&#39;s your real resume"],
 13:["Structured Text wins for math/loops/complex decisions but is harder to watch live",
     "AOIs package tested logic into reusable custom instructions - fix once, propagate everywhere",
     "UDTs bundle related tags (.Run/.Speed/.Fault) into consistent, self-documenting structures",
     "Fault routines and explicit machine faults turn a dead machine into &#39;Fault 214: Zone 3 photo-eye&#39;",
     "State machines (one defined state at a time) make sequences predictable and easy to troubleshoot"],
 14:["IIoT/Industry 4.0 connects machines to analytics; the payoff is predictive maintenance",
     "Put latency-critical and high-volume work at the edge; storage and cross-site intelligence in the cloud",
     "MQTT publish/subscribe decouples devices via a broker and topics - scales to thousands of sensors",
     "IEC 62443: zones and conduits, least privilege, segmentation - never plug unknown gear into control networks"],
 15:["Voltage across (parallel), current through (series), resistance/continuity de-energized only",
     "Do the live-dead-live check to trust your meter; know your CAT rating",
     "Voltage-drop under load finds high-resistance connections a resistance test misses",
     "A megger tests insulation with high DC - trend it to catch motor breakdown before it faults",
     "Systematic method beats knowledge: define, gather, hypothesize, test at the middle, verify - don&#39;t shotgun parts",
     "Reach for a scope when timing, noise, or signal shape matters; master triggering"],
 16:["Blend strategies: reactive for cheap parts, preventive on schedule, predictive for critical assets",
     "MTBF = reliability, MTTR = recovery speed, availability combines them, OEE exposes hidden losses",
     "Vibration signatures pinpoint faults: 1x=imbalance, 1x/2x=misalignment, harmonics=looseness, high-freq=bearings",
     "Design PMs from criticality and real failure data, then refine using your metrics",
     "The CMMS/EAM is where the program lives, schedules, and gets tracked"],
 17:["Panels follow codes (UL 508A, NFPA 79, NEC / IEC 60204-1) so they&#39;re safe and inspectable",
     "Size protection, contactors, transformers, and wire to the load; the panel SCCR must exceed available fault current",
     "Separate power and signal wiring, torque terminals to spec, label everything to the drawing",
     "Commission a panel bottom-up: verify wiring/grounds/shorts de-energized, then control power, then power circuits"],
 18:["Your portfolio of solved problems is your real resume - capture before/action/result, quantified",
     "Interviews test fundamentals + how you think; explain concepts simply and walk your method out loud",
     "Certs (SACA, ISA CCST, then vendor/FANUC) prove skills - pick ones matching your site&#39;s gear",
     "Run a deliberate 12-month plan with named resources and daily practice - consistency beats intensity"],
}
