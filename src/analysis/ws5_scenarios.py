"""
NSS X - WS5: Scenario Modeling 2030/2050
Modelagem de cenários de desenvolvimento territorial para a Arábia Saudita.
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from loguru import logger


class ScenarioType(Enum):
    """Types of development scenarios."""
    BASELINE = "baseline"           # Current trends continue
    VISION2030 = "vision2030"       # Full Vision 2030 achievement
    ACCELERATED = "accelerated"     # Beyond Vision 2030 targets
    CONSERVATIVE = "conservative"   # Slower transformation


@dataclass
class DemographicProjection:
    """Demographic projection for a scenario."""
    year: int
    total_population: float  # millions
    saudi_population: float
    expat_population: float
    urban_population_pct: float
    riyadh_share_pct: float
    youth_share_pct: float  # under 30


@dataclass
class EconomicProjection:
    """Economic projection for a scenario."""
    year: int
    gdp_billion_usd: float
    gdp_per_capita_usd: float
    oil_gdp_share_pct: float
    tourism_gdp_share_pct: float
    tech_gdp_share_pct: float
    unemployment_rate_pct: float
    female_labor_participation_pct: float


@dataclass
class SpatialProjection:
    """Spatial development projection."""
    year: int
    urbanized_area_sqkm: float
    new_cities_completed: int
    protected_area_pct: float
    renewable_capacity_gw: float
    rail_network_km: float
    desalination_capacity_mcm: float  # million cubic meters


@dataclass 
class Scenario:
    """Complete development scenario."""
    name: str
    type: ScenarioType
    description: str
    key_assumptions: List[str]
    demographic_path: List[DemographicProjection]
    economic_path: List[EconomicProjection]
    spatial_path: List[SpatialProjection]
    probability: float  # Estimated probability of occurrence
    key_risks: List[str]
    key_opportunities: List[str]


class ScenarioModeler:
    """
    WS5 - Scenario Modeling Module
    Projects development trajectories to 2030 and 2050.
    """
    
    def __init__(self):
        """Initialize scenario modeler."""
        self.base_year = 2024
        self.scenarios: Dict[ScenarioType, Scenario] = {}
        self._build_scenarios()
        logger.info("WS5 Scenario Modeler initialized with 4 scenarios")
    
    def _build_scenarios(self):
        """Build all development scenarios."""
        self.scenarios[ScenarioType.BASELINE] = self._build_baseline_scenario()
        self.scenarios[ScenarioType.VISION2030] = self._build_vision2030_scenario()
        self.scenarios[ScenarioType.ACCELERATED] = self._build_accelerated_scenario()
        self.scenarios[ScenarioType.CONSERVATIVE] = self._build_conservative_scenario()
    
    def _build_baseline_scenario(self) -> Scenario:
        """Build baseline (current trends) scenario."""
        
        # Demographic projections - moderate growth
        demographics = []
        base_pop = 36.4
        for year in [2025, 2030, 2040, 2050]:
            years = year - 2024
            pop = base_pop * (1.018 ** years)  # 1.8% growth
            demographics.append(DemographicProjection(
                year=year,
                total_population=pop,
                saudi_population=pop * 0.66,
                expat_population=pop * 0.34,
                urban_population_pct=min(86 + years * 0.3, 92),
                riyadh_share_pct=min(25 + years * 0.15, 32),
                youth_share_pct=max(63 - years * 0.4, 45)
            ))
        
        # Economic projections
        economics = []
        base_gdp = 1108  # billion USD
        for year in [2025, 2030, 2040, 2050]:
            years = year - 2024
            gdp = base_gdp * (1.03 ** years)  # 3% growth
            pop_millions = demographics[min(len(demographics)-1, [2025,2030,2040,2050].index(year))].total_population
            economics.append(EconomicProjection(
                year=year,
                gdp_billion_usd=gdp,
                gdp_per_capita_usd=(gdp * 1e9) / (pop_millions * 1e6),
                oil_gdp_share_pct=max(38 - years * 0.8, 20),
                tourism_gdp_share_pct=min(5 + years * 0.5, 15),
                tech_gdp_share_pct=min(4 + years * 0.4, 12),
                unemployment_rate_pct=max(11 - years * 0.2, 6),
                female_labor_participation_pct=min(33 + years * 0.8, 45)
            ))
        
        # Spatial projections
        spatial = []
        for year in [2025, 2030, 2040, 2050]:
            years = year - 2024
            spatial.append(SpatialProjection(
                year=year,
                urbanized_area_sqkm=5000 + years * 150,
                new_cities_completed=min(1 + years // 5, 3),
                protected_area_pct=4 + years * 0.1,
                renewable_capacity_gw=5 + years * 1.5,
                rail_network_km=1200 + years * 80,
                desalination_capacity_mcm=2500 + years * 100
            ))
        
        return Scenario(
            name="Baseline (Current Trends)",
            type=ScenarioType.BASELINE,
            description="Continuation of current development trends without major policy shifts.",
            key_assumptions=[
                "Oil prices remain moderate ($70-80/barrel)",
                "Vision 2030 targets partially achieved",
                "Regional stability maintained",
                "Gradual economic diversification",
                "Climate policies implemented slowly"
            ],
            demographic_path=demographics,
            economic_path=economics,
            spatial_path=spatial,
            probability=0.30,
            key_risks=[
                "Insufficient diversification",
                "Youth unemployment persistence",
                "Water stress intensification",
                "Climate change impacts"
            ],
            key_opportunities=[
                "Incremental progress on transformation",
                "Lower financial risk",
                "Social stability"
            ]
        )
    
    def _build_vision2030_scenario(self) -> Scenario:
        """Build Vision 2030 achievement scenario."""
        
        demographics = []
        base_pop = 36.4
        for year in [2025, 2030, 2040, 2050]:
            years = year - 2024
            pop = base_pop * (1.022 ** years)  # 2.2% growth
            demographics.append(DemographicProjection(
                year=year,
                total_population=pop,
                saudi_population=pop * 0.62,
                expat_population=pop * 0.38,  # More expats for mega-projects
                urban_population_pct=min(86 + years * 0.4, 95),
                riyadh_share_pct=min(25 + years * 0.2, 35),
                youth_share_pct=max(63 - years * 0.35, 48)
            ))
        
        economics = []
        base_gdp = 1108
        for year in [2025, 2030, 2040, 2050]:
            years = year - 2024
            gdp = base_gdp * (1.05 ** years)  # 5% growth
            pop_millions = demographics[min(len(demographics)-1, [2025,2030,2040,2050].index(year))].total_population
            economics.append(EconomicProjection(
                year=year,
                gdp_billion_usd=gdp,
                gdp_per_capita_usd=(gdp * 1e9) / (pop_millions * 1e6),
                oil_gdp_share_pct=max(38 - years * 1.5, 12),
                tourism_gdp_share_pct=min(5 + years * 1.0, 20),
                tech_gdp_share_pct=min(4 + years * 0.8, 18),
                unemployment_rate_pct=max(11 - years * 0.5, 4),
                female_labor_participation_pct=min(33 + years * 1.5, 55)
            ))
        
        spatial = []
        for year in [2025, 2030, 2040, 2050]:
            years = year - 2024
            spatial.append(SpatialProjection(
                year=year,
                urbanized_area_sqkm=5000 + years * 250,
                new_cities_completed=min(2 + years // 3, 8),  # NEOM, KAEC, etc.
                protected_area_pct=4 + years * 0.25,  # 30% by 2030 target
                renewable_capacity_gw=5 + years * 4,  # 50GW by 2030
                rail_network_km=1200 + years * 150,
                desalination_capacity_mcm=2500 + years * 200
            ))
        
        return Scenario(
            name="Vision 2030 Achievement",
            type=ScenarioType.VISION2030,
            description="Full achievement of Vision 2030 targets and continued progress to 2050.",
            key_assumptions=[
                "Strong oil prices support transition ($80-100/barrel)",
                "Mega-projects delivered on schedule",
                "Tourism reaches 100M visitors by 2030",
                "Non-oil GDP dominates by 2040",
                "Significant social reforms continue"
            ],
            demographic_path=demographics,
            economic_path=economics,
            spatial_path=spatial,
            probability=0.35,
            key_risks=[
                "Mega-project cost overruns",
                "Global economic downturn",
                "Execution capacity constraints",
                "Labor market imbalances"
            ],
            key_opportunities=[
                "Global tourism hub",
                "Regional technology leader",
                "Clean energy pioneer",
                "Entertainment capital"
            ]
        )
    
    def _build_accelerated_scenario(self) -> Scenario:
        """Build accelerated transformation scenario."""
        
        demographics = []
        base_pop = 36.4
        for year in [2025, 2030, 2040, 2050]:
            years = year - 2024
            pop = base_pop * (1.025 ** years)  # 2.5% growth
            demographics.append(DemographicProjection(
                year=year,
                total_population=pop,
                saudi_population=pop * 0.58,
                expat_population=pop * 0.42,  # High immigration
                urban_population_pct=min(86 + years * 0.5, 98),
                riyadh_share_pct=min(25 + years * 0.1, 30),  # More distributed
                youth_share_pct=max(63 - years * 0.3, 50)
            ))
        
        economics = []
        base_gdp = 1108
        for year in [2025, 2030, 2040, 2050]:
            years = year - 2024
            gdp = base_gdp * (1.07 ** years)  # 7% growth
            pop_millions = demographics[min(len(demographics)-1, [2025,2030,2040,2050].index(year))].total_population
            economics.append(EconomicProjection(
                year=year,
                gdp_billion_usd=gdp,
                gdp_per_capita_usd=(gdp * 1e9) / (pop_millions * 1e6),
                oil_gdp_share_pct=max(38 - years * 2.0, 8),
                tourism_gdp_share_pct=min(5 + years * 1.2, 25),
                tech_gdp_share_pct=min(4 + years * 1.2, 25),
                unemployment_rate_pct=max(11 - years * 0.6, 3),
                female_labor_participation_pct=min(33 + years * 2.0, 65)
            ))
        
        spatial = []
        for year in [2025, 2030, 2040, 2050]:
            years = year - 2024
            spatial.append(SpatialProjection(
                year=year,
                urbanized_area_sqkm=5000 + years * 350,
                new_cities_completed=min(3 + years // 2, 15),
                protected_area_pct=4 + years * 0.4,  # 40% by 2040
                renewable_capacity_gw=5 + years * 6,  # 100GW+ by 2040
                rail_network_km=1200 + years * 200,
                desalination_capacity_mcm=2500 + years * 300
            ))
        
        return Scenario(
            name="Accelerated Transformation",
            type=ScenarioType.ACCELERATED,
            description="Beyond Vision 2030 - rapid diversification and global leadership.",
            key_assumptions=[
                "Green hydrogen becomes major export",
                "NEOM becomes global innovation hub",
                "KSA leads G20 in growth rates",
                "Full energy transition by 2045",
                "Regional economic integration (GCC+)"
            ],
            demographic_path=demographics,
            economic_path=economics,
            spatial_path=spatial,
            probability=0.15,
            key_risks=[
                "Social disruption from rapid change",
                "Infrastructure capacity limits",
                "Environmental carrying capacity",
                "Geopolitical instability"
            ],
            key_opportunities=[
                "Global economic power",
                "Technology leadership",
                "Sustainable development model",
                "Polycentric urban network"
            ]
        )
    
    def _build_conservative_scenario(self) -> Scenario:
        """Build conservative (slower transition) scenario."""
        
        demographics = []
        base_pop = 36.4
        for year in [2025, 2030, 2040, 2050]:
            years = year - 2024
            pop = base_pop * (1.012 ** years)  # 1.2% growth
            demographics.append(DemographicProjection(
                year=year,
                total_population=pop,
                saudi_population=pop * 0.70,
                expat_population=pop * 0.30,  # Fewer expats
                urban_population_pct=min(86 + years * 0.2, 90),
                riyadh_share_pct=min(25 + years * 0.25, 38),  # More concentration
                youth_share_pct=max(63 - years * 0.5, 42)
            ))
        
        economics = []
        base_gdp = 1108
        for year in [2025, 2030, 2040, 2050]:
            years = year - 2024
            gdp = base_gdp * (1.02 ** years)  # 2% growth
            pop_millions = demographics[min(len(demographics)-1, [2025,2030,2040,2050].index(year))].total_population
            economics.append(EconomicProjection(
                year=year,
                gdp_billion_usd=gdp,
                gdp_per_capita_usd=(gdp * 1e9) / (pop_millions * 1e6),
                oil_gdp_share_pct=max(38 - years * 0.5, 28),
                tourism_gdp_share_pct=min(5 + years * 0.3, 10),
                tech_gdp_share_pct=min(4 + years * 0.2, 8),
                unemployment_rate_pct=max(11 - years * 0.1, 8),
                female_labor_participation_pct=min(33 + years * 0.5, 40)
            ))
        
        spatial = []
        for year in [2025, 2030, 2040, 2050]:
            years = year - 2024
            spatial.append(SpatialProjection(
                year=year,
                urbanized_area_sqkm=5000 + years * 100,
                new_cities_completed=min(1 + years // 8, 2),
                protected_area_pct=4 + years * 0.05,
                renewable_capacity_gw=5 + years * 0.8,
                rail_network_km=1200 + years * 50,
                desalination_capacity_mcm=2500 + years * 80
            ))
        
        return Scenario(
            name="Conservative (Slower Transition)",
            type=ScenarioType.CONSERVATIVE,
            description="Slower transformation due to external or internal constraints.",
            key_assumptions=[
                "Oil prices decline ($50-60/barrel)",
                "Global recession impacts investment",
                "Mega-projects scaled back",
                "Gradual social reforms",
                "Regional tensions increase"
            ],
            demographic_path=demographics,
            economic_path=economics,
            spatial_path=spatial,
            probability=0.20,
            key_risks=[
                "Economic stagnation",
                "Youth frustration",
                "Continued oil dependence",
                "Brain drain"
            ],
            key_opportunities=[
                "Lower risk exposure",
                "More sustainable pace",
                "Consolidation of gains"
            ]
        )
    
    def get_scenario(self, scenario_type: ScenarioType) -> Scenario:
        """Get a specific scenario."""
        return self.scenarios[scenario_type]
    
    def compare_scenarios(self, year: int = 2030) -> pd.DataFrame:
        """Compare all scenarios at a specific year."""
        comparisons = []
        
        for scenario in self.scenarios.values():
            # Find projections for the target year
            demo = next((d for d in scenario.demographic_path if d.year == year), None)
            econ = next((e for e in scenario.economic_path if e.year == year), None)
            spatial = next((s for s in scenario.spatial_path if s.year == year), None)
            
            if demo and econ and spatial:
                comparisons.append({
                    'Scenario': scenario.name,
                    'Population (M)': demo.total_population,
                    'GDP ($B)': econ.gdp_billion_usd,
                    'GDP/Capita ($)': econ.gdp_per_capita_usd,
                    'Oil Share (%)': econ.oil_gdp_share_pct,
                    'Tourism Share (%)': econ.tourism_gdp_share_pct,
                    'Urban (%)': demo.urban_population_pct,
                    'Renewable GW': spatial.renewable_capacity_gw,
                    'Probability': scenario.probability
                })
        
        return pd.DataFrame(comparisons)
    
    def project_region(self, region_name: str, scenario_type: ScenarioType) -> Dict:
        """Project development for a specific region under a scenario."""
        scenario = self.scenarios[scenario_type]
        
        # Regional factors (would come from spatial analysis in production)
        regional_factors = {
            'Riyadh': {'growth_multiplier': 1.2, 'diversification_leader': True},
            'Eastern Province': {'growth_multiplier': 0.9, 'oil_dependent': True},
            'Makkah': {'growth_multiplier': 1.1, 'tourism_focus': True},
            'Madinah': {'growth_multiplier': 1.0, 'tourism_focus': True},
            'Tabuk': {'growth_multiplier': 1.5, 'neom_effect': True},
            'Al-Qassim': {'growth_multiplier': 0.8, 'agricultural_focus': True},
        }
        
        factor = regional_factors.get(region_name, {'growth_multiplier': 1.0})
        
        projections = []
        for year in [2025, 2030, 2040, 2050]:
            demo = next((d for d in scenario.demographic_path if d.year == year), None)
            econ = next((e for e in scenario.economic_path if e.year == year), None)
            
            if demo and econ:
                projections.append({
                    'year': year,
                    'population': demo.total_population * 0.1 * factor['growth_multiplier'],  # Simplified
                    'gdp_share': econ.gdp_billion_usd * 0.1 * factor['growth_multiplier']
                })
        
        return {
            'region': region_name,
            'scenario': scenario.name,
            'projections': projections,
            'characteristics': factor
        }
    
    def generate_scenario_report(self) -> Dict:
        """Generate comprehensive scenario analysis report."""
        
        comparison_2030 = self.compare_scenarios(2030)
        comparison_2050 = self.compare_scenarios(2050)
        
        report = {
            "title": "WS5 - Scenario Analysis: Saudi Arabia 2030/2050",
            "base_year": self.base_year,
            "target_years": [2030, 2050],
            "scenarios_analyzed": 4,
            "scenario_summaries": {
                s.type.value: {
                    "name": s.name,
                    "description": s.description,
                    "probability": s.probability,
                    "key_assumptions": s.key_assumptions[:3],
                    "key_risks": s.key_risks[:3],
                    "key_opportunities": s.key_opportunities[:3]
                }
                for s in self.scenarios.values()
            },
            "comparison_2030": comparison_2030.to_dict(orient='records'),
            "comparison_2050": comparison_2050.to_dict(orient='records'),
            "key_findings": {
                "population_range_2030": f"{comparison_2030['Population (M)'].min():.1f}M - {comparison_2030['Population (M)'].max():.1f}M",
                "gdp_range_2030": f"${comparison_2030['GDP ($B)'].min():.0f}B - ${comparison_2030['GDP ($B)'].max():.0f}B",
                "population_range_2050": f"{comparison_2050['Population (M)'].min():.1f}M - {comparison_2050['Population (M)'].max():.1f}M",
                "gdp_range_2050": f"${comparison_2050['GDP ($B)'].min():.0f}B - ${comparison_2050['GDP ($B)'].max():.0f}B",
                "diversification_success": "Vision 2030 scenario achieves <20% oil dependence by 2030"
            },
            "recommendations": {
                "planning": [
                    "Adopt flexible spatial planning accommodating multiple scenarios",
                    "Prioritize infrastructure investments robust across scenarios",
                    "Develop adaptive management frameworks"
                ],
                "monitoring": [
                    "Establish scenario tracking indicators",
                    "Create early warning system for trajectory deviation",
                    "Regular scenario updates (bi-annual)"
                ],
                "resilience": [
                    "Build redundancy in critical systems",
                    "Diversify economic corridors",
                    "Protect natural capital as insurance"
                ]
            },
            "data_sources": [
                "GASTAT demographic projections",
                "Vision 2030 official targets",
                "IMF economic forecasts",
                "SAMA annual reports",
                "Academic research on KSA development"
            ]
        }
        
        return report


# Convenience function
def run_scenario_analysis() -> Dict:
    """Run complete WS5 scenario analysis."""
    modeler = ScenarioModeler()
    return modeler.generate_scenario_report()
