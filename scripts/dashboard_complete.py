"""
NSS X - Complete Dashboard for Saudi Arabia National Spatial Strategy
Integrates ALL workstreams: WS1-WS7 with real data.
Premium UI/UX with clean data presentation.
Run with: streamlit run scripts/dashboard_complete.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# Page config
st.set_page_config(
    page_title="NSS X - National Spatial Strategy",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CLEAN LIGHT THEME CSS
# ============================================================================
st.markdown("""
<style>
    /* ===== IMPORTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* ===== ROOT VARIABLES - LIGHT CLEAN THEME ===== */
    :root {
        --ksa-green: #006C35;
        --ksa-green-light: #00a650;
        --ksa-green-dark: #004d25;
        --accent: #006C35;
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --bg-card: #ffffff;
        --bg-card-hover: #f8f9fa;
        --bg-offwhite: #fafafa;
        --text-primary: #1a1a1a;
        --text-secondary: #6b7280;
        --text-muted: #9ca3af;
        --border-color: #e5e7eb;
        --border-light: #f0f0f0;
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.06);
        --shadow-lg: 0 8px 24px rgba(0,0,0,0.08);
        --radius-sm: 6px;
        --radius-md: 10px;
        --radius-lg: 14px;
    }
    
    /* ===== GLOBAL STYLES ===== */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: var(--bg-offwhite) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ===== HERO HEADER ===== */
    .hero-container {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 2rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
    }
    
    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        font-size: 1rem;
        color: var(--text-secondary);
        margin: 0.35rem 0 0 0;
        font-weight: 400;
    }
    
    .hero-badge {
        display: inline-block;
        background: var(--ksa-green);
        color: white;
        padding: 0.3rem 0.7rem;
        border-radius: 16px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-top: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    
    /* ===== KPI CARDS ===== */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 0.6rem;
        margin: 0.75rem 0;
    }
    
    .kpi-grid-compact {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .kpi-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 0.85rem 1rem;
        transition: all 0.15s ease;
    }
    
    .kpi-card:hover {
        border-color: var(--ksa-green);
        box-shadow: var(--shadow-md);
    }
    
    .kpi-card-compact {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-sm);
        padding: 0.6rem 0.8rem;
        transition: all 0.15s ease;
    }
    
    .kpi-icon {
        font-size: 1.1rem;
        margin-bottom: 0.25rem;
    }
    
    .kpi-label {
        font-size: 0.65rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 0.15rem;
    }
    
    .kpi-value {
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1.2;
    }
    
    .kpi-value-sm {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        line-height: 1.2;
    }
    
    .kpi-delta {
        font-size: 0.65rem;
        margin-top: 0.15rem;
    }
    
    .kpi-delta.positive { color: #16a34a; }
    .kpi-delta.negative { color: #dc2626; }
    .kpi-delta.neutral { color: var(--text-secondary); }
    
    /* ===== STAT MODULE GRID (NEW) ===== */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 0.6rem;
        margin: 0.75rem 0;
    }
    
    /* Inline row - all items in single line */
    .stat-row {
        display: flex;
        flex-wrap: nowrap;
        gap: 0.5rem;
        margin: 0.75rem 0;
        overflow-x: auto;
    }
    
    .stat-row .stat-module {
        flex: 1;
        min-width: 140px;
        max-width: 200px;
        padding: 0.6rem 0.75rem;
    }
    
    .stat-row .stat-icon {
        width: 32px;
        height: 32px;
        font-size: 0.95rem;
    }
    
    .stat-row .stat-value {
        font-size: 1rem;
    }
    
    .stat-row .stat-label {
        font-size: 0.6rem;
    }
    
    .stat-row .stat-sub {
        font-size: 0.6rem;
    }
    
    .stat-module {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 0.9rem 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .stat-module:hover {
        border-color: var(--ksa-green);
        box-shadow: var(--shadow-sm);
    }
    
    .stat-icon {
        width: 40px;
        height: 40px;
        border-radius: var(--radius-sm);
        background: var(--bg-secondary);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    
    .stat-icon.green { background: rgba(0, 108, 53, 0.1); }
    .stat-icon.blue { background: rgba(59, 130, 246, 0.1); }
    .stat-icon.amber { background: rgba(245, 158, 11, 0.1); }
    .stat-icon.red { background: rgba(239, 68, 68, 0.1); }
    .stat-icon.purple { background: rgba(139, 92, 246, 0.1); }
    
    .stat-content {
        flex: 1;
        min-width: 0;
    }
    
    .stat-label {
        font-size: 0.7rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.3px;
        margin-bottom: 0.1rem;
    }
    
    .stat-value {
        font-size: 1.15rem;
        font-weight: 600;
        color: var(--text-primary);
        line-height: 1.2;
    }
    
    .stat-sub {
        font-size: 0.7rem;
        color: var(--text-secondary);
        margin-top: 0.1rem;
    }
    
    /* ===== DATA MODULE CARDS (NEW) ===== */
    .module-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 0.75rem;
        margin: 0.75rem 0;
    }
    
    .module-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1rem;
    }
    
    .module-card:hover {
        border-color: var(--ksa-green);
    }
    
    .module-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.6rem;
    }
    
    .module-icon {
        font-size: 1rem;
    }
    
    .module-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .module-badge {
        margin-left: auto;
        background: var(--bg-secondary);
        color: var(--text-secondary);
        padding: 0.15rem 0.4rem;
        border-radius: 8px;
        font-size: 0.6rem;
        font-weight: 500;
    }
    
    .module-badge.green { background: rgba(0, 108, 53, 0.1); color: var(--ksa-green); }
    .module-badge.blue { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
    .module-badge.amber { background: rgba(245, 158, 11, 0.1); color: #d97706; }
    
    .module-content {
        font-size: 0.8rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }
    
    .module-stats {
        display: flex;
        gap: 1rem;
        margin-top: 0.6rem;
        padding-top: 0.6rem;
        border-top: 1px solid var(--border-light);
    }
    
    .module-stat {
        text-align: center;
    }
    
    .module-stat-value {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .module-stat-label {
        font-size: 0.6rem;
        color: var(--text-muted);
        text-transform: uppercase;
    }
    
    /* ===== COMPACT TABLE WRAPPER ===== */
    .table-wrapper {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        overflow: hidden;
    }
    
    .table-header {
        background: var(--bg-secondary);
        padding: 0.6rem 1rem;
        border-bottom: 1px solid var(--border-color);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .table-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .table-badge {
        background: var(--bg-card);
        color: var(--text-secondary);
        padding: 0.2rem 0.5rem;
        border-radius: 8px;
        font-size: 0.65rem;
        font-weight: 500;
    }
    
    /* ===== SECTION HEADERS ===== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin: 1.5rem 0 0.75rem 0;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid var(--border-light);
    }
    
    .section-header-icon {
        font-size: 1.1rem;
    }
    
    .section-header-text h2 {
        margin: 0;
        font-size: 1.15rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .section-header-text p {
        margin: 0;
        font-size: 0.8rem;
        color: var(--text-secondary);
    }
    
    /* ===== DATA CARDS ===== */
    .data-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        margin: 0.75rem 0;
    }
    
    .data-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid var(--border-light);
    }
    
    .data-card-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    
    .data-card-badge {
        background: var(--bg-secondary);
        color: var(--text-secondary);
        padding: 0.2rem 0.5rem;
        border-radius: 10px;
        font-size: 0.65rem;
        font-weight: 500;
    }
    
    /* ===== INFO BOXES ===== */
    .info-box {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
    }
    
    .info-box-title {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--ksa-green);
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 0.4rem;
    }
    
    .info-box-content {
        font-size: 0.9rem;
        color: var(--text-primary);
        line-height: 1.6;
    }
    
    /* ===== PROGRESS BARS ===== */
    .progress-container {
        margin: 0.4rem 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.25rem;
    }
    
    .progress-label span:first-child {
        font-size: 0.8rem;
        color: var(--text-primary);
    }
    
    .progress-label span:last-child {
        font-size: 0.8rem;
        color: var(--ksa-green);
        font-weight: 600;
    }
    
    .progress-bar {
        height: 6px;
        background: var(--border-color);
        border-radius: 3px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: var(--ksa-green);
        border-radius: 3px;
        transition: width 0.4s ease;
    }
    
    /* ===== SIDEBAR STYLING ===== */
    .sidebar-section {
        background: var(--bg-card);
        border-radius: var(--radius-md);
        padding: 0.75rem;
        margin-bottom: 0.75rem;
    }
    
    .sidebar-section-title {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        color: var(--text-muted);
        margin-bottom: 0.5rem;
    }
    
    .ws-item {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem;
        margin: 0.15rem 0;
        border-radius: var(--radius-sm);
    }
    
    .ws-item:hover {
        background: var(--bg-secondary);
    }
    
    .ws-item-status {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #16a34a;
    }
    
    .ws-item-name {
        flex: 1;
        font-size: 0.8rem;
        color: var(--text-primary);
    }
    
    .ws-item-pct {
        font-size: 0.7rem;
        color: var(--text-secondary);
    }
    
    /* ===== TABLE STYLING ===== */
    .stDataFrame {
        font-size: 0.75rem !important;
    }
    
    .stDataFrame > div > div > div > div {
        font-size: 0.75rem !important;
    }
    
    div[data-testid="stDataFrame"] {
        width: 100% !important;
    }
    
    div[data-testid="stDataFrame"] > div {
        width: 100% !important;
    }
    
    .dataframe {
        font-size: 0.75rem !important;
        width: 100% !important;
    }
    
    .dataframe th {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 0.6rem !important;
        letter-spacing: 0.3px !important;
        border-bottom: 2px solid var(--border-color) !important;
        white-space: nowrap !important;
        padding: 0.4rem 0.5rem !important;
    }
    
    .dataframe td {
        border-color: var(--border-light) !important;
        padding: 0.35rem 0.5rem !important;
        white-space: nowrap !important;
    }
    
    .dataframe tr:hover td {
        background: var(--bg-secondary) !important;
    }
    
    /* ===== TAB STYLING ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm);
        padding: 0.5rem 1rem;
        font-size: 0.8rem;
        font-weight: 500;
        color: var(--text-secondary);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--ksa-green) !important;
        color: white !important;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 1.5rem 0;
        margin-top: 2rem;
        border-top: 1px solid var(--border-light);
    }
    
    .footer-brand {
        font-size: 1rem;
        font-weight: 600;
        color: var(--ksa-green);
    }
    
    .footer-text {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-top: 0.35rem;
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .hero-title { font-size: 1.5rem; }
        .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# DATA LOADING
# ============================================================================
DATA_DIR = Path(__file__).parent.parent / "02_analytics"
WS2_DIR = DATA_DIR / "ws2_outputs"
WS3_DIR = DATA_DIR / "ws3_outputs"
WS4_DIR = DATA_DIR / "ws4_outputs"
WS5_DIR = DATA_DIR / "ws5_outputs"
WS6_DIR = DATA_DIR / "ws6_outputs"
WS7_DIR = DATA_DIR / "ws7_outputs"


@st.cache_data
def load_ws2_data():
    """Load WS2 retrospective data."""
    try:
        with open(WS2_DIR / "WS2_RETROSPECTIVE_REPORT.json", 'r', encoding='utf-8') as f:
            report = json.load(f)
        continuity = pd.read_csv(WS2_DIR / "continuity_change_matrix.csv")
        return {"report": report, "continuity": continuity}
    except Exception as e:
        return None


@st.cache_data
def load_ws3_data():
    """Load WS3 benchmarking data."""
    try:
        with open(WS3_DIR / "WS3_BENCHMARKING_REPORT.json", 'r', encoding='utf-8') as f:
            report = json.load(f)
        methodology = pd.read_csv(WS3_DIR / "methodology_comparison_matrix.csv")
        principles = pd.read_csv(WS3_DIR / "country_x_fit_design_principles.csv")
        return {"report": report, "methodology": methodology, "principles": principles}
    except Exception as e:
        return None


@st.cache_data
def load_ws4_data():
    """Load WS4 sectoral/regional data."""
    try:
        with open(WS4_DIR / "WS4_SECTORAL_REGIONAL_REPORT.json", 'r', encoding='utf-8') as f:
            report = json.load(f)
        diagnostics = pd.read_csv(WS4_DIR / "regional_diagnostics_summary.csv")
        conflicts = pd.read_csv(WS4_DIR / "land_use_conflict_matrix.csv")
        measures = pd.read_csv(WS4_DIR / "corrective_measures_playbook.csv")
        return {"report": report, "diagnostics": diagnostics, "conflicts": conflicts, "measures": measures}
    except Exception as e:
        return None


@st.cache_data
def load_ws5_data():
    """Load WS5 scenario data."""
    try:
        with open(WS5_DIR / "WS5_SCENARIO_REPORT.json", 'r', encoding='utf-8') as f:
            report = json.load(f)
        comparison_2030 = pd.read_csv(WS5_DIR / "scenario_comparison_2030.csv")
        comparison_2050 = pd.read_csv(WS5_DIR / "scenario_comparison_2050.csv")
        risks = pd.read_csv(WS5_DIR / "risk_heatmap_by_region.csv")
        opportunities = pd.read_csv(WS5_DIR / "opportunity_heatmap_by_region.csv")
        return {
            "report": report, 
            "comparison_2030": comparison_2030,
            "comparison_2050": comparison_2050,
            "risks": risks,
            "opportunities": opportunities
        }
    except Exception as e:
        return None


@st.cache_data
def load_ws6_data():
    """Load WS6 NSS draft data."""
    try:
        with open(WS6_DIR / "WS6_NSS_DRAFT_REPORT.json", 'r', encoding='utf-8') as f:
            report = json.load(f)
        nodes = pd.read_csv(WS6_DIR / "strategic_nodes.csv")
        corridors = pd.read_csv(WS6_DIR / "development_corridors.csv")
        zones = pd.read_csv(WS6_DIR / "functional_zones.csv")
        objectives = pd.read_csv(WS6_DIR / "regional_objectives.csv")
        investments = pd.read_csv(WS6_DIR / "investment_priorities.csv")
        return {
            "report": report,
            "nodes": nodes,
            "corridors": corridors,
            "zones": zones,
            "objectives": objectives,
            "investments": investments
        }
    except Exception as e:
        return None


@st.cache_data
def load_ws7_data():
    """Load WS7 governance data."""
    try:
        with open(WS7_DIR / "WS7_GOVERNANCE_REPORT.json", 'r', encoding='utf-8') as f:
            report = json.load(f)
        bodies = pd.read_csv(WS7_DIR / "governance_bodies.csv")
        processes = pd.read_csv(WS7_DIR / "decision_processes.csv")
        raci = pd.read_csv(WS7_DIR / "raci_matrix.csv")
        kpis = pd.read_csv(WS7_DIR / "kpi_framework.csv")
        mechanisms = pd.read_csv(WS7_DIR / "monitoring_mechanisms.csv")
        return {
            "report": report,
            "bodies": bodies,
            "processes": processes,
            "raci": raci,
            "kpis": kpis,
            "mechanisms": mechanisms
        }
    except Exception as e:
        return None


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def render_kpi_card(icon: str, label: str, value: str, delta: str = None, delta_type: str = "neutral"):
    """Render a styled KPI card."""
    delta_html = ""
    if delta:
        delta_class = delta_type
        delta_icon = "↑" if delta_type == "positive" else "↓" if delta_type == "negative" else "→"
        delta_html = f'<div class="kpi-delta {delta_class}">{delta_icon} {delta}</div>'
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """


def render_section_header(icon: str, title: str, subtitle: str = ""):
    """Render a styled section header."""
    return f"""
    <div class="section-header">
        <div class="section-header-icon">{icon}</div>
        <div class="section-header-text">
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
    </div>
    """


def render_info_box(title: str, content: str):
    """Render an info box."""
    return f"""
    <div class="info-box">
        <div class="info-box-title">{title}</div>
        <div class="info-box-content">{content}</div>
    </div>
    """


def render_progress_bar(label: str, value: int, max_value: int = 100):
    """Render a progress bar."""
    pct = min(100, int((value / max_value) * 100))
    return f"""
    <div class="progress-container">
        <div class="progress-label">
            <span>{label}</span>
            <span>{pct}%</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {pct}%;"></div>
        </div>
    </div>
    """


def render_stat_module(icon: str, label: str, value: str, subtitle: str = "", color: str = ""):
    """Render a compact stat module for inline display."""
    color_class = f" {color}" if color else ""
    sub_html = f'<div class="stat-sub">{subtitle}</div>' if subtitle else ""
    return f"""
    <div class="stat-module">
        <div class="stat-icon{color_class}">{icon}</div>
        <div class="stat-content">
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
            {sub_html}
        </div>
    </div>
    """


def render_module_card(icon: str, title: str, content: str, badge: str = "", badge_color: str = "", stats: list = None):
    """Render a data module card with optional stats."""
    badge_html = ""
    if badge:
        badge_class = f" {badge_color}" if badge_color else ""
        badge_html = f'<span class="module-badge{badge_class}">{badge}</span>'
    
    stats_html = ""
    if stats:
        stats_items = "".join([
            f'<div class="module-stat"><div class="module-stat-value">{s["value"]}</div><div class="module-stat-label">{s["label"]}</div></div>'
            for s in stats
        ])
        stats_html = f'<div class="module-stats">{stats_items}</div>'
    
    return f"""
    <div class="module-card">
        <div class="module-header">
            <span class="module-icon">{icon}</span>
            <span class="module-title">{title}</span>
            {badge_html}
        </div>
        <div class="module-content">{content}</div>
        {stats_html}
    </div>
    """


def get_chart_layout(title: str = "", height: int = 400):
    """Get consistent chart layout for light theme."""
    return dict(
        title=dict(text=title, font=dict(size=14, color='#1a1a1a'), x=0, xanchor='left'),
        font=dict(family="Inter, sans-serif", color='#6b7280', size=11),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=height,
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
            font=dict(size=10)
        ),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.06)',
            zerolinecolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.06)',
            zerolinecolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=10)
        )
    )


KSA_COLORS = ['#006C35', '#16a34a', '#22c55e', '#4ade80', '#86efac', '#3b82f6', '#6366f1']


# ============================================================================
# RENDER FUNCTIONS
# ============================================================================

def render_header():
    """Render hero header."""
    st.markdown("""
    <div class="hero-container">
        <p class="hero-title">🇸🇦 NSS X - National Spatial Strategy</p>
        <p class="hero-subtitle">Kingdom of Saudi Arabia • Vision 2030 • Horizon 2050</p>
        <span class="hero-badge">✓ Complete Tender Deliverables</span>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar with workstream status."""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">Workstream Progress</div>
        """, unsafe_allow_html=True)
        
        workstreams = [
            ("WS1", "Data Collection", 95),
            ("WS2", "NSS Review", 100),
            ("WS3", "Benchmarking", 100),
            ("WS4", "Sectoral Analysis", 100),
            ("WS5", "Scenarios", 100),
            ("WS6", "NSS Draft", 100),
            ("WS7", "Governance", 100),
        ]
        
        for ws_id, name, pct in workstreams:
            st.markdown(f"""
            <div class="ws-item">
                <div class="ws-item-status"></div>
                <span class="ws-item-name"><strong>{ws_id}</strong> {name}</span>
                <span class="ws-item-pct">{pct}%</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick stats
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        col1.metric("Deliverables", "45+")
        col2.metric("KPIs", "26")
        col1.metric("Investment", "1.4T SAR")
        col2.metric("Regions", "13")
        
        st.markdown("---")
        st.markdown("### 🔗 Resources")
        st.markdown("""
        - [Vision 2030](https://vision2030.gov.sa)
        - [GASTAT](https://stats.gov.sa)
        """)


def render_overview():
    """Render overview tab with premium styling."""
    ws6 = load_ws6_data()
    
    # Compact KPI modules using Streamlit columns
    cols = st.columns(5)
    with cols[0]:
        st.markdown(render_stat_module("👥", "Population 2024", "34.1M", "+2.3% YoY", "green"), unsafe_allow_html=True)
    with cols[1]:
        st.markdown(render_stat_module("💰", "GDP 2024", "$1.1T", "+4.5%", "green"), unsafe_allow_html=True)
    with cols[2]:
        st.markdown(render_stat_module("🗺️", "Regions", "13", "All Covered", "blue"), unsafe_allow_html=True)
    with cols[3]:
        st.markdown(render_stat_module("🏙️", "Strategic Nodes", "20", "Tier 1-3", "amber"), unsafe_allow_html=True)
    with cols[4]:
        st.markdown(render_stat_module("📈", "Investment", "SAR 1.4T", "2025-2050", "purple"), unsafe_allow_html=True)
    
    # Vision Statement
    if ws6:
        st.markdown(render_section_header("🎯", "NSS Vision 2050", "Strategic direction for spatial development"), unsafe_allow_html=True)
        
        vision = ws6['report'].get('section_1_vision', {}).get('vision_statement', '')
        if vision:
            truncated = vision[:600] + "..." if len(vision) > 600 else vision
            st.markdown(render_info_box("VISION STATEMENT", truncated), unsafe_allow_html=True)
    
    # Two columns for principles and objectives
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(render_section_header("🧭", "Guiding Principles", "Foundation for spatial planning"), unsafe_allow_html=True)
        
        if ws6:
            principles = ws6['report'].get('section_1_vision', {}).get('guiding_principles', [])
            for i, p in enumerate(principles[:5]):
                st.markdown(f"""
                <div class="data-card" style="padding: 1rem; margin: 0.5rem 0;">
                    <strong style="color: var(--ksa-green-light);">{i+1}. {p.get('principle', '')}</strong>
                    <p style="color: var(--text-secondary); font-size: 0.85rem; margin: 0.5rem 0 0 0;">
                        {p.get('description', '')[:120]}...
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(render_section_header("🎯", "Strategic Objectives", "Measurable targets for 2050"), unsafe_allow_html=True)
        
        if ws6:
            objectives = ws6['report'].get('section_1_vision', {}).get('strategic_objectives', [])
            for obj in objectives[:5]:
                st.markdown(f"""
                <div class="data-card" style="padding: 1rem; margin: 0.5rem 0;">
                    <strong style="color: var(--ksa-gold);">{obj.get('id', '')}</strong>
                    <p style="color: var(--text-primary); font-size: 0.9rem; margin: 0.25rem 0;">{obj.get('objective', '')}</p>
                    <p style="color: var(--text-secondary); font-size: 0.8rem; margin: 0;">
                        Target: {obj.get('target_2050', '')[:80]}
                    </p>
                </div>
                """, unsafe_allow_html=True)


def render_ws2_retrospective():
    """Render WS2 retrospective analysis with compact modules."""
    st.markdown(render_section_header("📜", "NSS 2001 & 2030 Review", "Analysis of existing policies and recommendations"), unsafe_allow_html=True)
    
    ws2 = load_ws2_data()
    if not ws2:
        st.warning("WS2 data not available. Run: `python src/analysis/ws2_comprehensive.py`")
        return
    
    continuity = ws2['continuity']
    
    # Summary metrics
    maintain = len(continuity[continuity['Recommendation'] == 'MAINTAIN'])
    strengthen = len(continuity[continuity['Recommendation'] == 'STRENGTHEN'])
    modify = len(continuity[continuity['Recommendation'] == 'MODIFY'])
    new_items = len(continuity[continuity['Recommendation'] == 'NEW'])
    discontinue = len(continuity[continuity['Recommendation'] == 'DISCONTINUE'])
    total = len(continuity)
    
    # Compact stat modules using st.columns
    cols = st.columns(5)
    with cols[0]:
        st.markdown(render_stat_module("✓", "Maintain", str(maintain), f"{maintain*100//total}% of policies", "green"), unsafe_allow_html=True)
    with cols[1]:
        st.markdown(render_stat_module("⬆", "Strengthen", str(strengthen), "Enhance existing", "blue"), unsafe_allow_html=True)
    with cols[2]:
        st.markdown(render_stat_module("↻", "Modify", str(modify), "Update approach", "amber"), unsafe_allow_html=True)
    with cols[3]:
        st.markdown(render_stat_module("✚", "New", str(new_items), "Introduce fresh", "purple"), unsafe_allow_html=True)
    with cols[4]:
        st.markdown(render_stat_module("✗", "Discontinue", str(discontinue), "Phase out", "red"), unsafe_allow_html=True)
    
    # Modern visualizations in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Treemap for hierarchical distribution
        rec_counts = continuity['Recommendation'].value_counts().reset_index()
        rec_counts.columns = ['Recommendation', 'Count']
        rec_counts['Percentage'] = (rec_counts['Count'] / rec_counts['Count'].sum() * 100).round(1)
        
        fig = px.treemap(
            rec_counts,
            path=['Recommendation'],
            values='Count',
            color='Recommendation',
            color_discrete_map={
                'MAINTAIN': '#22c55e',
                'STRENGTHEN': '#3b82f6',
                'MODIFY': '#f59e0b',
                'NEW': '#8b5cf6',
                'DISCONTINUE': '#ef4444'
            },
            custom_data=['Percentage']
        )
        fig.update_traces(
            texttemplate="<b>%{label}</b><br>%{value} policies<br>%{customdata[0]}%",
            textfont=dict(size=13, color='white'),
            marker=dict(cornerradius=8)
        )
        fig.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            title=dict(text="Policy Distribution", font=dict(size=13, color='#1a1a1a'), x=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Heatmap for Priority x Recommendation matrix
        priority_rec = continuity.groupby(['Priority', 'Recommendation']).size().unstack(fill_value=0)
        priority_order = ['High', 'Medium', 'Low'] if 'High' in priority_rec.index else priority_rec.index.tolist()
        rec_order = ['MAINTAIN', 'STRENGTHEN', 'MODIFY', 'NEW', 'DISCONTINUE']
        rec_order = [r for r in rec_order if r in priority_rec.columns]
        priority_rec = priority_rec.reindex(index=[p for p in priority_order if p in priority_rec.index], columns=rec_order)
        
        fig2 = px.imshow(
            priority_rec.values,
            x=priority_rec.columns,
            y=priority_rec.index,
            color_continuous_scale=['#f0f9ff', '#006C35'],
            aspect='auto',
            text_auto=True
        )
        fig2.update_traces(
            texttemplate='%{z}',
            textfont=dict(size=14, color='#1a1a1a'),
            hovertemplate='Priority: %{y}<br>Recommendation: %{x}<br>Count: %{z}<extra></extra>'
        )
        fig2.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title=dict(text="Priority × Recommendation Matrix", font=dict(size=13, color='#1a1a1a'), x=0),
            xaxis=dict(title='', tickfont=dict(size=10)),
            yaxis=dict(title='', tickfont=dict(size=11)),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Data table with expander
    with st.expander("📋 View Full Continuity Matrix", expanded=False):
        st.dataframe(continuity, use_container_width=True, height=350)


def render_ws3_benchmarking():
    """Render WS3 international benchmarking with improved visualizations."""
    st.markdown(render_section_header("🌍", "International Benchmarking", "Learning from global best practices"), unsafe_allow_html=True)
    
    ws3 = load_ws3_data()
    if not ws3:
        st.warning("WS3 data not available. Run: `python src/analysis/ws3_benchmarking.py`")
        return
    
    report = ws3['report']
    methodology = ws3['methodology']
    principles = ws3['principles']
    
    # Use methodology data for country stats (more reliable than report JSON)
    if not methodology.empty and 'Country' in methodology.columns:
        country_icons = {"Singapore": "🇸🇬", "Netherlands": "🇳🇱", "UAE": "🇦🇪", "South Korea": "🇰🇷", "Malaysia": "🇲🇾", "Japan": "🇯🇵", "Germany": "🇩🇪"}
        country_lessons = {
            "Singapore": "Compact city-state with world-class integrated planning",
            "Netherlands": "Water management & polycentric urban development",
            "UAE": "Rapid urbanization & economic diversification model", 
            "South Korea": "Technology-driven spatial development",
            "Malaysia": "Regional corridor approach & industrial zones"
        }
        
        # Country stat modules inline
        countries_list = methodology['Country'].tolist()
        if countries_list:
            cols = st.columns(len(countries_list))
            avg_col = 'Average' if 'Average' in methodology.columns else None
            
            for i, country in enumerate(countries_list):
                row = methodology[methodology['Country'] == country].iloc[0]
                avg_score = row[avg_col] if avg_col else 0
                icon = country_icons.get(country, "🌍")
                
                with cols[i]:
                    st.markdown(render_stat_module(
                        icon, 
                        country, 
                        f"{avg_score:.1f}" if isinstance(avg_score, (int, float)) else str(avg_score),
                        country_lessons.get(country, "Benchmark country")[:35],
                        "green" if avg_score >= 4 else "blue" if avg_score >= 3 else "amber"
                    ), unsafe_allow_html=True)
    
    # Modern Methodology Comparison - Heatmap instead of Radar
    st.markdown(render_section_header("📊", "Methodology Comparison", "Multi-dimensional analysis across criteria"), unsafe_allow_html=True)
    
    if not methodology.empty and 'Country' in methodology.columns:
        categories = [col for col in methodology.columns if col not in ['Country', 'Average']]
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Heatmap for methodology comparison (much cleaner than radar)
            heatmap_data = methodology.set_index('Country')[categories]
            
            fig = px.imshow(
                heatmap_data.values,
                x=categories,
                y=heatmap_data.index,
                color_continuous_scale=['#fef3c7', '#f59e0b', '#006C35'],
                aspect='auto',
                text_auto='.1f'
            )
            fig.update_traces(
                texttemplate='%{z:.1f}',
                textfont=dict(size=11, color='#1a1a1a'),
                hovertemplate='%{y}<br>%{x}: %{z:.1f}<extra></extra>'
            )
            fig.update_layout(
                height=280,
                margin=dict(l=10, r=10, t=35, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title=dict(text="Score Matrix (1-5 scale)", font=dict(size=13, color='#1a1a1a'), x=0),
                xaxis=dict(title='', tickfont=dict(size=9), tickangle=30),
                yaxis=dict(title='', tickfont=dict(size=11)),
                coloraxis=dict(
                    colorbar=dict(
                        title='Score',
                        thickness=12,
                        len=0.7,
                        tickfont=dict(size=9)
                    )
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Overall Ranking - Horizontal bars
            if 'Average' in methodology.columns:
                meth_sorted = methodology.sort_values('Average', ascending=True)
                
                fig_bar = go.Figure()
                colors = ['#006C35' if v >= 4 else '#3b82f6' if v >= 3 else '#f59e0b' for v in meth_sorted['Average']]
                
                fig_bar.add_trace(go.Bar(
                    y=meth_sorted['Country'],
                    x=meth_sorted['Average'],
                    orientation='h',
                    marker=dict(color=colors, cornerradius=6),
                    text=[f"{v:.2f}" for v in meth_sorted['Average']],
                    textposition='inside',
                    textfont=dict(size=12, color='white')
                ))
                
                fig_bar.update_layout(
                    height=280,
                    margin=dict(l=10, r=10, t=35, b=10),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    title=dict(text="Overall Ranking", font=dict(size=13, color='#1a1a1a'), x=0),
                    xaxis=dict(title='', range=[0, 5], tickfont=dict(size=10), gridcolor='rgba(0,0,0,0.05)'),
                    yaxis=dict(title='', tickfont=dict(size=11)),
                    showlegend=False
                )
                st.plotly_chart(fig_bar, use_container_width=True)
    
    # Design Principles - Better visualization
    st.markdown(render_section_header("🎨", "Design Principles for KSA", "Adapted from international benchmarks"), unsafe_allow_html=True)
    
    if not principles.empty:
        # Group by category for treemap
        if 'Category' in principles.columns and 'Priority' in principles.columns:
            # Priority distribution by category
            cat_priority = principles.groupby(['Category', 'Priority']).size().reset_index(name='Count')
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Treemap for categories
                fig_tree = px.treemap(
                    principles,
                    path=['Category', 'Approach'] if 'Approach' in principles.columns else ['Category'],
                    color='Priority',
                    color_discrete_map={'CRITICAL': '#ef4444', 'HIGH': '#f59e0b', 'MEDIUM': '#22c55e'},
                    hover_data=['Principle'] if 'Principle' in principles.columns else None
                )
                fig_tree.update_layout(
                    height=350,
                    margin=dict(l=10, r=10, t=30, b=10),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif", size=11)
                )
                fig_tree.update_traces(
                    textinfo='label+value',
                    textfont=dict(size=11)
                )
                st.plotly_chart(fig_tree, use_container_width=True)
            
            with col2:
                # Summary stats
                critical = len(principles[principles['Priority'] == 'CRITICAL'])
                high = len(principles[principles['Priority'] == 'HIGH'])
                medium = len(principles[principles['Priority'] == 'MEDIUM'])
                
                st.markdown(f"""
                <div class="data-card" style="height: 100%;">
                    <div class="data-card-header" style="border-bottom: none; padding-bottom: 0;">
                        <h3 class="data-card-title">Priority Breakdown</h3>
                    </div>
                    {render_progress_bar("Critical", critical, len(principles))}
                    {render_progress_bar("High", high, len(principles))}
                    {render_progress_bar("Medium", medium, len(principles))}
                    <div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid var(--border-light);">
                        <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.3rem;">Total Principles</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: var(--ksa-green);">{len(principles)}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with st.expander("📋 View All Design Principles"):
            # Show key columns only
            display_cols = ['ID', 'Principle', 'Category', 'Priority', 'Approach']
            display_cols = [c for c in display_cols if c in principles.columns]
            st.dataframe(principles[display_cols], use_container_width=True, hide_index=True, height=300)


def render_ws4_sectoral():
    """Render WS4 sectoral and regional analysis."""
    st.markdown(render_section_header("🏭", "Sectoral & Regional Analysis", "Comprehensive diagnostic of all sectors and regions"), unsafe_allow_html=True)
    
    ws4 = load_ws4_data()
    if not ws4:
        st.warning("WS4 data not available. Run: `python src/analysis/ws4_comprehensive.py`")
        return
    
    tab1, tab2, tab3 = st.tabs(["📊 Regional Diagnostics", "⚔️ Land Use Conflicts", "🔧 Corrective Measures"])
    
    with tab1:
        diagnostics = ws4['diagnostics']
        
        if 'Region' in diagnostics.columns:
            # Get only truly numeric columns (exclude text columns like Water_Availability)
            numeric_cols = []
            for col in diagnostics.columns:
                if col != 'Region':
                    # Check if column has actual numeric values (not text like "critical", "high")
                    try:
                        col_data = pd.to_numeric(diagnostics[col], errors='coerce')
                        if col_data.notna().sum() > 0 and col_data.notna().sum() == len(diagnostics):
                            numeric_cols.append(col)
                    except:
                        pass
            
            if numeric_cols:
                # Normalize each column to 0-100 for fair comparison
                normalized_data = diagnostics[numeric_cols].copy()
                for col in numeric_cols:
                    col_min = normalized_data[col].min()
                    col_max = normalized_data[col].max()
                    if col_max > col_min:
                        normalized_data[col] = ((normalized_data[col] - col_min) / (col_max - col_min) * 100).round(1)
                
                fig = px.imshow(
                    normalized_data.values,
                    x=numeric_cols,
                    y=diagnostics['Region'].values,
                    color_continuous_scale='RdYlGn',  # Red-Yellow-Green diverging
                    aspect='auto',
                    text_auto='.0f',
                    zmin=0,
                    zmax=100
                )
                fig.update_traces(
                    texttemplate='%{z:.0f}',
                    textfont=dict(size=10, color='#1a1a1a'),
                    hovertemplate='Region: %{y}<br>Indicator: %{x}<br>Score: %{z:.0f}%<extra></extra>'
                )
                fig.update_layout(
                    height=450,
                    margin=dict(l=10, r=10, t=40, b=10),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    title=dict(text="Regional Performance (Normalized 0-100)", font=dict(size=13, color='#1a1a1a'), x=0),
                    xaxis=dict(title='', tickfont=dict(size=9), tickangle=35),
                    yaxis=dict(title='', tickfont=dict(size=10)),
                    coloraxis=dict(
                        colorbar=dict(
                            title='Score',
                            thickness=12,
                            len=0.6,
                            tickfont=dict(size=9)
                        )
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 View Full Diagnostics Data"):
            st.dataframe(diagnostics, use_container_width=True, hide_index=True)
    
    with tab2:
        conflicts = ws4['conflicts']
        
        # Check if conflicts has proper structure for heatmap
        if len(conflicts.columns) > 1:
            # Try to create a conflict intensity visualization
            first_col = conflicts.columns[0]
            numeric_cols = conflicts.select_dtypes(include=[np.number]).columns.tolist()
            
            if numeric_cols and first_col not in numeric_cols:
                # Create heatmap of conflicts
                fig = px.imshow(
                    conflicts[numeric_cols].values,
                    x=numeric_cols,
                    y=conflicts[first_col].values if first_col in conflicts.columns else None,
                    color_continuous_scale=['#dcfce7', '#fef3c7', '#fecaca', '#ef4444'],
                    aspect='auto',
                    text_auto=True
                )
                fig.update_traces(
                    texttemplate='%{z}',
                    textfont=dict(size=11),
                    hovertemplate='%{y}<br>%{x}: %{z}<extra></extra>'
                )
                fig.update_layout(
                    height=400,
                    margin=dict(l=10, r=10, t=40, b=10),
                    paper_bgcolor='rgba(0,0,0,0)',
                    title=dict(text="Land Use Conflict Intensity", font=dict(size=13, color='#1a1a1a'), x=0),
                    xaxis=dict(title='', tickfont=dict(size=9), tickangle=30),
                    yaxis=dict(title='', tickfont=dict(size=10)),
                    coloraxis_showscale=True
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.markdown(render_info_box("CONFLICT MATRIX", "Analysis of land use conflicts across sectors and regions"), unsafe_allow_html=True)
        
        with st.expander("📋 View Full Conflict Matrix"):
            st.dataframe(conflicts, use_container_width=True, hide_index=True)
    
    with tab3:
        measures = ws4['measures']
        
        # Group measures by Type (REGULATORY, INVESTMENT, etc.) 
        group_col = None
        for col in ['Type', 'Category', 'Sector']:
            if col in measures.columns:
                group_col = col
                break
        
        priority_col = None
        for col in ['Priority', 'PRIORITY']:
            if col in measures.columns:
                priority_col = col
                break
        
        if group_col and priority_col:
            # Create treemap of measures
            # Ensure Priority values are mapped correctly
            priority_map = {
                'CRITICAL': '#dc2626', 'Critical': '#dc2626', 'critical': '#dc2626',
                'HIGH': '#ef4444', 'High': '#ef4444', 'high': '#ef4444',
                'MEDIUM': '#f59e0b', 'Medium': '#f59e0b', 'medium': '#f59e0b',
                'LOW': '#22c55e', 'Low': '#22c55e', 'low': '#22c55e'
            }
            
            # Use Title if available for leaf nodes
            path_cols = [group_col]
            if 'Title' in measures.columns:
                path_cols.append('Title')
            elif 'Measure' in measures.columns:
                path_cols.append('Measure')
            
            fig = px.treemap(
                measures,
                path=path_cols,
                color=priority_col,
                color_discrete_map=priority_map,
                hover_data=['Conflict'] if 'Conflict' in measures.columns else None
            )
            fig.update_traces(
                textfont=dict(size=11, color='white'),
                marker=dict(cornerradius=6),
                hovertemplate='<b>%{label}</b><br>Priority: %{color}<extra></extra>'
            )
            fig.update_layout(
                height=420,
                margin=dict(l=10, r=10, t=40, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                title=dict(text="Corrective Measures by Type & Priority", font=dict(size=13, color='#1a1a1a'), x=0)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary stats inline
            if priority_col:
                priority_counts = measures[priority_col].value_counts()
                critical = priority_counts.get('CRITICAL', 0) + priority_counts.get('Critical', 0)
                high = priority_counts.get('HIGH', 0) + priority_counts.get('High', 0)
                medium = priority_counts.get('MEDIUM', 0) + priority_counts.get('Medium', 0)
                
                cols = st.columns(4)
                with cols[0]:
                    st.markdown(render_stat_module("📋", "Total Measures", str(len(measures)), "Interventions planned", "green"), unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(render_stat_module("🔴", "Critical", str(critical), "Immediate action", "red"), unsafe_allow_html=True)
                with cols[2]:
                    st.markdown(render_stat_module("🟠", "High Priority", str(high), "Short-term focus", "amber"), unsafe_allow_html=True)
                with cols[3]:
                    st.markdown(render_stat_module("🟡", "Medium", str(medium), "Medium-term plan", "blue"), unsafe_allow_html=True)
        else:
            st.markdown(render_info_box("CORRECTIVE MEASURES", "Playbook of interventions to address identified issues"), unsafe_allow_html=True)
            st.dataframe(measures, use_container_width=True, hide_index=True)
        
        with st.expander("📋 View Full Measures Playbook"):
            st.dataframe(measures, use_container_width=True, hide_index=True)


def render_ws5_scenarios():
    """Render WS5 scenario planning with improved visualizations."""
    st.markdown(render_section_header("🔮", "Scenario Planning", "Alternative futures and strategic pathways"), unsafe_allow_html=True)
    
    ws5 = load_ws5_data()
    if not ws5:
        st.warning("WS5 data not available. Run: `python src/analysis/ws5_comprehensive.py`")
        return
    
    tab1, tab2, tab3 = st.tabs(["📈 Scenario Comparison", "⚠️ Risk Heatmap", "💎 Opportunity Heatmap"])
    
    with tab1:
        comparison_2030 = ws5['comparison_2030']
        comparison_2050 = ws5['comparison_2050']
        
        # Scenario Cards with key metrics
        if 'Scenario' in comparison_2030.columns:
            st.markdown("#### 2030 Projections", unsafe_allow_html=True)
            
            scenario_colors = {
                'Baseline': 'amber',
                'Vision 2030 Achievement': 'green', 
                'Accelerated Transformation': 'blue',
                'Conservative': 'red'
            }
            scenario_icons = {
                'Baseline': '📊',
                'Vision 2030 Achievement': '🎯',
                'Accelerated Transformation': '🚀',
                'Conservative': '📉'
            }
            
            # Build scenario data list
            scenarios_2030 = []
            for _, row in comparison_2030.iterrows():
                scenario = row['Scenario']
                pop = row.get('Population (M)', 'N/A')
                gdp = row.get('GDP ($B)', 'N/A')
                
                color = 'amber'
                icon = '📊'
                for key in scenario_colors:
                    if key.lower() in scenario.lower():
                        color = scenario_colors[key]
                        icon = scenario_icons.get(key, '📊')
                        break
                
                pop_str = f"{pop:.1f}M" if isinstance(pop, (int, float)) else str(pop)
                gdp_str = f"${gdp:.0f}B" if isinstance(gdp, (int, float)) else str(gdp)
                scenarios_2030.append((icon, scenario[:25] + "..." if len(scenario) > 25 else scenario, pop_str, gdp_str, color))
            
            # Render with st.columns
            if scenarios_2030:
                cols = st.columns(len(scenarios_2030))
                for i, (icon, name, pop_str, gdp_str, color) in enumerate(scenarios_2030):
                    with cols[i]:
                        st.markdown(render_stat_module(icon, name, pop_str, f"GDP: {gdp_str}", color), unsafe_allow_html=True)
            
            # Visual comparison chart
            numeric_cols = ['Population (M)', 'GDP ($B)', 'Oil Share (%)', 'Urban (%)', 'Renewable GW']
            numeric_cols = [c for c in numeric_cols if c in comparison_2030.columns]
            
            if numeric_cols:
                # Create grouped bar chart
                fig = go.Figure()
                colors_list = ['#006C35', '#3b82f6', '#8b5cf6', '#ef4444']
                
                for i, (_, row) in enumerate(comparison_2030.iterrows()):
                    scenario = row['Scenario'][:20] + "..." if len(row['Scenario']) > 20 else row['Scenario']
                    fig.add_trace(go.Bar(
                        name=scenario,
                        x=numeric_cols[:4],
                        y=[row[c] for c in numeric_cols[:4]],
                        marker_color=colors_list[i % len(colors_list)]
                    ))
                
                layout = get_chart_layout("Key Metrics Comparison - 2030", height=320)
                layout['legend'] = dict(orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5, bgcolor='rgba(0,0,0,0)', font=dict(size=10))
                layout['barmode'] = 'group'
                fig.update_layout(**layout)
                st.plotly_chart(fig, use_container_width=True)
        
        # 2050 Comparison
        if 'Scenario' in comparison_2050.columns:
            st.markdown("#### 2050 Projections", unsafe_allow_html=True)
            
            # Build scenario data list for 2050
            scenarios_2050 = []
            for _, row in comparison_2050.iterrows():
                scenario = row['Scenario']
                pop = row.get('Population (M)', 'N/A')
                gdp = row.get('GDP ($B)', 'N/A')
                
                color = 'amber'
                icon = '📊'
                for key in scenario_colors:
                    if key.lower() in scenario.lower():
                        color = scenario_colors[key]
                        icon = scenario_icons.get(key, '📊')
                        break
                
                pop_str = f"{pop:.1f}M" if isinstance(pop, (int, float)) else str(pop)
                gdp_str = f"${gdp:.0f}B" if isinstance(gdp, (int, float)) else str(gdp)
                scenarios_2050.append((icon, scenario[:25] + "..." if len(scenario) > 25 else scenario, pop_str, gdp_str, color))
            
            # Render with st.columns
            if scenarios_2050:
                cols_2050 = st.columns(len(scenarios_2050))
                for i, (icon, name, pop_str, gdp_str, color) in enumerate(scenarios_2050):
                    with cols_2050[i]:
                        st.markdown(render_stat_module(icon, name, pop_str, f"GDP: {gdp_str}", color), unsafe_allow_html=True)
            
            numeric_cols = [c for c in ['Population (M)', 'GDP ($B)', 'Oil Share (%)', 'Urban (%)', 'Renewable GW'] if c in comparison_2050.columns]
            
            if numeric_cols:
                fig2 = go.Figure()
                for i, (_, row) in enumerate(comparison_2050.iterrows()):
                    scenario = row['Scenario'][:20] + "..." if len(row['Scenario']) > 20 else row['Scenario']
                    fig2.add_trace(go.Bar(
                        name=scenario,
                        x=numeric_cols[:4],
                        y=[row[c] for c in numeric_cols[:4]],
                        marker_color=colors_list[i % len(colors_list)]
                    ))
                
                layout2 = get_chart_layout("Key Metrics Comparison - 2050", height=320)
                layout2['legend'] = dict(orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5, bgcolor='rgba(0,0,0,0)', font=dict(size=10))
                layout2['barmode'] = 'group'
                fig2.update_layout(**layout2)
                st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        risks = ws5['risks']
        if not risks.empty:
            numeric_cols = risks.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols and 'Region' in risks.columns:
                fig = px.imshow(
                    risks[numeric_cols].values,
                    x=numeric_cols,
                    y=risks['Region'].values,
                    color_continuous_scale=['#22c55e', '#f59e0b', '#ef4444'],
                    aspect='auto'
                )
                fig.update_layout(**get_chart_layout("Risk Levels by Region", height=450))
                st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("📋 View Risk Data"):
                st.dataframe(risks, use_container_width=True, hide_index=True, height=300)
    
    with tab3:
        opportunities = ws5['opportunities']
        if not opportunities.empty:
            numeric_cols = opportunities.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols and 'Region' in opportunities.columns:
                fig = px.imshow(
                    opportunities[numeric_cols].values,
                    x=numeric_cols,
                    y=opportunities['Region'].values,
                    color_continuous_scale=['#f8fafc', '#74c476', '#006C35'],
                    aspect='auto'
                )
                fig.update_layout(**get_chart_layout("Opportunity Levels by Region", height=450))
                st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("📋 View Opportunity Data"):
                st.dataframe(opportunities, use_container_width=True, hide_index=True, height=300)


def render_ws6_nss_draft():
    """Render WS6 NSS draft with improved visualizations."""
    st.markdown(render_section_header("📋", "National Spatial Strategy Draft", "Complete NSS with spatial structure and regional objectives"), unsafe_allow_html=True)
    
    ws6 = load_ws6_data()
    if not ws6:
        st.warning("WS6 data not available. Run: `python src/analysis/ws6_nss_draft.py`")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏙️ Strategic Nodes", "🛤️ Corridors", "🎯 Regional Objectives", "💰 Investments"])
    
    with tab1:
        nodes = ws6['nodes']
        
        # Compact tier metrics in modules
        tier1 = nodes[nodes['Tier'] == 1] if 'Tier' in nodes.columns else pd.DataFrame()
        tier2 = nodes[nodes['Tier'] == 2] if 'Tier' in nodes.columns else pd.DataFrame()
        tier3 = nodes[nodes['Tier'] == 3] if 'Tier' in nodes.columns else pd.DataFrame()
        
        # Tier stats with st.columns
        if 'Pop_2050_M' in nodes.columns:
            total_pop = nodes['Pop_2050_M'].sum()
            cols = st.columns(4)
            with cols[0]:
                st.markdown(render_stat_module("🏛️", "Tier 1 - National", str(len(tier1)), "Capital & Major Hubs", "green"), unsafe_allow_html=True)
            with cols[1]:
                st.markdown(render_stat_module("🏢", "Tier 2 - Regional", str(len(tier2)), "Regional Centers", "blue"), unsafe_allow_html=True)
            with cols[2]:
                st.markdown(render_stat_module("🏘️", "Tier 3 - Sub-regional", str(len(tier3)), "Growth Centers", "amber"), unsafe_allow_html=True)
            with cols[3]:
                st.markdown(render_stat_module("👥", "Target Population", f"{total_pop:.1f}M", "By 2050", "purple"), unsafe_allow_html=True)
        else:
            cols = st.columns(3)
            with cols[0]:
                st.markdown(render_stat_module("🏛️", "Tier 1 - National", str(len(tier1)), "Capital & Major Hubs", "green"), unsafe_allow_html=True)
            with cols[1]:
                st.markdown(render_stat_module("🏢", "Tier 2 - Regional", str(len(tier2)), "Regional Centers", "blue"), unsafe_allow_html=True)
            with cols[2]:
                st.markdown(render_stat_module("🏘️", "Tier 3 - Sub-regional", str(len(tier3)), "Growth Centers", "amber"), unsafe_allow_html=True)
        
        # Map and node details side by side
        col_map, col_detail = st.columns([3, 2])
        
        with col_map:
            if 'Lat' in nodes.columns and 'Lon' in nodes.columns:
                # Filter out nodes with default coordinates
                valid_nodes = nodes[(nodes['Lat'] != 24.5) | (nodes['Lon'] != 45.0)].copy()
                if len(valid_nodes) < len(nodes):
                    # Add back nodes with valid coords
                    valid_nodes = nodes[
                        ((nodes['Lat'] != 24.5) | (nodes['Lon'] != 45.0)) |
                        (nodes['Name'].isin(['Riyadh', 'Jeddah', 'Makkah', 'Madinah', 'NEOM']))
                    ].copy()
                
                fig_map = px.scatter_geo(
                    valid_nodes,
                    lat='Lat',
                    lon='Lon',
                    size='Pop_2050_M' if 'Pop_2050_M' in valid_nodes.columns else None,
                    color='Tier',
                    hover_name='Name' if 'Name' in valid_nodes.columns else None,
                    hover_data={
                        'Pop_2050_M': ':.1f',
                        'Tier': True,
                        'Region': True if 'Region' in valid_nodes.columns else False,
                        'Lat': False,
                        'Lon': False
                    } if 'Pop_2050_M' in valid_nodes.columns else None,
                    color_discrete_map={1: '#006C35', 2: '#3b82f6', 3: '#f59e0b'},
                    size_max=25
                )
                fig_map.update_geos(
                    center=dict(lat=24.0, lon=45.0),
                    projection_scale=5,
                    showland=True,
                    landcolor='#f8f9fa',
                    countrycolor='#e5e7eb',
                    showocean=True,
                    oceancolor='#ffffff',
                    showcoastlines=True,
                    coastlinecolor='#d1d5db',
                    framecolor='#e5e7eb'
                )
                fig_map.update_layout(
                    height=380,
                    margin=dict(l=0, r=0, t=30, b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    geo=dict(bgcolor='rgba(0,0,0,0)'),
                    legend=dict(orientation='h', yanchor='bottom', y=-0.1, xanchor='center', x=0.5, font=dict(size=10)),
                    title=dict(text="Strategic Nodes Network", font=dict(size=13, color='#1a1a1a'), x=0)
                )
                st.plotly_chart(fig_map, use_container_width=True)
        
        with col_detail:
            # Node cards for Tier 1
            st.markdown("##### Tier 1 Nodes", unsafe_allow_html=True)
            st.markdown('<div class="module-grid" style="grid-template-columns: 1fr;">', unsafe_allow_html=True)
            for _, node in tier1.iterrows():
                pop_2024 = node.get('Pop_2024_M', 0)
                pop_2050 = node.get('Pop_2050_M', 0)
                growth = ((pop_2050 - pop_2024) / pop_2024 * 100) if pop_2024 > 0 else 0
                st.markdown(render_module_card(
                    "🏛️",
                    node.get('Name', 'Unknown'),
                    node.get('Functions', '')[:80] + "..." if len(str(node.get('Functions', ''))) > 80 else node.get('Functions', ''),
                    badge=node.get('Priority', '').upper() if node.get('Priority') else '',
                    badge_color="green" if node.get('Priority') == 'critical' else "amber",
                    stats=[
                        {"value": f"{pop_2024:.1f}M", "label": "Pop 2024"},
                        {"value": f"{pop_2050:.1f}M", "label": "Pop 2050"},
                        {"value": f"+{growth:.0f}%", "label": "Growth"}
                    ]
                ), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Population comparison bar chart
        if 'Pop_2050_M' in nodes.columns and 'Name' in nodes.columns:
            nodes_sorted = nodes.sort_values('Pop_2050_M', ascending=True).tail(12)
            fig = px.bar(
                nodes_sorted,
                x='Pop_2050_M',
                y='Name',
                color='Tier',
                orientation='h',
                color_discrete_map={1: '#006C35', 2: '#3b82f6', 3: '#f59e0b'}
            )
            fig.update_layout(**get_chart_layout("Population Targets 2050 - Top 12 Nodes (Millions)", height=380))
            st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 View All Strategic Nodes"):
            display_cols = ['Name', 'Region', 'Tier', 'Type', 'Pop_2024_M', 'Pop_2050_M', 'Priority']
            display_cols = [c for c in display_cols if c in nodes.columns]
            st.dataframe(nodes[display_cols], use_container_width=True, hide_index=True, height=300)
    
    with tab2:
        corridors = ws6['corridors']
        
        # Summary stats
        if 'Investment_SAR_B' in corridors.columns:
            total_investment = corridors['Investment_SAR_B'].sum()
            critical = len(corridors[corridors['Priority'] == 'critical']) if 'Priority' in corridors.columns else 0
            high = len(corridors[corridors['Priority'] == 'high']) if 'Priority' in corridors.columns else 0
            total_km = corridors['Length_km'].sum() if 'Length_km' in corridors.columns else 0
            
            cols = st.columns(4)
            with cols[0]:
                st.markdown(render_stat_module("🛤️", "Total Corridors", str(len(corridors)), f"{total_km:,.0f} km", "green"), unsafe_allow_html=True)
            with cols[1]:
                st.markdown(render_stat_module("💰", "Investment", f"SAR {total_investment:.0f}B", "Total planned", "blue"), unsafe_allow_html=True)
            with cols[2]:
                st.markdown(render_stat_module("🔴", "Critical Priority", str(critical), "Urgent corridors", "red"), unsafe_allow_html=True)
            with cols[3]:
                st.markdown(render_stat_module("🟡", "High Priority", str(high), "Important corridors", "amber"), unsafe_allow_html=True)
        
        # Full Corridor Map with ALL corridors
        if all(c in corridors.columns for c in ['Start_Lat', 'Start_Lon', 'End_Lat', 'End_Lon']):
            fig_corr = go.Figure()
            
            priority_colors = {'critical': '#ef4444', 'high': '#f59e0b', 'medium': '#22c55e'}
            priority_widths = {'critical': 4, 'high': 3, 'medium': 2}
            
            for _, row in corridors.iterrows():
                priority = row.get('Priority', 'medium')
                color = priority_colors.get(priority, '#22c55e')
                width = priority_widths.get(priority, 2)
                
                fig_corr.add_trace(go.Scattergeo(
                    lon=[row['Start_Lon'], row['End_Lon']],
                    lat=[row['Start_Lat'], row['End_Lat']],
                    mode='lines+markers',
                    line=dict(width=width, color=color),
                    marker=dict(size=8, color=color, symbol='circle'),
                    name=row['Name'],
                    hovertemplate=f"<b>{row['Name']}</b><br>" +
                                  f"Type: {row.get('Type', 'N/A')}<br>" +
                                  f"Length: {row.get('Length_km', 'N/A')} km<br>" +
                                  f"Investment: SAR {row.get('Investment_SAR_B', 'N/A')}B<br>" +
                                  f"Priority: {priority.upper()}<extra></extra>"
                ))
            
            fig_corr.update_geos(
                center=dict(lat=24.0, lon=44.0),
                projection_scale=4.5,
                showland=True,
                landcolor='#f8f9fa',
                countrycolor='#e5e7eb',
                showocean=True,
                oceancolor='#ffffff',
                framecolor='#e5e7eb',
                showcoastlines=True,
                coastlinecolor='#d1d5db'
            )
            fig_corr.update_layout(
                height=450,
                margin=dict(l=0, r=0, t=40, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                geo=dict(bgcolor='rgba(0,0,0,0)'),
                showlegend=True,
                legend=dict(
                    orientation='v',
                    yanchor='top',
                    y=0.98,
                    xanchor='left',
                    x=0.01,
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='#e5e7eb',
                    borderwidth=1,
                    font=dict(size=9)
                ),
                title=dict(text=f"Development Corridors Network ({len(corridors)} Corridors)", font=dict(size=13, color='#1a1a1a'), x=0)
            )
            st.plotly_chart(fig_corr, use_container_width=True)
        
        # Corridor details in module cards
        st.markdown('<div class="module-grid">', unsafe_allow_html=True)
        for _, corr in corridors.iterrows():
            priority = corr.get('Priority', 'medium')
            badge_color = "red" if priority == 'critical' else "amber" if priority == 'high' else "green"
            
            st.markdown(render_module_card(
                "🛤️",
                corr.get('Name', 'Unknown'),
                f"{corr.get('Origin', '')} → {corr.get('Destination', '')}",
                badge=priority.upper() if priority else '',
                badge_color=badge_color,
                stats=[
                    {"value": f"{corr.get('Length_km', 0):,.0f}", "label": "KM"},
                    {"value": f"{corr.get('Investment_SAR_B', 0):.0f}B", "label": "SAR"},
                    {"value": corr.get('Timeline', 'N/A')[:9], "label": "Timeline"}
                ]
            ), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Investment comparison
        if 'Name' in corridors.columns and 'Investment_SAR_B' in corridors.columns:
            fig = px.bar(
                corridors.sort_values('Investment_SAR_B', ascending=True),
                x='Investment_SAR_B',
                y='Name',
                color='Priority' if 'Priority' in corridors.columns else None,
                orientation='h',
                color_discrete_map={'critical': '#ef4444', 'high': '#f59e0b', 'medium': '#22c55e'}
            )
            fig.update_layout(**get_chart_layout("Corridor Investments (SAR Billions)", height=280))
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        objectives = ws6['objectives']
        
        if 'Region' in objectives.columns and 'GDP_Share_2050' in objectives.columns:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Treemap for GDP distribution
                fig = px.treemap(
                    objectives,
                    path=['Region'],
                    values='GDP_Share_2050',
                    color='GDP_Share_2050',
                    color_continuous_scale=['#f8f9fa', '#74c476', '#006C35']
                )
                fig.update_layout(
                    height=350,
                    margin=dict(l=10, r=10, t=30, b=10),
                    paper_bgcolor='rgba(0,0,0,0)',
                    title=dict(text="Target GDP Share by Region (2050)", font=dict(size=13, color='#1a1a1a'), x=0)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Top regions
                top_regions = objectives.nlargest(5, 'GDP_Share_2050')
                st.markdown("##### Top 5 Regions by GDP", unsafe_allow_html=True)
                for _, reg in top_regions.iterrows():
                    st.markdown(render_progress_bar(
                        reg['Region'], 
                        int(reg['GDP_Share_2050']), 
                        100
                    ), unsafe_allow_html=True)
        
        with st.expander("📋 View All Regional Objectives"):
            st.dataframe(objectives, use_container_width=True, hide_index=True, height=300)
    
    with tab4:
        investments = ws6['investments']
        
        if 'Cost_SAR_B' in investments.columns:
            total = investments['Cost_SAR_B'].sum()
            
            st.markdown('<div class="stat-grid">', unsafe_allow_html=True)
            st.markdown(render_stat_module("💰", "Total Investment", f"SAR {total:.0f}B", f"{len(investments)} priority items", "green"), unsafe_allow_html=True)
            
            if 'Category' in investments.columns:
                top_cat = investments.groupby('Category')['Cost_SAR_B'].sum().idxmax()
                top_cat_val = investments.groupby('Category')['Cost_SAR_B'].sum().max()
                st.markdown(render_stat_module("📊", "Top Category", top_cat, f"SAR {top_cat_val:.0f}B", "blue"), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if 'Category' in investments.columns and 'Cost_SAR_B' in investments.columns:
            by_cat = investments.groupby('Category')['Cost_SAR_B'].sum().reset_index()
            by_cat = by_cat.sort_values('Cost_SAR_B', ascending=True)
            
            fig = px.bar(
                by_cat,
                x='Cost_SAR_B',
                y='Category',
                orientation='h',
                color='Cost_SAR_B',
                color_continuous_scale=['#74c476', '#006C35']
            )
            fig.update_layout(**get_chart_layout("Investment by Category (SAR Billions)", height=300))
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 View All Investment Priorities"):
            st.dataframe(investments, use_container_width=True, hide_index=True, height=300)


def render_ws7_governance():
    """Render WS7 governance framework with improved layout."""
    st.markdown(render_section_header("🏛️", "Governance & Implementation", "Framework for strategy execution and monitoring"), unsafe_allow_html=True)
    
    ws7 = load_ws7_data()
    if not ws7:
        st.warning("WS7 data not available. Run: `python src/analysis/ws7_governance.py`")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Governance Bodies", "📊 RACI Matrix", "📈 KPI Framework", "🔍 Monitoring"])
    
    with tab1:
        bodies = ws7['bodies']
        
        if 'Level' in bodies.columns:
            national = bodies[bodies['Level'] == 'national']
            regional = bodies[bodies['Level'] == 'regional']
            local = bodies[bodies['Level'] == 'local']
            
            # Compact stats
            st.markdown('<div class="stat-grid">', unsafe_allow_html=True)
            st.markdown(render_stat_module("🏛️", "National Level", str(len(national)), "Central coordination", "green"), unsafe_allow_html=True)
            st.markdown(render_stat_module("🏢", "Regional Level", str(len(regional)), "Regional execution", "blue"), unsafe_allow_html=True)
            st.markdown(render_stat_module("🏘️", "Local Level", str(len(local)), "Local implementation", "amber"), unsafe_allow_html=True)
            st.markdown(render_stat_module("📋", "Total Bodies", str(len(bodies)), "Complete framework", "purple"), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Governance bodies as module cards
            st.markdown("##### Governance Structure", unsafe_allow_html=True)
            
            # National bodies
            if len(national) > 0:
                st.markdown("###### 🏛️ National Level", unsafe_allow_html=True)
                st.markdown('<div class="module-grid">', unsafe_allow_html=True)
                for _, body in national.iterrows():
                    mandate = str(body.get('Mandate', ''))[:120]
                    if len(str(body.get('Mandate', ''))) > 120:
                        mandate += "..."
                    
                    st.markdown(render_module_card(
                        "🏛️",
                        str(body.get('Name', 'Unknown'))[:40],
                        mandate,
                        badge=body.get('Type', '').upper() if body.get('Type') else '',
                        badge_color="green",
                        stats=[
                            {"value": body.get('Meeting_Frequency', 'N/A'), "label": "Meetings"}
                        ]
                    ), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Regional bodies
            if len(regional) > 0:
                st.markdown("###### 🏢 Regional Level", unsafe_allow_html=True)
                st.markdown('<div class="module-grid">', unsafe_allow_html=True)
                for _, body in regional.iterrows():
                    mandate = str(body.get('Mandate', ''))[:120]
                    if len(str(body.get('Mandate', ''))) > 120:
                        mandate += "..."
                    
                    st.markdown(render_module_card(
                        "🏢",
                        str(body.get('Name', 'Unknown'))[:40],
                        mandate,
                        badge=body.get('Type', '').upper() if body.get('Type') else '',
                        badge_color="blue",
                        stats=[
                            {"value": body.get('Meeting_Frequency', 'N/A'), "label": "Meetings"}
                        ]
                    ), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Local bodies
            if len(local) > 0:
                st.markdown("###### 🏘️ Local Level", unsafe_allow_html=True)
                st.markdown('<div class="module-grid">', unsafe_allow_html=True)
                for _, body in local.iterrows():
                    mandate = str(body.get('Mandate', ''))[:120]
                    if len(str(body.get('Mandate', ''))) > 120:
                        mandate += "..."
                    
                    st.markdown(render_module_card(
                        "🏘️",
                        str(body.get('Name', 'Unknown'))[:40],
                        mandate,
                        badge=body.get('Type', '').upper() if body.get('Type') else '',
                        badge_color="amber",
                        stats=[
                            {"value": body.get('Meeting_Frequency', 'N/A'), "label": "Meetings"}
                        ]
                    ), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Structure visualization
            if 'Type' in bodies.columns:
                fig = px.sunburst(
                    bodies,
                    path=['Level', 'Type'],
                    color='Level',
                    color_discrete_map={'national': '#006C35', 'regional': '#3b82f6', 'local': '#f59e0b'}
                )
                fig.update_layout(
                    height=320,
                    margin=dict(l=10, r=10, t=30, b=10),
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        raci = ws7['raci']
        
        st.markdown(render_info_box("RACI LEGEND", "R = Responsible | A = Accountable | C = Consulted | I = Informed"), unsafe_allow_html=True)
        
        def color_raci(val):
            colors = {
                'R': 'background-color: #22c55e; color: white; font-weight: 600; text-align: center;',
                'A': 'background-color: #3b82f6; color: white; font-weight: 600; text-align: center;',
                'C': 'background-color: #f59e0b; color: black; font-weight: 600; text-align: center;',
                'I': 'background-color: #6b7280; color: white; font-weight: 600; text-align: center;',
                '-': 'background-color: #f3f4f6; color: #9ca3af; text-align: center;'
            }
            return colors.get(val, '')
        
        raci_cols = [col for col in raci.columns if col not in ['Activity', 'Category']]
        styled_raci = raci.style.applymap(color_raci, subset=raci_cols)
        st.dataframe(styled_raci, use_container_width=True, height=400)
    
    with tab3:
        kpis = ws7['kpis']
        
        if 'Category' in kpis.columns:
            # KPI summary by category
            by_cat = kpis.groupby('Category').size().reset_index(name='Count')
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.bar(
                    by_cat.sort_values('Count', ascending=True),
                    y='Category',
                    x='Count',
                    orientation='h',
                    color='Count',
                    color_continuous_scale=['#74c476', '#006C35']
                )
                fig.update_layout(**get_chart_layout("KPIs by Category", height=280))
                fig.update_coloraxes(showscale=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown(f"""
                <div class="data-card">
                    <div class="data-card-header" style="border-bottom: none;">
                        <h3 class="data-card-title">KPI Summary</h3>
                    </div>
                    <div style="font-size: 2rem; font-weight: 700; color: var(--ksa-green); margin: 0.5rem 0;">{len(kpis)}</div>
                    <div style="font-size: 0.8rem; color: var(--text-secondary);">Total KPIs</div>
                    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid var(--border-light);">
                        <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;">Categories</div>
                        <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">{len(by_cat)}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Target tracking
        if 'Target_2030' in kpis.columns and 'Baseline_2024' in kpis.columns:
            kpis_copy = kpis.copy()
            kpis_copy['Improvement_Needed'] = kpis_copy['Target_2030'] - kpis_copy['Baseline_2024']
            
            name_col = 'Name' if 'Name' in kpis_copy.columns else 'KPI_ID'
            top_kpis = kpis_copy.nlargest(8, 'Improvement_Needed')
            
            fig = px.bar(
                top_kpis.sort_values('Improvement_Needed', ascending=True),
                y=name_col,
                x='Improvement_Needed',
                orientation='h',
                color='Improvement_Needed',
                color_continuous_scale=['#f59e0b', '#22c55e', '#006C35']
            )
            fig.update_layout(**get_chart_layout("Top 8 KPIs - Improvement Needed by 2030", height=300))
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 View All KPIs"):
            display_cols = ['KPI_ID', 'Name', 'Category', 'Baseline_2024', 'Target_2030', 'Unit']
            display_cols = [c for c in display_cols if c in kpis.columns]
            st.dataframe(kpis[display_cols] if display_cols else kpis, use_container_width=True, hide_index=True, height=300)
    
    with tab4:
        mechanisms = ws7['mechanisms']
        processes = ws7['processes']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Monitoring Mechanisms", unsafe_allow_html=True)
            st.markdown(render_info_box("OVERVIEW", "Systems and processes for tracking implementation progress"), unsafe_allow_html=True)
            st.dataframe(mechanisms, use_container_width=True, hide_index=True, height=280)
        
        with col2:
            st.markdown("##### Decision Processes", unsafe_allow_html=True)
            st.markdown(render_info_box("OVERVIEW", "Workflow for strategic decisions"), unsafe_allow_html=True)
            st.dataframe(processes, use_container_width=True, hide_index=True, height=280)


def render_deliverables():
    """Render deliverables summary."""
    st.markdown(render_section_header("📦", "Deliverables Summary", "Complete list of tender outputs"), unsafe_allow_html=True)
    
    deliverables = [
        {"WS": "WS1", "Name": "Data Collection", "Files": 17, "Status": "✅ Complete"},
        {"WS": "WS2", "Name": "NSS Review", "Files": 6, "Status": "✅ Complete"},
        {"WS": "WS3", "Name": "Benchmarking", "Files": 4, "Status": "✅ Complete"},
        {"WS": "WS4", "Name": "Sectoral Analysis", "Files": 6, "Status": "✅ Complete"},
        {"WS": "WS5", "Name": "Scenarios", "Files": 8, "Status": "✅ Complete"},
        {"WS": "WS6", "Name": "NSS Draft", "Files": 7, "Status": "✅ Complete"},
        {"WS": "WS7", "Name": "Governance", "Files": 7, "Status": "✅ Complete"},
    ]
    
    df = pd.DataFrame(deliverables)
    total_files = df['Files'].sum()
    
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    st.markdown(render_kpi_card("📁", "Total Files", str(total_files), "All Deliverables", "positive"), unsafe_allow_html=True)
    st.markdown(render_kpi_card("✅", "Workstreams", "7/7", "100% Complete", "positive"), unsafe_allow_html=True)
    st.markdown(render_kpi_card("📋", "Tender Compliance", "100%", "All Requirements Met", "positive"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Progress bars
    st.markdown("""
    <div class="data-card">
        <div class="data-card-header">
            <h3 class="data-card-title">Workstream Completion</h3>
        </div>
    """, unsafe_allow_html=True)
    
    for item in deliverables:
        st.markdown(render_progress_bar(f"{item['WS']}: {item['Name']}", 100), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # File structure
    with st.expander("📁 Generated File Structure"):
        st.code("""
02_analytics/
├── ws2_outputs/
│   ├── WS2_RETROSPECTIVE_REPORT.json
│   ├── WS2_RETROSPECTIVE_REPORT.md
│   ├── continuity_change_matrix.csv
│   └── timeseries_*.csv
├── ws3_outputs/
│   ├── WS3_BENCHMARKING_REPORT.json
│   ├── WS3_BENCHMARKING_REPORT.md
│   ├── methodology_comparison_matrix.csv
│   └── country_x_fit_design_principles.csv
├── ws4_outputs/
│   ├── WS4_SECTORAL_REGIONAL_REPORT.json
│   ├── WS4_SECTORAL_REGIONAL_REPORT.md
│   ├── regional_diagnostics_summary.csv
│   ├── land_use_conflict_matrix.csv
│   └── corrective_measures_playbook.csv
├── ws5_outputs/
│   ├── WS5_SCENARIO_REPORT.json
│   ├── WS5_SCENARIO_REPORT.md
│   ├── scenario_comparison_*.csv
│   ├── risk_heatmap_by_region.csv
│   └── opportunity_heatmap_by_region.csv
├── ws6_outputs/
│   ├── WS6_NSS_DRAFT_REPORT.json
│   ├── WS6_NSS_DRAFT_REPORT.md
│   ├── strategic_nodes.csv
│   ├── development_corridors.csv
│   ├── functional_zones.csv
│   ├── regional_objectives.csv
│   └── investment_priorities.csv
└── ws7_outputs/
    ├── WS7_GOVERNANCE_REPORT.json
    ├── WS7_GOVERNANCE_REPORT.md
    ├── governance_bodies.csv
    ├── decision_processes.csv
    ├── raci_matrix.csv
    ├── kpi_framework.csv
    └── monitoring_mechanisms.csv
        """, language="")


def main():
    """Main application."""
    render_header()
    render_sidebar()
    
    # Main tabs with improved styling
    tabs = st.tabs([
        "🏠 Overview",
        "📜 WS2: Review",
        "🌍 WS3: Benchmarking",
        "🏭 WS4: Sectoral",
        "🔮 WS5: Scenarios",
        "📋 WS6: NSS Draft",
        "🏛️ WS7: Governance",
        "📦 Deliverables"
    ])
    
    with tabs[0]:
        render_overview()
    
    with tabs[1]:
        render_ws2_retrospective()
    
    with tabs[2]:
        render_ws3_benchmarking()
    
    with tabs[3]:
        render_ws4_sectoral()
    
    with tabs[4]:
        render_ws5_scenarios()
    
    with tabs[5]:
        render_ws6_nss_draft()
    
    with tabs[6]:
        render_ws7_governance()
    
    with tabs[7]:
        render_deliverables()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p class="footer-brand">NSS X - National Spatial Strategy</p>
        <p class="footer-text">Kingdom of Saudi Arabia • Vision 2030 Aligned • All Workstreams Complete</p>
        <p class="footer-text">© 2025-2026 Confidential</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
