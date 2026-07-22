"""
AET Course Builder v2 - 19 modules + progress tracking + glossary + completion badges
Run: python build_course.py
Output: AET_Course.html (self-contained interactive course, ~70KB)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules_data import MODULES
from modules_data2 import MODULES_2
from modules_data3 import MODULES_3

ALL_MODULES = MODULES + MODULES_2 + MODULES_3

GLOSSARY = [
  {"term":"AET","def":"Automation Engineering Technology - applied discipline of industrial automation systems"},
  {"term":"PLC","def":"Programmable Logic Controller - ruggedized industrial computer for real-time control"},
  {"term":"HMI","def":"Human-Machine Interface - operator panel/screen for machine interaction"},
  {"term":"SCADA","def":"Supervisory Control And Data Acquisition - plant-wide monitoring/control system"},
  {"term":"VFD","def":"Variable Frequency Drive - controls AC motor speed by varying frequency and voltage"},
  {"term":"OPC-UA","def":"Open Platform Communications Unified Architecture - vendor-neutral industrial data exchange"},
  {"term":"IIoT","def":"Industrial Internet of Things - connecting equipment to networks for data/analytics"},
  {"term":"MQTT","def":"Message Queuing Telemetry Transport - lightweight pub/sub protocol for IoT"},
  {"term":"Ladder Logic","def":"Graphical PLC programming language resembling relay wiring diagrams"},
  {"term":"Structured Text","def":"Text-based PLC language (IEC 61131-3), similar to Pascal"},
  {"term":"AOI","def":"Add-On Instruction - reusable custom PLC logic block (Rockwell)"},
  {"term":"UDT","def":"User-Defined Type - custom data structure grouping related tags"},
  {"term":"FBD","def":"Function Block Diagram - graphical PLC language using connected blocks"},
  {"term":"SFC","def":"Sequential Function Chart - state-machine PLC language for sequences"},
  {"term":"XIC","def":"Examine If Closed - ladder instruction TRUE when bit=1"},
  {"term":"XIO","def":"Examine If Open - ladder instruction TRUE when bit=0"},
  {"term":"OTE","def":"Output Energize - ladder output ON when rung true, OFF when false"},
  {"term":"TON","def":"Timer On-Delay - accumulates while input true, DN bit sets at preset"},
  {"term":"CTU","def":"Count Up - increments on each false-to-true transition"},
  {"term":"NPN","def":"Sinking sensor/output - switches load to 0V (ground)"},
  {"term":"PNP","def":"Sourcing sensor/output - switches load to +V (supply)"},
  {"term":"4-20 mA","def":"Standard analog signal: 4mA=zero (live zero for fault detection), 20mA=full scale"},
  {"term":"RTD","def":"Resistance Temperature Detector - precise temp sensor (Pt100 common)"},
  {"term":"Thermocouple","def":"Temperature sensor using junction of dissimilar metals (J/K/T types)"},
  {"term":"Encoder","def":"Position/speed feedback device - incremental (A/B/Z) or absolute"},
  {"term":"PPR","def":"Pulses Per Revolution - encoder resolution specification"},
  {"term":"V/Hz","def":"Volts per Hertz ratio - maintained constant in VFD to preserve motor flux"},
  {"term":"IGBT","def":"Insulated-Gate Bipolar Transistor - switching device in VFD inverter section"},
  {"term":"DC Bus","def":"Internal DC voltage section of a VFD (capacitor bank, ~650V for 480V input)"},
  {"term":"FRL","def":"Filter-Regulator-Lubricator - pneumatic air preparation unit"},
  {"term":"DCV","def":"Directional Control Valve - controls air/oil flow direction (3/2, 5/2, 5/3)"},
  {"term":"Pascal's Law","def":"Pressure in enclosed fluid is transmitted equally: F = P x A"},
  {"term":"PID","def":"Proportional-Integral-Derivative controller for closed-loop process control"},
  {"term":"SP/PV/CV","def":"Setpoint / Process Variable / Control Variable (output) in a control loop"},
  {"term":"ISA-5.1","def":"Standard for P&ID instrument tag and symbol conventions"},
  {"term":"P&ID","def":"Piping and Instrumentation Diagram - process engineering drawing"},
  {"term":"LOTO","def":"Lockout/Tagout - OSHA 1910.147 procedure for controlling hazardous energy"},
  {"term":"NFPA 70E","def":"Standard for electrical safety / arc-flash protection in the workplace"},
  {"term":"NFPA 79","def":"Electrical standard for industrial machinery (panel design)"},
  {"term":"ISO 13849","def":"Safety standard defining Performance Levels (PL a-e) and Categories (B,1-4)"},
  {"term":"Performance Level","def":"ISO 13849 safety integrity measure: PL a (lowest) to PL e (highest)"},
  {"term":"E-Stop","def":"Emergency Stop - immediate machine stop (Category 0 or 1)"},
  {"term":"IEC 62443","def":"Standard series for industrial automation cybersecurity"},
  {"term":"SCCR","def":"Short-Circuit Current Rating - max fault current a panel can safely withstand"},
  {"term":"MTBF","def":"Mean Time Between Failures = Uptime / Number of failures"},
  {"term":"MTTR","def":"Mean Time To Repair = Downtime / Number of repairs"},
  {"term":"OEE","def":"Overall Equipment Effectiveness = Availability x Performance x Quality"},
  {"term":"FFT","def":"Fast Fourier Transform - converts time-domain vibration to frequency spectrum"},
  {"term":"ISA CCST","def":"Certified Control Systems Technician - industry credential (Levels I-III)"},
  {"term":"SACA","def":"Smart Automation Certification Alliance - Industry 4.0 credentials"},
  {"term":"Ethernet/IP","def":"Industrial Ethernet protocol (CIP over TCP/UDP), Allen-Bradley standard"},
  {"term":"PROFINET","def":"Industrial Ethernet protocol, Siemens standard"},
  {"term":"Modbus","def":"Simple serial/TCP industrial protocol (RTU=serial, TCP=Ethernet)"},
  {"term":"RPI","def":"Requested Packet Interval - cyclic I/O exchange rate in Ethernet/IP (ms)"},
  {"term":"DLR","def":"Device Level Ring - fault-tolerant ring topology for Ethernet/IP devices"},
  {"term":"TCP/IP","def":"Transmission Control Protocol / Internet Protocol - foundation of all Ethernet"},
  {"term":"Scan Cycle","def":"PLC execution loop: read inputs, solve logic, write outputs, housekeeping"},
  {"term":"Seal-in","def":"Auxiliary contact in parallel with Start PB to maintain motor coil circuit"},
  {"term":"Megohmmeter","def":"Tests insulation resistance at high DC voltage (500V/1000V) in megohms"},
  {"term":"True RMS","def":"Meter that accurately measures non-sinusoidal waveforms (required for VFD output)"},
  {"term":"CAT III/IV","def":"IEC safety categories for test equipment (III=distribution, IV=origin)"},
  {"term":"Sparkplug B","def":"Industrial MQTT specification standardizing topic/payload for SCADA"}
]

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>AET Course - Automation Engineering Technology (19 Modules)</title>
<style>
:root{--bg:#1a1a2e;--card:#16213e;--accent:#0f3460;--hi:#e94560;--text:#eee;--text2:#aab;--ok:#27ae60;--warn:#f39c12;--fail:#e74c3c;--r:10px}
*{box-sizing:border-box;margin:0;padding:0}body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);display:flex;height:100vh;overflow:hidden}
#sb{width:290px;min-width:290px;background:var(--card);border-right:1px solid #333;overflow-y:auto;padding:0}
#sb-head{padding:1rem;border-bottom:1px solid #333;position:sticky;top:0;background:var(--card);z-index:2}
#sb-head h1{font-size:1rem;color:var(--hi);margin-bottom:.5rem}
#search{width:100%;padding:.4rem .6rem;border-radius:5px;border:1px solid #444;background:#111;color:#eee;font-size:.82rem}
#nav{padding:.5rem 0}.ni{padding:.5rem 1rem;cursor:pointer;border-left:3px solid transparent;font-size:.82rem;transition:all .15s;display:flex;align-items:center;gap:.4rem}
.ni:hover{background:var(--accent);border-left-color:var(--hi)}.ni.active{background:var(--accent);border-left-color:var(--hi);font-weight:600}
.ni .mn{color:var(--hi);font-weight:700;min-width:1.4rem}.ni .badge{margin-left:auto;font-size:.7rem;padding:1px 5px;border-radius:8px;background:var(--ok);color:#fff}
#main{flex:1;overflow-y:auto;padding:2rem 3rem}
.mh{margin-bottom:1.5rem}.mh h2{font-size:1.7rem;color:var(--hi);margin-bottom:.2rem}.mh .sub{color:var(--text2);font-size:.85rem}
.obj{background:var(--accent);border-radius:var(--r);padding:1rem 1.3rem;margin-bottom:1.5rem}.obj h3{color:var(--warn);margin-bottom:.5rem;font-size:.95rem}.obj li{margin:.3rem 0 .3rem 1.2rem;font-size:.88rem;line-height:1.5}
.sec{margin-bottom:1.8rem}.sec h3{color:var(--hi);font-size:1.1rem;margin-bottom:.6rem;border-bottom:1px solid #333;padding-bottom:.2rem}
.sec .bd{font-size:.9rem;line-height:1.7}.sec .bd b{color:#fff}.sec .bd pre{background:#111;padding:.7rem;border-radius:6px;overflow-x:auto;font-size:.8rem;margin:.5rem 0}.sec .bd code{background:#222;padding:2px 4px;border-radius:3px;font-size:.83rem}
.lab{background:#0a2a1a;border:1px solid var(--ok);border-radius:var(--r);padding:1rem 1.3rem;margin-bottom:1.5rem}.lab h3{color:var(--ok);margin-bottom:.2rem}.lab .tool{font-size:.8rem;color:var(--text2);margin-bottom:.5rem}.lab ol{margin-left:1.2rem;font-size:.88rem;line-height:1.7}
.qz{background:#1a1020;border:1px solid #555;border-radius:var(--r);padding:1rem 1.3rem;margin-bottom:1.5rem}.qz h3{color:var(--warn);margin-bottom:.8rem}
.qb{margin-bottom:1rem;padding-bottom:.8rem;border-bottom:1px solid #333}.qb:last-child{border-bottom:none}
.qt{font-size:.9rem;font-weight:600;margin-bottom:.4rem}.qo label{display:block;padding:.25rem .5rem;margin:.15rem 0;border-radius:4px;cursor:pointer;font-size:.85rem;transition:background .15s}.qo label:hover{background:#333}.qo input{margin-right:.4rem}
.qf{margin-top:.3rem;padding:.4rem .6rem;border-radius:5px;font-size:.83rem;display:none}.qf.c{display:block;background:#1a3a1a;color:var(--ok)}.qf.w{display:block;background:#3a1a1a;color:var(--fail)}
.res{margin-bottom:1.5rem}.res h3{color:var(--text2);margin-bottom:.4rem;font-size:.95rem}.res a{display:block;color:#5dade2;font-size:.85rem;margin:.2rem 0;text-decoration:none}.res a:hover{text-decoration:underline}
.pbar{position:fixed;top:0;left:290px;right:0;height:4px;background:#111;z-index:99}.pfill{height:100%;background:var(--hi);transition:width .3s}
.next-btn{background:var(--hi);color:#fff;border:none;padding:.7rem 1.8rem;border-radius:6px;cursor:pointer;font-size:.95rem;margin:1.5rem 0}
.next-btn:hover{opacity:.85}
#glossary{display:none;padding:2rem 3rem;overflow-y:auto}
#glossary h2{color:var(--hi);margin-bottom:1rem}
#glossary .gi{padding:.4rem 0;border-bottom:1px solid #222;font-size:.88rem}
#glossary .gi b{color:var(--warn)}
.tab-bar{display:flex;gap:0;border-bottom:1px solid #444;margin-bottom:1rem;position:sticky;top:0;background:var(--bg);z-index:5;padding-top:.5rem}
.tab{padding:.5rem 1.2rem;cursor:pointer;color:var(--text2);font-size:.9rem;border-bottom:2px solid transparent}.tab.active{color:var(--hi);border-bottom-color:var(--hi)}
.score-bar{margin:1.5rem 0;padding:1rem;background:var(--accent);border-radius:var(--r);font-size:.9rem}
.score-bar b{color:var(--ok)}
@media(max-width:900px){#sb{width:240px;min-width:240px}#main,#glossary{padding:1.2rem}}
@media(max-width:600px){body{flex-direction:column}#sb{width:100%;min-width:unset;max-height:180px;border-right:none;border-bottom:1px solid #333}#main,#glossary{padding:1rem}.pbar{left:0}}
.qlink{flex:1;min-width:80px;background:var(--accent);color:var(--text);border:1px solid #345;padding:.35rem;border-radius:5px;cursor:pointer;font-size:.72rem}.qlink:hover{background:var(--hi);color:#fff}
.sim{background:#0a1a2a;border:1px solid #5dade2;border-radius:var(--r);padding:1rem 1.3rem;margin-bottom:1.5rem}
.sim h3{color:#5dade2;margin-bottom:.3rem}.sim .desc{font-size:.83rem;color:var(--text2);margin-bottom:.7rem;line-height:1.5}
.sim label{display:block;font-size:.83rem;margin:.4rem 0 .15rem;color:var(--text2)}
.sim input,.sim select{width:100%;max-width:220px;padding:.35rem .5rem;border-radius:5px;border:1px solid #444;background:#111;color:#eee;font-size:.85rem}
.sim .row{display:flex;gap:1.2rem;flex-wrap:wrap;margin-bottom:.5rem}.sim .row>div{flex:1;min-width:150px}
.sim .out{margin-top:.8rem;padding:.7rem 1rem;background:#111;border-radius:6px;font-size:.9rem;line-height:1.6;border-left:3px solid #5dade2}
.sim .out b{color:#5dade2}.sim .big{font-size:1.3rem;color:var(--ok);font-weight:700}
.sim .btn{background:#5dade2;color:#03263d;border:none;padding:.4rem 1rem;border-radius:5px;cursor:pointer;font-weight:600;font-size:.85rem;margin-top:.4rem}
.sim .lamp{display:inline-block;width:14px;height:14px;border-radius:50%;background:#333;border:1px solid #666;vertical-align:middle}.sim .lamp.on{background:var(--ok);box-shadow:0 0 6px var(--ok)}
.exam-hd{background:var(--accent);border-radius:var(--r);padding:1.2rem 1.5rem;margin-bottom:1.5rem}.exam-hd h2{color:var(--hi)}.exam-hd p{font-size:.85rem;color:var(--text2);margin-top:.4rem;line-height:1.5}
.exresult{padding:1.2rem 1.5rem;border-radius:var(--r);margin-bottom:1.5rem;font-size:1rem}.exresult.pass{background:#0a2a1a;border:1px solid var(--ok)}.exresult.failg{background:#2a0a0a;border:1px solid var(--fail)}
@media print{
  #sb,.pbar,.tab-bar,.next-btn,.qz,.qo,.sim .btn,#printbtn,.res a{display:none!important}
  body{display:block;height:auto;overflow:visible;background:#fff;color:#000}
  #main,#glossary{display:block!important;padding:0;overflow:visible}
  .obj,.sec,.lab,.sim{background:#fff!important;border:1px solid #ccc!important;color:#000;page-break-inside:avoid}
  .mh h2,.sec h3,.obj h3,.lab h3,.sim h3{color:#000!important}
  .sec .bd b,.sec .bd pre,.sec .bd code{color:#000;background:#f0f0f0}
  a{color:#000;text-decoration:none}
  .printall .mh{page-break-before:always}
}
</style>
</head>
<body>
<div id="sb">
<div id="sb-head"><h1>&#9889; AET Course <span style="font-size:.7rem;color:var(--text2)">v3 &bull; 19 modules</span></h1><input id="search" placeholder="Search modules..." oninput="filterNav(this.value)"><div style="display:flex;gap:.3rem;margin-top:.5rem;flex-wrap:wrap"><button class="qlink" onclick="showExam()">&#127891; Final Exam</button><button class="qlink" onclick="showSims()">&#128300; Simulators</button><button class="qlink" onclick="printAll()">&#128424; Print All</button></div></div>
<div id="nav"></div>
</div>
<div class="pbar"><div class="pfill" id="progress"></div></div>
<div id="main"></div>
<div id="glossary"></div>
<script>
const M=__MODULES__;
const G=__GLOSSARY__;
let cur=0,scores=JSON.parse(localStorage.getItem('aet_scores')||'{}'),completed=JSON.parse(localStorage.getItem('aet_done')||'[]');
const nav=document.getElementById('nav'),main=document.getElementById('main'),gloss=document.getElementById('glossary'),prog=document.getElementById('progress');

function save(){localStorage.setItem('aet_scores',JSON.stringify(scores));localStorage.setItem('aet_done',JSON.stringify(completed));}
function buildNav(filter){
  const f=filter?filter.toLowerCase():'';
  nav.innerHTML=M.filter(m=>!f||m.title.toLowerCase().includes(f)).map(m=>{
    const done=completed.includes(m.id);
    return `<div class="ni${m.id===cur?' active':''}" onclick="showMod(${m.id})"><span class="mn">${m.id}</span>${m.title}${done?'<span class="badge">&#10003;</span>':''}</div>`;
  }).join('');
}
function filterNav(v){buildNav(v);}
function showMod(id){
  cur=id;gloss.style.display='none';main.style.display='block';buildNav();
  const m=M.find(x=>x.id===id);if(!m)return;
  let h=`<div class="tab-bar"><div class="tab active" onclick="showMod(${id})">Lesson</div><div class="tab" onclick="showGlossary()">Glossary (${G.length})</div></div>`;
  h+=`<div class="mh"><h2>Module ${m.id}: ${m.title}</h2><div class="sub">AET Course &mdash; Automation Engineering Technology</div></div>`;
  h+=`<div class="obj"><h3>&#127919; Learning Objectives</h3><ol>${m.objectives.map(o=>`<li>${o}</li>`).join('')}</ol></div>`;
  m.sections.forEach(s=>{h+=`<div class="sec"><h3>${s.h}</h3><div class="bd">${s.body}</div></div>`;});
  h+=`<div class="lab"><h3>&#128295; Hands-On Lab: ${m.lab.title}</h3><div class="tool">Tool: ${m.lab.tool}</div><ol>${m.lab.steps.map(s=>`<li>${s}</li>`).join('')}</ol></div>`;
  h+=`<div class="qz"><h3>&#128221; Check Your Understanding</h3>`;
  m.quiz.forEach((q,qi)=>{const qid=`q${id}_${qi}`;h+=`<div class="qb"><div class="qt">${qi+1}. ${q.q}</div><div class="qo" id="${qid}">${q.options.map((o,oi)=>`<label><input type="radio" name="${qid}" value="${oi}" onchange="chk(${id},${qi},${oi})">${o}</label>`).join('')}</div><div class="qf" id="${qid}_f"></div></div>`;});
  h+=`</div>`;
  const sc=scores[id];if(sc!==undefined)h+=`<div class="score-bar">Module score: <b>${sc}/${m.quiz.length}</b> correct${sc===m.quiz.length?' &#127942; Perfect!':''}</div>`;
  h+=`<div class="res"><h3>&#128218; Free Resources</h3>${m.resources.map(r=>`<a href="${r.url}" target="_blank">${r.name}</a>`).join('')}</div>`;
  if(id<M.length-1)h+=`<button class="next-btn" onclick="showMod(${id+1})">Next Module &rarr;</button>`;
  h+=`<button class="next-btn" style="background:#333;margin-left:.5rem" onclick="markDone(${id})">&#10003; Mark Complete</button>`;
  h+=`<button class="next-btn" id="printbtn" style="background:#5dade2;color:#03263d;margin-left:.5rem" onclick="printModule()">&#128424; Print Study Guide</button>`;
  main.innerHTML=h;main.scrollTop=0;
  prog.style.width=((completed.length)/M.length*100)+'%';
}
function chk(mid,qi,sel){
  const m=M.find(x=>x.id===mid),q=m.quiz[qi],fb=document.getElementById(`q${mid}_${qi}_f`);
  if(sel===q.answer){fb.className='qf c';fb.textContent='\u2713 Correct! '+q.explain;}
  else{fb.className='qf w';fb.textContent='\u2717 Incorrect. '+q.explain;}
  // score tracking
  if(!scores[mid])scores[mid]=0;
  const allQ=document.querySelectorAll(`[id^="q${mid}_"][id$="_f"]`);
  let correct=0;allQ.forEach(f=>{if(f.classList.contains('c'))correct++;});
  scores[mid]=correct;save();
}
function markDone(id){if(!completed.includes(id)){completed.push(id);save();showMod(id);}}
function showGlossary(){
  main.style.display='none';gloss.style.display='block';
  let h=`<div class="tab-bar"><div class="tab" onclick="showMod(cur)">Lesson</div><div class="tab active">Glossary (${G.length})</div></div>`;
  h+=`<h2>&#128214; AET Glossary (${G.length} terms)</h2>`;
  h+=`<input id="gsearch" placeholder="Filter terms..." oninput="filterGloss(this.value)" style="width:100%;padding:.4rem;margin-bottom:1rem;border-radius:5px;border:1px solid #444;background:#111;color:#eee">`;
  h+=`<div id="glist">${G.map(g=>`<div class="gi"><b>${g.term}</b> &mdash; ${g.def}</div>`).join('')}</div>`;
  gloss.innerHTML=h;
}
function filterGloss(v){
  const f=v.toLowerCase();
  document.getElementById('glist').innerHTML=G.filter(g=>g.term.toLowerCase().includes(f)||g.def.toLowerCase().includes(f)).map(g=>`<div class="gi"><b>${g.term}</b> &mdash; ${g.def}</div>`).join('');
}

function v(id){const e=document.getElementById(id);return e?e.value:0;}
// ---- Print ----
function printModule(){window.print();}
function printAll(){
  document.body.classList.add('printall');
  let h='';
  M.forEach(m=>{
    h+=`<div class="mh"><h2>Module ${m.id}: ${m.title}</h2></div>`;
    h+=`<div class="obj"><h3>Learning Objectives</h3><ol>${m.objectives.map(o=>`<li>${o}</li>`).join('')}</ol></div>`;
    m.sections.forEach(sc=>{h+=`<div class="sec"><h3>${sc.h}</h3><div class="bd">${sc.body}</div></div>`;});
    h+=`<div class="lab"><h3>Lab: ${m.lab.title}</h3><div class="tool">Tool: ${m.lab.tool}</div><ol>${m.lab.steps.map(x=>`<li>${x}</li>`).join('')}</ol></div>`;
  });
  h+=`<div class="mh"><h2>Glossary (${G.length} terms)</h2></div>`+G.map(g=>`<div class="gi"><b>${g.term}</b> &mdash; ${g.def}</div>`).join('');
  gloss.style.display='none';main.style.display='block';main.innerHTML=h;main.scrollTop=0;
  setTimeout(()=>{window.print();},350);
}
// ---- Lab Simulators ----
const SIM_SCALE=`<div class="sim"><h3>&#128225; 4-20 mA / Analog Scaling Calculator</h3>
<div class="desc">Convert a raw analog signal into engineering units. Live-zero: 4 mA = 0%, 20 mA = 100%. Below 4 mA usually means a broken wire.</div>
<div class="row"><div><label>Signal type</label><select id="sc_type" onchange="scale420()"><option value="ma">4-20 mA</option><option value="cnt">Raw counts (0-32767)</option></select></div>
<div><label>Input value</label><input id="sc_in" type="number" value="12" oninput="scale420()"></div></div>
<div class="row"><div><label>EU at min (0% / 4 mA)</label><input id="sc_lo" type="number" value="0" oninput="scale420()"></div>
<div><label>EU at max (100% / 20 mA)</label><input id="sc_hi" type="number" value="150" oninput="scale420()"></div></div>
<div class="out" id="sc_out"></div></div>`;
const SIM_REL=`<div class="sim"><h3>&#128202; Reliability &amp; OEE Calculator</h3>
<div class="desc">MTBF = uptime / failures. MTTR = downtime / repairs. Availability = MTBF / (MTBF + MTTR). OEE = Availability x Performance x Quality.</div>
<div class="row"><div><label>Operating hours</label><input id="r_up" type="number" value="720" oninput="calcRel()"></div>
<div><label>Number of failures</label><input id="r_f" type="number" value="4" oninput="calcRel()"></div>
<div><label>Total downtime (hrs)</label><input id="r_dn" type="number" value="8" oninput="calcRel()"></div></div>
<div class="row"><div><label>Performance %</label><input id="r_perf" type="number" value="95" oninput="calcRel()"></div>
<div><label>Quality %</label><input id="r_q" type="number" value="99" oninput="calcRel()"></div></div>
<div class="out" id="r_out"></div></div>`;
const SIM_VHZ=`<div class="sim"><h3>&#9881; VFD Motor Speed / V-Hz Calculator</h3>
<div class="desc">Synchronous RPM = 120 x f / poles. Slip = (Ns - Nfl) / Ns. Constant V/Hz keeps motor flux steady below base speed.</div>
<div class="row"><div><label>Line frequency (Hz)</label><input id="m_f" type="number" value="60" oninput="calcVHz()"></div>
<div><label>Motor poles</label><select id="m_p" onchange="calcVHz()"><option>2</option><option selected>4</option><option>6</option><option>8</option></select></div></div>
<div class="row"><div><label>Nameplate voltage (V)</label><input id="m_v" type="number" value="460" oninput="calcVHz()"></div>
<div><label>Full-load RPM (nameplate)</label><input id="m_fl" type="number" value="1750" oninput="calcVHz()"></div></div>
<div class="out" id="m_out"></div></div>`;
const SIM_SEAL=`<div class="sim"><h3>&#128268; Start / Stop Seal-In Logic Simulator</h3>
<div class="desc">Classic 3-wire motor control. Start is momentary; the run relay's aux contact "seals in" around it. Stop (NC) or an overload trip drops the coil.</div>
<div class="row"><div><button class="btn" onmousedown="sealStart(1)" onmouseup="sealStart(0)" onmouseleave="sealStart(0)" ontouchstart="sealStart(1)" ontouchend="sealStart(0)">HOLD Start PB</button></div>
<div><button class="btn" style="background:var(--fail);color:#fff" onclick="sealStop()">Press Stop PB</button></div>
<div><button class="btn" style="background:var(--warn);color:#000" id="seal_ol" onclick="sealOL()">Trip Overload</button></div></div>
<div class="out" id="seal_out"></div></div>`;
function showSims(){
  cur=-1;gloss.style.display='none';main.style.display='block';buildNav();
  main.innerHTML=`<div class="tab-bar"><div class="tab" onclick="showMod(0)">Modules</div><div class="tab active">Lab Simulators</div></div>`+
    `<div class="mh"><h2>&#128300; Lab Simulators</h2><div class="sub">Interactive tools &mdash; change any value to see live results. Great for practice before the real floor.</div></div>`+
    SIM_SCALE+SIM_REL+SIM_VHZ+SIM_SEAL;
  main.scrollTop=0;scale420();calcRel();calcVHz();sealDraw();
}
function scale420(){
  const t=document.getElementById('sc_type').value;
  const val=parseFloat(v('sc_in'))||0,lo=parseFloat(v('sc_lo'))||0,hi=parseFloat(v('sc_hi'))||0;
  let pct=(t==='ma')?(val-4)/16*100:val/32767*100;
  const eu=lo+(pct/100)*(hi-lo);
  const mm=(t==='ma')?val:(4+val/32767*16);
  document.getElementById('sc_out').innerHTML=`Percent of span: <b>${pct.toFixed(1)}%</b><br>Engineering value: <span class="big">${eu.toFixed(2)}</span><br>Equivalent current: <b>${mm.toFixed(2)} mA</b>`+((pct<0||pct>100)?'<br><span style="color:var(--warn)">&#9888; Out of 4-20 mA range &mdash; possible sensor fault / broken wire</span>':'');
}
function calcRel(){
  const up=parseFloat(v('r_up'))||0,f=parseFloat(v('r_f'))||0,dn=parseFloat(v('r_dn'))||0,perf=(parseFloat(v('r_perf'))||0)/100,ql=(parseFloat(v('r_q'))||0)/100;
  const mtbf=f>0?up/f:up,mttr=f>0?dn/f:0,avail=(mtbf+mttr)>0?mtbf/(mtbf+mttr):1,oee=avail*perf*ql;
  document.getElementById('r_out').innerHTML=`MTBF: <b>${mtbf.toFixed(1)} h</b> &nbsp; MTTR: <b>${mttr.toFixed(2)} h</b><br>Availability: <b>${(avail*100).toFixed(2)}%</b><br>OEE: <span class="big">${(oee*100).toFixed(1)}%</span> <span style="font-size:.8rem;color:var(--text2)">(world-class &ge; 85%)</span>`;
}
function calcVHz(){
  const f=parseFloat(v('m_f'))||0,p=parseFloat(v('m_p'))||4,vt=parseFloat(v('m_v'))||0,fl=parseFloat(v('m_fl'))||0;
  const ns=p>0?120*f/p:0,slip=ns>0?(ns-fl)/ns*100:0,vhz=f>0?vt/f:0;
  document.getElementById('m_out').innerHTML=`Synchronous speed: <b>${ns.toFixed(0)} RPM</b><br>Slip: <b>${slip.toFixed(1)}%</b><br>V/Hz ratio: <span class="big">${vhz.toFixed(2)} V/Hz</span> <span style="font-size:.8rem;color:var(--text2)">(460V / 60Hz &approx; 7.67)</span>`;
}
let sealRun=false,sealOLok=true;
function sealStart(down){if(down&&sealOLok)sealRun=true;sealDraw();}
function sealStop(){sealRun=false;sealDraw();}
function sealOL(){sealOLok=!sealOLok;if(!sealOLok)sealRun=false;const b=document.getElementById('seal_ol');if(b)b.textContent=sealOLok?'Trip Overload':'Reset Overload';sealDraw();}
function sealDraw(){
  const el=document.getElementById('seal_out');if(!el)return;
  el.innerHTML=`Motor coil M: <span class="lamp ${sealRun?'on':''}"></span> <b>${sealRun?'RUNNING':'stopped'}</b><br>Seal-in aux contact: <b>${sealRun?'closed (holding)':'open'}</b> &nbsp; Overload: <b>${sealOLok?'OK':'TRIPPED'}</b><br><span style="font-size:.8rem;color:var(--text2)">Tip: hold Start to energize, then release &mdash; the seal-in keeps the motor running until Stop or an overload trip.</span>`;
}
// ---- Final Exam ----
let examQ=[],examAns={},examResult=null;
function buildExamPool(){let p=[];M.forEach(m=>{if(m.quiz)m.quiz.forEach(q=>p.push({q:q.q,options:q.options,answer:q.answer,explain:q.explain,mod:m.id}));});return p;}
function showExam(){
  cur=-2;gloss.style.display='none';main.style.display='block';buildNav();
  const last=JSON.parse(localStorage.getItem('aet_exam')||'null');
  let h=`<div class="tab-bar"><div class="tab" onclick="showMod(0)">Modules</div><div class="tab active">Final Exam</div></div>`;
  h+=`<div class="exam-hd"><h2>&#127891; Final Exam</h2><p>20 questions drawn at random from all ${M.length} modules. Passing score: <b>80% (16/20)</b>. Retake as many times as you like &mdash; you get a fresh random set each attempt.</p>`;
  if(last)h+=`<p>Last attempt: <b style="color:${last.pct>=80?'var(--ok)':'var(--fail)'}">${last.score}/${last.total} (${last.pct}%)</b> &mdash; ${last.pct>=80?'PASS':'not passed yet'}</p>`;
  h+=`<button class="next-btn" style="margin-top:.8rem" onclick="startExam()">Start / Retake Exam &rarr;</button></div>`;
  main.innerHTML=h;main.scrollTop=0;
}
function startExam(){
  const pool=buildExamPool();
  for(let i=pool.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));const t=pool[i];pool[i]=pool[j];pool[j]=t;}
  examQ=pool.slice(0,Math.min(20,pool.length));examAns={};examResult=null;renderExam(false);
}
function examPick(qi,oi){examAns[qi]=oi;}
function renderExam(graded){
  let h=`<div class="tab-bar"><div class="tab" onclick="showMod(0)">Modules</div><div class="tab active">Final Exam</div></div>`;
  if(graded&&examResult){const pass=examResult.pct>=80;h+=`<div class="exresult ${pass?'pass':'failg'}"><b style="font-size:1.3rem;color:${pass?'var(--ok)':'var(--fail)'}">${pass?'\u2705 PASS':'\u274c Keep studying'}</b> &mdash; you scored <b>${examResult.score}/${examResult.total} (${examResult.pct}%)</b>. ${pass?'Nice work &mdash; solid AET fundamentals!':'Passing is 80%. Review the questions marked incorrect below and retake.'}</div>`;}
  h+=`<div class="mh"><h2>&#127891; Final Exam &mdash; ${examQ.length} questions</h2></div>`;
  examQ.forEach((q,qi)=>{
    const qid='ex'+qi;
    h+=`<div class="qb"><div class="qt">${qi+1}. ${q.q} <span style="font-size:.72rem;color:var(--text2)">[M${q.mod}]</span></div><div class="qo">`;
    q.options.forEach((o,oi)=>{
      let extra='';
      if(graded){if(oi===q.answer)extra=' style="color:var(--ok);font-weight:600"';else if(examAns[qi]===oi)extra=' style="color:var(--fail)"';}
      h+=`<label${extra}><input type="radio" name="${qid}" value="${oi}" ${examAns[qi]===oi?'checked':''} ${graded?'disabled':''} onchange="examPick(${qi},${oi})">${o}</label>`;
    });
    h+=`</div>`;
    if(graded){const ok=examAns[qi]===q.answer;h+=`<div class="qf ${ok?'c':'w'}" style="display:block">${ok?'\u2713 Correct':(examAns[qi]===undefined?'\u2717 No answer':'\u2717 Incorrect')}. ${q.explain}</div>`;}
    h+=`</div>`;
  });
  if(!graded)h+=`<button class="next-btn" onclick="gradeExam()">Submit Exam</button>`;
  else h+=`<button class="next-btn" onclick="startExam()">Retake (new questions) &rarr;</button> <button class="next-btn" style="background:#333;margin-left:.5rem" onclick="showExam()">Exam Home</button>`;
  main.innerHTML=h;main.scrollTop=0;
}
function gradeExam(){
  let score=0;examQ.forEach((q,qi)=>{if(examAns[qi]===q.answer)score++;});
  const total=examQ.length,pct=Math.round(score/total*100);
  examResult={score,total,pct};
  localStorage.setItem('aet_exam',JSON.stringify({score,total,pct,ts:Date.now()}));
  renderExam(true);
}
buildNav();showMod(0);
</script>
</body>
</html>'''

def build():
    d = os.path.dirname(os.path.abspath(__file__))
    mj = json.dumps(ALL_MODULES, ensure_ascii=False)
    gj = json.dumps(GLOSSARY, ensure_ascii=False)
    html = HTML.replace('__MODULES__', mj).replace('__GLOSSARY__', gj)
    p = os.path.join(d, 'AET_Course.html')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Built: {p} ({os.path.getsize(p):,} bytes, {len(ALL_MODULES)} modules, {len(GLOSSARY)} glossary terms)")

    # Outline
    op = os.path.join(d, 'COURSE_OUTLINE.md')
    with open(op, 'w', encoding='utf-8') as f:
        f.write("# AET Course - Automation Engineering Technology\n\n")
        f.write(f"**{len(ALL_MODULES)} Modules | Self-paced | Interactive HTML | Free tools | Progress saved locally**\n\n")
        f.write("**Audience:** Industrial maintenance technicians, RME techs, aspiring automation engineers\n")
        f.write("**Prerequisites:** High-school algebra, basic tool familiarity\n\n")
        f.write("## Modules\n\n")
        for m in ALL_MODULES:
            f.write(f"### Module {m['id']}: {m['title']}\n")
            for o in m['objectives']:
                f.write(f"- {o}\n")
            f.write(f"- **Lab:** {m['lab']['title']} ({m['lab']['tool']})\n")
            f.write(f"- **Quiz:** {len(m['quiz'])} questions\n\n")
        f.write("---\n*Open AET_Course.html for the full interactive experience.*\n")
    print(f"Built: {op} ({os.path.getsize(op):,} bytes)")

if __name__ == '__main__':
    build()
