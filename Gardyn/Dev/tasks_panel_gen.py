#!/usr/bin/env python3
# Generates an SVG reproduction of the TrackerMbile.html "Tasks" panel (#today)
# at 1920px wide with the artboard height auto-fit to the full content.
# Includes embedded logo + tab-nav placeholders, all four task sections, and the
# closing tip callout. SVG <text>/<rect> import into Illustrator as editable
# text frames + vector shapes.

import html, re, math

S = 2  # scale: CSS px -> SVG px

# ---- palette (from :root) ----
CREAM      = "#f0faf0"
PARCHMENT  = "#dff0da"
INK        = "#0f1a0f"
MOSS       = "#0f6b22"
SAGE       = "#6aaa50"
TERRACOTTA = "#b85c38"
GOLD       = "#c4962a"
MUTED      = "#4a6b52"
DIVIDER    = "#9cc49c"
STEPINK    = "#2a402a"
WHITE      = "#ffffff"

BADGE = {
    "green": ("#d0f0d0", MOSS),
    "blue":  ("#e0e8f0", "#2d5a8a"),
    "gold":  ("#f5edda", GOLD),
}

SANS = "Jost, sans-serif"
DISP = "Papyrus, fantasy"

# ---- geometry ----
W = 1920
COL_W = 780 * S                 # 1560
COL_X = (W - COL_W) / 2         # 180
PAN_PAD = 16 * S                # 32
CX0 = COL_X + PAN_PAD           # 212
CX1 = COL_X + COL_W - PAN_PAD   # 1708
INNER = CX1 - CX0               # 1496

# ---- data ----
sections = [
    {"emoji":"💧","title":"Every 2–3 Days","sub":"QUICK CHECKS — TAKES 5 MINUTES","items":[
        {"t":"Check Reservoir Water Level","b":None,
         "d":"Plants drink more water than nutrients — top up between feeding days",
         "s":["Top up with plain water if below the minimum line",
              "Listen for the pump — should be running quietly and consistently",
              "Confirm water is trickling down through all pods from the top"]},
        {"t":"Check Nursery Tray Moisture","b":None,
         "d":"While you have seedlings germinating on the lid",
         "s":["Dark green & moist to touch = fine, leave it alone",
              "Light green & dry = re-soak for 5 minutes, drain, replace lid",
              "Look for sprouts — lettuce 3–7 days, herbs 5–14 days, flowers 5–21 days"]},
        {"t":"Deadhead Flowers","b":None,
         "d":"Especially petunias and dianthus — prevents petals dropping into reservoir",
         "s":["Pinch spent blooms at the base of the flower stem as soon as petals fade",
              "Check reservoir area for any fallen petals and remove them",
              "Deadheading triggers new buds — the more you do it the more it flowers"]},
    ]},
    {"emoji":"📅","title":"Weekly Tasks","sub":"CORE MAINTENANCE — RESET EACH WEEK","items":[
        {"t":"Harvest Leafy Greens","b":("Outer Leaf Method","green"),
         "d":"Cut from the outside in — never touch the center growing crown",
         "s":["Cut at the base of outer leaf stems with sharp scissors — don't pull",
              "Never take more than 1/3 of the plant in one session",
              "Harvest before leaves press against LEDs or neighboring pods",
              "Chives: cut the whole clump to 1–2 inches tall, regrows within a week"]},
        {"t":"Prune Herbs","b":None,
         "d":"Keep them bushy and productive — neglect causes bolting and legginess",
         "s":["Basil: pinch any flower buds the moment they appear · cut to a node if overgrown",
              "Mint: trim runners escaping into other pods · cut hard to 3–4 inches if overgrown",
              "Rosemary: snip 1–2 inches from stem tips only, never into woody growth"]},
        {"t":"Add Plant Food","b":("Week 3+ only","blue"),
         "d":"Leafy greens need nitrogen-forward formula at lighter EC than fruiting plants",
         "s":["New seedlings weeks 1–2: plain water only, zero nutrients",
              "Week 3: half dose · Week 4+: full dose weekly",
              "Target EC 1.0–1.6 · Target pH 5.5–6.5",
              "Overfeeding signs: brown crispy leaf edges, white crust on rockwool — flush 1 week"]},
        {"t":"Mildew Prevention Spray","b":("Alternate Weeks","gold"),
         "d":"Rotate to prevent resistance — morning application only so leaves dry fully",
         "s":["Week A: Baking soda spray — 1 tsp baking soda + 1 tsp dish soap + 1 qt water",
              "Week B: Neem oil spray — few drops neem + 1 tsp dish soap + 1 qt water, shake constantly",
              "Spray both sides of all leaves · never spray a freshly pruned stressed plant"]},
        {"t":"Inspect for Pests & Mildew","b":None,
         "d":"Catch problems early before they spread across pods",
         "s":["Check undersides of all leaves — that's where pests hide and lay eggs",
              "White powdery patches = mildew · Silver streaks = thrips · Fine webbing = spider mites",
              "Any affected leaves: bag and trash immediately, never compost"]},
        {"t":"Check Hibiscus Stake & Tilt","b":None,
         "d":"If still in the tower — monitor lean and adjust support",
         "s":["If leaning: pack a small piece of damp sponge beside the rockwool cube to wedge it upright",
              "A bamboo skewer or chopstick inserted alongside the stem acts as a stake",
              "Tie loosely with a twist tie or soft plant tape — never tight against the stem",
              "Best long-term fix: transplant to a pot in full sun outdoors (see General tab)"]},
    ]},
    {"emoji":"🔄","title":"Every 2–3 Weeks","sub":"DEEPER MAINTENANCE — SCHEDULE A 30 MIN SESSION","items":[
        {"t":"Full Reservoir Drain & Clean","b":None,
         "d":"Prevents salt buildup, algae, and root rot bacteria accumulation",
         "s":["Drain completely — don't just top up",
              "Wipe interior with a cloth, rinse thoroughly",
              "Add a few ml of 3% H2O2 to fresh clean water on refill",
              "Mix fresh nutrient dose into the clean water before replacing"]},
        {"t":"Root Inspection","b":None,
         "d":"Do during reservoir drain when you can see roots clearly",
         "s":["Gently pull each pod slightly to check roots below",
              "White & fuzzy = perfect · Tan/beige = normal · Brown & slimy = treat immediately",
              "If brown & slimy: rinse, trim dead roots, soak in 1:5 H2O2 solution for 10 min"]},
        {"t":"Triage Declining Pods","b":None,
         "d":"Regular turnover keeps the garden productive — don't hang onto lost causes",
         "s":["Remove any pod more than 50% brown or with slimy base",
              "Clean empty pods with H2O2 solution, air dry fully",
              "Start new yCubes in nursery tray to replace pulled pods"]},
    ]},
    {"emoji":"🗓️","title":"Monthly Tasks","sub":"DEEP CLEAN SESSION — ABOUT AN HOUR","items":[
        {"t":"Root Trimming","b":None,
         "d":"Roots clogging the pump starve every plant in the system silently",
         "s":["Do during reservoir drain so roots are fully visible",
              "Sterilize scissors with rubbing alcohol before starting",
              "Trim only roots clogging the reservoir or wrapping the pump",
              "Never remove more than 1/3 of root mass at once"]},
        {"t":"Pump Clean","b":None,
         "d":"A failing pump can kill every plant within 24 hours",
         "s":["Remove pump, rinse under warm water",
              "Clear any root debris or algae from the intake",
              "Return and confirm strong water flow from the top of the tower"]},
        {"t":"Tower Column Scrub","b":None,
         "d":"Algae and mineral deposits restrict water flow over time",
         "s":["Remove all pods, rinse column interior with warm water",
              "Bottle brush for algae · 1:1 white vinegar soak 15 min for mineral deposits",
              "Rinse thoroughly before replacing pods — vinegar residue affects pH"]},
    ]},
]
CALLOUT = ("Tip:  Tasks reset each session — uncheck everything at the start of a new "
           "maintenance day to use this as a fresh checklist. Full guides and how-tos for "
           "every task are in the General Care Guide tab.")

# ---- text helpers ----
def esc(t): return html.escape(t, quote=False)

def wrap(text, font_px, max_w, cw=0.52):
    avg = font_px * cw
    max_chars = max(8, int(max_w / avg))
    lines, cur = [], ""
    for w in text.split():
        trial = w if not cur else cur + " " + w
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines or [""]

# ---- load logo inner markup ----
with open("/Users/torque/Documents/GitHub/puffer3.github.io/Gardyn/Dev/MenuLogoMoody.svg",
          encoding="utf-8") as f:
    _logo = f.read()
_logo = re.sub(r'<\?xml.*?\?>', '', _logo, flags=re.S)
_m = re.search(r'<svg[^>]*>(.*)</svg>', _logo, flags=re.S)
LOGO_INNER = _m.group(1) if _m else ""
LOGO_VB = "0 0 550.70 163.67"

body = []
def emit(s): body.append(s)

y = 50

# ---------- HEADER ----------
emit('<g id="header-placeholder">')
gs = 48
gx, gy = CX1 - gs, y
emit(f'<rect x="{gx}" y="{gy}" width="{gs}" height="{gs}" rx="10" fill="none" stroke="{DIVIDER}" stroke-width="2"/>')
emit(f'<circle cx="{gx+gs/2}" cy="{gy+gs/2}" r="9" fill="none" stroke="{MUTED}" stroke-width="2"/>')
emit(f'<circle cx="{gx+gs/2}" cy="{gy+gs/2}" r="3" fill="{MUTED}"/>')
logo_w = 520
logo_h = logo_w * 163.67 / 550.70
lx = (W - logo_w) / 2
ly = y + 6
emit(f'<svg x="{lx:.0f}" y="{ly:.0f}" width="{logo_w}" height="{logo_h:.1f}" viewBox="{LOGO_VB}">{LOGO_INNER}</svg>')
emit('</g>')
y = ly + logo_h + 26

# ---------- TAB NAV ----------
tabs = [("Tower", False), ("Tracker", False), ("Tasks", True), ("Info", False)]
nav_h = 92
nav_top = y
cell_w = COL_W / 4
ai = next(i for i,(_,a) in enumerate(tabs) if a)
emit(f'<rect x="{COL_X+ai*cell_w:.1f}" y="{nav_top}" width="{cell_w:.1f}" height="{nav_h}" fill="#e3efe4"/>')
emit(f'<rect x="{COL_X}" y="{nav_top+nav_h-2}" width="{COL_W}" height="2" fill="{DIVIDER}"/>')
tab_font = round(0.72*16*S, 1)
for i,(label,active) in enumerate(tabs):
    cx = COL_X + cell_w*(i+0.5)
    col = MOSS if active else MUTED
    icon = 30
    lw_est = len(label)*tab_font*0.62
    total = icon + 10 + lw_est
    sx = cx - total/2
    midy = nav_top + nav_h/2
    emit(f'<rect x="{sx:.0f}" y="{midy-icon/2:.0f}" width="{icon}" height="{icon}" rx="7" fill="none" stroke="{col}" stroke-width="2.5"/>')
    weight = '700' if active else '400'
    emit(f'<text x="{sx+icon+10:.0f}" y="{midy+tab_font*0.34:.0f}" font-family="{SANS}" font-size="{tab_font}" font-weight="{weight}" letter-spacing="{0.14*tab_font:.1f}" fill="{col}">{esc(label.upper())}</text>')
    if active:
        emit(f'<rect x="{COL_X+i*cell_w:.1f}" y="{nav_top+nav_h-4}" width="{cell_w:.1f}" height="4" fill="{MOSS}"/>')
y = nav_top + nav_h + 24

# ---------- intro ----------
intro_pad_v, intro_pad_h = 16*S, 20*S
intro_font = 16*S
intro_lh = intro_font * 1.6
intro_text = ("Your reset day.  Work through this list top to bottom — remove first, then prune, "
              "then prep new pods. Checking off tasks as you go will track your progress.")
intro_lines = wrap(intro_text, intro_font, INNER - 2*intro_pad_h - 6)
intro_box_h = 2*intro_pad_v + len(intro_lines)*intro_lh
emit('<g id="intro">')
emit(f'<rect x="{CX0}" y="{y}" width="{INNER}" height="{intro_box_h:.0f}" rx="16" fill="{PARCHMENT}"/>')
emit(f'<rect x="{CX0}" y="{y}" width="6" height="{intro_box_h:.0f}" fill="{GOLD}"/>')
ty = y + intro_pad_v + intro_font
tx = CX0 + intro_pad_h
emit(f'<text x="{tx}" y="{ty:.0f}" font-family="{SANS}" font-size="{intro_font}" font-style="italic" fill="{MUTED}">')
for i,ln in enumerate(intro_lines):
    emit(f'<tspan x="{tx}" y="{ty + i*intro_lh:.0f}">{esc(ln)}</tspan>')
emit('</text>')
emit('</g>')
y += intro_box_h + 28*S

# ---------- progress ----------
pl_font = 13*S
emit(f'<text x="{CX0}" y="{y+pl_font:.0f}" font-family="{SANS}" font-size="{pl_font}" letter-spacing="{0.15*pl_font:.1f}" fill="{MUTED}">0 COMPLETE</text>')
btn_h, btn_w = 24*S, 150
emit(f'<rect x="{CX1-btn_w}" y="{y-4}" width="{btn_w}" height="{btn_h}" rx="6" fill="none" stroke="{DIVIDER}" stroke-width="2"/>')
emit(f'<text x="{CX1-btn_w/2}" y="{y-4+btn_h/2+pl_font*0.36:.0f}" text-anchor="middle" font-family="{SANS}" font-size="{pl_font}" letter-spacing="{0.12*pl_font:.1f}" fill="{MUTED}">RESET</text>')
y += btn_h + 12
bar_h = 6*S
emit(f'<rect x="{CX0}" y="{y}" width="{INNER}" height="{bar_h}" rx="6" fill="#ddf0da"/>')
y += bar_h + 24*S

# ---------- sections ----------
GAP = 32*S
CARD_PAD_V, CARD_PAD_H = 14*S, 16*S
CB, CB_GAP = 20*S, 12*S
title_font = 16*S
desc_font  = round(0.9*16*S, 1)
step_font  = round(0.88*16*S, 1)
desc_lh, step_lh = desc_font*1.5, step_font*1.5
text_x = CX0 + CARD_PAD_H + CB + CB_GAP
text_w = INNER - 2*CARD_PAD_H - CB - CB_GAP

def card_height(item):
    h = CARD_PAD_V*2 + title_font*1.25
    h += 4 + len(wrap(item["d"], desc_font, text_w))*desc_lh
    h += 12 + sum(len(wrap(s, step_font, text_w - 28))*step_lh for s in item["s"])
    return h

for sec in sections:
    sec_title_font = round(1.4*16*S,1)
    emit(f'<text x="{W/2}" y="{y+sec_title_font:.0f}" text-anchor="middle" font-family="{DISP}" font-size="{sec_title_font}" fill="{MOSS}">{esc(sec["emoji"]+"  "+sec["title"])}</text>')
    y += sec_title_font*1.2 + 8
    sub_font = round(0.62*16*S,1)
    emit(f'<text x="{W/2}" y="{y+sub_font:.0f}" text-anchor="middle" font-family="{SANS}" font-size="{sub_font}" letter-spacing="{0.18*sub_font:.1f}" fill="{MUTED}">{esc(sec["sub"])}</text>')
    y += sub_font + 24
    emit(f'<rect x="{CX0}" y="{y+16}" width="{INNER}" height="2" fill="{DIVIDER}"/>')
    y += 16 + 2 + 28
    for item in sec["items"]:
        ch = card_height(item)
        emit('<g>')
        emit(f'<rect x="{CX0}" y="{y:.0f}" width="{INNER}" height="{ch:.0f}" rx="20" fill="{WHITE}" stroke="{DIVIDER}" stroke-width="2"/>')
        emit(f'<rect x="{CX0}" y="{y:.0f}" width="6" height="{ch:.0f}" fill="{SAGE}"/>')
        cbx, cby = CX0 + CARD_PAD_H, y + CARD_PAD_V + 4
        emit(f'<rect x="{cbx:.0f}" y="{cby:.0f}" width="{CB}" height="{CB}" rx="6" fill="{WHITE}" stroke="{DIVIDER}" stroke-width="3"/>')
        cy = y + CARD_PAD_V + title_font
        emit(f'<text x="{text_x:.0f}" y="{cy:.0f}" font-family="{DISP}" font-size="{title_font}" font-weight="700" fill="{INK}">{esc(item["t"])}</text>')
        if item["b"]:
            btxt, bkind = item["b"]
            bg, fg = BADGE[bkind]
            bx = text_x + len(item["t"])*title_font*0.5 + 16
            bfont = round(0.58*16*S,1)
            bw = len(btxt)*bfont*0.6 + 28
            by = cy - title_font*0.78
            bh = bfont + 16
            emit(f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="4" fill="{bg}"/>')
            emit(f'<text x="{bx+bw/2:.0f}" y="{by+bh/2+bfont*0.36:.0f}" text-anchor="middle" font-family="{SANS}" font-size="{bfont}" letter-spacing="{0.08*bfont:.1f}" fill="{fg}">{esc(btxt.upper())}</text>')
        cy += 4 + desc_font
        for ln in wrap(item["d"], desc_font, text_w):
            emit(f'<text x="{text_x:.0f}" y="{cy:.0f}" font-family="{SANS}" font-size="{desc_font}" font-style="italic" fill="{MUTED}">{esc(ln)}</text>')
            cy += desc_lh
        cy += 12 - desc_lh + step_font
        for s in item["s"]:
            for j, ln in enumerate(wrap(s, step_font, text_w - 28)):
                if j == 0:
                    emit(f'<text x="{text_x:.0f}" y="{cy:.0f}" font-family="{SANS}" font-size="{step_font}" fill="{SAGE}">—</text>')
                emit(f'<text x="{text_x+28:.0f}" y="{cy:.0f}" font-family="{SANS}" font-size="{step_font}" fill="{STEPINK}">{esc(ln)}</text>')
                cy += step_lh
        emit('</g>')
        y += ch + 8*S
    y += GAP - 8*S

# ---------- callout ----------
co_font = round(0.9*16*S,1)
co_pad = 18*S
co_lines = wrap(CALLOUT, co_font, INNER - 2*co_pad)
co_h = 2*co_pad + len(co_lines)*co_font*1.5
emit(f'<rect x="{CX0}" y="{y}" width="{INNER}" height="{co_h:.0f}" rx="12" fill="{PARCHMENT}"/>')
cyy = y + co_pad + co_font
for ln in co_lines:
    emit(f'<text x="{CX0+co_pad:.0f}" y="{cyy:.0f}" font-family="{SANS}" font-size="{co_font}" fill="{INK}">{esc(ln)}</text>')
    cyy += co_font*1.5
y += co_h + 50

# ---- assemble with auto-fit height ----
H = int(math.ceil(y))
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       f'<rect x="0" y="0" width="{W}" height="{H}" fill="{CREAM}"/>'
       + "".join(body) + '</svg>')

path = "/Users/torque/Documents/GitHub/puffer3.github.io/Gardyn/Dev/tasks_panel.svg"
with open(path, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", path, "size", W, "x", H)
