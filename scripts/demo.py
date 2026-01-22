"""
NSS X - Demo Script
Demonstrates the simulation engine and data provider architecture.
Run this to generate demo data and visualize results.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data import get_data_provider, SimulationEngine, COUNTRY_PROFILES
from loguru import logger
import matplotlib.pyplot as plt


def run_demo():
    """Run demonstration of NSS X capabilities."""
    
    logger.info("=" * 60)
    logger.info("NSS X - National Spatial Strategy System")
    logger.info("DEMO MODE - Using Simulation Engine")
    logger.info("=" * 60)
    
    # Initialize simulation engine
    provider = get_data_provider('simulation', profile='country_x', seed=42)
    
    # Health check
    health = provider.health_check()
    logger.info(f"Provider: {health['provider']}")
    logger.info(f"Simulated: {health['is_simulation']}")
    
    print("\n" + "=" * 60)
    print("1. SPATIAL UNITS (REGIONS)")
    print("=" * 60)
    
    # Get regions
    regions_response = provider.get_spatial_units(level=2)
    regions = regions_response.data
    
    print(f"\nGenerated {len(regions)} regions:")
    print(regions[['id', 'code', 'name_en', 'area_sqkm']].to_string())
    
    print("\n" + "=" * 60)
    print("2. SETTLEMENTS")
    print("=" * 60)
    
    # Get all settlements
    settlements_response = provider.get_settlements()
    settlements = settlements_response.data
    
    print(f"\nGenerated {len(settlements)} settlements")
    print("\nTop 10 by population:")
    print(settlements.nlargest(10, 'population')[
        ['name_en', 'population', 'hierarchy_class', 'region_id']
    ].to_string())
    
    # Settlement hierarchy summary
    print("\nSettlement Hierarchy:")
    print(settlements['hierarchy_class'].value_counts().to_string())
    
    print("\n" + "=" * 60)
    print("3. POPULATION DATA (2025)")
    print("=" * 60)
    
    # Get population
    pop_response = provider.get_population(spatial_level=2, year=2025)
    pop_data = pop_response.data
    
    print("\nPopulation by Region:")
    print(pop_data[['name_en', 'population', 'pop_density']].to_string())
    
    total_pop = pop_data['population'].sum()
    print(f"\nTotal Population: {total_pop:,}")
    
    print("\n" + "=" * 60)
    print("4. ECONOMIC DATA (2025)")
    print("=" * 60)
    
    # Get economic data
    econ_response = provider.get_economic_data(indicator='gdp', spatial_level=2, year=2025)
    econ_data = econ_response.data
    
    print("\nGDP by Region:")
    print(econ_data[['name_en', 'gdp_billion_usd', 'gdp_per_capita_usd']].to_string())
    
    total_gdp = econ_data['gdp_billion_usd'].sum()
    print(f"\nTotal GDP: ${total_gdp:.1f} billion")
    
    print("\n" + "=" * 60)
    print("5. INFRASTRUCTURE (ROADS)")
    print("=" * 60)
    
    # Get roads
    roads_response = provider.get_infrastructure(infra_type='roads')
    roads = roads_response.data
    
    print(f"\nGenerated {len(roads)} road segments")
    print("\nRoad network by class:")
    print(roads['road_class'].value_counts().to_string())
    print(f"\nTotal road length: {roads['length_km'].sum():,.0f} km")
    
    print("\n" + "=" * 60)
    print("6. MAJOR PROJECTS")
    print("=" * 60)
    
    # Get projects
    projects_response = provider.get_projects()
    projects = projects_response.data
    
    print(f"\nGenerated {len(projects)} major projects")
    print("\nProjects by status:")
    print(projects['status'].value_counts().to_string())
    print("\nProjects by sector:")
    print(projects['sector'].value_counts().to_string())
    
    total_investment = projects['budget_billion_usd'].sum()
    print(f"\nTotal investment: ${total_investment:.1f} billion")
    
    print("\n" + "=" * 60)
    print("7. SPATIAL ANALYTICS")
    print("=" * 60)
    
    # Calculate primacy index
    top_cities = settlements.nlargest(4, 'population')
    primacy = top_cities['population'].iloc[0] / top_cities['population'].iloc[1:4].sum()
    print(f"\nUrban Primacy Index: {primacy:.2f}")
    
    # Calculate Gini coefficient (simplified)
    pop_values = pop_data['population'].sort_values().values
    n = len(pop_values)
    cumulative = pop_values.cumsum()
    gini = (2 * sum((i + 1) * v for i, v in enumerate(pop_values))) / (n * pop_values.sum()) - (n + 1) / n
    print(f"Population Gini Coefficient: {gini:.3f}")
    
    # HHI for economic concentration
    gdp_shares = econ_data['gdp_billion_usd'] / econ_data['gdp_billion_usd'].sum()
    hhi = (gdp_shares ** 2).sum()
    print(f"Economic Concentration (HHI): {hhi:.3f}")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nThis demo used SIMULATED data.")
    print("In production, the same code connects to REAL data sources.")
    print("\nTo switch to production mode:")
    print("  provider = get_data_provider('production', db_connection_string='...')")
    
    return {
        'regions': regions,
        'settlements': settlements,
        'population': pop_data,
        'economic': econ_data,
        'roads': roads,
        'projects': projects
    }


def create_demo_maps(data: dict):
    """Create demonstration maps."""
    
    logger.info("Generating demo maps...")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # 1. Regions
    ax = axes[0, 0]
    data['regions'].plot(ax=ax, edgecolor='black', alpha=0.7, cmap='Set3')
    ax.set_title('Administrative Regions')
    ax.set_axis_off()
    
    # 2. Settlements by population
    ax = axes[0, 1]
    data['regions'].plot(ax=ax, color='lightgray', edgecolor='white')
    data['settlements'].plot(
        ax=ax, 
        markersize=data['settlements']['population'] / 50000,
        alpha=0.6,
        color='red'
    )
    ax.set_title('Settlements (sized by population)')
    ax.set_axis_off()
    
    # 3. Population density
    ax = axes[0, 2]
    data['population'].plot(
        ax=ax, 
        column='pop_density',
        cmap='YlOrRd',
        legend=True,
        edgecolor='black'
    )
    ax.set_title('Population Density')
    ax.set_axis_off()
    
    # 4. GDP by region
    ax = axes[1, 0]
    data['economic'].plot(
        ax=ax,
        column='gdp_billion_usd',
        cmap='Greens',
        legend=True,
        edgecolor='black'
    )
    ax.set_title('GDP by Region (billion USD)')
    ax.set_axis_off()
    
    # 5. Road network
    ax = axes[1, 1]
    data['regions'].plot(ax=ax, color='lightyellow', edgecolor='lightgray')
    data['roads'][data['roads']['road_class'] == 'highway'].plot(
        ax=ax, color='red', linewidth=2, label='Highway'
    )
    data['roads'][data['roads']['road_class'] == 'primary'].plot(
        ax=ax, color='orange', linewidth=1, label='Primary'
    )
    ax.set_title('Road Network')
    ax.set_axis_off()
    
    # 6. Major projects
    ax = axes[1, 2]
    data['regions'].plot(ax=ax, color='lightblue', edgecolor='white')
    
    colors = {
        'operational': 'green',
        'under_construction': 'orange',
        'planned': 'blue',
        'announced': 'gray'
    }
    
    for status, color in colors.items():
        subset = data['projects'][data['projects']['status'] == status]
        if len(subset) > 0:
            subset.plot(ax=ax, color=color, markersize=50, label=status, alpha=0.7)
    
    ax.legend(loc='lower left', fontsize=8)
    ax.set_title('Major Projects')
    ax.set_axis_off()
    
    plt.tight_layout()
    
    # Save
    output_path = Path(__file__).parent.parent / '06_deliverables' / 'presentations' / 'demo_maps.png'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"Maps saved to: {output_path}")
    
    plt.show()


if __name__ == "__main__":
    data = run_demo()
    
    # Uncomment to generate maps (requires matplotlib display)
    # create_demo_maps(data)
