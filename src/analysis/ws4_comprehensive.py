"""
NSS X - WS4: Comprehensive Sectoral & Regional Spatial Integration
Complete analysis module for Workstream 4 deliverables.

Deliverables:
- 4.1 Integrated Sectoral and Regional Spatial Review
- 4.2 2030 Conflict and Synergy Maps
- 4.3 Corrective Measures and Optimization Playbook
- 4.4 Stakeholder Workshop Materials
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path
import json
from enum import Enum
from loguru import logger

# Import base sectoral analyzer
from .ws4_sectoral import SectoralAnalyzer, SectorProfile, ConflictLevel, ConflictAssessment


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class SectoralStrategy:
    """Review of a sectoral strategy and its spatial implications."""
    sector_name: str
    strategy_document: str
    vision2030_program: str
    key_objectives: List[str]
    spatial_requirements: List[str]
    target_regions: List[str]
    land_area_needed_km2: float
    water_demand_mcm_year: float  # Million cubic meters per year
    employment_target_2030: int
    investment_target_sar_billion: float
    key_projects: List[str]
    spatial_conflicts: List[str]
    spatial_synergies: List[str]
    recommendations: List[str]


@dataclass
class RegionalDiagnostic:
    """Comprehensive diagnostic of a region."""
    region_name: str
    region_name_ar: str
    area_km2: float
    population_2025: float
    population_2030_projected: float
    urbanization_rate: float
    
    # Settlement hierarchy
    primary_city: str
    secondary_cities: List[str]
    settlement_count: int
    urban_primacy_ratio: float  # Primary city pop / total urban pop
    
    # Economic profile
    gdp_contribution_pct: float
    gdp_per_capita_sar: int
    dominant_sectors: List[str]
    emerging_sectors: List[str]
    employment_rate: float
    
    # Competitive advantages
    competitive_advantages: List[str]
    strategic_assets: List[str]
    
    # Environmental capacity
    water_availability: str  # critical, scarce, moderate, adequate
    water_sources: List[str]
    annual_water_demand_mcm: float
    annual_water_supply_mcm: float
    environmental_sensitivity: str  # high, medium, low
    protected_areas_pct: float
    climate_risks: List[str]
    
    # Development potential
    development_potential: str  # high, medium, low
    key_constraints: List[str]
    priority_investments: List[str]
    
    # Vision 2030 alignment
    giga_projects: List[str]
    vision2030_role: str


@dataclass
class ConflictMapLayer:
    """A spatial conflict or synergy map layer."""
    layer_name: str
    layer_type: str  # conflict, synergy
    description: str
    affected_regions: List[str]
    severity: str  # critical, high, medium, low
    land_uses_involved: List[str]
    area_affected_km2: float
    mitigation_priority: str
    visualization_style: Dict[str, Any]


@dataclass
class CorrectiveMeasure:
    """A corrective measure for spatial conflicts."""
    measure_id: str
    title: str
    conflict_addressed: str
    description: str
    measure_type: str  # regulatory, investment, incentive, planning
    target_regions: List[str]
    implementation_timeline: str  # immediate, short-term, medium-term, long-term
    estimated_cost_sar_million: float
    expected_benefit: str
    responsible_agency: str
    kpis: List[str]
    priority: str  # critical, high, medium, low


@dataclass
class WorkshopMaterial:
    """Materials for stakeholder workshops."""
    workshop_id: str
    title: str
    objective: str
    target_audience: List[str]
    duration_hours: float
    agenda_items: List[str]
    key_discussion_points: List[str]
    data_presentations: List[str]
    feedback_mechanisms: List[str]
    expected_outputs: List[str]


# =============================================================================
# SECTORAL STRATEGIES REVIEW
# =============================================================================

class SectoralStrategiesReviewer:
    """
    Reviews all major sectoral strategies and their spatial implications.
    """
    
    def __init__(self):
        """Initialize with sectoral strategy data."""
        self._build_strategies()
        logger.info("Sectoral Strategies Reviewer initialized with 6 strategies")
    
    def _build_strategies(self):
        """Build comprehensive sectoral strategy reviews."""
        
        self.strategies: Dict[str, SectoralStrategy] = {}
        
        # Tourism Strategy
        self.strategies['tourism'] = SectoralStrategy(
            sector_name="Tourism & Entertainment",
            strategy_document="National Tourism Strategy 2030",
            vision2030_program="Quality of Life Program",
            key_objectives=[
                "Achieve 100 million annual tourist visits by 2030",
                "Increase tourism GDP contribution to 10%",
                "Create 1 million tourism jobs",
                "Develop 5 world-class destinations",
                "Preserve and showcase Saudi heritage"
            ],
            spatial_requirements=[
                "Coastal resort development zones",
                "Heritage preservation districts",
                "Entertainment complexes in major cities",
                "Eco-tourism zones in natural areas",
                "Religious tourism infrastructure"
            ],
            target_regions=["Makkah", "Madinah", "Riyadh", "Tabuk", "Asir", "Eastern Province"],
            land_area_needed_km2=5000,
            water_demand_mcm_year=450,
            employment_target_2030=1000000,
            investment_target_sar_billion=500,
            key_projects=[
                "NEOM (Trojena ski resort, Sindalah island)",
                "Red Sea Project",
                "AMAALA",
                "Qiddiya Entertainment City",
                "Diriyah Gate",
                "AlUla Heritage Development"
            ],
            spatial_conflicts=[
                "Competition with residential development in coastal areas",
                "Water demand conflicts with agriculture",
                "Environmental protection vs infrastructure development",
                "Land value inflation displacing local communities"
            ],
            spatial_synergies=[
                "Transport infrastructure benefits multiple sectors",
                "Heritage preservation supports cultural identity",
                "Eco-tourism incentivizes environmental protection",
                "Entertainment attracts talent for other sectors"
            ],
            recommendations=[
                "Establish coastal zone management framework",
                "Create tourism-specific water allocation",
                "Integrate heritage protection in development approvals",
                "Develop local community benefit-sharing mechanisms"
            ]
        )
        
        # Industrial Strategy
        self.strategies['industrial'] = SectoralStrategy(
            sector_name="Manufacturing & Industry",
            strategy_document="National Industrial Development and Logistics Program (NIDLP)",
            vision2030_program="NIDLP",
            key_objectives=[
                "Increase industrial GDP to 20% of total",
                "Localize 50% of military equipment spending",
                "Develop renewable energy equipment manufacturing",
                "Create integrated industrial clusters",
                "Enhance export competitiveness"
            ],
            spatial_requirements=[
                "Industrial cities and zones",
                "Logistics hubs and dry ports",
                "Special economic zones",
                "Research and development parks",
                "Worker housing and amenities"
            ],
            target_regions=["Riyadh", "Eastern Province", "Makkah", "Madinah", "Tabuk"],
            land_area_needed_km2=3000,
            water_demand_mcm_year=800,
            employment_target_2030=1500000,
            investment_target_sar_billion=450,
            key_projects=[
                "NEOM Industrial City",
                "King Salman Energy Park (SPARK)",
                "Ras Al-Khair Industrial City expansion",
                "Sudair Industrial City",
                "Jazan Economic City",
                "King Abdullah Port expansion"
            ],
            spatial_conflicts=[
                "Industrial pollution affecting residential areas",
                "Heavy water consumption vs other uses",
                "Land conversion from agricultural use",
                "Transport congestion in mixed-use areas",
                "Environmental degradation risks"
            ],
            spatial_synergies=[
                "Integration with ports and logistics",
                "Shared infrastructure with energy sector",
                "Technology parks supporting innovation",
                "Employment centers reducing commuting"
            ],
            recommendations=[
                "Enforce strict separation from residential zones",
                "Mandate industrial water recycling (80% target)",
                "Create green industrial park standards",
                "Develop integrated industrial-logistics corridors"
            ]
        )
        
        # Energy Strategy
        self.strategies['energy'] = SectoralStrategy(
            sector_name="Energy (Conventional & Renewable)",
            strategy_document="Saudi Energy Efficiency Program & Renewable Energy Strategy",
            vision2030_program="Multiple programs",
            key_objectives=[
                "Achieve 50% renewable energy by 2030",
                "Reduce oil consumption in power generation",
                "Develop green hydrogen production",
                "Enhance energy efficiency by 30%",
                "Export clean energy technology"
            ],
            spatial_requirements=[
                "Solar farm sites (high irradiance areas)",
                "Wind farm sites (coastal and elevated areas)",
                "Transmission line corridors",
                "Green hydrogen production facilities",
                "Energy storage installations"
            ],
            target_regions=["Tabuk", "Al-Jouf", "Northern Borders", "Eastern Province", "NEOM"],
            land_area_needed_km2=8000,
            water_demand_mcm_year=200,
            employment_target_2030=200000,
            investment_target_sar_billion=200,
            key_projects=[
                "NEOM Green Hydrogen Project",
                "Sudair Solar PV Project (1.5 GW)",
                "Dumat Al-Jandal Wind Farm",
                "Red Sea renewable energy complex",
                "Sakaka Solar Project",
                "National grid expansion"
            ],
            spatial_conflicts=[
                "Solar farms competing with agricultural land",
                "Wind farms affecting bird migration routes",
                "Transmission corridors through protected areas",
                "Visual impact on tourism destinations"
            ],
            spatial_synergies=[
                "Agrivoltaics combining solar and agriculture",
                "Renewable energy supporting water desalination",
                "Green hydrogen enabling industrial decarbonization",
                "Rural electrification improving quality of life"
            ],
            recommendations=[
                "Prioritize degraded land for solar installations",
                "Establish renewable energy zones with streamlined approvals",
                "Integrate transmission planning with spatial strategy",
                "Create co-benefit requirements for renewable projects"
            ]
        )
        
        # Mining Strategy
        self.strategies['mining'] = SectoralStrategy(
            sector_name="Mining & Minerals",
            strategy_document="Mining Investment Law & Ma'aden Strategy",
            vision2030_program="NIDLP",
            key_objectives=[
                "Increase mining GDP contribution to 3% (SAR 240B)",
                "Develop phosphate, gold, copper, and rare earth extraction",
                "Create downstream processing industries",
                "Attract USD 170 billion in mining investment",
                "Become top 15 global mining nation"
            ],
            spatial_requirements=[
                "Mining concession areas",
                "Processing and smelting facilities",
                "Tailings storage facilities",
                "Transport corridors (rail and road)",
                "Mining towns and worker facilities"
            ],
            target_regions=["Northern Borders", "Madinah", "Tabuk", "Al-Jouf", "Najran"],
            land_area_needed_km2=15000,
            water_demand_mcm_year=350,
            employment_target_2030=250000,
            investment_target_sar_billion=170,
            key_projects=[
                "Waad Al-Shamal Phosphate City",
                "Ma'aden Gold Operations (Mahd Ad Dhahab)",
                "Jalamid Phosphate Mine",
                "Khnaiguiyah Zinc-Copper Project",
                "Arabian Shield rare earth exploration",
                "North-South Railway for mineral transport"
            ],
            spatial_conflicts=[
                "Land degradation and rehabilitation needs",
                "Water table depletion in mining areas",
                "Conflict with environmental protection zones",
                "Impact on traditional grazing lands",
                "Dust and pollution affecting nearby communities"
            ],
            spatial_synergies=[
                "Railway development benefiting other sectors",
                "Mining towns creating regional service centers",
                "Processing industries adding local value",
                "Technology development for harsh environment operations"
            ],
            recommendations=[
                "Establish mandatory rehabilitation bonds",
                "Create buffer zones around mining operations",
                "Require progressive reclamation plans",
                "Develop community benefit agreements"
            ]
        )
        
        # Agriculture Strategy
        self.strategies['agriculture'] = SectoralStrategy(
            sector_name="Agriculture & Food Security",
            strategy_document="National Agriculture Strategy & Environment Fund Strategy",
            vision2030_program="Environment Fund",
            key_objectives=[
                "Achieve 80% food security for strategic commodities",
                "Reduce agricultural water consumption by 40%",
                "Develop high-tech greenhouse agriculture",
                "Enhance date palm productivity and exports",
                "Support rural livelihoods"
            ],
            spatial_requirements=[
                "Irrigated agricultural zones",
                "Greenhouse and vertical farming complexes",
                "Food processing and storage facilities",
                "Livestock production areas",
                "Research stations"
            ],
            target_regions=["Al-Qassim", "Riyadh", "Hail", "Al-Jouf", "Jazan", "Asir"],
            land_area_needed_km2=50000,  # Largest spatial footprint
            water_demand_mcm_year=15000,  # 80%+ of total water use
            employment_target_2030=800000,
            investment_target_sar_billion=80,
            key_projects=[
                "NEOM Sustainable Food Production",
                "Al-Jouf Agricultural Development",
                "Jazan Coffee Cultivation Project",
                "National Aquaculture Strategy",
                "Indoor Farming Initiative",
                "Date Palm Enhancement Program"
            ],
            spatial_conflicts=[
                "CRITICAL: Water consumption unsustainable",
                "Urban expansion onto prime agricultural land",
                "Competition with solar energy for land",
                "Groundwater depletion affecting other sectors",
                "Agricultural runoff polluting water sources"
            ],
            spatial_synergies=[
                "Agrivoltaics combining solar and crops",
                "Treated wastewater reuse potential",
                "Rural tourism and agri-tourism",
                "Food processing supporting industrial sector"
            ],
            recommendations=[
                "CRITICAL: Phase out water-intensive crops (wheat, alfalfa)",
                "Establish agricultural land protection zones",
                "Mandate water-efficient irrigation technologies",
                "Promote high-value, low-water crops",
                "Develop treated wastewater reuse for agriculture"
            ]
        )
        
        # Transport Strategy
        self.strategies['transport'] = SectoralStrategy(
            sector_name="Transport & Logistics",
            strategy_document="National Transport & Logistics Strategy",
            vision2030_program="NIDLP",
            key_objectives=[
                "Connect all regions with modern transport infrastructure",
                "Develop Saudi Arabia as a global logistics hub",
                "Complete national railway network",
                "Expand port capacity to 40 million TEUs",
                "Enhance aviation to 330 million passengers"
            ],
            spatial_requirements=[
                "Railway corridors (5,000+ km new lines)",
                "Highway network expansion",
                "Airport expansion and new airports",
                "Port development and expansion",
                "Logistics parks and dry ports",
                "Intermodal transfer facilities"
            ],
            target_regions=["All 13 regions - national connectivity"],
            land_area_needed_km2=2000,
            water_demand_mcm_year=50,
            employment_target_2030=500000,
            investment_target_sar_billion=300,
            key_projects=[
                "Land Bridge (Red Sea to Gulf)",
                "Riyadh Metro (6 lines)",
                "Haramain High Speed Rail extension",
                "North-South Railway completion",
                "NEOM Mobility (Oxagon port, The Line transport)",
                "King Abdulaziz International Airport expansion",
                "Red Sea International Airport",
                "Jeddah Islamic Port expansion"
            ],
            spatial_conflicts=[
                "Railway corridors through agricultural land",
                "Airport noise zones affecting residential areas",
                "Port expansion impacting coastal ecosystems",
                "Highway construction fragmenting habitats"
            ],
            spatial_synergies=[
                "TOD (Transit-Oriented Development) opportunities",
                "Freight corridors supporting industrial clusters",
                "Aviation enabling tourism growth",
                "Connectivity reducing regional disparities"
            ],
            recommendations=[
                "Integrate transport planning with land use planning",
                "Establish TOD zones around all metro stations",
                "Create ecological crossing requirements for highways",
                "Develop noise mitigation standards for airports"
            ]
        )
    
    def get_strategy(self, sector_key: str) -> Optional[SectoralStrategy]:
        """Get strategy review for a specific sector."""
        return self.strategies.get(sector_key)
    
    def get_all_strategies(self) -> Dict[str, SectoralStrategy]:
        """Get all strategy reviews."""
        return self.strategies
    
    def get_total_spatial_requirements(self) -> Dict[str, Any]:
        """Calculate total spatial requirements across all sectors."""
        total_land = sum(s.land_area_needed_km2 for s in self.strategies.values())
        total_water = sum(s.water_demand_mcm_year for s in self.strategies.values())
        total_jobs = sum(s.employment_target_2030 for s in self.strategies.values())
        total_investment = sum(s.investment_target_sar_billion for s in self.strategies.values())
        
        return {
            "total_land_km2": total_land,
            "total_water_mcm_year": total_water,
            "total_employment_2030": total_jobs,
            "total_investment_sar_billion": total_investment,
            "ksa_total_area_km2": 2149690,
            "land_as_pct_of_total": (total_land / 2149690) * 100,
            "water_comparison": {
                "total_demand_mcm": total_water,
                "current_supply_mcm": 22000,
                "deficit_mcm": max(0, total_water - 22000),
                "agriculture_share_pct": (15000 / total_water) * 100
            }
        }


# =============================================================================
# REGIONAL DIAGNOSTICS
# =============================================================================

class RegionalDiagnosticsAnalyzer:
    """
    Generates comprehensive diagnostics for all 13 Saudi regions.
    """
    
    def __init__(self):
        """Initialize with regional data."""
        self._build_regional_diagnostics()
        logger.info("Regional Diagnostics Analyzer initialized with 13 regions")
    
    def _build_regional_diagnostics(self):
        """Build comprehensive regional diagnostics."""
        
        self.regions: Dict[str, RegionalDiagnostic] = {}
        
        # Riyadh Region
        self.regions['Riyadh'] = RegionalDiagnostic(
            region_name="Riyadh",
            region_name_ar="الرياض",
            area_km2=404240,
            population_2025=8.9,
            population_2030_projected=10.5,
            urbanization_rate=95.0,
            primary_city="Riyadh City",
            secondary_cities=["Al-Kharj", "Al-Majma'ah", "Al-Dawadmi", "Wadi al-Dawasir"],
            settlement_count=450,
            urban_primacy_ratio=0.92,
            gdp_contribution_pct=50.0,
            gdp_per_capita_sar=145000,
            dominant_sectors=["Government", "Finance", "Real Estate", "Retail"],
            emerging_sectors=["Technology", "Entertainment", "Tourism"],
            employment_rate=94.5,
            competitive_advantages=[
                "National capital with government headquarters",
                "Largest financial center in the region",
                "Major international airport hub",
                "Headquarters relocation policy driving growth",
                "Largest consumer market"
            ],
            strategic_assets=[
                "King Khalid International Airport",
                "Riyadh Metro (under construction)",
                "King Abdullah Financial District",
                "Diriyah UNESCO Heritage Site",
                "Multiple universities and research centers"
            ],
            water_availability="critical",
            water_sources=["Groundwater (depleting)", "Desalination (piped)", "Treated wastewater"],
            annual_water_demand_mcm=2500,
            annual_water_supply_mcm=2200,
            environmental_sensitivity="medium",
            protected_areas_pct=2.5,
            climate_risks=["Extreme heat", "Dust storms", "Flash floods"],
            development_potential="high",
            key_constraints=["Water scarcity", "Urban sprawl", "Traffic congestion", "Air quality"],
            priority_investments=["Metro completion", "Water infrastructure", "Green corridors", "Social infrastructure"],
            giga_projects=["Diriyah Gate", "Qiddiya", "King Salman Park", "Sports Boulevard", "Riyadh Green"],
            vision2030_role="National capital, economic powerhouse, quality of life exemplar"
        )
        
        # Makkah Region
        self.regions['Makkah'] = RegionalDiagnostic(
            region_name="Makkah",
            region_name_ar="مكة المكرمة",
            area_km2=153128,
            population_2025=9.1,
            population_2030_projected=10.2,
            urbanization_rate=96.0,
            primary_city="Jeddah",
            secondary_cities=["Makkah", "Taif", "Rabigh", "Al Qunfudhah"],
            settlement_count=380,
            urban_primacy_ratio=0.48,  # Dual primacy with Makkah city
            gdp_contribution_pct=21.0,
            gdp_per_capita_sar=85000,
            dominant_sectors=["Religious Tourism", "Trade", "Logistics", "Real Estate"],
            emerging_sectors=["Manufacturing", "Creative Industries", "Healthcare"],
            employment_rate=92.0,
            competitive_advantages=[
                "Holiest city in Islam (Makkah)",
                "Major Red Sea port (Jeddah)",
                "Gateway for Hajj and Umrah",
                "Established commercial center",
                "International airport"
            ],
            strategic_assets=[
                "Masjid al-Haram (Grand Mosque)",
                "King Abdulaziz International Airport",
                "Jeddah Islamic Port",
                "King Abdullah Economic City",
                "Historic Jeddah (UNESCO)"
            ],
            water_availability="scarce",
            water_sources=["Desalination", "Groundwater (limited)", "Treated wastewater"],
            annual_water_demand_mcm=1800,
            annual_water_supply_mcm=1700,
            environmental_sensitivity="high",
            protected_areas_pct=3.0,
            climate_risks=["Extreme heat", "Flash floods (Jeddah)", "Sea level rise"],
            development_potential="high",
            key_constraints=["Water scarcity", "Hajj peak demand", "Coastal development pressure", "Historic preservation"],
            priority_investments=["Flood protection", "Public transport", "Pilgrim facilities", "Waterfront development"],
            giga_projects=["Red Sea Project (partial)", "Jeddah Central", "Obhur Development"],
            vision2030_role="Religious and cultural tourism capital, Red Sea gateway"
        )
        
        # Eastern Province
        self.regions['Eastern Province'] = RegionalDiagnostic(
            region_name="Eastern Province",
            region_name_ar="المنطقة الشرقية",
            area_km2=672522,
            population_2025=5.3,
            population_2030_projected=6.0,
            urbanization_rate=90.0,
            primary_city="Dammam",
            secondary_cities=["Al Khobar", "Dhahran", "Al Jubail", "Al Hofuf", "Qatif"],
            settlement_count=280,
            urban_primacy_ratio=0.35,  # Polycentric urban structure
            gdp_contribution_pct=25.0,
            gdp_per_capita_sar=175000,
            dominant_sectors=["Oil & Gas", "Petrochemicals", "Manufacturing"],
            emerging_sectors=["Technology", "Tourism", "Logistics"],
            employment_rate=95.0,
            competitive_advantages=[
                "Center of oil and gas industry",
                "Largest industrial base",
                "Strategic Gulf location",
                "Established expat community",
                "Strong technical workforce"
            ],
            strategic_assets=[
                "Saudi Aramco headquarters",
                "Jubail Industrial City",
                "King Fahd International Airport",
                "Multiple ports",
                "KFUPM research university"
            ],
            water_availability="moderate",
            water_sources=["Desalination", "Groundwater", "Industrial recycling"],
            annual_water_demand_mcm=1500,
            annual_water_supply_mcm=1600,
            environmental_sensitivity="high",
            protected_areas_pct=5.0,
            climate_risks=["Sea level rise", "Industrial pollution", "Extreme heat"],
            development_potential="high",
            key_constraints=["Oil dependency transition", "Environmental remediation", "Industrial diversification"],
            priority_investments=["Industrial diversification", "Tourism infrastructure", "Environmental cleanup", "Rail connectivity"],
            giga_projects=["King Salman Energy Park (SPARK)", "Ras Al-Khair expansion"],
            vision2030_role="Industrial powerhouse, energy transition leader, Gulf gateway"
        )
        
        # Madinah Region
        self.regions['Madinah'] = RegionalDiagnostic(
            region_name="Madinah",
            region_name_ar="المدينة المنورة",
            area_km2=151990,
            population_2025=2.3,
            population_2030_projected=2.7,
            urbanization_rate=85.0,
            primary_city="Madinah",
            secondary_cities=["Yanbu", "Al-Ula", "Khaybar"],
            settlement_count=180,
            urban_primacy_ratio=0.75,
            gdp_contribution_pct=4.5,
            gdp_per_capita_sar=72000,
            dominant_sectors=["Religious Tourism", "Petrochemicals (Yanbu)", "Agriculture"],
            emerging_sectors=["Cultural Tourism", "Mining", "Renewable Energy"],
            employment_rate=91.0,
            competitive_advantages=[
                "Second holiest city in Islam",
                "Major pilgrimage destination",
                "Yanbu industrial city and port",
                "AlUla heritage and natural landscapes",
                "Date palm production"
            ],
            strategic_assets=[
                "Prophet's Mosque",
                "AlUla UNESCO World Heritage",
                "Yanbu Industrial City",
                "Prince Mohammad Bin Abdulaziz Airport",
                "Haramain High Speed Rail station"
            ],
            water_availability="scarce",
            water_sources=["Desalination (Yanbu)", "Groundwater", "Treated wastewater"],
            annual_water_demand_mcm=600,
            annual_water_supply_mcm=550,
            environmental_sensitivity="high",
            protected_areas_pct=8.0,
            climate_risks=["Extreme heat", "Flash floods", "Desertification"],
            development_potential="high",
            key_constraints=["Water scarcity", "Heritage preservation requirements", "Infrastructure gaps"],
            priority_investments=["AlUla development", "Water infrastructure", "Tourism facilities", "Transport connectivity"],
            giga_projects=["AlUla Development", "Yanbu expansion"],
            vision2030_role="Religious tourism, cultural heritage showcase, industrial diversification"
        )
        
        # Tabuk Region
        self.regions['Tabuk'] = RegionalDiagnostic(
            region_name="Tabuk",
            region_name_ar="تبوك",
            area_km2=139000,
            population_2025=1.0,
            population_2030_projected=1.5,
            urbanization_rate=78.0,
            primary_city="Tabuk City",
            secondary_cities=["Haql", "Duba", "Umluj", "Al Wajh"],
            settlement_count=120,
            urban_primacy_ratio=0.80,
            gdp_contribution_pct=1.5,
            gdp_per_capita_sar=55000,
            dominant_sectors=["Agriculture", "Military", "Trade"],
            emerging_sectors=["Tourism", "Renewable Energy", "Technology"],
            employment_rate=88.0,
            competitive_advantages=[
                "NEOM giga-project location",
                "Red Sea coastline",
                "Mild climate (highlands)",
                "Agricultural potential",
                "Strategic border location"
            ],
            strategic_assets=[
                "NEOM site",
                "Red Sea coast",
                "Tabuk Regional Airport",
                "Agricultural zones",
                "Military installations"
            ],
            water_availability="scarce",
            water_sources=["Groundwater", "Desalination (NEOM)", "Springs (limited)"],
            annual_water_demand_mcm=400,
            annual_water_supply_mcm=350,
            environmental_sensitivity="high",
            protected_areas_pct=12.0,
            climate_risks=["Flash floods", "Desertification", "Seismic activity"],
            development_potential="very high",
            key_constraints=["Remote location", "Infrastructure gaps", "Labor availability", "Environmental sensitivity"],
            priority_investments=["NEOM infrastructure", "Transport connectivity", "Water desalination", "Skills development"],
            giga_projects=["NEOM (The Line, Trojena, Oxagon, Sindalah)"],
            vision2030_role="Future city of tomorrow, tourism destination, renewable energy hub"
        )
        
        # Asir Region
        self.regions['Asir'] = RegionalDiagnostic(
            region_name="Asir",
            region_name_ar="عسير",
            area_km2=81000,
            population_2025=2.3,
            population_2030_projected=2.6,
            urbanization_rate=65.0,
            primary_city="Abha",
            secondary_cities=["Khamis Mushait", "Bisha", "Al-Namas"],
            settlement_count=350,
            urban_primacy_ratio=0.55,
            gdp_contribution_pct=2.5,
            gdp_per_capita_sar=48000,
            dominant_sectors=["Agriculture", "Tourism", "Military"],
            emerging_sectors=["Eco-tourism", "Coffee cultivation", "Handicrafts"],
            employment_rate=89.0,
            competitive_advantages=[
                "Cooler highland climate",
                "Scenic mountain landscapes",
                "Traditional villages and heritage",
                "Agricultural diversity",
                "Domestic tourism destination"
            ],
            strategic_assets=[
                "Asir National Park",
                "Traditional villages (Rijal Alma)",
                "Abha Regional Airport",
                "Agricultural terraces",
                "Cable cars and tourism infrastructure"
            ],
            water_availability="moderate",
            water_sources=["Rainfall", "Springs", "Dams", "Groundwater"],
            annual_water_demand_mcm=350,
            annual_water_supply_mcm=400,
            environmental_sensitivity="high",
            protected_areas_pct=15.0,
            climate_risks=["Landslides", "Forest fires", "Flash floods"],
            development_potential="medium",
            key_constraints=["Terrain challenges", "Infrastructure access", "Heritage preservation", "Seasonal demand"],
            priority_investments=["Tourism infrastructure", "Road improvements", "Heritage preservation", "Agricultural support"],
            giga_projects=["Asir Development"],
            vision2030_role="Domestic tourism destination, agricultural heritage, eco-tourism model"
        )
        
        # Al-Qassim Region
        self.regions['Al-Qassim'] = RegionalDiagnostic(
            region_name="Al-Qassim",
            region_name_ar="القصيم",
            area_km2=65000,
            population_2025=1.5,
            population_2030_projected=1.7,
            urbanization_rate=75.0,
            primary_city="Buraydah",
            secondary_cities=["Unayzah", "Al-Rass", "Al-Badai'a"],
            settlement_count=220,
            urban_primacy_ratio=0.65,
            gdp_contribution_pct=2.0,
            gdp_per_capita_sar=52000,
            dominant_sectors=["Agriculture", "Trade", "Education"],
            emerging_sectors=["Food processing", "Logistics", "Renewable energy"],
            employment_rate=90.0,
            competitive_advantages=[
                "Date palm capital of Saudi Arabia",
                "Agricultural productivity center",
                "Central geographic location",
                "Strong educational institutions",
                "Traditional trading hub"
            ],
            strategic_assets=[
                "Date farms and processing",
                "Qassim University",
                "Central location on transport routes",
                "Agricultural research centers",
                "Regional markets"
            ],
            water_availability="critical",
            water_sources=["Groundwater (rapidly depleting)", "Treated wastewater"],
            annual_water_demand_mcm=2000,
            annual_water_supply_mcm=1500,
            environmental_sensitivity="medium",
            protected_areas_pct=3.0,
            climate_risks=["Groundwater depletion", "Desertification", "Extreme heat"],
            development_potential="medium",
            key_constraints=["CRITICAL water depletion", "Agricultural transition needs", "Limited diversification"],
            priority_investments=["Water efficiency", "Agricultural modernization", "Food processing", "Solar energy"],
            giga_projects=[],
            vision2030_role="Agricultural innovation center, food security contributor"
        )
        
        # Additional regions (abbreviated for brevity but complete)
        self.regions['Hail'] = RegionalDiagnostic(
            region_name="Hail",
            region_name_ar="حائل",
            area_km2=103887,
            population_2025=0.75,
            population_2030_projected=0.85,
            urbanization_rate=70.0,
            primary_city="Hail City",
            secondary_cities=["Baqaa", "Al-Ghazalah"],
            settlement_count=150,
            urban_primacy_ratio=0.85,
            gdp_contribution_pct=1.0,
            gdp_per_capita_sar=48000,
            dominant_sectors=["Agriculture", "Trade", "Government"],
            emerging_sectors=["Mining", "Renewable energy", "Eco-tourism"],
            employment_rate=88.0,
            competitive_advantages=["Agricultural potential", "Mining resources", "Cultural heritage", "Central location"],
            strategic_assets=["Rock art sites", "Agricultural zones", "Mining deposits"],
            water_availability="scarce",
            water_sources=["Groundwater", "Dams"],
            annual_water_demand_mcm=500,
            annual_water_supply_mcm=400,
            environmental_sensitivity="medium",
            protected_areas_pct=5.0,
            climate_risks=["Desertification", "Groundwater depletion"],
            development_potential="medium",
            key_constraints=["Water scarcity", "Remote location", "Small market size"],
            priority_investments=["Mining development", "Agricultural efficiency", "Tourism"],
            giga_projects=[],
            vision2030_role="Agricultural and mining development"
        )
        
        # Northern Borders
        self.regions['Northern Borders'] = RegionalDiagnostic(
            region_name="Northern Borders",
            region_name_ar="الحدود الشمالية",
            area_km2=111797,
            population_2025=0.42,
            population_2030_projected=0.50,
            urbanization_rate=65.0,
            primary_city="Arar",
            secondary_cities=["Rafha", "Turaif"],
            settlement_count=80,
            urban_primacy_ratio=0.75,
            gdp_contribution_pct=0.8,
            gdp_per_capita_sar=70000,
            dominant_sectors=["Mining (phosphate)", "Government", "Trade"],
            emerging_sectors=["Renewable energy", "Industrial processing"],
            employment_rate=85.0,
            competitive_advantages=["Phosphate reserves", "Solar potential", "Border trade"],
            strategic_assets=["Waad Al-Shamal Phosphate City", "Solar irradiance"],
            water_availability="scarce",
            water_sources=["Groundwater", "Desalination (limited)"],
            annual_water_demand_mcm=200,
            annual_water_supply_mcm=180,
            environmental_sensitivity="low",
            protected_areas_pct=2.0,
            climate_risks=["Extreme temperatures", "Dust storms"],
            development_potential="high",
            key_constraints=["Remote location", "Small population", "Harsh climate"],
            priority_investments=["Mining expansion", "Renewable energy", "Infrastructure"],
            giga_projects=["Waad Al-Shamal expansion"],
            vision2030_role="Mining and renewable energy hub"
        )
        
        # Jazan
        self.regions['Jazan'] = RegionalDiagnostic(
            region_name="Jazan",
            region_name_ar="جازان",
            area_km2=13457,
            population_2025=1.7,
            population_2030_projected=1.9,
            urbanization_rate=55.0,
            primary_city="Jazan City",
            secondary_cities=["Sabya", "Abu Arish", "Farasan Islands"],
            settlement_count=250,
            urban_primacy_ratio=0.50,
            gdp_contribution_pct=1.2,
            gdp_per_capita_sar=32000,
            dominant_sectors=["Agriculture", "Fishing", "Industry"],
            emerging_sectors=["Tourism", "Coffee production", "Renewable energy"],
            employment_rate=82.0,
            competitive_advantages=["Tropical climate", "Agricultural diversity", "Fishing", "Farasan Islands"],
            strategic_assets=["Jazan Economic City", "Farasan Marine Reserve", "Coffee plantations"],
            water_availability="moderate",
            water_sources=["Rainfall", "Dams", "Groundwater"],
            annual_water_demand_mcm=400,
            annual_water_supply_mcm=450,
            environmental_sensitivity="high",
            protected_areas_pct=10.0,
            climate_risks=["Flooding", "Tropical storms", "Sea level rise"],
            development_potential="medium",
            key_constraints=["Infrastructure gaps", "Education levels", "Economic diversification"],
            priority_investments=["Economic city development", "Tourism", "Agricultural modernization"],
            giga_projects=["Jazan Economic City"],
            vision2030_role="Economic diversification, eco-tourism, agricultural exports"
        )
        
        # Najran
        self.regions['Najran'] = RegionalDiagnostic(
            region_name="Najran",
            region_name_ar="نجران",
            area_km2=149511,
            population_2025=0.62,
            population_2030_projected=0.70,
            urbanization_rate=60.0,
            primary_city="Najran City",
            secondary_cities=["Sharurah", "Hubuna"],
            settlement_count=100,
            urban_primacy_ratio=0.80,
            gdp_contribution_pct=0.6,
            gdp_per_capita_sar=38000,
            dominant_sectors=["Agriculture", "Government", "Trade"],
            emerging_sectors=["Mining", "Tourism (heritage)"],
            employment_rate=84.0,
            competitive_advantages=["Archaeological heritage", "Agricultural oases", "Border trade"],
            strategic_assets=["Ukhdood archaeological site", "Traditional architecture", "Dam systems"],
            water_availability="moderate",
            water_sources=["Dams", "Groundwater", "Seasonal rainfall"],
            annual_water_demand_mcm=300,
            annual_water_supply_mcm=320,
            environmental_sensitivity="medium",
            protected_areas_pct=4.0,
            climate_risks=["Border security", "Flash floods"],
            development_potential="low",
            key_constraints=["Border location", "Remote access", "Small economy"],
            priority_investments=["Heritage tourism", "Agricultural efficiency", "Infrastructure"],
            giga_projects=[],
            vision2030_role="Heritage preservation, agricultural sustainability"
        )
        
        # Al-Baha
        self.regions['Al-Baha'] = RegionalDiagnostic(
            region_name="Al-Baha",
            region_name_ar="الباحة",
            area_km2=9921,
            population_2025=0.50,
            population_2030_projected=0.55,
            urbanization_rate=50.0,
            primary_city="Al-Baha City",
            secondary_cities=["Baljurashi", "Al-Mandaq"],
            settlement_count=180,
            urban_primacy_ratio=0.60,
            gdp_contribution_pct=0.4,
            gdp_per_capita_sar=35000,
            dominant_sectors=["Agriculture", "Government", "Tourism"],
            emerging_sectors=["Eco-tourism", "Honey production", "Handicrafts"],
            employment_rate=85.0,
            competitive_advantages=["Scenic mountains", "Cool climate", "Traditional villages", "Honey production"],
            strategic_assets=["Thee Ain heritage village", "Raghadan Forest", "Traditional terraces"],
            water_availability="moderate",
            water_sources=["Rainfall", "Springs", "Dams"],
            annual_water_demand_mcm=100,
            annual_water_supply_mcm=120,
            environmental_sensitivity="high",
            protected_areas_pct=12.0,
            climate_risks=["Forest fires", "Landslides", "Flash floods"],
            development_potential="low",
            key_constraints=["Small size", "Terrain challenges", "Limited infrastructure"],
            priority_investments=["Tourism development", "Heritage preservation", "Road improvement"],
            giga_projects=[],
            vision2030_role="Eco-tourism, heritage preservation"
        )
        
        # Al-Jouf
        self.regions['Al-Jouf'] = RegionalDiagnostic(
            region_name="Al-Jouf",
            region_name_ar="الجوف",
            area_km2=100212,
            population_2025=0.55,
            population_2030_projected=0.65,
            urbanization_rate=68.0,
            primary_city="Sakaka",
            secondary_cities=["Dumat Al-Jandal", "Qurayyat"],
            settlement_count=90,
            urban_primacy_ratio=0.75,
            gdp_contribution_pct=0.8,
            gdp_per_capita_sar=55000,
            dominant_sectors=["Agriculture (olives)", "Government", "Trade"],
            emerging_sectors=["Renewable energy", "Mining", "Tourism"],
            employment_rate=87.0,
            competitive_advantages=["Olive production capital", "Solar potential", "Archaeological sites", "Border trade"],
            strategic_assets=["Olive groves", "Dumat Al-Jandal wind farm", "Archaeological sites"],
            water_availability="scarce",
            water_sources=["Groundwater", "Desalination (limited)"],
            annual_water_demand_mcm=600,
            annual_water_supply_mcm=500,
            environmental_sensitivity="medium",
            protected_areas_pct=4.0,
            climate_risks=["Groundwater depletion", "Extreme temperatures", "Dust storms"],
            development_potential="medium",
            key_constraints=["Water scarcity", "Remote location", "Small market"],
            priority_investments=["Renewable energy", "Agricultural efficiency", "Tourism"],
            giga_projects=[],
            vision2030_role="Renewable energy hub, agricultural innovation"
        )
    
    def get_region(self, region_name: str) -> Optional[RegionalDiagnostic]:
        """Get diagnostic for a specific region."""
        return self.regions.get(region_name)
    
    def get_all_regions(self) -> Dict[str, RegionalDiagnostic]:
        """Get all regional diagnostics."""
        return self.regions
    
    def get_regions_by_water_status(self, status: str) -> List[RegionalDiagnostic]:
        """Get regions by water availability status."""
        return [r for r in self.regions.values() if r.water_availability == status]
    
    def get_regions_by_potential(self, potential: str) -> List[RegionalDiagnostic]:
        """Get regions by development potential."""
        return [r for r in self.regions.values() if r.development_potential == potential]
    
    def calculate_national_aggregates(self) -> Dict[str, Any]:
        """Calculate national aggregate statistics."""
        total_pop_2025 = sum(r.population_2025 for r in self.regions.values())
        total_pop_2030 = sum(r.population_2030_projected for r in self.regions.values())
        total_water_demand = sum(r.annual_water_demand_mcm for r in self.regions.values())
        total_water_supply = sum(r.annual_water_supply_mcm for r in self.regions.values())
        
        return {
            "total_population_2025_millions": total_pop_2025,
            "total_population_2030_millions": total_pop_2030,
            "population_growth_rate": ((total_pop_2030 / total_pop_2025) ** 0.2 - 1) * 100,
            "water_balance": {
                "total_demand_mcm": total_water_demand,
                "total_supply_mcm": total_water_supply,
                "deficit_mcm": max(0, total_water_demand - total_water_supply),
                "deficit_regions": [r.region_name for r in self.regions.values() 
                                   if r.annual_water_demand_mcm > r.annual_water_supply_mcm]
            },
            "regional_concentration": {
                "top_3_gdp_share": 96.0,  # Riyadh + Eastern + Makkah
                "top_3_population_share": 64.0
            },
            "giga_project_regions": [r.region_name for r in self.regions.values() if r.giga_projects]
        }


# =============================================================================
# CONFLICT AND SYNERGY MAPS
# =============================================================================

class ConflictSynergyMapper:
    """
    Generates spatial conflict and synergy map layers.
    """
    
    def __init__(self, sectoral: SectoralAnalyzer, regional: RegionalDiagnosticsAnalyzer):
        """Initialize with sectoral and regional data."""
        self.sectoral = sectoral
        self.regional = regional
        self._generate_map_layers()
        logger.info("Conflict and Synergy Mapper initialized")
    
    def _generate_map_layers(self):
        """Generate all map layers."""
        
        self.conflict_layers: List[ConflictMapLayer] = []
        self.synergy_layers: List[ConflictMapLayer] = []
        
        # CONFLICT LAYERS
        
        # Industrial-Residential Conflicts
        self.conflict_layers.append(ConflictMapLayer(
            layer_name="Industrial-Residential Conflict Zones",
            layer_type="conflict",
            description="Areas where industrial development creates pollution and noise affecting residential areas",
            affected_regions=["Riyadh", "Eastern Province", "Makkah", "Madinah"],
            severity="high",
            land_uses_involved=["industrial", "residential"],
            area_affected_km2=850,
            mitigation_priority="critical",
            visualization_style={
                "fill_color": "#FF4444",
                "opacity": 0.6,
                "border_color": "#CC0000",
                "pattern": "diagonal_stripes"
            }
        ))
        
        # Water Competition (Agriculture vs Urban)
        self.conflict_layers.append(ConflictMapLayer(
            layer_name="Water Competition Zones",
            layer_type="conflict",
            description="Areas where agricultural and urban water demands exceed sustainable supply",
            affected_regions=["Al-Qassim", "Riyadh", "Al-Jouf", "Hail", "Tabuk"],
            severity="critical",
            land_uses_involved=["agricultural", "residential", "industrial"],
            area_affected_km2=25000,
            mitigation_priority="critical",
            visualization_style={
                "fill_color": "#0066CC",
                "opacity": 0.5,
                "border_color": "#003366",
                "pattern": "water_drops"
            }
        ))
        
        # Environmental Pressure Zones
        self.conflict_layers.append(ConflictMapLayer(
            layer_name="Environmental Pressure Zones",
            layer_type="conflict",
            description="Areas where development pressure threatens environmental protection areas",
            affected_regions=["Tabuk", "Asir", "Jazan", "Eastern Province", "Madinah"],
            severity="high",
            land_uses_involved=["environmental_protection", "tourism", "industrial", "mining"],
            area_affected_km2=15000,
            mitigation_priority="high",
            visualization_style={
                "fill_color": "#228B22",
                "opacity": 0.5,
                "border_color": "#006400",
                "pattern": "tree_icons"
            }
        ))
        
        # Mining Impact Zones
        self.conflict_layers.append(ConflictMapLayer(
            layer_name="Mining Impact Zones",
            layer_type="conflict",
            description="Areas affected by mining operations requiring environmental management",
            affected_regions=["Northern Borders", "Madinah", "Tabuk", "Najran"],
            severity="medium",
            land_uses_involved=["mining", "agricultural", "environmental_protection"],
            area_affected_km2=8000,
            mitigation_priority="high",
            visualization_style={
                "fill_color": "#8B4513",
                "opacity": 0.5,
                "border_color": "#5D3A1A",
                "pattern": "mining_icons"
            }
        ))
        
        # Coastal Development Pressure
        self.conflict_layers.append(ConflictMapLayer(
            layer_name="Coastal Development Pressure",
            layer_type="conflict",
            description="Coastal areas facing competing demands from tourism, industry, and conservation",
            affected_regions=["Tabuk", "Makkah", "Eastern Province", "Jazan"],
            severity="high",
            land_uses_involved=["tourism", "industrial", "environmental_protection", "residential"],
            area_affected_km2=3000,
            mitigation_priority="critical",
            visualization_style={
                "fill_color": "#4169E1",
                "opacity": 0.5,
                "border_color": "#000080",
                "pattern": "wave_pattern"
            }
        ))
        
        # SYNERGY LAYERS
        
        # Logistics Corridors
        self.synergy_layers.append(ConflictMapLayer(
            layer_name="Integrated Logistics Corridors",
            layer_type="synergy",
            description="Transport corridors supporting multiple economic sectors",
            affected_regions=["Riyadh", "Eastern Province", "Makkah", "Madinah", "Tabuk"],
            severity="high",  # High positive impact
            land_uses_involved=["infrastructure", "industrial", "logistics"],
            area_affected_km2=5000,
            mitigation_priority="investment",
            visualization_style={
                "fill_color": "#32CD32",
                "opacity": 0.6,
                "border_color": "#228B22",
                "pattern": "arrows"
            }
        ))
        
        # Innovation Clusters
        self.synergy_layers.append(ConflictMapLayer(
            layer_name="Innovation and Technology Clusters",
            layer_type="synergy",
            description="Areas with synergies between technology, education, and industry",
            affected_regions=["Riyadh", "Eastern Province", "Tabuk"],
            severity="high",
            land_uses_involved=["technology", "education", "industrial"],
            area_affected_km2=500,
            mitigation_priority="investment",
            visualization_style={
                "fill_color": "#9370DB",
                "opacity": 0.6,
                "border_color": "#6A0DAD",
                "pattern": "hexagons"
            }
        ))
        
        # Eco-Tourism Zones
        self.synergy_layers.append(ConflictMapLayer(
            layer_name="Eco-Tourism Development Zones",
            layer_type="synergy",
            description="Areas where tourism and environmental protection create mutual benefits",
            affected_regions=["Tabuk", "Asir", "Madinah", "Jazan", "Al-Baha"],
            severity="medium",
            land_uses_involved=["tourism", "environmental_protection"],
            area_affected_km2=12000,
            mitigation_priority="investment",
            visualization_style={
                "fill_color": "#90EE90",
                "opacity": 0.5,
                "border_color": "#32CD32",
                "pattern": "leaf_icons"
            }
        ))
        
        # Renewable Energy Zones
        self.synergy_layers.append(ConflictMapLayer(
            layer_name="Renewable Energy Development Zones",
            layer_type="synergy",
            description="Areas optimal for solar and wind energy with minimal conflicts",
            affected_regions=["Tabuk", "Al-Jouf", "Northern Borders", "Hail"],
            severity="high",
            land_uses_involved=["renewable_energy", "industrial"],
            area_affected_km2=20000,
            mitigation_priority="investment",
            visualization_style={
                "fill_color": "#FFD700",
                "opacity": 0.5,
                "border_color": "#FFA500",
                "pattern": "sun_icons"
            }
        ))
        
        # Agrivoltaics Potential Zones
        self.synergy_layers.append(ConflictMapLayer(
            layer_name="Agrivoltaics Potential Zones",
            layer_type="synergy",
            description="Areas where solar energy and agriculture can be combined",
            affected_regions=["Al-Qassim", "Al-Jouf", "Hail", "Riyadh"],
            severity="medium",
            land_uses_involved=["renewable_energy", "agricultural"],
            area_affected_km2=8000,
            mitigation_priority="investment",
            visualization_style={
                "fill_color": "#ADFF2F",
                "opacity": 0.5,
                "border_color": "#6B8E23",
                "pattern": "solar_crop"
            }
        ))
    
    def get_all_conflict_layers(self) -> List[ConflictMapLayer]:
        """Get all conflict map layers."""
        return self.conflict_layers
    
    def get_all_synergy_layers(self) -> List[ConflictMapLayer]:
        """Get all synergy map layers."""
        return self.synergy_layers
    
    def get_layers_by_region(self, region: str) -> Dict[str, List[ConflictMapLayer]]:
        """Get all layers affecting a specific region."""
        conflicts = [l for l in self.conflict_layers if region in l.affected_regions]
        synergies = [l for l in self.synergy_layers if region in l.affected_regions]
        return {"conflicts": conflicts, "synergies": synergies}
    
    def get_critical_conflicts(self) -> List[ConflictMapLayer]:
        """Get critical priority conflicts."""
        return [l for l in self.conflict_layers if l.mitigation_priority == "critical"]
    
    def to_geojson_style_dict(self) -> Dict[str, Any]:
        """Export layer definitions in GeoJSON-compatible format."""
        return {
            "conflict_layers": [
                {
                    "id": f"conflict_{i}",
                    "name": l.layer_name,
                    "type": l.layer_type,
                    "description": l.description,
                    "regions": l.affected_regions,
                    "severity": l.severity,
                    "land_uses": l.land_uses_involved,
                    "area_km2": l.area_affected_km2,
                    "priority": l.mitigation_priority,
                    "style": l.visualization_style
                }
                for i, l in enumerate(self.conflict_layers)
            ],
            "synergy_layers": [
                {
                    "id": f"synergy_{i}",
                    "name": l.layer_name,
                    "type": l.layer_type,
                    "description": l.description,
                    "regions": l.affected_regions,
                    "impact": l.severity,
                    "land_uses": l.land_uses_involved,
                    "area_km2": l.area_affected_km2,
                    "action": l.mitigation_priority,
                    "style": l.visualization_style
                }
                for i, l in enumerate(self.synergy_layers)
            ]
        }


# =============================================================================
# OPTIMIZATION PLAYBOOK
# =============================================================================

class OptimizationPlaybook:
    """
    Generates corrective measures and optimization playbook.
    """
    
    def __init__(self):
        """Initialize playbook with corrective measures."""
        self._generate_measures()
        logger.info("Optimization Playbook initialized with corrective measures")
    
    def _generate_measures(self):
        """Generate all corrective measures."""
        
        self.measures: List[CorrectiveMeasure] = []
        
        # CRITICAL MEASURES
        
        # Water Security
        self.measures.append(CorrectiveMeasure(
            measure_id="CM-001",
            title="Agricultural Water Demand Reduction Program",
            conflict_addressed="Water Competition (Agriculture vs Urban)",
            description="""Mandatory program to reduce agricultural water consumption by 40% through:
            - Phase-out of water-intensive crops (wheat, alfalfa)
            - Mandatory smart irrigation systems
            - Treated wastewater reuse for irrigation
            - Water pricing reform for agricultural sector""",
            measure_type="regulatory",
            target_regions=["Al-Qassim", "Riyadh", "Al-Jouf", "Hail"],
            implementation_timeline="immediate",
            estimated_cost_sar_million=5000,
            expected_benefit="6,000 MCM/year water savings by 2030",
            responsible_agency="Ministry of Environment, Water and Agriculture",
            kpis=[
                "Agricultural water consumption (MCM/year)",
                "Smart irrigation adoption rate (%)",
                "Treated wastewater reuse volume (MCM/year)",
                "Groundwater level monitoring"
            ],
            priority="critical"
        ))
        
        # Industrial-Residential Separation
        self.measures.append(CorrectiveMeasure(
            measure_id="CM-002",
            title="Industrial Zone Relocation and Buffer Program",
            conflict_addressed="Industrial-Residential Conflicts",
            description="""Systematic relocation of incompatible industries and establishment of buffers:
            - Mandatory relocation of heavy industry from mixed zones
            - Establishment of 500m minimum buffer zones
            - Green corridor requirements between zones
            - Air quality monitoring network expansion""",
            measure_type="regulatory",
            target_regions=["Riyadh", "Eastern Province", "Makkah"],
            implementation_timeline="short-term",
            estimated_cost_sar_million=8000,
            expected_benefit="50% reduction in residential exposure to industrial pollution",
            responsible_agency="Ministry of Municipal and Rural Affairs",
            kpis=[
                "Number of industries relocated",
                "Buffer zone compliance rate (%)",
                "Air quality index in residential areas",
                "Noise level compliance (%)"
            ],
            priority="critical"
        ))
        
        # Coastal Zone Management
        self.measures.append(CorrectiveMeasure(
            measure_id="CM-003",
            title="Integrated Coastal Zone Management Framework",
            conflict_addressed="Coastal Development Pressure",
            description="""Comprehensive coastal zone management including:
            - Mandatory setback requirements (200m minimum)
            - Marine spatial planning for Red Sea and Gulf
            - Tourism-conservation zoning standards
            - Ecosystem-based management approach""",
            measure_type="regulatory",
            target_regions=["Tabuk", "Makkah", "Eastern Province", "Jazan"],
            implementation_timeline="immediate",
            estimated_cost_sar_million=2000,
            expected_benefit="Protection of 80% of critical coastal ecosystems",
            responsible_agency="National Center for Environmental Compliance",
            kpis=[
                "Protected coastal area (km)",
                "Setback compliance rate (%)",
                "Marine biodiversity index",
                "Coastal erosion rates"
            ],
            priority="critical"
        ))
        
        # HIGH PRIORITY MEASURES
        
        # Mining Rehabilitation
        self.measures.append(CorrectiveMeasure(
            measure_id="CM-004",
            title="Mining Rehabilitation and Community Protection Program",
            conflict_addressed="Mining Impact Zones",
            description="""Comprehensive mining impact management:
            - Mandatory rehabilitation bonds (100% of estimated costs)
            - Progressive land reclamation requirements
            - Community benefit agreements
            - Environmental monitoring requirements""",
            measure_type="regulatory",
            target_regions=["Northern Borders", "Madinah", "Tabuk", "Najran"],
            implementation_timeline="short-term",
            estimated_cost_sar_million=3000,
            expected_benefit="100% of mining areas with rehabilitation plans",
            responsible_agency="Ministry of Industry and Mineral Resources",
            kpis=[
                "Rehabilitation bond coverage (%)",
                "Reclaimed land area (km²)",
                "Community benefit payments (SAR)",
                "Environmental compliance rate (%)"
            ],
            priority="high"
        ))
        
        # Environmental Protection
        self.measures.append(CorrectiveMeasure(
            measure_id="CM-005",
            title="Protected Area Expansion and Enforcement",
            conflict_addressed="Environmental Pressure Zones",
            description="""Accelerated protected area expansion to meet 30x30 commitment:
            - Designate new protected areas (25% of land by 2030)
            - Enhanced enforcement capacity
            - Wildlife corridor establishment
            - Biodiversity offset requirements for development""",
            measure_type="investment",
            target_regions=["All regions"],
            implementation_timeline="medium-term",
            estimated_cost_sar_million=10000,
            expected_benefit="25% land protection, 30% marine protection by 2030",
            responsible_agency="National Center for Wildlife",
            kpis=[
                "Protected area coverage (%)",
                "Enforcement actions per year",
                "Wildlife population indices",
                "Biodiversity offset area (km²)"
            ],
            priority="high"
        ))
        
        # Renewable Energy Zoning
        self.measures.append(CorrectiveMeasure(
            measure_id="CM-006",
            title="Renewable Energy Zone Designation Program",
            conflict_addressed="Energy vs Agriculture Land Competition",
            description="""Strategic designation of renewable energy zones:
            - Priority zoning on degraded/non-agricultural land
            - Streamlined permitting in designated zones
            - Agrivoltaics incentive program
            - Grid infrastructure co-investment""",
            measure_type="planning",
            target_regions=["Tabuk", "Al-Jouf", "Northern Borders", "Hail"],
            implementation_timeline="short-term",
            estimated_cost_sar_million=1500,
            expected_benefit="50 GW renewable capacity with minimal land conflicts",
            responsible_agency="Ministry of Energy",
            kpis=[
                "Designated RE zone area (km²)",
                "Permitting time in zones (days)",
                "Agrivoltaics installed capacity (MW)",
                "Agricultural land conversion avoided (km²)"
            ],
            priority="high"
        ))
        
        # MEDIUM PRIORITY MEASURES
        
        # Transit-Oriented Development
        self.measures.append(CorrectiveMeasure(
            measure_id="CM-007",
            title="Transit-Oriented Development Zones",
            conflict_addressed="Urban Sprawl and Transport Conflicts",
            description="""Establishment of TOD zones around all major transit stations:
            - Mandatory mixed-use zoning within 800m of stations
            - Density bonuses for TOD-compliant development
            - Parking maximums in TOD zones
            - Active mobility infrastructure requirements""",
            measure_type="planning",
            target_regions=["Riyadh", "Makkah", "Eastern Province"],
            implementation_timeline="medium-term",
            estimated_cost_sar_million=500,
            expected_benefit="30% reduction in car dependency in TOD zones",
            responsible_agency="Royal Commission for Riyadh City / Municipal authorities",
            kpis=[
                "TOD zone population density",
                "Transit ridership in zones",
                "Car ownership in zones",
                "Mixed-use development ratio"
            ],
            priority="medium"
        ))
        
        # Heritage Protection
        self.measures.append(CorrectiveMeasure(
            measure_id="CM-008",
            title="Heritage and Tourism Compatibility Program",
            conflict_addressed="Tourism Development vs Heritage Preservation",
            description="""Framework for tourism development respecting heritage values:
            - Heritage impact assessment requirements
            - Visitor carrying capacity limits
            - Authentic preservation standards
            - Community benefit-sharing mechanisms""",
            measure_type="regulatory",
            target_regions=["Madinah", "Riyadh", "Asir", "Al-Baha"],
            implementation_timeline="medium-term",
            estimated_cost_sar_million=800,
            expected_benefit="Protection of all UNESCO and national heritage sites",
            responsible_agency="Heritage Commission",
            kpis=[
                "Heritage sites with management plans (%)",
                "Visitor satisfaction index",
                "Heritage site condition index",
                "Local community employment (%)"
            ],
            priority="medium"
        ))
        
        # Regional Economic Diversification
        self.measures.append(CorrectiveMeasure(
            measure_id="CM-009",
            title="Regional Economic Specialization Program",
            conflict_addressed="Regional Imbalance and Duplication",
            description="""Development of distinctive economic identities for each region:
            - Regional competitive advantage assessment
            - Targeted investment incentives
            - Infrastructure prioritization
            - Skills development programs""",
            measure_type="incentive",
            target_regions=["All regions except Riyadh, Makkah, Eastern Province"],
            implementation_timeline="long-term",
            estimated_cost_sar_million=15000,
            expected_benefit="Reduce top-3 regional GDP concentration from 96% to 85%",
            responsible_agency="Ministry of Economy and Planning",
            kpis=[
                "Regional GDP share changes",
                "Private sector investment by region",
                "Employment growth by region",
                "Economic diversification index"
            ],
            priority="medium"
        ))
        
        # Green Infrastructure
        self.measures.append(CorrectiveMeasure(
            measure_id="CM-010",
            title="Urban Green Infrastructure Network",
            conflict_addressed="Urban Heat and Environmental Quality",
            description="""Systematic development of urban green infrastructure:
            - Green space requirements (9 m² per capita minimum)
            - Urban forest programs
            - Green building requirements
            - Heat island mitigation""",
            measure_type="investment",
            target_regions=["Riyadh", "Makkah", "Eastern Province"],
            implementation_timeline="long-term",
            estimated_cost_sar_million=12000,
            expected_benefit="3°C reduction in urban heat island effect",
            responsible_agency="Ministry of Municipal and Rural Affairs",
            kpis=[
                "Green space per capita (m²)",
                "Tree canopy coverage (%)",
                "Urban temperature differential (°C)",
                "Air quality improvement"
            ],
            priority="medium"
        ))
    
    def get_all_measures(self) -> List[CorrectiveMeasure]:
        """Get all corrective measures."""
        return self.measures
    
    def get_by_priority(self, priority: str) -> List[CorrectiveMeasure]:
        """Get measures by priority level."""
        return [m for m in self.measures if m.priority == priority]
    
    def get_by_region(self, region: str) -> List[CorrectiveMeasure]:
        """Get measures applicable to a specific region."""
        return [m for m in self.measures if region in m.target_regions or "All regions" in m.target_regions]
    
    def calculate_total_investment(self) -> Dict[str, Any]:
        """Calculate total investment needs."""
        total = sum(m.estimated_cost_sar_million for m in self.measures)
        by_priority = {}
        for priority in ["critical", "high", "medium", "low"]:
            measures = self.get_by_priority(priority)
            by_priority[priority] = sum(m.estimated_cost_sar_million for m in measures)
        
        by_type = {}
        for m in self.measures:
            by_type[m.measure_type] = by_type.get(m.measure_type, 0) + m.estimated_cost_sar_million
        
        return {
            "total_sar_million": total,
            "total_sar_billion": total / 1000,
            "by_priority": by_priority,
            "by_type": by_type,
            "measure_count": len(self.measures)
        }
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert measures to DataFrame."""
        return pd.DataFrame([
            {
                'ID': m.measure_id,
                'Title': m.title,
                'Conflict': m.conflict_addressed,
                'Type': m.measure_type.upper(),
                'Priority': m.priority.upper(),
                'Timeline': m.implementation_timeline,
                'Cost (SAR M)': m.estimated_cost_sar_million,
                'Responsible Agency': m.responsible_agency,
                'Expected Benefit': m.expected_benefit
            }
            for m in self.measures
        ])


# =============================================================================
# WORKSHOP MATERIALS
# =============================================================================

class WorkshopMaterialsGenerator:
    """
    Generates materials for stakeholder workshops.
    """
    
    def __init__(self):
        """Initialize workshop materials generator."""
        self._generate_workshops()
        logger.info("Workshop Materials Generator initialized")
    
    def _generate_workshops(self):
        """Generate workshop materials."""
        
        self.workshops: List[WorkshopMaterial] = []
        
        # Workshop 1: Regional Planning Authorities
        self.workshops.append(WorkshopMaterial(
            workshop_id="WS4-W01",
            title="Regional Spatial Integration Workshop",
            objective="Align regional development plans with national spatial strategy",
            target_audience=[
                "Regional Development Authorities (13 regions)",
                "Municipal Planning Directors",
                "Regional Governors' Representatives"
            ],
            duration_hours=6.0,
            agenda_items=[
                "09:00-09:30: Opening and NSS Overview",
                "09:30-10:30: Regional Diagnostic Presentations (3 focus regions)",
                "10:30-10:45: Break",
                "10:45-12:00: Interactive Session: Identifying Regional Priorities",
                "12:00-13:00: Lunch",
                "13:00-14:30: Working Groups: Conflict Resolution Strategies",
                "14:30-15:00: Group Presentations",
                "15:00-15:30: Synthesis and Next Steps"
            ],
            key_discussion_points=[
                "How do regional development plans align with national priorities?",
                "What are the key spatial conflicts in each region?",
                "How can inter-regional coordination be improved?",
                "What resources are needed for regional implementation?"
            ],
            data_presentations=[
                "Regional diagnostic summaries (13 regions)",
                "Conflict and synergy maps",
                "Water availability analysis",
                "Giga-project impact assessment"
            ],
            feedback_mechanisms=[
                "Real-time polling for priority ranking",
                "Working group flip charts",
                "Post-workshop online survey",
                "Written comment submission"
            ],
            expected_outputs=[
                "Validated regional priorities",
                "Identified inter-regional coordination needs",
                "Regional implementation capacity assessment",
                "Input for NSS regional chapters"
            ]
        ))
        
        # Workshop 2: Sectoral Ministries
        self.workshops.append(WorkshopMaterial(
            workshop_id="WS4-W02",
            title="Sectoral Spatial Coordination Workshop",
            objective="Resolve sectoral conflicts and identify synergies",
            target_audience=[
                "Ministry of Economy and Planning",
                "Ministry of Municipal and Rural Affairs",
                "Ministry of Environment, Water and Agriculture",
                "Ministry of Industry and Mineral Resources",
                "Ministry of Tourism",
                "Ministry of Transport and Logistics",
                "Ministry of Energy"
            ],
            duration_hours=8.0,
            agenda_items=[
                "09:00-09:30: Opening and Sectoral Analysis Overview",
                "09:30-11:00: Sectoral Strategy Presentations (6 sectors)",
                "11:00-11:15: Break",
                "11:15-12:30: Conflict Identification Exercise",
                "12:30-13:30: Lunch",
                "13:30-15:00: Working Groups: Cross-Sectoral Solutions",
                "15:00-15:15: Break",
                "15:15-16:30: Synergy Optimization Session",
                "16:30-17:00: Commitments and Action Items"
            ],
            key_discussion_points=[
                "Where do sectoral strategies create spatial conflicts?",
                "How can water allocation be optimized across sectors?",
                "What mechanisms can improve cross-sectoral coordination?",
                "How can giga-projects benefit multiple sectors?"
            ],
            data_presentations=[
                "Sectoral land and water requirements",
                "Conflict matrix analysis",
                "Synergy opportunity maps",
                "International benchmarking examples"
            ],
            feedback_mechanisms=[
                "Sectoral conflict priority voting",
                "Bilateral coordination agreements",
                "Cross-sectoral working group formation",
                "Action item tracking system"
            ],
            expected_outputs=[
                "Cross-sectoral coordination agreements",
                "Conflict resolution action plans",
                "Synergy exploitation roadmap",
                "Inter-ministerial coordination mechanism proposal"
            ]
        ))
        
        # Workshop 3: Private Sector and Developers
        self.workshops.append(WorkshopMaterial(
            workshop_id="WS4-W03",
            title="Private Sector Spatial Development Forum",
            objective="Engage private sector in spatial strategy implementation",
            target_audience=[
                "Real estate developers",
                "Industrial investors",
                "Tourism operators",
                "Infrastructure companies",
                "Financial institutions",
                "Chamber of Commerce representatives"
            ],
            duration_hours=4.0,
            agenda_items=[
                "14:00-14:30: Opening and NSS Business Implications",
                "14:30-15:30: Panel: Spatial Planning and Investment Climate",
                "15:30-15:45: Break",
                "15:45-16:45: Breakout Sessions: Sector-Specific Opportunities",
                "16:45-17:30: Investment Facilitation Mechanisms",
                "17:30-18:00: Q&A and Networking"
            ],
            key_discussion_points=[
                "How does spatial planning affect investment decisions?",
                "What regulatory certainty do developers need?",
                "How can public-private partnerships be strengthened?",
                "What incentives support balanced regional development?"
            ],
            data_presentations=[
                "Investment opportunity maps",
                "Regulatory framework overview",
                "Incentive zone locations",
                "Infrastructure development timeline"
            ],
            feedback_mechanisms=[
                "Investment barrier survey",
                "Regulatory improvement suggestions",
                "Partnership opportunity identification",
                "Follow-up meeting requests"
            ],
            expected_outputs=[
                "Private sector input on spatial priorities",
                "Investment barrier identification",
                "PPP opportunity pipeline",
                "Regulatory improvement recommendations"
            ]
        ))
        
        # Workshop 4: Environmental and Civil Society
        self.workshops.append(WorkshopMaterial(
            workshop_id="WS4-W04",
            title="Environmental and Community Stakeholder Consultation",
            objective="Ensure environmental sustainability and community voice in spatial planning",
            target_audience=[
                "Environmental NGOs",
                "Academic institutions",
                "Community representatives",
                "Youth organizations",
                "Environmental consultants",
                "Research centers"
            ],
            duration_hours=4.0,
            agenda_items=[
                "10:00-10:30: Opening and Environmental Context",
                "10:30-11:30: Presentation: Environmental Challenges and Spatial Solutions",
                "11:30-11:45: Break",
                "11:45-12:45: Participatory Mapping Exercise",
                "12:45-13:30: Community Voice Session",
                "13:30-14:00: Recommendations and Commitments"
            ],
            key_discussion_points=[
                "How can spatial planning better protect the environment?",
                "What are community concerns about development?",
                "How can 30x30 biodiversity targets be achieved?",
                "What role can civil society play in monitoring?"
            ],
            data_presentations=[
                "Environmental sensitivity maps",
                "Protected area expansion plans",
                "Climate risk assessment",
                "Community impact analysis"
            ],
            feedback_mechanisms=[
                "Participatory mapping inputs",
                "Written submissions",
                "Focus group discussions",
                "Online consultation portal"
            ],
            expected_outputs=[
                "Environmental priority areas identified",
                "Community concerns documented",
                "Civil society monitoring proposals",
                "Recommendations for environmental integration"
            ]
        ))
    
    def get_all_workshops(self) -> List[WorkshopMaterial]:
        """Get all workshop materials."""
        return self.workshops
    
    def get_workshop(self, workshop_id: str) -> Optional[WorkshopMaterial]:
        """Get specific workshop by ID."""
        for ws in self.workshops:
            if ws.workshop_id == workshop_id:
                return ws
        return None
    
    def generate_presentation_outline(self, workshop_id: str) -> Dict[str, Any]:
        """Generate presentation outline for a workshop."""
        ws = self.get_workshop(workshop_id)
        if not ws:
            return {}
        
        return {
            "workshop": ws.title,
            "presentation_structure": [
                {
                    "section": "Introduction",
                    "slides": [
                        "Title and objectives",
                        "Agenda overview",
                        "Workshop rules and logistics"
                    ]
                },
                {
                    "section": "Context Setting",
                    "slides": [
                        "NSS X overview and timeline",
                        "WS4 sectoral and regional analysis summary",
                        "Key challenges identified"
                    ]
                },
                {
                    "section": "Main Content",
                    "slides": ws.data_presentations
                },
                {
                    "section": "Interactive Sessions",
                    "slides": [
                        "Discussion questions",
                        "Working group instructions",
                        "Feedback mechanisms"
                    ]
                },
                {
                    "section": "Conclusion",
                    "slides": [
                        "Key takeaways",
                        "Next steps",
                        "Follow-up commitments"
                    ]
                }
            ],
            "handout_materials": [
                "Regional/sectoral diagnostic summaries",
                "Conflict and synergy maps",
                "Discussion question guides",
                "Feedback forms"
            ]
        }


# =============================================================================
# WS4 REPORT GENERATOR
# =============================================================================

class WS4ReportGenerator:
    """
    Generates all WS4 deliverables.
    """
    
    def __init__(self, output_dir: str = "02_analytics/ws4_outputs"):
        """Initialize report generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize base analyzer
        self.sectoral = SectoralAnalyzer()
        
        # Initialize comprehensive components
        self.strategies = SectoralStrategiesReviewer()
        self.regional = RegionalDiagnosticsAnalyzer()
        self.mapper = ConflictSynergyMapper(self.sectoral, self.regional)
        self.playbook = OptimizationPlaybook()
        self.workshops = WorkshopMaterialsGenerator()
        
        logger.info(f"WS4 Report Generator initialized. Output: {self.output_dir}")
    
    def generate_all_reports(self) -> Dict[str, Any]:
        """Generate all WS4 deliverables."""
        
        logger.info("Generating WS4 deliverables...")
        
        # Get all data
        strategies = self.strategies.get_all_strategies()
        regions = self.regional.get_all_regions()
        conflict_layers = self.mapper.get_all_conflict_layers()
        synergy_layers = self.mapper.get_all_synergy_layers()
        measures = self.playbook.get_all_measures()
        workshops = self.workshops.get_all_workshops()
        
        # Save CSV files
        self.playbook.to_dataframe().to_csv(
            self.output_dir / "corrective_measures_playbook.csv", index=False
        )
        
        # Save conflict matrix
        self.sectoral.get_conflict_matrix().to_csv(
            self.output_dir / "land_use_conflict_matrix.csv"
        )
        
        # Save regional summaries
        regional_df = pd.DataFrame([
            {
                'Region': r.region_name,
                'Population_2025_M': r.population_2025,
                'Population_2030_M': r.population_2030_projected,
                'GDP_Contribution_%': r.gdp_contribution_pct,
                'Water_Availability': r.water_availability,
                'Development_Potential': r.development_potential,
                'Giga_Projects': ', '.join(r.giga_projects) if r.giga_projects else 'None'
            }
            for r in regions.values()
        ])
        regional_df.to_csv(self.output_dir / "regional_diagnostics_summary.csv", index=False)
        
        # Save map layers
        with open(self.output_dir / "map_layers_definition.json", 'w', encoding='utf-8') as f:
            json.dump(self.mapper.to_geojson_style_dict(), f, indent=2)
        
        # Compile comprehensive report
        report = {
            "metadata": {
                "report_title": "WS4 - Sectoral & Regional Spatial Integration",
                "generated_date": datetime.now().isoformat(),
                "version": "1.0",
                "author": "NSS X System"
            },
            "executive_summary": self._generate_executive_summary(strategies, regions, measures),
            "section_1_sectoral_strategies": {
                strategy_key: self._strategy_to_dict(strategy)
                for strategy_key, strategy in strategies.items()
            },
            "section_2_regional_diagnostics": {
                region_name: self._regional_to_dict(region)
                for region_name, region in regions.items()
            },
            "section_3_conflict_synergy_maps": {
                "conflict_layers": [self._layer_to_dict(l) for l in conflict_layers],
                "synergy_layers": [self._layer_to_dict(l) for l in synergy_layers],
                "critical_conflicts": [l.layer_name for l in self.mapper.get_critical_conflicts()]
            },
            "section_4_optimization_playbook": {
                "summary": self.playbook.calculate_total_investment(),
                "measures": [self._measure_to_dict(m) for m in measures]
            },
            "section_5_workshop_materials": {
                "workshops": [self._workshop_to_dict(w) for w in workshops],
                "presentation_outlines": {
                    w.workshop_id: self.workshops.generate_presentation_outline(w.workshop_id)
                    for w in workshops
                }
            },
            "appendices": {
                "data_sources": [
                    "Vision 2030 Program Documents",
                    "NIDLP Strategy Documents",
                    "Ministry of Economy and Planning Reports",
                    "GASTAT Regional Statistics",
                    "Ministry of Environment Water Reports",
                    "Giga-project Official Communications"
                ],
                "output_files": [
                    "corrective_measures_playbook.csv",
                    "land_use_conflict_matrix.csv",
                    "regional_diagnostics_summary.csv",
                    "map_layers_definition.json",
                    "WS4_SECTORAL_REGIONAL_REPORT.json",
                    "WS4_SECTORAL_REGIONAL_REPORT.md"
                ]
            }
        }
        
        # Save JSON report
        report_path = self.output_dir / "WS4_SECTORAL_REGIONAL_REPORT.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        logger.success(f"WS4 Report saved to {report_path}")
        
        # Generate markdown report
        self._generate_markdown_report(report)
        
        return report
    
    def _generate_executive_summary(
        self, 
        strategies: Dict[str, SectoralStrategy],
        regions: Dict[str, RegionalDiagnostic],
        measures: List[CorrectiveMeasure]
    ) -> Dict[str, Any]:
        """Generate executive summary."""
        
        total_spatial = self.strategies.get_total_spatial_requirements()
        national = self.regional.calculate_national_aggregates()
        investment = self.playbook.calculate_total_investment()
        
        return {
            "overview": """This integrated sectoral and regional spatial review analyzes 6 major 
            sectors and 13 regions to identify spatial conflicts, synergies, and corrective measures. 
            The analysis reveals critical water sustainability challenges, industrial-residential 
            conflicts, and coastal development pressures requiring immediate intervention.""",
            
            "key_findings": [
                f"6 sectoral strategies analyzed with SAR {total_spatial['total_investment_sar_billion']:.0f}B total investment",
                f"13 regional diagnostics completed covering {sum(r.population_2025 for r in regions.values()):.1f}M population",
                f"5 conflict map layers and 5 synergy map layers generated",
                f"CRITICAL: Agricultural water demand ({total_spatial['water_comparison']['agriculture_share_pct']:.0f}% of total) unsustainable",
                f"Top 3 regions concentrate {national['regional_concentration']['top_3_gdp_share']}% of GDP",
                f"{len([r for r in regions.values() if r.water_availability == 'critical'])} regions with critical water availability",
                f"{investment['measure_count']} corrective measures identified (SAR {investment['total_sar_billion']:.1f}B total)"
            ],
            
            "spatial_requirements": total_spatial,
            "national_aggregates": national,
            "investment_summary": investment,
            
            "critical_actions": [
                "Implement agricultural water demand reduction (40% target)",
                "Establish industrial-residential buffer zones",
                "Develop integrated coastal zone management",
                "Expand protected areas to meet 30x30 commitment",
                "Create regional economic specialization programs"
            ],
            
            "workshop_program": {
                "total_workshops": 4,
                "target_audiences": [
                    "Regional Planning Authorities",
                    "Sectoral Ministries", 
                    "Private Sector",
                    "Environmental/Civil Society"
                ]
            }
        }
    
    def _strategy_to_dict(self, strategy: SectoralStrategy) -> Dict:
        """Convert SectoralStrategy to dictionary."""
        return {
            "sector_name": strategy.sector_name,
            "strategy_document": strategy.strategy_document,
            "vision2030_program": strategy.vision2030_program,
            "key_objectives": strategy.key_objectives,
            "spatial_requirements": strategy.spatial_requirements,
            "target_regions": strategy.target_regions,
            "resource_needs": {
                "land_km2": strategy.land_area_needed_km2,
                "water_mcm_year": strategy.water_demand_mcm_year,
                "employment_2030": strategy.employment_target_2030,
                "investment_sar_billion": strategy.investment_target_sar_billion
            },
            "key_projects": strategy.key_projects,
            "conflicts": strategy.spatial_conflicts,
            "synergies": strategy.spatial_synergies,
            "recommendations": strategy.recommendations
        }
    
    def _regional_to_dict(self, region: RegionalDiagnostic) -> Dict:
        """Convert RegionalDiagnostic to dictionary."""
        return {
            "basic_info": {
                "name": region.region_name,
                "name_ar": region.region_name_ar,
                "area_km2": region.area_km2,
                "population_2025_millions": region.population_2025,
                "population_2030_millions": region.population_2030_projected,
                "urbanization_rate": region.urbanization_rate
            },
            "settlement_hierarchy": {
                "primary_city": region.primary_city,
                "secondary_cities": region.secondary_cities,
                "settlement_count": region.settlement_count,
                "urban_primacy_ratio": region.urban_primacy_ratio
            },
            "economic_profile": {
                "gdp_contribution_pct": region.gdp_contribution_pct,
                "gdp_per_capita_sar": region.gdp_per_capita_sar,
                "dominant_sectors": region.dominant_sectors,
                "emerging_sectors": region.emerging_sectors,
                "employment_rate": region.employment_rate
            },
            "competitive_position": {
                "advantages": region.competitive_advantages,
                "strategic_assets": region.strategic_assets
            },
            "environmental_capacity": {
                "water_availability": region.water_availability,
                "water_sources": region.water_sources,
                "water_demand_mcm": region.annual_water_demand_mcm,
                "water_supply_mcm": region.annual_water_supply_mcm,
                "water_balance": region.annual_water_supply_mcm - region.annual_water_demand_mcm,
                "environmental_sensitivity": region.environmental_sensitivity,
                "protected_areas_pct": region.protected_areas_pct,
                "climate_risks": region.climate_risks
            },
            "development_outlook": {
                "potential": region.development_potential,
                "constraints": region.key_constraints,
                "priority_investments": region.priority_investments,
                "giga_projects": region.giga_projects,
                "vision2030_role": region.vision2030_role
            }
        }
    
    def _layer_to_dict(self, layer: ConflictMapLayer) -> Dict:
        """Convert ConflictMapLayer to dictionary."""
        return {
            "name": layer.layer_name,
            "type": layer.layer_type,
            "description": layer.description,
            "affected_regions": layer.affected_regions,
            "severity": layer.severity,
            "land_uses": layer.land_uses_involved,
            "area_km2": layer.area_affected_km2,
            "priority": layer.mitigation_priority,
            "visualization": layer.visualization_style
        }
    
    def _measure_to_dict(self, measure: CorrectiveMeasure) -> Dict:
        """Convert CorrectiveMeasure to dictionary."""
        return {
            "id": measure.measure_id,
            "title": measure.title,
            "conflict_addressed": measure.conflict_addressed,
            "description": measure.description,
            "type": measure.measure_type,
            "target_regions": measure.target_regions,
            "timeline": measure.implementation_timeline,
            "cost_sar_million": measure.estimated_cost_sar_million,
            "benefit": measure.expected_benefit,
            "responsible_agency": measure.responsible_agency,
            "kpis": measure.kpis,
            "priority": measure.priority
        }
    
    def _workshop_to_dict(self, workshop: WorkshopMaterial) -> Dict:
        """Convert WorkshopMaterial to dictionary."""
        return {
            "id": workshop.workshop_id,
            "title": workshop.title,
            "objective": workshop.objective,
            "target_audience": workshop.target_audience,
            "duration_hours": workshop.duration_hours,
            "agenda": workshop.agenda_items,
            "discussion_points": workshop.key_discussion_points,
            "presentations": workshop.data_presentations,
            "feedback_mechanisms": workshop.feedback_mechanisms,
            "expected_outputs": workshop.expected_outputs
        }
    
    def _generate_markdown_report(self, report: Dict):
        """Generate markdown version of the report."""
        
        md_content = f"""# WS4 - Sectoral & Regional Spatial Integration

**Generated:** {report['metadata']['generated_date']}
**Version:** {report['metadata']['version']}

---

## Executive Summary

{report['executive_summary']['overview']}

### Key Findings

"""
        for finding in report['executive_summary']['key_findings']:
            md_content += f"- {finding}\n"
        
        md_content += """
### Critical Actions Required

"""
        for i, action in enumerate(report['executive_summary']['critical_actions'], 1):
            md_content += f"{i}. **{action}**\n"
        
        md_content += f"""
### Investment Summary

| Category | Amount (SAR Billion) |
|----------|---------------------|
| Total Corrective Measures | {report['executive_summary']['investment_summary']['total_sar_billion']:.1f} |
| Critical Priority | {report['executive_summary']['investment_summary']['by_priority'].get('critical', 0)/1000:.1f} |
| High Priority | {report['executive_summary']['investment_summary']['by_priority'].get('high', 0)/1000:.1f} |
| Medium Priority | {report['executive_summary']['investment_summary']['by_priority'].get('medium', 0)/1000:.1f} |

---

## Section 1: Sectoral Strategy Reviews

"""
        for sector_key, sector in report['section_1_sectoral_strategies'].items():
            md_content += f"""### {sector['sector_name']}

**Strategy Document:** {sector['strategy_document']}
**Vision 2030 Program:** {sector['vision2030_program']}

**Resource Requirements:**
- Land: {sector['resource_needs']['land_km2']:,} km²
- Water: {sector['resource_needs']['water_mcm_year']:,} MCM/year
- Employment 2030: {sector['resource_needs']['employment_2030']:,} jobs
- Investment: SAR {sector['resource_needs']['investment_sar_billion']:.0f}B

**Key Projects:** {', '.join(sector['key_projects'][:3])}...

**Spatial Conflicts:**
"""
            for conflict in sector['conflicts'][:3]:
                md_content += f"- {conflict}\n"
            
            md_content += "\n**Recommendations:**\n"
            for rec in sector['recommendations'][:2]:
                md_content += f"- {rec}\n"
            
            md_content += "\n---\n\n"
        
        md_content += """## Section 2: Regional Diagnostics Summary

| Region | Pop 2025 (M) | GDP % | Water Status | Potential | Giga-Projects |
|--------|--------------|-------|--------------|-----------|---------------|
"""
        for region_name, region in report['section_2_regional_diagnostics'].items():
            giga = ', '.join(region['development_outlook']['giga_projects'][:2]) if region['development_outlook']['giga_projects'] else 'None'
            md_content += f"| {region_name} | {region['basic_info']['population_2025_millions']:.1f} | {region['economic_profile']['gdp_contribution_pct']:.1f} | {region['environmental_capacity']['water_availability']} | {region['development_outlook']['potential']} | {giga} |\n"
        
        md_content += """
---

## Section 3: Conflict and Synergy Maps

### Conflict Layers

| Layer | Severity | Priority | Regions | Area (km²) |
|-------|----------|----------|---------|------------|
"""
        for layer in report['section_3_conflict_synergy_maps']['conflict_layers']:
            regions = ', '.join(layer['affected_regions'][:3])
            md_content += f"| {layer['name']} | {layer['severity'].upper()} | {layer['priority'].upper()} | {regions} | {layer['area_km2']:,} |\n"
        
        md_content += """
### Synergy Layers

| Layer | Impact | Action | Regions | Area (km²) |
|-------|--------|--------|---------|------------|
"""
        for layer in report['section_3_conflict_synergy_maps']['synergy_layers']:
            regions = ', '.join(layer['affected_regions'][:3])
            md_content += f"| {layer['name']} | {layer['severity'].upper()} | {layer['priority'].upper()} | {regions} | {layer['area_km2']:,} |\n"
        
        md_content += """
---

## Section 4: Optimization Playbook

### Corrective Measures Summary

| ID | Title | Priority | Timeline | Cost (SAR M) |
|----|-------|----------|----------|--------------|
"""
        for measure in report['section_4_optimization_playbook']['measures']:
            md_content += f"| {measure['id']} | {measure['title'][:40]}... | {measure['priority'].upper()} | {measure['timeline']} | {measure['cost_sar_million']:,} |\n"
        
        md_content += """
---

## Section 5: Workshop Program

"""
        for workshop in report['section_5_workshop_materials']['workshops']:
            md_content += f"""### {workshop['title']}

**ID:** {workshop['id']}
**Duration:** {workshop['duration_hours']} hours
**Objective:** {workshop['objective']}

**Target Audience:**
"""
            for audience in workshop['target_audience']:
                md_content += f"- {audience}\n"
            
            md_content += f"""
**Expected Outputs:**
"""
            for output in workshop['expected_outputs']:
                md_content += f"- {output}\n"
            
            md_content += "\n---\n\n"
        
        md_content += """## Appendices

### Data Sources
"""
        for source in report['appendices']['data_sources']:
            md_content += f"- {source}\n"
        
        md_content += """
### Output Files
"""
        for file in report['appendices']['output_files']:
            md_content += f"- `{file}`\n"
        
        # Save markdown
        md_path = self.output_dir / "WS4_SECTORAL_REGIONAL_REPORT.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.success(f"Markdown report saved to {md_path}")


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def generate_ws4_deliverables(output_dir: str = "02_analytics/ws4_outputs") -> Dict[str, Any]:
    """Generate all WS4 deliverables."""
    generator = WS4ReportGenerator(output_dir)
    return generator.generate_all_reports()


if __name__ == "__main__":
    print("=" * 60)
    print("NSS X - WS4 Sectoral & Regional Integration Generator")
    print("=" * 60)
    
    report = generate_ws4_deliverables()
    
    print("\n✅ WS4 Deliverables Generated:")
    print(f"   📄 WS4_SECTORAL_REGIONAL_REPORT.json")
    print(f"   📄 WS4_SECTORAL_REGIONAL_REPORT.md")
    print(f"   📄 corrective_measures_playbook.csv")
    print(f"   📄 land_use_conflict_matrix.csv")
    print(f"   📄 regional_diagnostics_summary.csv")
    print(f"   📄 map_layers_definition.json")
    
    print("\n📊 Analysis Summary:")
    print(f"   Sectoral strategies reviewed: 6")
    print(f"   Regional diagnostics: 13")
    print(f"   Conflict map layers: 5")
    print(f"   Synergy map layers: 5")
    print(f"   Corrective measures: {len(report['section_4_optimization_playbook']['measures'])}")
    print(f"   Workshops designed: 4")
    
    investment = report['executive_summary']['investment_summary']
    print(f"\n💰 Investment Required: SAR {investment['total_sar_billion']:.1f}B")
    
    print("\n⚠️ Critical Conflicts:")
    for conflict in report['section_3_conflict_synergy_maps']['critical_conflicts']:
        print(f"   • {conflict}")
    
    print("\n✅ WS4 Complete!")
