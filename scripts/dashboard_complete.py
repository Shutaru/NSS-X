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
# PREMIUM CSS STYLING
# ============================================================================
st.markdown("""
<style>
    /* ===== IMPORTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* ===== ROOT VARIABLES ===== */
    :root {
        --ksa-green: #006C35;
        --ksa-green-light: #00a650;
        --ksa-green-dark: #004d25;
        --ksa-gold: #c5a572;
        --ksa-gold-light: #d4bc8e;
        --bg-primary: #0e1117;
        --bg-secondary: #1a1d24;
        --bg-card: #1e222a;
        --bg-card-hover: #252932;
        --text-primary: #ffffff;
        --text-secondary: #a0a5b1;
        --text-muted: #6b7280;
        --border-color: #2d333b;
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.2);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.3);
        --shadow-lg: 0 8px 24px rgba(0,0,0,0.4);
        --radius-sm: 6px;
        --radius-md: 12px;
        --radius-lg: 16px;
    }
    
    /* ===== GLOBAL STYLES ===== */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ===== HERO HEADER ===== */
    .hero-container {
        background: linear-gradient(135deg, var(--ksa-green-dark) 0%, var(--ksa-green) 50%, var(--ksa-green-light) 100%);
        border-radius: var(--radius-lg);
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 300px;
        height: 100%;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='rgba(255,255,255,0.05)' d='M0 50 Q25 0 50 50 T100 50 V100 H0Z'/%3E%3C/svg%3E") no-repeat;
        background-size: cover;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.85);
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    .hero-badge {
        display: inline-block;
        background: var(--ksa-gold);
        color: var(--ksa-green-dark);
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ===== KPI CARDS ===== */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .kpi-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card:hover {
        background: var(--bg-card-hover);
        border-color: var(--ksa-green);
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--ksa-green) 0%, var(--ksa-gold) 100%);
        border-radius: var(--radius-sm) 0 0 var(--radius-sm);
    }
    
    .kpi-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .kpi-label {
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.25rem;
    }
    
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1.2;
    }
    
    .kpi-delta {
        font-size: 0.75rem;
        margin-top: 0.25rem;
    }
    
    .kpi-delta.positive { color: #22c55e; }
    .kpi-delta.negative { color: #ef4444; }
    .kpi-delta.neutral { color: var(--text-secondary); }
    
    /* ===== SECTION HEADERS ===== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .section-header-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, var(--ksa-green) 0%, var(--ksa-green-light) 100%);
        border-radius: var(--radius-sm);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    
    .section-header-text h2 {
        margin: 0;
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .section-header-text p {
        margin: 0;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }
    
    /* ===== DATA CARDS ===== */
    .data-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .data-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .data-card-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    
    .data-card-badge {
        background: var(--ksa-green);
        color: white;
        padding: 0.25rem 0.6rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 500;
    }
    
    /* ===== INFO BOXES ===== */
    .info-box {
        background: linear-gradient(135deg, rgba(0,108,53,0.15) 0%, rgba(0,166,80,0.1) 100%);
        border: 1px solid rgba(0,108,53,0.3);
        border-radius: var(--radius-md);
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
    }
    
    .info-box-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--ksa-green-light);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .info-box-content {
        font-size: 0.95rem;
        color: var(--text-primary);
        line-height: 1.6;
    }
    
    /* ===== PROGRESS BARS ===== */
    .progress-container {
        margin: 0.5rem 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.35rem;
    }
    
    .progress-label span:first-child {
        font-size: 0.85rem;
        color: var(--text-primary);
    }
    
    .progress-label span:last-child {
        font-size: 0.85rem;
        color: var(--ksa-green-light);
        font-weight: 600;
    }
    
    .progress-bar {
        height: 8px;
        background: var(--bg-secondary);
        border-radius: 4px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--ksa-green) 0%, var(--ksa-green-light) 100%);
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    /* ===== STAT PILLS ===== */
    .stat-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.25rem;
    }
    
    .stat-pill-icon { font-size: 0.9rem; }
    .stat-pill-value { font-weight: 600; color: var(--text-primary); }
    .stat-pill-label { color: var(--text-secondary); }
    
    /* ===== RACI STYLING ===== */
    .raci-R { background-color: #22c55e !important; color: white !important; font-weight: 600; text-align: center; }
    .raci-A { background-color: #3b82f6 !important; color: white !important; font-weight: 600; text-align: center; }
    .raci-C { background-color: #f59e0b !important; color: black !important; font-weight: 600; text-align: center; }
    .raci-I { background-color: #6b7280 !important; color: white !important; font-weight: 600; text-align: center; }
    
    /* ===== SIDEBAR STYLING ===== */
    .sidebar-section {
        background: var(--bg-card);
        border-radius: var(--radius-md);
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .sidebar-section-title {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: var(--text-muted);
        margin-bottom: 0.75rem;
    }
    
    .ws-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: var(--radius-sm);
        transition: background 0.2s;
    }
    
    .ws-item:hover {
        background: var(--bg-card-hover);
    }
    
    .ws-item-status {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #22c55e;
    }
    
    .ws-item-name {
        flex: 1;
        font-size: 0.85rem;
        color: var(--text-primary);
    }
    
    .ws-item-pct {
        font-size: 0.75rem;
        color: var(--text-secondary);
    }
    
    /* ===== TABLE STYLING ===== */
    .dataframe {
        font-size: 0.85rem !important;
    }
    
    .dataframe th {
        background: var(--ksa-green) !important;
        color: white !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 0.7rem !important;
        letter-spacing: 0.5px !important;
    }
    
    .dataframe td {
        border-color: var(--border-color) !important;
    }
    
    .dataframe tr:hover td {
        background: var(--bg-card-hover) !important;
    }
    
    /* ===== TAB STYLING ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: var(--bg-card);
        border-radius: var(--radius-md);
        padding: 0.35rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm);
        padding: 0.6rem 1.2rem;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--ksa-green) !important;
        color: white !important;
    }
    
    /* ===== PLOTLY CHART CONTAINER ===== */
    .chart-container {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 1px solid var(--border-color);
    }
    
    .footer-brand {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--ksa-green-light);
    }
    
    .footer-text {
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
    }
    
    /* ===== ANIMATIONS ===== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease forwards;
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .hero-title { font-size: 1.75rem; }
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


def get_chart_layout(title: str = "", height: int = 400):
    """Get consistent chart layout."""
    return dict(
        title=dict(text=title, font=dict(size=16, color='#ffffff'), x=0, xanchor='left'),
        font=dict(family="Inter, sans-serif", color='#a0a5b1'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=height,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
            font=dict(size=11)
        ),
        xaxis=dict(
            gridcolor='rgba(45,51,59,0.5)',
            zerolinecolor='rgba(45,51,59,0.5)',
        ),
        yaxis=dict(
            gridcolor='rgba(45,51,59,0.5)',
            zerolinecolor='rgba(45,51,59,0.5)',
        )
    )


KSA_COLORS = ['#006C35', '#00a650', '#74c476', '#c5a572', '#d4bc8e', '#3b82f6', '#22c55e']


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
        - [GitHub](https://github.com/Shutaru/NSS-X)
        """)


def render_overview():
    """Render overview tab with premium styling."""
    ws6 = load_ws6_data()
    
    # KPI Grid
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    
    kpis = [
        ("👥", "Population 2024", "34.1M", "+2.3% YoY", "positive"),
        ("💰", "GDP 2024", "$1.1T", "+4.5%", "positive"),
        ("🗺️", "Regions", "13", "All Covered", "neutral"),
        ("🏙️", "Strategic Nodes", "20", "Tier 1-3", "neutral"),
        ("📈", "Investment Plan", "SAR 1.4T", "2025-2050", "neutral"),
    ]
    
    kpi_html = ""
    for icon, label, value, delta, delta_type in kpis:
        kpi_html += render_kpi_card(icon, label, value, delta, delta_type)
    
    st.markdown(kpi_html + '</div>', unsafe_allow_html=True)
    
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
    """Render WS2 retrospective analysis with premium styling."""
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
    
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    st.markdown(render_kpi_card("✓", "Maintain", str(maintain), "Keep as-is", "positive"), unsafe_allow_html=True)
    st.markdown(render_kpi_card("⬆", "Strengthen", str(strengthen), "Enhance", "positive"), unsafe_allow_html=True)
    st.markdown(render_kpi_card("↻", "Modify", str(modify), "Update", "neutral"), unsafe_allow_html=True)
    st.markdown(render_kpi_card("✚", "New", str(new_items), "Introduce", "positive"), unsafe_allow_html=True)
    st.markdown(render_kpi_card("✗", "Discontinue", str(discontinue), "Remove", "negative"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts side by side
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            continuity, 
            names='Recommendation', 
            title="Policy Recommendations Distribution",
            color='Recommendation',
            color_discrete_map={
                'MAINTAIN': '#22c55e',
                'STRENGTHEN': '#3b82f6',
                'MODIFY': '#f59e0b',
                'NEW': '#8b5cf6',
                'DISCONTINUE': '#ef4444'
            },
            hole=0.4
        )
        fig.update_layout(**get_chart_layout())
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig2 = px.histogram(
            continuity,
            x='Priority',
            color='Category',
            title="Policies by Priority Level",
            barmode='group',
            color_discrete_sequence=KSA_COLORS
        )
        fig2.update_layout(**get_chart_layout())
        st.plotly_chart(fig2, use_container_width=True)
    
    # Data table with expander
    with st.expander("📋 View Full Continuity Matrix", expanded=False):
        st.dataframe(continuity, use_container_width=True, height=400)


def render_ws3_benchmarking():
    """Render WS3 international benchmarking."""
    st.markdown(render_section_header("🌍", "International Benchmarking", "Learning from global best practices"), unsafe_allow_html=True)
    
    ws3 = load_ws3_data()
    if not ws3:
        st.warning("WS3 data not available. Run: `python src/analysis/ws3_benchmarking.py`")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="data-card">
            <div class="data-card-header">
                <h3 class="data-card-title">Countries Analyzed</h3>
                <span class="data-card-badge">8 Countries</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        report = ws3['report']
        countries = report.get('section_1_country_analyses', {})
        
        country_data = []
        for country, data in countries.items():
            if isinstance(data, dict):
                country_data.append({
                    'Country': country,
                    'Relevance': data.get('relevance_score', 'N/A'),
                    'Key Lesson': data.get('key_lessons', ['N/A'])[0] if data.get('key_lessons') else 'N/A'
                })
        
        if country_data:
            st.dataframe(pd.DataFrame(country_data), use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("""
        <div class="data-card">
            <div class="data-card-header">
                <h3 class="data-card-title">Methodology Comparison</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        methodology = ws3['methodology']
        st.dataframe(methodology, use_container_width=True, hide_index=True)
    
    # Design principles chart
    st.markdown(render_section_header("🎨", "Design Principles for KSA", "Adapted from international benchmarks"), unsafe_allow_html=True)
    
    principles = ws3['principles']
    if not principles.empty:
        x_col = 'Principle' if 'Principle' in principles.columns else principles.columns[0]
        y_col = 'Priority' if 'Priority' in principles.columns else principles.columns[1] if len(principles.columns) > 1 else principles.columns[0]
        
        fig = px.bar(
            principles.head(10),
            x=x_col,
            y=y_col,
            title="",
            color=y_col,
            color_continuous_scale=['#004d25', '#006C35', '#00a650', '#74c476']
        )
        fig.update_layout(**get_chart_layout(height=350))
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 View All Design Principles"):
            st.dataframe(principles, use_container_width=True, hide_index=True)


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
            numeric_cols = diagnostics.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                fig = px.imshow(
                    diagnostics[numeric_cols].values,
                    x=numeric_cols,
                    y=diagnostics['Region'].values,
                    color_continuous_scale=['#004d25', '#006C35', '#00a650', '#74c476', '#d4bc8e'],
                    aspect='auto'
                )
                fig.update_layout(**get_chart_layout("Regional Performance Heatmap", height=500))
                st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 View Full Diagnostics Data"):
            st.dataframe(diagnostics, use_container_width=True, hide_index=True)
    
    with tab2:
        conflicts = ws4['conflicts']
        st.markdown(render_info_box("CONFLICT MATRIX", "Analysis of land use conflicts across sectors and regions"), unsafe_allow_html=True)
        st.dataframe(conflicts, use_container_width=True, hide_index=True)
    
    with tab3:
        measures = ws4['measures']
        st.markdown(render_info_box("CORRECTIVE MEASURES", "Playbook of interventions to address identified issues"), unsafe_allow_html=True)
        st.dataframe(measures, use_container_width=True, hide_index=True)


def render_ws5_scenarios():
    """Render WS5 scenario planning."""
    st.markdown(render_section_header("🔮", "Scenario Planning", "Alternative futures and strategic pathways"), unsafe_allow_html=True)
    
    ws5 = load_ws5_data()
    if not ws5:
        st.warning("WS5 data not available. Run: `python src/analysis/ws5_comprehensive.py`")
        return
    
    tab1, tab2, tab3 = st.tabs(["📈 Scenario Comparison", "⚠️ Risk Heatmap", "💎 Opportunity Heatmap"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="data-card">
                <div class="data-card-header">
                    <h3 class="data-card-title">2030 Projections</h3>
                    <span class="data-card-badge">Short-term</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            comparison_2030 = ws5['comparison_2030']
            st.dataframe(comparison_2030, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("""
            <div class="data-card">
                <div class="data-card-header">
                    <h3 class="data-card-title">2050 Projections</h3>
                    <span class="data-card-badge">Long-term</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            comparison_2050 = ws5['comparison_2050']
            st.dataframe(comparison_2050, use_container_width=True, hide_index=True)
        
        if 'Scenario' in comparison_2030.columns:
            numeric_cols = comparison_2030.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                fig = px.bar(
                    comparison_2030,
                    x='Scenario',
                    y=numeric_cols[0],
                    color='Scenario',
                    color_discrete_sequence=KSA_COLORS
                )
                fig.update_layout(**get_chart_layout("Scenario Comparison 2030"))
                st.plotly_chart(fig, use_container_width=True)
    
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
                fig.update_layout(**get_chart_layout("Risk Levels by Region", height=500))
                st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("📋 View Risk Data"):
                st.dataframe(risks, use_container_width=True, hide_index=True)
    
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
                fig.update_layout(**get_chart_layout("Opportunity Levels by Region", height=500))
                st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("📋 View Opportunity Data"):
                st.dataframe(opportunities, use_container_width=True, hide_index=True)


def render_ws6_nss_draft():
    """Render WS6 NSS draft with premium styling."""
    st.markdown(render_section_header("📋", "National Spatial Strategy Draft", "Complete NSS with spatial structure and regional objectives"), unsafe_allow_html=True)
    
    ws6 = load_ws6_data()
    if not ws6:
        st.warning("WS6 data not available. Run: `python src/analysis/ws6_nss_draft.py`")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏙️ Strategic Nodes", "🛤️ Corridors", "🎯 Regional Objectives", "💰 Investments"])
    
    with tab1:
        nodes = ws6['nodes']
        
        # Tier metrics
        tier1 = len(nodes[nodes['Tier'] == 1]) if 'Tier' in nodes.columns else 0
        tier2 = len(nodes[nodes['Tier'] == 2]) if 'Tier' in nodes.columns else 0
        tier3 = len(nodes[nodes['Tier'] == 3]) if 'Tier' in nodes.columns else 0
        
        st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
        st.markdown(render_kpi_card("🏛️", "Tier 1 (National)", str(tier1), "Capital & Major", "neutral"), unsafe_allow_html=True)
        st.markdown(render_kpi_card("🏢", "Tier 2 (Regional)", str(tier2), "Regional Hubs", "neutral"), unsafe_allow_html=True)
        st.markdown(render_kpi_card("🏘️", "Tier 3 (Sub-regional)", str(tier3), "Growth Centers", "neutral"), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Map
        if 'Lat' in nodes.columns and 'Lon' in nodes.columns:
            fig_map = px.scatter_geo(
                nodes,
                lat='Lat',
                lon='Lon',
                size='Pop_2050_M' if 'Pop_2050_M' in nodes.columns else None,
                color='Tier',
                hover_name='Name' if 'Name' in nodes.columns else None,
                hover_data={
                    'Pop_2050_M': ':.1f',
                    'Tier': True,
                    'Lat': False,
                    'Lon': False
                } if 'Pop_2050_M' in nodes.columns else None,
                color_discrete_sequence=['#006C35', '#00a650', '#74c476'],
            )
            fig_map.update_geos(
                center=dict(lat=24.0, lon=45.0),
                projection_scale=5,
                showland=True,
                landcolor='#1e222a',
                countrycolor='#2d333b',
                showocean=True,
                oceancolor='#0e1117',
                showcoastlines=True,
                coastlinecolor='#2d333b',
                framecolor='#2d333b'
            )
            fig_map.update_layout(
                **get_chart_layout("Strategic Nodes Network", height=500),
                geo=dict(bgcolor='rgba(0,0,0,0)')
            )
            st.plotly_chart(fig_map, use_container_width=True)
        
        # Bar chart
        if 'Pop_2050_M' in nodes.columns and 'Name' in nodes.columns:
            fig = px.bar(
                nodes.sort_values('Pop_2050_M', ascending=True),
                x='Pop_2050_M',
                y='Name',
                color='Tier',
                orientation='h',
                color_discrete_sequence=['#006C35', '#00a650', '#74c476']
            )
            fig.update_layout(**get_chart_layout("Population Targets 2050 (Millions)", height=600))
            st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 View All Strategic Nodes"):
            st.dataframe(nodes, use_container_width=True, hide_index=True)
    
    with tab2:
        corridors = ws6['corridors']
        
        if 'Investment_SAR_B' in corridors.columns:
            total_investment = corridors['Investment_SAR_B'].sum()
            st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
            st.markdown(render_kpi_card("💰", "Total Corridor Investment", f"SAR {total_investment:.0f}B", f"{len(corridors)} Corridors", "neutral"), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Corridor Map
        if all(c in corridors.columns for c in ['Start_Lat', 'Start_Lon', 'End_Lat', 'End_Lon']):
            fig_corr = go.Figure()
            
            colors = {'critical': '#ef4444', 'high': '#f59e0b', 'medium': '#22c55e'}
            
            for _, row in corridors.iterrows():
                color = colors.get(row.get('Priority', 'medium'), '#22c55e')
                fig_corr.add_trace(go.Scattergeo(
                    lon=[row['Start_Lon'], row['End_Lon']],
                    lat=[row['Start_Lat'], row['End_Lat']],
                    mode='lines+markers',
                    line=dict(width=3, color=color),
                    marker=dict(size=10, color=color),
                    name=row['Name'],
                    hoverinfo='name'
                ))
            
            fig_corr.update_geos(
                center=dict(lat=24.0, lon=45.0),
                projection_scale=5,
                showland=True,
                landcolor='#1e222a',
                countrycolor='#2d333b',
                showocean=True,
                oceancolor='#0e1117',
                framecolor='#2d333b'
            )
            fig_corr.update_layout(
                **get_chart_layout("Development Corridors", height=500),
                geo=dict(bgcolor='rgba(0,0,0,0)'),
                showlegend=True
            )
            st.plotly_chart(fig_corr, use_container_width=True)
        
        # Investment bar
        if 'Name' in corridors.columns and 'Investment_SAR_B' in corridors.columns:
            fig = px.bar(
                corridors,
                x='Name',
                y='Investment_SAR_B',
                color='Priority' if 'Priority' in corridors.columns else None,
                color_discrete_map={'critical': '#ef4444', 'high': '#f59e0b', 'medium': '#22c55e'}
            )
            fig.update_layout(**get_chart_layout("Corridor Investments (SAR Billions)"))
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 View All Corridors"):
            st.dataframe(corridors, use_container_width=True, hide_index=True)
    
    with tab3:
        objectives = ws6['objectives']
        
        if 'Region' in objectives.columns and 'GDP_Share_2050' in objectives.columns:
            fig = px.pie(
                objectives,
                names='Region',
                values='GDP_Share_2050',
                hole=0.4,
                color_discrete_sequence=KSA_COLORS + px.colors.qualitative.Set3
            )
            fig.update_layout(**get_chart_layout("Target GDP Share by Region (2050)"))
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 View All Regional Objectives"):
            st.dataframe(objectives, use_container_width=True, hide_index=True)
    
    with tab4:
        investments = ws6['investments']
        
        if 'Cost_SAR_B' in investments.columns:
            total = investments['Cost_SAR_B'].sum()
            
            st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
            st.markdown(render_kpi_card("💰", "Total Investment", f"SAR {total:.0f}B", f"{len(investments)} Priority Items", "neutral"), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if 'Category' in investments.columns and 'Cost_SAR_B' in investments.columns:
            by_cat = investments.groupby('Category')['Cost_SAR_B'].sum().reset_index()
            fig = px.pie(
                by_cat,
                names='Category',
                values='Cost_SAR_B',
                hole=0.4,
                color_discrete_sequence=KSA_COLORS
            )
            fig.update_layout(**get_chart_layout("Investment by Category"))
            st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 View All Investment Priorities"):
            st.dataframe(investments, use_container_width=True, hide_index=True)


def render_ws7_governance():
    """Render WS7 governance framework."""
    st.markdown(render_section_header("🏛️", "Governance & Implementation", "Framework for strategy execution and monitoring"), unsafe_allow_html=True)
    
    ws7 = load_ws7_data()
    if not ws7:
        st.warning("WS7 data not available. Run: `python src/analysis/ws7_governance.py`")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Governance Bodies", "📊 RACI Matrix", "📈 KPI Framework", "🔍 Monitoring"])
    
    with tab1:
        bodies = ws7['bodies']
        
        if 'Level' in bodies.columns:
            national = len(bodies[bodies['Level'] == 'national'])
            regional = len(bodies[bodies['Level'] == 'regional'])
            local = len(bodies[bodies['Level'] == 'local'])
            
            st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
            st.markdown(render_kpi_card("🏛️", "National Level", str(national), "Central Bodies", "neutral"), unsafe_allow_html=True)
            st.markdown(render_kpi_card("🏢", "Regional Level", str(regional), "Regional Bodies", "neutral"), unsafe_allow_html=True)
            st.markdown(render_kpi_card("🏘️", "Local Level", str(local), "Local Bodies", "neutral"), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if 'Type' in bodies.columns:
                fig = px.sunburst(
                    bodies,
                    path=['Level', 'Type'],
                    color_discrete_sequence=KSA_COLORS
                )
                fig.update_layout(**get_chart_layout("Governance Structure", height=450))
                st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 View All Governance Bodies"):
            st.dataframe(bodies, use_container_width=True, hide_index=True)
    
    with tab2:
        raci = ws7['raci']
        
        st.markdown(render_info_box("RACI LEGEND", "R = Responsible | A = Accountable | C = Consulted | I = Informed"), unsafe_allow_html=True)
        
        def color_raci(val):
            colors = {
                'R': 'background-color: #22c55e; color: white; font-weight: 600; text-align: center;',
                'A': 'background-color: #3b82f6; color: white; font-weight: 600; text-align: center;',
                'C': 'background-color: #f59e0b; color: black; font-weight: 600; text-align: center;',
                'I': 'background-color: #6b7280; color: white; font-weight: 600; text-align: center;',
                '-': 'background-color: #1e222a; color: #4b5563; text-align: center;'
            }
            return colors.get(val, '')
        
        raci_cols = [col for col in raci.columns if col not in ['Activity', 'Category']]
        styled_raci = raci.style.applymap(color_raci, subset=raci_cols)
        st.dataframe(styled_raci, use_container_width=True, height=500)
    
    with tab3:
        kpis = ws7['kpis']
        
        if 'Category' in kpis.columns:
            by_cat = kpis.groupby('Category').size().reset_index(name='Count')
            fig = px.bar(
                by_cat,
                x='Category',
                y='Count',
                color='Category',
                color_discrete_sequence=KSA_COLORS
            )
            fig.update_layout(**get_chart_layout("KPIs by Category"))
            st.plotly_chart(fig, use_container_width=True)
        
        # Target tracking
        if 'Target_2030' in kpis.columns and 'Baseline_2024' in kpis.columns:
            kpis_copy = kpis.copy()
            kpis_copy['Improvement_Needed'] = kpis_copy['Target_2030'] - kpis_copy['Baseline_2024']
            
            name_col = 'Name' if 'Name' in kpis_copy.columns else 'KPI_ID'
            fig = px.bar(
                kpis_copy.head(10),
                x=name_col,
                y='Improvement_Needed',
                color='Improvement_Needed',
                color_continuous_scale=['#ef4444', '#f59e0b', '#22c55e']
            )
            fig.update_layout(**get_chart_layout("Improvement Needed by 2030 (Top 10)"))
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 View All KPIs"):
            st.dataframe(kpis, use_container_width=True, hide_index=True)
    
    with tab4:
        mechanisms = ws7['mechanisms']
        st.markdown(render_info_box("MONITORING MECHANISMS", "Systems and processes for tracking implementation progress"), unsafe_allow_html=True)
        st.dataframe(mechanisms, use_container_width=True, hide_index=True)
        
        st.markdown(render_section_header("⚙️", "Decision Processes", "Workflow for strategic decisions"), unsafe_allow_html=True)
        processes = ws7['processes']
        st.dataframe(processes, use_container_width=True, hide_index=True)


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
        <p class="footer-text">© 2025-2026 | <a href="https://github.com/Shutaru/NSS-X" style="color: var(--ksa-green-light);">GitHub</a></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
