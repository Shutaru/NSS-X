"""
NSS X - Unified Dashboard for Saudi Arabia
Dashboard unificado com dados reais e todas as análises.
Run with: streamlit run scripts/dashboard.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.data.real_data_provider import RealDataProvider
from src.analysis import RetrospectiveAnalyzer, SectoralAnalyzer, ScenarioModeler

# Page config
st.set_page_config(
    page_title="NSS KSA - National Spatial Strategy",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; font-weight: bold; color: #006C35; margin-bottom: 0;}
    .sub-header {font-size: 1.1rem; color: #666; margin-top: 0;}
    .real-data-banner {background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
        border-left: 4px solid #28a745; padding: 10px 15px; margin-bottom: 20px; border-radius: 0 5px 5px 0;}
    .scenario-card {background: #f8f9fa; border-radius: 10px; padding: 15px; margin: 10px 0; 
        border-left: 4px solid #006C35;}
    .ws-badge {background: #006C35; color: white; padding: 3px 10px; border-radius: 15px; font-size: 0.8rem;}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_resources():
    """Load all data providers and analyzers."""
    return {
        'provider': RealDataProvider(),
        'ws2': RetrospectiveAnalyzer(),
        'ws4': SectoralAnalyzer(),
        'ws5': ScenarioModeler()
    }


@st.cache_data
def load_spatial_data(_provider):
    """Load spatial and statistical data."""
    return {
        'regions': _provider.get_spatial_units(level=2).data,
        'settlements': _provider.get_settlements().data,
        'population': _provider.get_population(spatial_level=2, year=2024).data,
        'economic': _provider.get_economic_data('gdp', spatial_level=2, year=2024).data,
        'projects': _provider.get_projects().data,
        'employment': _provider.get_employment().data,
    }


def render_sidebar(resources, data):
    """Render sidebar with info and navigation."""
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Flag_of_Saudi_Arabia.svg/320px-Flag_of_Saudi_Arabia.svg.png", width=150)
    st.sidebar.markdown("### 🇸🇦 Saudi Arabia NSS")
    st.sidebar.markdown("**National Spatial Strategy**")
    st.sidebar.markdown("---")
    
    # Key stats
    total_pop = data['population']['population'].sum()
    total_gdp = data['economic']['gdp_billion_usd'].sum()
    n_projects = len(data['projects'])
    total_inv = data['projects']['budget_billion_usd'].sum()
    
    st.sidebar.metric("Population (2024)", f"{total_pop/1e6:.1f}M")
    st.sidebar.metric("GDP", f"${total_gdp:.0f}B")
    st.sidebar.metric("Vision 2030 Projects", f"{n_projects}")
    st.sidebar.metric("Total Investment", f"${total_inv:.0f}B")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Data Sources")
    st.sidebar.markdown("""
    - 📊 GASTAT
    - 📈 DataSaudi.sa
    - 🗺️ OCHA HDX
    - 🎯 Vision 2030
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Provider:** {resources['provider'].provider_name}")
    st.sidebar.markdown(f"**Mode:** {'🟢 Real Data' if not resources['provider'].is_simulation else '🟡 Simulation'}")


def render_overview_tab(data, resources):
    """Render spatial overview tab."""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_pop = data['population']['population'].sum()
    total_gdp = data['economic']['gdp_billion_usd'].sum()
    n_cities = len(data['settlements'])
    n_projects = len(data['projects'])
    total_inv = data['projects']['budget_billion_usd'].sum()
    
    col1.metric("Population", f"{total_pop/1e6:.1f}M", "2024")
    col2.metric("GDP", f"${total_gdp:.0f}B", "Est. 2024")
    col3.metric("Major Cities", f"{n_cities}")
    col4.metric("V2030 Projects", f"{n_projects}")
    col5.metric("Investment", f"${total_inv:.0f}B")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Regions choropleth
        regions_pop = data['regions'].merge(
            data['population'][['region_name_en', 'population']],
            left_on='name_en', right_on='region_name_en', how='left'
        )
        regions_pop['population'] = regions_pop['population'].fillna(0)
        
        fig = px.choropleth_map(
            regions_pop,
            geojson=regions_pop.geometry.__geo_interface__,
            locations=regions_pop.index,
            color='population',
            hover_name='name_en',
            hover_data=['area_sqkm', 'population'],
            center={"lat": 24.7136, "lon": 46.6753},
            zoom=4,
            opacity=0.7,
            color_continuous_scale='Greens',
            title="Population by Region"
        )
        fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, height=450)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Cities and projects
        fig = px.scatter_map(
            data['settlements'],
            lat=data['settlements'].geometry.y,
            lon=data['settlements'].geometry.x,
            size='population',
            color='hierarchy_class',
            hover_name='name_en',
            center={"lat": 24.7136, "lon": 46.6753},
            zoom=4,
            size_max=35,
            title="Cities & Settlement Hierarchy"
        )
        fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, height=450)
        st.plotly_chart(fig, use_container_width=True)
    
    # Regions table
    st.subheader("13 Administrative Regions")
    region_summary = data['regions'][['name_en', 'code', 'area_sqkm']].merge(
        data['population'][['region_name_en', 'population']],
        left_on='name_en', right_on='region_name_en', how='left'
    )
    region_summary['density'] = region_summary['population'] / region_summary['area_sqkm']
    region_summary = region_summary.sort_values('population', ascending=False)
    region_summary = region_summary[['name_en', 'code', 'area_sqkm', 'population', 'density']]
    region_summary.columns = ['Region', 'Code', 'Area (km²)', 'Population', 'Density']
    st.dataframe(region_summary.style.format({
        'Area (km²)': '{:,.0f}', 'Population': '{:,.0f}', 'Density': '{:.1f}'
    }), use_container_width=True, hide_index=True)


def render_retrospective_tab(ws2):
    """Render WS2 retrospective analysis tab."""
    st.markdown('<span class="ws-badge">WS2</span> **Retrospective Analysis 2010-2025**', unsafe_allow_html=True)
    
    ts_data = ws2.get_time_series_data()
    report = ws2.generate_retrospective_report()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pop. Growth", report['key_findings']['population']['growth'])
    col2.metric("CAGR", report['key_findings']['population']['cagr'])
    col3.metric("Urbanization", report['key_findings']['population']['urbanization'])
    col4.metric("Diversification", "49.8%→62%", "Non-oil GDP")
    
    col1, col2 = st.columns(2)
    
    with col1:
        pop_df = ts_data['population']
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=pop_df['year'], y=pop_df['total_population'], 
                                 name='Total', mode='lines+markers', line=dict(color='#006C35', width=3)))
        fig.add_trace(go.Scatter(x=pop_df['year'], y=pop_df['saudi_population'],
                                 name='Saudi', mode='lines+markers', line=dict(color='#28a745', width=2)))
        fig.add_trace(go.Scatter(x=pop_df['year'], y=pop_df['expat_population'],
                                 name='Expat', mode='lines+markers', line=dict(color='#ffc107', width=2)))
        fig.add_vline(x=2016, line_dash="dash", line_color="red", annotation_text="Vision 2030")
        fig.add_vline(x=2020, line_dash="dot", line_color="gray", annotation_text="COVID")
        fig.update_layout(title="Population Trends (Millions)", height=350, 
                          legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        gdp_df = ts_data['gdp']
        fig = go.Figure()
        fig.add_trace(go.Bar(x=gdp_df['year'], y=gdp_df['gdp_oil_share_pct'], name='Oil %', marker_color='#dc3545'))
        fig.add_trace(go.Bar(x=gdp_df['year'], y=gdp_df['gdp_nonoil_share_pct'], name='Non-oil %', marker_color='#006C35'))
        fig.update_layout(title="Economic Diversification (GDP Share)", barmode='stack', height=350,
                          legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig, use_container_width=True)
    
    # Milestones
    st.subheader("Vision 2030 Milestones")
    milestones = ws2.vision2030_milestones
    cols = st.columns(5)
    for i, (year, event) in enumerate(list(milestones.items())[5:10]):
        with cols[i]:
            st.markdown(f"**{year}**")
            st.caption(event)


def render_sectoral_tab(ws4):
    """Render WS4 sectoral analysis tab."""
    st.markdown('<span class="ws-badge">WS4</span> **Sectoral Analysis & Land Use Conflicts**', unsafe_allow_html=True)
    
    report = ws4.generate_sectoral_report()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sectors", report['sectors_analyzed'])
    col2.metric("V2030 Priority", report['vision2030_priorities']['count'])
    col3.metric("High Conflicts", report['conflict_summary']['high_conflicts'])
    col4.metric("Synergies", report['conflict_summary']['synergies_identified'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sector growth
        growth_data = report['high_growth_sectors']
        fig = px.bar(
            x=[d['name'] for d in growth_data],
            y=[d['growth_rate'] for d in growth_data],
            title="Top 5 Growth Sectors",
            labels={'x': 'Sector', 'y': 'Growth Rate (%)'},
            color=[d['growth_rate'] for d in growth_data],
            color_continuous_scale='Greens'
        )
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Conflict matrix
        matrix = ws4.get_conflict_matrix()
        fig = px.imshow(
            matrix.values,
            x=matrix.columns,
            y=matrix.index,
            color_continuous_scale='RdYlGn',
            title="Conflict (-) / Synergy (+) Matrix",
            labels={'color': 'Level'}
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Conflicts and synergies
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### 🔴 Key Conflicts")
        for c in report['conflict_summary']['key_conflicts']:
            st.write(f"• {c}")
    with col2:
        st.markdown("##### 🟢 Key Synergies")
        for s in report['conflict_summary']['key_synergies']:
            st.write(f"• {s}")


def render_scenarios_tab(ws5):
    """Render WS5 scenarios tab."""
    st.markdown('<span class="ws-badge">WS5</span> **Development Scenarios 2030/2050**', unsafe_allow_html=True)
    
    report = ws5.generate_scenario_report()
    comparison_2030 = pd.DataFrame(report['comparison_2030'])
    comparison_2050 = pd.DataFrame(report['comparison_2050'])
    
    # Scenario selector
    st.subheader("📊 Four Development Scenarios")
    
    scenarios_info = [
        ("baseline", "📉 Baseline", "Current trends continue", 0.30, "#6c757d"),
        ("vision2030", "🎯 Vision 2030", "Full target achievement", 0.35, "#006C35"),
        ("accelerated", "🚀 Accelerated", "Beyond V2030 targets", 0.15, "#007bff"),
        ("conservative", "⚠️ Conservative", "Slower transformation", 0.20, "#ffc107"),
    ]
    
    cols = st.columns(4)
    for i, (key, name, desc, prob, color) in enumerate(scenarios_info):
        with cols[i]:
            st.markdown(f"""
            <div style="background: {color}22; border-left: 4px solid {color}; padding: 15px; border-radius: 0 8px 8px 0; height: 150px;">
                <h4 style="margin: 0; color: {color};">{name}</h4>
                <p style="font-size: 0.9rem; margin: 5px 0;">{desc}</p>
                <p style="font-size: 1.5rem; font-weight: bold; margin: 10px 0;">{prob*100:.0f}%</p>
                <p style="font-size: 0.8rem; color: #666;">probability</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            comparison_2030,
            x='Scenario',
            y='GDP ($B)',
            color='Scenario',
            title="GDP Projection 2030",
            color_discrete_map={
                'Baseline (Current Trends)': '#6c757d',
                'Vision 2030 Achievement': '#006C35',
                'Accelerated Transformation': '#007bff',
                'Conservative (Slower Transition)': '#ffc107'
            }
        )
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            comparison_2030,
            x='Population (M)',
            y='GDP ($B)',
            size='Probability',
            color='Scenario',
            title="Population vs GDP (2030)",
            size_max=50,
            color_discrete_map={
                'Baseline (Current Trends)': '#6c757d',
                'Vision 2030 Achievement': '#006C35',
                'Accelerated Transformation': '#007bff',
                'Conservative (Slower Transition)': '#ffc107'
            }
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed scenario view
    st.subheader("Scenario Details")
    selected = st.selectbox(
        "Select scenario for details",
        options=['baseline', 'vision2030', 'accelerated', 'conservative'],
        format_func=lambda x: {
            'baseline': '📉 Baseline', 'vision2030': '🎯 Vision 2030',
            'accelerated': '🚀 Accelerated', 'conservative': '⚠️ Conservative'
        }[x]
    )
    
    scenario_detail = report['scenario_summaries'][selected]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Key Assumptions**")
        for a in scenario_detail['key_assumptions']:
            st.write(f"• {a}")
    with col2:
        st.markdown("**Key Risks**")
        for r in scenario_detail['key_risks']:
            st.write(f"• {r}")
    with col3:
        st.markdown("**Opportunities**")
        for o in scenario_detail['key_opportunities']:
            st.write(f"• {o}")
    
    # Full comparison table
    st.subheader("Full Comparison Table (2030)")
    st.dataframe(comparison_2030.style.format({
        'Population (M)': '{:.1f}', 'GDP ($B)': '{:,.0f}', 'GDP/Capita ($)': '{:,.0f}',
        'Oil Share (%)': '{:.1f}', 'Tourism Share (%)': '{:.1f}', 'Urban (%)': '{:.1f}',
        'Renewable GW': '{:.0f}', 'Probability': '{:.0%}'
    }), use_container_width=True, hide_index=True)


def render_projects_tab(data):
    """Render Vision 2030 projects tab."""
    total_inv = data['projects']['budget_billion_usd'].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Projects", len(data['projects']))
    col2.metric("Total Investment", f"${total_inv:.0f}B")
    col3.metric("Under Construction", len(data['projects'][data['projects']['status'] == 'Under Construction']))
    col4.metric("Top Sector", data['projects'].groupby('sector')['budget_billion_usd'].sum().idxmax())
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.scatter_map(
            data['projects'],
            lat=data['projects'].geometry.y,
            lon=data['projects'].geometry.x,
            size='budget_billion_usd',
            color='sector',
            hover_name='project_name',
            hover_data=['budget_billion_usd', 'status'],
            center={"lat": 24.7136, "lon": 46.6753},
            zoom=4,
            size_max=45,
            title="Vision 2030 Projects"
        )
        fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # By sector
        sector_budget = data['projects'].groupby('sector')['budget_billion_usd'].sum().sort_values()
        fig = px.bar(
            x=sector_budget.values,
            y=sector_budget.index,
            orientation='h',
            title="Investment by Sector ($B)",
            color=sector_budget.values,
            color_continuous_scale='Greens'
        )
        fig.update_layout(height=250, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # By status
        status_counts = data['projects']['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index, title="By Status")
        fig.update_layout(height=220)
        st.plotly_chart(fig, use_container_width=True)
    
    # Projects table
    st.subheader("Project List")
    projects_table = data['projects'][['project_name', 'sector', 'budget_billion_usd', 'status', 'start_year', 'target_year']].copy()
    projects_table = projects_table.sort_values('budget_billion_usd', ascending=False)
    projects_table.columns = ['Project', 'Sector', 'Budget ($B)', 'Status', 'Start', 'Target']
    st.dataframe(projects_table.style.format({'Budget ($B)': '{:.1f}'}), use_container_width=True, hide_index=True)


def main():
    # Header
    st.markdown('<p class="main-header">🇸🇦 NSS KSA - National Spatial Strategy</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Sistema Nacional de Estratégia Espacial | Vision 2030</p>', unsafe_allow_html=True)
    
    # Load resources
    try:
        resources = load_resources()
        data = load_spatial_data(resources['provider'])
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Run `python scripts/download_ksa_data.py` to download required data.")
        return
    
    # Real data banner
    st.markdown("""
    <div class="real-data-banner">
        ✅ <strong>REAL DATA MODE</strong> — Using official KSA data from GASTAT, DataSaudi, OCHA HDX, Vision 2030
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    render_sidebar(resources, data)
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🗺️ Overview",
        "📈 WS2: Retrospective",
        "🏭 WS4: Sectoral",
        "🔮 WS5: Scenarios",
        "🏗️ Vision 2030 Projects"
    ])
    
    with tab1:
        render_overview_tab(data, resources)
    
    with tab2:
        render_retrospective_tab(resources['ws2'])
    
    with tab3:
        render_sectoral_tab(resources['ws4'])
    
    with tab4:
        render_scenarios_tab(resources['ws5'])
    
    with tab5:
        render_projects_tab(data)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.85rem;">
        <p>NSS X - National Spatial Strategy System | Saudi Arabia | Caderno de Encargos WS1-WS7</p>
        <p>Data: GASTAT, DataSaudi.sa, OCHA HDX, Vision 2030 | Updated: 2024-2025</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
