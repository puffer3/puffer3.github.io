#!/usr/bin/env python3
# Concept mocks: (1) tower-base reservoir showing the global SOW date, with the
# tank-tip "tooltip painting" states (item 4); (2) a light-theme GitHub-style
# garden-care completion heatmap. Editable text/shapes when opened in AI.

import html, math, random
random.seed(7)

CREAM="#f0faf0"; PARCH="#dff0da"; INK="#0f1a0f"; MOSS="#0f6b22"; SAGE="#6aaa50"
TERRA="#b85c38"; GOLD="#c4962a"; MUTED="#4a6b52"; DIV="#9cc49c"; WHITE="#ffffff"
WATER="#cfe9e2"; WATERLINE="#a9d8cc"
F="Avenir Next, sans-serif"

W=1500; M=60
body=[]
def e(s): body.append(s)
def esc(t): return html.escape(t, quote=False)
def text(x,y,s,fs,fill,*,w="400",anchor="start",ls=None,ital=False):
    a=f' text-anchor="{anchor}"' if anchor!="start" else ""
    l=f' letter-spacing="{ls}"' if ls else ""
    i=' font-style="italic"' if ital else ""
    e(f'<text x="{x:.0f}" y="{y:.0f}" font-family="{F}" font-size="{fs}" font-weight="{w}"{l}{i} fill="{fill}"{a}>{esc(s)}</text>')
def rrect(x,y,w,h,r,fill,stroke=None,sw=0):
    s=f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    e(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{r}" fill="{fill}"{s}/>')
def cap(x,y,s): text(x,y,s.upper(),15,MUTED,w="600",ls="1.6")

tips=[("💧","Water"),("🌿","Plant Food"),("⚗️","pH Target"),
      ("🔄","Full Drain"),("⚠️","Overfeed"),("💡","Lighting")]

def pill_row(x,y,w,hi):
    n=len(tips); gap=12; pw=(w-gap*(n-1))/n; ph=46
    for i,(ic,lab) in enumerate(tips):
        px=x+i*(pw+gap)
        on = (hi==i)
        rrect(px,y,pw,ph,10, MOSS if on else PARCH, None if on else DIV, 0 if on else 1.5)
        text(px+pw/2,y+ph/2+6,f"{ic} {lab}",16, WHITE if on else MOSS, w="700",anchor="middle")
    return ph

def reservoir(x,y,w,eyebrow,main):
    h=104
    rrect(x,y,w,h,16,WATER,WATERLINE,2)
    e(f'<rect x="{x+10:.0f}" y="{y+22:.0f}" width="{w-20:.0f}" height="2" fill="{WATERLINE}"/>')  # waterline
    text(x+w/2,y+50,eyebrow.upper(),16,MUTED,w="700",anchor="middle",ls="1.4")
    text(x+w/2,y+82,main,21,INK,w="600",anchor="middle")
    return h

# ---------- assemble ----------
y=70
text(W/2,y,"CONCEPTS · RESERVOIR SOW + CARE HEATMAP",26,MOSS,w="700",anchor="middle",ls="2")
y+=50
cap(M,y,"Tower base · SOW lives in the reservoir; tapping a tank-tip paints its note over it (item 4)")
y+=30

states=[
    ("Default — shows the global Start-of-Watering", -1, "💧 Start of Watering", "Jun 3, 2026  ·  Day 12"),
    ("“💧 Water” tapped — tip painted into the reservoir", 0, "💧 Water", "Check every 2–3 days  ·  top up plain water only between feeds"),
    ("“⚗️ pH Target” tapped", 2, "⚗️ pH Target", "Aim 5.5–6.5  ·  tap water is often 7–8  ·  use pH Down to reach 6.0"),
]
for label,hi,eb,mn in states:
    text(M,y,label,17,MUTED,w="600",ital=True); y+=20
    ph=pill_row(M,y,W-2*M,hi); y+=ph+14
    rh=reservoir(M,y,W-2*M,eb,mn); y+=rh+30

y+=14
cap(M,y,"Tasks tab · garden-care completion heatmap (GitHub style, brand greens)")
y+=34

# heatmap
LV=["#e6f1e6","#bfe3b6","#86cc78","#3a9d49","#0f6b22"]  # less -> more
cell=22; cg=6; weeks=30; rows=7
gx=M+58; gy=y+30
# month labels (approx every ~4.3 weeks)
months=["Jan","Feb","Mar","Apr","May","Jun","Jul"]
for i,mo in enumerate(months):
    text(gx + i*4.3*(cell+cg), y+18, mo, 15, MUTED, w="500")
# day labels
for r,lab in [(1,"Mon"),(3,"Wed"),(5,"Fri")]:
    text(M, gy + r*(cell+cg) + cell-6, lab, 14, MUTED)
# cells
for c in range(weeks):
    for r in range(rows):
        # demo intensity: ramps up toward "now" (right side), sparse early
        base = c/weeks
        lvl = 0
        rr = random.random()
        if rr < base*1.1: lvl = min(4, int(random.random()* (1+base*5)))
        col = LV[lvl]
        rrect(gx + c*(cell+cg), gy + r*(cell+cg), cell, cell, 5, col)
# legend
ly = gy + rows*(cell+cg) + 26
lx = gx + weeks*(cell+cg) - 5*(cell+cg) - 120
text(lx-8, ly+cell-7, "Less", 15, MUTED, anchor="end")
for i,c in enumerate(LV):
    rrect(lx + i*(cell+cg), ly, cell, cell, 5, c)
text(lx + 5*(cell+cg)+6, ly+cell-7, "More", 15, MUTED)
text(gx, ly+cell-7, "Each square = a day · greener = more care tasks completed", 15, MUTED, ital=True) if False else None
y = ly + cell + 36

H=int(math.ceil(y))
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
     f'<rect width="{W}" height="{H}" fill="{CREAM}"/>'+"".join(body)+'</svg>')
p="/Users/torque/Documents/GitHub/puffer3.github.io/Gardyn/Dev/concepts_board.svg"
open(p,"w",encoding="utf-8").write(svg)
print("wrote",p,W,"x",H)
