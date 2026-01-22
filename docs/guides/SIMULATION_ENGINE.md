# NSS X - Simulation Engine Configuration

## Overview

The NSS X system uses a **dual-mode architecture** that separates the solution from the data source:

```
┌─────────────────────────────────────────────────────────────────┐
│                     NSS X APPLICATION                            │
│  (Analytics, Scenarios, Strategy, Dashboards)                   │
├─────────────────────────────────────────────────────────────────┤
│                  DataProviderInterface                           │
│           (Abstract interface for all data access)              │
├─────────────────┬───────────────────────────────────────────────┤
│                 │                                                │
│   PRODUCTION    │            SIMULATION                         │
│   PROVIDER      │             ENGINE                            │
│                 │                                                │
│  ┌───────────┐  │  ┌─────────────────────────────────────────┐  │
│  │PostgreSQL │  │  │ Generates realistic synthetic data:     │  │
│  │ + PostGIS │  │  │  • Demographic distributions            │  │
│  ├───────────┤  │  │  • Economic indicators                  │  │
│  │ GIS Files │  │  │  • Settlement hierarchies               │  │
│  ├───────────┤  │  │  • Infrastructure networks              │  │
│  │   APIs    │  │  │  • Major projects                       │  │
│  └───────────┘  │  │  • Environmental layers                 │  │
│                 │  └─────────────────────────────────────────┘  │
└─────────────────┴───────────────────────────────────────────────┘
```

## Why This Architecture?

1. **Production-Ready from Day 1**: The main application code never references mock data
2. **Seamless Transition**: Switch from simulation to real data by changing one parameter
3. **Realistic Demos**: Simulation generates statistically plausible data
4. **Testing**: Run comprehensive tests without needing real data access
5. **Client Buy-in**: Demonstrate capabilities before data agreements are finalized

## Usage

### Demo/Testing Mode (Simulation)
```python
from src.data import get_data_provider

# Use simulation engine
provider = get_data_provider('simulation', profile='country_x', seed=42)

# Get data - same interface as production
regions = provider.get_spatial_units(level=2)
settlements = provider.get_settlements()
population = provider.get_population(spatial_level=2, year=2025)
```

### Production Mode (Real Data)
```python
from src.data import get_data_provider

# Use real data sources
provider = get_data_provider('production', 
    db_connection_string='postgresql://...',
    data_directory=Path('./data/gis')
)

# Same interface - no code changes needed
regions = provider.get_spatial_units(level=2)
settlements = provider.get_settlements()
population = provider.get_population(spatial_level=2, year=2025)
```

### Auto Mode
```python
# Auto-detect: uses production if configured, falls back to simulation
provider = get_data_provider('auto')
```

## Country Profiles

Pre-configured profiles for simulation:

| Profile | Population | Area (km²) | Regions | GDP (B$) |
|---------|------------|------------|---------|----------|
| `country_x` | 35M | 2.15M | 13 | 850 |
| `medium_country` | 15M | 500K | 8 | 200 |
| `small_country` | 5M | 100K | 5 | 50 |

### Custom Profile
```python
from src.data import SimulationEngine, CountryProfile

custom_profile = CountryProfile(
    name="Custom Country",
    total_population=20_000_000,
    total_area_sqkm=750_000,
    num_regions=10,
    gdp_billion_usd=300,
    urban_population_pct=75,
    center_lat=30.0,
    center_lon=35.0,
    bbox=(30.0, 25.0, 40.0, 35.0)
)

provider = SimulationEngine(profile=custom_profile, seed=42)
```

## Simulation Realism

The simulation engine generates data using realistic statistical models:

### Demographics
- **Population Distribution**: Pareto distribution (Zipf's law for cities)
- **Settlement Hierarchy**: Based on configurable thresholds
- **Urbanization**: Configurable urban population percentage

### Economy
- **GDP Distribution**: Correlated with population but with noise
- **Regional Inequality**: Configurable Gini coefficient
- **Employment**: Inversely correlated with prosperity

### Spatial
- **Regions**: Voronoi-like partitioning with irregular boundaries
- **Settlements**: Placed within regions, clustered by density
- **Roads**: Network connecting major settlements

### Projects
- **Types**: Giga projects, industrial zones, tourism, tech parks
- **Status**: Realistic distribution (announced → operational)
- **Budgets**: Based on project type ranges

## Running Demos

### Command Line Demo
```bash
cd "c:\Users\shuta\source\repos\NSS X"
python scripts/demo.py
```

### Interactive Dashboard
```bash
cd "c:\Users\shuta\source\repos\NSS X"
streamlit run scripts/dashboard_demo.py
```

## Data Provider Interface

All data providers implement `DataProviderInterface`:

| Method | Description |
|--------|-------------|
| `get_spatial_units(level)` | Administrative boundaries |
| `get_settlements(filters)` | Settlement points |
| `get_population(level, year, scenario)` | Population data |
| `get_economic_data(indicator, level, year)` | Economic indicators |
| `get_infrastructure(type, region)` | Infrastructure layers |
| `get_environment(type, region)` | Environmental layers |
| `get_projects(status, sector)` | Major projects |
| `health_check()` | Provider status |

## Adding New Data Types

1. Add method to `DataProviderInterface`
2. Implement in `SimulationEngine` (generate synthetic data)
3. Implement in `ProductionDataProvider` (connect to real source)
4. Application code works unchanged with both providers

---

*Documentation v1.0 - January 2026*
