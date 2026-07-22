# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import os

OUT = "ship/AET_Academy/Quick_Start.pdf"
NAVY = HexColor("#0b1220")
BLUE = HexColor("#0e7fb8")
ACC  = HexColor("#38bdf8")
AMBER= HexColor("#c77800")
GREY = HexColor("#475569")
DARK = HexColor("#1e293b")
LINE = HexColor("#cbd5e1")

c = canvas.Canvas(OUT, pagesize=letter)
W, H = letter
M = 0.7 * inch
y = H - M

# ---- header band ----
c.setFillColor(NAVY)
c.rect(0, H - 1.15*inch, W, 1.15*inch, fill=1, stroke=0)
c.setFillColor(ACC)
c.setFont("Helvetica-Bold", 24)
c.drawString(M, H - 0.62*inch, "AET Academy")
c.setFillColor(HexColor("#e2e8f0"))
c.setFont("Helvetica", 11)
c.drawString(M, H - 0.88*inch, "Automation Engineering Technology  |  Offline Training  |  Quick Start")
c.setFillColor(ACC)
c.setFont("Helvetica-Bold", 22)
c.drawRightString(W - M, H - 0.66*inch, "v13.48")

y = H - 1.55*inch

def h(txt, color=BLUE):
    global y
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M, y, txt)
    y -= 0.05*inch
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.line(M, y, W - M, y)
    y -= 0.22*inch

def body(txt, indent=0, gap=0.205, bold_lead=None):
    global y
    x = M + indent
    if bold_lead:
        c.setFillColor(DARK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x, y, bold_lead)
        w = c.stringWidth(bold_lead, "Helvetica-Bold", 10)
        c.setFillColor(GREY)
        c.setFont("Helvetica", 10)
        c.drawString(x + w, y, txt)
    else:
        c.setFillColor(GREY)
        c.setFont("Helvetica", 10)
        c.drawString(x, y, txt)
    y -= gap*inch

def step(n, title, txt):
    global y
    r = 0.11*inch
    cx = M + r
    cy = y + 0.035*inch
    c.setFillColor(BLUE)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(cx, cy - 0.045*inch, str(n))
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(M + 0.34*inch, y, title)
    y -= 0.18*inch
    c.setFillColor(GREY)
    c.setFont("Helvetica", 10)
    c.drawString(M + 0.34*inch, y, txt)
    y -= 0.30*inch

# ---- What you have ----
h("What you have")
body("Two self-contained apps that run in any modern browser \u2014 no internet, no install.")
body("The full learning platform: 19 modules, quizzes, flashcards, lab sims,", indent=0.15*inch, bold_lead="AET_Academy.html  ")
body("5 learning tracks, a final exam + printable certificate, and multi-user accounts.", indent=1.72*inch)
body("Interactive electrical-panel & circuit trainer \u2014", indent=0.15*inch, bold_lead="ElectronWrangler_dist.html  ")
body("meter live panels, trip breakers, and trace faults on real ACY1 schematics.", indent=2.34*inch)
y -= 0.08*inch

# ---- Getting started ----
h("Getting started")
step(1, "Keep all the files in ONE folder.",
     "The two apps link to each other, so they must stay side by side.")
step(2, "Double-click  index.html  (or AET_Academy.html).",
     "It opens in your default browser. Chrome, Edge, and Firefox all work.")
step(3, "Create your account on the sign-in screen and start learning.",
     "Pick a name and role. Your progress saves automatically in the browser.")

# ---- The two apps work together ----
h("The two apps work together", AMBER)
body("Many modules include a hands-on link into the panel trainer:")
body("opens the module\u2019s real ACY1 panel so you can explore it live.", indent=0.15*inch, bold_lead="Open live panel  ->  ")
body("opens that panel pre-broken \u2014 read the symptom and trace the fault.", indent=0.15*inch, bold_lead="Try a fault challenge  ->  ")
body("in the trainer returns you to the module you came from.", indent=0.15*inch, bold_lead="Back to AET Academy  ->  ")
y -= 0.08*inch

# ---- Good to know ----
h("Good to know")
body("saved in the browser (localStorage), separately for each account.", indent=0.15*inch, bold_lead="Progress is  ")
body("create accounts on the sign-in screen; a Lead can see the Team Roster.", indent=0.15*inch, bold_lead="Multi-user:  ")
body("Profile -> Reset, or clear the browser\u2019s data for this file.", indent=0.15*inch, bold_lead="To reset:  ")
body("everything runs from your local drive; no data ever leaves the machine.", indent=0.15*inch, bold_lead="Fully offline:  ")

# ---- footer ----
c.setStrokeColor(LINE)
c.setLineWidth(0.7)
c.line(M, M + 0.05*inch, W - M, M + 0.05*inch)
c.setFillColor(GREY)
c.setFont("Helvetica-Oblique", 8.5)
c.drawString(M, M - 0.12*inch, "AET Academy v13.48  \u2014  ACY1 RME training bundle.  Print this page and keep it with your workstation.")
c.drawRightString(W - M, M - 0.12*inch, "Double-click index.html to begin")

c.showPage()
c.save()
print("wrote", OUT, os.path.getsize(OUT), "bytes")
