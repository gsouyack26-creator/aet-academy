# Automation Engineering Technology (AET) — Course & Knowledge Base v3

## What's Here

| File | Description |
|------|-------------|
| **AET_Course.html** | Self-contained interactive course (19 modules, ~88KB, offline, dark theme) |
| COURSE_OUTLINE.md | Printable syllabus / module summary |
| build_course.py | Builder script (regenerate HTML after editing) |
| modules_data.py | Modules 0-5 (Foundations) |
| modules_data2.py | Modules 6-12 (Core Domains + Capstone) |
| modules_data3.py | Modules 13-18 (Advanced) |

## Course Structure (19 Modules)

### Foundations (0-5)
0. Introduction to AET
1. Electrical Fundamentals & Motor-Control Wiring
2. PLC Fundamentals
3. PLC Programming II — Timers, Counters & Data
4. Sensors & Instrumentation
5. Motors, VFDs & Drives

### Core Domains (6-12)
6. Fluid Power — Pneumatics & Hydraulics
7. HMI / SCADA Systems
8. Industrial Networks & Fieldbus
9. Robotics & Motion Control
10. Process Control & PID
11. Machine Safety & Functional Safety
12. Capstone — System Integration & Career Paths

### Advanced (13-18)
13. Advanced PLC — Structured Text, AOIs & Fault Handling
14. IIoT & Industry 4.0
15. Electrical Troubleshooting & Test Equipment
16. Preventive & Predictive Maintenance (Reliability)
17. Control Panel Design & Build
18. Career Acceleration — Portfolio, Interviews & Certifications

## Features
- **19 modules** with objectives, teaching sections, labs (free tools), quizzes (57 questions)
- **62-term searchable glossary**
- **Lab Simulators** (NEW v3) — 4 interactive tools, live results:
  - 4-20 mA / analog scaling calculator (mA & raw counts → engineering units, out-of-range fault flag)
  - Reliability & OEE calculator (MTBF / MTTR / Availability / OEE)
  - VFD motor speed / V-Hz calculator (synchronous RPM, slip, V/Hz ratio)
  - Start/Stop seal-in logic simulator (hold Start, watch the seal-in hold the coil; Stop / overload drop it)
- **Final Exam** (NEW v3) — 20 questions drawn at random from all 19 module quiz pools; 80% to pass; graded with per-question feedback; retake for a fresh random set; best result saved
- **Printable study guides** (NEW v3) — "Print Study Guide" per module + "Print All" (whole course + glossary) with a clean `@media print` layout
- **Progress tracking** (localStorage — scores, completed modules, and last exam result persist)
- **Module completion badges** + **module search**
- **Fully offline, single file** — just double-click AET_Course.html

## Sidebar quick links
- ⚡ AET Course header · module list · search
- 🎓 Final Exam · 🔬 Simulators · 🖨 Print All

## How to Edit / Rebuild
```
# Edit modules_data.py / modules_data2.py / modules_data3.py (module content)
# or build_course.py (glossary, simulators, exam, print CSS/JS)
python build_course.py   # regenerates AET_Course.html + COURSE_OUTLINE.md
```

## Related Skill (Akira)
`~/.aki/user_preference/akira/skills/automation-engineering-technology/`
- SKILL.md + knowledge/ (academic programs, competencies, 55 free resources)

*Built 2026-07-15 by Akira for ACY1 RME. v2: +6 advanced modules, glossary, progress tracking. v3: +lab simulators, final exam, printable study guides.*
