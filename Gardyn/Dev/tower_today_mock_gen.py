#!/usr/bin/env python3
# SVG mock of the mobile tracker — small day columns + the enlarged "today"
# column — so the enlarged-today design can be reworked by hand in Illustrator.
# Mirrors the M config from tracker_by_day_780.html (2x for comfortable editing).

import html

S=2
CELL=20*S; GAP=6*S; LABELW=64*S; ROWH=34*S; HEADH=46*S
BIG=round(CELL*1.6)
DAYS=12; TODAY=6
TASKS=['Water','Food','pH','Tank','Deadhead','Harvest','Prune','Tower','Tray','Mildew','Pests','Roots']

CREAM='#f0faf0'; ORANGE='#f0cd8a'; GREY='#d4d4d4'; GREEN='#86cc78'
INK='#0f1a0f'; MUTED='#4a6b52'; MOSS='#0f6b22'; DIV='#9cc49c'
F='Avenir Next, sans-serif'

def colX(i): return LABELW + GAP + i*(CELL+GAP)
def rowY(r): return HEADH + r*ROWH

W = int(colX(DAYS-1)+CELL+24)
H = int(rowY(len(TASKS))+24)

# today column states (o=orange incomplete, g=green done, None=blank)
TODAY_CELLS={0:'o',1:'o',2:'o',3:None,4:'o',5:'g',6:'o',7:None,8:'g',9:'o',10:'o',11:None}
COL={'o':ORANGE,'g':GREEN,'s':GREY}

def base_state(d,r):
    if d==TODAY: return None
    if (d+r)%4!=0: return None        # sparse "due" pattern
    return 's' if d>TODAY else 'o'    # upcoming grey / past incomplete orange

out=[]
def e(s): out.append(s)
def esc(t): return html.escape(t,quote=False)

e(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
e('<defs><filter id="sh" x="-60%" y="-60%" width="220%" height="220%">'
  '<feDropShadow dx="0" dy="6" stdDeviation="9" flood-color="#000" flood-opacity="0.18"/></filter></defs>')
e(f'<rect width="{W}" height="{H}" fill="{CREAM}"/>')

# ── enlarged TODAY white column (drawn first, behind) ──
cx = colX(TODAY)+CELL/2
barW = BIG+28
barTop = HEADH-44
barH = (len(TASKS)-1)*ROWH + BIG + 40 + (rowY(0)-barTop)
e(f'<rect x="{cx-barW/2:.0f}" y="{barTop:.0f}" width="{barW:.0f}" height="{barH:.0f}" rx="14" fill="#fff" filter="url(#sh)"/>')

# ── day numbers ──
for i in range(DAYS):
    day=i+1
    if i==TODAY: continue
    e(f'<text x="{colX(i)+CELL/2:.0f}" y="{HEADH-22:.0f}" font-family="{F}" font-size="{9*S}" '
      f'fill="{DIV}" text-anchor="middle">{day}</text>')
# big today date
e(f'<text x="{cx:.0f}" y="{HEADH-18:.0f}" font-family="{F}" font-size="{15*S}" font-weight="800" '
  f'fill="{MOSS}" text-anchor="middle">{TODAY+1}</text>')

# ── task labels ──
for r,t in enumerate(TASKS):
    e(f'<text x="0" y="{rowY(r)+CELL/2+5:.0f}" font-family="{F}" font-size="{12*S}" fill="{MUTED}">{esc(t)}</text>')

# ── base cells (small) ──
for r in range(len(TASKS)):
    for i in range(DAYS):
        if i==TODAY: continue
        st=base_state(i,r)
        if not st: continue
        e(f'<rect x="{colX(i):.0f}" y="{rowY(r):.0f}" width="{CELL}" height="{CELL}" rx="{5}" fill="{COL[st]}"/>')

# ── enlarged today cells (big) ──
for r in range(len(TASKS)):
    st=TODAY_CELLS.get(r)
    if not st: continue
    x=cx-BIG/2; y=rowY(r)+CELL/2-BIG/2
    e(f'<rect x="{x:.0f}" y="{y:.0f}" width="{BIG}" height="{BIG}" rx="{7}" fill="{COL[st]}"/>')

e('</svg>')
path="/Users/torque/Documents/GitHub/puffer3.github.io/Gardyn/Dev/tower_today_mock.svg"
open(path,"w",encoding="utf-8").write("\n".join(out))
print("wrote",path,W,"x",H)
