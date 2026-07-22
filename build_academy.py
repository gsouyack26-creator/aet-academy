# -*- coding: utf-8 -*-
"""AET Academy builder - assembles the full learning-platform SPA into AET_Academy.html.
Run: python build_academy.py"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules_data import MODULES
from modules_data2 import MODULES_2
from modules_data3 import MODULES_3
from ladder_labs_data import LADDER_LABS
from build_course import GLOSSARY
try:
    from glossary2_data import GLOSSARY_EXTRA
    _seen = set(g['term'].lower() for g in GLOSSARY)
    GLOSSARY = GLOSSARY + [g for g in GLOSSARY_EXTRA if g['term'].lower() not in _seen]
except Exception:
    pass
import academy_data as A
try:
    from reference_data import REFERENCE, REF_CATS
except Exception:
    REFERENCE, REF_CATS = [], []

D = os.path.dirname(os.path.abspath(__file__))
MODS = MODULES + MODULES_2 + MODULES_3
try:
    from applications_data import APPLICATIONS
except Exception:
    APPLICATIONS = {}
for _m in MODS:
    _m['apps'] = APPLICATIONS.get(_m['id'], [])

try:
    from labs2_data import LABS2
except Exception:
    LABS2 = {}
try:
    from quiz2_data import QUIZ2
except Exception:
    QUIZ2 = {}
for _m in MODS:
    _q2 = QUIZ2.get(_m['id'])
    if _q2:
        _m['quiz'] = _m['quiz'] + _q2
try:
    from quiz3_data import QUIZ3
except Exception:
    QUIZ3 = {}
for _m in MODS:
    _q3 = QUIZ3.get(_m['id'])
    if _q3:
        _m['quiz'] = _m['quiz'] + _q3
try:
    from quiz4_data import QUIZ4
except Exception:
    QUIZ4 = {}
for _m in MODS:
    _q4 = QUIZ4.get(_m['id'])
    if _q4:
        _m['quiz'] = _m['quiz'] + _q4
try:
    from quiz5_data import QUIZ5
except Exception:
    QUIZ5 = {}
for _m in MODS:
    _q5 = QUIZ5.get(_m['id'])
    if _q5:
        _m['quiz'] = _m['quiz'] + _q5
for _m in MODS:
    _l2 = LABS2.get(_m['id'])
    if _l2:
        _m['lab2'] = _l2

try:
    from lessons_data import DEEP
except Exception:
    DEEP = {}
try:
    from lessons_data import TAKEAWAYS
except Exception:
    TAKEAWAYS = {}
for _m in MODS:
    _tk = TAKEAWAYS.get(_m['id'])
    if _tk:
        _m['takeaways'] = _tk
for _m in MODS:
    _exp = DEEP.get(_m['id'], {})
    for _s in _m.get('sections', []):
        _h = _s.get('h', '')
        for _key, _extra in _exp.items():
            if _key in _h:
                _s['body'] = _s['body'] + _extra
                break

def rd(name):
    with open(os.path.join(D, name), encoding='utf-8') as f:
        return f.read()

CSS = rd('aet_css.txt')
_JSFILES=['aet_qr.txt','aet_js1.txt','aet_js2.txt','aet_js3.txt','aet_js4.txt','aet_auth.txt','aet_js5.txt']
JS = "\n".join(rd(n) for n in _JSFILES)

DATA = ("const MODS=%s;\nconst GLOSS=%s;\nconst TRACKS=%s;\nconst RANKS=%s;\nconst XP=%s;\nconst ACH=%s;\nconst FLASH=%s;\nconst SIMS=%s;\n" % (
    json.dumps(MODS, ensure_ascii=False), json.dumps(GLOSSARY, ensure_ascii=False),
    json.dumps(A.TRACKS, ensure_ascii=False), json.dumps(A.RANKS, ensure_ascii=False),
    json.dumps(A.XP, ensure_ascii=False), json.dumps(A.ACHIEVEMENTS, ensure_ascii=False),
    json.dumps(A.FLASHCARDS, ensure_ascii=False), json.dumps(A.SIMS, ensure_ascii=False)))
DATA += "const REF=%s;\nconst REFCATS=%s;\n" % (json.dumps(REFERENCE, ensure_ascii=False), json.dumps(REF_CATS, ensure_ascii=False))
PANELLINK_MAP={
 1:{'panel':'Residential \u2014 Lighting Load Center + 3-Way Circuit (120V)','label':'120V residential load center \u2014 trace a 3-way lighting circuit','challenge':{'states':'br1~tripped','prompt':'The hall light is dead but the receptacles still work. One breaker tripped \u2014 find it, then reset it and confirm the light comes back.'}},
 2:{'panel':'CP83 Beckhoff I/O Rack + Interposing Relays (M-16-00264 CP83 sh83169-83192)','label':'PLC I/O rack \u2014 Profibus coupler, input cards & interposing relays','challenge':{'states':'cb~tripped','prompt':'The entire I/O rack went dark \u2014 coupler, input cards, and every interposing-relay lamp are out. Trace it back to the one protective device that feeds rack power.'}},
 4:{'panel':'LS4000 Clock Pulse Unit \u2014 9 Photoeyes to PLC (M-16-00264 CLKPULSE sh140)','label':'9 photoeyes feeding a PLC \u2014 see real sensor wiring'},
 5:{'panel':'LS4000 LSM 480VAC VFD Drive Panel (M-16-00264 LSM480 sh061/067)','label':'480VAC VFD motor drive panel \u2014 enable, run & trip a drive','challenge':{'states':'sel~open','prompt':'The VFD panel has full 480V power but the linear motor will not run. Walk the enable circuit and find why the drive is not enabled.'}},
 8:{'panel':'LS4000 Profibus Networks \u2014 repeater power + topology (M-16-00264 PROFIBUS sh02-07)','label':'Profibus network \u2014 repeaters & segment topology'},
 11:{'panel':'LS4000 E-Stop Junction Box \u2014 dual-channel loop (M-16-00264 ESTOPJB sh121)','label':'Dual-channel E-stop safety loop','challenge':{'states':'pb1~open','prompt':'The line will not reset \u2014 the safety relay and the PLC ESTOP-OK input are both dropped out. Someone left an E-stop pressed. Walk the dual-channel loop and find it.'}},
 13:{'panel':'CP83 PLC Panel \u2014 24VDC Distribution + E-Stop Slave (M-16-00264 CP83 sh83080/83130)','label':'PLC panel \u2014 24VDC I/O distribution + E-stop slave'},
 15:{'panel':'DCP Induction Power Distribution \u2014 15x 30A Feeders (M-16-00264 DCP_PWR sh5-8)','label':'15-feeder power distribution \u2014 practice fault isolation','challenge':{'states':'cbr7~tripped','prompt':'One induction belt is down while the other 14 keep running. Isolate the single tripped feeder breaker \u2014 do not shut anything else off.'}},
 16:{'panel':'Conveyor Motor Thermal Protection \u2014 480VAC (Klixon/PTC)','label':'Motor thermal protection \u2014 Klixon/PTC overtemp trip'},
 17:{'panel':'CP82 Main Power Distribution (M-16-00264 p.82060-61)','label':'Main power distribution panel','challenge':{'states':'cbK~tripped','prompt':'The 120V control bus is dead \u2014 but the LSM, conductor-rail, and induction drives all still have voltage. Find the tripped breaker feeding control power.'}},
 3:{'panel':'Standard Induction I/O \u2014 E-Stop Safety Loop (M-16-00264 INDIO sh063/130)','label':'Real discrete I/O \u2014 the field inputs & outputs your ladder logic reads and drives','challenge':{'states':'e_rpc~open','prompt':'The conveyor will not reset. The dual-channel safety relay is dropped out and the PLC I0 SAFE input is gone \u2014 but the SYNC photoeye input is still healthy. One safety device in the loop is open. Walk the E-stop / pullcord safety loop and find which one.'}},
 9:{'panel':'OSL/ARSAW USS Tote Destacker MCP (480V Servo + 24VDC Safety)','label':'Servo motion + safety \u2014 a real servo-driven robotic destacker panel','challenge':{'states':'estp~open','prompt':'The tote destacker servo will not move and the CR215 safety relay is dropped out \u2014 yet control power, the A400 PLC, and the panel lights are all still on. The Kinetix servo drive is disabled. Walk the safety circuit and find what is holding the drive-enable open.'}},
 12:{'panel':'ACY1 13XP33 4000-4003 \u2014 Remote Shipping Panel (CC566-## 460VAC/Safety)','label':'Full integrated panel \u2014 460VAC power, a VFD lane & the safety loop in one system','challenge':{'states':'estop5244~open','prompt':'The shipping-lane conveyor will not run. 460VAC is present and DISC5001 is closed, but contactor CR5217 is dropped out, VFD5022 has no power, and the SR5212 safety relay is de-energized. Trace the safety chain and find why the contactor will not pull in.'}},
}
DATA += "const PANELLINK=%s;\n" % json.dumps(PANELLINK_MAP, ensure_ascii=False)
LADDERLINK_MAP={
 1:{'progs':['seal','latch','mcr'],'challenge':True,'fault':'fault'},
 2:{'progs':['seal'],'sandbox':True,'challenge':True,'fault':'fault'},
 3:{'progs':['delay','count','lock','data','seq','shift'],'challenge':True,'fault':'fault4'},
 4:{'progs':['scale'],'challenge':True,'fault':'fault8'},
 5:{'progs':['seal','tof'],'challenge':True,'fault':'fault2'},
 9:{'progs':['mcr'],'challenge':True,'fault':'fault13'},
 10:{'progs':['pid'],'challenge':True,'fault':'fault11'},
 11:{'progs':['lock','seq'],'challenge':True,'fault':'fault9'},
 12:{'progs':['firstout'],'challenge':True,'fault':'fault12'},
 13:{'progs':['latch','tof','firstout'],'challenge':True,'fault':'fault6'},
 15:{'progs':['seal','lock','data'],'challenge':True,'fault':'fault7'},
 16:{'progs':['shift'],'challenge':True,'fault':'fault10'},
 17:{'progs':['lock'],'challenge':True,'fault':'fault3'},
}
DATA += "const LADDERLINK=%s;\n" % json.dumps(LADDERLINK_MAP, ensure_ascii=False)
DATA += "const LADDERLABS=%s;\n" % json.dumps(LADDER_LABS, ensure_ascii=False)

VIEWS = "".join('<div class="view" id="v-%s"></div>' % v for v in
    ['dash','learn','module','sims','flash','arcade','review','exam','cert','glossary','resources','achieve','profile','roster','reference','search','notes','plan','leaderboard','ladderlab'])

SKELETON = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>AET Academy - Automation Engineering Technology</title>
<style>__CSS__</style>
</head>
<body>
<div id="gate" style="display:none"></div>
<div id="sb">
  <div id="brand"><h1>&#9889; AET Academy</h1><div class="v">Automation Engineering Technology &bull; v13.47</div></div>
  <div id="usercard" onclick="go('#profile')">
    <div class="nm"><span id="u-name">Set your name</span></div>
    <div class="rk" id="u-rank">Lv 1</div>
    <div class="xpbar"><div class="xpfill" id="xpfill"></div></div>
    <div class="xptxt"><span id="u-xp">0 XP</span><span id="u-next"></span></div>
  </div>
  <div id="navmenu"></div>
  <div id="sbfoot"><div id="sbtools"><button class="mini" id="themebtn" onclick="toggleTheme()" title="Theme">&#9728;&#65039;</button><button class="mini" id="fontbtn" onclick="cycleFont()" title="Text size">A</button><button class="mini" id="contrastbtn" onclick="toggleContrast()" title="High contrast">&#9681;</button><button class="mini" onclick="palOpen()" title="Command palette (Ctrl+K)">&#128269; Search</button><button class="mini" onclick="showShortcuts()" title="Keyboard shortcuts (?)">&#9000;&#65039;</button></div></div>
</div>
<div id="main">
  <div id="topbar"><span class="crumb" id="crumb">AET Academy</span><span class="streak" id="streaktop"></span><button id="searchbtn" onclick="palOpen()">&#128269; Search &middot; Ctrl+K</button></div>
  __VIEWS__
</div>
<div id="palette" onclick="if(event.target===this)palClose()"><div class="palbox"><input id="palinput" placeholder="Jump to a module, view, or simulator..." oninput="palFilter(this.value)"><div id="palresults"></div></div></div><div id="shortcuts" onclick="if(event.target===this)hideShortcuts()"><div class="palbox" style="max-width:460px"><div style="font-weight:700;font-size:1rem;margin-bottom:.6rem">&#9000;&#65039; Keyboard shortcuts</div><div id="scbody"></div><div class="btnrow" style="margin-top:.8rem"><button class="btn sec" onclick="hideShortcuts()">Close (Esc)</button></div></div></div>
<div id="qrmodal" onclick="if(event.target===this)hideQR()"><div class="palbox" style="max-width:320px"><div id="qrbody"></div><div class="btnrow" style="margin-top:.9rem;justify-content:center"><button class="btn sec" onclick="hideQR()">Close (Esc)</button></div></div></div>
<div id="toast"></div>
<script>
__DATA__
__JS__
</script>
</body>
</html>"""

def build():
    html = (SKELETON.replace('__CSS__', CSS).replace('__VIEWS__', VIEWS)
                    .replace('__DATA__', DATA).replace('__JS__', JS))
    p = os.path.join(D, 'AET_Academy.html')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Built: %s (%s bytes)" % (p, format(os.path.getsize(p), ",")))
    print("  modules=%d glossary=%d tracks=%d achievements=%d flashcards(+gloss)=%d sims=%d ladderlabs=%d" % (
        len(MODS), len(GLOSSARY), len(A.TRACKS), len(A.ACHIEVEMENTS), len(A.FLASHCARDS)+len(GLOSSARY), len(A.SIMS), len(LADDER_LABS)))

if __name__ == '__main__':
    build()
