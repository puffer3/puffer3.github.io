#!/usr/bin/env python3
# Mockup: the ARCHIVED (collapsed) state of a tracker card.
# When Archive is hit, the card stays in place but content clears to a slim
# tombstone — "{Plant} archived" + Undo + a category-specific funny line.
# Three category variants: flower / herb / edible. Editable text + shapes.

import html

CREAM='#f0faf0'; INK='#0f1a0f'; MOSS='#0f6b22'; MUTED='#4a6b52'; DIV='#9cc49c'
GOLD='#c4962a'; YEL_BG='#f9f0d3'; YEL_BD='#e2c878'; YEL_TX='#8f6a12'
ROSE='#c2557f'; HERB='#2e8b57'; TERRA='#b85c38'
F='Avenir Next, sans-serif'

PAD=24; W=472; IW=W-2*PAD; CH=88; GAP=16

# (pod, plant, "archived"-glyph, category label, accent color, funny line)
CARDS=[
 ('14','Marigold','FLOWER',ROSE,
  'Off to the great vase in the sky.'),
 ('3','Chervil','HERB',HERB,
  'Hung up to dry — permanently.'),
 ('7','Buttercrunch','EDIBLE',TERRA,
  'Gone to the great salad bowl in the sky.'),
]

out=[]
def e(s): out.append(s)
def esc(t): return html.escape(t,quote=False)
def txt(x,y,s,fs,fill,*,w='400',a='start',ital=False,ls=None):
    A=f' text-anchor="{a}"' if a!='start' else ''
    I=' font-style="italic"' if ital else ''
    L=f' letter-spacing="{ls}"' if ls else ''
    e(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{F}" font-size="{fs}" font-weight="{w}"{I}{L} fill="{fill}"{A}>{esc(s)}</text>')
def rr(x,y,w,h,r,fill,stroke=None,sw=0):
    S=f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    e(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}"{S}/>')

y=34
# ── header ──
txt(PAD,y,'Archived Card — collapsed state',17,MOSS,w='700'); y+=20
txt(PAD,y,'Hit Archive → the card keeps its slot but content clears to this. Undo restores it.',11,MUTED,ital=True)
y+=26

def card(y,pod,plant,cat,accent,phrase):
    # card shell
    rr(PAD,y,IW,CH,9,CREAM,DIV,1.5)
    # category accent bar on the left edge
    rr(PAD,y,5,CH,9,accent)
    rr(PAD+3,y,3,CH,0,CREAM)            # square off the inner side of the bar
    rr(PAD,y,5,CH,9,accent)
    cx=PAD+24
    # eyebrow: pod + category
    txt(cx,y+24,'POD '+pod,9,MUTED,w='600',ls='1.2')
    txt(cx+58,y+24,'·',9,DIV)
    txt(cx+70,y+24,cat,9,accent,w='700',ls='1.2')
    # archive glyph + headline
    e(f'<text x="{cx:.1f}" y="{y+50:.1f}" font-family="{F}" font-size="15" fill="{MUTED}">&#x1F5C3;</text>')
    txt(cx+24,y+50,plant,15,INK,w='700')
    nw=len(plant)*15*0.56
    txt(cx+24+nw+7,y+50,'archived',15,MUTED,w='400',ital=True)
    # funny line
    txt(cx,y+70,phrase,11.5,accent,ital=True)
    # Undo button (yellow), right-aligned, vertically centered
    bw=92; bh=36; bx=PAD+IW-20-bw; by=y+(CH-bh)/2
    rr(bx,by,bw,bh,9,YEL_BG,YEL_BD,1.5)
    txt(bx+bw/2,by+bh/2+4.5,'↩  Undo',12,YEL_TX,w='700',a='middle',ls='.4')
    return CH

for pod,plant,cat,accent,phrase in CARDS:
    y+=card(y,pod,plant,cat,accent,phrase)+GAP

y+=10
# footnote
e(f'<rect x="{PAD}" y="{y:.0f}" width="{IW}" height="1" fill="{DIV}"/>'); y+=20
txt(PAD,y,'Funny line keys off the plant family — flower / herb / edible each get their own pool.',11,MUTED,ital=True)
y+=22

H=int(y)
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
     f'<rect width="{W}" height="{H}" fill="#ffffff"/>'+''.join(out)+'</svg>')
path='/Users/torque/Documents/GitHub/puffer3.github.io/Gardyn/Dev/archived_card_mock.svg'
open(path,'w',encoding='utf-8').write(svg)
print('wrote',path,W,'x',H)
