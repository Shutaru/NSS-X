"""
NSS - Real Data Provider for Saudi Arabia
Loads and serves actual KSA data from downloaded files.
Implements the same DataProviderInterface as SimulationEngine.
"""

import pandas as pd
import geopandas as gpd
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from loguru import logger

from .provider_interface import DataProviderInterface, DataResponse, DataProviderFactory


class RealDataProvider(DataProviderInterface):
    """
    Real data provider that loads actual KSA statistics and GIS data.
    Implements DataProviderInterface for seamless integration.
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize real data provider.
        
        Args:
            data_dir: Path to raw data directory. Defaults to 01_data/01_raw
        """
        if data_dir is None:
            data_dir = Path(__file__).parent.parent.parent / "01_data" / "01_raw"
        
        self.data_dir = Path(data_dir)
        self.gis_dir = self.data_dir / "gis" / "admin_boundaries"
        self.stats_dir = self.data_dir / "statistics"
        
        # Cache for loaded data
        self._cache: Dict[str, Any] = {}
        
        # Validate data exists
        self._validate_data_files()
        
        logger.info(f"Real Data Provider initialized")
        logger.info(f"  Data directory: {self.data_dir}")
        logger.info(f"  GIS files: {len(list(self.gis_dir.glob('*.geojson')))} GeoJSON files")
        logger.info(f"  Statistics: {len(list(self.stats_dir.glob('*.csv')))} CSV files")
    
    def _validate_data_files(self):
        """Validate that required data files exist."""
        required_files = [
            self.gis_dir / "sau_admin1.geojson",
            self.stats_dir / "ksa_population_by_region.csv",
            self.stats_dir / "ksa_major_cities.csv",
            self.stats_dir / "ksa_economic_indicators.csv",
            self.stats_dir / "ksa_vision2030_projects.csv"
        ]
        
        missing = [f for f in required_files if not f.exists()]
        if missing:
            raise FileNotFoundError(
                f"Missing required data files: {missing}\n"
                f"Run 'python scripts/download_ksa_data.py' to download data."
            )
    
    @property
    def provider_name(self) -> str:
        return "RealDataProvider:Saudi Arabia"
    
    @property
    def is_simulation(self) -> bool:
        return False
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Get cached data."""
        return self._cache.get(key)
    
    def _set_cached(self, key: str, data: Any):
        """Cache data."""
        self._cache[key] = data
    
    def _make_response(self, data, source: str, metadata: Dict[str, Any]) -> DataResponse:
        """Helper to create DataResponse with common fields."""
        return DataResponse(
            data=data,
            metadata=metadata,
            source=source,
            retrieved_at=datetime.now(),
            is_simulated=False
        )
    
    # =========================================================================
    # SPATIAL UNITS
    # =========================================================================
    
    def get_spatial_units(self, level: int = 2) -> DataResponse:
        """
        Get administrative boundaries.
        
        Args:
            level: 1=country, 2=regions (default)
        """
        cache_key = f"spatial_units_{level}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return self._make_response(cached, "OCHA HDX (cached)", {"level": level})
        
        if level == 1:
            gdf = gpd.read_file(self.gis_dir / "sau_admin0.geojson")
        else:
            gdf = gpd.read_file(self.gis_dir / "sau_admin1.geojson")
        
        # Standardize column names based on actual OCHA data structure
        gdf = gdf.rename(columns={
            'adm1_name': 'name_en',
            'adm1_name1': 'name_ar', 
            'adm1_pcode': 'code',
            'adm0_name': 'country',
        })
        
        # Add ID column if not present
        if 'id' not in gdf.columns:
            gdf['id'] = range(1, len(gdf) + 1)
        
        # Calculate area if not present
        if 'area_sqkm' not in gdf.columns or gdf['area_sqkm'].isna().all():
            gdf_proj = gdf.to_crs("EPSG:32638")  # UTM Zone 38N for Saudi Arabia
            gdf['area_sqkm'] = gdf_proj.geometry.area / 1e6
        
        self._set_cached(cache_key, gdf)
        
        return self._make_response(
            gdf,
            source="OCHA HDX",
            metadata={
                "level": level,
                "count": len(gdf),
                "crs": str(gdf.crs)
            }
        )
    
    # =========================================================================
    # SETTLEMENTS
    # =========================================================================
    
    def get_settlements(self, 
                        min_population: Optional[int] = None,
                        region_id: Optional[int] = None) -> DataResponse:
        """Get major cities and settlements."""
        min_pop = min_population or 0
        cache_key = f"settlements_{min_pop}_{region_id}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return self._make_response(cached, "GASTAT (cached)", {"count": len(cached)})
        
        # Load cities data
        df = pd.read_csv(self.stats_dir / "ksa_major_cities.csv")
        
        # Filter by population
        df = df[df['population_estimate'] >= min_pop]
        
        # Create GeoDataFrame
        gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df['longitude'], df['latitude']),
            crs="EPSG:4326"
        )
        
        # Add hierarchy class based on population
        def classify_settlement(pop):
            if pop >= 3_000_000:
                return "Metropolis"
            elif pop >= 1_000_000:
                return "Large City"
            elif pop >= 500_000:
                return "Medium City"
            elif pop >= 100_000:
                return "Small City"
            else:
                return "Town"
        
        gdf['hierarchy_class'] = gdf['population_estimate'].apply(classify_settlement)
        gdf['population'] = gdf['population_estimate']
        gdf['name_en'] = gdf['city_name_en']
        
        self._set_cached(cache_key, gdf)
        
        return self._make_response(
            gdf,
            source="GASTAT",
            metadata={
                "count": len(gdf),
                "min_population": min_pop
            }
        )
    
    # =========================================================================
    # POPULATION
    # =========================================================================
    
    def get_population(self, 
                       spatial_level: int, 
                       year: int,
                       scenario_id: Optional[str] = None) -> DataResponse:
        """Get population data by region."""
        cache_key = f"population_{spatial_level}_{year}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return self._make_response(cached, "GASTAT (cached)", {"year": year})
        
        # Load population data
        df = pd.read_csv(self.stats_dir / "ksa_population_by_region.csv")
        
        # Rename for consistency
        df = df.rename(columns={
            'population_2024': 'population',
            'area_km2': 'area_sqkm',
            'pop_density_2022': 'pop_density'
        })
        
        df['year'] = year
        df['name_en'] = df['region_name_en']
        
        self._set_cached(cache_key, df)
        
        return self._make_response(
            df,
            source="GASTAT 2024",
            metadata={
                "year": year,
                "total_population": df['population'].sum(),
                "spatial_level": spatial_level
            }
        )
    
    # =========================================================================
    # ECONOMIC DATA
    # =========================================================================
    
    def get_economic_data(self, 
                          indicator: str,
                          spatial_level: int,
                          year: int) -> DataResponse:
        """Get economic indicators."""
        cache_key = f"economic_{indicator}_{spatial_level}_{year}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return self._make_response(cached, "GASTAT/DataSaudi (cached)", {"indicator": indicator})
        
        # Load economic indicators
        df_indicators = pd.read_csv(self.stats_dir / "ksa_economic_indicators.csv")
        
        # Load population for per-capita calculations
        pop_df = pd.read_csv(self.stats_dir / "ksa_population_by_region.csv")
        
        # Get total GDP from indicators
        gdp_row = df_indicators[df_indicators['indicator'] == 'GDP (Nominal)']
        total_gdp_sar = gdp_row['value'].values[0] if len(gdp_row) > 0 else 4700
        
        # Convert to USD (approximate rate)
        total_gdp_usd = total_gdp_sar / 3.75  # SAR to USD
        
        # Distribute GDP by region (proportional to population with adjustment)
        pop_df['pop_share'] = pop_df['population_2024'] / pop_df['population_2024'].sum()
        
        # Add regional adjustment factor (Eastern Province has oil, higher GDP)
        region_factors = {
            'Riyadh': 1.3,
            'Makkah': 1.1,
            'Eastern Province': 1.8,  # Oil industry
            'Madinah': 1.0,
            'Al-Qassim': 0.9,
            'Asir': 0.8,
            'Tabuk': 0.7,
            'Hail': 0.7,
            'Northern Borders': 0.6,
            'Jazan': 0.7,
            'Najran': 0.6,
            'Al-Baha': 0.6,
            'Al-Jouf': 0.6
        }
        
        pop_df['region_factor'] = pop_df['region_name_en'].map(region_factors).fillna(1.0)
        pop_df['adjusted_share'] = pop_df['pop_share'] * pop_df['region_factor']
        pop_df['adjusted_share'] = pop_df['adjusted_share'] / pop_df['adjusted_share'].sum()
        
        # Calculate regional GDP
        result_df = pd.DataFrame({
            'region_code': pop_df['region_code'],
            'name_en': pop_df['region_name_en'],
            'year': year,
            'gdp_billion_usd': pop_df['adjusted_share'] * total_gdp_usd,
            'population': pop_df['population_2024']
        })
        
        result_df['gdp_per_capita_usd'] = (
            result_df['gdp_billion_usd'] * 1e9 / result_df['population']
        )
        
        self._set_cached(cache_key, result_df)
        
        return self._make_response(
            result_df,
            source="GASTAT/DataSaudi 2024",
            metadata={
                "year": year,
                "total_gdp_usd": total_gdp_usd,
                "indicator": indicator,
                "spatial_level": spatial_level
            }
        )
    
    # =========================================================================
    # INFRASTRUCTURE
    # =========================================================================
    
    def get_infrastructure(self,
                           infra_type: str,
                           region_id: Optional[int] = None) -> DataResponse:
        """
        Get infrastructure data.
        Note: Road network data would come from OpenStreetMap or MOMRA.
        For now, returns placeholder based on regions.
        """
        # Create placeholder road data connecting major cities
        cities = self.get_settlements().data
        
        # For demo, create simple connections between nearby cities
        roads = []
        road_id = 1
        
        major_cities = cities[cities['population'] >= 500_000].copy()
        
        for i, city1 in major_cities.iterrows():
            # Connect to 2-3 nearest cities
            distances = major_cities.geometry.distance(city1.geometry)
            nearest = distances.nsmallest(4).index[1:4]
            
            for j in nearest:
                city2 = major_cities.loc[j]
                from shapely.geometry import LineString
                line = LineString([city1.geometry, city2.geometry])
                
                roads.append({
                    'id': road_id,
                    'road_name': f"{city1['city_name_en']} - {city2['city_name_en']}",
                    'road_class': 'highway',
                    'length_km': line.length * 111,  # Approximate km
                    'lanes': 4,
                    'status': 'operational',
                    'geometry': line
                })
                road_id += 1
        
        gdf = gpd.GeoDataFrame(roads, crs="EPSG:4326")
        
        return self._make_response(
            gdf,
            source="Derived from city locations",
            metadata={
                "type": infra_type,
                "note": "Placeholder data - real road data from MOMRA/OSM needed"
            }
        )
    
    # =========================================================================
    # ENVIRONMENT
    # =========================================================================
    
    def get_environment(self,
                        layer_type: str,
                        region_id: Optional[int] = None) -> DataResponse:
        """Get environmental indicators."""
        if layer_type == "water":
            df = pd.read_csv(self.stats_dir / "ksa_water_consumption.csv")
            return self._make_response(
                df,
                source="DataSaudi 2022",
                metadata={
                    "indicator": layer_type,
                    "unit": "million cubic meters"
                }
            )
        
        # Placeholder for other indicators
        return self._make_response(
            pd.DataFrame(),
            source="N/A",
            metadata={"error": f"Layer type {layer_type} not available"}
        )
    
    # =========================================================================
    # PROJECTS
    # =========================================================================
    
    def get_projects(self, 
                     status: Optional[str] = None,
                     sector: Optional[str] = None) -> DataResponse:
        """Get Vision 2030 projects."""
        cache_key = f"projects_{status}_{sector}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return self._make_response(cached, "Vision 2030 (cached)", {"count": len(cached)})
        
        # Load projects
        df = pd.read_csv(self.stats_dir / "ksa_vision2030_projects.csv")
        
        # Filter by status
        if status:
            df = df[df['status'].str.lower() == status.lower()]
        
        # Filter by sector
        if sector:
            df = df[df['sector'].str.lower() == sector.lower()]
        
        # Create GeoDataFrame
        gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df['longitude'], df['latitude']),
            crs="EPSG:4326"
        )
        
        self._set_cached(cache_key, gdf)
        
        return self._make_response(
            gdf,
            source="Vision 2030 Official Data",
            metadata={
                "count": len(gdf),
                "total_investment_billion": gdf['budget_billion_usd'].sum(),
                "status_filter": status,
                "sector_filter": sector
            }
        )
    
    # =========================================================================
    # EMPLOYMENT
    # =========================================================================
    
    def get_employment(self, year: int = 2025) -> DataResponse:
        """Get employment data by region."""
        df = pd.read_csv(self.stats_dir / "ksa_employment_by_region.csv")
        df['year'] = year
        
        return self._make_response(
            df,
            source="GOSI Q3 2025",
            metadata={
                "total_employees": df['total_gosi_employees'].sum()
            }
        )


# Register with factory
DataProviderFactory.register('real', RealDataProvider)
DataProviderFactory.register('production', RealDataProvider)  # Alias
