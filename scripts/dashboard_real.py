"""
NSS X - Real Data Dashboard for Saudi Arabia
Streamlit dashboard using actual KSA data from GASTAT, OCHA, and DataSaudi.
Run with: streamlit run scripts/dashboard_real.py
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

from src.data.real_data_provider import RealDataProvider

# Page config
st.set_page_config(
    page_title="NSS KSA - National Spatial Strategy",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #006C35;  /* KSA Green */
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-top: 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .real-data-banner {
        background-color: #d4edda;
        border: 1px solid #28a745;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 20px;
    }
    .vision2030 {
        background: linear-gradient(135deg, #006C35 0%, #00563B 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_provider():
    """Get cached real data provider."""
    return RealDataProvider()


@st.cache_data
def load_all_data(_provider):
    """Load all data from provider (cached)."""
    return {
        'regions': _provider.get_spatial_units(level=2).data,
        'settlements': _provider.get_settlements().data,
        'population': _provider.get_population(spatial_level=2, year=2024).data,
        'economic': _provider.get_economic_data('gdp', spatial_level=2, year=2024).data,
        'projects': _provider.get_projects().data,
        'employment': _provider.get_employment().data,
        'water': _provider.get_environment('water').data
    }


def main():
    # Header
    col_h1, col_h2 = st.columns([4, 1])
    with col_h1:
        st.markdown('<p class="main-header">🇸🇦 NSS KSA - National Spatial Strategy</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Sistema Nacional de Decisão Espacial para a Arábia Saudita | Vision 2030</p>', unsafe_allow_html=True)
    
    # Real data banner
    st.markdown("""
    <div class="real-data-banner">
        ✅ <strong>REAL DATA MODE</strong> - This dashboard uses actual data from official KSA sources:
        GASTAT, DataSaudi.sa, OCHA HDX, and Vision 2030 Program.
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    try:
        provider = get_provider()
        data = load_all_data(provider)
    except FileNotFoundError as e:
        st.error(f"Data not found. Please run: `python scripts/download_ksa_data.py`\n\nError: {e}")
        return
    
    # Sidebar
    st.sidebar.header("⚙️ Configuration")
    st.sidebar.markdown("### 🇸🇦 Saudi Arabia Profile")
    st.sidebar.write(f"**Data Source:** GASTAT/DataSaudi")
    st.sidebar.write(f"**Provider:** {provider.provider_name}")
    st.sidebar.write(f"**Simulation:** {provider.is_simulation}")
    st.sidebar.markdown("---")
    
    total_pop = data['population']['population'].sum()
    st.sidebar.write(f"**Population (2024):** {total_pop/1e6:.1f}M")
    st.sidebar.write(f"**Regions:** {len(data['regions'])}")
    st.sidebar.write(f"**GDP (2024):** ${data['economic']['gdp_billion_usd'].sum():.0f}B")
    st.sidebar.write(f"**Vision 2030 Projects:** {len(data['projects'])}")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Data Sources")
    st.sidebar.markdown("""
    - 📊 [GASTAT](https://stats.gov.sa)
    - 📈 [DataSaudi](https://datasaudi.sa)
    - 🗺️ [OCHA HDX](https://data.humdata.org)
    - 🎯 [Vision 2030](https://vision2030.gov.sa)
    """)
    
    # Key metrics
    st.header("📊 Key Indicators (2024)")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_gdp = data['economic']['gdp_billion_usd'].sum()
    n_cities = len(data['settlements'])
    n_projects = len(data['projects'])
    total_investment = data['projects']['budget_billion_usd'].sum()
    
    col1.metric("Population", f"{total_pop/1e6:.1f}M", "2024 Census")
    col2.metric("GDP", f"${total_gdp:.0f}B", "2024 Est.")
    col3.metric("Major Cities", f"{n_cities}", "Pop > 50k")
    col4.metric("Vision 2030 Projects", f"{n_projects}")
    col5.metric("Total Investment", f"${total_investment:.0f}B", "Committed")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🗺️ Spatial Overview",
        "👥 Demographics",
        "💰 Economy",
        "🏗️ Vision 2030 Projects",
        "👷 Employment",
        "📈 Analytics"
    ])
    
    with tab1:
        st.subheader("Saudi Arabia - Administrative Regions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Merge population with regions for choropleth
            regions_pop = data['regions'].merge(
                data['population'][['region_name_en', 'population']],
                left_on='name_en',
                right_on='region_name_en',
                how='left'
            )
            regions_pop['population'] = regions_pop['population'].fillna(0)
            
            # Regions map
            fig = px.choropleth_mapbox(
                regions_pop,
                geojson=regions_pop.geometry.__geo_interface__,
                locations=regions_pop.index,
                color='population',
                hover_name='name_en',
                hover_data=['area_sqkm', 'population'],
                mapbox_style="carto-positron",
                center={"lat": 24.7136, "lon": 46.6753},
                zoom=4,
                opacity=0.7,
                color_continuous_scale='Greens',
                title="Population by Region"
            )
            fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, height=450)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Settlements scatter
            fig = px.scatter_mapbox(
                data['settlements'],
                lat=data['settlements'].geometry.y,
                lon=data['settlements'].geometry.x,
                size='population',
                color='hierarchy_class',
                hover_name='name_en',
                hover_data=['population', 'region_code'],
                mapbox_style="carto-positron",
                center={"lat": 24.7136, "lon": 46.6753},
                zoom=4,
                size_max=35,
                color_discrete_map={
                    'Metropolis': '#006C35',
                    'Large City': '#28a745',
                    'Medium City': '#74c476',
                    'Small City': '#c7e9c0',
                    'Town': '#edf8e9'
                },
                title="Major Cities (by Population)"
            )
            fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, height=450)
            st.plotly_chart(fig, use_container_width=True)
        
        # Area table
        st.subheader("Regions Overview")
        region_summary = data['regions'][['name_en', 'code', 'area_sqkm']].copy()
        region_summary = region_summary.merge(
            data['population'][['region_name_en', 'population']],
            left_on='name_en',
            right_on='region_name_en',
            how='left'
        )
        region_summary['pop_density'] = region_summary['population'] / region_summary['area_sqkm']
        region_summary = region_summary.sort_values('population', ascending=False)
        region_summary = region_summary[['name_en', 'code', 'area_sqkm', 'population', 'pop_density']]
        region_summary.columns = ['Region', 'Code', 'Area (km²)', 'Population', 'Density (pop/km²)']
        st.dataframe(region_summary.style.format({
            'Area (km²)': '{:,.0f}',
            'Population': '{:,.0f}',
            'Density (pop/km²)': '{:.1f}'
        }), use_container_width=True)
    
    with tab2:
        st.subheader("Demographics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Population by region
            pop_sorted = data['population'].sort_values('population', ascending=True)
            fig = px.bar(
                pop_sorted,
                x='population',
                y='region_name_en',
                orientation='h',
                title="Population by Region (2024)",
                labels={'population': 'Population', 'region_name_en': 'Region'},
                color='population',
                color_continuous_scale='Greens'
            )
            fig.update_layout(height=450, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Population pie
            top_regions = data['population'].nlargest(6, 'population')
            others = pd.DataFrame({
                'region_name_en': ['Other Regions'],
                'population': [data['population']['population'].sum() - top_regions['population'].sum()]
            })
            pie_data = pd.concat([top_regions[['region_name_en', 'population']], others])
            
            fig = px.pie(
                pie_data,
                values='population',
                names='region_name_en',
                title="Population Distribution",
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)
        
        # Urban hierarchy
        st.subheader("Urban Hierarchy")
        hierarchy_counts = data['settlements']['hierarchy_class'].value_counts().reset_index()
        hierarchy_counts.columns = ['Class', 'Count']
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.dataframe(hierarchy_counts, use_container_width=True)
        with col2:
            fig = px.bar(
                hierarchy_counts,
                x='Class',
                y='Count',
                title="Settlement Hierarchy",
                color='Class',
                color_discrete_map={
                    'Metropolis': '#006C35',
                    'Large City': '#28a745',
                    'Medium City': '#74c476',
                    'Small City': '#c7e9c0',
                    'Town': '#edf8e9'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Economic Indicators")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # GDP by region
            econ_sorted = data['economic'].sort_values('gdp_billion_usd', ascending=True)
            fig = px.bar(
                econ_sorted,
                x='gdp_billion_usd',
                y='name_en',
                orientation='h',
                title="Regional GDP (Est. 2024)",
                labels={'gdp_billion_usd': 'GDP (Billion USD)', 'name_en': 'Region'},
                color='gdp_billion_usd',
                color_continuous_scale='Greens'
            )
            fig.update_layout(height=450, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # GDP per capita
            fig = px.bar(
                data['economic'].sort_values('gdp_per_capita_usd', ascending=True),
                x='gdp_per_capita_usd',
                y='name_en',
                orientation='h',
                title="GDP per Capita (Est. 2024)",
                labels={'gdp_per_capita_usd': 'GDP per Capita (USD)', 'name_en': 'Region'},
                color='gdp_per_capita_usd',
                color_continuous_scale='Greens'
            )
            fig.update_layout(height=450, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Economic summary
        st.markdown("### Economic Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total GDP", f"${total_gdp:.0f}B USD")
        col2.metric("GDP per Capita (avg)", f"${data['economic']['gdp_per_capita_usd'].mean():,.0f}")
        col3.metric("Top Region (GDP)", data['economic'].nlargest(1, 'gdp_billion_usd')['name_en'].values[0])
    
    with tab4:
        st.subheader("Vision 2030 Mega Projects")
        
        # Vision 2030 intro
        st.markdown("""
        <div class="vision2030">
            <h3 style="margin:0; color: white;">🎯 Vision 2030</h3>
            <p style="margin-top: 5px;">Saudi Arabia's strategic framework to reduce dependence on oil, 
            diversify the economy, and develop public sectors like health, education, infrastructure, 
            recreation, and tourism.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Projects map
            fig = px.scatter_mapbox(
                data['projects'],
                lat=data['projects'].geometry.y,
                lon=data['projects'].geometry.x,
                size='budget_billion_usd',
                color='sector',
                hover_name='project_name',
                hover_data=['budget_billion_usd', 'status', 'start_year', 'target_year'],
                mapbox_style="carto-positron",
                center={"lat": 24.7136, "lon": 46.6753},
                zoom=4,
                size_max=40,
                title="Vision 2030 Projects by Investment"
            )
            fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Projects by sector
            sector_budget = data['projects'].groupby('sector')['budget_billion_usd'].sum().sort_values(ascending=True)
            fig = px.bar(
                x=sector_budget.values,
                y=sector_budget.index,
                orientation='h',
                title="Investment by Sector",
                labels={'x': 'Budget (Billion USD)', 'y': 'Sector'}
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Status summary
            status_counts = data['projects']['status'].value_counts()
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Projects by Status",
                color_discrete_sequence=['#006C35', '#ffc107', '#dc3545']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Projects table
        st.subheader("Project Details")
        projects_table = data['projects'][['project_name', 'sector', 'region_code', 'budget_billion_usd', 'status', 'start_year', 'target_year']].copy()
        projects_table = projects_table.sort_values('budget_billion_usd', ascending=False)
        projects_table.columns = ['Project', 'Sector', 'Region', 'Budget ($B)', 'Status', 'Start', 'Target']
        st.dataframe(projects_table.style.format({'Budget ($B)': '{:.1f}'}), use_container_width=True)
    
    with tab5:
        st.subheader("Employment by Region")
        
        col1, col2 = st.columns(2)
        
        with col1:
            emp_sorted = data['employment'].sort_values('total_gosi_employees', ascending=True)
            fig = px.bar(
                emp_sorted,
                x='total_gosi_employees',
                y='region_name_en',
                orientation='h',
                title="GOSI Registered Employees by Region (Q3 2025)",
                labels={'total_gosi_employees': 'Employees', 'region_name_en': 'Region'},
                color='total_gosi_employees',
                color_continuous_scale='Greens'
            )
            fig.update_layout(height=450, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Employment distribution
            fig = px.pie(
                data['employment'].nlargest(6, 'total_gosi_employees'),
                values='total_gosi_employees',
                names='region_name_en',
                title="Employment Concentration",
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
            st.plotly_chart(fig, use_container_width=True)
        
        total_emp = data['employment']['total_gosi_employees'].sum()
        st.metric("Total GOSI Employees", f"{total_emp/1e6:.1f}M")
    
    with tab6:
        st.subheader("Spatial Analytics")
        
        # Population vs GDP scatter
        col1, col2 = st.columns(2)
        
        with col1:
            merged = data['population'].merge(
                data['economic'][['name_en', 'gdp_billion_usd', 'gdp_per_capita_usd']],
                left_on='region_name_en',
                right_on='name_en',
                how='left'
            )
            
            fig = px.scatter(
                merged,
                x='population',
                y='gdp_billion_usd',
                size='gdp_per_capita_usd',
                color='region_name_en',
                hover_name='region_name_en',
                title="Population vs GDP by Region",
                labels={'population': 'Population', 'gdp_billion_usd': 'GDP (Billion USD)'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Regional development index
            merged['dev_index'] = (
                merged['gdp_per_capita_usd'] / merged['gdp_per_capita_usd'].max() * 100
            )
            fig = px.bar(
                merged.sort_values('dev_index', ascending=True),
                x='dev_index',
                y='region_name_en',
                orientation='h',
                title="Regional Development Index",
                labels={'dev_index': 'Index (0-100)', 'region_name_en': 'Region'},
                color='dev_index',
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Analysis insights
        st.markdown("### Key Insights")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Population Concentration**")
            top3_pop = data['population'].nlargest(3, 'population')
            top3_share = top3_pop['population'].sum() / total_pop * 100
            st.write(f"Top 3 regions (Riyadh, Makkah, Eastern) hold **{top3_share:.1f}%** of population")
        
        with col2:
            st.markdown("**Economic Concentration**")
            top3_gdp = data['economic'].nlargest(3, 'gdp_billion_usd')
            top3_gdp_share = top3_gdp['gdp_billion_usd'].sum() / total_gdp * 100
            st.write(f"Top 3 regions generate **{top3_gdp_share:.1f}%** of GDP")
        
        with col3:
            st.markdown("**Investment Focus**")
            top_sector = data['projects'].groupby('sector')['budget_billion_usd'].sum().idxmax()
            top_sector_share = data['projects'][data['projects']['sector'] == top_sector]['budget_billion_usd'].sum() / total_investment * 100
            st.write(f"**{top_sector}** sector receives **{top_sector_share:.1f}%** of Vision 2030 investment")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>NSS X - National Spatial Strategy System | Data Updated: 2024-2025</p>
        <p>Sources: GASTAT, DataSaudi.sa, OCHA HDX, Vision 2030 Program</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
