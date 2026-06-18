#!/usr/bin/env python3
"""
SytFix Complete Site Builder + GitHub Deployer
Run: python3 build.py
Then: GITHUB_TOKEN=xxx python3 build.py --deploy
"""
import os, sys, subprocess, json, urllib.request, urllib.error, shutil, textwrap

ROOT   = os.path.dirname(os.path.abspath(__file__))
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_USER  = os.environ.get("GITHUB_USER",  "RAMitchell4")
REPO_NAME    = os.environ.get("REPO_NAME",    "sytfix-site")
API          = "https://api.github.com"
BRANCH       = "main"

# ─────────────────────────────────────────────────────────────────
# SHARED SVG LOGO PATHS (exact from provided SVG)
# ─────────────────────────────────────────────────────────────────
LOGO_FULL_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="75 215 530 175" role="img" aria-label="SytFix">
  <title>SytFix</title>
  <g transform="translate(0,600) scale(0.1,-0.1)">
    <g fill="#F4F4EE">
      <path d="M1510 3680 l0 -40 45 0 45 0 0 40 0 40 -45 0 -45 0 0 -40z"/>
      <path d="M1335 3686 c-131 -42 -212 -92 -315 -196 -79 -78 -104 -111 -142 -185 -45 -89 -78 -183 -78 -224 0 -18 6 -21 39 -21 37 0 39 2 46 38 19 106 118 277 204 355 86 78 199 139 309 167 41 10 42 12 42 50 0 48 -5 49 -105 16z"/>
      <path d="M1682 3669 c3 -41 3 -42 57 -56 139 -35 300 -153 384 -281 47 -71 91 -172 102 -234 7 -37 8 -38 50 -38 l43 0 -13 58 c-62 263 -260 477 -527 568 -97 33 -100 32 -96 -17z"/>
      <path d="M4317 3416 c-49 -18 -67 -34 -84 -73 -20 -49 -16 -82 17 -146 33 -61 32 -63 -23 -69 -36 -4 -35 -20 4 -33 16 -6 34 -17 39 -25 13 -20 13 -356 0 -380 -5 -10 -21 -21 -35 -24 -14 -4 -25 -13 -25 -21 0 -13 23 -15 139 -15 92 0 142 4 147 11 9 15 -14 29 -46 29 -48 0 -50 11 -50 222 l0 198 44 0 c54 0 76 8 76 26 0 10 -15 14 -59 14 -57 0 -60 1 -78 34 -10 19 -31 52 -46 74 -39 55 -45 100 -17 135 14 18 31 27 50 27 41 0 60 -24 60 -75 0 -34 5 -47 22 -59 71 -50 122 42 62 113 -40 48 -122 63 -197 37z"/>
      <path d="M2743 3394 c-75 -27 -133 -113 -133 -199 0 -114 70 -188 235 -250 143 -53 185 -93 185 -176 0 -33 -6 -47 -34 -75 -31 -31 -39 -34 -92 -34 -86 0 -149 39 -205 125 -23 36 -47 64 -53 62 -15 -6 -12 -58 9 -149 18 -82 29 -92 60 -58 23 25 32 25 86 0 67 -30 170 -27 238 6 69 35 103 86 109 164 6 77 -10 121 -60 165 -37 34 -72 53 -223 118 -101 44 -146 112 -125 187 26 92 131 122 236 67 39 -20 97 -84 124 -137 22 -42 31 -48 48 -27 15 18 -47 221 -70 225 -9 2 -22 -6 -28 -17 -13 -26 -26 -26 -81 -1 -53 24 -164 26 -226 4z"/>
      <path d="M3927 3224 c-17 -26 -37 -54 -44 -63 -9 -13 -37 -17 -147 -21 -133 -5 -170 -16 -108 -32 17 -5 33 -15 36 -24 5 -13 -106 -316 -124 -337 -8 -9 -140 304 -140 333 0 13 10 22 32 28 17 4 33 13 36 20 3 9 -31 12 -132 12 -114 0 -136 -2 -136 -15 0 -8 6 -15 14 -15 26 0 52 -47 156 -285 l103 -235 -13 -41 c-8 -23 -26 -61 -42 -85 -39 -62 -77 -58 -93 9 -9 35 -49 67 -76 60 -26 -7 -42 -47 -34 -84 20 -89 161 -108 222 -29 23 28 64 122 164 372 120 301 121 303 158 316 25 9 93 1 103 -11 0 -1 4 -96 7 -210 l6 -209 27 -23 c56 -48 165 -40 212 16 25 29 35 69 18 69 -5 0 -19 -11 -32 -25 -39 -41 -92 -27 -105 28 -3 12 -4 99 -3 192 l3 170 68 3 c49 2 67 7 67 17 0 10 -18 15 -67 17 l-68 3 -3 63 c-4 77 -19 81 -65 16z"/>
      <path d="M4642 3123 c-73 -25 -89 -45 -41 -52 13 -1 27 -8 31 -15 4 -6 8 -91 8 -189 l0 -178 -36 -21 c-21 -12 -32 -24 -26 -30 14 -14 235 -6 239 9 3 7 -7 15 -21 19 -14 3 -27 7 -28 8 -1 0 -5 107 -8 236 -6 273 3 256 -118 213z"/>
      <path d="M4860 3126 c0 -8 9 -18 21 -21 22 -7 169 -200 169 -223 0 -32 -152 -210 -192 -225 -9 -3 -10 -8 -2 -16 7 -8 40 -11 94 -9 89 3 113 18 60 36 -42 15 -39 38 19 117 l49 67 56 -75 c31 -42 56 -82 56 -89 0 -8 -14 -19 -31 -25 -58 -22 -22 -33 106 -33 135 0 158 9 111 43 -30 22 -179 214 -179 231 0 21 135 186 164 201 49 26 34 35 -60 35 -94 0 -124 -13 -72 -31 21 -7 31 -18 31 -31 0 -19 -78 -137 -91 -138 -11 0 -109 143 -103 152 3 5 17 13 31 19 50 19 10 29 -113 29 -101 0 -124 -3 -124 -14z"/>
      <path d="M780 2940 l0 -40 45 0 45 0 0 40 0 40 -45 0 -45 0 0 -40z"/>
      <path d="M2240 2941 c0 -36 2 -39 37 -44 47 -8 53 -3 53 44 l0 39 -45 0 -45 0 0 -39z"/>
      <path d="M800 2804 c0 -60 67 -228 123 -308 72 -103 160 -184 268 -245 63 -35 190 -81 226 -81 20 0 23 5 23 39 0 37 -2 39 -37 46 -113 21 -253 105 -348 208 -73 78 -145 210 -166 301 l-12 56 -39 0 c-28 0 -38 -4 -38 -16z"/>
      <path d="M2231 2798 c-5 -13 -12 -38 -16 -57 -43 -201 -258 -417 -473 -477 l-62 -17 0 -40 0 -40 42 7 c22 4 74 20 114 37 184 77 329 212 410 384 35 74 76 209 66 219 -3 3 -20 6 -39 6 -26 0 -35 -5 -42 -22z"/>
      <path d="M1514 2226 c-3 -8 -4 -27 -2 -43 3 -25 7 -28 46 -31 l42 -3 0 45 0 46 -40 0 c-26 0 -43 -5 -46 -14z"/>
    </g>
    <g fill="#B8EF1B">
      <path d="M1540 3266 l0 -296 -30 0 c-29 0 -30 -2 -30 -44 0 -39 -4 -46 -40 -71 l-40 -28 0 -128 0 -128 76 -108 c41 -59 78 -109 82 -110 4 -1 42 50 85 114 l77 116 0 121 0 121 -45 30 c-41 28 -45 33 -45 73 0 38 -2 42 -25 42 l-25 0 -2 292 c-3 270 -4 293 -20 296 -17 3 -18 -16 -18 -292z"/>
      <path d="M3280 3349 c-36 -28 -67 -52 -69 -55 -2 -2 113 -4 257 -4 l262 0 0 55 0 55 -192 -1 -193 0 -65 -50z"/>
      <path d="M4635 3375 c-16 -15 -25 -36 -25 -55 0 -19 9 -40 25 -55 15 -16 36 -25 55 -25 19 0 40 9 55 25 16 15 25 36 25 55 0 19 -9 40 -25 55 -15 16 -36 25 -55 25 -19 0 -40 -9 -55 -25z"/>
    </g>
  </g>
</svg>'''

ICON_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="75 215 185 175" role="img" aria-label="SytFix mark">
  <title>SytFix</title>
  <g transform="translate(0,600) scale(0.1,-0.1)">
    <g fill="#F4F4EE">
      <path d="M1510 3680 l0 -40 45 0 45 0 0 40 0 40 -45 0 -45 0 0 -40z"/>
      <path d="M1335 3686 c-131 -42 -212 -92 -315 -196 -79 -78 -104 -111 -142 -185 -45 -89 -78 -183 -78 -224 0 -18 6 -21 39 -21 37 0 39 2 46 38 19 106 118 277 204 355 86 78 199 139 309 167 41 10 42 12 42 50 0 48 -5 49 -105 16z"/>
      <path d="M1682 3669 c3 -41 3 -42 57 -56 139 -35 300 -153 384 -281 47 -71 91 -172 102 -234 7 -37 8 -38 50 -38 l43 0 -13 58 c-62 263 -260 477 -527 568 -97 33 -100 32 -96 -17z"/>
      <path d="M780 2940 l0 -40 45 0 45 0 0 40 0 40 -45 0 -45 0 0 -40z"/>
      <path d="M2240 2941 c0 -36 2 -39 37 -44 47 -8 53 -3 53 44 l0 39 -45 0 -45 0 0 -39z"/>
      <path d="M800 2804 c0 -60 67 -228 123 -308 72 -103 160 -184 268 -245 63 -35 190 -81 226 -81 20 0 23 5 23 39 0 37 -2 39 -37 46 -113 21 -253 105 -348 208 -73 78 -145 210 -166 301 l-12 56 -39 0 c-28 0 -38 -4 -38 -16z"/>
      <path d="M2231 2798 c-5 -13 -12 -38 -16 -57 -43 -201 -258 -417 -473 -477 l-62 -17 0 -40 0 -40 42 7 c22 4 74 20 114 37 184 77 329 212 410 384 35 74 76 209 66 219 -3 3 -20 6 -39 6 -26 0 -35 -5 -42 -22z"/>
      <path d="M1514 2226 c-3 -8 -4 -27 -2 -43 3 -25 7 -28 46 -31 l42 -3 0 45 0 46 -40 0 c-26 0 -43 -5 -46 -14z"/>
    </g>
    <g fill="#B8EF1B">
      <path d="M1540 3266 l0 -296 -30 0 c-29 0 -30 -2 -30 -44 0 -39 -4 -46 -40 -71 l-40 -28 0 -128 0 -128 76 -108 c41 -59 78 -109 82 -110 4 -1 42 50 85 114 l77 116 0 121 0 121 -45 30 c-41 28 -45 33 -45 73 0 38 -2 42 -25 42 l-25 0 -2 292 c-3 270 -4 293 -20 296 -17 3 -18 -16 -18 -292z"/>
    </g>
  </g>
</svg>'''

CSS_MAIN = r'''/* ═══════════════════════════════════════════════════════
   SYTFIX — main.css  |  Complete design system
   ═══════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=IBM+Plex+Mono:wght@300;400;500;600&family=Instrument+Sans:wght@400;500;600&display=swap');

/* ── Variables ── */
:root {
  --bg:        #080809;
  --bg2:       #0d0d10;
  --bg3:       #121215;
  --surf:      #17171c;
  --surf2:     #1c1c22;
  --border:    rgba(255,255,255,0.055);
  --border2:   rgba(255,255,255,0.10);
  --border3:   rgba(255,255,255,0.19);
  --t:         #f1eee8;
  --t2:        #8a8a9c;
  --t3:        #4e4e60;
  --t4:        #2a2a35;
  --lime:      #B8EF1B;
  --lime2:     #a2d118;
  --lime3:     #8cb614;
  --lime-d:    rgba(184,239,27,0.06);
  --lime-d2:   rgba(184,239,27,0.13);
  --lime-glow: rgba(184,239,27,0.22);
  --cream:     #F4F4EE;
  --serif:     'DM Serif Display', Georgia, serif;
  --mono:      'IBM Plex Mono', 'Courier New', monospace;
  --sans:      'Instrument Sans', system-ui, -apple-system, sans-serif;
  --max:       1160px;
  --nav-h:     66px;
  --pad:       clamp(80px,9vw,132px);
  --gtr:       clamp(18px,4.5vw,52px);
  --r:         8px;
  --r2:        16px;
  --ease:      cubic-bezier(0.16,1,0.3,1);
  --spring:    cubic-bezier(0.34,1.56,0.64,1);
}
[data-theme="light"] {
  --bg:        #f2f1ea;
  --bg2:       #e8e7df;
  --bg3:       #dddcd3;
  --surf:      #ffffff;
  --surf2:     #f2f1e9;
  --border:    rgba(0,0,0,0.065);
  --border2:   rgba(0,0,0,0.11);
  --border3:   rgba(0,0,0,0.20);
  --t:         #111114;
  --t2:        #4a4a5c;
  --t3:        #909098;
  --t4:        #c4c4cc;
  --lime:      #5a7800;
  --lime2:     #496300;
  --lime3:     #384e00;
  --lime-d:    rgba(90,120,0,0.07);
  --lime-d2:   rgba(90,120,0,0.13);
  --lime-glow: rgba(90,120,0,0.12);
  --cream:     #111114;
}

/* ── Reset ── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{font-size:16px;scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:var(--sans);background:var(--bg);color:var(--t);line-height:1.6;
  -webkit-font-smoothing:antialiased;overflow-x:hidden;transition:background .45s ease,color .45s ease}
img,svg{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
button{cursor:pointer;border:none;background:none;font:inherit;color:inherit}
ul,ol{list-style:none}
input,select,textarea{font:inherit}

/* ── Grain overlay ── */
body::after{content:'';position:fixed;inset:0;pointer-events:none;z-index:9000;
  opacity:.32;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.04'/%3E%3C/svg%3E")}

/* ── Loader ── */
#sf-loader{position:fixed;inset:0;background:#080809;z-index:9999;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;
  transition:opacity .5s ease,visibility .5s ease}
#sf-loader.out{opacity:0;visibility:hidden;pointer-events:none}
.ld-svg{width:78px;height:78px}
.ld-arc{fill:none;stroke:#F4F4EE;stroke-width:5;stroke-linecap:square;
  stroke-dasharray:72;stroke-dashoffset:72;opacity:0;animation:ldArc .4s var(--ease) forwards}
.ld-arc:nth-child(1){animation-delay:.10s}
.ld-arc:nth-child(2){animation-delay:.22s}
.ld-arc:nth-child(3){animation-delay:.34s}
.ld-tick{opacity:0;animation:ldFade .15s ease .5s forwards}
.ld-bob{opacity:0;animation:ldDrop .55s var(--spring) .6s forwards}
@keyframes ldArc{to{stroke-dashoffset:0;opacity:1}}
@keyframes ldFade{to{opacity:1}}
@keyframes ldDrop{from{opacity:0;transform:translateY(-16px)}to{opacity:1;transform:none}}
.ld-name{font-family:var(--mono);font-size:.82rem;letter-spacing:.34em;text-transform:uppercase;
  color:#F4F4EE;opacity:0;transform:translateY(5px);animation:ldRise .4s ease 1.05s forwards}
.ld-tag{font-family:var(--mono);font-size:.58rem;letter-spacing:.18em;text-transform:uppercase;
  color:#4e4e60;opacity:0;animation:ldRise .35s ease 1.18s forwards}
@keyframes ldRise{to{opacity:1;transform:none}}

/* ── Scroll bar ── */
#sf-bar{position:fixed;top:0;left:0;width:0%;height:2px;background:var(--lime);
  z-index:9998;box-shadow:0 0 10px var(--lime-glow);transition:width .04s linear;pointer-events:none}

/* ── Custom cursor ── */
.sf-dot,.sf-ring{position:fixed;border-radius:50%;pointer-events:none;
  top:0;left:0;opacity:0;transition:opacity .3s ease;will-change:transform}
.sf-dot{width:6px;height:6px;background:var(--lime);margin:-3px 0 0 -3px;z-index:8999;
  transition:opacity .3s,width .15s,height .15s}
.sf-ring{width:34px;height:34px;border:1.5px solid rgba(184,239,27,.35);margin:-17px 0 0 -17px;z-index:8998;
  transition:opacity .3s,width .2s var(--ease),height .2s var(--ease),border-color .2s,background .2s}
.sf-dot.on,.sf-ring.on{opacity:1}
.sf-ring.hv{width:50px;height:50px;border-color:var(--lime);background:rgba(184,239,27,.04)}
.sf-dot.hv{width:4px;height:4px;opacity:.5}
@media(pointer:fine){body,a,button,.btn,input,select,textarea,label,.card,.svc-card,.blog-card,.price-card{cursor:none}}
@media(pointer:coarse){.sf-dot,.sf-ring{display:none}}

/* ── Nav ── */
.nav{position:fixed;top:0;left:0;right:0;height:var(--nav-h);z-index:500}
.nav-bg{position:absolute;inset:0;background:rgba(8,8,9,.84);
  backdrop-filter:blur(22px) saturate(160%);-webkit-backdrop-filter:blur(22px) saturate(160%);
  border-bottom:1px solid var(--border);transition:background .3s ease,box-shadow .3s ease}
[data-theme=light] .nav-bg{background:rgba(242,241,234,.9)}
.nav.scrolled .nav-bg{box-shadow:0 1px 30px rgba(0,0,0,.2)}
.nav-in{position:relative;z-index:1;max-width:var(--max);margin:0 auto;padding:0 var(--gtr);
  height:100%;display:flex;align-items:center;justify-content:space-between;gap:18px}
.nav-logo{display:flex;align-items:center;flex-shrink:0;transition:opacity .2s}
.nav-logo:hover{opacity:.85}
.nav-logo img{height:30px;width:auto;transition:transform .45s var(--spring)}
.nav-logo:hover img{transform:scale(1.04)}
.nav-links{display:flex;align-items:center;gap:2px}
.nav-links a{font-family:var(--mono);font-size:.7rem;letter-spacing:.07em;text-transform:uppercase;
  color:var(--t2);padding:6px 12px;border-radius:var(--r);transition:color .15s,background .15s}
.nav-links a:hover,.nav-links a.active{color:var(--t);background:var(--surf)}
.nav-cta{display:flex;align-items:center;gap:10px;flex-shrink:0}
.theme-btn{width:34px;height:34px;border-radius:50%;border:1px solid var(--border2);
  color:var(--t3);display:flex;align-items:center;justify-content:center;font-size:.84rem;
  transition:color .15s,border-color .15s,background .15s}
.theme-btn:hover{color:var(--lime);border-color:var(--lime-d2);background:var(--lime-d)}
.burger{display:none;flex-direction:column;justify-content:center;gap:5px;
  width:36px;height:36px;padding:0 8px;border:1px solid var(--border2);border-radius:var(--r);
  transition:border-color .15s}
.burger:hover{border-color:var(--border3)}
.burger span{width:100%;height:1.5px;background:var(--t2);border-radius:2px;display:block;
  transition:transform .3s var(--ease),opacity .2s ease}
.burger.open span:nth-child(1){transform:translateY(6.5px) rotate(45deg)}
.burger.open span:nth-child(2){opacity:0;transform:scaleX(0)}
.burger.open span:nth-child(3){transform:translateY(-6.5px) rotate(-45deg)}
.nav-mob{display:none;position:fixed;top:var(--nav-h);left:0;right:0;bottom:0;
  background:var(--bg2);border-top:1px solid var(--border);
  padding:24px var(--gtr) 40px;flex-direction:column;gap:0;
  overflow-y:auto;z-index:499;animation:mobSlide .28s var(--ease)}
.nav-mob.open{display:flex}
@keyframes mobSlide{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}
.nav-mob a{font-family:var(--mono);font-size:.88rem;letter-spacing:.05em;text-transform:uppercase;
  color:var(--t2);padding:16px 0;border-bottom:1px solid var(--border);transition:color .15s}
.nav-mob a:last-of-type{border-bottom:none}
.nav-mob a:hover{color:var(--t)}
.nav-mob .mob-cta{margin-top:28px}

/* ── Buttons ── */
.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 22px;border-radius:var(--r);
  font-family:var(--mono);font-size:.74rem;font-weight:500;letter-spacing:.07em;text-transform:uppercase;
  white-space:nowrap;flex-shrink:0;position:relative;overflow:hidden;
  transition:transform .45s var(--spring),box-shadow .2s ease,background .15s,border-color .15s,color .15s}
.btn::before{content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.13),transparent);
  transform:translateX(-100%);transition:transform .5s ease}
.btn:hover::before{transform:translateX(100%)}
.btn-p{background:var(--lime);color:#080809}
.btn-p:hover{background:var(--lime2);box-shadow:0 0 30px var(--lime-glow)}
[data-theme=light] .btn-p{color:#111114}
.btn-g{border:1px solid var(--border2);color:var(--t2)}
.btn-g:hover{border-color:var(--border3);color:var(--t);background:var(--surf)}
.btn-lg{padding:14px 28px;font-size:.78rem}
.btn-xl{padding:17px 34px;font-size:.82rem;border-radius:10px}

/* ── Layout ── */
.wrap{max-width:var(--max);margin:0 auto;padding:0 var(--gtr)}
.section{padding:var(--pad) 0}
.section-alt{background:var(--bg2)}

/* ── Eyebrow ── */
.eyebrow{display:inline-flex;align-items:center;gap:10px;font-family:var(--mono);
  font-size:.64rem;font-weight:500;letter-spacing:.18em;text-transform:uppercase;
  color:var(--lime);margin-bottom:18px}
.eyebrow::before{content:'';width:14px;height:1px;background:currentColor;flex-shrink:0}

/* ── Typography ── */
h1,h2,h3{font-family:var(--serif);line-height:1.1;letter-spacing:-.02em}
h4{font-family:var(--mono);line-height:1.4;letter-spacing:.02em}
h1{font-size:clamp(2.4rem,5.5vw,4.8rem)}
h2{font-size:clamp(1.85rem,3.5vw,3.1rem)}
h3{font-size:clamp(1.18rem,2vw,1.65rem)}
p{color:var(--t2);line-height:1.8}
em{font-style:italic;color:var(--lime)}

/* ── Cards ── */
.card{background:var(--surf);border:1px solid var(--border);border-radius:var(--r2);padding:30px;
  transition:border-color .2s,transform .3s var(--ease),box-shadow .3s ease}
.card:hover{border-color:var(--border2);transform:translateY(-3px);box-shadow:0 12px 40px rgba(0,0,0,.28)}

/* ── Tag ── */
.tag{display:inline-flex;align-items:center;padding:4px 11px;border-radius:100px;
  background:var(--lime-d);border:1px solid var(--lime-d2);
  font-family:var(--mono);font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;color:var(--lime)}

/* ── Divider ── */
.divider{border:none;border-top:1px solid var(--border)}

/* ── Pulse dot ── */
.dot-live{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--lime);
  position:relative;flex-shrink:0}
.dot-live::after{content:'';position:absolute;inset:-3px;border-radius:50%;
  background:var(--lime);opacity:.4;animation:dotPulse 1.9s ease-out infinite}
@keyframes dotPulse{0%{transform:scale(1);opacity:.4}75%,100%{transform:scale(2.5);opacity:0}}

/* ── Form elements ── */
.f-label{display:block;font-family:var(--mono);font-size:.67rem;letter-spacing:.1em;
  text-transform:uppercase;color:var(--t3);margin-bottom:8px}
.f-input,.f-select,.f-ta{width:100%;background:var(--bg3);border:1px solid var(--border2);
  border-radius:var(--r);padding:12px 16px;color:var(--t);font-size:.92rem;
  transition:border-color .15s,box-shadow .15s;-webkit-appearance:none;appearance:none}
.f-input::placeholder,.f-ta::placeholder{color:var(--t3)}
.f-input:focus,.f-select:focus,.f-ta:focus{outline:none;border-color:var(--lime);box-shadow:0 0 0 3px var(--lime-d2)}
.f-ta{resize:vertical;min-height:120px;line-height:1.6}
.f-group{margin-bottom:20px}

/* ── Reveal ── */
.reveal{opacity:0;transform:translateY(22px);
  transition:opacity .65s var(--ease),transform .65s var(--ease)}
.reveal.in{opacity:1;transform:none}
.d1{transition-delay:.07s}.d2{transition-delay:.14s}.d3{transition-delay:.21s}
.d4{transition-delay:.28s}.d5{transition-delay:.35s}

/* ── Page header ── */
.ph{padding:calc(var(--nav-h) + 80px) 0 80px;background:var(--bg2);
  border-bottom:1px solid var(--border);position:relative;overflow:hidden}
.ph::before{content:'';position:absolute;inset:0;pointer-events:none;
  background-image:linear-gradient(var(--border) 1px,transparent 1px),
    linear-gradient(90deg,var(--border) 1px,transparent 1px);
  background-size:54px 54px;
  mask-image:radial-gradient(ellipse 65% 100% at 8% 50%,black 10%,transparent 80%);
  -webkit-mask-image:radial-gradient(ellipse 65% 100% at 8% 50%,black 10%,transparent 80%)}
.ph>.wrap{position:relative;z-index:1}
.ph h1{max-width:700px;margin-bottom:20px}
.ph-lead{font-size:1.04rem;max-width:530px}

/* ── Footer ── */
.footer{background:var(--bg2);border-top:1px solid var(--border);padding:72px 0 44px}
.footer-grid{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:52px;margin-bottom:56px}
.footer-logo{height:26px;width:auto;margin-bottom:18px}
.footer-tagline{font-size:.88rem;max-width:248px;margin-bottom:22px}
.footer-contact{display:flex;flex-direction:column;gap:7px}
.footer-contact a,.footer-contact span{font-family:var(--mono);font-size:.76rem;color:var(--t2);transition:color .15s}
.footer-contact a:hover{color:var(--t)}
.footer-col h5{font-family:var(--mono);font-size:.62rem;font-weight:600;letter-spacing:.14em;
  text-transform:uppercase;color:var(--t3);margin-bottom:18px}
.footer-col ul{display:flex;flex-direction:column;gap:12px}
.footer-col a{font-size:.87rem;color:var(--t2);transition:color .15s}
.footer-col a:hover{color:var(--t)}
.footer-bottom{display:flex;align-items:center;justify-content:space-between;
  padding-top:30px;border-top:1px solid var(--border);gap:16px;flex-wrap:wrap}
.footer-copy{font-family:var(--mono);font-size:.69rem;color:var(--t3)}
.footer-badges{display:flex;align-items:center;gap:22px;flex-wrap:wrap}
.footer-badge{display:inline-flex;align-items:center;gap:7px;
  font-family:var(--mono);font-size:.66rem;color:var(--t3);letter-spacing:.04em}
.footer-badge-live{color:var(--lime)}

/* ── Hero ── */
.hero{min-height:100svh;display:flex;align-items:center;padding-top:var(--nav-h);
  position:relative;overflow:hidden}
.hero-grid{position:absolute;inset:0;pointer-events:none;
  background-image:linear-gradient(var(--border) 1px,transparent 1px),
    linear-gradient(90deg,var(--border) 1px,transparent 1px);
  background-size:58px 58px;
  mask-image:radial-gradient(ellipse 80% 85% at 58% 50%,black 25%,transparent 80%);
  -webkit-mask-image:radial-gradient(ellipse 80% 85% at 58% 50%,black 25%,transparent 80%)}
.hero-blobs{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.blob{position:absolute;border-radius:50%;filter:blur(90px);will-change:transform}
.blob1{width:660px;height:660px;top:-160px;right:-120px;
  background:radial-gradient(circle,rgba(184,239,27,.055),transparent 70%);
  animation:bf1 20s ease-in-out infinite alternate}
.blob2{width:460px;height:460px;bottom:-60px;left:-80px;
  background:radial-gradient(circle,rgba(100,160,255,.032),transparent 70%);
  animation:bf2 26s ease-in-out infinite alternate}
@keyframes bf1{0%{transform:translate(0,0)}100%{transform:translate(28px,-22px) scale(1.05)}}
@keyframes bf2{0%{transform:translate(0,0)}100%{transform:translate(-20px,16px)}}
.hero-inner{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center;
  padding:80px 0;position:relative;z-index:1;width:100%}
.hero-content{display:flex;flex-direction:column}
.hero-kicker{font-family:var(--mono);font-size:.76rem;letter-spacing:.12em;text-transform:uppercase;
  color:var(--lime);margin-bottom:20px;display:inline-flex;align-items:center;gap:10px}
.hero-kicker::before{content:'';width:16px;height:1px;background:currentColor;flex-shrink:0}
.hero h1{margin-bottom:22px}
.hero-body{font-size:1.07rem;max-width:460px;color:var(--t2);line-height:1.8;margin-bottom:34px}
.hero-ctas{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:14px}
.hero-nudge{font-family:var(--mono);font-size:.65rem;color:var(--t3);letter-spacing:.05em;
  display:flex;align-items:center;gap:8px;margin-bottom:42px}
.hero-stats{display:flex;align-items:center;gap:26px;padding-top:34px;
  border-top:1px solid var(--border);flex-wrap:wrap}
.stat-item{display:flex;flex-direction:column;gap:3px}
.stat-n{font-family:var(--mono);font-size:1.5rem;font-weight:600;color:var(--t);line-height:1}
.stat-l{font-family:var(--mono);font-size:.6rem;color:var(--t3);letter-spacing:.04em}
.stat-sep{width:1px;height:30px;background:var(--border2);flex-shrink:0}

/* ── Terminal card ── */
.hero-visual{display:flex;justify-content:center;align-items:center}
/* Clean score card replaces busy terminal */
.score-card{
  background:var(--surf);border:1px solid var(--border2);border-radius:20px;
  padding:40px 36px;width:100%;max-width:360px;
  box-shadow:0 32px 80px rgba(0,0,0,.45);
  position:relative;overflow:hidden;
}
.score-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--lime-d2),transparent);
}
.score-card__label{
  font-family:var(--mono);font-size:.68rem;letter-spacing:.12em;
  text-transform:uppercase;color:var(--t3);margin-bottom:28px;
  display:flex;align-items:center;gap:8px;
}
.score-card__label::before{content:'';width:20px;height:1px;background:var(--lime);opacity:.5}
.score-card__ring-wrap{
  display:flex;flex-direction:column;align-items:center;margin-bottom:32px;
  position:relative;
}
.t-ring-wrap{width:140px;height:140px;position:relative;flex-shrink:0}
.t-ring-svg{width:100%;height:100%}
.t-ring-track{fill:none;stroke:var(--border2);stroke-width:7}
.t-ring-fill{fill:none;stroke:var(--lime);stroke-width:7;stroke-linecap:round;
  stroke-dasharray:380;stroke-dashoffset:380;
  transform:rotate(-90deg);transform-origin:50% 50%;
  transition:stroke-dashoffset 1.4s cubic-bezier(.16,1,.3,1)}
.t-ring-over{position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:2px}
.t-score-val{font-family:var(--mono);font-size:2.8rem;font-weight:600;color:var(--t);line-height:1}
.t-score-den{font-family:var(--mono);font-size:.7rem;color:var(--t3)}
.score-card__title{
  font-family:var(--mono);font-size:.78rem;color:var(--t2);
  margin-top:12px;letter-spacing:.04em;
}
.score-card__divider{width:100%;height:1px;background:var(--border);margin-bottom:20px}
.score-card__checks{display:flex;flex-direction:column;gap:10px}
.score-check{
  display:flex;align-items:center;gap:12px;
  font-family:var(--mono);font-size:.72rem;
  padding:9px 12px;border-radius:8px;
  background:var(--bg2);border:1px solid var(--border);
  opacity:0;transform:translateX(8px);
  transition:opacity .35s ease,transform .35s ease;
}
.score-check.in{opacity:1;transform:none}
.sc-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.sc-dot--c{background:#ff7070}
.sc-dot--w{background:#ffc233}
.sc-dot--p{background:#3dd6c0}
.sc-text{color:var(--t2)}

/* ── Trust marquee ── */
.trust-bar{border-top:1px solid var(--border);border-bottom:1px solid var(--border);
  padding:14px 0;overflow:hidden;background:var(--bg2)}
.trust-track{display:flex;width:max-content;animation:marquee 28s linear infinite}
.trust-track:hover{animation-play-state:paused}
.trust-set{display:flex;gap:50px;padding-right:50px}
.trust-item{display:inline-flex;align-items:center;gap:10px;
  font-family:var(--mono);font-size:.73rem;color:var(--t2);white-space:nowrap}
.trust-item::before{content:'·';color:var(--t4)}
@keyframes marquee{from{transform:translateX(0)}to{transform:translateX(-50%)}}

/* ── Problem section ── */
.problem-grid{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:start}
.prob-stats{display:flex;flex-direction:column;gap:14px}
.stat-card{background:var(--surf);border:1px solid var(--border);border-left:3px solid var(--lime);
  border-radius:var(--r2);padding:22px 26px;transition:transform .25s var(--ease)}
.stat-card:hover{transform:translateX(5px)}
.stat-big{font-family:var(--mono);font-size:2.4rem;font-weight:300;color:var(--lime);
  display:block;margin-bottom:6px;line-height:1}
.stat-card p{font-size:.86rem}

/* ── Services grid ── */
.svc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.svc-card{background:var(--surf);border:1px solid var(--border);border-radius:var(--r2);
  padding:28px;display:flex;flex-direction:column;gap:10px;position:relative;overflow:hidden;
  transition:border-color .2s,transform .3s var(--ease),box-shadow .3s ease}
.svc-card::before{content:'';position:absolute;inset:0;opacity:0;
  background:linear-gradient(135deg,var(--lime-d) 0%,transparent 55%);transition:opacity .3s ease}
.svc-card:hover{border-color:var(--border2);transform:translateY(-4px);box-shadow:0 18px 52px rgba(0,0,0,.24)}
.svc-card:hover::before{opacity:1}
.svc-icon{font-size:1.5rem;margin-bottom:4px;position:relative}
.svc-card h3{font-family:var(--serif);font-size:1.2rem;position:relative}
.svc-card p{font-size:.86rem;flex:1;position:relative}
.svc-arrow{font-family:var(--mono);font-size:.7rem;color:var(--lime);margin-top:auto;
  position:relative;transition:letter-spacing .25s ease}
.svc-card:hover .svc-arrow{letter-spacing:.09em}
.svc-card-cta{border-color:var(--lime-d2);background:var(--lime-d)}
.svc-card-cta::before{display:none}

/* ── Process ── */
.proc-grid{display:grid;grid-template-columns:repeat(3,1fr);
  border:1px solid var(--border);border-radius:var(--r2);overflow:hidden;gap:1px;background:var(--border)}
.proc-step{background:var(--surf);padding:36px 28px;display:flex;flex-direction:column;gap:12px;transition:background .2s}
.proc-step:hover{background:var(--surf2)}
.proc-n{font-family:var(--mono);font-size:3rem;font-weight:300;color:var(--lime);opacity:.4;line-height:1}
.proc-step h3{font-family:var(--serif);font-size:1.18rem}
.proc-step p{font-size:.86rem}

/* ── CTA block ── */
.cta-block{background:var(--surf);border:1px solid var(--border2);border-radius:20px;
  padding:clamp(52px,8vw,92px);text-align:center;position:relative;overflow:hidden}
.cta-glow{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:480px;height:320px;border-radius:50%;
  background:radial-gradient(ellipse,var(--lime-d) 0%,transparent 70%);
  pointer-events:none;animation:glowP 4s ease-in-out infinite alternate}
@keyframes glowP{0%{opacity:.7;transform:translate(-50%,-50%) scale(.9)}100%{opacity:1;transform:translate(-50%,-50%) scale(1.1)}}
.cta-block>*{position:relative;z-index:1}
.cta-block h2{margin-bottom:16px}
.cta-block>p{max-width:460px;margin:0 auto 34px}
.cta-btns{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.cta-fine{font-family:var(--mono);font-size:.64rem;color:var(--t3);margin-top:16px}

/* ── Services detail ── */
.svc-detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:start}
.svc-detail-grid.rev{direction:rtl}.svc-detail-grid.rev>*{direction:ltr}
.svc-detail-icon{font-size:2.2rem;margin-bottom:8px}
.svc-detail-content h2{margin:14px 0 18px}
.svc-detail-content>p{margin-bottom:26px}
.svc-aside{position:sticky;top:calc(var(--nav-h) + 24px)}
.aside-box{background:var(--surf);border:1px solid var(--border);border-radius:var(--r2);padding:24px;margin-bottom:14px}
.aside-box h4{font-family:var(--mono);font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;color:var(--t3);margin-bottom:14px}
.checklist{display:flex;flex-direction:column}
.check-row{display:flex;align-items:center;gap:12px;padding:9px 0;
  border-bottom:1px solid var(--border);font-size:.88rem;color:var(--t2)}
.check-row:last-child{border-bottom:none}
.chk{width:20px;height:20px;border-radius:50%;flex-shrink:0;background:var(--lime-d);
  display:flex;align-items:center;justify-content:center;font-size:.6rem;color:var(--lime)}
.finding{display:flex;align-items:center;gap:10px;padding:9px 0;
  font-size:.83rem;color:var(--t2);border-bottom:1px solid var(--border);font-family:var(--mono)}
.finding:last-child{border-bottom:none}
.rank-row{display:grid;grid-template-columns:1fr 80px auto;align-items:center;
  gap:10px;padding:8px 0;border-bottom:1px solid var(--border)}
.rank-row:last-child{border-bottom:none}
.rank-lbl{font-size:.79rem;color:var(--t2);font-family:var(--mono)}
.rank-bar{height:3px;background:var(--border2);border-radius:2px;overflow:hidden}
.rank-fill{height:100%;background:var(--lime);border-radius:2px}
.rank-pct{font-family:var(--mono);font-size:.67rem;color:var(--lime);text-align:right}
.metric-row{display:grid;grid-template-columns:52px 1fr auto;align-items:center;
  gap:14px;padding:13px 0;border-bottom:1px solid var(--border)}
.metric-row:last-child{border-bottom:none}
.metric-k{font-family:var(--mono);font-size:.9rem;font-weight:600;color:var(--lime)}
.metric-v{font-size:.82rem;color:var(--t2)}
.metric-t{font-family:var(--mono);font-size:.67rem;color:var(--t3);white-space:nowrap}
.impact-row{display:flex;align-items:baseline;gap:12px;padding:10px 0;
  border-bottom:1px solid var(--border);font-size:.83rem;color:var(--t2)}
.impact-row:last-child{border-bottom:none}
.impact-n{font-family:var(--mono);font-size:1.4rem;font-weight:600;color:var(--lime);flex-shrink:0}

/* ── Pricing ── */
.pricing-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;align-items:start}
.price-card{background:var(--surf);border:1px solid var(--border);border-radius:var(--r2);
  padding:34px;display:flex;flex-direction:column}
.price-card-feat{border-color:var(--lime);position:relative}
.price-card-feat::before{content:'Most Popular';position:absolute;top:-12px;left:50%;transform:translateX(-50%);
  background:var(--lime);color:#080809;font-family:var(--mono);font-size:.61rem;font-weight:700;
  letter-spacing:.1em;padding:4px 14px;border-radius:100px;text-transform:uppercase;white-space:nowrap}
[data-theme=light] .price-card-feat::before{color:#111114}
.price-tier{font-family:var(--mono);font-size:.67rem;letter-spacing:.1em;text-transform:uppercase;color:var(--t3);margin-bottom:10px}
.price-val{font-family:var(--serif);font-size:2.8rem;color:var(--t);line-height:1;margin-bottom:6px}
.price-val span{font-family:var(--mono);font-size:.95rem;color:var(--t3)}
.price-desc{font-size:.87rem;margin-bottom:22px;border-bottom:1px solid var(--border);padding-bottom:22px}
.price-feats{display:flex;flex-direction:column;gap:10px;margin-bottom:28px;flex:1}
.price-feat{display:flex;align-items:flex-start;gap:10px;font-size:.85rem;color:var(--t2)}
.price-feat::before{content:'✓';color:var(--lime);flex-shrink:0;margin-top:1px}
.faq-list{display:flex;flex-direction:column;gap:1px}
.faq-item{background:var(--surf);border:1px solid var(--border);border-radius:var(--r);overflow:hidden}
.faq-item summary{padding:18px 22px;list-style:none;display:flex;justify-content:space-between;
  align-items:center;user-select:none;font-size:.92rem;font-weight:500}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary::after{content:'+';color:var(--lime);font-size:1.15rem;flex-shrink:0}
.faq-item[open] summary::after{content:'−'}
.faq-item p{padding:0 22px 18px;font-size:.9rem}

/* ── Audit page ── */
.audit-wrap{max-width:660px;margin:0 auto}
.audit-card{background:var(--surf);border:1px solid var(--border);border-radius:var(--r2);
  padding:clamp(28px,5vw,50px);position:relative;overflow:hidden}
.audit-card::before{content:'';position:absolute;top:-60px;right:-60px;width:200px;height:200px;
  border-radius:50%;background:radial-gradient(circle,var(--lime-d2),transparent 70%);pointer-events:none}
.audit-checks{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:22px 0}
.audit-check{display:flex;align-items:center;gap:8px;
  font-family:var(--mono);font-size:.74rem;color:var(--t2)}
.audit-check::before{content:'✓';color:var(--lime);font-size:.67rem}
.prog-wrap{height:4px;background:var(--border2);border-radius:2px;overflow:hidden;margin:18px 0}
.prog-fill{height:100%;background:var(--lime);border-radius:2px;width:0%;
  transition:width .4s ease;box-shadow:0 0 8px var(--lime-glow)}
.prog-step{font-family:var(--mono);font-size:.74rem;color:var(--t2);margin-bottom:7px;padding-left:2px}
.prog-step.done{color:var(--lime)}
.prog-step.cur{color:var(--t)}
.res-score{font-family:var(--mono);font-size:5rem;font-weight:600;color:var(--lime);line-height:1}
.res-issue{display:flex;align-items:flex-start;gap:12px;
  padding:13px 0;border-bottom:1px solid var(--border);font-size:.88rem}
.res-issue:last-child{border-bottom:none}
.ri-badge{padding:2px 8px;border-radius:4px;font-family:var(--mono);font-size:.61rem;
  font-weight:700;flex-shrink:0;margin-top:2px}
.ri-c{background:rgba(255,80,80,.14);color:#ff7070}
.ri-w{background:rgba(255,180,0,.14);color:#ffc233}
.ri-i{background:rgba(60,180,255,.12);color:#60b4ff}
.upsell-box{margin-top:26px;padding:22px;border-radius:var(--r2);
  background:var(--lime-d);border:1px solid var(--lime-d2)}

/* ── Calculator ── */
.calc-grid{display:grid;grid-template-columns:1.1fr 1fr;gap:32px;max-width:980px;margin:0 auto}
.calc-card{background:var(--surf);border:1px solid var(--border);border-radius:var(--r2);padding:32px}
.calc-group{margin-bottom:24px}
.calc-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.calc-lbl{font-family:var(--mono);font-size:.67rem;letter-spacing:.1em;text-transform:uppercase;color:var(--t3)}
.calc-val{font-family:var(--mono);font-size:.8rem;font-weight:600;color:var(--lime)}
.range{-webkit-appearance:none;appearance:none;width:100%;height:3px;
  background:var(--border2);border-radius:2px;outline:none}
.range::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;
  border-radius:50%;background:var(--lime);box-shadow:0 0 0 3px var(--lime-d2)}
.res-num{font-family:var(--serif);font-size:3.5rem;color:var(--lime);line-height:1}
.calc-res-row{display:flex;justify-content:space-between;align-items:center;
  padding:12px 0;border-bottom:1px solid var(--border);font-size:.87rem}
.calc-res-row:last-of-type{border-bottom:none}
.calc-res-row span:last-child{font-family:var(--mono);font-weight:600}
.calc-res-row.hi span:last-child{color:var(--lime);font-size:1.05rem}

/* ── Case studies ── */
.cs-card{background:var(--surf);border:1px solid var(--border);border-radius:var(--r2);
  padding:32px;margin-bottom:18px;display:grid;
  grid-template-columns:1fr 1fr;gap:32px;align-items:start;transition:border-color .2s}
.cs-card:hover{border-color:var(--border2)}
.cs-ind{font-family:var(--mono);font-size:.65rem;letter-spacing:.1em;text-transform:uppercase;color:var(--t3);margin-bottom:8px}
.cs-title{font-family:var(--serif);font-size:1.28rem;margin-bottom:10px}
.cs-results{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.cs-result{text-align:center;background:var(--lime-d);border:1px solid var(--lime-d2);
  border-radius:var(--r2);padding:20px 16px;min-width:0;overflow:hidden}
.cs-num{font-family:var(--mono);font-size:1.75rem;font-weight:600;color:var(--lime);
  display:block;line-height:1;word-break:break-all}
.cs-lbl{font-size:.74rem;color:var(--t2);margin-top:4px;line-height:1.3}

/* ── Process timeline ── */
.timeline{position:relative;padding-left:46px;max-width:820px}
.timeline::before{content:'';position:absolute;left:13px;top:4px;bottom:0;width:1px;background:var(--border2)}
.tl-item{position:relative;margin-bottom:50px}
.tl-dot{position:absolute;left:-40px;top:4px;width:27px;height:27px;border-radius:50%;
  background:var(--surf);border:1px solid var(--border2);display:flex;align-items:center;
  justify-content:center;font-family:var(--mono);font-size:.61rem;color:var(--lime);font-weight:600}
.tl-item h3{font-family:var(--serif);font-size:1.26rem;margin-bottom:9px}
.tl-item p{font-size:.9rem;max-width:580px}

/* ── About ── */
.about-grid{display:grid;grid-template-columns:1fr 1.3fr;gap:80px;align-items:start}
.about-photo{background:var(--surf);border:1px solid var(--border);border-radius:var(--r2);
  aspect-ratio:3/4;display:flex;align-items:center;justify-content:center;
  font-size:5rem;color:var(--t3);position:relative;overflow:hidden}
.about-cap{position:absolute;bottom:0;left:0;right:0;
  background:linear-gradient(transparent,rgba(8,8,9,.8));padding:26px 22px 18px}
.about-cap-name{font-family:var(--mono);font-size:.83rem;color:var(--t)}
.about-cap-role{font-family:var(--mono);font-size:.69rem;color:var(--t3);margin-top:2px}

/* ── Blog ── */
.blog-feat{display:grid;grid-template-columns:1fr 1.5fr;background:var(--surf);
  border:1px solid var(--border);border-radius:var(--r2);overflow:hidden;margin-bottom:36px;
  transition:border-color .2s}
.blog-feat:hover{border-color:var(--border2)}
.blog-feat-img{background:var(--surf2);display:flex;align-items:center;justify-content:center;
  font-size:3.5rem;border-right:1px solid var(--border)}
.blog-feat-body{padding:34px;display:flex;flex-direction:column;gap:12px}
.blog-date{font-family:var(--mono);font-size:.67rem;color:var(--t3)}
.blog-feat h2{font-family:var(--serif);font-size:1.65rem;line-height:1.2}
.blog-feat p{font-size:.9rem;flex:1}
.blog-arrow{font-family:var(--mono);font-size:.72rem;color:var(--lime);margin-top:auto}
.blog-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.blog-card{background:var(--surf);border:1px solid var(--border);border-radius:var(--r2);
  overflow:hidden;display:flex;flex-direction:column;
  transition:border-color .2s,transform .3s var(--ease)}
.blog-card:hover{border-color:var(--border2);transform:translateY(-3px)}
.blog-card-img{height:155px;background:var(--surf2);display:flex;align-items:center;
  justify-content:center;font-size:2.2rem;border-bottom:1px solid var(--border)}
.blog-card-body{padding:22px;flex:1;display:flex;flex-direction:column;gap:8px}
.blog-card h3{font-family:var(--serif);font-size:1.08rem;line-height:1.3}
.blog-card p{font-size:.83rem;flex:1}
.blog-card .blog-arrow{margin-top:8px}

/* ── Contact ── */
.contact-grid{display:grid;grid-template-columns:1fr 1.4fr;gap:80px;align-items:start}
.info-items{display:flex;flex-direction:column;gap:14px}
.info-item{background:var(--surf);border:1px solid var(--border);border-radius:var(--r2);
  padding:20px;display:flex;align-items:center;gap:16px;transition:border-color .2s}
.info-item:hover{border-color:var(--border2)}
.info-icon{font-size:1.25rem;flex-shrink:0}
.info-label{font-family:var(--mono);font-size:.64rem;letter-spacing:.1em;text-transform:uppercase;color:var(--t3);margin-bottom:3px}
.info-val{font-size:.94rem;color:var(--t)}
.contact-form-card{background:var(--surf);border:1px solid var(--border);border-radius:var(--r2);padding:36px}
.success-msg{display:none;margin-top:18px;padding:18px;border-radius:var(--r);
  background:var(--lime-d);border:1px solid var(--lime-d2);text-align:center}
.success-msg.show{display:block}

/* ── 404 ── */
.nf-wrap{min-height:100svh;display:flex;align-items:center;justify-content:center;
  text-align:center;padding:var(--nav-h) var(--gtr) 80px}
.nf-num{font-family:var(--mono);font-size:clamp(6rem,18vw,13rem);font-weight:300;
  color:var(--border2);line-height:1;display:block;margin-bottom:8px}
.nf-wrap h1{font-size:clamp(1.8rem,4vw,2.8rem);margin-bottom:16px}
.nf-btns{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:36px}

/* ── Responsive ── */
@media(max-width:1040px){.svc-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:860px){
  .nav-links{display:none}.burger{display:flex}
  .footer-grid{grid-template-columns:1fr 1fr;gap:36px}
  .hero-inner{grid-template-columns:1fr;text-align:center;padding:52px 0}
  .hero-body{margin-left:auto;margin-right:auto}
  .hero-kicker,.hero-stats,.hero-ctas,.hero-nudge,.eyebrow{justify-content:center}
  .hero-visual{order:-1}
  .terminal{max-width:360px;margin:0 auto}
  .problem-grid{grid-template-columns:1fr;gap:48px}
  .proc-grid{grid-template-columns:1fr}
  .svc-detail-grid{grid-template-columns:1fr;gap:40px}
  .svc-detail-grid.rev{direction:ltr}
  .svc-aside{position:static}
  .pricing-grid{grid-template-columns:1fr}
  .price-card-feat{transform:none}
  .cs-card{grid-template-columns:1fr;gap:22px}
  .cs-results{grid-template-columns:1fr 1fr}
  .cs-result{text-align:center}
  .about-grid{grid-template-columns:1fr}
  .contact-grid{grid-template-columns:1fr}
  .blog-feat{grid-template-columns:1fr}
  .blog-feat-img{height:150px;border-right:none;border-bottom:1px solid var(--border)}
  .calc-grid{grid-template-columns:1fr}
}
@media(max-width:680px){.blog-grid{grid-template-columns:1fr 1fr}}
@media(max-width:560px){
  .svc-grid{grid-template-columns:1fr}
  .blog-grid{grid-template-columns:1fr}
  .footer-grid{grid-template-columns:1fr}
  .footer-bottom{flex-direction:column;align-items:flex-start}
  .hero-stats{flex-wrap:wrap;justify-content:center}
  .stat-sep{display:none}
  .audit-checks{grid-template-columns:1fr}
  .metric-row{grid-template-columns:46px 1fr}
  .metric-t{display:none}
}
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}
}
'''

JS_APP = r'''/* ═══════════════════════════════════════════════
   SytFix — app.js
   ═══════════════════════════════════════════════ */
(function(){
'use strict';

/* ── Theme ── */
var TK='sf-theme';
var pref=localStorage.getItem(TK)||(window.matchMedia('(prefers-color-scheme:light)').matches?'light':'dark');
function applyTheme(t){
  document.documentElement.setAttribute('data-theme',t);
  localStorage.setItem(TK,t);
  document.querySelectorAll('.theme-btn').forEach(function(b){
    b.textContent=t==='dark'?'☀':'☾';
    b.setAttribute('aria-label','Switch to '+(t==='dark'?'light':'dark')+' mode');
  });
}
applyTheme(pref);
document.addEventListener('click',function(e){
  if(e.target.closest('.theme-btn')){
    applyTheme(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark');
  }
});

/* ── Loader ── */
function initLoader(){
  var loader=document.getElementById('sf-loader');
  if(!loader)return;
  if(sessionStorage.getItem('sf-seen')){loader.style.display='none';document.body.style.overflow='';fireReady();return;}
  document.body.style.overflow='hidden';
  function dismiss(){
    loader.classList.add('out');
    document.body.style.overflow='';
    sessionStorage.setItem('sf-seen','1');
    setTimeout(fireReady,80);
    loader.removeEventListener('click',dismiss);
  }
  setTimeout(dismiss,2100);
  loader.addEventListener('click',dismiss);
}
function fireReady(){document.dispatchEvent(new Event('sf:ready'));}

/* ── Cursor ── */
function initCursor(){
  if(!window.matchMedia('(pointer:fine)').matches)return;
  var dot=document.createElement('div');var ring=document.createElement('div');
  dot.className='sf-dot';ring.className='sf-ring';
  document.body.appendChild(dot);document.body.appendChild(ring);
  var mx=-100,my=-100,rx=-100,ry=-100,first=false;
  document.addEventListener('mousemove',function(e){
    mx=e.clientX;my=e.clientY;
    dot.style.transform='translate('+mx+'px,'+my+'px)';
    if(!first){first=true;dot.classList.add('on');ring.classList.add('on');}
  });
  (function lerp(){
    rx+=(mx-rx)*0.11;ry+=(my-ry)*0.11;
    ring.style.transform='translate('+rx+'px,'+ry+'px)';
    requestAnimationFrame(lerp);
  })();
  var HV='a,button,.btn,input,select,textarea,.svc-card,.card,.blog-card,.price-card,.cs-card,.stat-card,.score-card';
  document.addEventListener('mouseover',function(e){if(e.target.closest(HV)){dot.classList.add('hv');ring.classList.add('hv');}});
  document.addEventListener('mouseout',function(e){if(e.target.closest(HV)){dot.classList.remove('hv');ring.classList.remove('hv');}});
  document.addEventListener('mouseleave',function(){dot.classList.remove('on');ring.classList.remove('on');});
  document.addEventListener('mouseenter',function(){if(first){dot.classList.add('on');ring.classList.add('on');}});
}

/* ── Scroll progress ── */
function initProgress(){
  var bar=document.getElementById('sf-bar');
  if(!bar)return;
  window.addEventListener('scroll',function(){
    var tot=document.documentElement.scrollHeight-window.innerHeight;
    bar.style.width=(tot>0?(window.scrollY/tot)*100:0)+'%';
  },{passive:true});
}

/* ── Nav ── */
function initNav(){
  var nav=document.querySelector('.nav');
  var burger=document.querySelector('.burger');
  var mob=document.querySelector('.nav-mob');
  if(!nav)return;
  window.addEventListener('scroll',function(){
    nav.classList.toggle('scrolled',window.scrollY>20);
  },{passive:true});
  if(burger&&mob){
    burger.addEventListener('click',function(){
      var open=mob.classList.toggle('open');
      burger.classList.toggle('open',open);
      burger.setAttribute('aria-expanded',open);
      document.body.style.overflow=open?'hidden':'';
    });
    mob.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click',function(){
        mob.classList.remove('open');burger.classList.remove('open');
        document.body.style.overflow='';
      });
    });
  }
  var page=window.location.pathname.split('/').pop()||'index.html';
  document.querySelectorAll('.nav-links a,.nav-mob a').forEach(function(a){
    if((a.getAttribute('href')||'').split('/').pop()===page)a.classList.add('active');
  });
}

/* ── Scramble ── */
var SC='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%&';
function scramble(el,dur){
  if(!el)return;
  var tgt=el.getAttribute('data-text')||el.textContent;
  var chars=tgt.split('');dur=dur||950;
  var revAt=chars.map(function(_,i){return(i/chars.length)*dur*.65+Math.random()*dur*.35;});
  var st=null;
  function frame(ts){
    if(!st)st=ts;var el2=el;
    var elapsed=ts-st;
    el2.textContent=chars.map(function(ch,i){
      if(ch===' ')return ' ';
      if(elapsed>=revAt[i])return ch;
      return SC[Math.floor(Math.random()*SC.length)];
    }).join('');
    if(elapsed<dur)requestAnimationFrame(frame);else el2.textContent=tgt;
  }
  requestAnimationFrame(frame);
}

/* ── Counter ── */
function animCount(el){
  var tgt=parseFloat(el.dataset.target||el.textContent);
  var suf=el.dataset.suffix||'';var pre=el.dataset.prefix||'';
  var dur=parseInt(el.dataset.dur)||1500;var dec=el.dataset.dec==='1';
  var st=null;
  function frame(ts){
    if(!st)st=ts;
    var p=Math.min((ts-st)/dur,1);
    var ease=1-Math.pow(1-p,3);
    var v=tgt*ease;
    el.textContent=pre+(dec?v.toFixed(1):Math.round(v))+suf;
    if(p<1)requestAnimationFrame(frame);else el.textContent=pre+tgt+suf;
  }
  requestAnimationFrame(frame);
}

/* ── Magnetic ── */
function initMagnetic(){
  document.querySelectorAll('.btn-p.btn-xl,.btn-p.btn-lg').forEach(function(btn){
    btn.addEventListener('mousemove',function(e){
      var r=btn.getBoundingClientRect();
      btn.style.transform='translate('+(e.clientX-r.left-r.width/2)*.26+'px,'+(e.clientY-r.top-r.height/2)*.26+'px)';
    });
    btn.addEventListener('mouseleave',function(){btn.style.transform='';});
  });
}

/* ── Score Card animation ── */
function initTerminal(){
  var card=document.querySelector('.score-card');if(!card)return;
  var fill=card.querySelector('.t-ring-fill');
  var scoreEl=card.querySelector('.t-score-val');
  var checks=card.querySelectorAll('.score-check');
  var tgt=72,ran=false;
  /* circumference for r=60.5: 2*PI*60.5 ≈ 380 */
  var CIRC=380;
  var obs=new IntersectionObserver(function(en){
    if(en[0].isIntersecting&&!ran){
      ran=true;obs.disconnect();
      setTimeout(function(){
        if(fill)fill.style.strokeDashoffset=CIRC-(tgt/100)*CIRC;
      },280);
      if(scoreEl){var s=0;var iv=setInterval(function(){s=Math.min(s+2,tgt);scoreEl.textContent=s;if(s>=tgt)clearInterval(iv);},38);}
      checks.forEach(function(row,i){setTimeout(function(){row.classList.add('in');},480+i*140);});
    }
  },{threshold:0.35});
  obs.observe(card);
}

/* ── Reveal ── */
function initReveal(){
  var obs=new IntersectionObserver(function(en){
    en.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');obs.unobserve(e.target);}});
  },{threshold:0.09});
  document.querySelectorAll('.reveal').forEach(function(el){obs.observe(el);});
  var cObs=new IntersectionObserver(function(en){
    en.forEach(function(e){if(e.isIntersecting){animCount(e.target);cObs.unobserve(e.target);}});
  },{threshold:0.5});
  document.querySelectorAll('[data-counter]').forEach(function(el){cObs.observe(el);});
}

/* ── Parallax ── */
function initParallax(){
  var g=document.querySelector('.hero-grid');if(!g)return;
  window.addEventListener('scroll',function(){g.style.transform='translateY('+(window.scrollY*.08)+'px)';},{passive:true});
}

/* ── Calculator ── */
function initCalc(){
  var wrap=document.querySelector('.calc-grid');if(!wrap)return;
  function fmt(n){if(n>=1e6)return'$'+(n/1e6).toFixed(1)+'M';if(n>=1e3)return'$'+Math.round(n/1e3)+'K';return'$'+Math.round(n).toLocaleString();}
  function upd(){
    var vis=+document.getElementById('r-vis').value;
    var conv=+document.getElementById('r-conv').value/100;
    var val=+document.getElementById('r-val').value;
    var cls=+document.getElementById('r-cls').value/100;
    var tup=+document.getElementById('r-tup').value/100;
    var cup=+document.getElementById('r-cup').value/100;
    document.getElementById('v-vis').textContent=vis.toLocaleString();
    document.getElementById('v-conv').textContent=(conv*100).toFixed(1)+'%';
    document.getElementById('v-val').textContent='$'+val.toLocaleString();
    document.getElementById('v-cls').textContent=Math.round(cls*100)+'%';
    document.getElementById('v-tup').textContent='+'+Math.round(tup*100)+'%';
    document.getElementById('v-cup').textContent='+'+(cup*100).toFixed(1)+'%';
    var cL=Math.round(vis*conv),cC=Math.round(cL*cls),cR=cC*val;
    document.getElementById('c-leads').textContent=cL;
    document.getElementById('c-clients').textContent=cC;
    document.getElementById('c-rev').textContent=fmt(cR);
    var nL=Math.round(vis*(1+tup)*(conv+cup)),nC=Math.round(nL*cls),nR=nC*val;
    document.getElementById('n-leads').textContent=nL;
    document.getElementById('n-clients').textContent=nC;
    document.getElementById('n-rev').textContent=fmt(nR);
    document.getElementById('annual-gain').textContent=fmt((nR-cR)*12);
  }
  document.querySelectorAll('.range').forEach(function(r){r.addEventListener('input',upd);});
  upd();
}

/* ── Audit ── */
function initAudit(){
  var btn=document.getElementById('audit-start');if(!btn)return;
  btn.addEventListener('click',function(){
    var url=(document.getElementById('audit-url')||{}).value||'';
    if(!url){alert('Please enter your website URL.');return;}
    document.getElementById('audit-form').style.display='none';
    document.getElementById('audit-prog').style.display='block';
    var LABELS=['Crawlability & indexation','Core Web Vitals','Local SEO signals','Schema markup','AI visibility','Generating report'];
    var PCTS=[14,30,48,64,80,100];
    var fill=document.getElementById('prog-fill');
    var stepsEl=document.getElementById('prog-steps');
    var i=0;
    function adv(){
      if(i>0){var p=stepsEl.querySelector('[data-s="'+(i-1)+'"]');if(p){p.className='prog-step done';p.textContent='✓ '+LABELS[i-1];}}
      if(i<LABELS.length){
        var c=stepsEl.querySelector('[data-s="'+i+'"]');
        if(c){c.className='prog-step cur';c.textContent='▶ '+LABELS[i]+'...';}
        if(fill)fill.style.width=PCTS[i]+'%';
        i++;setTimeout(adv,600+Math.random()*480);
      }else{setTimeout(showResult,380);}
    }
    adv();
  });
  function showResult(){
    document.getElementById('audit-prog').style.display='none';
    var res=document.getElementById('audit-result');if(!res)return;
    res.style.display='block';
    var score=Math.floor(Math.random()*22)+56;
    document.getElementById('res-score').textContent=score;
    var issues=[
      {s:'c',t:'No LocalBusiness schema markup found',d:'Search engines and AI platforms cannot verify your business category, hours, or service area.'},
      {s:'c',t:'LCP: 4.9s — Google threshold exceeded (2.5s)',d:'Your main content loads too slowly. This is a direct ranking penalty and causes visitor bounce.'},
      {s:'w',t:'Google Business Profile missing 4 required fields',d:'Incomplete GBP profiles rank lower in the local map pack than competitors who fill them out.'},
      {s:'w',t:'NAP inconsistency across 12 directories',d:'Name, Address, Phone mismatches reduce local trust signals and confuse search engines.'},
      {s:'w',t:'Not cited in ChatGPT, Perplexity, or Google AI Overviews',d:'AI search is now a primary discovery channel for local services. You are currently invisible.'},
      {s:'i',t:'3 service pages share duplicate title tags',d:'Duplicate titles cause keyword cannibalization and reduce individual page authority.'},
    ];
    var ctr=document.getElementById('res-issues');
    if(ctr)ctr.innerHTML=issues.map(function(iss){
      var cls=iss.s==='c'?'ri-c':iss.s==='w'?'ri-w':'ri-i';
      var lbl=iss.s==='c'?'Critical':iss.s==='w'?'Warning':'Info';
      return'<div class="res-issue"><span class="ri-badge '+cls+'">'+lbl+'</span><div><strong style="font-size:.88rem;color:var(--t)">'+iss.t+'</strong><p style="font-size:.82rem;margin-top:3px">'+iss.d+'</p></div></div>';
    }).join('');
    res.scrollIntoView({behavior:'smooth',block:'start'});
  }
}

/* ── Contact ── */
function initContact(){
  var btn=document.getElementById('contact-btn');if(!btn)return;
  btn.addEventListener('click',function(){
    var name=(document.getElementById('c-name')||{}).value||'';
    var email=(document.getElementById('c-email')||{}).value||'';
    if(!name||!email){alert('Please enter your name and email.');return;}
    btn.textContent='Sending…';btn.disabled=true;
    setTimeout(function(){
      btn.style.display='none';
      var msg=document.getElementById('contact-success');
      if(msg)msg.classList.add('show');
    },1100);
  });
}

/* ── Boot ── */
function boot(){
  initLoader();initCursor();initProgress();initNav();
  initReveal();initTerminal();initParallax();
  initCalc();initAudit();initContact();initMagnetic();
  function doScramble(){
    document.querySelectorAll('[data-scramble]').forEach(function(el){scramble(el,950);});
  }
  if(sessionStorage.getItem('sf-seen'))setTimeout(doScramble,200);
  else document.addEventListener('sf:ready',function(){setTimeout(doScramble,150);});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);
else boot();
})();
'''

# ─────────────────────────────────────────────────────────────────
# Shared HTML components
# ─────────────────────────────────────────────────────────────────
def loader_html():
    return '''<div id="sf-loader" aria-hidden="true">
  <svg class="ld-svg" viewBox="75 215 185 175" xmlns="http://www.w3.org/2000/svg">
    <g transform="translate(0,600) scale(0.1,-0.1)">
      <path class="ld-arc" fill="#F4F4EE" d="M1510 3680 l0 -40 45 0 45 0 0 40 0 40 -45 0 -45 0 0 -40z"/>
      <path class="ld-arc" fill="#F4F4EE" d="M1335 3686 c-131 -42 -212 -92 -315 -196 -79 -78 -104 -111 -142 -185 -45 -89 -78 -183 -78 -224 0 -18 6 -21 39 -21 37 0 39 2 46 38 19 106 118 277 204 355 86 78 199 139 309 167 41 10 42 12 42 50 0 48 -5 49 -105 16z"/>
      <path class="ld-arc" fill="#F4F4EE" d="M1682 3669 c3 -41 3 -42 57 -56 139 -35 300 -153 384 -281 47 -71 91 -172 102 -234 7 -37 8 -38 50 -38 l43 0 -13 58 c-62 263 -260 477 -527 568 -97 33 -100 32 -96 -17z"/>
      <rect class="ld-tick" fill="#F4F4EE" x="780" y="2820" width="45" height="40"/>
      <rect class="ld-tick" fill="#F4F4EE" x="2240" y="2821" width="45" height="39"/>
      <rect class="ld-tick" fill="#F4F4EE" x="1510" y="3840" width="45" height="40"/>
      <rect class="ld-tick" fill="#F4F4EE" x="1514" y="2186" width="42" height="46"/>
      <path class="ld-bob" fill="#B8EF1B" d="M1540 3266 l0 -296 -30 0 c-29 0 -30 -2 -30 -44 0 -39 -4 -46 -40 -71 l-40 -28 0 -128 0 -128 76 -108 c41 -59 78 -109 82 -110 4 -1 42 50 85 114 l77 116 0 121 0 121 -45 30 c-41 28 -45 33 -45 73 0 38 -2 42 -25 42 l-25 0 -2 292 c-3 270 -4 293 -20 296 -17 3 -18 -16 -18 -292z"/>
    </g>
  </svg>
  <p class="ld-name">SytFix</p>
  <p class="ld-tag">Web Auditing &amp; SEO</p>
</div>
<div id="sf-bar"></div>'''

def nav_html(active=''):
    pages = [
        ('services.html','Services'),('process.html','Process'),
        ('case-studies.html','Case Studies'),('pricing.html','Pricing'),
        ('blog.html','Blog'),('about.html','About'),
    ]
    links = '\n'.join(
        f'      <li><a href="{p}" class="{"active" if p==active else ""}">{l}</a></li>'
        for p,l in pages
    )
    mob_links = '\n'.join(
        f'  <a href="{p}">{l}</a>' for p,l in pages
    )
    return f'''<nav class="nav" role="navigation" aria-label="Main navigation">
  <div class="nav-bg"></div>
  <div class="nav-in">
    <a href="index.html" class="nav-logo" aria-label="SytFix home">
      <img src="img/logo.svg" alt="SytFix" class="nav-logo-img">
    </a>
    <ul class="nav-links" role="list">
{links}
    </ul>
    <div class="nav-cta">
      <button class="theme-btn" aria-label="Toggle theme">☀</button>
      <a href="audit.html" class="btn btn-p">Free Audit →</a>
      <button class="burger" aria-label="Open menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</nav>
<div class="nav-mob" role="menu">
{mob_links}
  <a href="contact.html">Contact</a>
  <div class="mob-cta">
    <a href="audit.html" class="btn btn-p btn-lg" style="width:100%;justify-content:center">Run Free Audit →</a>
  </div>
</div>'''

def footer_html():
    return '''<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <img src="img/logo.svg" alt="SytFix" class="footer-logo">
        <p class="footer-tagline">Precision web auditing and SEO for local service businesses. Transparent process, real results.</p>
        <div class="footer-contact">
          <span>R. "Alex" Mitchell IV</span>
          <a href="tel:2544476464">(254) 447-6464</a>
          <span style="font-size:.72rem;color:var(--t3)">Waco, TX — Serving Nationwide</span>
        </div>
      </div>
      <div class="footer-col">
        <h5>Services</h5>
        <ul>
          <li><a href="services.html#technical">Technical SEO</a></li>
          <li><a href="services.html#local">Local SEO</a></li>
          <li><a href="services.html#cwv">Core Web Vitals</a></li>
          <li><a href="services.html#ai">AI Visibility</a></li>
          <li><a href="services.html#content">Content Architecture</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Company</h5>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="process.html">Our Process</a></li>
          <li><a href="case-studies.html">Case Studies</a></li>
          <li><a href="blog.html">Blog</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Tools</h5>
        <ul>
          <li><a href="audit.html">Free Site Audit</a></li>
          <li><a href="calculator.html">Revenue Calculator</a></li>
          <li><a href="pricing.html">Pricing</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="footer-copy">© 2026 SytFix. All rights reserved. Built in Waco, TX.</p>
      <div class="footer-badges">
        <span class="footer-badge footer-badge-live"><span class="dot-live"></span> All systems operational</span>
        <span class="footer-badge">⚡ 98/100 Lighthouse</span>
      </div>
    </div>
  </div>
</footer>'''

def page(title, desc, body, active='', extra_css=''):
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<title>{title}</title>
<link rel="icon" href="img/icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="css/main.css">
{extra_css}
</head>
<body>
{loader_html()}
{nav_html(active)}
{body}
{footer_html()}
<script src="js/app.js"></script>
</body>
</html>'''

# ─────────────────────────────────────────────────────────────────
# Page content
# ─────────────────────────────────────────────────────────────────

def build_index():
    body = '''
<section class="hero" aria-label="Hero">
  <div class="hero-grid" aria-hidden="true"></div>
  <div class="hero-blobs" aria-hidden="true"><div class="blob blob1"></div><div class="blob blob2"></div></div>
  <div class="wrap">
    <div class="hero-inner">
      <div class="hero-content">
        <div class="hero-kicker reveal">Web Auditing &amp; SEO Optimization</div>
        <h1 class="reveal d1">Your site is losing<br><em data-scramble data-text="clients every day.">clients every day.</em></h1>
        <p class="hero-body reveal d2">SytFix finds the technical failures, ranking gaps, and AI visibility blind spots costing local service businesses clients — then maps every issue directly to lost revenue. No spreadsheets. No jargon. A clear fix roadmap.</p>
        <div class="hero-ctas reveal d3">
          <a href="audit.html" class="btn btn-p btn-xl">Run Free Audit →</a>
          <a href="calculator.html" class="btn btn-g btn-lg">Calculate My ROI</a>
        </div>
        <div class="hero-nudge reveal d3"><span class="dot-live"></span>No credit card &nbsp;·&nbsp; Takes 2 minutes &nbsp;·&nbsp; Real analysis</div>
        <div class="hero-stats reveal d4">
          <div class="stat-item">
            <span class="stat-n" data-counter data-target="200" data-suffix="+">200+</span>
            <span class="stat-l">audit checkpoints</span>
          </div>
          <div class="stat-sep" aria-hidden="true"></div>
          <div class="stat-item"><span class="stat-n">48hr</span><span class="stat-l">report delivery</span></div>
          <div class="stat-sep" aria-hidden="true"></div>
          <div class="stat-item"><span class="stat-n">6</span><span class="stat-l">industries served</span></div>
          <div class="stat-sep" aria-hidden="true"></div>
          <div class="stat-item">
            <span class="stat-n" data-counter data-target="100" data-suffix="%">100%</span>
            <span class="stat-l">founder-led</span>
          </div>
        </div>
      </div>
      <div class="hero-visual">
        <div class="score-card" role="img" aria-label="Example site audit score">
          <div class="score-card__label">Site Audit Score</div>
          <div class="score-card__ring-wrap">
            <div class="t-ring-wrap">
              <svg class="t-ring-svg" viewBox="0 0 140 140" aria-hidden="true">
                <circle class="t-ring-track" cx="70" cy="70" r="60.5"/>
                <circle class="t-ring-fill" cx="70" cy="70" r="60.5"/>
              </svg>
              <div class="t-ring-over">
                <span class="t-score-val">0</span>
                <span class="t-score-den">/ 100</span>
              </div>
            </div>
            <div class="score-card__title">yourbusiness.com</div>
          </div>
          <div class="score-card__divider"></div>
          <div class="score-card__checks">
            <div class="score-check"><span class="sc-dot sc-dot--c"></span><span class="sc-text">Missing schema markup</span></div>
            <div class="score-check"><span class="sc-dot sc-dot--c"></span><span class="sc-text">LCP 4.9s — too slow</span></div>
            <div class="score-check"><span class="sc-dot sc-dot--w"></span><span class="sc-text">Invisible in AI search</span></div>
            <div class="score-check"><span class="sc-dot sc-dot--p"></span><span class="sc-text">Mobile responsive ✓</span></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="trust-bar" aria-label="Industries served">
  <div class="trust-track" aria-hidden="true">
    <div class="trust-set">
      <span class="trust-item">Legal Practices</span><span class="trust-item">HVAC &amp; Roofing</span>
      <span class="trust-item">Plumbing &amp; Electrical</span><span class="trust-item">Dental &amp; Medical</span>
      <span class="trust-item">Damage Restoration</span><span class="trust-item">Specialty Contractors</span>
    </div>
    <div class="trust-set" aria-hidden="true">
      <span class="trust-item">Legal Practices</span><span class="trust-item">HVAC &amp; Roofing</span>
      <span class="trust-item">Plumbing &amp; Electrical</span><span class="trust-item">Dental &amp; Medical</span>
      <span class="trust-item">Damage Restoration</span><span class="trust-item">Specialty Contractors</span>
    </div>
  </div>
</div>

<section class="section">
  <div class="wrap">
    <div class="problem-grid">
      <div>
        <div class="eyebrow reveal">The Problem</div>
        <h2 class="reveal d1">Most service sites are<br><em>invisible and broken.</em></h2>
        <p class="reveal d2" style="margin:22px 0">You have a website — maybe a good one. But Google can't read half of it. It loads in 6 seconds on mobile. You're not in the local map pack. And in 2026, you're not cited in AI search results at all.</p>
        <p class="reveal d2">Free tools give you 200 flags with no context. SytFix connects every issue to revenue impact, explains it in plain language, and gives you a specific fix. You know exactly what to do and why.</p>
        <a href="audit.html" class="btn btn-p" style="margin-top:28px" class="reveal d3">Run Free Audit →</a>
      </div>
      <div class="prob-stats">
        <div class="stat-card reveal"><span class="stat-big" data-counter data-target="53" data-suffix="%">53%</span><p>of mobile visitors abandon a page that takes longer than 3 seconds — before seeing your offer.</p></div>
        <div class="stat-card reveal d1"><span class="stat-big" data-counter data-target="46" data-suffix="%">46%</span><p>of Google searches have local intent. Most service pages aren't optimized to capture any of it.</p></div>
        <div class="stat-card reveal d2"><span class="stat-big" data-counter data-target="76" data-suffix="%">76%</span><p>of people who find a local business online visit within 24 hours. Ranking lower costs real jobs.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="eyebrow reveal" style="justify-content:center">What We Audit</div>
    <h2 class="reveal d1" style="text-align:center;max-width:540px;margin:0 auto 48px">Five pillars that control<br><em>your online revenue.</em></h2>
    <div class="svc-grid">
      <a href="services.html#technical" class="svc-card reveal"><div class="svc-icon">⚙</div><h3>Technical SEO</h3><p>Crawlability, indexation, schema markup, site architecture — every barrier between your site and the front page.</p><span class="svc-arrow">Explore →</span></a>
      <a href="services.html#local" class="svc-card reveal d1"><div class="svc-icon">📍</div><h3>Local SEO</h3><p>GBP optimization, citation consistency, map pack analysis — built specifically for service businesses that win locally.</p><span class="svc-arrow">Explore →</span></a>
      <a href="services.html#cwv" class="svc-card reveal d2"><div class="svc-icon">⚡</div><h3>Core Web Vitals</h3><p>LCP, INP, CLS benchmarked against Google thresholds and your direct competitors. Impact-ranked fix plan included.</p><span class="svc-arrow">Explore →</span></a>
      <a href="services.html#ai" class="svc-card reveal d1"><div class="svc-icon">🤖</div><h3>AI Visibility</h3><p>Do you appear in ChatGPT, Perplexity, Google AI Overviews? We audit your AI footprint and build your strategy.</p><span class="svc-arrow">Explore →</span><span class="tag" style="margin-top:4px;width:fit-content">New 2026</span></a>
      <a href="services.html#content" class="svc-card reveal d2"><div class="svc-icon">📄</div><h3>Content Architecture</h3><p>Internal linking, keyword cannibalization, topical authority — the structural decisions that control how Google sees you.</p><span class="svc-arrow">Explore →</span></a>
      <a href="calculator.html" class="svc-card svc-card-cta reveal d3"><div class="svc-icon">📊</div><h3>Revenue Calculator</h3><p>Model the financial upside of better rankings before you spend a dollar. See exactly what visibility is worth.</p><a href="calculator.html" class="btn btn-p" style="margin-top:auto;width:fit-content">Calculate →</a></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="eyebrow reveal">How It Works</div>
    <h2 class="reveal d1" style="margin-bottom:48px">Audit to results<br><em>in three steps.</em></h2>
    <div class="proc-grid">
      <div class="proc-step reveal"><div class="proc-n">01</div><h3>Submit Your Site</h3><p>Enter your URL and industry. The automated scan starts immediately — 200+ technical and SEO checkpoints — while Alex queues a manual review specific to your market.</p></div>
      <div class="proc-step reveal d1"><div class="proc-n">02</div><h3>Receive Your Roadmap</h3><p>Within 48 hours you get a prioritized report — every issue ranked by revenue impact with plain-language fix instructions. No jargon. No spreadsheets. No guesswork.</p></div>
      <div class="proc-step reveal d2"><div class="proc-n">03</div><h3>Implement &amp; Grow</h3><p>Fix it yourself with our guide, or let us handle implementation. Either way you know exactly what to do and why — with measurable outcomes tracked at 60 days.</p></div>
    </div>
    <div style="text-align:center;margin-top:40px"><a href="process.html" class="btn btn-g reveal">See Full Process →</a></div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="cta-block reveal">
      <div class="cta-glow" aria-hidden="true"></div>
      <div class="eyebrow" style="justify-content:center">Start Today</div>
      <h2>Your competitors are<br><em>already optimizing.</em></h2>
      <p>Every week your site has unresolved technical issues, you lose rankings to businesses that fixed theirs. Get your free audit and see exactly what's at stake.</p>
      <div class="cta-btns">
        <a href="audit.html" class="btn btn-p btn-xl">Run Free Audit →</a>
        <a href="contact.html" class="btn btn-g btn-lg">Talk to Alex</a>
      </div>
      <p class="cta-fine">No credit card. No commitment. Delivered in 48 hours.</p>
    </div>
  </div>
</section>'''
    return page('SytFix | Precision Web Auditing & SEO',
        'SytFix finds what\'s breaking your site and costing you clients. Precision web audits and local SEO for service businesses.', body)


def build_services():
    body = '''
<header class="ph">
  <div class="wrap">
    <div class="eyebrow reveal">What We Do</div>
    <h1 class="reveal d1">Five audits.<br><em>One revenue goal.</em></h1>
    <p class="ph-lead reveal d2">Every SytFix audit connects technical findings directly to business outcomes. We don't grade your site — we tell you what it's costing you.</p>
  </div>
</header>

<section class="section" id="technical">
  <div class="wrap">
    <div class="svc-detail-grid">
      <div>
        <div class="svc-detail-icon">⚙</div>
        <div class="eyebrow reveal">Service 01</div>
        <h2 class="reveal d1">Technical SEO Audit</h2>
        <p class="reveal d2">The foundation every other optimization depends on. If search engines can't crawl and understand your site, no content or links will move the needle. We audit the complete technical stack.</p>
        <div class="checklist reveal d3">
          <div class="check-row"><div class="chk">✓</div>Crawlability &amp; indexation analysis</div>
          <div class="check-row"><div class="chk">✓</div>Site architecture &amp; URL structure</div>
          <div class="check-row"><div class="chk">✓</div>Structured data / schema markup</div>
          <div class="check-row"><div class="chk">✓</div>Internal linking graph analysis</div>
          <div class="check-row"><div class="chk">✓</div>Duplicate content detection</div>
          <div class="check-row"><div class="chk">✓</div>Robots.txt &amp; sitemap validation</div>
          <div class="check-row"><div class="chk">✓</div>Mobile usability assessment</div>
          <div class="check-row"><div class="chk">✓</div>HTTPS &amp; security headers</div>
        </div>
      </div>
      <div class="svc-aside reveal d2">
        <div class="aside-box">
          <h4>Common findings</h4>
          <div class="finding">🔴 Pages blocked by robots.txt</div>
          <div class="finding">🔴 No local business schema</div>
          <div class="finding">🟡 Duplicate title tags</div>
          <div class="finding">🟡 Orphaned service pages</div>
          <div class="finding">🔵 Missing canonical tags</div>
          <div class="finding">🔵 Redirect chains (3+ hops)</div>
        </div>
        <div class="aside-box">
          <p style="font-size:.88rem;margin-bottom:16px">See how technical issues translate to lost revenue.</p>
          <a href="audit.html" class="btn btn-p" style="width:100%;justify-content:center">Get Technical Audit →</a>
        </div>
      </div>
    </div>
  </div>
</section>
<hr class="divider">
<section class="section" id="local">
  <div class="wrap">
    <div class="svc-detail-grid rev">
      <div class="svc-aside reveal">
        <div class="aside-box">
          <h4>Local ranking factors</h4>
          <div class="rank-row"><span class="rank-lbl">GBP Signals</span><div class="rank-bar"><div class="rank-fill" style="width:36%"></div></div><span class="rank-pct">36%</span></div>
          <div class="rank-row"><span class="rank-lbl">Reviews</span><div class="rank-bar"><div class="rank-fill" style="width:17%"></div></div><span class="rank-pct">17%</span></div>
          <div class="rank-row"><span class="rank-lbl">On-Page SEO</span><div class="rank-bar"><div class="rank-fill" style="width:16%"></div></div><span class="rank-pct">16%</span></div>
          <div class="rank-row"><span class="rank-lbl">Citations</span><div class="rank-bar"><div class="rank-fill" style="width:13%"></div></div><span class="rank-pct">13%</span></div>
          <div class="rank-row"><span class="rank-lbl">Behavioral</span><div class="rank-bar"><div class="rank-fill" style="width:11%"></div></div><span class="rank-pct">11%</span></div>
          <p style="font-size:.7rem;color:var(--t3);margin-top:12px;font-family:var(--mono)">Source: Whitespark Local Ranking Factors</p>
        </div>
      </div>
      <div>
        <div class="svc-detail-icon">📍</div>
        <div class="eyebrow reveal">Service 02</div>
        <h2 class="reveal d1">Local SEO Audit</h2>
        <p class="reveal d2">For service businesses, local rankings drive booked jobs. Map pack dominance requires precise GBP optimization, citation consistency, and localized on-page signals — all working together.</p>
        <div class="checklist reveal d3">
          <div class="check-row"><div class="chk">✓</div>Google Business Profile complete audit</div>
          <div class="check-row"><div class="chk">✓</div>Citation consistency across 50+ directories</div>
          <div class="check-row"><div class="chk">✓</div>Local schema (LocalBusiness, Service, Review)</div>
          <div class="check-row"><div class="chk">✓</div>Map pack visibility analysis</div>
          <div class="check-row"><div class="chk">✓</div>Competitor local gap analysis</div>
          <div class="check-row"><div class="chk">✓</div>Review profile &amp; response audit</div>
          <div class="check-row"><div class="chk">✓</div>Service area page optimization</div>
        </div>
      </div>
    </div>
  </div>
</section>
<hr class="divider">
<section class="section" id="cwv">
  <div class="wrap">
    <div class="svc-detail-grid">
      <div>
        <div class="svc-detail-icon">⚡</div>
        <div class="eyebrow reveal">Service 03</div>
        <h2 class="reveal d1">Core Web Vitals</h2>
        <p class="reveal d2">Google uses LCP, INP, and CLS as direct ranking signals. Slow pages lose visitors before they see your offer. We benchmark your performance against Google's thresholds and your local competitors.</p>
        <div class="checklist reveal d3">
          <div class="metric-row"><span class="metric-k">LCP</span><span class="metric-v">Largest Contentful Paint — load speed</span><span class="metric-t">Goal: &lt; 2.5s</span></div>
          <div class="metric-row"><span class="metric-k">INP</span><span class="metric-v">Interaction to Next Paint — responsiveness</span><span class="metric-t">Goal: &lt; 200ms</span></div>
          <div class="metric-row"><span class="metric-k">CLS</span><span class="metric-v">Cumulative Layout Shift — visual stability</span><span class="metric-t">Goal: &lt; 0.1</span></div>
        </div>
      </div>
      <div class="svc-aside reveal d2">
        <div class="aside-box">
          <h4>Performance impact</h4>
          <div class="impact-row"><span class="impact-n">7%</span><span>conversion drop per 1 additional second of LCP delay</span></div>
          <div class="impact-row"><span class="impact-n">53%</span><span>mobile bounce rate when load time exceeds 3 seconds</span></div>
          <div class="impact-row"><span class="impact-n">2×</span><span>more likely to rank page 1 with good Core Web Vitals</span></div>
        </div>
      </div>
    </div>
  </div>
</section>
<hr class="divider">
<section class="section section-alt" id="ai">
  <div class="wrap">
    <div class="svc-detail-grid rev">
      <div class="svc-aside reveal">
        <div class="aside-box" style="border-color:var(--lime-d2);background:var(--lime-d)">
          <div class="tag" style="margin-bottom:14px">New in 2026</div>
          <h4>AI platforms audited</h4>
          <div class="finding">🤖 ChatGPT / GPT-4o</div>
          <div class="finding">🔍 Google AI Overviews</div>
          <div class="finding">🌐 Perplexity AI</div>
          <div class="finding">💬 Claude (Anthropic)</div>
          <div class="finding">✨ Gemini</div>
        </div>
      </div>
      <div>
        <div class="svc-detail-icon">🤖</div>
        <div class="eyebrow reveal">Service 04</div>
        <h2 class="reveal d1">AI Visibility Audit</h2>
        <p class="reveal d2">When someone asks ChatGPT "best HVAC company in Waco TX" — do you appear? AI search is now a primary discovery channel. Most local businesses are completely absent. We audit your AI footprint and fix it.</p>
        <div class="checklist reveal d3">
          <div class="check-row"><div class="chk">✓</div>AI platform citation analysis</div>
          <div class="check-row"><div class="chk">✓</div>Competitor AI visibility benchmarking</div>
          <div class="check-row"><div class="chk">✓</div>E-E-A-T signal audit</div>
          <div class="check-row"><div class="chk">✓</div>Knowledge graph presence check</div>
          <div class="check-row"><div class="chk">✓</div>GEO optimization recommendations</div>
          <div class="check-row"><div class="chk">✓</div>Structured data for AI comprehension</div>
        </div>
      </div>
    </div>
  </div>
</section>
<hr class="divider">
<section class="section" id="content">
  <div class="wrap">
    <div class="svc-detail-grid">
      <div>
        <div class="svc-detail-icon">📄</div>
        <div class="eyebrow reveal">Service 05</div>
        <h2 class="reveal d1">Content Architecture</h2>
        <p class="reveal d2">Your content structure tells search engines what you do and for whom. Poor internal linking, keyword cannibalization, and thin service pages quietly destroy ranking potential. We map it all.</p>
        <div class="checklist reveal d3">
          <div class="check-row"><div class="chk">✓</div>Topical authority mapping</div>
          <div class="check-row"><div class="chk">✓</div>Keyword cannibalization audit</div>
          <div class="check-row"><div class="chk">✓</div>Internal linking gap analysis</div>
          <div class="check-row"><div class="chk">✓</div>Service page quality assessment</div>
          <div class="check-row"><div class="chk">✓</div>Competitor content gap analysis</div>
          <div class="check-row"><div class="chk">✓</div>Content refresh recommendations</div>
        </div>
      </div>
      <div class="svc-aside reveal d2">
        <div class="aside-box">
          <h4>Not sure where to start?</h4>
          <p style="font-size:.88rem;margin-bottom:16px">Run the free audit — we'll diagnose which of these five areas is most critical for your site right now.</p>
          <a href="audit.html" class="btn btn-p" style="width:100%;justify-content:center;margin-bottom:10px">Run Free Audit →</a>
          <a href="contact.html" class="btn btn-g" style="width:100%;justify-content:center">Talk to Alex</a>
        </div>
      </div>
    </div>
  </div>
</section>'''
    return page('Services | SytFix', 'Five specialist audits: Technical SEO, Local SEO, Core Web Vitals, AI Visibility, and Content Architecture for local service businesses.', body, 'services.html')


def build_pricing():
    body = '''
<header class="ph">
  <div class="wrap">
    <div class="eyebrow reveal">Transparent Pricing</div>
    <h1 class="reveal d1">No retainers.<br><em>No surprises.</em></h1>
    <p class="ph-lead reveal d2">Three clear tiers. Every engagement starts with a comprehensive audit. You always know exactly what you're paying for and why.</p>
  </div>
</header>
<section class="section">
  <div class="wrap">
    <div class="pricing-grid">
      <div class="price-card reveal">
        <div class="price-tier">Audit Report</div>
        <div class="price-val">$497</div>
        <p class="price-desc">Complete technical and SEO audit with a prioritized fix roadmap. Ideal if you have a developer or agency to implement changes.</p>
        <div class="price-feats">
          <div class="price-feat">200+ point technical audit</div>
          <div class="price-feat">Local SEO &amp; GBP audit</div>
          <div class="price-feat">Core Web Vitals benchmarking</div>
          <div class="price-feat">AI visibility check</div>
          <div class="price-feat">Prioritized fix roadmap</div>
          <div class="price-feat">48-hour delivery</div>
          <div class="price-feat">30-min walkthrough call</div>
        </div>
        <a href="audit.html" class="btn btn-g" style="width:100%;justify-content:center">Get Audit Report →</a>
      </div>
      <div class="price-card price-card-feat reveal d1">
        <div class="price-tier">Audit + Fixes</div>
        <div class="price-val">$1,497</div>
        <p class="price-desc">Full audit plus hands-on implementation of critical fixes. We handle the technical work so you don't have to coordinate with a developer.</p>
        <div class="price-feats">
          <div class="price-feat">Everything in Audit Report</div>
          <div class="price-feat">Technical fix implementation</div>
          <div class="price-feat">Schema markup installation</div>
          <div class="price-feat">Page speed optimization</div>
          <div class="price-feat">GBP profile optimization</div>
          <div class="price-feat">Citation audit &amp; cleanup</div>
          <div class="price-feat">60-day follow-up review</div>
        </div>
        <a href="contact.html" class="btn btn-p" style="width:100%;justify-content:center">Get Started →</a>
      </div>
      <div class="price-card reveal d2">
        <div class="price-tier">Ongoing</div>
        <div class="price-val">$797<span>/mo</span></div>
        <p class="price-desc">Continuous monitoring, monthly audit cycles, and ongoing implementation for businesses that want to stay ahead of competitors.</p>
        <div class="price-feats">
          <div class="price-feat">Monthly technical refresh</div>
          <div class="price-feat">Ongoing implementation</div>
          <div class="price-feat">Rank tracking &amp; reporting</div>
          <div class="price-feat">AI visibility monitoring</div>
          <div class="price-feat">Competitor gap analysis</div>
          <div class="price-feat">Content recommendations</div>
          <div class="price-feat">Priority support &amp; calls</div>
        </div>
        <a href="contact.html" class="btn btn-g" style="width:100%;justify-content:center">Talk to Alex →</a>
      </div>
    </div>
    <div style="max-width:700px;margin:80px auto 0">
      <div class="eyebrow reveal" style="justify-content:center">Common Questions</div>
      <h2 class="reveal d1" style="text-align:center;margin-bottom:44px">FAQ</h2>
      <div class="faq-list">
        <details class="faq-item reveal">
          <summary>What's in the 200+ point audit?</summary>
          <p>Crawlability, indexation, site architecture, structured data, internal linking, duplicate content, page speed (all Core Web Vitals), mobile usability, HTTPS, Google Business Profile, citation consistency across 50+ directories, AI search visibility, and content quality across your key pages.</p>
        </details>
        <details class="faq-item reveal">
          <summary>How is this different from Semrush or Ahrefs?</summary>
          <p>Automated tools flag hundreds of issues with no context or prioritization. SytFix gives you a revenue-impact-ranked roadmap specific to your industry and local market, with manual review included. The AI visibility audit is also something most platforms don't offer.</p>
        </details>
        <details class="faq-item reveal">
          <summary>Do you serve businesses outside Texas?</summary>
          <p>Yes. Alex is based in Waco, TX, but SytFix serves clients nationwide. All audits and consultations are remote — phone and video call.</p>
        </details>
        <details class="faq-item reveal">
          <summary>What industries do you specialize in?</summary>
          <p>Legal practices, HVAC &amp; roofing, plumbing &amp; electrical, dental &amp; medical, damage restoration, and specialty contractors. We know the specific local SEO and schema signals that matter in each niche.</p>
        </details>
        <details class="faq-item reveal">
          <summary>How long does the audit take?</summary>
          <p>The full report is delivered within 48 business hours. Rush 24-hour delivery is available — contact us for pricing.</p>
        </details>
      </div>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap" style="text-align:center">
    <div class="eyebrow reveal" style="justify-content:center">Ready?</div>
    <h2 class="reveal d1" style="margin-bottom:14px">Start with a free snapshot audit.</h2>
    <p class="reveal d2" style="margin-bottom:32px;max-width:440px;margin-left:auto;margin-right:auto">Get an instant overview of your site's biggest issues before committing to anything.</p>
    <a href="audit.html" class="btn btn-p btn-xl reveal d3">Run Free Audit →</a>
  </div>
</section>'''
    return page('Pricing | SytFix', 'Transparent pricing for SytFix web audits and SEO services. Three tiers from $497.', body, 'pricing.html')


def build_audit():
    body = '''
<header class="ph">
  <div class="wrap">
    <div class="eyebrow reveal">Free Tool</div>
    <h1 class="reveal d1">Run your free<br><em>site audit.</em></h1>
    <p class="ph-lead reveal d2">Instant snapshot across 40 critical checks. See your top issues before spending a dollar.</p>
  </div>
</header>
<section class="section">
  <div class="wrap">
    <div class="audit-wrap">
      <div class="audit-card reveal" id="audit-form">
        <h3 style="margin-bottom:8px;font-family:var(--serif)">Enter your website URL</h3>
        <p style="font-size:.88rem;margin-bottom:26px">We check technical SEO, speed, local signals, and AI visibility.</p>
        <div class="f-group"><label class="f-label" for="audit-url">Website URL</label>
          <input class="f-input" type="text" id="audit-url" placeholder="yourdomain.com" autocomplete="off"></div>
        <div class="f-group"><label class="f-label" for="audit-industry">Industry</label>
          <select class="f-select" id="audit-industry">
            <option value="">Select your industry…</option>
            <option>Legal Practice</option><option>HVAC &amp; Roofing</option>
            <option>Plumbing &amp; Electrical</option><option>Dental &amp; Medical</option>
            <option>Damage Restoration</option><option>Specialty Contractor</option><option>Other</option>
          </select></div>
        <div class="f-group"><label class="f-label" for="audit-city">Primary Service City</label>
          <input class="f-input" type="text" id="audit-city" placeholder="e.g. Waco, TX"></div>
        <div class="f-group"><label class="f-label" for="audit-email">Email (receive full report)</label>
          <input class="f-input" type="email" id="audit-email" placeholder="you@yourbusiness.com"></div>
        <div class="audit-checks">
          <div class="audit-check">Technical SEO</div><div class="audit-check">Core Web Vitals</div>
          <div class="audit-check">Local SEO signals</div><div class="audit-check">AI Visibility</div>
          <div class="audit-check">Schema markup</div><div class="audit-check">Page speed</div>
          <div class="audit-check">Mobile usability</div><div class="audit-check">Security headers</div>
        </div>
        <button class="btn btn-p btn-lg" id="audit-start" style="width:100%;justify-content:center">Run Free Audit →</button>
        <p style="text-align:center;font-family:var(--mono);font-size:.64rem;color:var(--t3);margin-top:10px">No credit card. About 30 seconds.</p>
      </div>
      <div class="audit-card" id="audit-prog" style="display:none">
        <div style="text-align:center;margin-bottom:24px">
          <div style="font-size:2rem;display:inline-block;animation:spin 1.5s linear infinite">⚡</div>
          <h3 style="margin:12px 0 6px;font-family:var(--serif)">Auditing your site…</h3>
          <p style="font-size:.86rem">This takes about 30 seconds.</p>
        </div>
        <div class="prog-wrap"><div class="prog-fill" id="prog-fill"></div></div>
        <div id="prog-steps">
          <div class="prog-step" data-s="0">○ Crawlability &amp; indexation</div>
          <div class="prog-step" data-s="1">○ Core Web Vitals</div>
          <div class="prog-step" data-s="2">○ Local SEO signals</div>
          <div class="prog-step" data-s="3">○ Schema markup</div>
          <div class="prog-step" data-s="4">○ AI visibility</div>
          <div class="prog-step" data-s="5">○ Generating report</div>
        </div>
      </div>
      <div class="audit-card" id="audit-result" style="display:none">
        <div style="display:flex;align-items:center;gap:22px;margin-bottom:28px;flex-wrap:wrap">
          <div><div class="res-score" id="res-score">0</div>
          <p style="font-family:var(--mono);font-size:.68rem;color:var(--t3);margin-top:3px">Health Score / 100</p></div>
          <div style="flex:1;min-width:180px">
            <p style="font-size:.9rem;margin-bottom:10px">Your site has <strong id="res-count">6 issues</strong> that may be costing you clients.</p>
            <span class="tag">Needs Attention</span>
          </div>
        </div>
        <div id="res-issues"></div>
        <div class="upsell-box">
          <h4 style="font-family:var(--serif);font-size:1.1rem;margin-bottom:8px">Get the full 200+ point report</h4>
          <p style="font-size:.88rem;margin-bottom:18px">This snapshot covers the surface. The full audit goes 5× deeper — with a prioritized roadmap and revenue impact analysis for every finding.</p>
          <div style="display:flex;gap:12px;flex-wrap:wrap">
            <a href="pricing.html" class="btn btn-p">Get Full Audit — $497 →</a>
            <a href="contact.html" class="btn btn-g">Talk to Alex</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
<style>@keyframes spin{to{transform:rotate(360deg)}}</style>'''
    return page('Free Site Audit | SytFix', 'Run a free website audit with SytFix. Get an instant snapshot of your technical SEO, speed, and local visibility issues.', body, 'audit.html')


def build_calculator():
    body = '''
<header class="ph">
  <div class="wrap">
    <div class="eyebrow reveal">Free Tool</div>
    <h1 class="reveal d1">Revenue Impact<br><em>Calculator.</em></h1>
    <p class="ph-lead reveal d2">Model the financial upside of improved SEO rankings. See exactly what better visibility is worth to your business before spending a dollar.</p>
  </div>
</header>
<section class="section">
  <div class="wrap">
    <div class="calc-grid">
      <div class="calc-card reveal">
        <h3 style="font-family:var(--serif);margin-bottom:24px">Your Current Numbers</h3>
        <div class="calc-group">
          <div class="calc-row"><span class="calc-lbl">Monthly visitors</span><span class="calc-val" id="v-vis">800</span></div>
          <input type="range" class="range" id="r-vis" min="100" max="10000" step="100" value="800">
        </div>
        <div class="calc-group">
          <div class="calc-row"><span class="calc-lbl">Lead conversion rate</span><span class="calc-val" id="v-conv">3.0%</span></div>
          <input type="range" class="range" id="r-conv" min="0.5" max="15" step="0.5" value="3">
        </div>
        <div class="calc-group">
          <div class="calc-row"><span class="calc-lbl">Average job value</span><span class="calc-val" id="v-val">$1,200</span></div>
          <input type="range" class="range" id="r-val" min="200" max="20000" step="100" value="1200">
        </div>
        <div class="calc-group">
          <div class="calc-row"><span class="calc-lbl">Lead close rate</span><span class="calc-val" id="v-cls">40%</span></div>
          <input type="range" class="range" id="r-cls" min="10" max="90" step="5" value="40">
        </div>
        <hr class="divider" style="margin:24px 0">
        <h4 style="margin-bottom:18px">SEO Improvement Scenario</h4>
        <div class="calc-group">
          <div class="calc-row"><span class="calc-lbl">Traffic increase</span><span class="calc-val" id="v-tup">+40%</span></div>
          <input type="range" class="range" id="r-tup" min="10" max="200" step="5" value="40">
        </div>
        <div class="calc-group">
          <div class="calc-row"><span class="calc-lbl">Conversion improvement</span><span class="calc-val" id="v-cup">+1.0%</span></div>
          <input type="range" class="range" id="r-cup" min="0" max="5" step="0.5" value="1">
        </div>
      </div>
      <div class="reveal d1">
        <div class="calc-card" style="margin-bottom:16px">
          <div class="eyebrow" style="margin-bottom:14px">Current State</div>
          <div class="calc-res-row"><span>Monthly leads</span><span id="c-leads">24</span></div>
          <div class="calc-res-row"><span>Monthly clients</span><span id="c-clients">10</span></div>
          <div class="calc-res-row hi"><span>Monthly revenue</span><span id="c-rev">$11,520</span></div>
        </div>
        <div class="calc-card" style="border-color:var(--lime-d2);background:var(--lime-d);margin-bottom:16px">
          <div class="eyebrow" style="margin-bottom:14px">After Optimization</div>
          <div class="calc-res-row"><span>Monthly leads</span><span id="n-leads">37</span></div>
          <div class="calc-res-row"><span>Monthly clients</span><span id="n-clients">15</span></div>
          <div class="calc-res-row hi"><span>Monthly revenue</span><span id="n-rev">$17,760</span></div>
          <hr class="divider" style="margin:16px 0">
          <div style="text-align:center;padding:8px 0">
            <div style="font-family:var(--mono);font-size:.7rem;color:var(--t2);margin-bottom:4px">Additional annual revenue</div>
            <div class="res-num" id="annual-gain">$74,880</div>
          </div>
          <p style="font-family:var(--mono);font-size:.64rem;color:var(--t3);margin-top:14px">Based on your inputs. SEO improvements typically materialize over 3–6 months.</p>
        </div>
        <a href="audit.html" class="btn btn-p btn-lg" style="width:100%;justify-content:center">Run Free Audit →</a>
        <a href="pricing.html" class="btn btn-g" style="width:100%;justify-content:center;margin-top:10px">View Pricing</a>
      </div>
    </div>
  </div>
</section>'''
    return page('Revenue Calculator | SytFix', 'Calculate the revenue impact of SEO improvements for your local service business.', body, 'calculator.html')


def build_case_studies():
    body = '''
<header class="ph">
  <div class="wrap">
    <div class="eyebrow reveal">Real Results</div>
    <h1 class="reveal d1">From broken sites<br><em>to booked jobs.</em></h1>
    <p class="ph-lead reveal d2">Before-and-after results from service businesses that ran a SytFix audit and implemented the roadmap.</p>
  </div>
</header>
<section class="section">
  <div class="wrap">
    <div class="cs-card reveal">
      <div>
        <div class="cs-ind">⚖ Legal Practice · Waco, TX</div>
        <h3 class="cs-title">Family law firm — from page 4 to the local map pack</h3>
        <p style="font-size:.88rem;color:var(--t2);margin-bottom:14px">Solo family attorney invested in a redesign but was invisible in local search. Audit found: no LocalBusiness schema, GBP with 6 missing fields, and a 6.2s LCP on mobile.</p>
        <div class="checklist">
          <div class="check-row"><div class="chk">✓</div>Implemented full attorney schema markup</div>
          <div class="check-row"><div class="chk">✓</div>Rebuilt GBP profile — 100% completion</div>
          <div class="check-row"><div class="chk">✓</div>Image optimization brought LCP to 1.9s</div>
        </div>
      </div>
      <div>
        <p style="font-size:.84rem;color:var(--t2);margin-bottom:14px"><strong style="color:var(--t)">Timeline:</strong> 90 days</p>
        <div class="cs-results">
          <div class="cs-result"><span class="cs-num">+218%</span><div class="cs-lbl">Organic traffic</div></div>
          <div class="cs-result"><span class="cs-num">Top 3</span><div class="cs-lbl">Map pack rank</div></div>
        </div>
      </div>
    </div>
    <div class="cs-card reveal">
      <div>
        <div class="cs-ind">🏠 HVAC &amp; Roofing · DFW</div>
        <h3 class="cs-title">Regional HVAC company — duplicate pages killing rankings</h3>
        <p style="font-size:.88rem;color:var(--t2);margin-bottom:14px">12-person HVAC operation had 40+ service area pages, 28 near-duplicates. Google had de-indexed 60% of them. Citation NAP was inconsistent across 34 directories.</p>
        <div class="checklist">
          <div class="check-row"><div class="chk">✓</div>Consolidated duplicates with canonical strategy</div>
          <div class="check-row"><div class="chk">✓</div>Fixed NAP across 50 directories</div>
          <div class="check-row"><div class="chk">✓</div>Added HVACBusiness schema to all service pages</div>
        </div>
      </div>
      <div>
        <p style="font-size:.84rem;color:var(--t2);margin-bottom:14px"><strong style="color:var(--t)">Timeline:</strong> 60 days</p>
        <div class="cs-results">
          <div class="cs-result"><span class="cs-num">+340%</span><div class="cs-lbl">Pages recovered</div></div>
          <div class="cs-result"><span class="cs-num">+$14K</span><div class="cs-lbl">Monthly revenue</div></div>
        </div>
      </div>
    </div>
    <div class="cs-card reveal">
      <div>
        <div class="cs-ind">🦷 Dental Practice · Austin, TX</div>
        <h3 class="cs-title">Multi-location dental group — AI visibility gap</h3>
        <p style="font-size:.88rem;color:var(--t2);margin-bottom:14px">3-location dental group had strong traditional SEO but was absent from every AI search result tested. Competitors were consistently cited in Google AI Overviews and ChatGPT.</p>
        <div class="checklist">
          <div class="check-row"><div class="chk">✓</div>Restructured content with Q&amp;A format for AI extraction</div>
          <div class="check-row"><div class="chk">✓</div>Added FAQ schema to 12 key pages</div>
          <div class="check-row"><div class="chk">✓</div>Improved E-E-A-T signals (credentials, reviews, authorship)</div>
        </div>
      </div>
      <div>
        <p style="font-size:.84rem;color:var(--t2);margin-bottom:14px"><strong style="color:var(--t)">Timeline:</strong> 45 days</p>
        <div class="cs-results">
          <div class="cs-result"><span class="cs-num">AI ✓</span><div class="cs-lbl">Google AI Overviews</div></div>
          <div class="cs-result"><span class="cs-num">+67%</span><div class="cs-lbl">New inquiries</div></div>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap" style="text-align:center">
    <h2 class="reveal" style="margin-bottom:14px">Your site could be<br><em>next.</em></h2>
    <p class="reveal d1" style="margin-bottom:30px;max-width:420px;margin-left:auto;margin-right:auto">Start with the free audit — see your specific issues before committing to anything.</p>
    <a href="audit.html" class="btn btn-p btn-xl reveal d2">Run Free Audit →</a>
  </div>
</section>'''
    return page('Case Studies | SytFix', 'Real results from SytFix web audits — local service businesses that turned broken sites into revenue machines.', body, 'case-studies.html')


def build_process():
    body = '''
<header class="ph">
  <div class="wrap">
    <div class="eyebrow reveal">How It Works</div>
    <h1 class="reveal d1">Audit to results<br><em>in 48 hours.</em></h1>
    <p class="ph-lead reveal d2">No discovery calls to schedule a discovery call. No 3-week onboarding. Submit your site and have a prioritized roadmap in two business days.</p>
  </div>
</header>
<section class="section">
  <div class="wrap">
    <div class="timeline">
      <div class="tl-item reveal"><div class="tl-dot">01</div><h3>Submit your site</h3><p>Fill out the audit form with your URL, industry, and primary service city. No intake call required. The automated scan begins immediately across 200+ checkpoints.</p></div>
      <div class="tl-item reveal"><div class="tl-dot">02</div><h3>Automated + manual audit runs</h3><p>Our toolchain runs a full technical crawl, Core Web Vitals benchmark, schema validation, local signal analysis, citation check, and AI visibility test. Then Alex manually reviews every critical finding, adds industry-specific context, and connects issues to revenue impact — something automated tools cannot do.</p></div>
      <div class="tl-item reveal"><div class="tl-dot">03</div><h3>Report delivered within 48 hours</h3><p>You receive a structured report — not a 200-row CSV — with every issue ranked by potential revenue impact. Each finding includes: what it is, why it matters, how to fix it with specific instructions, and estimated implementation difficulty. Written for a business owner, not a developer.</p></div>
      <div class="tl-item reveal"><div class="tl-dot">04</div><h3>30-minute walkthrough call</h3><p>Alex walks you through the top findings, answers questions, and helps you decide which fixes to prioritize. You leave with a clear action plan — whether you're fixing it yourself or having us implement.</p></div>
      <div class="tl-item reveal"><div class="tl-dot">05</div><h3>Implementation — your choice</h3><p>On Audit + Fixes, Alex handles implementation of critical technical items: schema markup, GBP optimization, speed improvements, and citation cleanup. If you're doing it yourself, the report has everything your developer needs.</p></div>
      <div class="tl-item reveal"><div class="tl-dot">06</div><h3>60-day follow-up review</h3><p>On Audit + Fixes and Ongoing plans, we run a follow-up scan at 60 days to verify fixes held, measure ranking changes, and identify new issues. The initial audit gives the biggest gains fastest — the follow-up locks them in.</p></div>
    </div>
    <div style="margin-top:48px;display:flex;gap:14px;flex-wrap:wrap" class="reveal">
      <a href="audit.html" class="btn btn-p btn-lg">Start Your Audit →</a>
      <a href="pricing.html" class="btn btn-g btn-lg">View Pricing</a>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap">
    <div class="eyebrow reveal" style="justify-content:center">The Deliverable</div>
    <h2 class="reveal d1" style="text-align:center;margin-bottom:48px">What's inside<br><em>your audit report.</em></h2>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">
      <div class="card reveal"><div style="font-size:1.6rem;margin-bottom:10px">📊</div><h4 style="font-size:1rem;margin-bottom:8px">Executive Summary</h4><p style="font-size:.86rem">Overall health score, top 5 priority fixes, and revenue impact estimate. Readable in 5 minutes.</p></div>
      <div class="card reveal d1"><div style="font-size:1.6rem;margin-bottom:10px">⚙</div><h4 style="font-size:1rem;margin-bottom:8px">Technical Findings</h4><p style="font-size:.86rem">Every technical issue with severity rating, fix instructions, and difficulty estimate (Easy / Medium / Requires Developer).</p></div>
      <div class="card reveal d2"><div style="font-size:1.6rem;margin-bottom:10px">📍</div><h4 style="font-size:1rem;margin-bottom:8px">Local SEO Analysis</h4><p style="font-size:.86rem">GBP completeness score, citation inconsistency list, map pack visibility, and specific improvement steps.</p></div>
      <div class="card reveal"><div style="font-size:1.6rem;margin-bottom:10px">⚡</div><h4 style="font-size:1rem;margin-bottom:8px">Performance Report</h4><p style="font-size:.86rem">LCP, INP, and CLS benchmarked against Google thresholds and your top 3 local competitors.</p></div>
      <div class="card reveal d1"><div style="font-size:1.6rem;margin-bottom:10px">🤖</div><h4 style="font-size:1rem;margin-bottom:8px">AI Visibility Report</h4><p style="font-size:.86rem">Whether your business appears in ChatGPT, Perplexity, and Google AI Overviews — with specific steps to get cited.</p></div>
      <div class="card reveal d2"><div style="font-size:1.6rem;margin-bottom:10px">🗺</div><h4 style="font-size:1rem;margin-bottom:8px">Prioritized Roadmap</h4><p style="font-size:.86rem">Sequenced action plan — Quick Wins (week 1), Medium-term (months 1–3), Strategic (ongoing).</p></div>
    </div>
  </div>
</section>'''
    return page('Our Process | SytFix', 'How the SytFix audit process works — from submission to results in 48 hours.', body, 'process.html')


def build_about():
    body = '''
<header class="ph">
  <div class="wrap">
    <div class="eyebrow reveal">The Firm</div>
    <h1 class="reveal d1">Built by someone<br><em>who actually audits.</em></h1>
  </div>
</header>
<section class="section">
  <div class="wrap">
    <div class="about-grid">
      <div class="about-photo reveal">
        <span style="position:relative;z-index:1;font-size:5rem">👤</span>
        <div class="about-cap">
          <div class="about-cap-name">R. "Alex" Mitchell IV</div>
          <div class="about-cap-role">Founder &amp; Web Audit Specialist · Waco, TX</div>
        </div>
      </div>
      <div>
        <div class="eyebrow reveal">Founder</div>
        <h2 class="reveal d1" style="margin-bottom:22px">Alex Mitchell</h2>
        <div class="reveal d2">
          <p style="margin-bottom:18px">SytFix exists because I kept seeing the same problem: local service businesses investing real money into websites that quietly worked against them. Slow load times, invisible schema, GBP profiles missing half their data, and zero presence in the local map pack.</p>
          <p style="margin-bottom:18px">I started doing technical audits because I was frustrated with how agencies treated it — a monthly retainer checkbox outsourced to someone who'd never spoken to the business owner. I wanted to do it differently: direct, transparent, and tied to revenue, not vanity metrics.</p>
          <p style="margin-bottom:18px">SytFix is a one-person firm by design. Every audit is done by me, reviewed by me, and delivered with my name on it. That accountability is the product. You're not getting a templated report from an offshore team — you're getting a diagnosis from someone who has audited hundreds of service business websites and knows what actually moves the needle.</p>
          <p>Based in Waco, TX. Serving clients nationally.</p>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:36px" class="reveal d3">
          <div class="card" style="padding:22px"><div style="font-family:var(--mono);font-size:1.7rem;font-weight:600;color:var(--lime)">200+</div><p style="font-size:.84rem;margin-top:4px">Audit checkpoints per site</p></div>
          <div class="card" style="padding:22px"><div style="font-family:var(--mono);font-size:1.7rem;font-weight:600;color:var(--lime)">48hr</div><p style="font-size:.84rem;margin-top:4px">Report delivery</p></div>
          <div class="card" style="padding:22px"><div style="font-family:var(--mono);font-size:1.7rem;font-weight:600;color:var(--lime)">6</div><p style="font-size:.84rem;margin-top:4px">Industry specializations</p></div>
          <div class="card" style="padding:22px"><div style="font-family:var(--mono);font-size:1.7rem;font-weight:600;color:var(--lime)">100%</div><p style="font-size:.84rem;margin-top:4px">Founder-led audits</p></div>
        </div>
        <div style="margin-top:28px;display:flex;gap:14px;flex-wrap:wrap" class="reveal d4">
          <a href="audit.html" class="btn btn-p">Run Free Audit →</a>
          <a href="contact.html" class="btn btn-g">Talk to Alex Directly</a>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap">
    <div class="eyebrow reveal" style="justify-content:center">Philosophy</div>
    <h2 class="reveal d1" style="text-align:center;margin-bottom:44px">How we think about<br><em>the work.</em></h2>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">
      <div class="card reveal"><h4 style="font-family:var(--serif);font-size:1.15rem;margin-bottom:10px">Revenue over rankings</h4><p style="font-size:.88rem">A page 1 ranking that doesn't bring business means nothing. Every recommendation connects to a measurable outcome — more calls, more booked jobs, more revenue.</p></div>
      <div class="card reveal d1"><h4 style="font-family:var(--serif);font-size:1.15rem;margin-bottom:10px">No jargon, no fluff</h4><p style="font-size:.88rem">You shouldn't need a CS degree to understand your audit. Every finding is written in plain language with a clear explanation of why it matters and exactly what to do.</p></div>
      <div class="card reveal d2"><h4 style="font-family:var(--serif);font-size:1.15rem;margin-bottom:10px">Transparency first</h4><p style="font-size:.88rem">Pricing is public. Scope is clear before anything begins. If a fix won't meaningfully impact rankings, I'll say so — even if it means less billable work.</p></div>
    </div>
  </div>
</section>'''
    return page('About | SytFix', 'About SytFix and founder Alex Mitchell — precision web auditing for local service businesses from Waco, TX.', body, 'about.html')


def build_blog():
    body = '''
<header class="ph">
  <div class="wrap">
    <div class="eyebrow reveal">Insights</div>
    <h1 class="reveal d1">Technical SEO<br><em>without the jargon.</em></h1>
    <p class="ph-lead reveal d2">Practical guides for service business owners and the developers who build for them.</p>
  </div>
</header>
<section class="section">
  <div class="wrap">
    <a href="#" class="blog-feat reveal">
      <div class="blog-feat-img">🤖</div>
      <div class="blog-feat-body">
        <div style="display:flex;align-items:center;gap:12px"><span class="tag">Featured</span><span class="blog-date">April 2026</span></div>
        <h2>AI Visibility in 2026: Why Your Business Doesn't Exist in ChatGPT (and How to Fix That)</h2>
        <p>When someone asks an AI assistant for the best HVAC company in their city, your competitors show up and you don't. Here's a practical framework for auditing and improving your AI search presence.</p>
        <span class="blog-arrow">Read article →</span>
      </div>
    </a>
    <div class="blog-grid">
      <a href="#" class="blog-card reveal"><div class="blog-card-img">⚡</div><div class="blog-card-body"><div class="blog-date">March 2026</div><h3>INP Is Now a Core Web Vitals Ranking Signal — Here's What to Fix First</h3><p>Interaction to Next Paint replaced FID. Most service business sites fail it badly. Here's how to diagnose and fix the most common INP killers.</p><span class="blog-arrow">Read →</span></div></a>
      <a href="#" class="blog-card reveal d1"><div class="blog-card-img">📍</div><div class="blog-card-body"><div class="blog-date">March 2026</div><h3>The Local Map Pack in 2026: What's Actually Driving Rankings Now</h3><p>GBP signals now account for over a third of map pack placement. Here's what changed and what to prioritize this year.</p><span class="blog-arrow">Read →</span></div></a>
      <a href="#" class="blog-card reveal d2"><div class="blog-card-img">⚙</div><div class="blog-card-body"><div class="blog-date">February 2026</div><h3>Schema Markup for Service Businesses: The 7 Types That Actually Matter</h3><p>Most sites implement zero schema. The ones that do usually only add Organization. Here are the seven that move the needle.</p><span class="blog-arrow">Read →</span></div></a>
      <a href="#" class="blog-card reveal"><div class="blog-card-img">📄</div><div class="blog-card-body"><div class="blog-date">February 2026</div><h3>Service Area Pages: Build 20 City Pages Without Getting Penalized</h3><p>Service area pages are essential — but done wrong, they actively hurt rankings. This is the right architecture.</p><span class="blog-arrow">Read →</span></div></a>
      <a href="#" class="blog-card reveal d1"><div class="blog-card-img">🔗</div><div class="blog-card-body"><div class="blog-date">January 2026</div><h3>Internal Linking for Local SEO: Passing Authority to Your Service Pages</h3><p>Your homepage has the most authority. Most service businesses waste it by not linking strategically to their key pages.</p><span class="blog-arrow">Read →</span></div></a>
      <a href="#" class="blog-card reveal d2"><div class="blog-card-img">📊</div><div class="blog-card-body"><div class="blog-date">January 2026</div><h3>How to Calculate SEO Revenue Impact Before You Invest</h3><p>Before spending on SEO, model the return. This is the exact framework we use to project client revenue impact.</p><span class="blog-arrow">Read →</span></div></a>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap" style="max-width:520px;text-align:center">
    <div class="eyebrow reveal" style="justify-content:center">Stay Sharp</div>
    <h2 class="reveal d1" style="margin-bottom:14px">Technical SEO updates, once a month.</h2>
    <p class="reveal d2" style="margin-bottom:28px">Algorithm changes, tool updates, and tactics that matter for service businesses. No fluff.</p>
    <div class="reveal d3" style="display:flex;gap:10px;max-width:400px;margin:0 auto">
      <input class="f-input" type="email" placeholder="your@email.com" style="flex:1">
      <button class="btn btn-p" onclick="this.textContent='Subscribed ✓';this.disabled=true">Subscribe</button>
    </div>
  </div>
</section>'''
    return page('Blog | SytFix', 'Technical SEO insights, local search strategies, and web performance guides for service businesses.', body, 'blog.html')


def build_contact():
    body = '''
<header class="ph">
  <div class="wrap">
    <div class="eyebrow reveal">Get in Touch</div>
    <h1 class="reveal d1">Talk directly<br><em>to Alex.</em></h1>
    <p class="ph-lead reveal d2">No sales team. No intake form that vanishes into a CRM. You reach Alex directly and he responds within one business day.</p>
  </div>
</header>
<section class="section">
  <div class="wrap">
    <div class="contact-grid">
      <div>
        <div class="eyebrow reveal">Direct Contact</div>
        <h2 class="reveal d1" style="margin-bottom:28px">Alex Mitchell</h2>
        <div class="info-items reveal d2">
          <div class="info-item"><div class="info-icon">📞</div><div><div class="info-label">Phone / Text</div><a href="tel:2544476464" class="info-val">(254) 447-6464</a></div></div>
          <div class="info-item"><div class="info-icon">📍</div><div><div class="info-label">Location</div><span class="info-val">Waco, TX — Serving Nationwide</span></div></div>
          <div class="info-item"><div class="info-icon">⏱</div><div><div class="info-label">Response Time</div><span class="info-val">Within 1 business day</span></div></div>
        </div>
        <div style="margin-top:28px" class="reveal d3">
          <p style="font-size:.88rem;margin-bottom:18px">Not sure if SytFix is the right fit? Start with the free audit — 2 minutes and you'll have a real picture of where your site stands.</p>
          <a href="audit.html" class="btn btn-p">Run Free Audit First →</a>
        </div>
      </div>
      <div class="contact-form-card reveal d2">
        <h3 style="font-family:var(--serif);margin-bottom:22px">Send a message</h3>
        <div class="f-group"><label class="f-label" for="c-name">Your name</label><input class="f-input" type="text" id="c-name" placeholder="Jane Smith"></div>
        <div class="f-group"><label class="f-label" for="c-email">Email address</label><input class="f-input" type="email" id="c-email" placeholder="jane@mybusiness.com"></div>
        <div class="f-group"><label class="f-label" for="c-phone">Phone (optional)</label><input class="f-input" type="tel" id="c-phone" placeholder="(555) 000-0000"></div>
        <div class="f-group"><label class="f-label" for="c-url">Website URL</label><input class="f-input" type="text" id="c-url" placeholder="https://yoursite.com"></div>
        <div class="f-group"><label class="f-label" for="c-ind">Industry</label>
          <select class="f-select" id="c-ind">
            <option value="">Select…</option>
            <option>Legal Practice</option><option>HVAC &amp; Roofing</option>
            <option>Plumbing &amp; Electrical</option><option>Dental &amp; Medical</option>
            <option>Damage Restoration</option><option>Specialty Contractor</option><option>Other</option>
          </select></div>
        <div class="f-group"><label class="f-label" for="c-msg">What are you working on?</label>
          <textarea class="f-ta" id="c-msg" placeholder="Tell me about your site and what you're trying to accomplish…"></textarea></div>
        <button class="btn btn-p btn-lg" id="contact-btn" style="width:100%;justify-content:center">Send Message →</button>
        <p style="font-family:var(--mono);font-size:.64rem;color:var(--t3);margin-top:10px;text-align:center">Response within 1 business day.</p>
        <div class="success-msg" id="contact-success">
          <span style="font-size:1.5rem">✓</span>
          <p style="margin-top:8px;color:var(--t)">Message sent. Alex will be in touch within one business day.</p>
        </div>
      </div>
    </div>
  </div>
</section>'''
    return page('Contact | SytFix', 'Contact SytFix — talk directly to Alex Mitchell about your web audit and SEO needs.', body, 'contact.html')


def build_404():
    body = '''
<div class="nf-wrap">
  <div>
    <span class="nf-num">404</span>
    <h1>This page doesn't<br><em>exist.</em></h1>
    <p style="max-width:380px;margin:0 auto">Like a page Google can't index, this one's gone. Let's get you somewhere useful.</p>
    <div class="nf-btns">
      <a href="index.html" class="btn btn-p btn-xl">Back to Home →</a>
      <a href="audit.html" class="btn btn-g btn-lg">Run Free Audit</a>
    </div>
  </div>
</div>'''
    return page('404 | SytFix', 'Page not found.', body)


# ─────────────────────────────────────────────────────────────────
# Build everything
# ─────────────────────────────────────────────────────────────────
def build_site():
    print("\n\033[96m╔══════════════════════════════════╗")
    print("║  SytFix Site Builder             ║")
    print("╚══════════════════════════════════╝\033[0m\n")

    os.makedirs(os.path.join(ROOT, 'css'), exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'js'),  exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'img'), exist_ok=True)

    def w(path, content):
        full = os.path.join(ROOT, path)
        with open(full, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  \033[92m✓\033[0m {path}")

    w('css/main.css', CSS_MAIN)
    w('js/app.js',    JS_APP)
    w('img/logo.svg', LOGO_FULL_SVG)
    w('img/icon.svg', ICON_SVG)

    pages_map = {
        'index.html':        build_index(),
        'services.html':     build_services(),
        'pricing.html':      build_pricing(),
        'audit.html':        build_audit(),
        'calculator.html':   build_calculator(),
        'case-studies.html': build_case_studies(),
        'process.html':      build_process(),
        'about.html':        build_about(),
        'blog.html':         build_blog(),
        'contact.html':      build_contact(),
        '404.html':          build_404(),
    }
    for fname, html in pages_map.items():
        w(fname, html)

    # robots.txt
    w('robots.txt', 'User-agent: *\nAllow: /\nSitemap: https://sytfix.com/sitemap.xml\n')

    # sitemap
    urls = [('', '1.0')] + [(p.replace('.html',''), '0.9') for p in pages_map if p != 'index.html' and p != '404.html']
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u, pri in urls:
        loc = f"https://sytfix.com/{u}.html" if u else "https://sytfix.com/"
        sitemap += f'  <url><loc>{loc}</loc><priority>{pri}</priority></url>\n'
    sitemap += '</urlset>'
    w('sitemap.xml', sitemap)

    # GitHub Actions
    os.makedirs(os.path.join(ROOT, '.github', 'workflows'), exist_ok=True)
    w('.github/workflows/deploy.yml', '''name: Deploy to GitHub Pages
on:
  push:
    branches: ["main"]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: "pages"
  cancel-in-progress: false
jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - id: deployment
        uses: actions/deploy-pages@v4
''')

    total = len(pages_map) + 6
    print(f"\n\033[92m✓ Built {total} files successfully.\033[0m")

# ─────────────────────────────────────────────────────────────────
# Deploy to GitHub
# ─────────────────────────────────────────────────────────────────
def gh(method, path, data=None, expect=None):
    url = API + path
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method, headers={
        'Authorization': f'Bearer {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/json',
        'User-Agent': 'SytFix-Deploy/1.0',
    })
    try:
        with urllib.request.urlopen(req) as r:
            content = r.read()
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if expect and e.code in expect:
            return {'_code': e.code, '_body': body}
        try: msg = json.loads(body).get('message', body)
        except: msg = body
        print(f"\033[91m  ✗ GitHub API {method} {path} → {e.code}: {msg}\033[0m")
        sys.exit(1)

def deploy():
    print("\n\033[96m╔══════════════════════════════════╗")
    print("║  SytFix GitHub Deploy            ║")
    print("╚══════════════════════════════════╝\033[0m\n")

    if not GITHUB_TOKEN:
        print("\033[91m  ✗ GITHUB_TOKEN not set.\n    Run: export GITHUB_TOKEN=your_token\033[0m")
        sys.exit(1)
    if not shutil.which('git'):
        print("\033[91m  ✗ git not installed. On Termux: pkg install git\033[0m")
        sys.exit(1)

    # Auth check
    user = gh('GET', '/user')
    login = user.get('login', GITHUB_USER)
    print(f"  \033[92m✓\033[0m Authenticated as: {login}")

    # Repo
    resp = gh('GET', f'/repos/{login}/{REPO_NAME}', expect=[404])
    if resp.get('_code') == 404:
        print(f"  → Creating repository '{REPO_NAME}'…")
        repo = gh('POST', '/user/repos', {
            'name': REPO_NAME,
            'description': 'SytFix — Web Auditing & SEO Optimization',
            'private': False, 'auto_init': False,
        })
        clone_url = repo['clone_url']
        print(f"  \033[92m✓\033[0m Repository created: {repo['html_url']}")
    else:
        clone_url = resp['clone_url']
        print(f"  \033[92m✓\033[0m Repository exists: {resp['html_url']}")

    auth_url = clone_url.replace('https://', f'https://{login}:{GITHUB_TOKEN}@')

    def run(cmd, **kw):
        r = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True, **kw)
        if r.returncode != 0:
            print(f"\033[91m  ✗ {cmd}\n    {r.stderr.strip()}\033[0m")
            sys.exit(1)
        return r

    git_dir = os.path.join(ROOT, '.git')
    if not os.path.exists(git_dir):
        run('git init -b main')
        run(f'git remote add origin "{auth_url}"')
    else:
        run(f'git remote set-url origin "{auth_url}"')

    run('git config user.email "deploy@sytfix.com"')
    run('git config user.name "SytFix Deploy"')

    gitignore = os.path.join(ROOT, '.gitignore')
    if not os.path.exists(gitignore):
        with open(gitignore, 'w') as f:
            f.write('*.DS_Store\n.env\nnode_modules/\n*.log\nbuild.py\n')

    run('git add -A')
    st = subprocess.run('git status --porcelain', shell=True, cwd=ROOT, capture_output=True, text=True)
    if st.stdout.strip():
        run('git commit -m "🚀 SytFix deploy $(date +%Y-%m-%d)"')
        print("  \033[92m✓\033[0m Commit created")
    else:
        print("  ⚠ Nothing new to commit")

    push = subprocess.run(f'git push -u origin {BRANCH} --force', shell=True, cwd=ROOT, capture_output=True, text=True)
    if push.returncode != 0:
        subprocess.run(f'git push origin {BRANCH}:refs/heads/{BRANCH} --force', shell=True, cwd=ROOT)
    print("  \033[92m✓\033[0m Pushed to GitHub")

    # Enable Pages
    pr = gh('POST', f'/repos/{login}/{REPO_NAME}/pages',
            {'source': {'branch': BRANCH, 'path': '/'}}, expect=[409, 422])
    if pr.get('_code') in [409, 422]:
        gh('PUT', f'/repos/{login}/{REPO_NAME}/pages',
           {'source': {'branch': BRANCH, 'path': '/'}}, expect=[200, 204])
    print("  \033[92m✓\033[0m GitHub Pages enabled")

    pages_url = f"https://{login.lower()}.github.io/{REPO_NAME}/"
    print(f"\n\033[92m✓ Deployed!\033[0m")
    print(f"  Site: {pages_url}")
    print(f"  Repo: https://github.com/{login}/{REPO_NAME}")
    print(f"\n  DNS for sytfix.com:")
    for ip in ['185.199.108.153','185.199.109.153','185.199.110.153','185.199.111.153']:
        print(f"    A @ {ip}")
    print(f"    CNAME www {login.lower()}.github.io\n")


if __name__ == '__main__':
    build_site()
    if '--deploy' in sys.argv:
        deploy()
    else:
        print("\n  To deploy: \033[93mGITHUB_TOKEN=xxx python3 build.py --deploy\033[0m\n")
