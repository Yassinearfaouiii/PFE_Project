import streamlit as st

FONTS = "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap"

BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg:        #06080f;
    --bg2:       #0b0e1a;
    --bg3:       #111527;
    --surface:   rgba(255,255,255,0.032);
    --surface2:  rgba(255,255,255,0.06);
    --blue:      #3b82f6;
    --blue-dim:  rgba(59,130,246,0.18);
    --blue-glow: rgba(59,130,246,0.35);
    --violet:    #8b5cf6;
    --violet-dim:rgba(139,92,246,0.18);
    --cyan:      #06b6d4;
    --green:     #10b981;
    --green-dim: rgba(16,185,129,0.14);
    --amber:     #f59e0b;
    --amber-dim: rgba(245,158,11,0.14);
    --red:       #ef4444;
    --red-dim:   rgba(239,68,68,0.14);
    --border:    rgba(255,255,255,0.07);
    --border2:   rgba(59,130,246,0.22);
    --text:      #f8fafc;
    --text2:     #94a3b8;
    --text3:     #475569;
    --r:         12px;
    --r2:        18px;
    --r3:        24px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, [data-testid="stAppViewContainer"], .stApp {
    background: var(--bg) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
}

/* ── REMOVE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stToolbar"] { display: none; }

/* ── LAYOUT ── */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── GLOBAL SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 99px; }

/* ── BUTTONS ── */
.stButton > button {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.01em !important;
    border-radius: var(--r) !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.18s ease !important;
    border: 1px solid var(--border2) !important;
    background: var(--blue-dim) !important;
    color: #93c5fd !important;
}
.stButton > button:hover {
    background: rgba(59,130,246,0.28) !important;
    border-color: var(--blue) !important;
    box-shadow: 0 0 22px var(--blue-glow) !important;
    transform: translateY(-1px) !important;
    color: #fff !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox > div > div > div {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.9rem !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
    outline: none !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label,
.stFileUploader label, .stSlider label {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.09em !important;
    text-transform: uppercase !important;
    color: var(--text3) !important;
}

/* ── TABS ── */
[data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
[data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text3) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 0.8rem 1.6rem !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.15s !important;
}
[aria-selected="true"] {
    color: var(--blue) !important;
    border-bottom: 2px solid var(--blue) !important;
}
[data-baseweb="tab"]:hover { color: var(--text) !important; }

/* ── EXPANDER ── */
.stExpander {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r2) !important;
    margin-bottom: 0.6rem !important;
    overflow: hidden !important;
    transition: border-color 0.15s !important;
}
.stExpander:hover { border-color: var(--border2) !important; }
details > summary {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 1rem 1.25rem !important;
    color: var(--text) !important;
}

/* ── FORMS ── */
[data-testid="stForm"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r2) !important;
    padding: 1.5rem !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r2) !important;
    padding: 1.4rem 1.6rem !important;
    position: relative !important;
    overflow: hidden !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
[data-testid="stMetric"]:hover {
    border-color: var(--border2) !important;
    box-shadow: 0 6px 28px rgba(59,130,246,0.12) !important;
}
[data-testid="stMetricLabel"] p {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--text3) !important;
}
[data-testid="stMetricValue"] div {
    font-family: 'Outfit', sans-serif !important;
    font-size: 2.1rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
}

/* ── ALERTS ── */
[data-testid="stNotification"] {
    border-radius: var(--r) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stSuccess { border: none !important; }
.stError   { border: none !important; }
.stWarning { border: none !important; }
.stInfo    { border: none !important; }

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: var(--bg3) !important;
    border: 1.5px dashed var(--border2) !important;
    border-radius: var(--r2) !important;
    transition: all 0.15s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--blue) !important;
    background: var(--blue-dim) !important;
}

/* ── SELECTBOX ── */
[data-baseweb="select"] > div {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--text) !important;
}

/* ── PROGRESS ── */
.stProgress > div > div { background: var(--bg3) !important; border-radius: 99px !important; }
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--blue), var(--violet)) !important;
    border-radius: 99px !important;
    transition: width 0.3s ease !important;
}

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }

/* ── POPOVER ── */
[data-testid="stPopover"] > div {
    background: var(--bg2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: var(--r2) !important;
}

/* ── SPINNER ── */
.stSpinner > div { border-top-color: var(--blue) !important; }

/* ─────────────────────────────────────────
   SHARED COMPONENT CLASSES
───────────────────────────────────────── */

/* Page wrapper */
.page-wrap {
    padding: 2rem 2.5rem 3rem;
    max-width: 1280px;
    margin: 0 auto;
}

/* Top navigation bar */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 2.5rem;
    background: rgba(6,8,15,0.85);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
}
.topbar-logo {
    font-family: 'Outfit', sans-serif;
    font-weight: 900;
    font-size: 1.1rem;
    letter-spacing: -0.02em;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 10px;
}
.topbar-logo span { color: var(--blue); }
.topbar-nav { display: flex; gap: 6px; align-items: center; }
.nav-link {
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text2);
    text-decoration: none;
    transition: all 0.15s;
    font-family: 'Space Grotesk', sans-serif;
    cursor: pointer;
    border: 1px solid transparent;
}
.nav-link:hover, .nav-link.active {
    background: var(--blue-dim);
    color: #93c5fd;
    border-color: var(--border2);
}
.nav-badge {
    display: inline-block;
    background: var(--blue);
    color: white;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 99px;
    margin-left: 4px;
    vertical-align: middle;
}

/* Section heading */
.sec-head {
    margin-bottom: 1.5rem;
}
.sec-eyebrow {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--blue);
    font-family: 'Space Grotesk', sans-serif;
    margin-bottom: 6px;
}
.sec-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 1.9rem;
    letter-spacing: -0.03em;
    color: var(--text);
    line-height: 1.15;
}
.sec-title em {
    font-style: normal;
    background: linear-gradient(135deg, var(--blue), var(--violet));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sec-sub {
    font-size: 0.9rem;
    color: var(--text2);
    font-family: 'Space Grotesk', sans-serif;
    margin-top: 6px;
    line-height: 1.65;
}

/* Card */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r2);
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.15s, transform 0.15s, box-shadow 0.15s;
}
.card:hover {
    border-color: var(--border2);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}
.card-accent-top::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--blue), var(--violet));
}

/* Status badges */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 11px;
    border-radius: 99px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    font-family: 'Space Grotesk', sans-serif;
}
.badge-accepted { background: var(--green-dim); color: var(--green); border: 1px solid rgba(16,185,129,0.25); }
.badge-pending  { background: var(--amber-dim); color: var(--amber); border: 1px solid rgba(245,158,11,0.25); }
.badge-rejected { background: var(--red-dim);   color: var(--red);   border: 1px solid rgba(239,68,68,0.25); }

/* Divider label */
.divlabel {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--blue);
    font-family: 'Space Grotesk', sans-serif;
    margin: 1.2rem 0 0.75rem;
}
.divlabel::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Skill chips */
.chip {
    display: inline-block;
    padding: 3px 11px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.04em;
    margin: 3px;
}
.chip-green { background: var(--green-dim); color: #34d399; border: 1px solid rgba(16,185,129,0.2); }
.chip-red   { background: var(--red-dim);   color: #f87171; border: 1px solid rgba(239,68,68,0.2); }
.chip-blue  { background: var(--blue-dim);  color: #93c5fd; border: 1px solid rgba(59,130,246,0.2); }
.chip-gray  { background: var(--surface2);  color: var(--text2); border: 1px solid var(--border); }

/* Download button */
.dl-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: var(--blue-dim);
    color: #93c5fd;
    border: 1px solid var(--border2);
    border-radius: var(--r);
    padding: 9px 14px;
    font-size: 0.83rem;
    font-weight: 600;
    text-decoration: none;
    font-family: 'Space Grotesk', sans-serif;
    transition: all 0.15s;
    margin-bottom: 8px;
}
.dl-btn:hover {
    background: rgba(59,130,246,0.28);
    border-color: var(--blue);
    color: #fff;
    box-shadow: 0 0 18px var(--blue-glow);
}

/* Score ring display */
.score-block {
    text-align: center;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--r2);
    padding: 1rem;
}
.score-num {
    font-family: 'Outfit', sans-serif;
    font-size: 2rem;
    font-weight: 900;
    line-height: 1;
}
.score-lbl {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text3);
    margin-top: 4px;
    font-family: 'Space Grotesk', sans-serif;
}

/* AI report box */
.ai-box {
    background: rgba(0,0,0,0.3);
    border-left: 3px solid var(--blue);
    border-radius: 0 var(--r) var(--r) 0;
    padding: 1rem 1.25rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--text2);
    line-height: 1.8;
    white-space: pre-wrap;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--text3);
    font-family: 'Space Grotesk', sans-serif;
}
.empty-state .icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
.empty-state .msg  { font-size: 0.92rem; }
</style>
"""

def inject():
    st.markdown(BASE_CSS, unsafe_allow_html=True)

def topbar(active="home", is_admin=False):
    """Render the sticky top navigation bar."""
    if is_admin:
        nav = f"""
        <div class="topbar">
            <div class="topbar-logo">
                <span>◈</span> PFE <span>Hub</span>
                <span style="font-size:0.65rem;background:var(--blue-dim);color:#93c5fd;border:1px solid var(--border2);
                             padding:2px 9px;border-radius:99px;margin-left:8px;font-family:'Space Grotesk',sans-serif;
                             font-weight:700;letter-spacing:0.08em;">ADMIN</span>
            </div>
            <div class="topbar-nav">
                <span class="nav-link {'active' if active=='dashboard' else ''}">Dashboard</span>
                <span class="nav-link {'active' if active=='ats' else ''}">ATS Analyzer</span>
                <span class="nav-link {'active' if active=='subjects' else ''}">Sujets</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <div style="width:8px;height:8px;border-radius:50%;background:var(--green);
                            box-shadow:0 0 8px var(--green);"></div>
                <span style="font-size:0.78rem;color:var(--text2);font-family:'Space Grotesk',sans-serif;">Session active</span>
            </div>
        </div>
        """
    else:
        nav = f"""
        <div class="topbar">
            <div class="topbar-logo">
                <span>◈</span> PFE <span>Hub</span>
            </div>
            <div class="topbar-nav">
                <span class="nav-link {'active' if active=='home' else ''}">Accueil</span>
                <span class="nav-link {'active' if active=='catalogue' else ''}">Catalogue</span>
                <span class="nav-link {'active' if active=='postuler' else ''}">Postuler</span>
            </div>
        </div>
        """
    st.markdown(nav, unsafe_allow_html=True)