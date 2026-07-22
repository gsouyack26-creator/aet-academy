# -*- coding: utf-8 -*-
"""AET Academy - 'In the Field' real-world applications.
Each module gets 2 scenarios that reiterate the SAME core concept in DIFFERENT
real-world contexts (fulfillment-center / Amazon-Robotics + an everyday parallel),
each ending with the concept restated. Interleaving + varied examples lowers the
learning curve and builds transfer. Rendered as trusted HTML after the reading."""

def app(ctx, body):
    return {"ctx": ctx, "body": body}

R = "<p class='appr'><b>Remember:</b> %s</p>"

APPLICATIONS = {
 0: [
   app("On the sortation floor",
     "<p>Walk a package from induct to chute and you touch every layer of the automation pyramid: a photo-eye (field device) sees the box, a PLC (control) decides the chute, an HMI/SCADA (supervisory) shows the rate, and reports roll up to the business layer. One jam clears faster when you know which layer owns the problem.</p>" +
     (R % "Automation is layered - field devices sense, controllers decide, supervisory systems watch, and business systems plan.")),
   app("Your car as a control system",
     "<p>Your car is the same pyramid: sensors (O2, wheel speed) feed the ECU (controller), the dash is your HMI, and the dealer's diagnostics are the business layer. You already troubleshoot by layer - &lsquo;is it the sensor or the computer?&rsquo;</p>" +
     (R % "Every automated system - a sorter or a car - splits into sense, decide, display, plan. Find the layer, find the fault.")),
 ],
 1: [
   app("Conveyor motor starter",
     "<p>A belt won't run. The start button energizes a contactor coil; a seal-in contact latches it; the overload relay protects the motor. Ohm's law tells you the 24V coil pulling 0.2A needs ~120&Omega; - measure it. No seal-in = motor stops the instant you release start.</p>" +
     (R % "V = I x R governs every circuit, and a seal-in contact is what keeps a motor running after you let go of the button.")),
   app("A wall outlet at home",
     "<p>The same rules run your house. A 120V outlet feeding a 10&Omega; heater draws 12A (I = V/R) and dissipates ~1440W (P = V x I). Overload that circuit and the breaker - your overload protection - trips, exactly like the conveyor's overload relay.</p>" +
     (R % "The identical Ohm's-law and overprotection ideas scale from a shop motor to your kitchen outlet.")),
 ],
 2: [
   app("Divert logic on a sorter",
     "<p>A box hits a scan zone: photo-eye ON (input) plus a &lsquo;divert-to-chute-7&rsquo; command makes the PLC energize a divert output. The processor reads inputs, solves the ladder, then updates outputs - once per scan, a few milliseconds.</p>" +
     (R % "A PLC repeats read-inputs, solve-logic, write-outputs every scan - outputs only change at the end of the scan.")),
   app("A smart garage door",
     "<p>Home automation is the same loop: a button and a safety-beam (inputs) let the controller decide to run the door motor (output), and it re-checks the beam every cycle. Break the beam mid-close and the next scan reverses it.</p>" +
     (R % "Whether a sorter or a garage door, the controller endlessly scans inputs, decides, and drives outputs.")),
 ],
 3: [
   app("Accumulation counter + jam timer",
     "<p>A counter tallies boxes past a photo-eye; when it hits a batch size, the PLC releases them. A timer watches the same eye - if it stays blocked longer than 3 seconds, a jam timer times out and faults the zone.</p>" +
     (R % "Counters track how many; timers track how long. Together they turn raw sensor pulses into decisions.")),
   app("A parking garage &lsquo;FULL&rsquo; sign",
     "<p>Cars in minus cars out is a counter; when it equals capacity the &lsquo;FULL&rsquo; sign lights. A gate that must stay open a minimum time uses a timer. Same two instructions, different building.</p>" +
     (R % "Count events with counters, measure durations with timers - the two most-used PLC instructions anywhere.")),
 ],
 4: [
   app("Photo-eye + level on a diverter",
     "<p>A retroreflective photo-eye (discrete) confirms a box is present; a 4-20mA sensor reports an analog value like belt tension. At 12mA you're at 50% of span: EU = ((12-4)/16) x span + min. A broken wire reads 0mA - the live zero flags the fault.</p>" +
     (R % "Discrete sensors answer yes/no; 4-20mA sensors report how much, and 4mA (not 0) means &lsquo;alive and zero&rsquo;.")),
   app("A home thermostat",
     "<p>Your thermostat's temp sensor is an analog input scaled to degrees, and the &lsquo;is-someone-home&rsquo; motion sensor is discrete. Same split as the plant: analog for a value, discrete for a state.</p>" +
     (R % "Pick discrete for on/off states and analog (like 4-20mA) for measured quantities - true in a plant or a house.")),
 ],
 5: [
   app("VFD soft-start on a belt",
     "<p>Instead of slamming a belt to full speed, a VFD ramps frequency up, holding the V/Hz ratio (460V/60Hz = 7.67) for constant torque. Slower ramp = less belt shock and lower inrush. Push past 60Hz and you lose torque (field weakening).</p>" +
     (R % "A VFD varies motor speed by varying frequency, keeping V/Hz constant for steady torque up to base speed.")),
   app("A furnace blower fan",
     "<p>Modern HVAC uses a VFD on the blower: run it at 40Hz when demand is low and you save big energy (fan power drops with the cube of speed). Same drive, same V/Hz logic, in a mechanical room.</p>" +
     (R % "Slowing a motor with a VFD saves energy and reduces wear - fans and pumps benefit the most.")),
 ],
 6: [
   app("Pneumatic pusher arm",
     "<p>An air cylinder shoves a box off the line. Force = pressure x piston area, so an 80psi supply on a 2&quot; bore piston pushes ~250 lb. A solenoid valve, triggered by the PLC, ports air to extend or retract. Air is fast and springy - perfect for quick, light pushes.</p>" +
     (R % "Cylinder force = pressure x area; pneumatics give fast, clean, moderate-force motion.")),
   app("A hydraulic dock leveler",
     "<p>The dock plate a truck backs onto lifts with hydraulics - same F = P x A, but at 2000+ psi with oil, so it moves heavy loads smoothly. Oil doesn't compress, so it holds position under load where air would sag.</p>" +
     (R % "Same force formula, but hydraulics trade speed for high, controlled force on heavy loads.")),
 ],
 7: [
   app("A sorter HMI",
     "<p>The operator screen shows live throughput, which chutes are full, and active faults with timestamps. It's a window into the PLC's data - the HMI doesn't run the machine, it visualizes and lets an operator acknowledge alarms or jog a zone.</p>" +
     (R % "An HMI/SCADA visualizes and commands the process; the PLC is still the one making real-time decisions.")),
   app("A building management dashboard",
     "<p>A facility's BMS screen shows zone temps, fan status, and energy use - the exact same idea as the sorter HMI, just for HVAC and lighting. Operators watch trends and set points; controllers do the work.</p>" +
     (R % "Whether a sorter or a building, supervisory screens watch and adjust while controllers execute.")),
 ],
 8: [
   app("EtherNet/IP on the controls network",
     "<p>PLCs, drives, and remote I/O talk over EtherNet/IP on a managed switch. Each device needs an IP on the same subnet (e.g. 192.168.1.x /24) to communicate. A duplicate IP or a device on the wrong subnet goes silent - a common &lsquo;comms fault&rsquo;.</p>" +
     (R % "Industrial Ethernet devices must share a subnet and have unique IPs to talk - just like any network.")),
   app("Your home Wi-Fi",
     "<p>Your router hands out 192.168.x addresses on one subnet so phones and TVs can reach each other and the gateway to the internet. Same addressing rules the plant uses - the concepts you know at home transfer directly.</p>" +
     (R % "IP addressing, subnets, and gateways work identically at home and on the plant floor.")),
 ],
 9: [
   app("An Amazon Robotics drive fleet",
     "<p>Hundreds of drives move pods across the floor - each is closed-loop motion control: commanded position vs. encoder feedback, corrected continuously. Fiducial markers and a central system coordinate paths, but each drive servos its own wheels precisely.</p>" +
     (R % "Motion control = command a position/velocity, measure with feedback (encoders), and correct the error in a loop.")),
   app("A palletizing robot arm",
     "<p>A 6-axis arm stacking cases uses the same closed-loop control per joint, plus coordinated motion so the tool follows a planned path. Feedback devices tell the controller where each joint actually is, every cycle.</p>" +
     (R % "From mobile drives to arms, motion control always closes the loop between command and measured position.")),
 ],
 10: [
   app("Belt tension / speed loop",
     "<p>To hold a set tension, a controller compares measured tension (PV) to the target (SP) and trims motor speed. Too much P and it hunts; add I to erase steady offset; D only if needed. The loop never &lsquo;arrives&rsquo; - it constantly nudges toward setpoint.</p>" +
     (R % "PID drives the process variable toward setpoint: P reacts to error, I removes offset, D dampens.")),
   app("Room temperature control",
     "<p>A smart thermostat is a PID (or PI) loop: it doesn't just switch at a threshold, it modulates heating to hold 70&deg;F without overshoot. The same P/I/D behaviors you tune on a line tune your comfort at home.</p>" +
     (R % "Any loop holding a value at setpoint - tension or temperature - is doing the same PID job.")),
 ],
 11: [
   app("A robotic cell",
     "<p>A light curtain guards the cell opening; break the beam and a safety relay commands a Category-1 stop. An e-stop and interlocked gate provide redundant, monitored paths. The safety function is rated (PL/SIL) for the risk - higher risk demands redundancy and monitoring.</p>" +
     (R % "Safeguarding senses the hazard and commands a rated safe stop; higher risk = higher PL/SIL and redundancy.")),
   app("A sorter access door",
     "<p>Open a guard door to clear a jam and a coded interlock drops power to the zone - the same principle as the robot cell, scaled to a conveyor. LOTO takes over for hands-in-the-machine work: isolate, lock, verify zero energy.</p>" +
     (R % "Guards and interlocks stop motion when opened; LOTO controls energy for real hands-on work.")),
 ],
 12: [
   app("Adding an induct to a live sorter",
     "<p>Integrating a new induction line means tying its PLC to the existing network, mapping its I/O, matching the HMI, and proving safety - every discipline in one project. Documentation and testing are what make it go live without taking down the running system.</p>" +
     (R % "System integration ties field devices, control, networks, HMI, and safety into one working whole.")),
   app("Planning your own upskilling",
     "<p>Your career is a system too: assess where you are (audit), pick target skills (design), build them project by project (integration), and verify with certs. Treat growth like commissioning a machine - staged and tested.</p>" +
     (R % "Integration thinking - assess, design, build, verify - works on a plant and on your own skill set.")),
 ],
 13: [
   app("A reusable divert AOI",
     "<p>Fifty divert stations behave identically, so you write one Add-On Instruction and reuse it - change the logic once, all stations update. Structured Text handles the math and fault-handling that ladder makes clumsy.</p>" +
     (R % "AOIs/functions package logic for reuse; Structured Text is best for math and complex decisions.")),
   app("Fault-handling routine",
     "<p>A dedicated ST routine watches for out-of-range values and drive faults, latches a first-out alarm, and holds diagnostic data for the tech. Reusable, structured code turns a mystery stop into a labeled fault.</p>" +
     (R % "Good structured code isolates faults and reports them clearly instead of just stopping.")),
 ],
 14: [
   app("Monitron on a gearbox",
     "<p>Wireless vibration/temperature sensors stream data to the cloud; ML flags a rising vibration signature days before a bearing fails. You get a work order before the breakdown - condition-based, not calendar-based, maintenance.</p>" +
     (R % "IIoT sensors + analytics predict failures early, shifting maintenance from reactive to predictive.")),
   app("A connected home",
     "<p>Smart thermostats and leak sensors report data and trigger alerts - the consumer version of IIoT. The same edge-to-cloud-to-insight chain the plant uses to catch a failing motor catches a leak in your basement.</p>" +
     (R % "Edge sensing plus cloud analytics turns raw data into early warnings, at the plant or at home.")),
 ],
 15: [
   app("A dead conveyor",
     "<p>Belt won't start. Prove-test-prove your meter, then half-split: is control voltage at the contactor coil? If yes, check the load side; if no, work back to the estop/overload/start string. Systematic beats guessing - you find it in minutes, not hours.</p>" +
     (R % "Troubleshoot by splitting the system and measuring - let readings, not hunches, point to the fault.")),
   app("A tripped breaker at home",
     "<p>An outlet's dead. Same method: is the breaker tripped (isolate the source), does it re-trip (a fault downstream), or is it just that outlet (open the circuit)? You already half-split at home without naming it.</p>" +
     (R % "The measure-and-split method finds a fault the same way on a machine or a house circuit.")),
 ],
 16: [
   app("A conveyor PM route",
     "<p>Scheduled PMs (belt tracking, bearing lube, sensor cleaning) catch wear early; vibration trending on drives adds predictive insight. A caught-early bearing is a 10-minute swap on a PM; a missed one is a line-down at 2am.</p>" +
     (R % "Preventive = time-based upkeep; predictive = condition-based. Both beat run-to-failure.")),
   app("Maintaining your car",
     "<p>Oil changes on a schedule are preventive; the dashboard's oil-life monitor is predictive. You already practice reliability maintenance - the plant just does it at scale with data.</p>" +
     (R % "Calendar service plus condition monitoring keeps a car - or a fleet of conveyors - from surprise failures.")),
 ],
 17: [
   app("Building a sorter control panel",
     "<p>Lay out the panel for airflow and access: line power to a disconnect, then breakers, contactors, a 24V supply, the PLC, and I/O - power segregated from signal. Neat wire duct, ferrules, and labeled conductors make the next tech's troubleshoot fast.</p>" +
     (R % "Good panel design separates power from signal, protects each circuit, and labels everything for service.")),
   app("A home load center",
     "<p>Your breaker panel is a control panel too: a main disconnect, branch breakers sized to their wire, a neutral and ground bus. The same &lsquo;protect each circuit, organize, label&rsquo; discipline keeps it safe and serviceable.</p>" +
     (R % "Whether an industrial panel or a house load center, protect each branch, organize, and label.")),
 ],
 18: [
   app("A portfolio from FC projects",
     "<p>That divert-logic fix or panel rebuild is portfolio gold: document the problem, your approach, and the result. Concrete plant projects prove skills better than a list of buzzwords in an interview.</p>" +
     (R % "Turn real work into documented projects - evidence beats claims when you advance.")),
   app("The interview scenario",
     "<p>Asked &lsquo;tell me about a tough troubleshoot,&rsquo; you walk the systematic method from Module 15 on a real jam. Reiterating what you've done, clearly and with results, is the whole game.</p>" +
     (R % "Communicate your real problem-solving story clearly - that is what lands the role.")),
 ],
}
