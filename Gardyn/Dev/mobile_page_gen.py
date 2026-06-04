#!/usr/bin/env python3
# Editable SVG of the MOBILE tracker page — using the REAL state computed exactly
# like tracker_by_day_780.html (SOW 2026-04-22, per-task OFFSET/cadence, the live
# day-window, true orange/grey/blank states, today where it actually falls).

import html, re, datetime

CREAM='#f0faf0'; INK='#0f1a0f'; MOSS='#0f6b22'; MUTED='#4a6b52'; DIV='#9cc49c'
ORANGE='#f0cd8a'; GREY='#d4d4d4'; GREEN='#86cc78'; NAVACT='#e2efe4'
TEAL='#78b39c'; TEALBD='#54ac9b'
F='Avenir Next, sans-serif'

# ── geometry (mirrors M config, mobile 1x) ──
CELL=20; GAP=6; LABELW=64; ROWH=34; HEADH=46; BIG=round(CELL*1.6)
PAD=20
WIN_DAYS=12                     # ~ what fits a phone column
TODAY=datetime.date.today()
SOW=TODAY-datetime.timedelta(days=42)               # live default: 42 days before today
YEAR,MONTH,TODAY_D=TODAY.year,TODAY.month,TODAY.day
_nm=datetime.date(YEAR+(MONTH==12),(MONTH%12)+1,1)
N=(_nm-datetime.date(YEAR,MONTH,1)).days            # days in the current month
WIN_START=max(1, min(TODAY_D-WIN_DAYS//2, N-WIN_DAYS+1))
TODAY_COL=TODAY_D-WIN_START
MONTHS=['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER']

W=LABELW+GAP+WIN_DAYS*(CELL+GAP)+PAD*2
def colX(i): return PAD+LABELW+GAP+i*(CELL+GAP)
def rowY(r,y0): return y0+r*ROWH

# ── task data + real cadence ──
TASKS=[
 ('water','Water',3,0),('food','Food',7,0),('ph','pH',7,1),('tank','Tank',21,4),
 ('deadhead','Deadhead',7,2),('harvest','Harvest',7,5),('prune','Prune',7,3),
 ('tower','Tower',30,10),('tray','Tray',3,1),('mildew','Mildew',14,6),
 ('pests','Pests',7,4),('roots','Roots',21,11)]
def d0(d): return (d-SOW).days
def due(every,off,d): return d0(d)>=off and (d0(d)-off)%every==0
def state(every,off,day):
    d=datetime.date(YEAR,MONTH,day)
    if not due(every,off,d): return None
    if d==TODAY: return 'T'           # today (enlarged, orange)
    return ORANGE if d<=TODAY else GREY

# cards = today's due tasks
CARDS=[
 ('Check Reservoir Water Level','EVERY 3 DAYS',
  'Plants drink more water than nutrients — top up between feeding days',
  ['Top up with plain water if below the minimum line','Check the Gardyn app for water level','Confirm water trickles down through all pods']),
 ('Add Plant Food','WEEKLY',
  'Leafy greens need a lighter, nitrogen-forward feed than fruiting plants',
  ['Weeks 1–2 after transplant: plain water only','Week 3 half dose · Week 4+ full dose weekly','Target EC 1.0–1.6 · pH 5.5–6.5'])]

with open('/Users/torque/Documents/GitHub/puffer3.github.io/Gardyn/Dev/MenuLogoMoody.svg',encoding='utf-8') as f:
    _l=re.sub(r'<\?xml.*?\?>','',f.read(),flags=re.S)
LOGO=re.search(r'<svg[^>]*>(.*)</svg>',_l,flags=re.S).group(1)

out=[]
def e(s): out.append(s)
def esc(t): return html.escape(t,quote=False)
def txt(x,y,s,fs,fill,*,w='400',a='start',ital=False,ls=None):
    A=f' text-anchor="{a}"' if a!='start' else ''; I=' font-style="italic"' if ital else ''
    L=f' letter-spacing="{ls}"' if ls else ''
    e(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{F}" font-size="{fs}" font-weight="{w}"{I}{L} fill="{fill}"{A}>{esc(s)}</text>')
def rr(x,y,w,h,r,fill,stroke=None,sw=0):
    S=f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    e(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}"{S}/>')
def wrap(t,maxw,fs,cw=0.55):
    mc=max(6,int(maxw/(fs*cw))); ln=[]; cur=''
    for w in t.split():
        x=w if not cur else cur+' '+w
        if len(x)<=mc: cur=x
        else: ln.append(cur); cur=w
    if cur: ln.append(cur)
    return ln or ['']

y=24
# ── logo ──
lw=148; lh=lw*163.67/550.70
e(f'<svg x="{(W-lw)/2:.0f}" y="{y:.0f}" width="{lw}" height="{lh:.1f}" viewBox="0 0 550.70 163.67">{LOGO}</svg>')
y+=lh+14
# ── nav ──
navH=34; tabs=[('TOWER',0),('TRACKER',0),('TASKS',1),('INFO',0)]; cw=(W-2*PAD)/4
e(f'<rect x="{PAD+2*cw:.1f}" y="{y:.0f}" width="{cw:.1f}" height="{navH}" fill="{NAVACT}"/>')
e(f'<rect x="{PAD}" y="{y+navH-2:.0f}" width="{W-2*PAD}" height="2" fill="{DIV}"/>')
for i,(lab,act) in enumerate(tabs):
    txt(PAD+cw*(i+0.5),y+navH/2+4,lab,9,MOSS if act else MUTED,w='700' if act else '400',a='middle',ls='1')
    if act: e(f'<rect x="{PAD+i*cw:.1f}" y="{y+navH-3:.0f}" width="{cw:.1f}" height="3" fill="{MOSS}"/>')
y+=navH+16
# ── sub ──
for ln in ['White column = today · dull orange = incomplete · grey = upcoming · green = done.',
           'Click today’s orange tasks to complete — they turn green.']:
    txt(PAD,y,ln,9.5,MUTED,ital=True); y+=14
y+=12
# ── month bar ──
e(f'<circle cx="{W/2-72:.0f}" cy="{y:.0f}" r="11" fill="none" stroke="{MUTED}" stroke-width="1.2"/>')
e(f'<polyline points="{W/2-69},{y-4} {W/2-73},{y} {W/2-69},{y+4}" fill="none" stroke="{MUTED}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>')
e(f'<circle cx="{W/2+72:.0f}" cy="{y:.0f}" r="11" fill="none" stroke="{MUTED}" stroke-width="1.2"/>')
e(f'<polyline points="{W/2+69},{y-4} {W/2+73},{y} {W/2+69},{y+4}" fill="none" stroke="{MUTED}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>')
txt(W/2,y+5,MONTHS[MONTH-1]+' '+str(YEAR),14,MUTED,w='600',a='middle',ls='1.4')
y+=30

# ── grid ──
g0=y+22
cx=colX(TODAY_COL)+CELL/2; barW=BIG+14; barTop=g0-22
barH=(len(TASKS)-1)*ROWH+BIG+22+(g0-barTop)
e(f'<rect x="{cx-barW/2:.1f}" y="{barTop:.1f}" width="{barW:.1f}" height="{barH:.1f}" rx="9" fill="#fff" style="filter:drop-shadow(0 5px 12px rgba(0,0,0,0.18))"/>')
# day numbers
for i in range(WIN_DAYS):
    if i==TODAY_COL: continue
    txt(colX(i)+CELL/2,g0-11,str(WIN_START+i),9,DIV,a='middle')
txt(cx,g0-9,str(TODAY_D),15,MOSS,w='800',a='middle')
# labels + base cells
for r,(tid,lab,every,off) in enumerate(TASKS):
    txt(PAD,rowY(r,g0)+CELL/2+4,lab,12,MUTED)
    for i in range(WIN_DAYS):
        if i==TODAY_COL: continue
        st=state(every,off,WIN_START+i)
        if st and st!='T': rr(colX(i),rowY(r,g0),CELL,CELL,5,st)
# enlarged today cells (only tasks due today)
for r,(tid,lab,every,off) in enumerate(TASKS):
    if state(every,off,TODAY_D)=='T':
        rr(cx-BIG/2,rowY(r,g0)+CELL/2-BIG/2,BIG,BIG,7,ORANGE)
y=rowY(len(TASKS),g0)+12

# ── legend + SOW print ──
lx=PAD
for lab,col in [('Scheduled',GREY),('Incomplete',ORANGE),('Done',GREEN)]:
    rr(lx,y-9,12,12,4,col); txt(lx+17,y+1,lab,10,MUTED); lx+=len(lab)*6+34
txt(W-PAD,y+1,'Start of Watering · '+SOW.strftime('%b %-d, %Y'),9.5,MUTED,ital=True,a='end')
y+=20
e(f'<rect x="{PAD}" y="{y:.0f}" width="{W-2*PAD}" height="1" fill="{DIV}"/>'); y+=18

# ── export ──
rr(PAD,y,108,40,10,TEAL,TEALBD,2)
txt(PAD+54,y+25,'EXPORT',11,'#fff',w='700',a='middle',ls='1')
y+=58

# ── cards ──
txt(PAD,y,'TODAY’S TASK CARDS',11,MOSS,w='700',ls='1.2'); y+=16
def card(y,title,badge,desc,steps):
    pad=18; hH=44; iw=W-2*PAD
    dl=wrap(desc,iw-2*pad,12)
    bh=hH+18+len(dl)*17+8+len(steps)*30+12
    rr(PAD,y,iw,bh,12,'#fff',DIV,1.5)
    e(f'<rect x="{PAD}" y="{y}" width="{iw}" height="{hH}" rx="12" fill="url(#cg)"/>')
    e(f'<rect x="{PAD}" y="{y+hH-12:.0f}" width="{iw}" height="12" fill="#cdeec0"/>')
    rr(PAD+pad,y+(hH-22)/2,22,22,5,ORANGE,DIV,2)
    txt(PAD+pad+32,y+hH/2+6,title,16,'#4b8c46',w='600')
    pw=len(badge)*5.6+18
    rr(PAD+iw-pad-pw,y+(hH-21)/2,pw,21,10.5,'#d0f0d0','#89c689',1)
    txt(PAD+iw-pad-pw/2,y+hH/2+4,badge,8.5,MOSS,w='600',a='middle',ls='.4')
    cy=y+hH+20
    for ln in dl: txt(PAD+pad,cy,ln,12,MUTED,ital=True); cy+=17
    cy+=8
    for i,s in enumerate(steps):
        e(f'<circle cx="{PAD+pad+11:.0f}" cy="{cy-4:.0f}" r="11" fill="{GREEN}"/>')
        txt(PAD+pad+11,cy,str(i+1),11,'#fff',w='700',a='middle')
        sl=wrap(s,iw-2*pad-32,11.5)
        for j,ln in enumerate(sl): txt(PAD+pad+30,cy+j*14,ln,11.5,'#2a402a')
        cy+=30
    return bh
for t,b,d,s in CARDS:
    y+=card(y,t,b,d,s)+14
y+=8

H=int(y)
defs=('<defs><linearGradient id="cg" x1="0" y1="0" x2="1" y2="0.5">'
      '<stop offset="0.06" stop-color="#dff0da"/><stop offset="1" stop-color="#a1ff7f"/></linearGradient></defs>')
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
     f'{defs}<rect width="{W}" height="{H}" fill="{CREAM}"/>'+''.join(out)+'</svg>')
open('/Users/torque/Documents/GitHub/puffer3.github.io/Gardyn/Dev/mobile_page.svg','w',encoding='utf-8').write(svg)
print('wrote mobile_page.svg',W,'x',H,' today col index',TODAY_COL,' window',WIN_START,'-',WIN_START+WIN_DAYS-1)
print('today due:',[lab for (tid,lab,ev,of) in TASKS if state(ev,of,TODAY_D)=='T'])
