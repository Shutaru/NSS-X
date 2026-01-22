"""
NSS X - WS6: National Spatial Strategy Draft Development
Complete NSS draft with vision, spatial structure, and regional objectives.

Deliverables:
- 6.1 National Spatial Strategy Draft Report
- 6.2 National Spatial Structure Maps (data)
- 6.3 Sectoral and Regional Strategy Maps (data)
- 6.4 Stakeholder Engagement Materials
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


# =============================================================================
# COORDINATE LOOKUPS (Module-level for CSV generation)
# =============================================================================

CITY_COORDS = {
    "Riyadh": (24.7136, 46.6753),
    "Jeddah": (21.4858, 39.1925),
    "Dammam-Khobar-Dhahran": (26.4207, 50.0888),
    "NEOM": (28.0000, 35.0000),
    "Makkah": (21.3891, 39.8579),
    "Madinah": (24.5247, 39.5692),
    "Tabuk City": (28.3835, 36.5662),
    "Abha": (18.2164, 42.5053),
    "Jubail": (27.0046, 49.6225),
    "Yanbu": (24.0895, 38.0618),
    "Buraydah": (26.3260, 43.9750),
    "Taif": (21.2703, 40.4158),
    "Khamis Mushait": (18.3000, 42.7333),
    "Hail": (27.5114, 41.7208),
    "Jizan City": (16.8894, 42.5511),
    "Najran City": (17.4917, 44.1322),
    "Al Bahah City": (20.0129, 41.4677),
    "Arar City": (30.9753, 41.0381),
    "Sakaka": (29.9697, 40.2064),
    "Al Hofuf": (25.3648, 49.5870)
}

CORRIDOR_COORDS = {
    "Riyadh-Jeddah Economic Corridor": ((24.7136, 46.6753), (21.4858, 39.1925)),
    "Eastern Economic Corridor": ((26.4207, 50.0888), (27.0046, 49.6225)),
    "Red Sea Tourism Corridor": ((28.0000, 35.0000), (21.4858, 39.1925)),
    "Northern Development Corridor": ((28.3835, 36.5662), (30.9753, 41.0381)),
    "Southern Growth Corridor": ((18.2164, 42.5053), (16.8894, 42.5511)),
    "Central Logistics Spine": ((24.7136, 46.6753), (26.3260, 43.9750))
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class NSSVision:
    """National Spatial Strategy Vision."""
    vision_statement: str
    vision_statement_ar: str
    time_horizon: int
    guiding_principles: List[Dict[str, str]]
    strategic_objectives: List[Dict[str, Any]]
    alignment_with_vision2030: List[str]


@dataclass
class StrategicNode:
    """Strategic node (anchor city) in the spatial structure."""
    name: str
    name_ar: str
    region: str
    tier: int  # 1=National, 2=Regional, 3=Sub-regional
    node_type: str  # capital, economic, tourism, industrial, emerging
    population_2024: float
    population_2050_target: float
    primary_functions: List[str]
    key_investments: List[str]
    connectivity_priority: str  # critical, high, medium
    giga_projects: List[str]
    lat: float = 0.0  # Latitude
    lon: float = 0.0  # Longitude


@dataclass
class DevelopmentCorridor:
    """Development corridor connecting strategic nodes."""
    name: str
    name_ar: str
    corridor_type: str  # economic, logistics, tourism, mixed
    origin_node: str
    destination_node: str
    intermediate_nodes: List[str]
    length_km: float
    infrastructure_components: List[str]
    economic_sectors: List[str]
    investment_sar_billion: float
    priority: str  # critical, high, medium
    timeline: str  # 2025-2030, 2030-2040, 2040-2050
    start_lat: float = 0.0
    start_lon: float = 0.0
    end_lat: float = 0.0
    end_lon: float = 0.0


@dataclass
class FunctionalZone:
    """Functional zone designation."""
    zone_name: str
    zone_type: str  # urban_growth, industrial, agricultural, protected, tourism, mixed
    description: str
    area_km2: float
    regions_covered: List[str]
    permitted_uses: List[str]
    restricted_uses: List[str]
    development_intensity: str  # high, medium, low, minimal
    environmental_sensitivity: str  # high, medium, low


@dataclass
class RegionalObjective:
    """Strategic objective for a region."""
    region: str
    region_ar: str
    strategic_role: str
    vision_statement: str
    population_target_2050: float
    gdp_share_target_2050: float
    priority_sectors: List[str]
    key_projects: List[str]
    infrastructure_priorities: List[str]
    environmental_targets: Dict[str, Any]
    complementarities: List[str]
    challenges: List[str]


@dataclass
class InvestmentPriority:
    """Investment priority item."""
    priority_id: str
    title: str
    category: str  # infrastructure, economic, social, environmental
    description: str
    estimated_cost_sar_billion: float
    timeline: str
    regions_benefited: List[str]
    expected_outcomes: List[str]
    funding_sources: List[str]
    implementation_agency: str


# =============================================================================
# NSS VISION BUILDER
# =============================================================================

class NSSVisionBuilder:
    """
    Builds the NSS Vision, Principles and Strategic Objectives.
    """
    
    def __init__(self):
        """Initialize vision builder."""
        self.vision = self._build_vision()
        logger.info("NSS Vision Builder initialized")
    
    def _build_vision(self) -> NSSVision:
        """Build the complete NSS Vision."""
        
        return NSSVision(
            vision_statement="""By 2050, Saudi Arabia will be a thriving, sustainable, and connected 
            nation where all regions prosper, cities are livable, natural heritage is preserved, 
            and every citizen has access to economic opportunity and quality of life - a global 
            model of balanced territorial development in harmony with Vision 2030 aspirations.""",
            
            vision_statement_ar="""بحلول عام 2050، ستكون المملكة العربية السعودية دولة مزدهرة ومستدامة 
            ومتصلة حيث تزدهر جميع المناطق، وتكون المدن صالحة للعيش، ويُحافظ على التراث الطبيعي، 
            ويتمتع كل مواطن بفرص اقتصادية وجودة حياة عالية - نموذج عالمي للتنمية الإقليمية المتوازنة 
            بانسجام مع تطلعات رؤية 2030.""",
            
            time_horizon=2050,
            
            guiding_principles=[
                {
                    "principle": "Balanced Regional Development",
                    "principle_ar": "التنمية الإقليمية المتوازنة",
                    "description": "Ensure all 13 regions have distinct economic roles and adequate investment to reduce spatial inequality and concentration in top 3 regions."
                },
                {
                    "principle": "Water Security as Foundation",
                    "principle_ar": "الأمن المائي كأساس",
                    "description": "Treat water as the binding constraint for all spatial development decisions. No development approval without sustainable water solution."
                },
                {
                    "principle": "Connected Corridors",
                    "principle_ar": "الممرات المتصلة",
                    "description": "Develop integrated transport and economic corridors linking regions to maximize economic spillovers and reduce isolation."
                },
                {
                    "principle": "Environmental Sustainability",
                    "principle_ar": "الاستدامة البيئية",
                    "description": "Protect 30% of land and sea by 2030, mainstream climate resilience, and achieve net-zero domestic emissions by 2060."
                },
                {
                    "principle": "Compact Urban Form",
                    "principle_ar": "الشكل الحضري المدمج",
                    "description": "Promote compact, mixed-use urban development around transit nodes to reduce sprawl, car dependency, and infrastructure costs."
                },
                {
                    "principle": "Heritage Integration",
                    "principle_ar": "التكامل مع التراث",
                    "description": "Preserve and celebrate Saudi cultural heritage as asset for tourism, identity, and community wellbeing."
                },
                {
                    "principle": "Adaptive Planning",
                    "principle_ar": "التخطيط التكيفي",
                    "description": "Design spatial strategies flexible enough to accommodate multiple future scenarios including climate stress and energy transition."
                },
                {
                    "principle": "Implementation Focus",
                    "principle_ar": "التركيز على التنفيذ",
                    "description": "Every spatial policy must have clear accountability, funding mechanism, timeline, and monitoring indicators."
                }
            ],
            
            strategic_objectives=[
                {
                    "id": "SO1",
                    "objective": "Polycentric Urban Network",
                    "description": "Develop 5 national-tier cities (Riyadh, Jeddah, Dammam, NEOM, Makkah) and 15 regional-tier cities as balanced growth poles",
                    "target_2050": "Reduce top-3 regional population concentration from 64% to 55%",
                    "kpis": ["Regional population share", "Urban primacy ratio", "Inter-city connectivity index"]
                },
                {
                    "id": "SO2",
                    "objective": "Integrated Economic Corridors",
                    "description": "Establish 5 major economic corridors connecting all regions with multimodal transport and economic activity",
                    "target_2050": "100% of regions within 4 hours of a national corridor",
                    "kpis": ["Corridor GDP contribution", "Freight volumes", "Journey times"]
                },
                {
                    "id": "SO3",
                    "objective": "Sustainable Water Management",
                    "description": "Achieve water security through demand reduction, supply diversification, and 100% treated wastewater reuse",
                    "target_2050": "Reduce per capita water consumption by 40%, eliminate groundwater overextraction",
                    "kpis": ["Per capita consumption", "Groundwater balance", "Reuse rate", "Desalination share"]
                },
                {
                    "id": "SO4",
                    "objective": "Climate-Resilient Territories",
                    "description": "Build climate adaptation into all spatial development and protect vulnerable areas",
                    "target_2050": "All development designed for +3°C scenario, 30% protected areas",
                    "kpis": ["Protected area coverage", "Heat vulnerability index", "Coastal protection coverage"]
                },
                {
                    "id": "SO5",
                    "objective": "Economic Diversification Zones",
                    "description": "Create specialized economic zones aligned with regional competitive advantages",
                    "target_2050": "Each region has distinct economic specialization with <30% oil dependency",
                    "kpis": ["Regional diversification index", "Non-oil GDP share", "Private sector employment"]
                },
                {
                    "id": "SO6",
                    "objective": "Quality of Life for All",
                    "description": "Ensure all Saudis have access to quality services, green spaces, and affordable housing",
                    "target_2050": "9 sqm green space per capita, 30-min access to services, 70% housing affordability",
                    "kpis": ["Green space per capita", "Service accessibility", "Housing affordability index"]
                },
                {
                    "id": "SO7",
                    "objective": "Digital and Physical Connectivity",
                    "description": "Achieve universal high-speed connectivity and comprehensive transport network",
                    "target_2050": "100% fiber/5G coverage, all cities on rail network, 6 international hubs",
                    "kpis": ["Broadband coverage", "Rail network km", "Air connectivity index"]
                }
            ],
            
            alignment_with_vision2030=[
                "Vibrant Society: Quality of life, heritage preservation, social development",
                "Thriving Economy: Economic diversification, private sector growth, tourism",
                "Ambitious Nation: Effective governance, implementation excellence, global positioning"
            ]
        )
    
    def get_vision(self) -> NSSVision:
        """Return the NSS Vision."""
        return self.vision


# =============================================================================
# SPATIAL STRUCTURE BUILDER
# =============================================================================

class SpatialStructureBuilder:
    """
    Builds the National Spatial Structure: nodes, corridors, and zones.
    """
    
    def __init__(self):
        """Initialize spatial structure builder."""
        self.nodes = self._build_strategic_nodes()
        self.corridors = self._build_development_corridors()
        self.zones = self._build_functional_zones()
        logger.info(f"Spatial Structure: {len(self.nodes)} nodes, {len(self.corridors)} corridors, {len(self.zones)} zones")
    
    def _build_strategic_nodes(self) -> List[StrategicNode]:
        """Build the hierarchy of strategic nodes."""
        
        nodes = [
            # TIER 1 - National Strategic Nodes (5)
            StrategicNode(
                name="Riyadh",
                name_ar="الرياض",
                region="Riyadh",
                tier=1,
                node_type="capital",
                population_2024=8.9,
                population_2050_target=15.0,
                primary_functions=["National Capital", "Financial Hub", "Technology Center", "Entertainment Capital"],
                key_investments=["Riyadh Metro", "King Salman Park", "Sports Boulevard", "Downtown redevelopment"],
                connectivity_priority="critical",
                giga_projects=["Diriyah Gate", "Qiddiya", "King Salman Park", "Riyadh Green"],
                lat=24.7136, lon=46.6753
            ),
            StrategicNode(
                name="Jeddah",
                name_ar="جدة",
                region="Makkah",
                tier=1,
                node_type="economic",
                population_2024=4.8,
                population_2050_target=7.5,
                primary_functions=["Commercial Gateway", "Red Sea Hub", "Creative Industries", "Logistics"],
                key_investments=["Jeddah Central", "Port expansion", "Waterfront development", "Metro system"],
                connectivity_priority="critical",
                giga_projects=["Jeddah Central", "Obhur Development"]
            ),
            StrategicNode(
                name="Dammam-Khobar-Dhahran",
                name_ar="الدمام-الخبر-الظهران",
                region="Eastern Province",
                tier=1,
                node_type="industrial",
                population_2024=5.3,
                population_2050_target=8.0,
                primary_functions=["Energy Hub", "Industrial Base", "Technology R&D", "Gulf Gateway"],
                key_investments=["SPARK", "Industrial diversification", "Waterfront development", "Rail connectivity"],
                connectivity_priority="critical",
                giga_projects=["King Salman Energy Park"]
            ),
            StrategicNode(
                name="NEOM",
                name_ar="نيوم",
                region="Tabuk",
                tier=1,
                node_type="emerging",
                population_2024=0.05,
                population_2050_target=2.0,
                primary_functions=["Future City", "Innovation Hub", "Sustainable Living", "Tourism Destination"],
                key_investments=["The Line", "Trojena", "Oxagon", "Sindalah"],
                connectivity_priority="critical",
                giga_projects=["NEOM - The Line", "Trojena", "Oxagon", "Sindalah"]
            ),
            StrategicNode(
                name="Makkah",
                name_ar="مكة المكرمة",
                region="Makkah",
                tier=1,
                node_type="tourism",
                population_2024=2.4,
                population_2050_target=4.0,
                primary_functions=["Holy City", "Religious Tourism", "Services Hub"],
                key_investments=["Haram expansion", "Transport infrastructure", "Hospitality"],
                connectivity_priority="critical",
                giga_projects=[]
            ),
            
            # TIER 2 - Regional Strategic Nodes (10)
            StrategicNode(
                name="Madinah",
                name_ar="المدينة المنورة",
                region="Madinah",
                tier=2,
                node_type="tourism",
                population_2024=1.5,
                population_2050_target=2.8,
                primary_functions=["Holy City", "Cultural Tourism", "Knowledge Hub"],
                key_investments=["Prophet's Mosque surroundings", "AlUla connectivity", "University expansion"],
                connectivity_priority="high",
                giga_projects=["AlUla Development"]
            ),
            StrategicNode(
                name="Tabuk City",
                name_ar="تبوك",
                region="Tabuk",
                tier=2,
                node_type="emerging",
                population_2024=0.7,
                population_2050_target=1.5,
                primary_functions=["NEOM Gateway", "Agriculture", "Tourism Base"],
                key_investments=["Airport expansion", "NEOM connectivity", "Agricultural modernization"],
                connectivity_priority="high",
                giga_projects=[]
            ),
            StrategicNode(
                name="Abha",
                name_ar="أبها",
                region="Asir",
                tier=2,
                node_type="tourism",
                population_2024=1.2,
                population_2050_target=2.0,
                primary_functions=["Mountain Tourism", "Regional Capital", "Agriculture"],
                key_investments=["Tourism infrastructure", "Airport expansion", "Cable car network"],
                connectivity_priority="medium",
                giga_projects=["Asir Development"]
            ),
            StrategicNode(
                name="Jubail",
                name_ar="الجبيل",
                region="Eastern Province",
                tier=2,
                node_type="industrial",
                population_2024=0.5,
                population_2050_target=1.2,
                primary_functions=["Industrial City", "Petrochemicals", "Manufacturing"],
                key_investments=["Industrial expansion", "Green hydrogen", "Desalination"],
                connectivity_priority="high",
                giga_projects=[]
            ),
            StrategicNode(
                name="Yanbu",
                name_ar="ينبع",
                region="Madinah",
                tier=2,
                node_type="industrial",
                population_2024=0.3,
                population_2050_target=0.8,
                primary_functions=["Industrial Port", "Petrochemicals", "Red Sea Access"],
                key_investments=["Port expansion", "Industrial zones", "Renewable energy"],
                connectivity_priority="high",
                giga_projects=[]
            ),
            StrategicNode(
                name="Buraydah",
                name_ar="بريدة",
                region="Al-Qassim",
                tier=2,
                node_type="economic",
                population_2024=0.8,
                population_2050_target=1.2,
                primary_functions=["Agricultural Hub", "Food Processing", "Logistics"],
                key_investments=["Water efficiency", "Agri-tech", "Solar energy", "Food processing"],
                connectivity_priority="medium",
                giga_projects=[]
            ),
            StrategicNode(
                name="Hail",
                name_ar="حائل",
                region="Hail",
                tier=2,
                node_type="economic",
                population_2024=0.5,
                population_2050_target=0.8,
                primary_functions=["Agricultural Center", "Mining Gateway", "Heritage Tourism"],
                key_investments=["Mining development", "Agricultural modernization", "Tourism"],
                connectivity_priority="medium",
                giga_projects=[]
            ),
            StrategicNode(
                name="Jazan City",
                name_ar="جيزان",
                region="Jazan",
                tier=2,
                node_type="industrial",
                population_2024=0.5,
                population_2050_target=0.9,
                primary_functions=["Economic City", "Agriculture", "Fishing"],
                key_investments=["Economic city completion", "Port development", "Agriculture"],
                connectivity_priority="medium",
                giga_projects=["Jazan Economic City"]
            ),
            StrategicNode(
                name="Arar",
                name_ar="عرعر",
                region="Northern Borders",
                tier=2,
                node_type="industrial",
                population_2024=0.3,
                population_2050_target=0.6,
                primary_functions=["Mining Hub", "Renewable Energy", "Border Trade"],
                key_investments=["Phosphate processing", "Solar farms", "Cross-border infrastructure"],
                connectivity_priority="medium",
                giga_projects=["Waad Al-Shamal"]
            ),
            StrategicNode(
                name="Sakaka",
                name_ar="سكاكا",
                region="Al-Jouf",
                tier=2,
                node_type="economic",
                population_2024=0.35,
                population_2050_target=0.6,
                primary_functions=["Olive Capital", "Renewable Energy", "Heritage Tourism"],
                key_investments=["Renewable energy", "Agricultural efficiency", "Heritage sites"],
                connectivity_priority="medium",
                giga_projects=[]
            ),
            
            # TIER 3 - Sub-Regional Nodes (5 examples)
            StrategicNode(
                name="Al-Kharj",
                name_ar="الخرج",
                region="Riyadh",
                tier=3,
                node_type="economic",
                population_2024=0.4,
                population_2050_target=0.7,
                primary_functions=["Agricultural Processing", "Industrial Zone", "Riyadh Satellite"],
                key_investments=["Industrial development", "Riyadh connectivity"],
                connectivity_priority="medium",
                giga_projects=[]
            ),
            StrategicNode(
                name="Taif",
                name_ar="الطائف",
                region="Makkah",
                tier=3,
                node_type="tourism",
                population_2024=0.7,
                population_2050_target=1.0,
                primary_functions=["Summer Resort", "Agriculture", "Heritage"],
                key_investments=["Tourism development", "Rose cultivation", "Heritage preservation"],
                connectivity_priority="medium",
                giga_projects=[]
            ),
            StrategicNode(
                name="AlUla",
                name_ar="العلا",
                region="Madinah",
                tier=3,
                node_type="tourism",
                population_2024=0.05,
                population_2050_target=0.15,
                primary_functions=["Heritage Tourism", "Cultural Destination", "Arts"],
                key_investments=["Heritage development", "Airport", "Hospitality"],
                connectivity_priority="high",
                giga_projects=["AlUla Development"]
            ),
            StrategicNode(
                name="Najran",
                name_ar="نجران",
                region="Najran",
                tier=3,
                node_type="economic",
                population_2024=0.4,
                population_2050_target=0.55,
                primary_functions=["Heritage City", "Agriculture", "Border Trade"],
                key_investments=["Heritage preservation", "Agricultural development"],
                connectivity_priority="low",
                giga_projects=[]
            ),
            StrategicNode(
                name="Al-Baha",
                name_ar="الباحة",
                region="Al-Baha",
                tier=3,
                node_type="tourism",
                population_2024=0.25,
                population_2050_target=0.35,
                primary_functions=["Mountain Tourism", "Heritage", "Agriculture"],
                key_investments=["Tourism infrastructure", "Heritage preservation"],
                connectivity_priority="low",
                giga_projects=[]
            )
        ]
        
        return nodes
    
    def _build_development_corridors(self) -> List[DevelopmentCorridor]:
        """Build the development corridors."""
        
        corridors = [
            # CENTRAL CORRIDOR - Riyadh hub connectivity
            DevelopmentCorridor(
                name="Central Economic Corridor",
                name_ar="الممر الاقتصادي الأوسط",
                corridor_type="economic",
                origin_node="Riyadh",
                destination_node="Dammam",
                intermediate_nodes=["Al-Kharj"],
                length_km=450,
                infrastructure_components=["High-speed rail", "Highway upgrade", "Fiber backbone", "Industrial zones"],
                economic_sectors=["Finance", "Technology", "Logistics", "Manufacturing"],
                investment_sar_billion=85,
                priority="critical",
                timeline="2025-2035"
            ),
            
            # RED SEA CORRIDOR - Western coast development
            DevelopmentCorridor(
                name="Red Sea Tourism Corridor",
                name_ar="ممر البحر الأحمر السياحي",
                corridor_type="tourism",
                origin_node="NEOM",
                destination_node="Jeddah",
                intermediate_nodes=["Tabuk City", "AlUla", "Yanbu"],
                length_km=1200,
                infrastructure_components=["Coastal highway", "Rail link", "Airports", "Marinas"],
                economic_sectors=["Tourism", "Hospitality", "Entertainment", "Creative Industries"],
                investment_sar_billion=150,
                priority="critical",
                timeline="2025-2040"
            ),
            
            # HOLY CITIES CORRIDOR
            DevelopmentCorridor(
                name="Holy Cities Corridor",
                name_ar="ممر المدن المقدسة",
                corridor_type="mixed",
                origin_node="Makkah",
                destination_node="Madinah",
                intermediate_nodes=["Jeddah"],
                length_km=450,
                infrastructure_components=["Haramain Rail (existing)", "Highway upgrade", "Pilgrim services"],
                economic_sectors=["Religious Tourism", "Hospitality", "Services", "Real Estate"],
                investment_sar_billion=40,
                priority="critical",
                timeline="2025-2030"
            ),
            
            # NORTHERN MINING CORRIDOR
            DevelopmentCorridor(
                name="Northern Mining & Energy Corridor",
                name_ar="ممر التعدين والطاقة الشمالي",
                corridor_type="logistics",
                origin_node="Arar",
                destination_node="Jubail",
                intermediate_nodes=["Sakaka", "Hail", "Buraydah"],
                length_km=1100,
                infrastructure_components=["Freight rail", "Mining roads", "Power grid", "Solar farms"],
                economic_sectors=["Mining", "Renewable Energy", "Logistics", "Processing"],
                investment_sar_billion=95,
                priority="high",
                timeline="2025-2040"
            ),
            
            # SOUTHERN DEVELOPMENT CORRIDOR
            DevelopmentCorridor(
                name="Southern Tourism & Agriculture Corridor",
                name_ar="ممر السياحة والزراعة الجنوبي",
                corridor_type="mixed",
                origin_node="Abha",
                destination_node="Jazan City",
                intermediate_nodes=["Al-Baha", "Najran"],
                length_km=600,
                infrastructure_components=["Mountain roads", "Regional airports", "Tourism infrastructure"],
                economic_sectors=["Tourism", "Agriculture", "Coffee", "Handicrafts"],
                investment_sar_billion=35,
                priority="medium",
                timeline="2030-2045"
            ),
            
            # LAND BRIDGE - Red Sea to Gulf
            DevelopmentCorridor(
                name="Trans-Arabia Land Bridge",
                name_ar="الجسر البري عبر الجزيرة",
                corridor_type="logistics",
                origin_node="Jeddah",
                destination_node="Dammam",
                intermediate_nodes=["Riyadh"],
                length_km=1200,
                infrastructure_components=["Freight rail", "Container terminals", "Dry ports", "Logistics hubs"],
                economic_sectors=["Logistics", "Trade", "Manufacturing", "E-commerce"],
                investment_sar_billion=120,
                priority="critical",
                timeline="2025-2035"
            )
        ]
        
        return corridors
    
    def _build_functional_zones(self) -> List[FunctionalZone]:
        """Build functional zones."""
        
        zones = [
            # URBAN GROWTH ZONES
            FunctionalZone(
                zone_name="Riyadh Metropolitan Growth Zone",
                zone_type="urban_growth",
                description="Primary national growth pole with controlled expansion",
                area_km2=6500,
                regions_covered=["Riyadh"],
                permitted_uses=["Residential", "Commercial", "Industrial", "Services", "Green spaces"],
                restricted_uses=["Heavy industry", "Mining", "Large-scale agriculture"],
                development_intensity="high",
                environmental_sensitivity="medium"
            ),
            FunctionalZone(
                zone_name="Jeddah-Makkah Urban Agglomeration",
                zone_type="urban_growth",
                description="Western urban corridor with tourism and commerce focus",
                area_km2=4500,
                regions_covered=["Makkah"],
                permitted_uses=["Residential", "Commercial", "Tourism", "Services"],
                restricted_uses=["Heavy industry", "Polluting activities"],
                development_intensity="high",
                environmental_sensitivity="high"
            ),
            FunctionalZone(
                zone_name="Eastern Province Industrial-Urban Zone",
                zone_type="urban_growth",
                description="Polycentric industrial and residential development",
                area_km2=5000,
                regions_covered=["Eastern Province"],
                permitted_uses=["Industrial", "Residential", "Commercial", "Port facilities"],
                restricted_uses=["Large-scale agriculture"],
                development_intensity="high",
                environmental_sensitivity="high"
            ),
            
            # INDUSTRIAL ZONES
            FunctionalZone(
                zone_name="NEOM Innovation Zone",
                zone_type="industrial",
                description="Future technology and sustainable industry hub",
                area_km2=26500,
                regions_covered=["Tabuk"],
                permitted_uses=["Clean technology", "Tourism", "Research", "Sustainable living"],
                restricted_uses=["Polluting industry", "Traditional energy"],
                development_intensity="medium",
                environmental_sensitivity="high"
            ),
            FunctionalZone(
                zone_name="Northern Mining Belt",
                zone_type="industrial",
                description="Mining and mineral processing zone",
                area_km2=35000,
                regions_covered=["Northern Borders", "Al-Jouf", "Hail"],
                permitted_uses=["Mining", "Processing", "Renewable energy"],
                restricted_uses=["Residential (outside designated areas)", "Tourism"],
                development_intensity="low",
                environmental_sensitivity="medium"
            ),
            
            # AGRICULTURAL ZONES
            FunctionalZone(
                zone_name="Central Agricultural Zone",
                zone_type="agricultural",
                description="Modernized agriculture with water efficiency requirements",
                area_km2=45000,
                regions_covered=["Al-Qassim", "Riyadh (rural)"],
                permitted_uses=["Smart agriculture", "Agri-tech", "Food processing"],
                restricted_uses=["Water-intensive crops", "Urban expansion"],
                development_intensity="low",
                environmental_sensitivity="medium"
            ),
            FunctionalZone(
                zone_name="Southern Agricultural Terraces",
                zone_type="agricultural",
                description="Mountain agriculture and specialty crops",
                area_km2=15000,
                regions_covered=["Asir", "Al-Baha", "Jazan"],
                permitted_uses=["Traditional agriculture", "Coffee", "Fruit orchards", "Agri-tourism"],
                restricted_uses=["Industrial agriculture", "Large-scale development"],
                development_intensity="low",
                environmental_sensitivity="high"
            ),
            
            # PROTECTED ZONES
            FunctionalZone(
                zone_name="Red Sea Marine Protected Area",
                zone_type="protected",
                description="Marine conservation with controlled eco-tourism",
                area_km2=28000,  # Sea area
                regions_covered=["Tabuk", "Madinah", "Makkah"],
                permitted_uses=["Conservation", "Research", "Eco-tourism", "Sustainable fishing"],
                restricted_uses=["Industrial activity", "Large-scale development", "Dredging"],
                development_intensity="minimal",
                environmental_sensitivity="high"
            ),
            FunctionalZone(
                zone_name="Asir-Sarawat Protected Highlands",
                zone_type="protected",
                description="Mountain ecosystem conservation",
                area_km2=18000,
                regions_covered=["Asir", "Al-Baha"],
                permitted_uses=["Conservation", "Hiking", "Eco-tourism", "Research"],
                restricted_uses=["Urban development", "Mining", "Industrial activity"],
                development_intensity="minimal",
                environmental_sensitivity="high"
            ),
            FunctionalZone(
                zone_name="Empty Quarter Conservation Zone",
                zone_type="protected",
                description="Desert ecosystem and cultural landscape protection",
                area_km2=250000,
                regions_covered=["Riyadh", "Eastern Province", "Najran"],
                permitted_uses=["Conservation", "Research", "Controlled tourism", "Renewable energy"],
                restricted_uses=["Urban development", "Water extraction", "Industrial activity"],
                development_intensity="minimal",
                environmental_sensitivity="medium"
            ),
            
            # TOURISM ZONES
            FunctionalZone(
                zone_name="AlUla Heritage Tourism Zone",
                zone_type="tourism",
                description="World-class heritage and cultural tourism destination",
                area_km2=22000,
                regions_covered=["Madinah"],
                permitted_uses=["Heritage tourism", "Cultural facilities", "Eco-lodges", "Arts"],
                restricted_uses=["Heavy industry", "Large-scale agriculture", "Mass housing"],
                development_intensity="low",
                environmental_sensitivity="high"
            ),
            FunctionalZone(
                zone_name="Red Sea Tourism Development Zone",
                zone_type="tourism",
                description="Luxury coastal tourism and eco-resorts",
                area_km2=34000,  # Including islands
                regions_covered=["Tabuk", "Madinah"],
                permitted_uses=["Resort development", "Marinas", "Eco-tourism", "Water sports"],
                restricted_uses=["Industrial activity", "Mass housing", "Polluting uses"],
                development_intensity="low",
                environmental_sensitivity="high"
            )
        ]
        
        return zones
    
    def get_nodes(self) -> List[StrategicNode]:
        return self.nodes
    
    def get_corridors(self) -> List[DevelopmentCorridor]:
        return self.corridors
    
    def get_zones(self) -> List[FunctionalZone]:
        return self.zones
    
    def get_nodes_by_tier(self, tier: int) -> List[StrategicNode]:
        return [n for n in self.nodes if n.tier == tier]


# =============================================================================
# REGIONAL OBJECTIVES BUILDER
# =============================================================================

class RegionalObjectivesBuilder:
    """
    Builds strategic objectives for each of the 13 regions.
    """
    
    def __init__(self):
        """Initialize regional objectives builder."""
        self.objectives = self._build_regional_objectives()
        logger.info(f"Regional Objectives: {len(self.objectives)} regions")
    
    def _build_regional_objectives(self) -> Dict[str, RegionalObjective]:
        """Build objectives for all 13 regions."""
        
        objectives = {}
        
        objectives['Riyadh'] = RegionalObjective(
            region="Riyadh",
            region_ar="الرياض",
            strategic_role="National Capital & Economic Powerhouse",
            vision_statement="A world-class capital city that leads the nation's transformation while providing exceptional quality of life for all residents",
            population_target_2050=15.0,
            gdp_share_target_2050=45.0,
            priority_sectors=["Financial Services", "Technology", "Entertainment", "Government", "Tourism"],
            key_projects=["Riyadh Metro completion", "Diriyah Gate", "Qiddiya", "King Salman Park", "Sports Boulevard"],
            infrastructure_priorities=["Metro expansion", "Water recycling 100%", "Green corridors", "Smart city systems"],
            environmental_targets={"green_space_per_capita_sqm": 12, "water_recycling_pct": 100, "renewable_energy_pct": 50},
            complementarities=["Financial center for all regions", "Entertainment destination", "Technology hub"],
            challenges=["Water scarcity", "Urban heat island", "Traffic congestion", "Housing affordability"]
        )
        
        objectives['Makkah'] = RegionalObjective(
            region="Makkah",
            region_ar="مكة المكرمة",
            strategic_role="Spiritual Heart & Western Gateway",
            vision_statement="The spiritual center of the Muslim world with a thriving commercial economy and preserved heritage",
            population_target_2050=12.0,
            gdp_share_target_2050=18.0,
            priority_sectors=["Religious Tourism", "Hospitality", "Trade", "Logistics", "Healthcare"],
            key_projects=["Haram expansion", "Jeddah Central", "Port modernization", "Metro systems"],
            infrastructure_priorities=["Pilgrim transport", "Flood protection", "Port expansion", "Water security"],
            environmental_targets={"green_space_per_capita_sqm": 6, "water_recycling_pct": 80, "coastal_protection_km": 200},
            complementarities=["Religious tourism for all", "Commercial gateway", "Red Sea access"],
            challenges=["Peak season management", "Flood risk", "Heritage preservation", "Housing density"]
        )
        
        objectives['Eastern Province'] = RegionalObjective(
            region="Eastern Province",
            region_ar="المنطقة الشرقية",
            strategic_role="Industrial Powerhouse & Energy Transition Leader",
            vision_statement="Transform from oil capital to diversified industrial leader, pioneering the energy transition",
            population_target_2050=8.0,
            gdp_share_target_2050=22.0,
            priority_sectors=["Petrochemicals", "Manufacturing", "Green Hydrogen", "Technology", "Tourism"],
            key_projects=["SPARK", "Industrial diversification", "Waterfront development", "Green hydrogen"],
            infrastructure_priorities=["Industrial infrastructure", "Port expansion", "Rail connectivity", "Renewable energy"],
            environmental_targets={"green_space_per_capita_sqm": 10, "water_recycling_pct": 90, "renewable_energy_pct": 60},
            complementarities=["Industrial services for nation", "Energy expertise", "Gulf connectivity"],
            challenges=["Economic diversification", "Environmental cleanup", "Workforce transition"]
        )
        
        objectives['Madinah'] = RegionalObjective(
            region="Madinah",
            region_ar="المدينة المنورة",
            strategic_role="Holy City & Cultural Heritage Capital",
            vision_statement="A sacred city that welcomes pilgrims while becoming the premier cultural tourism destination",
            population_target_2050=3.5,
            gdp_share_target_2050=6.0,
            priority_sectors=["Religious Tourism", "Cultural Tourism", "Agriculture", "Industry"],
            key_projects=["AlUla Development", "Prophet's Mosque surroundings", "Yanbu expansion"],
            infrastructure_priorities=["Tourism infrastructure", "Water security", "Connectivity to AlUla"],
            environmental_targets={"green_space_per_capita_sqm": 8, "heritage_sites_protected": 100, "water_recycling_pct": 75},
            complementarities=["Religious tourism synergy with Makkah", "Cultural tourism leader", "Industrial port at Yanbu"],
            challenges=["Water scarcity", "Heritage preservation", "Seasonal demand fluctuation"]
        )
        
        objectives['Tabuk'] = RegionalObjective(
            region="Tabuk",
            region_ar="تبوك",
            strategic_role="Future City & Tourism Frontier",
            vision_statement="Home to NEOM, the world's most ambitious sustainable development, and gateway to Red Sea wonders",
            population_target_2050=3.5,
            gdp_share_target_2050=8.0,
            priority_sectors=["NEOM Industries", "Tourism", "Technology", "Renewable Energy", "Sustainable Agriculture"],
            key_projects=["NEOM (The Line, Trojena, Oxagon)", "Red Sea Project", "AMAALA"],
            infrastructure_priorities=["NEOM infrastructure", "Airports", "Desalination", "Renewable energy"],
            environmental_targets={"protected_area_pct": 50, "renewable_energy_pct": 100, "zero_carbon_target": 2040},
            complementarities=["Innovation laboratory for nation", "Tourism anchor", "Sustainability model"],
            challenges=["Execution risk", "Labor availability", "Environmental sensitivity", "Remote location"]
        )
        
        objectives['Asir'] = RegionalObjective(
            region="Asir",
            region_ar="عسير",
            strategic_role="Mountain Tourism & Agricultural Heritage",
            vision_statement="Saudi Arabia's premier domestic tourism destination celebrating mountain culture and natural beauty",
            population_target_2050=3.0,
            gdp_share_target_2050=3.5,
            priority_sectors=["Tourism", "Agriculture", "Handicrafts", "Healthcare"],
            key_projects=["Asir Development", "Tourism infrastructure", "Heritage preservation"],
            infrastructure_priorities=["Mountain roads", "Cable cars", "Airports", "Tourism facilities"],
            environmental_targets={"protected_area_pct": 30, "forest_conservation_pct": 90, "water_harvesting_capacity_mcm": 50},
            complementarities=["Domestic tourism escape", "Agricultural diversity", "Cultural heritage"],
            challenges=["Accessibility", "Seasonal demand", "Infrastructure in terrain", "Brain drain"]
        )
        
        objectives['Al-Qassim'] = RegionalObjective(
            region="Al-Qassim",
            region_ar="القصيم",
            strategic_role="Agricultural Innovation Hub",
            vision_statement="Transform from water-depleting agriculture to model of sustainable, high-tech food production",
            population_target_2050=2.0,
            gdp_share_target_2050=2.5,
            priority_sectors=["Smart Agriculture", "Food Processing", "Logistics", "Solar Energy"],
            key_projects=["Agricultural transformation", "Solar farms", "Food processing cluster"],
            infrastructure_priorities=["Water efficiency", "Solar energy", "Logistics connectivity", "Agri-tech facilities"],
            environmental_targets={"water_consumption_reduction_pct": 50, "solar_capacity_gw": 10, "groundwater_balance": "neutral"},
            complementarities=["Food security for nation", "Agricultural expertise", "Central location"],
            challenges=["CRITICAL water depletion", "Crop transition", "Economic diversification"]
        )
        
        objectives['Hail'] = RegionalObjective(
            region="Hail",
            region_ar="حائل",
            strategic_role="Agricultural & Mining Development Hub",
            vision_statement="Leverage mining potential and agricultural heritage for sustainable regional growth",
            population_target_2050=1.0,
            gdp_share_target_2050=1.5,
            priority_sectors=["Mining", "Agriculture", "Renewable Energy", "Tourism"],
            key_projects=["Mining development", "Agricultural modernization", "Heritage tourism"],
            infrastructure_priorities=["Mining roads", "Water efficiency", "Rail connectivity"],
            environmental_targets={"water_efficiency_improvement_pct": 40, "mining_rehabilitation_pct": 100},
            complementarities=["Mining corridor link", "Agricultural production", "Heritage sites"],
            challenges=["Water scarcity", "Remote location", "Small market size"]
        )
        
        objectives['Northern Borders'] = RegionalObjective(
            region="Northern Borders",
            region_ar="الحدود الشمالية",
            strategic_role="Mining & Renewable Energy Frontier",
            vision_statement="The nation's mining and clean energy powerhouse, transforming resources into sustainable prosperity",
            population_target_2050=0.8,
            gdp_share_target_2050=2.0,
            priority_sectors=["Mining", "Renewable Energy", "Industrial Processing", "Border Trade"],
            key_projects=["Waad Al-Shamal expansion", "Solar mega-farms", "Phosphate processing"],
            infrastructure_priorities=["Mining rail", "Power grid", "Processing facilities", "Cross-border links"],
            environmental_targets={"renewable_energy_capacity_gw": 15, "mining_rehabilitation_pct": 100},
            complementarities=["Mineral supply for nation", "Renewable energy export", "Northern gateway"],
            challenges=["Remote location", "Harsh climate", "Labor availability", "Infrastructure gaps"]
        )
        
        objectives['Jazan'] = RegionalObjective(
            region="Jazan",
            region_ar="جازان",
            strategic_role="Tropical Agriculture & Economic Diversification",
            vision_statement="Leverage unique climate for agricultural excellence and become Red Sea industrial hub",
            population_target_2050=2.2,
            gdp_share_target_2050=1.8,
            priority_sectors=["Agriculture", "Industry", "Tourism", "Fishing"],
            key_projects=["Jazan Economic City", "Agricultural development", "Farasan tourism"],
            infrastructure_priorities=["Economic city completion", "Port development", "Agricultural infrastructure"],
            environmental_targets={"marine_protected_area_pct": 30, "agricultural_diversity_index": "high"},
            complementarities=["Tropical agriculture", "Red Sea industry", "Island tourism"],
            challenges=["Economic city completion", "Flood risk", "Border proximity"]
        )
        
        objectives['Najran'] = RegionalObjective(
            region="Najran",
            region_ar="نجران",
            strategic_role="Heritage Preservation & Agricultural Oasis",
            vision_statement="Preserve unique cultural heritage while developing sustainable agriculture and tourism",
            population_target_2050=0.75,
            gdp_share_target_2050=0.8,
            priority_sectors=["Heritage Tourism", "Agriculture", "Trade"],
            key_projects=["Ukhdood site development", "Agricultural modernization", "Heritage preservation"],
            infrastructure_priorities=["Heritage facilities", "Water management", "Connectivity"],
            environmental_targets={"heritage_sites_preserved": 100, "water_efficiency_pct": 60},
            complementarities=["Archaeological tourism", "Agricultural tradition", "Border trade"],
            challenges=["Border security", "Remote location", "Small economy"]
        )
        
        objectives['Al-Baha'] = RegionalObjective(
            region="Al-Baha",
            region_ar="الباحة",
            strategic_role="Mountain Retreat & Heritage Village",
            vision_statement="A preserved mountain heritage region offering unique domestic tourism experiences",
            population_target_2050=0.6,
            gdp_share_target_2050=0.6,
            priority_sectors=["Tourism", "Agriculture", "Handicrafts", "Honey Production"],
            key_projects=["Tourism development", "Heritage village preservation", "Road improvements"],
            infrastructure_priorities=["Tourism infrastructure", "Road access", "Heritage preservation"],
            environmental_targets={"forest_preservation_pct": 90, "heritage_villages_preserved": 50},
            complementarities=["Asir tourism synergy", "Unique heritage", "Agricultural products"],
            challenges=["Small size", "Terrain challenges", "Infrastructure cost"]
        )
        
        objectives['Al-Jouf'] = RegionalObjective(
            region="Al-Jouf",
            region_ar="الجوف",
            strategic_role="Renewable Energy Hub & Agricultural Innovation",
            vision_statement="Become Saudi Arabia's renewable energy capital while modernizing olive and agricultural production",
            population_target_2050=0.85,
            gdp_share_target_2050=1.3,
            priority_sectors=["Renewable Energy", "Agriculture", "Tourism", "Mining"],
            key_projects=["Solar mega-farms", "Olive processing", "Heritage tourism", "Wind farms"],
            infrastructure_priorities=["Renewable energy grid", "Water efficiency", "Tourism access"],
            environmental_targets={"renewable_capacity_gw": 20, "water_efficiency_improvement_pct": 45},
            complementarities=["Renewable energy for grid", "Agricultural exports", "Heritage sites"],
            challenges=["Water scarcity", "Remote location", "Infrastructure needs"]
        )
        
        return objectives
    
    def get_objectives(self) -> Dict[str, RegionalObjective]:
        return self.objectives
    
    def get_region(self, region: str) -> Optional[RegionalObjective]:
        return self.objectives.get(region)


# =============================================================================
# INVESTMENT PRIORITIES BUILDER
# =============================================================================

class InvestmentPrioritiesBuilder:
    """
    Builds investment priorities and sequencing.
    """
    
    def __init__(self):
        """Initialize investment priorities builder."""
        self.priorities = self._build_investment_priorities()
        logger.info(f"Investment Priorities: {len(self.priorities)} items")
    
    def _build_investment_priorities(self) -> List[InvestmentPriority]:
        """Build prioritized investment list."""
        
        priorities = [
            # CRITICAL INFRASTRUCTURE
            InvestmentPriority(
                priority_id="IP-001",
                title="National Water Security Program",
                category="infrastructure",
                description="Massive expansion of desalination, 100% wastewater reuse, agricultural water efficiency",
                estimated_cost_sar_billion=150,
                timeline="2025-2035",
                regions_benefited=["All regions"],
                expected_outcomes=["40% reduction in water consumption", "Eliminate groundwater overdraft", "100% reuse"],
                funding_sources=["Government budget", "PIF", "PPP for desalination"],
                implementation_agency="Ministry of Environment, Water and Agriculture"
            ),
            InvestmentPriority(
                priority_id="IP-002",
                title="National Rail Network Completion",
                category="infrastructure",
                description="Complete freight and passenger rail connecting all major cities",
                estimated_cost_sar_billion=200,
                timeline="2025-2040",
                regions_benefited=["All regions"],
                expected_outcomes=["5,500 km rail network", "All tier-1 cities connected", "50% freight shift to rail"],
                funding_sources=["Government budget", "PIF", "PPP"],
                implementation_agency="Saudi Railway Company"
            ),
            InvestmentPriority(
                priority_id="IP-003",
                title="Renewable Energy Mega-Program",
                category="infrastructure",
                description="Achieve 100GW renewable capacity with grid integration",
                estimated_cost_sar_billion=180,
                timeline="2025-2040",
                regions_benefited=["Tabuk", "Northern Borders", "Al-Jouf", "Hail"],
                expected_outcomes=["100GW capacity", "50% domestic energy from renewables", "Green hydrogen export"],
                funding_sources=["PIF", "Private sector", "International investment"],
                implementation_agency="Ministry of Energy"
            ),
            
            # TRANSFORMATIONAL PROJECTS
            InvestmentPriority(
                priority_id="IP-004",
                title="NEOM Phase 1 Completion",
                category="economic",
                description="Complete The Line, Trojena, Oxagon, and Sindalah by 2035",
                estimated_cost_sar_billion=500,
                timeline="2025-2035",
                regions_benefited=["Tabuk"],
                expected_outcomes=["1M residents in The Line", "Trojena ski resort operational", "Oxagon port operational"],
                funding_sources=["PIF"],
                implementation_agency="NEOM Company"
            ),
            InvestmentPriority(
                priority_id="IP-005",
                title="Red Sea & AMAALA Tourism",
                category="economic",
                description="Complete luxury tourism destinations on Red Sea coast",
                estimated_cost_sar_billion=75,
                timeline="2025-2035",
                regions_benefited=["Tabuk", "Madinah"],
                expected_outcomes=["50 resorts", "30,000 hotel rooms", "8,000 jobs"],
                funding_sources=["PIF", "Private investors"],
                implementation_agency="Red Sea Global"
            ),
            InvestmentPriority(
                priority_id="IP-006",
                title="AlUla Heritage Development",
                category="economic",
                description="World-class heritage tourism destination development",
                estimated_cost_sar_billion=35,
                timeline="2025-2035",
                regions_benefited=["Madinah"],
                expected_outcomes=["UNESCO site protection", "2M annual visitors", "Sustainable tourism model"],
                funding_sources=["PIF", "Royal Commission for AlUla"],
                implementation_agency="Royal Commission for AlUla"
            ),
            
            # REGIONAL DEVELOPMENT
            InvestmentPriority(
                priority_id="IP-007",
                title="Agricultural Transformation Program",
                category="economic",
                description="Transform water-intensive agriculture to sustainable, high-tech production",
                estimated_cost_sar_billion=45,
                timeline="2025-2035",
                regions_benefited=["Al-Qassim", "Hail", "Al-Jouf", "Riyadh"],
                expected_outcomes=["50% water reduction", "Crop transition complete", "Agri-tech leadership"],
                funding_sources=["Government subsidies", "Environment Fund", "Private sector"],
                implementation_agency="Ministry of Environment, Water and Agriculture"
            ),
            InvestmentPriority(
                priority_id="IP-008",
                title="Mining Sector Development",
                category="economic",
                description="Develop mining sector to SAR 240B contribution",
                estimated_cost_sar_billion=60,
                timeline="2025-2040",
                regions_benefited=["Northern Borders", "Madinah", "Hail", "Tabuk"],
                expected_outcomes=["3% GDP contribution", "90,000 jobs", "Downstream processing"],
                funding_sources=["Private investment", "Ma'aden", "PIF"],
                implementation_agency="Ministry of Industry and Mineral Resources"
            ),
            InvestmentPriority(
                priority_id="IP-009",
                title="Asir Tourism Development",
                category="economic",
                description="Develop Asir as premier domestic tourism destination",
                estimated_cost_sar_billion=25,
                timeline="2025-2035",
                regions_benefited=["Asir", "Al-Baha"],
                expected_outcomes=["5M annual visitors", "Heritage preservation", "Mountain resorts"],
                funding_sources=["Government budget", "Private sector"],
                implementation_agency="Ministry of Tourism"
            ),
            
            # SOCIAL INFRASTRUCTURE
            InvestmentPriority(
                priority_id="IP-010",
                title="National Housing Program",
                category="social",
                description="Achieve 70% Saudi home ownership through affordable housing",
                estimated_cost_sar_billion=100,
                timeline="2025-2035",
                regions_benefited=["All regions"],
                expected_outcomes=["70% ownership", "500,000 affordable units", "TOD communities"],
                funding_sources=["Real Estate Development Fund", "PIF", "Private sector"],
                implementation_agency="Ministry of Housing"
            ),
            InvestmentPriority(
                priority_id="IP-011",
                title="Urban Green Infrastructure",
                category="environmental",
                description="Achieve 9 sqm green space per capita in all cities",
                estimated_cost_sar_billion=40,
                timeline="2025-2040",
                regions_benefited=["All regions"],
                expected_outcomes=["9 sqm per capita", "Urban forests", "Heat island reduction"],
                funding_sources=["Municipal budgets", "Green Fund"],
                implementation_agency="Ministry of Municipal and Rural Affairs"
            ),
            InvestmentPriority(
                priority_id="IP-012",
                title="Protected Areas Expansion",
                category="environmental",
                description="Expand protected areas to 30% of land and sea by 2030",
                estimated_cost_sar_billion=15,
                timeline="2025-2030",
                regions_benefited=["All regions"],
                expected_outcomes=["30% land protected", "30% sea protected", "Wildlife corridors"],
                funding_sources=["Government budget", "International funds"],
                implementation_agency="National Center for Wildlife"
            )
        ]
        
        return priorities
    
    def get_priorities(self) -> List[InvestmentPriority]:
        return self.priorities
    
    def get_by_category(self, category: str) -> List[InvestmentPriority]:
        return [p for p in self.priorities if p.category == category]
    
    def calculate_total_investment(self) -> Dict[str, Any]:
        """Calculate total investment by category."""
        total = sum(p.estimated_cost_sar_billion for p in self.priorities)
        by_category = {}
        for p in self.priorities:
            by_category[p.category] = by_category.get(p.category, 0) + p.estimated_cost_sar_billion
        
        return {
            "total_sar_billion": total,
            "by_category": by_category,
            "priority_count": len(self.priorities)
        }


# =============================================================================
# STAKEHOLDER MATERIALS GENERATOR
# =============================================================================

class StakeholderMaterialsGenerator:
    """
    Generates stakeholder engagement materials.
    """
    
    def __init__(self, vision: NSSVision, structure: SpatialStructureBuilder, 
                 objectives: RegionalObjectivesBuilder, investments: InvestmentPrioritiesBuilder):
        """Initialize with all NSS components."""
        self.vision = vision
        self.structure = structure
        self.objectives = objectives
        self.investments = investments
        logger.info("Stakeholder Materials Generator initialized")
    
    def generate_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary for decision makers."""
        
        return {
            "title": "National Spatial Strategy - Executive Summary",
            "subtitle": "Saudi Arabia 2050: A Vision for Balanced Territorial Development",
            "for": "Royal Court, Council of Ministers, Regional Governors",
            "sections": [
                {
                    "title": "Vision",
                    "content": self.vision.vision_statement
                },
                {
                    "title": "Strategic Objectives",
                    "content": [obj["objective"] for obj in self.vision.strategic_objectives]
                },
                {
                    "title": "Spatial Structure",
                    "content": {
                        "strategic_nodes": len(self.structure.get_nodes()),
                        "development_corridors": len(self.structure.get_corridors()),
                        "functional_zones": len(self.structure.get_zones())
                    }
                },
                {
                    "title": "Investment Required",
                    "content": self.investments.calculate_total_investment()
                },
                {
                    "title": "Key Actions",
                    "content": [
                        "Establish NSS Coordination Authority",
                        "Approve spatial structure and zoning",
                        "Prioritize water security investments",
                        "Align sectoral strategies with NSS"
                    ]
                }
            ]
        }
    
    def generate_public_consultation_materials(self) -> Dict[str, Any]:
        """Generate materials for public consultation."""
        
        return {
            "title": "Shape Your Country's Future",
            "subtitle": "Public Consultation on National Spatial Strategy 2050",
            "key_messages": [
                "Your voice matters in shaping where and how Saudi Arabia develops",
                "We want to hear about your region's needs and opportunities",
                "The NSS will guide development for the next 25 years"
            ],
            "consultation_topics": [
                {
                    "topic": "Quality of Life",
                    "questions": [
                        "What services are missing in your community?",
                        "How can we improve your neighborhood?",
                        "What would make your daily life better?"
                    ]
                },
                {
                    "topic": "Economic Opportunities",
                    "questions": [
                        "What industries should develop in your region?",
                        "How can we create more local jobs?",
                        "What skills training is needed?"
                    ]
                },
                {
                    "topic": "Environment",
                    "questions": [
                        "What natural areas should be protected?",
                        "How can we address water scarcity?",
                        "What green spaces are needed in cities?"
                    ]
                },
                {
                    "topic": "Connectivity",
                    "questions": [
                        "How can transport be improved?",
                        "What digital services are needed?",
                        "How can we better connect regions?"
                    ]
                }
            ],
            "feedback_channels": [
                "Online portal: nss.gov.sa",
                "Regional workshops in all 13 regions",
                "Written submissions",
                "Municipal office feedback forms"
            ],
            "timeline": "90-day consultation period"
        }
    
    def generate_faq(self) -> List[Dict[str, str]]:
        """Generate FAQ document."""
        
        return [
            {
                "question": "What is the National Spatial Strategy (NSS)?",
                "answer": "The NSS is a comprehensive plan that guides where and how development occurs across Saudi Arabia until 2050. It coordinates land use, infrastructure, economic development, and environmental protection across all 13 regions."
            },
            {
                "question": "How does the NSS relate to Vision 2030?",
                "answer": "The NSS translates Vision 2030's ambitious goals into spatial reality. It identifies where giga-projects, cities, corridors, and protected areas will be located to achieve Vision 2030 targets in a coordinated way."
            },
            {
                "question": "What are the main goals of the NSS?",
                "answer": "The NSS aims to: (1) Balance development across all 13 regions, (2) Ensure water security, (3) Connect regions with transport corridors, (4) Protect the environment, (5) Improve quality of life for all Saudis."
            },
            {
                "question": "How will my region benefit?",
                "answer": "Every region has a specific role and investment priorities in the NSS. Check the Regional Objectives section for your region's strategic role, priority sectors, and planned infrastructure investments."
            },
            {
                "question": "How much investment is planned?",
                "answer": "The NSS identifies over SAR 1.4 trillion in priority investments across infrastructure, economic development, social services, and environmental protection over 25 years."
            },
            {
                "question": "Who is responsible for implementing the NSS?",
                "answer": "A National NSS Coordination Authority will oversee implementation, working with line ministries, regional authorities, and the private sector. Each ministry has specific responsibilities defined in the Governance Framework."
            },
            {
                "question": "How can I participate?",
                "answer": "Public consultation is open for 90 days. You can provide feedback through the online portal (nss.gov.sa), attend regional workshops, or submit written comments to your local municipality."
            },
            {
                "question": "Will the NSS affect my property?",
                "answer": "The NSS provides high-level guidance that will be detailed through regional and local plans. Specific zoning changes will go through proper legal processes with affected communities consulted."
            },
            {
                "question": "How will water scarcity be addressed?",
                "answer": "Water security is the #1 priority. The NSS mandates: 40% reduction in consumption, 100% wastewater reuse, expansion of desalination, and transition away from water-intensive agriculture."
            },
            {
                "question": "How will the NSS be monitored?",
                "answer": "A comprehensive KPI framework tracks progress annually. Bi-annual reviews assess performance and the strategy will be updated every 5 years based on changing conditions."
            }
        ]


# =============================================================================
# WS6 REPORT GENERATOR
# =============================================================================

class WS6ReportGenerator:
    """
    Generates all WS6 deliverables.
    """
    
    def __init__(self, output_dir: str = "02_analytics/ws6_outputs"):
        """Initialize report generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize all components
        self.vision_builder = NSSVisionBuilder()
        self.structure_builder = SpatialStructureBuilder()
        self.objectives_builder = RegionalObjectivesBuilder()
        self.investments_builder = InvestmentPrioritiesBuilder()
        self.stakeholder_gen = StakeholderMaterialsGenerator(
            self.vision_builder.get_vision(),
            self.structure_builder,
            self.objectives_builder,
            self.investments_builder
        )
        
        logger.info(f"WS6 Report Generator initialized. Output: {self.output_dir}")
    
    def generate_all_reports(self) -> Dict[str, Any]:
        """Generate all WS6 deliverables."""
        
        logger.info("Generating WS6 deliverables...")
        
        # Get all data
        vision = self.vision_builder.get_vision()
        nodes = self.structure_builder.get_nodes()
        corridors = self.structure_builder.get_corridors()
        zones = self.structure_builder.get_zones()
        objectives = self.objectives_builder.get_objectives()
        investments = self.investments_builder.get_priorities()
        
        # Save spatial structure CSVs
        nodes_df = pd.DataFrame([{
            'Name': n.name,
            'Region': n.region,
            'Tier': n.tier,
            'Type': n.node_type,
            'Pop_2024_M': n.population_2024,
            'Pop_2050_M': n.population_2050_target,
            'Functions': ', '.join(n.primary_functions[:3]),
            'Priority': n.connectivity_priority,
            'Lat': CITY_COORDS.get(n.name, (24.5, 45.0))[0],
            'Lon': CITY_COORDS.get(n.name, (24.5, 45.0))[1]
        } for n in nodes])
        nodes_df.to_csv(self.output_dir / "strategic_nodes.csv", index=False)
        
        corridors_df = pd.DataFrame([{
            'Name': c.name,
            'Type': c.corridor_type,
            'Origin': c.origin_node,
            'Destination': c.destination_node,
            'Length_km': c.length_km,
            'Investment_SAR_B': c.investment_sar_billion,
            'Priority': c.priority,
            'Timeline': c.timeline,
            'Start_Lat': CORRIDOR_COORDS.get(c.name, ((24.5, 45.0), (25.0, 46.0)))[0][0],
            'Start_Lon': CORRIDOR_COORDS.get(c.name, ((24.5, 45.0), (25.0, 46.0)))[0][1],
            'End_Lat': CORRIDOR_COORDS.get(c.name, ((24.5, 45.0), (25.0, 46.0)))[1][0],
            'End_Lon': CORRIDOR_COORDS.get(c.name, ((24.5, 45.0), (25.0, 46.0)))[1][1]
        } for c in corridors])
        corridors_df.to_csv(self.output_dir / "development_corridors.csv", index=False)
        
        zones_df = pd.DataFrame([{
            'Zone': z.zone_name,
            'Type': z.zone_type,
            'Area_km2': z.area_km2,
            'Regions': ', '.join(z.regions_covered),
            'Intensity': z.development_intensity,
            'Sensitivity': z.environmental_sensitivity
        } for z in zones])
        zones_df.to_csv(self.output_dir / "functional_zones.csv", index=False)
        
        # Save regional objectives
        objectives_df = pd.DataFrame([{
            'Region': obj.region,
            'Strategic_Role': obj.strategic_role,
            'Pop_2050_M': obj.population_target_2050,
            'GDP_Share_2050': obj.gdp_share_target_2050,
            'Priority_Sectors': ', '.join(obj.priority_sectors[:3]),
            'Key_Challenges': ', '.join(obj.challenges[:2])
        } for obj in objectives.values()])
        objectives_df.to_csv(self.output_dir / "regional_objectives.csv", index=False)
        
        # Save investment priorities
        investments_df = pd.DataFrame([{
            'ID': p.priority_id,
            'Title': p.title,
            'Category': p.category,
            'Cost_SAR_B': p.estimated_cost_sar_billion,
            'Timeline': p.timeline,
            'Agency': p.implementation_agency
        } for p in investments])
        investments_df.to_csv(self.output_dir / "investment_priorities.csv", index=False)
        
        # Generate stakeholder materials
        exec_summary = self.stakeholder_gen.generate_executive_summary()
        public_materials = self.stakeholder_gen.generate_public_consultation_materials()
        faq = self.stakeholder_gen.generate_faq()
        
        # Compile comprehensive report
        report = {
            "metadata": {
                "report_title": "WS6 - National Spatial Strategy Draft",
                "generated_date": datetime.now().isoformat(),
                "version": "1.0",
                "author": "NSS X System"
            },
            "section_1_vision": {
                "vision_statement": vision.vision_statement,
                "vision_statement_ar": vision.vision_statement_ar,
                "time_horizon": vision.time_horizon,
                "guiding_principles": vision.guiding_principles,
                "strategic_objectives": vision.strategic_objectives,
                "vision2030_alignment": vision.alignment_with_vision2030
            },
            "section_2_spatial_structure": {
                "summary": {
                    "strategic_nodes": len(nodes),
                    "tier_1_national": len([n for n in nodes if n.tier == 1]),
                    "tier_2_regional": len([n for n in nodes if n.tier == 2]),
                    "tier_3_subregional": len([n for n in nodes if n.tier == 3]),
                    "development_corridors": len(corridors),
                    "functional_zones": len(zones)
                },
                "strategic_nodes": [self._node_to_dict(n) for n in nodes],
                "development_corridors": [self._corridor_to_dict(c) for c in corridors],
                "functional_zones": [self._zone_to_dict(z) for z in zones]
            },
            "section_3_regional_objectives": {
                region: self._objective_to_dict(obj) 
                for region, obj in objectives.items()
            },
            "section_4_investment_priorities": {
                "summary": self.investments_builder.calculate_total_investment(),
                "priorities": [self._investment_to_dict(p) for p in investments]
            },
            "section_5_stakeholder_materials": {
                "executive_summary": exec_summary,
                "public_consultation": public_materials,
                "faq": faq
            },
            "appendices": {
                "output_files": [
                    "WS6_NSS_DRAFT_REPORT.json",
                    "WS6_NSS_DRAFT_REPORT.md",
                    "strategic_nodes.csv",
                    "development_corridors.csv",
                    "functional_zones.csv",
                    "regional_objectives.csv",
                    "investment_priorities.csv"
                ]
            }
        }
        
        # Save JSON report
        report_path = self.output_dir / "WS6_NSS_DRAFT_REPORT.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        logger.success(f"WS6 Report saved to {report_path}")
        
        # Generate markdown report
        self._generate_markdown_report(report)
        
        return report
    
    def _node_to_dict(self, node: StrategicNode) -> Dict:
        # Get coordinates from lookup or use node's own coords
        coords = CITY_COORDS.get(node.name, (node.lat, node.lon))
        lat, lon = coords if coords != (0.0, 0.0) else (24.0, 45.0)  # Default to center of KSA
        
        return {
            "name": node.name,
            "name_ar": node.name_ar,
            "region": node.region,
            "tier": node.tier,
            "type": node.node_type,
            "population_2024": node.population_2024,
            "population_2050": node.population_2050_target,
            "functions": node.primary_functions,
            "investments": node.key_investments,
            "connectivity": node.connectivity_priority,
            "giga_projects": node.giga_projects,
            "lat": lat,
            "lon": lon
        }
    
    def _corridor_to_dict(self, corridor: DevelopmentCorridor) -> Dict:
        # Get coordinates from lookup or use corridor's own coords
        coords = CORRIDOR_COORDS.get(corridor.name, None)
        if coords:
            start_lat, start_lon = coords[0]
            end_lat, end_lon = coords[1]
        else:
            start_lat, start_lon = corridor.start_lat, corridor.start_lon
            end_lat, end_lon = corridor.end_lat, corridor.end_lon
        
        return {
            "name": corridor.name,
            "name_ar": corridor.name_ar,
            "type": corridor.corridor_type,
            "origin": corridor.origin_node,
            "destination": corridor.destination_node,
            "intermediate": corridor.intermediate_nodes,
            "length_km": corridor.length_km,
            "infrastructure": corridor.infrastructure_components,
            "sectors": corridor.economic_sectors,
            "investment_sar_b": corridor.investment_sar_billion,
            "priority": corridor.priority,
            "timeline": corridor.timeline,
            "start_lat": start_lat,
            "start_lon": start_lon,
            "end_lat": end_lat,
            "end_lon": end_lon
        }
    
    def _zone_to_dict(self, zone: FunctionalZone) -> Dict:
        return {
            "name": zone.zone_name,
            "type": zone.zone_type,
            "description": zone.description,
            "area_km2": zone.area_km2,
            "regions": zone.regions_covered,
            "permitted": zone.permitted_uses,
            "restricted": zone.restricted_uses,
            "intensity": zone.development_intensity,
            "sensitivity": zone.environmental_sensitivity
        }
    
    def _objective_to_dict(self, obj: RegionalObjective) -> Dict:
        return {
            "region": obj.region,
            "region_ar": obj.region_ar,
            "strategic_role": obj.strategic_role,
            "vision": obj.vision_statement,
            "population_2050": obj.population_target_2050,
            "gdp_share_2050": obj.gdp_share_target_2050,
            "priority_sectors": obj.priority_sectors,
            "key_projects": obj.key_projects,
            "infrastructure": obj.infrastructure_priorities,
            "environmental_targets": obj.environmental_targets,
            "complementarities": obj.complementarities,
            "challenges": obj.challenges
        }
    
    def _investment_to_dict(self, inv: InvestmentPriority) -> Dict:
        return {
            "id": inv.priority_id,
            "title": inv.title,
            "category": inv.category,
            "description": inv.description,
            "cost_sar_b": inv.estimated_cost_sar_billion,
            "timeline": inv.timeline,
            "regions": inv.regions_benefited,
            "outcomes": inv.expected_outcomes,
            "funding": inv.funding_sources,
            "agency": inv.implementation_agency
        }
    
    def _generate_markdown_report(self, report: Dict):
        """Generate markdown version."""
        
        md_content = f"""# National Spatial Strategy Draft - Saudi Arabia 2050

**Generated:** {report['metadata']['generated_date']}
**Version:** {report['metadata']['version']}

---

## Vision Statement

> {report['section_1_vision']['vision_statement']}

**Arabic:**
> {report['section_1_vision']['vision_statement_ar']}

---

## Guiding Principles

| # | Principle | Description |
|---|-----------|-------------|
"""
        for i, p in enumerate(report['section_1_vision']['guiding_principles'], 1):
            md_content += f"| {i} | **{p['principle']}** | {p['description'][:80]}... |\n"
        
        md_content += """
---

## Strategic Objectives

| ID | Objective | Target 2050 |
|----|-----------|-------------|
"""
        for obj in report['section_1_vision']['strategic_objectives']:
            md_content += f"| {obj['id']} | {obj['objective']} | {obj['target_2050'][:50]}... |\n"
        
        md_content += f"""
---

## National Spatial Structure

### Summary
- **Strategic Nodes:** {report['section_2_spatial_structure']['summary']['strategic_nodes']}
  - Tier 1 (National): {report['section_2_spatial_structure']['summary']['tier_1_national']}
  - Tier 2 (Regional): {report['section_2_spatial_structure']['summary']['tier_2_regional']}
  - Tier 3 (Sub-regional): {report['section_2_spatial_structure']['summary']['tier_3_subregional']}
- **Development Corridors:** {report['section_2_spatial_structure']['summary']['development_corridors']}
- **Functional Zones:** {report['section_2_spatial_structure']['summary']['functional_zones']}

### Tier 1 Strategic Nodes (National)

| Node | Region | Type | Pop 2050 (M) | Key Functions |
|------|--------|------|--------------|---------------|
"""
        for node in report['section_2_spatial_structure']['strategic_nodes']:
            if node['tier'] == 1:
                funcs = ', '.join(node['functions'][:2])
                md_content += f"| **{node['name']}** | {node['region']} | {node['type']} | {node['population_2050']} | {funcs} |\n"
        
        md_content += """
### Development Corridors

| Corridor | Type | Route | Length (km) | Investment (SAR B) | Priority |
|----------|------|-------|-------------|-------------------|----------|
"""
        for c in report['section_2_spatial_structure']['development_corridors']:
            route = f"{c['origin']} → {c['destination']}"
            md_content += f"| {c['name'][:25]} | {c['type']} | {route[:30]} | {c['length_km']} | {c['investment_sar_b']} | {c['priority']} |\n"
        
        md_content += """
---

## Regional Objectives Summary

| Region | Strategic Role | Pop 2050 (M) | GDP % | Priority Sectors |
|--------|---------------|--------------|-------|------------------|
"""
        for region, obj in report['section_3_regional_objectives'].items():
            sectors = ', '.join(obj['priority_sectors'][:2])
            md_content += f"| {region} | {obj['strategic_role'][:25]}... | {obj['population_2050']} | {obj['gdp_share_2050']}% | {sectors} |\n"
        
        md_content += f"""
---

## Investment Priorities

### Summary
- **Total Investment:** SAR {report['section_4_investment_priorities']['summary']['total_sar_billion']} Billion
- **Priority Items:** {report['section_4_investment_priorities']['summary']['priority_count']}

### By Category
| Category | Investment (SAR B) |
|----------|-------------------|
"""
        for cat, amount in report['section_4_investment_priorities']['summary']['by_category'].items():
            md_content += f"| {cat.upper()} | {amount} |\n"
        
        md_content += """
### Top Investment Priorities

| ID | Title | Category | Cost (SAR B) | Timeline |
|----|-------|----------|--------------|----------|
"""
        for inv in report['section_4_investment_priorities']['priorities'][:8]:
            md_content += f"| {inv['id']} | {inv['title'][:35]}... | {inv['category']} | {inv['cost_sar_b']} | {inv['timeline']} |\n"
        
        md_content += """
---

## Stakeholder Engagement

### Key Messages for Public Consultation
"""
        for msg in report['section_5_stakeholder_materials']['public_consultation']['key_messages']:
            md_content += f"- {msg}\n"
        
        md_content += """
### Feedback Channels
"""
        for channel in report['section_5_stakeholder_materials']['public_consultation']['feedback_channels']:
            md_content += f"- {channel}\n"
        
        md_content += """
---

## Output Files
"""
        for f in report['appendices']['output_files']:
            md_content += f"- `{f}`\n"
        
        # Save markdown
        md_path = self.output_dir / "WS6_NSS_DRAFT_REPORT.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.success(f"Markdown report saved to {md_path}")


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

def generate_ws6_deliverables(output_dir: str = "02_analytics/ws6_outputs") -> Dict[str, Any]:
    """Generate all WS6 deliverables."""
    generator = WS6ReportGenerator(output_dir)
    return generator.generate_all_reports()


if __name__ == "__main__":
    print("=" * 60)
    print("NSS X - WS6 National Spatial Strategy Draft Generator")
    print("=" * 60)
    
    report = generate_ws6_deliverables()
    
    print("\n✅ WS6 Deliverables Generated:")
    print(f"   📄 WS6_NSS_DRAFT_REPORT.json")
    print(f"   📄 WS6_NSS_DRAFT_REPORT.md")
    print(f"   📄 strategic_nodes.csv")
    print(f"   📄 development_corridors.csv")
    print(f"   📄 functional_zones.csv")
    print(f"   📄 regional_objectives.csv")
    print(f"   📄 investment_priorities.csv")
    
    print("\n📊 NSS Structure:")
    print(f"   Strategic Nodes: {report['section_2_spatial_structure']['summary']['strategic_nodes']}")
    print(f"   Development Corridors: {report['section_2_spatial_structure']['summary']['development_corridors']}")
    print(f"   Functional Zones: {report['section_2_spatial_structure']['summary']['functional_zones']}")
    print(f"   Regional Objectives: 13")
    
    investment = report['section_4_investment_priorities']['summary']
    print(f"\n💰 Total Investment: SAR {investment['total_sar_billion']}B")
    
    print("\n✅ WS6 Complete!")
