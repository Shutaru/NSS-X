"""
NSS X - Integrated Analytics Dashboard
Dashboard integrado com análises WS2, WS4, WS5.
Run with: streamlit run scripts/dashboard_analytics.py
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

from src.analysis import (
    RetrospectiveAnalyzer, 
    SectoralAnalyzer,
    ScenarioModeler
)

# Page config
st.set_page_config(
    page_title="NSS KSA - Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {font-size: 2.2rem; font-weight: bold; color: #006C35;}
    .ws-header {font-size: 1.5rem; font-weight: bold; color: #1E3A5F; border-bottom: 2px solid #006C35; padding-bottom: 5px;}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_analyzers():
    return {
        'ws2': RetrospectiveAnalyzer(),
        'ws4': SectoralAnalyzer(),
        'ws5': ScenarioModeler()
    }


def main():
    st.markdown('<p class="main-header">📊 NSS KSA - Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown("Análises do Caderno de Encargos: WS2, WS4, WS5")
    
    analyzers = load_analyzers()
    
    tab1, tab2, tab3 = st.tabs([
        "📈 WS2: Retrospective 2010-2025",
        "🏭 WS4: Sectoral Analysis",
        "🔮 WS5: Scenarios 2030/2050"
    ])
    
    # =========================================================================
    # WS2 - RETROSPECTIVE ANALYSIS
    # =========================================================================
    with tab1:
        st.markdown('<p class="ws-header">WS2: Análise Retrospectiva 2010-2025</p>', unsafe_allow_html=True)
        
        ws2 = analyzers['ws2']
        ts_data = ws2.get_time_series_data()
        report = ws2.generate_retrospective_report()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Pop. Growth", report['key_findings']['population']['growth'], "2010-2025")
        col2.metric("CAGR", report['key_findings']['population']['cagr'])
        col3.metric("Diversification", "49.8% → 62%", "Non-oil GDP")
        
        # Population trends
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            pop_df = ts_data['population']
            fig.add_trace(go.Scatter(x=pop_df['year'], y=pop_df['total_population'], 
                                     name='Total', mode='lines+markers', line=dict(color='#006C35', width=3)))
            fig.add_trace(go.Scatter(x=pop_df['year'], y=pop_df['saudi_population'],
                                     name='Saudi', mode='lines+markers', line=dict(color='#28a745', width=2)))
            fig.add_trace(go.Scatter(x=pop_df['year'], y=pop_df['expat_population'],
                                     name='Expat', mode='lines+markers', line=dict(color='#ffc107', width=2)))
            fig.add_vline(x=2016, line_dash="dash", line_color="red", annotation_text="Vision 2030")
            fig.add_vline(x=2020, line_dash="dot", line_color="gray", annotation_text="COVID-19")
            fig.update_layout(title="Population Trends (Millions)", height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            gdp_df = ts_data['gdp']
            fig = go.Figure()
            fig.add_trace(go.Bar(x=gdp_df['year'], y=gdp_df['gdp_oil_share_pct'], name='Oil GDP %', marker_color='#dc3545'))
            fig.add_trace(go.Bar(x=gdp_df['year'], y=gdp_df['gdp_nonoil_share_pct'], name='Non-oil GDP %', marker_color='#006C35'))
            fig.update_layout(title="Economic Diversification", barmode='stack', height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        # Regional dynamics
        st.subheader("Regional Population Growth")
        regional_df = ts_data['regional']
        
        fig = px.line(
            regional_df, 
            x='year', 
            y='population_millions', 
            color='region',
            title="Regional Population Trends 2010-2025"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Key milestones
        st.subheader("Vision 2030 Milestones")
        milestones = ws2.vision2030_milestones
        cols = st.columns(5)
        for i, (year, event) in enumerate(list(milestones.items())[:5]):
            cols[i].markdown(f"**{year}**")
            cols[i].write(event)
    
    # =========================================================================
    # WS4 - SECTORAL ANALYSIS
    # =========================================================================
    with tab2:
        st.markdown('<p class="ws-header">WS4: Análise Setorial e Conflitos</p>', unsafe_allow_html=True)
        
        ws4 = analyzers['ws4']
        report = ws4.generate_sectoral_report()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Sectors Analyzed", report['sectors_analyzed'])
        col2.metric("Vision 2030 Priorities", report['vision2030_priorities']['count'])
        col3.metric("High Conflicts", report['conflict_summary']['high_conflicts'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sector growth rates
            st.subheader("Sector Growth Rates")
            growth_data = report['high_growth_sectors']
            fig = px.bar(
                x=[d['name'] for d in growth_data],
                y=[d['growth_rate'] for d in growth_data],
                title="Top 5 Growing Sectors",
                labels={'x': 'Sector', 'y': 'Growth Rate (%)'},
                color=[d['growth_rate'] for d in growth_data],
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Conflict matrix heatmap
            st.subheader("Land Use Conflict Matrix")
            matrix = ws4.get_conflict_matrix()
            fig = px.imshow(
                matrix.values,
                x=matrix.columns,
                y=matrix.index,
                color_continuous_scale='RdYlGn',
                title="Conflict (-) / Synergy (+)",
                labels={'color': 'Level'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Sector profiles
        st.subheader("Sector Profiles")
        sectors = ws4.get_all_sectors()
        sector_data = []
        for key, s in sectors.items():
            sector_data.append({
                'Sector': s.name,
                'GDP %': s.gdp_contribution_pct,
                'Employment %': s.employment_share_pct,
                'Growth %': s.growth_rate_pct,
                'Vision 2030': '✅' if s.vision2030_priority else '❌',
                'Water': s.water_intensity
            })
        st.dataframe(pd.DataFrame(sector_data), use_container_width=True)
        
        # Key conflicts and synergies
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔴 Key Conflicts")
            for conflict in report['conflict_summary']['key_conflicts']:
                st.write(f"• {conflict}")
        with col2:
            st.subheader("🟢 Key Synergies")
            for synergy in report['conflict_summary']['key_synergies']:
                st.write(f"• {synergy}")
    
    # =========================================================================
    # WS5 - SCENARIO MODELING
    # =========================================================================
    with tab3:
        st.markdown('<p class="ws-header">WS5: Cenários 2030/2050</p>', unsafe_allow_html=True)
        
        ws5 = analyzers['ws5']
        report = ws5.generate_scenario_report()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Scenarios", report['scenarios_analyzed'])
        col2.metric("Pop. Range 2030", report['key_findings']['population_range_2030'])
        col3.metric("GDP Range 2050", report['key_findings']['gdp_range_2050'])
        
        # Scenario comparison
        st.subheader("Scenario Comparison (2030)")
        comparison_2030 = pd.DataFrame(report['comparison_2030'])
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                comparison_2030,
                x='Scenario',
                y='GDP ($B)',
                color='Probability',
                title="GDP Projections 2030",
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(
                comparison_2030,
                x='Population (M)',
                y='GDP ($B)',
                size='Probability',
                color='Scenario',
                title="Population vs GDP (2030)",
                size_max=40
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Scenario details
        st.subheader("Scenario Details")
        scenario_select = st.selectbox(
            "Select Scenario",
            options=['baseline', 'vision2030', 'accelerated', 'conservative'],
            format_func=lambda x: report['scenario_summaries'][x]['name']
        )
        
        selected = report['scenario_summaries'][scenario_select]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Key Assumptions**")
            for a in selected['key_assumptions']:
                st.write(f"• {a}")
        with col2:
            st.markdown("**Key Risks**")
            for r in selected['key_risks']:
                st.write(f"• {r}")
        with col3:
            st.markdown("**Opportunities**")
            for o in selected['key_opportunities']:
                st.write(f"• {o}")
        
        st.metric("Probability", f"{selected['probability']*100:.0f}%")
        
        # Comparison table
        st.subheader("Full Comparison")
        st.dataframe(comparison_2030.style.format({
            'Population (M)': '{:.1f}',
            'GDP ($B)': '{:,.0f}',
            'GDP/Capita ($)': '{:,.0f}',
            'Oil Share (%)': '{:.1f}',
            'Tourism Share (%)': '{:.1f}',
            'Urban (%)': '{:.1f}',
            'Renewable GW': '{:.0f}',
            'Probability': '{:.0%}'
        }), use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("NSS X - National Spatial Strategy | Analytics Module | Caderno de Encargos WS2/WS4/WS5")


if __name__ == "__main__":
    main()
