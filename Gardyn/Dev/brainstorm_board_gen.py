#!/usr/bin/env python3
# Brainstorm board: one faithful Tracker pod-card + four alternate card
# treatments of the "Check Reservoir Water Level" task card, for hands-on
# tweaking in Illustrator. Output imports as editable text frames + shapes.

import html, math

# palette
CREAM="#f0faf0"; PARCH="#dff0da"; INK="#0f1a0f"; MOSS="#0f6b22"; SAGE="#6aaa50"
TERRA="#b85c38"; GOLD="#c4962a"; MUTED="#4a6b52"; DIV="#9cc49c"; STEPINK="#2a402a"
WHITE="#ffffff"; BLUE="#5a8abf"; TOPBAR="#eaf7ea"

F = "Avenir Next, sans-serif"   # readable placeholder; swap freely in AI

W = 1760
MARGIN = 60

body=[]
def e(s): body.append(s)
def esc(t): return html.escape(t, quote=False)

def wrap(text, fs, maxw, cw=0.54):
    mc=max(6,int(maxw/(fs*cw))); ln=[]; cur=""
    for w in text.split():
        t=w if not cur else cur+" "+w
        if len(t)<=mc: cur=t
        else:
            if cur: ln.append(cur)
            cur=w
    if cur: ln.append(cur)
    return ln or [""]

def text(x,y,s,fs,fill,*,w="400",anchor="start",ital=False,ls=None,fam=F):
    a=f' text-anchor="{anchor}"' if anchor!="start" else ""
    i=' font-style="italic"' if ital else ""
    l=f' letter-spacing="{ls}"' if ls else ""
    e(f'<text x="{x:.0f}" y="{y:.0f}" font-family="{fam}" font-size="{fs}" font-weight="{w}"{i}{l} fill="{fill}"{a}>{esc(s)}</text>')

def rrect(x,y,w,h,r,fill,stroke=None,sw=0):
    s=f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    e(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{r}" fill="{fill}"{s}/>')

def caption(x,y,s):
    text(x,y,s.upper(),15,MUTED,w="600",ls="1.6")

# ---- task content (shared across variants) ----
T_TITLE="Check Reservoir Water Level"
T_DESC="Plants drink more water than nutrients — top up between feeding days"
T_STEPS=["Top up with plain water if below the minimum line",
         "Listen for the pump — should be running quietly and consistently",
         "Confirm water is trickling down through all pods from the top"]

# =================================================================
#  VARIANT A — current style (white card, left sage bar, checkbox)
# =================================================================
def variant_A(x,y,w):
    pad=26; tx=x+pad+30+16; tw=w-pad*2-30-16
    cy=y+pad+30
    # measure
    h=pad*2+30  # title
    h+=8+len(wrap(T_DESC,20,tw))*30
    h+=14+sum(len(wrap(s,19,tw-22))*28 for s in T_STEPS)
    rrect(x,y,w,h,14,WHITE,DIV,1.5)
    rrect(x,y,6,h,14,SAGE)
    rrect(x+pad,y+pad+2,28,28,6,WHITE,DIV,2)   # checkbox
    text(tx,cy,T_TITLE,24,INK,w="700")
    cy+=8+22
    for ln in wrap(T_DESC,20,tw):
        text(tx,cy,ln,20,MUTED,ital=True); cy+=30
    cy+=10
    for s in T_STEPS:
        for j,ln in enumerate(wrap(s,19,tw-22)):
            if j==0: text(tx,cy,"—",19,SAGE)
            text(tx+22,cy,ln,19,STEPINK); cy+=28
    return h

# =================================================================
#  VARIANT B — icon tile, bullet dots, no left bar
# =================================================================
def variant_B(x,y,w):
    pad=26; tile=58; tx=x+pad+tile+18; tw=w-pad*2-tile-18
    cy=y+pad+30
    h=pad*2+30+8+len(wrap(T_DESC,20,tw))*30+16+sum(len(wrap(s,19,tw-24))*28 for s in T_STEPS)
    rrect(x,y,w,h,18,WHITE,"#e3ece6",1.5)
    rrect(x+pad,y+pad,tile,tile,14,"#e7f0fa")          # droplet tile
    text(x+pad+tile/2,y+pad+tile/2+12,"💧",30,BLUE,anchor="middle")
    text(tx,cy,T_TITLE,24,INK,w="700")
    cy+=8+22
    for ln in wrap(T_DESC,20,tw):
        text(tx,cy,ln,20,MUTED,ital=True); cy+=30
    cy+=12
    for s in T_STEPS:
        for j,ln in enumerate(wrap(s,19,tw-24)):
            if j==0: e(f'<circle cx="{tx+5:.0f}" cy="{cy-6:.0f}" r="4" fill="{BLUE}"/>')
            text(tx+24,cy,ln,19,STEPINK); cy+=28
    return h

# =================================================================
#  VARIANT C — tinted header band + pill, body below
# =================================================================
def variant_C(x,y,w):
    pad=24; band=64
    tw=w-pad*2-30-16; tx=x+pad+30+16
    bh=pad*2+0
    # body height
    by=y+band+pad+24
    h_body=pad*2+len(wrap(T_DESC,20,w-pad*2))*30+14+sum(len(wrap(s,19,w-pad*2-22))*28 for s in T_STEPS)
    h=band+h_body
    rrect(x,y,w,h,14,WHITE,DIV,1.5)
    rrect(x,y,w,band,14,PARCH)
    e(f'<rect x="{x:.0f}" y="{y+band-14:.0f}" width="{w:.0f}" height="14" fill="{PARCH}"/>')
    rrect(x+pad,y+(band-26)/2,26,26,6,WHITE,DIV,2)     # checkbox
    text(x+pad+26+14,y+band/2+8,T_TITLE,23,INK,w="700")
    # pill
    pl="EVERY 2–3 DAYS"; pw=len(pl)*10+28
    rrect(x+w-pad-pw,y+(band-30)/2,pw,30,15,"#d6ebd6")
    text(x+w-pad-pw/2,y+band/2+5,pl,14,MOSS,w="600",anchor="middle",ls="1")
    cy=y+band+pad+22
    for ln in wrap(T_DESC,20,w-pad*2):
        text(x+pad,cy,ln,20,MUTED,ital=True); cy+=30
    cy+=12
    for s in T_STEPS:
        for j,ln in enumerate(wrap(s,19,w-pad*2-22)):
            if j==0: text(x+pad,cy,"—",19,SAGE)
            text(x+pad+22,cy,ln,19,STEPINK); cy+=28
    return h

# =================================================================
#  VARIANT D — minimal, numbered step circles, left rule only
# =================================================================
def variant_D(x,y,w):
    pad=20; rule=4; tx=x+pad+34+18; tw=w-pad-rule-34-18-pad
    cy=y+pad+30
    h=pad*2+34+8+len(wrap(T_DESC,21,tw))*31+16+len(T_STEPS)*40
    rrect(x,y,rule,h,2,SAGE)
    rrect(x+rule,y,w-rule,h,0,"none")  # invisible (no card bg) — just spacing anchor
    rrect(x+pad,y+pad,34,34,8,WHITE,SAGE,2.5)          # big checkbox
    text(tx,cy,T_TITLE,26,INK,w="700")
    cy+=8+24
    for ln in wrap(T_DESC,21,tw):
        text(tx,cy,ln,21,MUTED,ital=True); cy+=31
    cy+=14
    for i,s in enumerate(T_STEPS,1):
        e(f'<circle cx="{tx+13:.0f}" cy="{cy-7:.0f}" r="13" fill="{SAGE}"/>')
        text(tx+13,cy-2,str(i),15,WHITE,w="700",anchor="middle")
        for j,ln in enumerate(wrap(s,19,tw-40)):
            text(tx+38,cy,ln,19,STEPINK); cy+= (28 if j< len(wrap(s,19,tw-40))-1 else 40)
    return h

# =================================================================
#  TRACKER POD CARD (faithful)
# =================================================================
def tracker_card(x,y,w):
    topbar=52
    rows=3; rowh=66; h=topbar+rows*rowh
    # shell
    rrect(x,y,w,h,8,WHITE,DIV,1.5)
    # top bar
    rrect(x,y,w,topbar,8,TOPBAR)
    e(f'<rect x="{x:.0f}" y="{y+topbar-8:.0f}" width="{w:.0f}" height="8" fill="{TOPBAR}"/>')
    bx=x+18; by=y+topbar/2+6
    text(bx,by,"POD",15,MUTED,w="600",ls="1.4"); bx+=58
    text(bx,by,"3",20,INK,w="700"); bx+=28
    text(bx,by,"|",18,DIV); bx+=22
    text(bx,by,"Buttercrunch",20,INK,w="700"); bx+=185
    text(bx,by,"|",18,DIV); bx+=22
    text(bx,by,"2026-05-15",17,MUTED); bx+=160
    text(bx,by,"|",18,DIV); bx+=22
    pw=130; rrect(bx,y+(topbar-30)/2,pw,30,6,"#d0f0d0"); text(bx+pw/2,y+topbar/2+5,"🌱 Sprouted",16,"#2d6a2d",anchor="middle");
    # actions right
    rrect(x+w-150,y+(topbar-30)/2,86,30,5,"#eaf2fb",None,0); text(x+w-150+43,y+topbar/2+5,"✎ Edit",15,"#2a6496",anchor="middle")
    rrect(x+w-56,y+(topbar-30)/2,34,30,5,"#fde8e8",None,0); text(x+w-56+17,y+topbar/2+5,"✕",15,TERRA,anchor="middle")
    # grid 4 cols x 3 rows
    cw=w/4
    cells=[
        [("Seed → Sprout","7 days",INK),("Sprout → Harvest","28 days",INK),("Good For","21 days",INK),("Health","Healthy",MOSS)],
        [("Expected Sprout","May 22",MUTED),("1st Harvest","Jun 19",MOSS),("Est. Die-Off","Jul 10",TERRA),("Replant By","Jun 12",GOLD)],
        [("Light · Pets · pH","medium · Safe · pH 5.5–6.5",MUTED),("Qty · Thin To","3 · →1",MUTED),("Notes","Looking strong — thin next week",MUTED),("","",MUTED)],
    ]
    gy=y+topbar
    for r,row in enumerate(cells):
        for c,(lbl,val,col) in enumerate(row):
            cx=x+c*cw; cyy=gy+r*rowh
            if c<3: e(f'<rect x="{cx+cw:.0f}" y="{cyy:.0f}" width="1" height="{rowh}" fill="{DIV}"/>')
            if r<2: e(f'<rect x="{cx:.0f}" y="{cyy+rowh:.0f}" width="{cw:.0f}" height="1" fill="{DIV}"/>')
            if lbl:
                text(cx+16,cyy+24,lbl.upper(),13,MUTED,w="600",ls="1")
                # light dot for first cell row3
                vx=cx+16
                if r==2 and c==0:
                    e(f'<circle cx="{vx+4:.0f}" cy="{cyy+42:.0f}" r="5" fill="{SAGE}"/>'); vx+=14
                text(vx,cyy+46,val,17,col,w=("600" if col in (MOSS,) else "400"))
    return h

# ================= assemble =================
y=70
text(W/2,y,"BRAINSTORM BOARD · CARD TREATMENTS",26,MOSS,w="700",anchor="middle",ls="2")
y+=46
caption(MARGIN,y,"Tracker · pod card")
y+=22
y+=tracker_card(MARGIN,y,W-2*MARGIN)+70

caption(MARGIN,y,"Task card · four treatments of “Check Reservoir Water Level”")
y+=34

colw=(W-2*MARGIN-44)/2
gx=MARGIN+colw+44
labels=["A · Current","B · Icon tile + dots","C · Header band + pill","D · Minimal, numbered"]
funcs=[variant_A,variant_B,variant_C,variant_D]
# place in 2x2 grid, row heights = max of the two
i=0
while i<4:
    caption(MARGIN,y,labels[i]); caption(gx,y,labels[i+1])
    yy=y+24
    h1=funcs[i](MARGIN,yy,colw)
    h2=funcs[i+1](gx,yy,colw)
    y=yy+max(h1,h2)+56
    i+=2

H=int(math.ceil(y+30))
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
     f'<rect x="0" y="0" width="{W}" height="{H}" fill="{CREAM}"/>'+"".join(body)+'</svg>')
p="/Users/torque/Documents/GitHub/puffer3.github.io/Gardyn/Dev/brainstorm_board.svg"
open(p,"w",encoding="utf-8").write(svg)
print("wrote",p,W,"x",H)
