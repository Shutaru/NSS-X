"""
NSS X - WS1 Data Generator
Generates comprehensive datasets for National Spatial Strategy.
Uses real data where available, simulation engine for gaps.
"""

import pandas as pd
import numpy as np
import geopandas as gpd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from loguru import logger
import json

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "01_data"
RAW_DIR = DATA_DIR / "01_raw"
PROCESSED_DIR = DATA_DIR / "processed"
STATS_DIR = RAW_DIR / "statistics"


class WS1DataGenerator:
    """
    WS1 - Comprehensive Data Generator for NSS.
    Combines real data with realistic simulated data.
    """
    
    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)
        self.base_year = 2024
        
        # Load real data where available
        self._load_real_data()
        
        logger.info("WS1 Data Generator initialized")
    
    def _load_real_data(self):
        """Load available real data."""
        try:
            self.regions_real = pd.read_csv(STATS_DIR / "ksa_population_by_region.csv")
            self.cities_real = pd.read_csv(STATS_DIR / "ksa_major_cities.csv")
            self.economic_real = pd.read_csv(STATS_DIR / "ksa_economic_indicators.csv")
            self.employment_real = pd.read_csv(STATS_DIR / "ksa_employment_by_region.csv")
            self.projects_real = pd.read_csv(STATS_DIR / "ksa_vision2030_projects.csv")
            self.water_real = pd.read_csv(STATS_DIR / "ksa_water_consumption.csv")
            logger.info("Loaded real KSA data from statistics/")
        except Exception as e:
            logger.warning(f"Could not load some real data: {e}")
            self.regions_real = None
    
    # =========================================================================
    # 1. DEMOGRAPHIC DATA
    # =========================================================================
    
    def generate_demographic_detailed(self) -> Dict[str, pd.DataFrame]:
        """Generate detailed demographic data by region."""
        
        if self.regions_real is None:
            raise ValueError("Real regional data not loaded")
        
        # Age distribution (based on KSA demographics - young population)
        age_groups = ['0-4', '5-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65+']
        # KSA has very young population - 63% under 30
        national_age_dist = [0.08, 0.15, 0.18, 0.22, 0.16, 0.11, 0.06, 0.04]
        
        demographics = []
        
        for _, region in self.regions_real.iterrows():
            total_pop = region['population_2024']
            region_name = region['region_name_en']
            
            # Vary age distribution slightly by region
            # Urban regions (Riyadh, Eastern, Makkah) have more working-age
            if region_name in ['Riyadh', 'Eastern Province', 'Makkah']:
                age_dist = [d * self.rng.uniform(0.9, 1.1) for d in national_age_dist]
                age_dist[3] *= 1.15  # More 25-34 (workers)
                age_dist[4] *= 1.1   # More 35-44
            else:
                age_dist = [d * self.rng.uniform(0.95, 1.05) for d in national_age_dist]
            
            # Normalize
            age_dist = np.array(age_dist) / sum(age_dist)
            
            # Gender split (KSA has more males due to expat workers)
            male_ratio = 0.57 if region_name in ['Riyadh', 'Eastern Province'] else 0.54
            
            for i, age_group in enumerate(age_groups):
                age_pop = int(total_pop * age_dist[i])
                male_pop = int(age_pop * male_ratio)
                female_pop = age_pop - male_pop
                
                demographics.append({
                    'region_code': region['region_code'],
                    'region_name_en': region_name,
                    'age_group': age_group,
                    'total': age_pop,
                    'male': male_pop,
                    'female': female_pop,
                    'year': 2024
                })
        
        # Create time series
        demographics_ts = []
        for year in range(2010, 2051):
            growth_factor = self._get_population_growth_factor(year)
            for demo in demographics:
                demographics_ts.append({
                    **demo,
                    'year': year,
                    'total': int(demo['total'] * growth_factor),
                    'male': int(demo['male'] * growth_factor),
                    'female': int(demo['female'] * growth_factor),
                })
        
        # Urban/Rural split by region
        urban_rural = []
        urbanization_rates = {
            'Riyadh': 0.96, 'Makkah': 0.92, 'Eastern Province': 0.89,
            'Madinah': 0.85, 'Al-Qassim': 0.78, 'Asir': 0.65,
            'Tabuk': 0.72, 'Hail': 0.68, 'Northern Borders': 0.70,
            'Jazan': 0.55, 'Najran': 0.62, 'Al-Baha': 0.58, 'Al-Jouf': 0.70
        }
        
        for _, region in self.regions_real.iterrows():
            urban_rate = urbanization_rates.get(region['region_name_en'], 0.70)
            total_pop = region['population_2024']
            
            urban_rural.append({
                'region_code': region['region_code'],
                'region_name_en': region['region_name_en'],
                'total_population': total_pop,
                'urban_population': int(total_pop * urban_rate),
                'rural_population': int(total_pop * (1 - urban_rate)),
                'urbanization_rate': urban_rate * 100,
                'year': 2024
            })
        
        # Saudi vs Expat by region
        nationality = []
        saudi_ratios = {
            'Riyadh': 0.58, 'Makkah': 0.55, 'Eastern Province': 0.52,
            'Madinah': 0.65, 'Al-Qassim': 0.75, 'Asir': 0.82,
            'Tabuk': 0.70, 'Hail': 0.78, 'Northern Borders': 0.72,
            'Jazan': 0.85, 'Najran': 0.78, 'Al-Baha': 0.88, 'Al-Jouf': 0.75
        }
        
        for _, region in self.regions_real.iterrows():
            saudi_ratio = saudi_ratios.get(region['region_name_en'], 0.66)
            total_pop = region['population_2024']
            
            nationality.append({
                'region_code': region['region_code'],
                'region_name_en': region['region_name_en'],
                'total_population': total_pop,
                'saudi_population': int(total_pop * saudi_ratio),
                'expat_population': int(total_pop * (1 - saudi_ratio)),
                'saudi_ratio': saudi_ratio * 100,
                'year': 2024
            })
        
        return {
            'age_distribution': pd.DataFrame(demographics),
            'age_distribution_timeseries': pd.DataFrame(demographics_ts),
            'urban_rural': pd.DataFrame(urban_rural),
            'nationality': pd.DataFrame(nationality)
        }
    
    def _get_population_growth_factor(self, year: int) -> float:
        """Get population growth factor relative to 2024."""
        base_year = 2024
        if year < base_year:
            # Historical - average 2.5% growth
            years_diff = base_year - year
            return 1 / (1.025 ** years_diff)
        else:
            # Future - declining growth rate
            years_diff = year - base_year
            if years_diff <= 6:  # 2024-2030
                rate = 0.022
            elif years_diff <= 16:  # 2030-2040
                rate = 0.018
            else:  # 2040-2050
                rate = 0.012
            return (1 + rate) ** years_diff
    
    # =========================================================================
    # 2. ECONOMIC DATA
    # =========================================================================
    
    def generate_economic_detailed(self) -> Dict[str, pd.DataFrame]:
        """Generate detailed economic data by region and sector."""
        
        # National GDP breakdown by sector (2024 estimates)
        sectors = {
            'Oil & Gas': {'gdp_share': 0.38, 'employment_share': 0.035, 'growth': 0.02},
            'Manufacturing': {'gdp_share': 0.13, 'employment_share': 0.085, 'growth': 0.05},
            'Wholesale & Retail': {'gdp_share': 0.10, 'employment_share': 0.18, 'growth': 0.04},
            'Construction': {'gdp_share': 0.06, 'employment_share': 0.12, 'growth': 0.06},
            'Real Estate': {'gdp_share': 0.075, 'employment_share': 0.02, 'growth': 0.04},
            'Transport & Storage': {'gdp_share': 0.06, 'employment_share': 0.07, 'growth': 0.05},
            'Finance & Insurance': {'gdp_share': 0.05, 'employment_share': 0.03, 'growth': 0.06},
            'Tourism & Hospitality': {'gdp_share': 0.05, 'employment_share': 0.06, 'growth': 0.12},
            'ICT': {'gdp_share': 0.04, 'employment_share': 0.025, 'growth': 0.15},
            'Agriculture': {'gdp_share': 0.025, 'employment_share': 0.065, 'growth': 0.02},
            'Mining (non-oil)': {'gdp_share': 0.035, 'employment_share': 0.015, 'growth': 0.10},
            'Public Admin': {'gdp_share': 0.08, 'employment_share': 0.15, 'growth': 0.02},
            'Other Services': {'gdp_share': 0.045, 'employment_share': 0.08, 'growth': 0.04}
        }
        
        total_gdp_billion_sar = 4700  # 2024
        total_gdp_billion_usd = total_gdp_billion_sar / 3.75
        
        # Regional GDP distribution (based on economic activity)
        regional_gdp_shares = {
            'Riyadh': 0.30, 'Makkah': 0.22, 'Eastern Province': 0.28,
            'Madinah': 0.045, 'Al-Qassim': 0.035, 'Asir': 0.035,
            'Tabuk': 0.025, 'Hail': 0.015, 'Northern Borders': 0.01,
            'Jazan': 0.02, 'Najran': 0.01, 'Al-Baha': 0.008, 'Al-Jouf': 0.012
        }
        
        # Generate GDP by region and sector
        gdp_regional_sectoral = []
        
        for region_name, region_share in regional_gdp_shares.items():
            region_gdp = total_gdp_billion_usd * region_share
            
            # Sector mix varies by region
            sector_weights = self._get_regional_sector_weights(region_name)
            
            for sector_name, sector_info in sectors.items():
                weight = sector_weights.get(sector_name, sector_info['gdp_share'])
                sector_gdp = region_gdp * weight / sum(sector_weights.values())
                
                gdp_regional_sectoral.append({
                    'region_name_en': region_name,
                    'sector': sector_name,
                    'gdp_billion_usd': round(sector_gdp, 3),
                    'gdp_share_regional': round(weight / sum(sector_weights.values()) * 100, 2),
                    'year': 2024
                })
        
        # Time series GDP
        gdp_timeseries = []
        for year in range(2015, 2051):
            year_factor = self._get_gdp_factor(year)
            for entry in gdp_regional_sectoral:
                sector_growth = sectors[entry['sector']]['growth']
                if year > 2024:
                    sector_factor = (1 + sector_growth) ** (year - 2024)
                else:
                    sector_factor = 1 / ((1 + sector_growth) ** (2024 - year))
                
                gdp_timeseries.append({
                    **entry,
                    'year': year,
                    'gdp_billion_usd': round(entry['gdp_billion_usd'] * year_factor * sector_factor, 3)
                })
        
        # Investment by region
        investments = []
        total_investment = 200  # Billion USD annual
        
        for region_name, region_share in regional_gdp_shares.items():
            # Investment higher in development regions
            inv_multiplier = 1.5 if region_name in ['Tabuk', 'Riyadh'] else 1.0
            region_inv = total_investment * region_share * inv_multiplier
            
            investments.append({
                'region_name_en': region_name,
                'total_investment_billion_usd': round(region_inv, 2),
                'private_investment': round(region_inv * 0.6, 2),
                'public_investment': round(region_inv * 0.3, 2),
                'foreign_investment': round(region_inv * 0.1, 2),
                'year': 2024
            })
        
        return {
            'gdp_regional_sectoral': pd.DataFrame(gdp_regional_sectoral),
            'gdp_timeseries': pd.DataFrame(gdp_timeseries),
            'investments': pd.DataFrame(investments),
            'sectors': pd.DataFrame([
                {'sector': k, **v} for k, v in sectors.items()
            ])
        }
    
    def _get_regional_sector_weights(self, region: str) -> Dict[str, float]:
        """Get sector weights by region."""
        base = {
            'Oil & Gas': 0.38, 'Manufacturing': 0.13, 'Wholesale & Retail': 0.10,
            'Construction': 0.06, 'Real Estate': 0.075, 'Transport & Storage': 0.06,
            'Finance & Insurance': 0.05, 'Tourism & Hospitality': 0.05, 'ICT': 0.04,
            'Agriculture': 0.025, 'Mining (non-oil)': 0.035, 'Public Admin': 0.08,
            'Other Services': 0.045
        }
        
        # Regional specializations
        if region == 'Eastern Province':
            base['Oil & Gas'] = 0.55
            base['Manufacturing'] = 0.18
        elif region == 'Riyadh':
            base['Finance & Insurance'] = 0.12
            base['ICT'] = 0.08
            base['Public Admin'] = 0.15
            base['Oil & Gas'] = 0.15
        elif region == 'Makkah':
            base['Tourism & Hospitality'] = 0.15
            base['Wholesale & Retail'] = 0.15
            base['Oil & Gas'] = 0.10
        elif region == 'Madinah':
            base['Tourism & Hospitality'] = 0.12
        elif region == 'Al-Qassim':
            base['Agriculture'] = 0.12
        elif region == 'Asir':
            base['Agriculture'] = 0.08
            base['Tourism & Hospitality'] = 0.08
        elif region == 'Tabuk':
            base['Tourism & Hospitality'] = 0.10  # NEOM effect
            base['Construction'] = 0.15
        
        return base
    
    def _get_gdp_factor(self, year: int) -> float:
        """Get GDP growth factor relative to 2024."""
        if year < 2024:
            # Historical - varies by year
            gdp_history = {
                2015: 0.52, 2016: 0.52, 2017: 0.55, 2018: 0.63,
                2019: 0.63, 2020: 0.56, 2021: 0.66, 2022: 0.89,
                2023: 0.89, 2024: 1.0
            }
            return gdp_history.get(year, 0.5)
        else:
            # Future projections
            years = year - 2024
            if years <= 6:  # 2024-2030
                rate = 0.045
            elif years <= 16:  # 2030-2040
                rate = 0.035
            else:  # 2040-2050
                rate = 0.025
            return (1 + rate) ** years
    
    # =========================================================================
    # 3. ENVIRONMENTAL DATA
    # =========================================================================
    
    def generate_environmental_data(self) -> Dict[str, pd.DataFrame]:
        """Generate environmental data by region."""
        
        # Water resources
        water_data = []
        
        water_profiles = {
            'Riyadh': {'consumption_mcm': 2500, 'groundwater_pct': 40, 'desal_pct': 45, 'treated_pct': 15},
            'Makkah': {'consumption_mcm': 2200, 'groundwater_pct': 30, 'desal_pct': 55, 'treated_pct': 15},
            'Eastern Province': {'consumption_mcm': 1800, 'groundwater_pct': 45, 'desal_pct': 40, 'treated_pct': 15},
            'Madinah': {'consumption_mcm': 800, 'groundwater_pct': 35, 'desal_pct': 50, 'treated_pct': 15},
            'Al-Qassim': {'consumption_mcm': 1200, 'groundwater_pct': 85, 'desal_pct': 0, 'treated_pct': 15},
            'Asir': {'consumption_mcm': 600, 'groundwater_pct': 60, 'desal_pct': 20, 'treated_pct': 20},
            'Tabuk': {'consumption_mcm': 400, 'groundwater_pct': 70, 'desal_pct': 15, 'treated_pct': 15},
            'Hail': {'consumption_mcm': 350, 'groundwater_pct': 80, 'desal_pct': 5, 'treated_pct': 15},
            'Northern Borders': {'consumption_mcm': 150, 'groundwater_pct': 75, 'desal_pct': 10, 'treated_pct': 15},
            'Jazan': {'consumption_mcm': 450, 'groundwater_pct': 50, 'desal_pct': 35, 'treated_pct': 15},
            'Najran': {'consumption_mcm': 250, 'groundwater_pct': 80, 'desal_pct': 5, 'treated_pct': 15},
            'Al-Baha': {'consumption_mcm': 150, 'groundwater_pct': 70, 'desal_pct': 10, 'treated_pct': 20},
            'Al-Jouf': {'consumption_mcm': 300, 'groundwater_pct': 90, 'desal_pct': 0, 'treated_pct': 10}
        }
        
        for region, profile in water_profiles.items():
            water_data.append({
                'region_name_en': region,
                'total_consumption_mcm': profile['consumption_mcm'],
                'groundwater_mcm': int(profile['consumption_mcm'] * profile['groundwater_pct'] / 100),
                'desalination_mcm': int(profile['consumption_mcm'] * profile['desal_pct'] / 100),
                'treated_wastewater_mcm': int(profile['consumption_mcm'] * profile['treated_pct'] / 100),
                'agriculture_share_pct': 80 if region in ['Al-Qassim', 'Al-Jouf', 'Hail'] else 65,
                'municipal_share_pct': 20 if region in ['Al-Qassim', 'Al-Jouf', 'Hail'] else 30,
                'industrial_share_pct': 5,
                'aquifer_stress_level': 'Critical' if region in ['Al-Qassim', 'Riyadh', 'Al-Jouf'] else 'High',
                'year': 2024
            })
        
        # Climate data
        climate_data = []
        
        climate_profiles = {
            'Riyadh': {'avg_temp_c': 26.5, 'max_temp_c': 45, 'min_temp_c': 8, 'rainfall_mm': 100},
            'Makkah': {'avg_temp_c': 31, 'max_temp_c': 48, 'min_temp_c': 18, 'rainfall_mm': 111},
            'Eastern Province': {'avg_temp_c': 27, 'max_temp_c': 46, 'min_temp_c': 10, 'rainfall_mm': 90},
            'Madinah': {'avg_temp_c': 28, 'max_temp_c': 47, 'min_temp_c': 12, 'rainfall_mm': 62},
            'Al-Qassim': {'avg_temp_c': 25, 'max_temp_c': 44, 'min_temp_c': 5, 'rainfall_mm': 130},
            'Asir': {'avg_temp_c': 19, 'max_temp_c': 32, 'min_temp_c': 5, 'rainfall_mm': 350},
            'Tabuk': {'avg_temp_c': 22, 'max_temp_c': 40, 'min_temp_c': 2, 'rainfall_mm': 35},
            'Hail': {'avg_temp_c': 22, 'max_temp_c': 42, 'min_temp_c': 0, 'rainfall_mm': 100},
            'Northern Borders': {'avg_temp_c': 21, 'max_temp_c': 43, 'min_temp_c': -2, 'rainfall_mm': 70},
            'Jazan': {'avg_temp_c': 30, 'max_temp_c': 42, 'min_temp_c': 22, 'rainfall_mm': 130},
            'Najran': {'avg_temp_c': 24, 'max_temp_c': 40, 'min_temp_c': 8, 'rainfall_mm': 80},
            'Al-Baha': {'avg_temp_c': 20, 'max_temp_c': 34, 'min_temp_c': 6, 'rainfall_mm': 250},
            'Al-Jouf': {'avg_temp_c': 21, 'max_temp_c': 42, 'min_temp_c': -3, 'rainfall_mm': 55}
        }
        
        for region, profile in climate_profiles.items():
            climate_data.append({
                'region_name_en': region,
                **profile,
                'extreme_heat_days': int((profile['max_temp_c'] - 35) * 8),
                'drought_risk': 'High' if profile['rainfall_mm'] < 100 else 'Medium',
                'year': 2024
            })
        
        # Protected areas
        protected_areas = []
        
        protected_profiles = {
            'Tabuk': {'protected_pct': 8.5, 'marine_protected_km2': 500, 'key_site': 'NEOM Nature Reserve'},
            'Makkah': {'protected_pct': 3.2, 'marine_protected_km2': 200, 'key_site': 'Red Sea Coast'},
            'Madinah': {'protected_pct': 5.0, 'marine_protected_km2': 1500, 'key_site': 'Red Sea Project'},
            'Asir': {'protected_pct': 12.0, 'marine_protected_km2': 0, 'key_site': 'Asir National Park'},
            'Eastern Province': {'protected_pct': 2.5, 'marine_protected_km2': 100, 'key_site': 'Arabian Gulf Coast'},
            'Al-Baha': {'protected_pct': 6.0, 'marine_protected_km2': 0, 'key_site': 'Al-Baha Forest'},
            'Riyadh': {'protected_pct': 1.5, 'marine_protected_km2': 0, 'key_site': 'King Abdulaziz Royal Reserve'},
            'Najran': {'protected_pct': 3.0, 'marine_protected_km2': 0, 'key_site': None},
            'Jazan': {'protected_pct': 4.0, 'marine_protected_km2': 300, 'key_site': 'Farasan Islands'},
            'Al-Qassim': {'protected_pct': 1.0, 'marine_protected_km2': 0, 'key_site': None},
            'Hail': {'protected_pct': 2.0, 'marine_protected_km2': 0, 'key_site': None},
            'Northern Borders': {'protected_pct': 1.5, 'marine_protected_km2': 0, 'key_site': None},
            'Al-Jouf': {'protected_pct': 1.0, 'marine_protected_km2': 0, 'key_site': None}
        }
        
        for region, profile in protected_profiles.items():
            protected_areas.append({
                'region_name_en': region,
                'terrestrial_protected_pct': profile['protected_pct'],
                'marine_protected_km2': profile['marine_protected_km2'],
                'key_protected_site': profile['key_site'],
                'target_2030_pct': 30,  # Saudi Green Initiative target
                'year': 2024
            })
        
        # Air quality
        air_quality = []
        for region in climate_profiles.keys():
            # PM2.5 levels (higher in industrial/urban areas)
            if region in ['Riyadh', 'Eastern Province', 'Makkah']:
                pm25 = self.rng.uniform(45, 65)
            else:
                pm25 = self.rng.uniform(25, 45)
            
            air_quality.append({
                'region_name_en': region,
                'pm25_annual_avg': round(pm25, 1),
                'pm10_annual_avg': round(pm25 * 2.1, 1),
                'aqi_category': 'Moderate' if pm25 < 55 else 'Unhealthy for Sensitive',
                'main_pollution_source': 'Industry' if region == 'Eastern Province' else 'Traffic' if region in ['Riyadh', 'Makkah'] else 'Dust',
                'year': 2024
            })
        
        return {
            'water_resources': pd.DataFrame(water_data),
            'climate': pd.DataFrame(climate_data),
            'protected_areas': pd.DataFrame(protected_areas),
            'air_quality': pd.DataFrame(air_quality)
        }
    
    # =========================================================================
    # 4. INFRASTRUCTURE DATA
    # =========================================================================
    
    def generate_infrastructure_data(self) -> Dict[str, pd.DataFrame]:
        """Generate infrastructure data."""
        
        # Transport infrastructure
        transport = []
        
        transport_profiles = {
            'Riyadh': {
                'airports': 2, 'airport_capacity_mpax': 35,
                'rail_km': 176, 'metro_km': 176, 'highway_km': 4500,
                'bus_routes': 85
            },
            'Makkah': {
                'airports': 1, 'airport_capacity_mpax': 80,  # Jeddah
                'rail_km': 450, 'metro_km': 18, 'highway_km': 3800,
                'bus_routes': 65
            },
            'Eastern Province': {
                'airports': 3, 'airport_capacity_mpax': 15,
                'rail_km': 200, 'metro_km': 0, 'highway_km': 3200,
                'bus_routes': 45
            },
            'Madinah': {
                'airports': 1, 'airport_capacity_mpax': 12,
                'rail_km': 400, 'metro_km': 0, 'highway_km': 1500,
                'bus_routes': 25
            },
            'Al-Qassim': {
                'airports': 1, 'airport_capacity_mpax': 2,
                'rail_km': 100, 'metro_km': 0, 'highway_km': 1200,
                'bus_routes': 15
            },
            'Asir': {
                'airports': 2, 'airport_capacity_mpax': 3,
                'rail_km': 0, 'metro_km': 0, 'highway_km': 1800,
                'bus_routes': 20
            },
            'Tabuk': {
                'airports': 1, 'airport_capacity_mpax': 2,
                'rail_km': 0, 'metro_km': 0, 'highway_km': 1500,
                'bus_routes': 10
            },
            'Hail': {
                'airports': 1, 'airport_capacity_mpax': 1.5,
                'rail_km': 0, 'metro_km': 0, 'highway_km': 1100,
                'bus_routes': 10
            },
            'Northern Borders': {
                'airports': 1, 'airport_capacity_mpax': 0.5,
                'rail_km': 0, 'metro_km': 0, 'highway_km': 800,
                'bus_routes': 5
            },
            'Jazan': {
                'airports': 1, 'airport_capacity_mpax': 1.5,
                'rail_km': 0, 'metro_km': 0, 'highway_km': 900,
                'bus_routes': 12
            },
            'Najran': {
                'airports': 1, 'airport_capacity_mpax': 0.8,
                'rail_km': 0, 'metro_km': 0, 'highway_km': 700,
                'bus_routes': 8
            },
            'Al-Baha': {
                'airports': 1, 'airport_capacity_mpax': 0.3,
                'rail_km': 0, 'metro_km': 0, 'highway_km': 500,
                'bus_routes': 6
            },
            'Al-Jouf': {
                'airports': 1, 'airport_capacity_mpax': 0.5,
                'rail_km': 0, 'metro_km': 0, 'highway_km': 600,
                'bus_routes': 5
            }
        }
        
        for region, profile in transport_profiles.items():
            transport.append({
                'region_name_en': region,
                **profile,
                'year': 2024
            })
        
        # Energy infrastructure
        energy = []
        
        energy_profiles = {
            'Riyadh': {'power_capacity_gw': 25, 'solar_capacity_mw': 1500, 'grid_coverage_pct': 100},
            'Makkah': {'power_capacity_gw': 18, 'solar_capacity_mw': 500, 'grid_coverage_pct': 100},
            'Eastern Province': {'power_capacity_gw': 22, 'solar_capacity_mw': 800, 'grid_coverage_pct': 100},
            'Madinah': {'power_capacity_gw': 6, 'solar_capacity_mw': 300, 'grid_coverage_pct': 99},
            'Al-Qassim': {'power_capacity_gw': 4, 'solar_capacity_mw': 600, 'grid_coverage_pct': 98},
            'Asir': {'power_capacity_gw': 3.5, 'solar_capacity_mw': 200, 'grid_coverage_pct': 97},
            'Tabuk': {'power_capacity_gw': 2.5, 'solar_capacity_mw': 400, 'grid_coverage_pct': 95},
            'Hail': {'power_capacity_gw': 2, 'solar_capacity_mw': 300, 'grid_coverage_pct': 96},
            'Northern Borders': {'power_capacity_gw': 1.2, 'solar_capacity_mw': 150, 'grid_coverage_pct': 94},
            'Jazan': {'power_capacity_gw': 2.5, 'solar_capacity_mw': 100, 'grid_coverage_pct': 96},
            'Najran': {'power_capacity_gw': 1.5, 'solar_capacity_mw': 200, 'grid_coverage_pct': 95},
            'Al-Baha': {'power_capacity_gw': 0.8, 'solar_capacity_mw': 50, 'grid_coverage_pct': 97},
            'Al-Jouf': {'power_capacity_gw': 1.5, 'solar_capacity_mw': 400, 'grid_coverage_pct': 95}
        }
        
        for region, profile in energy_profiles.items():
            energy.append({
                'region_name_en': region,
                **profile,
                'wind_capacity_mw': 400 if region == 'Al-Jouf' else self.rng.integers(0, 100),
                'renewable_share_pct': round((profile['solar_capacity_mw'] / (profile['power_capacity_gw'] * 1000)) * 100, 1),
                'year': 2024
            })
        
        # Ports (coastal regions only)
        ports = []
        port_data = [
            {'region': 'Makkah', 'port_name': 'Jeddah Islamic Port', 'type': 'Commercial', 'capacity_teu': 7500000, 'lat': 21.48, 'lon': 39.17},
            {'region': 'Makkah', 'port_name': 'King Abdullah Port', 'type': 'Commercial', 'capacity_teu': 3000000, 'lat': 22.45, 'lon': 39.13},
            {'region': 'Eastern Province', 'port_name': 'King Abdulaziz Port (Dammam)', 'type': 'Commercial', 'capacity_teu': 2500000, 'lat': 26.43, 'lon': 50.10},
            {'region': 'Eastern Province', 'port_name': 'Jubail Commercial Port', 'type': 'Industrial', 'capacity_teu': 1500000, 'lat': 27.01, 'lon': 49.66},
            {'region': 'Eastern Province', 'port_name': 'Ras Tanura', 'type': 'Oil', 'capacity_teu': 0, 'lat': 26.64, 'lon': 50.16},
            {'region': 'Tabuk', 'port_name': 'NEOM Port', 'type': 'Commercial', 'capacity_teu': 500000, 'lat': 28.0, 'lon': 35.0},
            {'region': 'Jazan', 'port_name': 'Jazan Port', 'type': 'Commercial', 'capacity_teu': 800000, 'lat': 16.9, 'lon': 42.55},
            {'region': 'Madinah', 'port_name': 'Yanbu Commercial Port', 'type': 'Industrial', 'capacity_teu': 1200000, 'lat': 24.09, 'lon': 38.06}
        ]
        
        for p in port_data:
            ports.append({
                'region_name_en': p['region'],
                'port_name': p['port_name'],
                'port_type': p['type'],
                'capacity_teu_annual': p['capacity_teu'],
                'latitude': p['lat'],
                'longitude': p['lon'],
                'year': 2024
            })
        
        # Telecommunications
        telecom = []
        for region in transport_profiles.keys():
            if region in ['Riyadh', 'Makkah', 'Eastern Province']:
                fiber_coverage = self.rng.uniform(85, 95)
                mobile_5g = self.rng.uniform(70, 85)
            else:
                fiber_coverage = self.rng.uniform(50, 75)
                mobile_5g = self.rng.uniform(40, 60)
            
            telecom.append({
                'region_name_en': region,
                'fiber_coverage_pct': round(fiber_coverage, 1),
                'mobile_coverage_4g_pct': round(self.rng.uniform(95, 99), 1),
                'mobile_coverage_5g_pct': round(mobile_5g, 1),
                'internet_penetration_pct': round(self.rng.uniform(90, 98), 1),
                'data_centers': 5 if region == 'Riyadh' else 2 if region in ['Makkah', 'Eastern Province'] else 0,
                'year': 2024
            })
        
        return {
            'transport': pd.DataFrame(transport),
            'energy': pd.DataFrame(energy),
            'ports': pd.DataFrame(ports),
            'telecommunications': pd.DataFrame(telecom)
        }
    
    # =========================================================================
    # 5. PROJECTS DATA (Enhanced)
    # =========================================================================
    
    def generate_projects_detailed(self) -> pd.DataFrame:
        """Generate detailed Vision 2030 and other major projects."""
        
        projects = [
            # NEOM Ecosystem
            {'name': 'NEOM', 'sector': 'Giga City', 'budget_b': 500, 'jobs': 380000, 'region': 'Tabuk',
             'status': 'Under Construction', 'start': 2017, 'end': 2039, 'lat': 28.0, 'lon': 35.0,
             'description': 'Smart city megaproject on Red Sea coast', 'flagship': True},
            {'name': 'THE LINE', 'sector': 'Urban', 'budget_b': 200, 'jobs': 100000, 'region': 'Tabuk',
             'status': 'Under Construction', 'start': 2021, 'end': 2030, 'lat': 28.1, 'lon': 34.8,
             'description': '170km linear city with zero cars', 'flagship': True},
            {'name': 'OXAGON', 'sector': 'Industrial', 'budget_b': 50, 'jobs': 90000, 'region': 'Tabuk',
             'status': 'Under Construction', 'start': 2021, 'end': 2030, 'lat': 27.8, 'lon': 35.2,
             'description': 'Floating industrial city', 'flagship': True},
            {'name': 'TROJENA', 'sector': 'Tourism', 'budget_b': 30, 'jobs': 35000, 'region': 'Tabuk',
             'status': 'Under Construction', 'start': 2022, 'end': 2026, 'lat': 28.2, 'lon': 35.5,
             'description': 'Mountain tourism with year-round skiing', 'flagship': True},
            {'name': 'SINDALAH', 'sector': 'Tourism', 'budget_b': 5, 'jobs': 3500, 'region': 'Tabuk',
             'status': 'Operational', 'start': 2022, 'end': 2024, 'lat': 27.5, 'lon': 35.8,
             'description': 'Luxury island destination', 'flagship': False},
            
            # Red Sea
            {'name': 'Red Sea Global', 'sector': 'Tourism', 'budget_b': 15, 'jobs': 70000, 'region': 'Madinah',
             'status': 'Under Construction', 'start': 2019, 'end': 2030, 'lat': 25.5, 'lon': 37.0,
             'description': 'Luxury resort across 90+ islands', 'flagship': True},
            {'name': 'AMAALA', 'sector': 'Tourism', 'budget_b': 8, 'jobs': 25000, 'region': 'Tabuk',
             'status': 'Under Construction', 'start': 2020, 'end': 2028, 'lat': 26.0, 'lon': 36.5,
             'description': 'Ultra-luxury wellness destination', 'flagship': True},
            
            # Riyadh
            {'name': 'Qiddiya', 'sector': 'Entertainment', 'budget_b': 8, 'jobs': 57000, 'region': 'Riyadh',
             'status': 'Under Construction', 'start': 2019, 'end': 2030, 'lat': 24.4, 'lon': 46.2,
             'description': 'Entertainment mega-city', 'flagship': True},
            {'name': 'Diriyah Gate', 'sector': 'Heritage', 'budget_b': 20, 'jobs': 55000, 'region': 'Riyadh',
             'status': 'Under Construction', 'start': 2018, 'end': 2027, 'lat': 24.73, 'lon': 46.58,
             'description': 'UNESCO heritage district', 'flagship': True},
            {'name': 'King Salman Park', 'sector': 'Urban', 'budget_b': 23, 'jobs': 22000, 'region': 'Riyadh',
             'status': 'Under Construction', 'start': 2019, 'end': 2027, 'lat': 24.68, 'lon': 46.72,
             'description': '13 sq km urban park', 'flagship': True},
            {'name': 'Riyadh Metro', 'sector': 'Transport', 'budget_b': 22.5, 'jobs': 15000, 'region': 'Riyadh',
             'status': 'Operational', 'start': 2014, 'end': 2024, 'lat': 24.7, 'lon': 46.7,
             'description': '176km metro with 6 lines', 'flagship': True},
            {'name': 'New Murabba', 'sector': 'Urban', 'budget_b': 50, 'jobs': 85000, 'region': 'Riyadh',
             'status': 'Under Construction', 'start': 2024, 'end': 2030, 'lat': 24.8, 'lon': 46.6,
             'description': 'Downtown with Mukaab cube', 'flagship': True},
            {'name': 'King Abdullah Financial District', 'sector': 'Commercial', 'budget_b': 10, 'jobs': 45000, 'region': 'Riyadh',
             'status': 'Operational', 'start': 2006, 'end': 2023, 'lat': 24.76, 'lon': 46.64,
             'description': 'Financial hub of Saudi Arabia', 'flagship': False},
            {'name': 'Sports Boulevard', 'sector': 'Urban', 'budget_b': 5, 'jobs': 12000, 'region': 'Riyadh',
             'status': 'Under Construction', 'start': 2019, 'end': 2028, 'lat': 24.68, 'lon': 46.65,
             'description': '135km sports and recreation corridor', 'flagship': False},
            
            # AlUla
            {'name': 'AlUla Development', 'sector': 'Heritage', 'budget_b': 15, 'jobs': 38000, 'region': 'Madinah',
             'status': 'Under Construction', 'start': 2018, 'end': 2035, 'lat': 26.6, 'lon': 37.9,
             'description': 'UNESCO heritage tourism', 'flagship': True},
            
            # Jeddah
            {'name': 'Jeddah Tower', 'sector': 'Urban', 'budget_b': 2, 'jobs': 5000, 'region': 'Makkah',
             'status': 'Under Construction', 'start': 2013, 'end': 2028, 'lat': 21.48, 'lon': 39.24,
             'description': '1km tall skyscraper', 'flagship': True},
            {'name': 'Jeddah Central', 'sector': 'Urban', 'budget_b': 20, 'jobs': 42000, 'region': 'Makkah',
             'status': 'Planned', 'start': 2025, 'end': 2035, 'lat': 21.53, 'lon': 39.12,
             'description': 'Waterfront mega development', 'flagship': True},
            
            # Energy
            {'name': 'NEOM Green Hydrogen', 'sector': 'Energy', 'budget_b': 8.5, 'jobs': 4000, 'region': 'Tabuk',
             'status': 'Under Construction', 'start': 2021, 'end': 2026, 'lat': 28.3, 'lon': 35.3,
             'description': 'World largest green hydrogen', 'flagship': True},
            {'name': 'Sudair Solar PV', 'sector': 'Energy', 'budget_b': 1.5, 'jobs': 1200, 'region': 'Riyadh',
             'status': 'Operational', 'start': 2021, 'end': 2024, 'lat': 25.5, 'lon': 45.7,
             'description': '1.5 GW solar power', 'flagship': False},
            {'name': 'Dumat Al Jandal Wind', 'sector': 'Energy', 'budget_b': 0.5, 'jobs': 500, 'region': 'Al-Jouf',
             'status': 'Operational', 'start': 2019, 'end': 2022, 'lat': 29.8, 'lon': 39.9,
             'description': '400 MW wind farm', 'flagship': False},
            {'name': 'Shuaibah 3 IWP', 'sector': 'Water', 'budget_b': 0.8, 'jobs': 800, 'region': 'Makkah',
             'status': 'Operational', 'start': 2019, 'end': 2023, 'lat': 21.12, 'lon': 39.33,
             'description': 'Desalination plant', 'flagship': False},
            
            # Industrial
            {'name': 'King Abdullah Economic City', 'sector': 'Industrial', 'budget_b': 100, 'jobs': 1000000, 'region': 'Makkah',
             'status': 'Operational', 'start': 2006, 'end': 2035, 'lat': 22.4, 'lon': 39.1,
             'description': 'Industrial port city', 'flagship': True},
            {'name': 'SPARK Energy Park', 'sector': 'Industrial', 'budget_b': 2, 'jobs': 100000, 'region': 'Eastern Province',
             'status': 'Under Construction', 'start': 2018, 'end': 2035, 'lat': 25.5, 'lon': 49.2,
             'description': '50 sq km energy city', 'flagship': True},
            {'name': 'Ras Al-Khair Mining City', 'sector': 'Mining', 'budget_b': 7, 'jobs': 15000, 'region': 'Eastern Province',
             'status': 'Operational', 'start': 2011, 'end': 2020, 'lat': 27.5, 'lon': 49.2,
             'description': 'Phosphate & aluminum complex', 'flagship': False},
            
            # Transport
            {'name': 'Haramain High Speed Rail', 'sector': 'Transport', 'budget_b': 16, 'jobs': 8000, 'region': 'Makkah',
             'status': 'Operational', 'start': 2009, 'end': 2018, 'lat': 21.95, 'lon': 39.32,
             'description': '450km Makkah-Madinah railway', 'flagship': True},
            {'name': 'Saudi Landbridge', 'sector': 'Transport', 'budget_b': 7, 'jobs': 12000, 'region': 'Riyadh',
             'status': 'Under Construction', 'start': 2021, 'end': 2030, 'lat': 24.7, 'lon': 46.7,
             'description': 'East-West railway connection', 'flagship': True},
        ]
        
        df = pd.DataFrame(projects)
        df['budget_billion_usd'] = df['budget_b']
        df = df.drop(columns=['budget_b'])
        
        return df
    
    # =========================================================================
    # MASTER GENERATOR
    # =========================================================================
    
    def generate_all_ws1_data(self, output_dir: Optional[Path] = None) -> Dict[str, pd.DataFrame]:
        """Generate all WS1 data and optionally save to files."""
        
        if output_dir is None:
            output_dir = PROCESSED_DIR / "ws1_complete"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Generating WS1 comprehensive dataset...")
        
        all_data = {}
        
        # 1. Demographics
        logger.info("  Generating demographic data...")
        demo_data = self.generate_demographic_detailed()
        for name, df in demo_data.items():
            all_data[f'demographics_{name}'] = df
            df.to_csv(output_dir / f'demographics_{name}.csv', index=False)
        
        # 2. Economics
        logger.info("  Generating economic data...")
        econ_data = self.generate_economic_detailed()
        for name, df in econ_data.items():
            all_data[f'economics_{name}'] = df
            df.to_csv(output_dir / f'economics_{name}.csv', index=False)
        
        # 3. Environment
        logger.info("  Generating environmental data...")
        env_data = self.generate_environmental_data()
        for name, df in env_data.items():
            all_data[f'environment_{name}'] = df
            df.to_csv(output_dir / f'environment_{name}.csv', index=False)
        
        # 4. Infrastructure
        logger.info("  Generating infrastructure data...")
        infra_data = self.generate_infrastructure_data()
        for name, df in infra_data.items():
            all_data[f'infrastructure_{name}'] = df
            df.to_csv(output_dir / f'infrastructure_{name}.csv', index=False)
        
        # 5. Projects
        logger.info("  Generating projects data...")
        projects_df = self.generate_projects_detailed()
        all_data['projects_vision2030'] = projects_df
        projects_df.to_csv(output_dir / 'projects_vision2030.csv', index=False)
        
        # Generate summary catalog
        catalog = {
            'generated_at': datetime.now().isoformat(),
            'datasets': [
                {
                    'name': name,
                    'rows': len(df),
                    'columns': list(df.columns)
                }
                for name, df in all_data.items()
            ]
        }
        
        with open(output_dir / 'DATA_CATALOG_WS1.json', 'w') as f:
            json.dump(catalog, f, indent=2)
        
        logger.info(f"✅ Generated {len(all_data)} datasets with {sum(len(df) for df in all_data.values())} total rows")
        logger.info(f"   Saved to: {output_dir}")
        
        return all_data


# CLI interface
if __name__ == "__main__":
    generator = WS1DataGenerator()
    data = generator.generate_all_ws1_data()
    
    print("\n📊 WS1 Data Generation Complete!")
    print("=" * 50)
    for name, df in data.items():
        print(f"  {name}: {len(df)} rows, {len(df.columns)} columns")
