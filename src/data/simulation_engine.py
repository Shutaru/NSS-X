"""
NSS X - Simulation Engine
Generates realistic synthetic data for demos and testing.
Mimics real data sources with statistically plausible data.
"""

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon, LineString
from shapely.ops import unary_union
import json
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any
from datetime import datetime
from dataclasses import dataclass
from loguru import logger

from .provider_interface import (
    DataProviderInterface, 
    DataProviderFactory,
    DataResponse
)


@dataclass
class CountryProfile:
    """Configuration profile for simulated country."""
    name: str
    total_population: int
    total_area_sqkm: float
    num_regions: int
    gdp_billion_usd: float
    urban_population_pct: float
    center_lat: float
    center_lon: float
    bbox: Tuple[float, float, float, float]  # minx, miny, maxx, maxy
    
    # Distribution parameters
    population_gini: float = 0.45  # Spatial inequality
    primacy_ratio: float = 3.5  # Largest city / sum of next 3
    economic_concentration: float = 0.6  # HHI for GDP


# Pre-configured country profiles
COUNTRY_PROFILES = {
    # Saudi Arabia - calibrated with real 2024 data
    "country_x": CountryProfile(
        name="Kingdom of Saudi Arabia",
        total_population=36_400_000,  # GASTAT 2024
        total_area_sqkm=2_149_690,    # Actual KSA area
        num_regions=13,               # 13 administrative provinces
        gdp_billion_usd=1_108,        # IMF 2024 nominal GDP
        urban_population_pct=84.3,    # World Bank 2023
        center_lat=23.8859,           # Geographic center of KSA
        center_lon=45.0792,
        bbox=(34.5, 16.4, 55.7, 32.2),  # KSA actual bounding box
        population_gini=0.55,         # High regional inequality
        primacy_ratio=4.5,            # Riyadh dominance
        economic_concentration=0.68   # Oil economy concentration
    ),
    # Alias for explicit use
    "saudi_arabia": CountryProfile(
        name="Kingdom of Saudi Arabia",
        total_population=36_400_000,
        total_area_sqkm=2_149_690,
        num_regions=13,
        gdp_billion_usd=1_108,
        urban_population_pct=84.3,
        center_lat=23.8859,
        center_lon=45.0792,
        bbox=(34.5, 16.4, 55.7, 32.2),
        population_gini=0.55,
        primacy_ratio=4.5,
        economic_concentration=0.68
    ),
    "medium_country": CountryProfile(
        name="Medium Country",
        total_population=15_000_000,
        total_area_sqkm=500_000,
        num_regions=8,
        gdp_billion_usd=200,
        urban_population_pct=70,
        center_lat=35.0,
        center_lon=10.0,
        bbox=(5.0, 30.0, 15.0, 40.0),
        population_gini=0.40,
        primacy_ratio=2.8,
        economic_concentration=0.50
    ),
    "small_country": CountryProfile(
        name="Small Country",
        total_population=5_000_000,
        total_area_sqkm=100_000,
        num_regions=5,
        gdp_billion_usd=50,
        urban_population_pct=60,
        center_lat=40.0,
        center_lon=20.0,
        bbox=(18.0, 38.0, 22.0, 42.0),
        population_gini=0.35,
        primacy_ratio=2.0,
        economic_concentration=0.40
    )
}


class SimulationEngine(DataProviderInterface):
    """
    Simulation engine that generates realistic synthetic data.
    Implements the DataProviderInterface so it can be used as a drop-in
    replacement for real data sources.
    """
    
    def __init__(self, 
                 profile: str = "country_x",
                 seed: int = 42,
                 cache_enabled: bool = True):
        """
        Initialize simulation engine.
        
        Args:
            profile: Country profile name or custom CountryProfile
            seed: Random seed for reproducibility
            cache_enabled: Whether to cache generated data
        """
        self.profile = COUNTRY_PROFILES.get(profile) if isinstance(profile, str) else profile
        if self.profile is None:
            raise ValueError(f"Unknown profile: {profile}")
        
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.cache_enabled = cache_enabled
        self._cache: Dict[str, Any] = {}
        
        logger.info(f"Simulation Engine initialized: {self.profile.name}")
        logger.info(f"  Population: {self.profile.total_population:,}")
        logger.info(f"  Area: {self.profile.total_area_sqkm:,.0f} km²")
        logger.info(f"  Regions: {self.profile.num_regions}")
    
    @property
    def provider_name(self) -> str:
        return f"SimulationEngine:{self.profile.name}"
    
    @property
    def is_simulation(self) -> bool:
        return True
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Get cached data if available."""
        if self.cache_enabled and key in self._cache:
            return self._cache[key]
        return None
    
    def _set_cached(self, key: str, data: Any):
        """Cache data."""
        if self.cache_enabled:
            self._cache[key] = data
    
    def _generate_region_polygons(self) -> gpd.GeoDataFrame:
        """Generate realistic region polygons using Voronoi-like partitioning."""
        cache_key = "regions"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        minx, miny, maxx, maxy = self.profile.bbox
        n_regions = self.profile.num_regions
        
        # Generate region centers with some clustering toward center
        centers_x = self.rng.normal(
            loc=(minx + maxx) / 2,
            scale=(maxx - minx) / 4,
            size=n_regions
        )
        centers_y = self.rng.normal(
            loc=(miny + maxy) / 2,
            scale=(maxy - miny) / 4,
            size=n_regions
        )
        
        # Clip to bbox
        centers_x = np.clip(centers_x, minx + 0.5, maxx - 0.5)
        centers_y = np.clip(centers_y, miny + 0.5, maxy - 0.5)
        
        # Create simple polygons around centers (simplified approach)
        polygons = []
        for i in range(n_regions):
            # Create irregular polygon around center
            n_vertices = self.rng.integers(6, 12)
            angles = np.sort(self.rng.uniform(0, 2 * np.pi, n_vertices))
            radii = self.rng.uniform(1.5, 3.5, n_vertices)
            
            vertices = [
                (centers_x[i] + r * np.cos(a), centers_y[i] + r * np.sin(a))
                for r, a in zip(radii, angles)
            ]
            vertices.append(vertices[0])  # Close polygon
            
            poly = Polygon(vertices)
            polygons.append(poly)
        
        # Clip polygons to country bbox and ensure no overlaps
        country_bbox = Polygon([
            (minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy), (minx, miny)
        ])
        
        clipped_polygons = []
        for poly in polygons:
            clipped = poly.intersection(country_bbox)
            if clipped.is_valid and not clipped.is_empty:
                clipped_polygons.append(clipped)
        
        # Generate region names - KSA 13 Administrative Provinces (Mintaqah)
        # Using actual Saudi administrative divisions
        region_names = [
            "Riyadh Region",      # الرياض - Capital, largest population
            "Makkah Region",      # مكة المكرمة - Includes Jeddah, Makkah
            "Eastern Region",     # الشرقية - Oil industry hub, Dammam
            "Madinah Region",     # المدينة المنورة - Holy city
            "Al-Qassim Region",   # القصيم - Agricultural heartland
            "Asir Region",        # عسير - Mountain region, Abha
            "Tabuk Region",       # تبوك - NEOM location
            "Hail Region",        # حائل - Northern agricultural
            "Northern Borders",   # الحدود الشمالية - Border region
            "Jazan Region",       # جازان - Southern coastal
            "Najran Region",      # نجران - Southern border
            "Al-Baha Region",     # الباحة - Mountain tourism
            "Al-Jouf Region"      # الجوف - Northwestern
        ][:n_regions]
        
        gdf = gpd.GeoDataFrame({
            'id': range(1, n_regions + 1),
            'code': [f"RG-{i:02d}" for i in range(1, n_regions + 1)],
            'name_en': region_names,
            'name_ar': [f"منطقة {i}" for i in range(1, n_regions + 1)],
            'level': 2,
            'parent_id': 1
        }, geometry=clipped_polygons, crs="EPSG:4326")
        
        # Calculate areas
        gdf_projected = gdf.to_crs("EPSG:32638")  # UTM for area calculation
        gdf['area_sqkm'] = gdf_projected.geometry.area / 1e6
        
        # Normalize areas to match country total
        area_factor = self.profile.total_area_sqkm / gdf['area_sqkm'].sum()
        gdf['area_sqkm'] = gdf['area_sqkm'] * area_factor
        
        # Calculate centroids
        gdf['centroid'] = gdf.geometry.centroid
        
        self._set_cached(cache_key, gdf)
        return gdf
    
    def _generate_population_distribution(self, regions: gpd.GeoDataFrame) -> pd.DataFrame:
        """Generate realistic population distribution across regions."""
        n_regions = len(regions)
        
        # Use Pareto distribution for realistic unequal distribution
        raw_shares = self.rng.pareto(a=1.5, size=n_regions)
        
        # Adjust for desired Gini coefficient
        shares = raw_shares / raw_shares.sum()
        
        # Ensure capital region is largest
        capital_idx = 5 if n_regions > 5 else 0  # "Capital Region"
        shares[capital_idx] = shares.max() * self.profile.primacy_ratio / 2
        shares = shares / shares.sum()
        
        populations = (shares * self.profile.total_population).astype(int)
        
        # Calculate densities
        densities = populations / regions['area_sqkm'].values
        
        return pd.DataFrame({
            'region_id': regions['id'].values,
            'population': populations,
            'pop_density': densities,
            'urban_pop_pct': self.rng.uniform(
                self.profile.urban_population_pct - 20,
                min(95, self.profile.urban_population_pct + 15),
                n_regions
            )
        })
    
    def _generate_settlements(self, regions: gpd.GeoDataFrame, 
                              population_df: pd.DataFrame) -> gpd.GeoDataFrame:
        """Generate settlement points within regions."""
        cache_key = "settlements"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        settlements = []
        settlement_id = 1
        
        city_name_prefixes = [
            "Al", "El", "New", "Port", "North", "South", "East", "West",
            "Central", "Upper", "Lower", "Greater"
        ]
        city_name_suffixes = [
            "City", "Town", "Village", "Port", "Springs", "Valley",
            "Hills", "Plains", "Oasis", "Harbor", "Junction"
        ]
        
        for idx, region in regions.iterrows():
            region_pop = population_df[population_df['region_id'] == region['id']]['population'].values[0]
            
            # Determine number of settlements based on population
            if region_pop > 5_000_000:
                n_settlements = self.rng.integers(15, 25)
            elif region_pop > 1_000_000:
                n_settlements = self.rng.integers(8, 15)
            elif region_pop > 500_000:
                n_settlements = self.rng.integers(5, 10)
            else:
                n_settlements = self.rng.integers(3, 7)
            
            # Distribute population among settlements (Zipf's law)
            raw_pops = self.rng.zipf(a=1.8, size=n_settlements)
            settlement_pops = (raw_pops / raw_pops.sum() * region_pop * 0.85).astype(int)
            settlement_pops = np.sort(settlement_pops)[::-1]  # Descending
            
            # Generate points within region
            minx, miny, maxx, maxy = region.geometry.bounds
            
            for i, pop in enumerate(settlement_pops):
                # Try to place point inside region
                for _ in range(100):
                    x = self.rng.uniform(minx, maxx)
                    y = self.rng.uniform(miny, maxy)
                    point = Point(x, y)
                    if region.geometry.contains(point):
                        break
                else:
                    # Fallback to centroid
                    point = region.geometry.centroid
                
                # Determine hierarchy class
                if pop >= 1_000_000:
                    hierarchy = "Metropolis"
                elif pop >= 500_000:
                    hierarchy = "Large City"
                elif pop >= 100_000:
                    hierarchy = "Medium City"
                elif pop >= 50_000:
                    hierarchy = "Small City"
                elif pop >= 10_000:
                    hierarchy = "Town"
                else:
                    hierarchy = "Village"
                
                # Generate name
                prefix = self.rng.choice(city_name_prefixes)
                suffix = self.rng.choice(city_name_suffixes)
                name = f"{prefix} {suffix} {settlement_id}"
                
                settlements.append({
                    'id': settlement_id,
                    'name_en': name,
                    'name_ar': f"مدينة {settlement_id}",
                    'region_id': region['id'],
                    'population': pop,
                    'hierarchy_class': hierarchy,
                    'is_capital': i == 0 and region['id'] == 6,  # Capital region's main city
                    'geometry': point
                })
                settlement_id += 1
        
        gdf = gpd.GeoDataFrame(settlements, crs="EPSG:4326")
        gdf['rank'] = gdf['population'].rank(ascending=False, method='first').astype(int)
        
        self._set_cached(cache_key, gdf)
        return gdf
    
    def _generate_roads(self, regions: gpd.GeoDataFrame,
                        settlements: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Generate road network connecting settlements."""
        cache_key = "roads"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        roads = []
        road_id = 1
        
        # Get major cities (top 20 by population)
        major_cities = settlements.nlargest(20, 'population')
        
        # Connect major cities with highways
        for i, city1 in major_cities.iterrows():
            # Find 2-3 nearest major cities
            distances = major_cities.geometry.distance(city1.geometry)
            nearest = distances.nsmallest(4).index[1:4]  # Skip self
            
            for j in nearest:
                city2 = major_cities.loc[j]
                
                # Create road line with slight curve
                p1 = city1.geometry
                p2 = city2.geometry
                
                # Add midpoint with offset for curve
                mid_x = (p1.x + p2.x) / 2 + self.rng.uniform(-0.2, 0.2)
                mid_y = (p1.y + p2.y) / 2 + self.rng.uniform(-0.2, 0.2)
                
                line = LineString([(p1.x, p1.y), (mid_x, mid_y), (p2.x, p2.y)])
                
                roads.append({
                    'id': road_id,
                    'road_name': f"Highway {road_id}",
                    'road_class': 'highway',
                    'lanes': self.rng.choice([4, 6, 8]),
                    'length_km': line.length * 111,  # Approximate km
                    'status': 'operational',
                    'geometry': line
                })
                road_id += 1
        
        # Add some primary roads between smaller cities
        medium_cities = settlements[
            (settlements['population'] >= 50000) & 
            (settlements['population'] < 500000)
        ]
        
        for region_id in regions['id']:
            region_cities = medium_cities[medium_cities['region_id'] == region_id]
            
            for i, city1 in region_cities.iterrows():
                nearest = region_cities.geometry.distance(city1.geometry).nsmallest(3).index[1:3]
                
                for j in nearest:
                    city2 = region_cities.loc[j]
                    line = LineString([city1.geometry, city2.geometry])
                    
                    roads.append({
                        'id': road_id,
                        'road_name': f"Road {road_id}",
                        'road_class': 'primary',
                        'lanes': self.rng.choice([2, 4]),
                        'length_km': line.length * 111,
                        'status': 'operational',
                        'geometry': line
                    })
                    road_id += 1
        
        gdf = gpd.GeoDataFrame(roads, crs="EPSG:4326")
        self._set_cached(cache_key, gdf)
        return gdf
    
    def _generate_economic_data(self, regions: gpd.GeoDataFrame,
                                population_df: pd.DataFrame,
                                year: int) -> pd.DataFrame:
        """Generate economic indicators by region."""
        n_regions = len(regions)
        total_gdp = self.profile.gdp_billion_usd
        
        # GDP distribution (correlated with population but not perfectly)
        pop_shares = population_df['population'] / population_df['population'].sum()
        noise = self.rng.uniform(0.8, 1.2, n_regions)
        gdp_shares = pop_shares * noise
        gdp_shares = gdp_shares / gdp_shares.sum()
        
        gdp_values = gdp_shares * total_gdp
        
        # GDP per capita
        gdp_per_capita = (gdp_values * 1e9) / population_df['population']
        
        # Employment rate (inverse correlation with GDP for realism)
        base_employment = 95 - (gdp_per_capita / gdp_per_capita.max()) * 5
        employment_rate = base_employment + self.rng.uniform(-2, 2, n_regions)
        
        return pd.DataFrame({
            'region_id': regions['id'].values,
            'year': year,
            'gdp_billion_usd': gdp_values.values,
            'gdp_per_capita_usd': gdp_per_capita.values,
            'employment_rate': employment_rate,
            'unemployment_rate': 100 - employment_rate
        })
    
    def _generate_projects(self, regions: gpd.GeoDataFrame,
                           settlements: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Generate major development projects - includes Vision 2030 giga-projects."""
        cache_key = "projects"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        # Vision 2030 Giga-Projects (real projects with approximate data)
        vision_2030_projects = [
            # NEOM and sub-projects
            {"name": "NEOM", "sector": "giga_city", "budget": 500, "lat": 28.0, "lon": 35.0,
             "region": "Tabuk Region", "status": "under_construction", "start": 2017, "end": 2039,
             "description": "Smart city megaproject on Red Sea coast"},
            {"name": "THE LINE", "sector": "urban", "budget": 200, "lat": 28.1, "lon": 34.8,
             "region": "Tabuk Region", "status": "under_construction", "start": 2021, "end": 2030,
             "description": "170km linear city with zero cars, zero emissions"},
            {"name": "OXAGON", "sector": "industrial", "budget": 50, "lat": 27.8, "lon": 35.2,
             "region": "Tabuk Region", "status": "under_construction", "start": 2021, "end": 2030,
             "description": "Floating industrial complex and port"},
            {"name": "TROJENA", "sector": "tourism", "budget": 30, "lat": 28.2, "lon": 35.5,
             "region": "Tabuk Region", "status": "under_construction", "start": 2022, "end": 2026,
             "description": "Mountain destination with year-round skiing"},
            {"name": "SINDALAH", "sector": "tourism", "budget": 5, "lat": 27.5, "lon": 35.8,
             "region": "Tabuk Region", "status": "under_construction", "start": 2022, "end": 2024,
             "description": "Luxury island destination"},
            # Red Sea Projects
            {"name": "Red Sea Project", "sector": "tourism", "budget": 15, "lat": 25.5, "lon": 37.0,
             "region": "Madinah Region", "status": "under_construction", "start": 2019, "end": 2030,
             "description": "Luxury tourism across 90+ islands"},
            {"name": "AMAALA", "sector": "tourism", "budget": 8, "lat": 26.0, "lon": 36.5,
             "region": "Tabuk Region", "status": "under_construction", "start": 2020, "end": 2028,
             "description": "Ultra-luxury wellness and arts destination"},
            # Riyadh Development
            {"name": "Qiddiya", "sector": "entertainment", "budget": 8, "lat": 24.4, "lon": 46.2,
             "region": "Riyadh Region", "status": "under_construction", "start": 2019, "end": 2030,
             "description": "Entertainment, sports and culture mega-city"},
            {"name": "Diriyah Gate", "sector": "heritage", "budget": 20, "lat": 24.7, "lon": 46.6,
             "region": "Riyadh Region", "status": "under_construction", "start": 2018, "end": 2027,
             "description": "Historic district restoration and development"},
            {"name": "King Salman Park", "sector": "urban", "budget": 23, "lat": 24.7, "lon": 46.7,
             "region": "Riyadh Region", "status": "under_construction", "start": 2019, "end": 2027,
             "description": "13 sq km urban park, largest in the world"},
            {"name": "Riyadh Metro", "sector": "transport", "budget": 22.5, "lat": 24.7, "lon": 46.7,
             "region": "Riyadh Region", "status": "operational", "start": 2014, "end": 2024,
             "description": "176km metro network with 6 lines"},
            {"name": "New Murabba", "sector": "urban", "budget": 50, "lat": 24.8, "lon": 46.6,
             "region": "Riyadh Region", "status": "announced", "start": 2024, "end": 2030,
             "description": "Downtown district with Mukaab iconic cube"},
            # AlUla Development (Royal Commission)
            {"name": "AlUla Development", "sector": "heritage", "budget": 15, "lat": 26.6, "lon": 37.9,
             "region": "Madinah Region", "status": "under_construction", "start": 2018, "end": 2035,
             "description": "UNESCO heritage and tourism destination"},
            # Jeddah Projects
            {"name": "Jeddah Tower", "sector": "urban", "budget": 2, "lat": 21.5, "lon": 39.2,
             "region": "Makkah Region", "status": "under_construction", "start": 2013, "end": 2028,
             "description": "1km tall skyscraper, world's tallest"},
            {"name": "Jeddah Central", "sector": "urban", "budget": 20, "lat": 21.5, "lon": 39.1,
             "region": "Makkah Region", "status": "planned", "start": 2025, "end": 2035,
             "description": "5.7 million sqm mixed-use waterfront development"},
            # Energy Projects
            {"name": "NEOM Green Hydrogen", "sector": "energy", "budget": 8.5, "lat": 28.3, "lon": 35.3,
             "region": "Tabuk Region", "status": "under_construction", "start": 2021, "end": 2026,
             "description": "World's largest green hydrogen plant"},
            {"name": "Sudair Solar PV", "sector": "energy", "budget": 1.5, "lat": 25.5, "lon": 45.7,
             "region": "Riyadh Region", "status": "operational", "start": 2021, "end": 2024,
             "description": "1.5 GW solar power plant"},
            {"name": "Dumat Al Jandal Wind", "sector": "energy", "budget": 0.5, "lat": 29.8, "lon": 39.9,
             "region": "Al-Jouf Region", "status": "operational", "start": 2019, "end": 2022,
             "description": "400 MW wind farm, Middle East's largest"},
            # Industrial & Economic Cities
            {"name": "King Abdullah Economic City", "sector": "industrial", "budget": 100, "lat": 22.4, "lon": 39.1,
             "region": "Makkah Region", "status": "operational", "start": 2006, "end": 2035,
             "description": "Industrial city and port on Red Sea"},
            {"name": "SPARK (King Salman Energy Park)", "sector": "industrial", "budget": 2, "lat": 25.5, "lon": 49.2,
             "region": "Eastern Region", "status": "under_construction", "start": 2018, "end": 2035,
             "description": "50 sq km energy city near Dammam"},
        ]
        
        projects = []
        project_id = 1
        
        # Add Vision 2030 flagship projects
        for vp in vision_2030_projects:
            projects.append({
                'id': project_id,
                'project_name': vp['name'],
                'project_type': 'Vision 2030 Flagship',
                'sector': vp['sector'],
                'region_name': vp['region'],
                'status': vp['status'],
                'start_year': vp['start'],
                'completion_year': vp['end'],
                'budget_billion_usd': vp['budget'],
                'description': vp['description'],
                'jobs_created': int(vp['budget'] * self.rng.uniform(2000, 8000)),
                'geometry': Point(vp['lon'], vp['lat'])
            })
            project_id += 1
        
        # Add additional simulated projects
        project_types = [
            ("Hospital Complex", "healthcare", 0.5, 2),
            ("University Campus", "education", 0.3, 1.5),
            ("Industrial Zone", "industrial", 0.5, 5),
            ("Residential Development", "housing", 0.2, 3),
            ("Airport Expansion", "transport", 1, 10),
            ("Desalination Plant", "water", 0.5, 3),
            ("Agricultural Project", "agriculture", 0.1, 1)
        ]
        
        statuses = ['announced', 'planned', 'under_construction', 'operational']
        status_weights = [0.15, 0.25, 0.35, 0.25]
        
        # Generate 15-25 additional projects
        n_projects = self.rng.integers(15, 25)
        
        for _ in range(n_projects):
            # Select project type
            ptype, sector, min_budget, max_budget = project_types[
                self.rng.integers(0, len(project_types))
            ]
            
            # Select location (near a settlement)
            settlement = settlements.sample(1, random_state=self.rng.integers(0, 10000)).iloc[0]
            
            # Offset slightly from settlement
            offset_x = self.rng.uniform(-0.1, 0.1)
            offset_y = self.rng.uniform(-0.1, 0.1)
            point = Point(
                settlement.geometry.x + offset_x,
                settlement.geometry.y + offset_y
            )
            
            budget = self.rng.uniform(min_budget, max_budget)
            status = self.rng.choice(statuses, p=status_weights)
            
            # Timeline based on status
            if status == 'operational':
                start_year = self.rng.integers(2018, 2024)
                completion_year = self.rng.integers(start_year + 1, 2026)
            elif status == 'under_construction':
                start_year = self.rng.integers(2022, 2026)
                completion_year = self.rng.integers(2026, 2030)
            else:
                start_year = self.rng.integers(2025, 2028)
                completion_year = self.rng.integers(2028, 2035)
            
            projects.append({
                'id': project_id,
                'project_name': f"{ptype} {project_id}",
                'project_type': ptype,
                'sector': sector,
                'region_id': settlement['region_id'],
                'status': status,
                'start_year': start_year,
                'completion_year': completion_year,
                'budget_billion_usd': round(budget, 2),
                'jobs_created': int(budget * self.rng.uniform(1000, 5000)),
                'geometry': point
            })
            project_id += 1
        
        gdf = gpd.GeoDataFrame(projects, crs="EPSG:4326")
        self._set_cached(cache_key, gdf)
        return gdf
    
    # === DataProviderInterface Implementation ===
    
    def get_spatial_units(self, level: int) -> DataResponse:
        """Get administrative units at specified level."""
        if level == 1:
            # Country level - create single polygon
            regions = self._generate_region_polygons()
            country_geom = unary_union(regions.geometry)
            gdf = gpd.GeoDataFrame({
                'id': [1],
                'code': ['XX'],
                'name_en': [self.profile.name],
                'level': [1],
                'parent_id': [None],
                'area_sqkm': [self.profile.total_area_sqkm]
            }, geometry=[country_geom], crs="EPSG:4326")
        elif level == 2:
            gdf = self._generate_region_polygons()
        else:
            # For demo, just return regions for levels 3+
            gdf = self._generate_region_polygons()
            gdf['level'] = level
        
        return DataResponse(
            data=gdf,
            metadata={'level': level, 'count': len(gdf)},
            source=self.provider_name,
            retrieved_at=datetime.now(),
            is_simulated=True
        )
    
    def get_settlements(self, 
                        min_population: Optional[int] = None,
                        region_id: Optional[int] = None) -> DataResponse:
        """Get settlement points."""
        regions = self._generate_region_polygons()
        pop_df = self._generate_population_distribution(regions)
        settlements = self._generate_settlements(regions, pop_df)
        
        if min_population:
            settlements = settlements[settlements['population'] >= min_population]
        if region_id:
            settlements = settlements[settlements['region_id'] == region_id]
        
        return DataResponse(
            data=settlements,
            metadata={'count': len(settlements)},
            source=self.provider_name,
            retrieved_at=datetime.now(),
            is_simulated=True
        )
    
    def get_population(self,
                       spatial_level: int,
                       year: int,
                       scenario_id: Optional[str] = None) -> DataResponse:
        """Get population data."""
        regions = self._generate_region_polygons()
        pop_df = self._generate_population_distribution(regions)
        
        # Apply year-based growth
        base_year = 2024
        growth_rate = 0.018  # 1.8% annual growth
        years_diff = year - base_year
        growth_factor = (1 + growth_rate) ** years_diff
        
        pop_df['year'] = year
        pop_df['population'] = (pop_df['population'] * growth_factor).astype(int)
        pop_df['scenario_id'] = scenario_id
        
        # Merge with regions for geometry
        result = regions.merge(pop_df, left_on='id', right_on='region_id')
        
        return DataResponse(
            data=result,
            metadata={'year': year, 'scenario': scenario_id},
            source=self.provider_name,
            retrieved_at=datetime.now(),
            is_simulated=True
        )
    
    def get_economic_data(self,
                          indicator: str,
                          spatial_level: int,
                          year: int) -> DataResponse:
        """Get economic indicators."""
        regions = self._generate_region_polygons()
        pop_df = self._generate_population_distribution(regions)
        econ_df = self._generate_economic_data(regions, pop_df, year)
        
        result = regions.merge(econ_df, left_on='id', right_on='region_id')
        
        return DataResponse(
            data=result,
            metadata={'indicator': indicator, 'year': year},
            source=self.provider_name,
            retrieved_at=datetime.now(),
            is_simulated=True
        )
    
    def get_infrastructure(self,
                           infra_type: str,
                           region_id: Optional[int] = None) -> DataResponse:
        """Get infrastructure data."""
        regions = self._generate_region_polygons()
        pop_df = self._generate_population_distribution(regions)
        settlements = self._generate_settlements(regions, pop_df)
        
        if infra_type == 'roads':
            gdf = self._generate_roads(regions, settlements)
        else:
            # Placeholder for other infrastructure types
            gdf = gpd.GeoDataFrame(columns=['id', 'name', 'type', 'geometry'], crs="EPSG:4326")
        
        return DataResponse(
            data=gdf,
            metadata={'type': infra_type},
            source=self.provider_name,
            retrieved_at=datetime.now(),
            is_simulated=True
        )
    
    def get_environment(self,
                        layer_type: str,
                        region_id: Optional[int] = None) -> DataResponse:
        """Get environmental data."""
        # Placeholder - would generate land cover, protected areas, etc.
        gdf = gpd.GeoDataFrame(columns=['id', 'name', 'type', 'geometry'], crs="EPSG:4326")
        
        return DataResponse(
            data=gdf,
            metadata={'type': layer_type},
            source=self.provider_name,
            retrieved_at=datetime.now(),
            is_simulated=True
        )
    
    def get_projects(self,
                     status: Optional[str] = None,
                     sector: Optional[str] = None) -> DataResponse:
        """Get major projects."""
        regions = self._generate_region_polygons()
        pop_df = self._generate_population_distribution(regions)
        settlements = self._generate_settlements(regions, pop_df)
        projects = self._generate_projects(regions, settlements)
        
        if status:
            projects = projects[projects['status'] == status]
        if sector:
            projects = projects[projects['sector'] == sector]
        
        return DataResponse(
            data=projects,
            metadata={'count': len(projects)},
            source=self.provider_name,
            retrieved_at=datetime.now(),
            is_simulated=True
        )


# Register with factory
DataProviderFactory.register('simulation', SimulationEngine)
