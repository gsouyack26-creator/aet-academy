# -*- coding: utf-8 -*-
"""AET Academy data layer: tracks, ranks, achievements, flashcards, simulator registry."""

# 5 learning tracks mapping all 19 modules (0-18)
TRACKS = [
  {"id":"found","name":"Foundations","icon":"&#9889;","color":"#e94560",
   "desc":"Electrical basics, motor control, and PLC fundamentals - the bedrock of automation.","mods":[0,1,2,3,19]},
  {"id":"field","name":"Field Devices & Drives","icon":"&#128225;","color":"#f39c12",
   "desc":"Sensors, instrumentation, motors, VFDs, fluid power, and material-handling conveyors - the muscles and senses of a machine.","mods":[4,5,6,20]},
  {"id":"systems","name":"Systems & Control","icon":"&#128421;","color":"#5dade2",
   "desc":"HMI/SCADA, industrial networks, robotics, PID process control, and Amazon Robotics / AMR fleets - tying it all together.","mods":[7,8,9,10,21]},
  {"id":"safety","name":"Safety & Advanced","icon":"&#128737;","color":"#27ae60",
   "desc":"Machine safety, advanced PLC programming, and IIoT / Industry 4.0.","mods":[11,13,14]},
  {"id":"reliab","name":"Reliability & Career","icon":"&#127942;","color":"#9b59b6",
   "desc":"System integration, troubleshooting, maintenance/reliability, panel design, and career growth.","mods":[12,15,16,17,18]}
]

# XP ranks - level thresholds (cumulative XP)
RANKS = [
  {"lvl":1,"name":"Apprentice","xp":0},
  {"lvl":2,"name":"Helper","xp":150},
  {"lvl":3,"name":"Junior Tech","xp":400},
  {"lvl":4,"name":"Technician","xp":800},
  {"lvl":5,"name":"Senior Tech","xp":1400},
  {"lvl":6,"name":"Controls Tech","xp":2200},
  {"lvl":7,"name":"Automation Specialist","xp":3200},
  {"lvl":8,"name":"Lead Technician","xp":4500},
  {"lvl":9,"name":"Controls Engineer","xp":6200},
  {"lvl":10,"name":"Automation Master","xp":8500}
]

# XP awards
XP = {"module_open":5,"quiz_correct":10,"quiz_perfect":40,"module_done":60,
      "flashcard":3,"flash_graduate":25,"sim_use":15,"exam_pass":300,"exam_ace":150,
      "track_done":250,"daily_visit":20}

# Achievement badges (evaluated in JS against state)
ACHIEVEMENTS = [
  {"id":"first_step","name":"First Step","icon":"&#128075;","desc":"Open your first module"},
  {"id":"quiz_ace","name":"Quiz Ace","icon":"&#127919;","desc":"Score 100% on a module quiz"},
  {"id":"sharpshooter","name":"Sharpshooter","icon":"&#127993;","desc":"Ace 5 different module quizzes"},
  {"id":"tinkerer","name":"Tinkerer","icon":"&#128295;","desc":"Use any lab simulator"},
  {"id":"lab_rat","name":"Lab Rat","icon":"&#129514;","desc":"Try every simulator at least once"},
  {"id":"flash_novice","name":"Flash Novice","icon":"&#128218;","desc":"Review 50 flashcards"},
  {"id":"flash_master","name":"Flash Master","icon":"&#127891;","desc":"Review 250 flashcards"},
  {"id":"halfway","name":"Halfway There","icon":"&#9878;","desc":"Complete 10 modules"},
  {"id":"track_done","name":"Track Finisher","icon":"&#127937;","desc":"Complete an entire track"},
  {"id":"graduate","name":"AET Graduate","icon":"&#127891;","desc":"Complete all 19 modules"},
  {"id":"exam_pass","name":"Certified","icon":"&#128220;","desc":"Pass the final exam (80%+)"},
  {"id":"exam_ace","name":"Distinction","icon":"&#11088;","desc":"Score 95%+ on the final exam"},
  {"id":"field_diag","name":"Field Diagnostician","icon":"&#128736;","desc":"Pass the Practical Skills Exam (75%+)"},
  {"id":"streak_3","name":"On a Roll","icon":"&#128293;","desc":"3-day study streak"},
  {"id":"streak_7","name":"Dedicated","icon":"&#128293;","desc":"7-day study streak"},
  {"id":"streak_30","name":"Unstoppable","icon":"&#128302;","desc":"30-day study streak"},
  {"id":"night_owl","name":"Night Owl","icon":"&#127765;","desc":"Study after 10 PM"},
  {"id":"early_bird","name":"Early Bird","icon":"&#127749;","desc":"Study before 6 AM"},
  {"id":"goal_met","name":"Goal Getter","icon":"&#127919;","desc":"Hit your daily study goal"},
  {"id":"module_examiner","name":"Examined","icon":"&#128221;","desc":"Pass a module exam (80%+)"},
  {"id":"module_scholar","name":"Scholar","icon":"&#127891;","desc":"Pass 5 module exams"},
  {"id":"collector","name":"Collector","icon":"&#11088;","desc":"Bookmark 5 items"}
]

# Curated concept flashcards (formulas + rules of thumb) - added on top of auto-generated glossary cards
FLASHCARDS = [
  {"f":"Ohm's Law","b":"V = I x R  (Volts = Amps x Ohms). Power: P = V x I = I&sup2; x R = V&sup2; / R"},
  {"f":"Three-phase power","b":"P = &#8730;3 x V(line) x I(line) x PF  (watts). &#8730;3 &approx; 1.732"},
  {"f":"Synchronous motor speed","b":"Ns (RPM) = 120 x f / poles.  60Hz, 4-pole = 1800 RPM synchronous"},
  {"f":"Motor slip","b":"Slip % = (Ns - Nfl) / Ns x 100.  Typical 2-5% at full load"},
  {"f":"VFD V/Hz ratio","b":"Constant V/Hz keeps motor flux steady. 460V / 60Hz &approx; 7.67 V/Hz"},
  {"f":"4-20 mA scaling","b":"% = (mA - 4) / 16 x 100.  EU = min + (%/100) x (max - min).  4mA = live zero"},
  {"f":"MTBF","b":"Mean Time Between Failures = total operating time / number of failures"},
  {"f":"MTTR","b":"Mean Time To Repair = total downtime / number of repairs"},
  {"f":"Availability","b":"A = MTBF / (MTBF + MTTR).  Uptime as a fraction of total time"},
  {"f":"OEE","b":"Overall Equipment Effectiveness = Availability x Performance x Quality. World-class &ge; 85%"},
  {"f":"PLC scan cycle","b":"1) Read inputs  2) Solve logic (top-to-bottom, left-to-right)  3) Write outputs  4) Housekeeping/comms"},
  {"f":"XIC vs XIO","b":"XIC (Examine If Closed) = TRUE when bit = 1.  XIO (Examine If Open) = TRUE when bit = 0"},
  {"f":"TON timer","b":"Timer On-Delay: accumulates while input is TRUE; DN bit sets when ACC reaches PRE"},
  {"f":"Seal-in (3-wire control)","b":"An aux contact of the run relay wired parallel to the momentary Start PB keeps the coil energized"},
  {"f":"NPN vs PNP sensor","b":"NPN = sinking (switches load to 0V / ground).  PNP = sourcing (switches load to +V)"},
  {"f":"RTD vs thermocouple","b":"RTD: resistance changes with temp (Pt100, precise, lower range). TC: voltage from dissimilar-metal junction (wide range, less precise)"},
  {"f":"Pascal's Law","b":"Pressure in an enclosed fluid transmits equally in all directions.  Force = Pressure x Area"},
  {"f":"Pneumatic cylinder force","b":"Force = Pressure x Piston Area.  Extend uses full bore area; retract loses the rod area"},
  {"f":"PID terms","b":"P reacts to present error, I eliminates steady-state offset (past), D dampens rate of change (future)"},
  {"f":"Directional valve notation","b":"x/y valve: x = ports, y = positions.  5/2 = 5 ports, 2 positions (typical double-acting cylinder)"},
  {"f":"LOTO","b":"Lockout/Tagout (OSHA 1910.147): isolate, lock, tag, and verify zero energy before servicing"},
  {"f":"Arc-flash standard","b":"NFPA 70E governs electrical safety and arc-flash PPE / boundaries in the workplace"},
  {"f":"ISO 13849 PL","b":"Performance Levels PL a (lowest) to PL e (highest) quantify safety-function reliability"},
  {"f":"E-stop categories","b":"Cat 0 = immediate removal of power. Cat 1 = controlled stop, then power removed"},
  {"f":"SCCR","b":"Short-Circuit Current Rating: max fault current a panel can safely withstand (UL 508A)"},
  {"f":"Ethernet/IP vs PROFINET","b":"Ethernet/IP = CIP over standard Ethernet (Rockwell). PROFINET = Siemens industrial Ethernet"},
  {"f":"Modbus RTU vs TCP","b":"RTU = serial (RS-485). TCP = Modbus frames over Ethernet. Simple, widely supported"},
  {"f":"MQTT QoS","b":"0 = fire-and-forget, 1 = at least once, 2 = exactly once. Sparkplug B standardizes SCADA topics"},
  {"f":"Half-split troubleshooting","b":"Test at the midpoint of a suspect path; each good/bad result halves the search space"},
  {"f":"True-RMS meter","b":"Required to accurately measure the non-sinusoidal (chopped) output of a VFD"},
  {"f": "Ladder scan cycle order", "b": "Read inputs to image table &rarr; solve rungs top-to-bottom/left-to-right &rarr; write outputs &rarr; housekeeping, then repeat (typ 1-10 ms)."},
  {"f": "Double-coil bug", "b": "Writing the same output coil on two rungs: only the LAST one solved each scan controls the output - the earlier is ignored. Avoid it."},
  {"f": "Series vs parallel contacts", "b": "Series contacts = logical AND (all must be true); parallel branches = logical OR (any true path energizes the output)."},
  {"f": "ONS / OSR / OSF (one-shots)", "b": "Edge instructions that stay true for exactly one scan: ONS/OSR on a rising edge, OSF on a falling edge. Use for count-once-per-press actions."},
  {"f": "RTO (retentive timer)", "b": "Retentive on-delay: accumulates true-time and HOLDS .ACC through rung/power loss. Only a RES instruction clears it. Used for total runtime tracking."},
  {"f": "R_TRIG / F_TRIG (ST)", "b": "Structured Text edge-detect function blocks: R_TRIG.Q pulses one scan on a rising CLK edge, F_TRIG on falling - the ST equivalent of a ladder one-shot."},
  {"f": "IEC timer in ST", "b": "A function-block instance, not a box: declare (JamTmr : TON;), call each scan JamTmr(IN:=cond, PT:=T#3s), then read JamTmr.Q (done) and JamTmr.ET (elapsed)."},
  {"f": "IN_OUT parameter", "b": "AOI/function parameter passed BY REFERENCE (no copy) - the block edits your live tag directly. Best for large UDTs; INPUT is copied in, OUTPUT copied out."},
  {"f": "Hysteresis (deadband)", "b": "Two thresholds prevent output chatter: e.g. Fan ON at &gt;=80&deg;, OFF at &lt;=70&deg;; between the two it HOLDS its last state."},
  {"f": "Safe divide (ST)", "b": "Always guard division: IF Divisor &lt;&gt; 0 THEN Result := Total / Divisor; ELSE handle; - dividing by zero faults the processor."},
  {"f": "Let-go threshold", "b": "10-20 mA of 60 Hz current through the body makes muscles clamp so you CANNOT release the conductor. ~5 mA is the safe limit (GFCI trips here); 100-300 mA causes ventricular fibrillation."},
  {"f": "Live-dead-live", "b": "LOTO verification: test your meter on a KNOWN live source, prove the circuit dead, then re-test the meter on the known source. Confirms the meter worked the whole time before you touch anything."},
  {"f": "RMS vs peak", "b": "V_rms = V_peak / 1.414 (0.707 x peak). V_peak = V_rms x 1.414. A '480 V' rating is RMS -&gt; ~679 V peak. Nameplates and meters read RMS; insulation must survive the peak."},
  {"f": "sqrt(3) rule (3-phase)", "b": "In a wye system V_line = V_phase x 1.732. So 480 V line gives 277 V to neutral; 208 V line gives 120 V to neutral. Power: P = 1.732 x V_line x I_line x PF."},
  {"f": "Wye vs Delta", "b": "Wye (star): windings share a neutral, gives two voltages (line &amp; line-to-neutral). Delta: windings form a triangle, no neutral, line voltage = phase voltage."},
  {"f": "Power factor", "b": "PF = real power (kW) / apparent power (kVA) = cos(theta), 0 to 1. Motors are inductive so current LAGS and PF &lt; 1 (0.8-0.9 typical). Low PF = utility penalty + bigger conductors; fixed with capacitor banks."},
  {"f": "Power triangle", "b": "kW (real, does work) and kVAR (reactive, builds magnetic fields) are the two legs; kVA (apparent, what the utility supplies) is the hypotenuse: kVA = sqrt(kW&sup2; + kVAR&sup2;)."},
  {"f": "AWG gotcha", "b": "Bigger AWG number = SMALLER wire. 14 AWG is small (lighting), 12/10 for receptacles/small motors; the number drops (4, 2, 1/0, 2/0) as wire gets fatter for feeders."},
  {"f": "Voltage drop rule", "b": "Keep drop under 3% on a branch circuit, 5% feeder-plus-branch. An under-volted motor draws MORE current for the same torque, overheats, and trips overloads - fix by up-sizing the wire, not the overload."},
  {"f": "Grounding vs bonding", "b": "Bonding ties metal parts together so they share one potential; grounding connects that system to earth. The equipment grounding conductor (EGC) gives fault current a low-impedance path back to trip the breaker."},
  {"f": "Transformer turns ratio", "b": "Vp/Vs = Np/Ns. Voltage and turns scale together; current scales inversely (step-down voltage = step-up current). VA rating (Vp x Ip = Vs x Is) stays constant minus losses."},
  {"f": "3-wire control", "b": "Momentary Start energizes the coil (M); an M auxiliary contact wired parallel to Start 'seals in' to hold it after you release. NC Stop breaks the seal. Loss of power drops out and it will NOT auto-restart - the safety feature vs 2-wire."},
  {"f": "Overload relay class", "b": "Trip class = seconds to trip at 600% FLA. Class 10 (10 s, most common), Class 20, Class 30 (high-inertia loads). Protects the motor from sustained over-current; the NC OL contact opens the coil circuit."},
  {"f": "PLC scan cycle", "b": "Every scan, in order: (1) read all inputs into the input image table, (2) solve the logic top-to-bottom left-to-right, (3) write the output image to the physical outputs. Then repeat. Inputs are sampled once per scan, not continuously."},
  {"f": "Sinking vs sourcing I/O", "b": "Sourcing output supplies (+) current TO the load; sinking output provides the return path to (-). PNP sensor = sourcing, pairs with a sinking input; NPN sensor = sinking, pairs with a sourcing input. Mismatch = device never reads."},
  {"f": "Automation pyramid", "b": "L0 field devices (motors/sensors) - L1 direct control (PLC/safety) - L2 supervisory (HMI/SCADA) - L3 operations (MES/historian) - L4 enterprise (ERP). Controls techs live at L0-L2."}
]

# Simulator registry (metadata; the interactive JS lives in the app)
SIMS = [
  {"id":"scale","name":"4-20 mA / Analog Scaling","icon":"&#128225;","track":"field"},
  {"id":"ohm","name":"Ohm's Law &amp; Power Wheel","icon":"&#9889;","track":"found"},
  {"id":"resistor","name":"Resistor Color Code","icon":"&#127937;","track":"found"},
  {"id":"phase3","name":"Three-Phase Power","icon":"&#128268;","track":"found"},
  {"id":"vhz","name":"VFD Motor Speed / V-Hz","icon":"&#9881;","track":"field"},
  {"id":"seal","name":"Start/Stop Seal-In Logic","icon":"&#128268;","track":"found"},
  {"id":"rel","name":"Reliability &amp; OEE","icon":"&#128202;","track":"reliab"},
  {"id":"pulley","name":"Pulley &amp; Belt Speed","icon":"&#9881;","track":"field"},
  {"id":"rnet","name":"Series / Parallel Resistance","icon":"&#128268;","track":"found"},
  {"id":"pid","name":"PID Control Loop","icon":"&#127919;","track":"systems"},
  {"id":"ladder","name":"PLC Ladder Logic (Live)","icon":"&#129520;","track":"systems"}
]
