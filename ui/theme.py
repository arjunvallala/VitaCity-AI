"""
VitaCity AI — Premium Dark-Mode Theme
Custom CSS injected via st.markdown for glassmorphism and gradient UI.
"""

CUSTOM_CSS = """
<style>
/* ── Google Font Import ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── CSS Variables ── */
:root {
  --bg-primary: #080c14;
  --bg-secondary: #0d1520;
  --bg-card: rgba(255,255,255,0.04);
  --bg-card-hover: rgba(255,255,255,0.07);
  --border-color: rgba(255,255,255,0.08);
  --border-hover: rgba(76,201,240,0.4);

  --accent-blue: #4CC9F0;
  --accent-green: #4ADE80;
  --accent-purple: #A78BFA;
  --accent-pink: #EC4899;
  --accent-orange: #F97316;
  --accent-yellow: #FBBF24;

  --text-primary: #F0F6FF;
  --text-secondary: #8B9EC5;
  --text-muted: #4B5E7A;

  --gradient-1: linear-gradient(135deg, #4CC9F0, #A78BFA);
  --gradient-2: linear-gradient(135deg, #4ADE80, #4CC9F0);
  --gradient-3: linear-gradient(135deg, #F97316, #EC4899);
  --gradient-hero: linear-gradient(135deg, #0d1520 0%, #141c2e 50%, #0d1520 100%);

  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;

  --shadow-glow-blue: 0 0 20px rgba(76,201,240,0.15);
  --shadow-glow-green: 0 0 20px rgba(74,222,128,0.15);
  --shadow-card: 0 4px 24px rgba(0,0,0,0.4);
}

/* ── Global Reset ── */
html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--bg-primary) !important;
  font-family: 'Inter', sans-serif !important;
  color: var(--text-primary) !important;
}

[data-testid="stApp"] {
  background-color: var(--bg-primary) !important;
}

/* ── Hide Streamlit Defaults ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--bg-secondary) !important;
  border-right: 1px solid var(--border-color) !important;
}

[data-testid="stSidebar"] > div:first-child {
  padding-top: 0 !important;
}

/* ── Sidebar Radio Buttons (Navigation) ── */
[data-testid="stSidebar"] .stRadio > label {
  color: var(--text-secondary) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 4px !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
  background: transparent !important;
  border: 1px solid transparent !important;
  border-radius: var(--radius-sm) !important;
  padding: 10px 14px !important;
  margin: 2px 0 !important;
  transition: all 0.2s ease !important;
  color: var(--text-secondary) !important;
  font-size: 14px !important;
  cursor: pointer !important;
  display: flex !important;
  align-items: center !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
  background: var(--bg-card-hover) !important;
  border-color: var(--border-hover) !important;
  color: var(--text-primary) !important;
}

/* ── Main Content Area ── */
.main .block-container {
  padding: 1.5rem 2rem 2rem 2rem !important;
  max-width: 1400px !important;
}

/* ── Headings ── */
h1, h2, h3, h4 {
  font-family: 'Inter', sans-serif !important;
  color: var(--text-primary) !important;
}

/* ── Streamlit Buttons ── */
.stButton > button {
  background: var(--bg-card) !important;
  color: var(--text-primary) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-md) !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 500 !important;
  font-size: 13px !important;
  padding: 8px 18px !important;
  transition: all 0.2s ease !important;
  cursor: pointer !important;
}

.stButton > button:hover {
  background: rgba(76,201,240,0.1) !important;
  border-color: var(--accent-blue) !important;
  color: var(--accent-blue) !important;
  box-shadow: var(--shadow-glow-blue) !important;
  transform: translateY(-1px) !important;
}

.stButton > button:active {
  transform: translateY(0) !important;
}

/* ── Primary Button (for CTAs) ── */
.stButton > button[kind="primary"] {
  background: var(--gradient-1) !important;
  border: none !important;
  color: white !important;
  font-weight: 600 !important;
}

.stButton > button[kind="primary"]:hover {
  opacity: 0.9 !important;
  box-shadow: 0 0 24px rgba(76,201,240,0.3) !important;
  color: white !important;
}

/* ── Text Input & Text Area ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-md) !important;
  color: var(--text-primary) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 14px !important;
  transition: border-color 0.2s !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--accent-blue) !important;
  box-shadow: var(--shadow-glow-blue) !important;
}

/* ── Selectbox / Dropdown ── */
.stSelectbox > div > div {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-md) !important;
  color: var(--text-primary) !important;
}

/* ── Slider ── */
.stSlider > div > div > div > div {
  background: var(--gradient-1) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-lg) !important;
  padding: 16px 20px !important;
}

[data-testid="stMetricLabel"] {
  color: var(--text-secondary) !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
}

[data-testid="stMetricValue"] {
  color: var(--text-primary) !important;
  font-size: 28px !important;
  font-weight: 700 !important;
}

[data-testid="stMetricDelta"] {
  font-size: 12px !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-md) !important;
}

[data-testid="stExpander"] summary {
  color: var(--text-primary) !important;
  font-weight: 500 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important;
  gap: 4px !important;
  border-bottom: 1px solid var(--border-color) !important;
}

.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: var(--radius-sm) var(--radius-sm) 0 0 !important;
  color: var(--text-secondary) !important;
  font-weight: 500 !important;
  border: none !important;
  padding: 8px 16px !important;
  transition: all 0.2s !important;
}

.stTabs [aria-selected="true"] {
  background: transparent !important;
  color: var(--accent-blue) !important;
  border-bottom: 2px solid var(--accent-blue) !important;
}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {
  background: var(--bg-card) !important;
  border: 1px dashed var(--border-color) !important;
  border-radius: var(--radius-lg) !important;
}

[data-testid="stFileUploader"]:hover {
  border-color: var(--accent-blue) !important;
}

/* ── Divider ── */
hr {
  border-color: var(--border-color) !important;
  margin: 1.5rem 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--text-muted); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-secondary); }

/* ── Toast / Info/Warning boxes ── */
.stInfo, .stSuccess, .stWarning, .stError {
  border-radius: var(--radius-md) !important;
  font-family: 'Inter', sans-serif !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent-blue) !important; }

/* ── Progress Bar ── */
.stProgress > div > div > div {
  background: var(--gradient-1) !important;
}

/* ── DataFrame / Table ── */
[data-testid="stDataFrame"] {
  border-radius: var(--radius-md) !important;
  overflow: hidden !important;
}

/* ── Number Input ── */
.stNumberInput > div > div > input {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-md) !important;
  color: var(--text-primary) !important;
}

/* ── Caption Text ── */
.stCaption {
  color: var(--text-muted) !important;
  font-size: 12px !important;
}

/* ═══════════════════════════════════════
   CUSTOM COMPONENT STYLES
═══════════════════════════════════════ */

/* Hero Banner */
.vitacity-hero {
  background: linear-gradient(135deg, rgba(76,201,240,0.08) 0%, rgba(167,139,250,0.08) 50%, rgba(74,222,128,0.05) 100%);
  border: 1px solid rgba(76,201,240,0.2);
  border-radius: var(--radius-xl);
  padding: 32px 40px;
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;
}

.vitacity-hero::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(76,201,240,0.06) 0%, transparent 70%);
  border-radius: 50%;
}

.vitacity-logo {
  font-size: 28px;
  font-weight: 800;
  background: linear-gradient(135deg, #4CC9F0, #A78BFA);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
}

.vitacity-tagline {
  font-size: 13px;
  color: var(--text-muted);
  margin-top: 4px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* KPI Card */
.kpi-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 20px 24px;
  transition: all 0.3s ease;
  cursor: default;
}

.kpi-card:hover {
  background: var(--bg-card-hover);
  border-color: rgba(76,201,240,0.3);
  transform: translateY(-2px);
  box-shadow: var(--shadow-card);
}

.kpi-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.kpi-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.1;
}

.kpi-label {
  font-size: 12px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: 4px;
}

.kpi-delta {
  font-size: 11px;
  margin-top: 6px;
}

.kpi-delta.positive { color: #4ADE80; }
.kpi-delta.negative { color: #EF4444; }

/* Chat Bubble */
.chat-bubble-user {
  background: linear-gradient(135deg, rgba(76,201,240,0.15), rgba(167,139,250,0.1));
  border: 1px solid rgba(76,201,240,0.2);
  border-radius: 16px 16px 4px 16px;
  padding: 14px 18px;
  margin: 8px 0 8px 15%;
  color: var(--text-primary);
  font-size: 14px;
  line-height: 1.6;
}

.chat-bubble-ai {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px 16px 16px 4px;
  padding: 18px 22px;
  margin: 8px 15% 8px 0;
  color: var(--text-primary);
  font-size: 14px;
  line-height: 1.7;
}

.chat-bubble-ai table {
  border-collapse: collapse;
  width: 100%;
  margin: 12px 0;
}

.chat-bubble-ai th {
  background: rgba(76,201,240,0.1);
  color: var(--accent-blue);
  padding: 8px 12px;
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 1px solid var(--border-color);
}

.chat-bubble-ai td {
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  font-size: 13px;
}

.chat-bubble-ai tr:nth-child(even) td {
  background: rgba(255,255,255,0.02);
}

/* Confidence Badge */
.confidence-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.03em;
}

.confidence-high {
  background: rgba(74,222,128,0.12);
  color: #4ADE80;
  border: 1px solid rgba(74,222,128,0.25);
}

.confidence-medium {
  background: rgba(251,191,36,0.12);
  color: #FBBF24;
  border: 1px solid rgba(251,191,36,0.25);
}

.confidence-low {
  background: rgba(249,115,22,0.12);
  color: #F97316;
  border: 1px solid rgba(249,115,22,0.25);
}

/* Domain Badge */
.domain-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  background: rgba(76,201,240,0.1);
  color: var(--accent-blue);
  border: 1px solid rgba(76,201,240,0.2);
}

/* Alert Cards */
.alert-card {
  border-radius: var(--radius-md);
  padding: 14px 18px;
  margin: 8px 0;
  border-left: 3px solid;
  font-size: 13px;
}

.alert-high {
  background: rgba(239,68,68,0.08);
  border-left-color: #EF4444;
  color: var(--text-primary);
}

.alert-medium {
  background: rgba(249,115,22,0.08);
  border-left-color: #F97316;
  color: var(--text-primary);
}

.alert-low {
  background: rgba(251,191,36,0.08);
  border-left-color: #FBBF24;
  color: var(--text-primary);
}

/* Impact Score Ring (for simulator) */
.impact-ring {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 20px;
  text-align: center;
  transition: all 0.3s ease;
}

.impact-ring:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-card);
}

.impact-score-big {
  font-size: 42px;
  font-weight: 800;
  line-height: 1;
  background: var(--gradient-1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Source Citation */
.source-citation {
  background: rgba(76,201,240,0.05);
  border: 1px solid rgba(76,201,240,0.15);
  border-radius: var(--radius-sm);
  padding: 8px 12px;
  font-size: 12px;
  color: var(--text-secondary);
  margin: 4px 0;
}

/* Scenario Button */
.scenario-btn-wrapper .stButton > button {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-md) !important;
  text-align: left !important;
  padding: 14px 16px !important;
  height: auto !important;
  line-height: 1.4 !important;
  font-size: 13px !important;
  width: 100% !important;
  transition: all 0.25s ease !important;
}

.scenario-btn-wrapper .stButton > button:hover {
  background: var(--bg-card-hover) !important;
  border-color: var(--accent-blue) !important;
  transform: translateY(-2px) !important;
  box-shadow: var(--shadow-glow-blue) !important;
}

/* Sidebar Logo Section */
.sidebar-logo {
  padding: 24px 16px 20px 16px;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 16px;
}

.sidebar-logo .logo-text {
  font-size: 20px;
  font-weight: 800;
  background: linear-gradient(135deg, #4CC9F0, #A78BFA);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.sidebar-logo .logo-sub {
  font-size: 10px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-top: 2px;
}

/* Status Indicator */
.status-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse-dot 2s infinite;
}

.status-dot.green { background: #4ADE80; }
.status-dot.yellow { background: #FBBF24; }
.status-dot.red { background: #EF4444; }

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* Recommendation Card */
.rec-card {
  background: rgba(76,201,240,0.04);
  border: 1px solid rgba(76,201,240,0.12);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  margin: 6px 0;
  font-size: 13px;
  color: var(--text-primary);
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.rec-card::before {
  content: '→';
  color: var(--accent-blue);
  font-weight: 700;
  flex-shrink: 0;
  margin-top: 1px;
}

/* Plotly chart container */
.js-plotly-plot {
  border-radius: var(--radius-md) !important;
}

/* Image analysis result */
.image-analysis-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 20px 24px;
}

/* Severity badges */
.severity-critical { color: #EF4444; font-weight: 700; }
.severity-high { color: #F97316; font-weight: 700; }
.severity-medium { color: #FBBF24; font-weight: 700; }
.severity-low { color: #4ADE80; font-weight: 700; }

/* Loading dots animation */
@keyframes loading-dots {
  0%, 20% { content: '.'; }
  40% { content: '..'; }
  60%, 100% { content: '...'; }
}

/* Tooltip hover */
[title] { cursor: help; }

/* Section Header */
.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.section-header .section-icon {
  font-size: 20px;
}

.section-header .section-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
}

.section-header .section-subtitle {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}

/* Shimmer loading effect */
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.shimmer {
  background: linear-gradient(90deg,
    rgba(255,255,255,0.03) 25%,
    rgba(255,255,255,0.07) 50%,
    rgba(255,255,255,0.03) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-md);
}
</style>
"""


def inject_css():
    """Inject the custom CSS into the Streamlit app."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def sidebar_logo_html() -> str:
    return """
    <div class="sidebar-logo">
      <div class="logo-text">🏙️ VitaCity AI</div>
      <div class="logo-sub">Decision Intelligence Platform</div>
    </div>
    """


def page_hero_html(title: str, subtitle: str, icon: str = "🏙️") -> str:
    return f"""
    <div class="vitacity-hero">
      <div style="display:flex; align-items:flex-start; gap:16px;">
        <div style="font-size:40px; line-height:1;">{icon}</div>
        <div>
          <div class="vitacity-logo">{title}</div>
          <div class="vitacity-tagline">{subtitle}</div>
        </div>
      </div>
    </div>
    """


def kpi_card_html(icon: str, value: str, label: str, delta: str = "", delta_positive: bool = True, color: str = "#4CC9F0") -> str:
    delta_class = "positive" if delta_positive else "negative"
    delta_arrow = "▲" if delta_positive else "▼"
    delta_html = f'<div class="kpi-delta {delta_class}">{delta_arrow} {delta}</div>' if delta else ""
    return f"""
    <div class="kpi-card">
      <div class="kpi-icon" style="color:{color};">{icon}</div>
      <div class="kpi-value" style="color:{color};">{value}</div>
      <div class="kpi-label">{label}</div>
      {delta_html}
    </div>
    """


def confidence_badge_html(confidence: float) -> str:
    pct = int(confidence * 100)
    if confidence >= 0.85:
        cls = "confidence-high"
        label = "High Confidence"
    elif confidence >= 0.70:
        cls = "confidence-medium"
        label = "Medium Confidence"
    else:
        cls = "confidence-low"
        label = "Low Confidence"
    return f'<span class="confidence-badge {cls}">● {label} {pct}%</span>'


def domain_badge_html(domain: str, icon: str = "🏙️") -> str:
    return f'<span class="domain-badge">{icon} {domain}</span>'


def alert_card_html(title: str, description: str, severity: str, domain: str, timestamp: str) -> str:
    severity_icons = {"high": "🔴", "medium": "🟠", "low": "🟡"}
    icon = severity_icons.get(severity, "⚪")
    return f"""
    <div class="alert-card alert-{severity}">
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div style="font-weight:600; font-size:13px;">{icon} {title}</div>
        <div style="font-size:11px; color:var(--text-muted); white-space:nowrap; margin-left:12px;">{timestamp}</div>
      </div>
      <div style="margin-top:6px; color:var(--text-secondary); font-size:12px;">{description}</div>
      <div style="margin-top:6px; font-size:11px; color:var(--text-muted);">Domain: {domain}</div>
    </div>
    """


def source_citation_html(title: str, domain: str, similarity: float = 0.0) -> str:
    pct = int(similarity * 100) if similarity > 0 else ""
    relevance = f" · {pct}% match" if pct else ""
    return f"""
    <div class="source-citation">
      📄 <strong>{title}</strong> <span style="color:var(--text-muted);">· {domain}{relevance}</span>
    </div>
    """


def rec_card_html(text: str) -> str:
    return f'<div class="rec-card">{text}</div>'


def status_indicator_html(label: str, status: str = "green") -> str:
    return f"""
    <div style="display:inline-flex; align-items:center; gap:6px; font-size:12px; color:var(--text-secondary);">
      <span class="status-dot {status}"></span>{label}
    </div>
    """
