"""
NSS X - WS3: International Benchmarking
Comprehensive international spatial strategy benchmarking module.

Deliverables:
- 3.1 International Spatial Strategy Benchmarking Report
- 3.2 Comparative Methodology Matrix
- 3.3 Country X-Fit NSS Design Principles
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
# ENUMS AND DATA CLASSES
# =============================================================================

class GovernanceModel(Enum):
    """Types of spatial planning governance models."""
    CENTRALIZED = "centralized"
    FEDERAL = "federal"
    DECENTRALIZED = "decentralized"
    HYBRID = "hybrid"
    CITY_STATE = "city_state"


class PlanningApproach(Enum):
    """Types of spatial planning approaches."""
    COMPREHENSIVE = "comprehensive"  # Full national coverage
    STRATEGIC = "strategic"  # Key corridors/zones only
    PROJECT_BASED = "project_based"  # Mega-project focused
    INCREMENTAL = "incremental"  # Gradual adaptation
    VISIONARY = "visionary"  # Long-term transformation


class ImplementationMechanism(Enum):
    """Types of implementation mechanisms."""
    REGULATORY = "regulatory"  # Laws and regulations
    FISCAL = "fiscal"  # Tax and incentives
    INVESTMENT = "investment"  # Direct state investment
    PARTNERSHIP = "partnership"  # Public-private partnerships
    MARKET = "market"  # Market-based mechanisms


@dataclass
class SpatialStrategyProfile:
    """Complete profile of a country's spatial strategy."""
    country_name: str
    strategy_name: str
    period: str
    population_millions: float
    area_km2: float
    gdp_per_capita_usd: int
    
    # Core characteristics
    governance_model: GovernanceModel
    planning_approach: PlanningApproach
    primary_mechanisms: List[ImplementationMechanism]
    
    # Context
    context: str
    key_challenges: List[str]
    strategic_objectives: List[str]
    
    # Methodology
    analytical_framework: Dict[str, str]
    scenario_approach: str
    time_horizons: List[int]
    
    # Governance
    lead_agency: str
    coordination_mechanism: str
    review_cycle_years: int
    
    # Key features
    distinctive_features: List[str]
    success_factors: List[str]
    limitations: List[str]
    
    # Outcomes
    key_achievements: List[str]
    ongoing_challenges: List[str]
    
    # Lessons for KSA
    lessons_learned: List[str]
    transferability_to_ksa: str  # high, medium, low
    specific_recommendations: List[str]


@dataclass
class MethodologyDimension:
    """A dimension for comparing methodologies."""
    dimension: str
    description: str
    ksa_relevance: str  # Why this matters for KSA


@dataclass
class CountryMethodologyScore:
    """Methodology scores for a country."""
    country: str
    scores: Dict[str, int]  # dimension -> score (1-5)
    strengths: List[str]
    weaknesses: List[str]
    best_practices: List[str]


@dataclass
class DesignPrinciple:
    """A design principle for Country X NSS."""
    id: str
    principle: str
    category: str  # governance, methodology, implementation, content
    source_countries: List[str]
    adoption_approach: str  # adopt_directly, adapt, avoid
    rationale: str
    implementation_guidance: str
    priority: str  # critical, high, medium, low


# =============================================================================
# COUNTRY CASE STUDIES
# =============================================================================

class InternationalBenchmarks:
    """
    Comprehensive international benchmarking database.
    Contains detailed case studies of 5 countries with spatial strategies.
    """
    
    def __init__(self):
        """Initialize benchmarking database."""
        self._build_country_profiles()
        logger.info("International Benchmarks initialized with 5 country profiles")
    
    def _build_country_profiles(self):
        """Build detailed profiles for benchmark countries."""
        
        self.countries: Dict[str, SpatialStrategyProfile] = {}
        
        # =====================================================================
        # UAE - UNITED ARAB EMIRATES
        # =====================================================================
        self.countries['UAE'] = SpatialStrategyProfile(
            country_name="United Arab Emirates",
            strategy_name="UAE National Spatial Framework 2071",
            period="2017-2071",
            population_millions=9.9,
            area_km2=83600,
            gdp_per_capita_usd=43103,
            
            governance_model=GovernanceModel.FEDERAL,
            planning_approach=PlanningApproach.VISIONARY,
            primary_mechanisms=[
                ImplementationMechanism.INVESTMENT,
                ImplementationMechanism.PARTNERSHIP,
                ImplementationMechanism.REGULATORY
            ],
            
            context="""UAE transformed from desert federation to global hub in 50 years.
            Federal structure with 7 emirates having significant autonomy.
            Abu Dhabi and Dubai drive 85% of GDP. Oil revenue enabled massive investment.
            Diversification into tourism, finance, logistics, and technology.""",
            
            key_challenges=[
                "Coordinating 7 emirates with different priorities",
                "Abu Dhabi-Dubai competition and duplication",
                "Water scarcity and environmental sustainability",
                "Expat-dominated population (88% non-citizens)",
                "Economic diversification from oil dependency",
                "Climate change vulnerability"
            ],
            
            strategic_objectives=[
                "Create integrated national spatial vision across emirates",
                "Develop economic corridors connecting major centers",
                "Achieve sustainable urban development",
                "Protect natural heritage and resources",
                "Build resilient infrastructure networks",
                "Enable economic diversification spatially"
            ],
            
            analytical_framework={
                "data_foundation": "Federal Geographic Information Center integrated database",
                "modeling_approach": "GIS-based scenario modeling with demographic projections",
                "sector_integration": "Cross-sectoral spatial impact assessment",
                "stakeholder_input": "Emirate-level consultations and federal coordination"
            },
            
            scenario_approach="Multiple scenarios: Business-as-usual, Accelerated Growth, Sustainable Transition",
            time_horizons=[2030, 2050, 2071],
            
            lead_agency="Ministry of Cabinet Affairs (Federal)",
            coordination_mechanism="UAE Council for Spatial Planning with emirate representatives",
            review_cycle_years=5,
            
            distinctive_features=[
                "Ultra-long 50-year vision (to UAE centenary)",
                "Federal framework respecting emirate autonomy",
                "Strong integration with Vision 2021 and Centennial 2071",
                "Emphasis on economic corridors (Abu Dhabi-Dubai-RAK)",
                "Masdar City as sustainability model",
                "Smart city integration across emirates"
            ],
            
            success_factors=[
                "Strong federal leadership and funding",
                "Clear division of federal vs emirate responsibilities",
                "Flexible framework allowing emirate innovation",
                "Integration with economic planning",
                "Advanced GIS and data infrastructure",
                "Regular progress monitoring"
            ],
            
            limitations=[
                "Inter-emirate coordination still challenging",
                "Implementation varies significantly by emirate",
                "Environmental targets often secondary to growth",
                "Limited public participation in planning",
                "Dependency on continued oil revenue for investment"
            ],
            
            key_achievements=[
                "Integrated national transport network (Etihad Rail)",
                "World-class airport and port infrastructure",
                "Dubai-Abu Dhabi economic corridor development",
                "Masdar City renewable energy showcase",
                "Tourism infrastructure diversification"
            ],
            
            ongoing_challenges=[
                "Reducing inter-emirate competition/duplication",
                "Achieving sustainability targets",
                "Managing rapid urban expansion",
                "Water security"
            ],
            
            lessons_learned=[
                "Federal-regional coordination requires dedicated mechanisms",
                "Long-term vision provides stability but needs flexibility",
                "Economic corridors can drive regional integration",
                "Mega-projects need careful spatial integration",
                "Sustainability must be embedded, not added later"
            ],
            
            transferability_to_ksa="high",
            specific_recommendations=[
                "Adopt economic corridor approach for connecting giga-projects",
                "Create dedicated coordination body for inter-regional planning",
                "Use similar tiered time horizons (2030, 2050, 2070)",
                "Learn from Masdar for NEOM sustainability integration",
                "Implement federal-style flexibility for regional authorities"
            ]
        )
        
        # =====================================================================
        # SINGAPORE
        # =====================================================================
        self.countries['Singapore'] = SpatialStrategyProfile(
            country_name="Singapore",
            strategy_name="Singapore Master Plan & Long-Term Plan",
            period="2019-2030 (Master Plan), 2050+ (Long-Term Plan)",
            population_millions=5.9,
            area_km2=733,
            gdp_per_capita_usd=65233,
            
            governance_model=GovernanceModel.CITY_STATE,
            planning_approach=PlanningApproach.COMPREHENSIVE,
            primary_mechanisms=[
                ImplementationMechanism.REGULATORY,
                ImplementationMechanism.INVESTMENT,
                ImplementationMechanism.FISCAL
            ],
            
            context="""Singapore is a city-state with extreme land scarcity (733 km²).
            Every square meter must serve multiple functions. Government owns 90% of land.
            Comprehensive planning since independence (1965) enabled transformation.
            Global financial center, port hub, and technology leader.""",
            
            key_challenges=[
                "Extreme land scarcity - no hinterland",
                "Balancing density with livability",
                "Climate change and sea level rise",
                "Aging population and workforce needs",
                "Maintaining competitiveness",
                "Housing affordability"
            ],
            
            strategic_objectives=[
                "Optimize every parcel for highest and best use",
                "Create 30-minute city with jobs near homes",
                "Achieve 80% green and blue spaces by 2030",
                "Build climate-resilient infrastructure",
                "Enable economic transformation through spatial planning",
                "Maintain housing affordability through HDB system"
            ],
            
            analytical_framework={
                "data_foundation": "Comprehensive land use database (OneMap)",
                "modeling_approach": "Detailed plot-level planning with 3D modeling",
                "sector_integration": "Mandatory cross-agency coordination for all developments",
                "stakeholder_input": "Extensive public consultation for Master Plan reviews"
            },
            
            scenario_approach="Population scenarios (6.5M-7M) driving land use allocation",
            time_horizons=[2030, 2040, 2050],
            
            lead_agency="Urban Redevelopment Authority (URA)",
            coordination_mechanism="Inter-agency planning committees chaired by URA",
            review_cycle_years=5,
            
            distinctive_features=[
                "Plot-level detailed planning for entire nation",
                "Land banking and strategic release system",
                "Integrated public housing (HDB) planning",
                "Marina Bay as urban transformation exemplar",
                "Garden City to City in Nature evolution",
                "Underground and vertical space maximization"
            ],
            
            success_factors=[
                "Government land ownership enables comprehensive planning",
                "Long-term consistency in planning approach",
                "Strong technical capacity in URA",
                "Integration of transport and land use",
                "Public trust in planning system",
                "Effective enforcement mechanisms"
            ],
            
            limitations=[
                "City-state model not directly transferable to large countries",
                "Highly centralized - limited regional variation",
                "High cost of comprehensive planning",
                "Can be inflexible to rapid changes",
                "Dependent on competent bureaucracy"
            ],
            
            key_achievements=[
                "Transformed from colonial port to global city",
                "World-class public transport (90% public transit mode share)",
                "89% home ownership through HDB",
                "Marina Bay Financial District development",
                "Changi Airport expansion and Jewel"
            ],
            
            ongoing_challenges=[
                "Climate adaptation and coastal protection",
                "Land reclamation limits",
                "Aging infrastructure renewal",
                "Maintaining green spaces with densification"
            ],
            
            lessons_learned=[
                "Comprehensive planning requires strong data foundation",
                "Land ownership/control enables long-term planning",
                "Transport and land use must be fully integrated",
                "Public housing can be planning instrument",
                "Regular review cycles maintain relevance",
                "Green infrastructure is compatible with density"
            ],
            
            transferability_to_ksa="medium",
            specific_recommendations=[
                "Adopt integrated transport-land use planning for major cities",
                "Learn from HDB model for Saudi housing programs",
                "Use similar public consultation approach for key developments",
                "Apply 3D planning concepts for dense urban areas (Riyadh, Jeddah)",
                "Adopt climate resilience integration methodology",
                "Consider Marina Bay-style transformation for Jeddah waterfront"
            ]
        )
        
        # =====================================================================
        # NETHERLANDS
        # =====================================================================
        self.countries['Netherlands'] = SpatialStrategyProfile(
            country_name="Netherlands",
            strategy_name="National Strategy on Spatial Planning and the Environment (NOVI)",
            period="2020-2050",
            population_millions=17.5,
            area_km2=41543,
            gdp_per_capita_usd=57768,
            
            governance_model=GovernanceModel.DECENTRALIZED,
            planning_approach=PlanningApproach.STRATEGIC,
            primary_mechanisms=[
                ImplementationMechanism.REGULATORY,
                ImplementationMechanism.FISCAL,
                ImplementationMechanism.PARTNERSHIP
            ],
            
            context="""Netherlands is one of world's most densely planned countries.
            26% below sea level - water management is existential. Strong tradition of
            collaborative planning (poldermodel). Decentralized with 12 provinces and
            352 municipalities. EU integration shapes many policies.""",
            
            key_challenges=[
                "Sea level rise and flood protection",
                "Housing shortage (1 million homes needed)",
                "Agricultural nitrogen emissions",
                "Energy transition from gas",
                "Infrastructure capacity constraints",
                "Balancing growth with environmental limits"
            ],
            
            strategic_objectives=[
                "Achieve climate-neutral and resilient country by 2050",
                "Build 1 million homes while protecting green space",
                "Complete energy transition (renewable by 2050)",
                "Maintain competitiveness of Randstad region",
                "Protect and enhance natural environment",
                "Ensure equitable regional development"
            ],
            
            analytical_framework={
                "data_foundation": "National geodata infrastructure (PDOK)",
                "modeling_approach": "Integrated assessment modeling (DPSIR framework)",
                "sector_integration": "Environmental integration mandatory (Strategic Environmental Assessment)",
                "stakeholder_input": "Multi-level governance with provincial and municipal input"
            },
            
            scenario_approach="Four WLO scenarios combining economic and demographic variables",
            time_horizons=[2030, 2040, 2050],
            
            lead_agency="Ministry of Interior and Kingdom Relations",
            coordination_mechanism="National Planning Conference with provinces/municipalities",
            review_cycle_years=4,
            
            distinctive_features=[
                "Water management as spatial organizing principle",
                "Compact city policy preventing sprawl",
                "Room for the River program - adaptive water management",
                "MIRT process for infrastructure investment decisions",
                "Strong environmental assessment integration",
                "Collaborative 'poldermodel' decision-making"
            ],
            
            success_factors=[
                "Long planning tradition and technical expertise",
                "Strong data and modeling infrastructure",
                "Effective multi-level governance",
                "Mandatory environmental assessment",
                "Public trust in planning institutions",
                "EU framework providing policy coherence"
            ],
            
            limitations=[
                "Complex multi-level governance can slow decisions",
                "Consensus-seeking takes time",
                "Local autonomy can conflict with national priorities",
                "Resource-intensive planning process",
                "Implementation gaps between policy and practice"
            ],
            
            key_achievements=[
                "Delta Works - world-class flood protection",
                "Compact city policy limited sprawl",
                "Room for the River - innovative climate adaptation",
                "High-speed rail integration (HSL Zuid)",
                "Renewable energy growth (offshore wind)"
            ],
            
            ongoing_challenges=[
                "Accelerating housing construction",
                "Nitrogen emissions reduction in agriculture",
                "Energy transition speed",
                "Climate adaptation investment needs"
            ],
            
            lessons_learned=[
                "Environmental sustainability must be core organizing principle",
                "Multi-level governance requires clear frameworks",
                "Scenario planning helps manage uncertainty",
                "Infrastructure investment decisions need systematic process",
                "Adaptive management better than rigid plans for climate",
                "Stakeholder engagement builds implementation support"
            ],
            
            transferability_to_ksa="medium",
            specific_recommendations=[
                "Adopt water security as organizing principle (like Dutch water management)",
                "Learn from Room for the River for adaptive infrastructure",
                "Apply MIRT-style systematic infrastructure investment appraisal",
                "Use Strategic Environmental Assessment for major projects",
                "Consider Dutch scenario methodology for uncertainty management",
                "Implement compact city policies for major urban areas"
            ]
        )
        
        # =====================================================================
        # SOUTH KOREA
        # =====================================================================
        self.countries['South Korea'] = SpatialStrategyProfile(
            country_name="South Korea",
            strategy_name="Fifth Comprehensive National Territorial Plan (CNTP)",
            period="2020-2040",
            population_millions=51.8,
            area_km2=100210,
            gdp_per_capita_usd=34998,
            
            governance_model=GovernanceModel.CENTRALIZED,
            planning_approach=PlanningApproach.COMPREHENSIVE,
            primary_mechanisms=[
                ImplementationMechanism.INVESTMENT,
                ImplementationMechanism.REGULATORY,
                ImplementationMechanism.FISCAL
            ],
            
            context="""South Korea transformed from war-devastated nation to advanced economy
            in 60 years. Strong centralized planning tradition. Seoul metropolitan area
            dominates (50% of population). Comprehensive national plans since 1972.
            Aging population and declining birth rate major concerns.""",
            
            key_challenges=[
                "Seoul metropolitan area over-concentration",
                "Declining population and aging society",
                "Regional economic disparities",
                "North Korea reunification uncertainty",
                "Climate change adaptation",
                "Industrial restructuring"
            ],
            
            strategic_objectives=[
                "Achieve balanced national development",
                "Adapt to population decline and aging",
                "Strengthen regional competitiveness",
                "Build sustainable and safe territory",
                "Prepare for Korean peninsula integration",
                "Develop smart and innovative spaces"
            ],
            
            analytical_framework={
                "data_foundation": "National Spatial Data Infrastructure (NSDI)",
                "modeling_approach": "Regional econometric modeling with spatial allocation",
                "sector_integration": "Cross-ministerial coordination through MOLIT",
                "stakeholder_input": "Regional development plans feed into national plan"
            },
            
            scenario_approach="Population-driven scenarios with regional allocation models",
            time_horizons=[2030, 2040],
            
            lead_agency="Ministry of Land, Infrastructure and Transport (MOLIT)",
            coordination_mechanism="Presidential Committee on Balanced National Development",
            review_cycle_years=5,
            
            distinctive_features=[
                "New administrative capital (Sejong City)",
                "Innovation cities program dispersing government functions",
                "Special economic zones for regional development",
                "Korean New Deal (green + digital transformation)",
                "Preparation for potential reunification",
                "Smart city national pilot program"
            ],
            
            success_factors=[
                "Strong central planning capacity",
                "Integration of economic and spatial planning",
                "Major public investment in regional infrastructure",
                "Dedicated regional development programs",
                "Technical excellence in planning agencies",
                "Political commitment to balanced development"
            ],
            
            limitations=[
                "Seoul dominance persists despite policies",
                "Top-down approach limits local innovation",
                "Frequent policy changes with governments",
                "Implementation gaps in smaller regions",
                "Environmental concerns sometimes secondary"
            ],
            
            key_achievements=[
                "Sejong City development as new administrative capital",
                "KTX high-speed rail network connecting nation",
                "Innovation cities redistributing government functions",
                "Industrial restructuring (shipbuilding to semiconductors)",
                "World-class digital infrastructure"
            ],
            
            ongoing_challenges=[
                "Reducing Seoul concentration",
                "Managing population decline",
                "Regional economic diversification",
                "Climate adaptation"
            ],
            
            lessons_learned=[
                "Balanced development requires sustained investment",
                "Administrative capital relocation can work but takes decades",
                "High-speed rail is powerful spatial integration tool",
                "Innovation clusters need critical mass to succeed",
                "Population decline requires fundamental planning rethink",
                "Technology (smart cities) can enhance planning effectiveness"
            ],
            
            transferability_to_ksa="high",
            specific_recommendations=[
                "Learn from Sejong City for NEOM and new city development",
                "Adopt innovation cities model for distributing government functions",
                "Use KTX model for national rail network (Land Bridge)",
                "Apply Korean New Deal approach for green+digital transformation",
                "Consider special economic zones for regional development",
                "Adopt Korean smart city standards and pilots"
            ]
        )
        
        # =====================================================================
        # MALAYSIA
        # =====================================================================
        self.countries['Malaysia'] = SpatialStrategyProfile(
            country_name="Malaysia",
            strategy_name="National Physical Plan 3 (NPP3)",
            period="2015-2040",
            population_millions=32.7,
            area_km2=330803,
            gdp_per_capita_usd=12364,
            
            governance_model=GovernanceModel.FEDERAL,
            planning_approach=PlanningApproach.STRATEGIC,
            primary_mechanisms=[
                ImplementationMechanism.REGULATORY,
                ImplementationMechanism.INVESTMENT,
                ImplementationMechanism.PARTNERSHIP
            ],
            
            context="""Malaysia is a federal state with 13 states and 3 federal territories.
            Peninsular Malaysia and East Malaysia (Borneo) have distinct characteristics.
            Multi-ethnic society with Bumiputera affirmative action. Middle-income economy
            seeking high-income status. Strong planning tradition since 1980s.""",
            
            key_challenges=[
                "Regional disparities (Peninsular vs East Malaysia)",
                "Urban-rural development gaps",
                "Environmental degradation (deforestation, pollution)",
                "Federal-state planning coordination",
                "Middle-income trap",
                "Climate change vulnerability"
            ],
            
            strategic_objectives=[
                "Achieve high-income nation status by 2030",
                "Ensure sustainable and resilient development",
                "Reduce regional development disparities",
                "Protect natural heritage and biodiversity",
                "Strengthen urban systems and hierarchies",
                "Enhance rural development and connectivity"
            ],
            
            analytical_framework={
                "data_foundation": "MyGeoportal national spatial data infrastructure",
                "modeling_approach": "Hierarchical planning with state structure plans",
                "sector_integration": "Economic Planning Unit coordination",
                "stakeholder_input": "State and local authority consultation process"
            },
            
            scenario_approach="High/Medium/Low growth scenarios based on economic projections",
            time_horizons=[2025, 2030, 2040],
            
            lead_agency="Federal Town and Country Planning Department (PLANMalaysia)",
            coordination_mechanism="National Physical Planning Council",
            review_cycle_years=5,
            
            distinctive_features=[
                "Federal-state planning hierarchy",
                "Development corridor approach (Northern, Eastern, Sabah, Sarawak)",
                "Forest City and major projects in Iskandar Malaysia",
                "Strict environmental areas (Central Forest Spine)",
                "Rural transformation programs",
                "Islamic finance center development"
            ],
            
            success_factors=[
                "Clear planning hierarchy (National > State > Local)",
                "Integration with 5-year Malaysia Plans",
                "Strong technical capacity in PLANMalaysia",
                "Development corridor approach for regional targeting",
                "Environmental protection integrated",
                "Regular review and update cycles"
            ],
            
            limitations=[
                "Federal-state coordination challenges",
                "Implementation varies by state capacity",
                "Environmental enforcement gaps",
                "East Malaysia development lag persists",
                "Private sector mega-projects sometimes conflict with plans"
            ],
            
            key_achievements=[
                "Iskandar Malaysia development zone success",
                "Central Forest Spine protection",
                "Kuala Lumpur transformation and connectivity",
                "East Coast Rail Link (ECRL) development",
                "Rural infrastructure improvement"
            ],
            
            ongoing_challenges=[
                "Reducing Peninsular-East Malaysia gap",
                "Environmental protection vs development",
                "Urban sprawl management",
                "Climate adaptation"
            ],
            
            lessons_learned=[
                "Development corridors can target regional investment",
                "Federal-state coordination needs clear mechanisms",
                "Planning hierarchy must be enforced",
                "Environmental protection needs strong legislation",
                "Mega-projects require careful spatial integration",
                "Rural development needs dedicated programs"
            ],
            
            transferability_to_ksa="high",
            specific_recommendations=[
                "Adopt development corridor model for KSA regions",
                "Use similar planning hierarchy (National > Regional > Local)",
                "Learn from Iskandar Malaysia for special zone development",
                "Apply Central Forest Spine approach for environmental protection",
                "Integrate 5-year plan approach with spatial planning",
                "Consider Malaysia's rural transformation program design"
            ]
        )
    
    def get_country(self, country_code: str) -> Optional[SpatialStrategyProfile]:
        """Get country profile by code."""
        return self.countries.get(country_code)
    
    def get_all_countries(self) -> Dict[str, SpatialStrategyProfile]:
        """Get all country profiles."""
        return self.countries
    
    def get_countries_by_governance(self, model: GovernanceModel) -> List[SpatialStrategyProfile]:
        """Get countries by governance model."""
        return [c for c in self.countries.values() if c.governance_model == model]
    
    def get_high_transferability_countries(self) -> List[SpatialStrategyProfile]:
        """Get countries with high transferability to KSA."""
        return [c for c in self.countries.values() if c.transferability_to_ksa == "high"]


# =============================================================================
# METHODOLOGY COMPARISON MATRIX
# =============================================================================

class MethodologyMatrix:
    """
    Comparative methodology matrix across benchmark countries.
    """
    
    def __init__(self, benchmarks: InternationalBenchmarks):
        """Initialize with benchmark data."""
        self.benchmarks = benchmarks
        self._build_dimensions()
        self._score_countries()
        logger.info("Methodology Matrix initialized")
    
    def _build_dimensions(self):
        """Define comparison dimensions."""
        
        self.dimensions: List[MethodologyDimension] = [
            MethodologyDimension(
                dimension="Data Infrastructure",
                description="Quality and comprehensiveness of spatial data systems",
                ksa_relevance="KSA needs strong GIS foundation for spatial decisions"
            ),
            MethodologyDimension(
                dimension="Scenario Planning",
                description="Use of multiple scenarios for uncertainty management",
                ksa_relevance="Vision 2030 requires scenario-based stress testing"
            ),
            MethodologyDimension(
                dimension="Stakeholder Engagement",
                description="Breadth and depth of consultation processes",
                ksa_relevance="Building support for spatial transformations"
            ),
            MethodologyDimension(
                dimension="Environmental Integration",
                description="Integration of environmental assessment in planning",
                ksa_relevance="Water security and climate adaptation are critical"
            ),
            MethodologyDimension(
                dimension="Implementation Mechanisms",
                description="Tools for translating plans into action",
                ksa_relevance="Historical implementation gaps need addressing"
            ),
            MethodologyDimension(
                dimension="Monitoring & Evaluation",
                description="Systems for tracking progress and adaptation",
                ksa_relevance="Vision 2030 requires robust performance tracking"
            ),
            MethodologyDimension(
                dimension="Regional Coordination",
                description="Mechanisms for coordinating across regions",
                ksa_relevance="13 regions need coherent spatial coordination"
            ),
            MethodologyDimension(
                dimension="Economic Integration",
                description="Integration of economic and spatial planning",
                ksa_relevance="Diversification requires spatial expression"
            ),
            MethodologyDimension(
                dimension="Long-term Vision",
                description="Quality of long-term strategic thinking",
                ksa_relevance="NSS needs 2030-2070 horizon"
            ),
            MethodologyDimension(
                dimension="Adaptability",
                description="Flexibility to respond to changing conditions",
                ksa_relevance="Rapid transformation requires adaptive planning"
            )
        ]
    
    def _score_countries(self):
        """Score each country on methodology dimensions."""
        
        self.scores: Dict[str, CountryMethodologyScore] = {}
        
        # UAE Scores
        self.scores['UAE'] = CountryMethodologyScore(
            country="UAE",
            scores={
                "Data Infrastructure": 4,
                "Scenario Planning": 4,
                "Stakeholder Engagement": 3,
                "Environmental Integration": 3,
                "Implementation Mechanisms": 5,
                "Monitoring & Evaluation": 4,
                "Regional Coordination": 3,
                "Economic Integration": 5,
                "Long-term Vision": 5,
                "Adaptability": 4
            },
            strengths=[
                "Strong long-term visioning (2071 horizon)",
                "Excellent implementation through sovereign wealth",
                "Tight economic-spatial integration"
            ],
            weaknesses=[
                "Inter-emirate coordination challenges",
                "Limited public engagement",
                "Environmental targets secondary"
            ],
            best_practices=[
                "Economic corridor development approach",
                "Integration with national vision",
                "Flexible federal framework"
            ]
        )
        
        # Singapore Scores
        self.scores['Singapore'] = CountryMethodologyScore(
            country="Singapore",
            scores={
                "Data Infrastructure": 5,
                "Scenario Planning": 4,
                "Stakeholder Engagement": 4,
                "Environmental Integration": 4,
                "Implementation Mechanisms": 5,
                "Monitoring & Evaluation": 5,
                "Regional Coordination": 5,  # N/A but effectively perfect for city-state
                "Economic Integration": 5,
                "Long-term Vision": 5,
                "Adaptability": 4
            },
            strengths=[
                "World-class data and modeling",
                "Comprehensive implementation",
                "Excellent monitoring systems"
            ],
            weaknesses=[
                "City-state model limits transferability",
                "Highly centralized approach",
                "Resource-intensive planning"
            ],
            best_practices=[
                "Integrated transport-land use planning",
                "Plot-level planning precision",
                "Regular plan review cycles"
            ]
        )
        
        # Netherlands Scores
        self.scores['Netherlands'] = CountryMethodologyScore(
            country="Netherlands",
            scores={
                "Data Infrastructure": 5,
                "Scenario Planning": 5,
                "Stakeholder Engagement": 5,
                "Environmental Integration": 5,
                "Implementation Mechanisms": 4,
                "Monitoring & Evaluation": 4,
                "Regional Coordination": 4,
                "Economic Integration": 4,
                "Long-term Vision": 4,
                "Adaptability": 5
            },
            strengths=[
                "Excellent environmental integration",
                "Strong scenario methodology",
                "Highly adaptive planning"
            ],
            weaknesses=[
                "Complex multi-level governance",
                "Slow consensus processes",
                "Implementation gaps"
            ],
            best_practices=[
                "Strategic Environmental Assessment",
                "Room for the River adaptive approach",
                "MIRT infrastructure appraisal"
            ]
        )
        
        # South Korea Scores
        self.scores['South Korea'] = CountryMethodologyScore(
            country="South Korea",
            scores={
                "Data Infrastructure": 5,
                "Scenario Planning": 4,
                "Stakeholder Engagement": 3,
                "Environmental Integration": 3,
                "Implementation Mechanisms": 5,
                "Monitoring & Evaluation": 4,
                "Regional Coordination": 4,
                "Economic Integration": 5,
                "Long-term Vision": 4,
                "Adaptability": 3
            },
            strengths=[
                "Powerful implementation capacity",
                "Tight economic integration",
                "Technical planning excellence"
            ],
            weaknesses=[
                "Limited public engagement",
                "Environmental concerns secondary",
                "Policy instability with governments"
            ],
            best_practices=[
                "Innovation cities program",
                "Administrative capital relocation",
                "High-speed rail spatial integration"
            ]
        )
        
        # Malaysia Scores
        self.scores['Malaysia'] = CountryMethodologyScore(
            country="Malaysia",
            scores={
                "Data Infrastructure": 4,
                "Scenario Planning": 3,
                "Stakeholder Engagement": 3,
                "Environmental Integration": 4,
                "Implementation Mechanisms": 3,
                "Monitoring & Evaluation": 3,
                "Regional Coordination": 4,
                "Economic Integration": 4,
                "Long-term Vision": 4,
                "Adaptability": 3
            },
            strengths=[
                "Clear planning hierarchy",
                "Development corridor approach",
                "Environmental protection integration"
            ],
            weaknesses=[
                "Federal-state coordination gaps",
                "Implementation varies by state",
                "Enforcement challenges"
            ],
            best_practices=[
                "Development corridor model",
                "Planning hierarchy structure",
                "Central Forest Spine protection"
            ]
        )
    
    def get_dimension_comparison(self, dimension: str) -> pd.DataFrame:
        """Get scores for a specific dimension across all countries."""
        data = []
        for country, score in self.scores.items():
            data.append({
                'Country': country,
                'Score': score.scores.get(dimension, 0)
            })
        return pd.DataFrame(data).sort_values('Score', ascending=False)
    
    def get_full_matrix(self) -> pd.DataFrame:
        """Get full comparison matrix."""
        data = []
        for country, score in self.scores.items():
            row = {'Country': country}
            row.update(score.scores)
            row['Average'] = np.mean(list(score.scores.values()))
            data.append(row)
        
        df = pd.DataFrame(data)
        return df.sort_values('Average', ascending=False)
    
    def get_best_practices_by_dimension(self) -> Dict[str, List[Tuple[str, str]]]:
        """Get best practices organized by dimension."""
        result = {}
        for dim in self.dimensions:
            dimension = dim.dimension
            # Get top scorers for this dimension
            comparison = self.get_dimension_comparison(dimension)
            top_countries = comparison[comparison['Score'] >= 4]['Country'].tolist()
            
            practices = []
            for country in top_countries:
                score = self.scores[country]
                for practice in score.best_practices:
                    practices.append((country, practice))
            
            result[dimension] = practices
        
        return result


# =============================================================================
# COUNTRY X-FIT DESIGN PRINCIPLES
# =============================================================================

class CountryXFitDesignPrinciples:
    """
    Generates design principles tailored for Country X (Saudi Arabia)
    based on international benchmarking analysis.
    """
    
    def __init__(self, benchmarks: InternationalBenchmarks, matrix: MethodologyMatrix):
        """Initialize with benchmark analysis."""
        self.benchmarks = benchmarks
        self.matrix = matrix
        self._generate_principles()
        logger.info("Country X-Fit Design Principles generated")
    
    def _generate_principles(self):
        """Generate tailored design principles for KSA."""
        
        self.principles: List[DesignPrinciple] = [
            # GOVERNANCE PRINCIPLES
            DesignPrinciple(
                id="GOV-01",
                principle="Establish dedicated NSS Implementation Authority with cross-ministerial coordination power",
                category="governance",
                source_countries=["UAE", "South Korea"],
                adoption_approach="adopt_directly",
                rationale="Both UAE and Korea succeeded through strong central coordination. KSA's Vision 2030 governance provides foundation.",
                implementation_guidance="Create body under Royal Court or Council of Ministers with authority over spatial decisions across ministries",
                priority="critical"
            ),
            DesignPrinciple(
                id="GOV-02",
                principle="Implement tiered planning hierarchy: National > Regional > Municipal",
                category="governance",
                source_countries=["Malaysia", "Netherlands"],
                adoption_approach="adopt_directly",
                rationale="Clear hierarchy prevents conflicts and ensures alignment. Malaysia's NPP model is directly applicable.",
                implementation_guidance="National framework sets principles; Regional plans translate to context; Municipal plans implement",
                priority="critical"
            ),
            DesignPrinciple(
                id="GOV-03",
                principle="Establish 5-year formal review cycles with public reporting",
                category="governance",
                source_countries=["Singapore", "Netherlands", "Malaysia"],
                adoption_approach="adopt_directly",
                rationale="All successful countries have regular reviews. NSS 2001 failed partly due to lack of reviews.",
                implementation_guidance="Mandatory comprehensive review every 5 years; annual progress reports; mid-term adjustments allowed",
                priority="high"
            ),
            DesignPrinciple(
                id="GOV-04",
                principle="Strengthen regional authority capacity while maintaining strategic alignment",
                category="governance",
                source_countries=["UAE", "Malaysia"],
                adoption_approach="adapt",
                rationale="UAE's emirate flexibility and Malaysia's state role show benefits. KSA regions need more capacity.",
                implementation_guidance="Increase regional planning staff; delegate operational decisions; maintain strategic oversight centrally",
                priority="high"
            ),
            
            # METHODOLOGY PRINCIPLES
            DesignPrinciple(
                id="MTH-01",
                principle="Develop comprehensive national spatial data infrastructure",
                category="methodology",
                source_countries=["Singapore", "Netherlands", "South Korea"],
                adoption_approach="adopt_directly",
                rationale="All top performers have excellent data foundations. KSA has made progress but needs consolidation.",
                implementation_guidance="Integrate all government spatial data; implement standards; ensure real-time updates; enable public access",
                priority="critical"
            ),
            DesignPrinciple(
                id="MTH-02",
                principle="Implement robust scenario planning with stress testing",
                category="methodology",
                source_countries=["Netherlands", "UAE", "Singapore"],
                adoption_approach="adopt_directly",
                rationale="Uncertainty management essential given KSA's transformation ambition. Dutch methodology is most advanced.",
                implementation_guidance="Develop 3-4 scenarios (baseline, accelerated, sustainable, stress); test all major decisions against scenarios",
                priority="critical"
            ),
            DesignPrinciple(
                id="MTH-03",
                principle="Integrate environmental sustainability as core organizing principle",
                category="methodology",
                source_countries=["Netherlands", "Singapore"],
                adoption_approach="adopt_directly",
                rationale="Water security and climate adaptation are existential for KSA. Netherlands' water management model relevant.",
                implementation_guidance="Water security to drive spatial allocation; mandatory SEA for all major projects; climate adaptation integrated",
                priority="critical"
            ),
            DesignPrinciple(
                id="MTH-04",
                principle="Adopt economic corridor development approach",
                category="methodology",
                source_countries=["UAE", "Malaysia"],
                adoption_approach="adapt",
                rationale="Corridors can connect giga-projects and distribute development. UAE and Malaysia show effectiveness.",
                implementation_guidance="Define 3-4 national corridors (e.g., Red Sea-Gulf, Riyadh-Qassim, NEOM-Tabuk); prioritize infrastructure",
                priority="high"
            ),
            
            # IMPLEMENTATION PRINCIPLES
            DesignPrinciple(
                id="IMP-01",
                principle="Link spatial plan approval to budget allocation",
                category="implementation",
                source_countries=["South Korea", "UAE"],
                adoption_approach="adapt",
                rationale="Implementation requires financial backing. Korea's CNTP-budget link is effective.",
                implementation_guidance="Major infrastructure investments require spatial plan alignment; create spatial investment review process",
                priority="critical"
            ),
            DesignPrinciple(
                id="IMP-02",
                principle="Develop systematic infrastructure investment appraisal (MIRT-style)",
                category="implementation",
                source_countries=["Netherlands"],
                adoption_approach="adopt_directly",
                rationale="Avoid ad-hoc mega-project decisions. Dutch MIRT provides systematic framework.",
                implementation_guidance="Create multi-criteria appraisal process for all major infrastructure; spatial impact mandatory criterion",
                priority="high"
            ),
            DesignPrinciple(
                id="IMP-03",
                principle="Create special economic zones for regional development targeting",
                category="implementation",
                source_countries=["South Korea", "UAE", "Malaysia"],
                adoption_approach="adopt_directly",
                rationale="All benchmark countries use SEZs effectively. KSA has foundation but needs expansion.",
                implementation_guidance="Designate zones in underserved regions; differentiated incentive packages; infrastructure priority",
                priority="high"
            ),
            DesignPrinciple(
                id="IMP-04",
                principle="Ensure mega-projects have explicit regional spillover requirements",
                category="implementation",
                source_countries=["Malaysia", "UAE"],
                adoption_approach="adapt",
                rationale="Giga-projects risk being enclaves. Malaysia's Iskandar integration provides model.",
                implementation_guidance="Require regional benefit plans for all giga-projects; local employment targets; supplier development",
                priority="high"
            ),
            
            # CONTENT PRINCIPLES
            DesignPrinciple(
                id="CNT-01",
                principle="Water security as primary spatial organizing principle",
                category="content",
                source_countries=["Netherlands"],
                adoption_approach="adapt",
                rationale="Netherlands organizes around water management. KSA must organize around water scarcity.",
                implementation_guidance="Spatial allocation to consider water supply; water-intensive uses in coastal/desal areas; efficiency targets",
                priority="critical"
            ),
            DesignPrinciple(
                id="CNT-02",
                principle="Define functional urban hierarchy with specialized roles",
                category="content",
                source_countries=["South Korea", "Singapore"],
                adoption_approach="adopt_directly",
                rationale="Clear city functions prevent duplication. Korea's tier system and innovation cities model relevant.",
                implementation_guidance="Riyadh=National Capital; Jeddah/Dammam=Regional Gateways; 4-5 specialized regional centers",
                priority="high"
            ),
            DesignPrinciple(
                id="CNT-03",
                principle="Integrate transport and land use planning at all scales",
                category="content",
                source_countries=["Singapore", "South Korea"],
                adoption_approach="adopt_directly",
                rationale="Singapore and Korea show transport-led development success. Critical for KSA's rail expansion.",
                implementation_guidance="TOD principles for all rail stations; Land Bridge to drive corridor development; airport economic zones",
                priority="high"
            ),
            DesignPrinciple(
                id="CNT-04",
                principle="Establish quantitative protected area targets with enforcement",
                category="content",
                source_countries=["Netherlands", "Malaysia"],
                adoption_approach="adopt_directly",
                rationale="KSA's 4.3% protection far below 30x30 commitment. Malaysia's Central Forest Spine shows effectiveness.",
                implementation_guidance="Target 30% by 2030; designate new protected areas; enforcement mechanisms; no-go zones for development",
                priority="high"
            ),
            
            # AVOID PRINCIPLES
            DesignPrinciple(
                id="AVD-01",
                principle="Avoid over-reliance on mega-projects without distributed development",
                category="implementation",
                source_countries=["UAE", "Malaysia"],
                adoption_approach="avoid",
                rationale="UAE's inter-emirate competition and Malaysia's Forest City struggles show risks of mega-project-only approach.",
                implementation_guidance="Balance giga-projects with regional development programs; ensure projects connect to surrounding areas",
                priority="high"
            ),
            DesignPrinciple(
                id="AVD-02",
                principle="Avoid top-down planning without local engagement",
                category="governance",
                source_countries=["South Korea"],
                adoption_approach="avoid",
                rationale="Korea's limited engagement contributed to Seoul concentration persistence. Local buy-in needed.",
                implementation_guidance="Meaningful consultation in regional planning; local implementation partners; feedback mechanisms",
                priority="medium"
            ),
            DesignPrinciple(
                id="AVD-03",
                principle="Avoid environmental targets without enforcement mechanisms",
                category="content",
                source_countries=["Malaysia"],
                adoption_approach="avoid",
                rationale="Malaysia's enforcement gaps limited environmental protection effectiveness. NSS 2001 had same issue.",
                implementation_guidance="Targets must have enforcement powers; violations have consequences; monitoring mandatory",
                priority="high"
            )
        ]
    
    def get_all_principles(self) -> List[DesignPrinciple]:
        """Get all design principles."""
        return self.principles
    
    def get_by_category(self, category: str) -> List[DesignPrinciple]:
        """Get principles by category."""
        return [p for p in self.principles if p.category == category]
    
    def get_by_adoption_approach(self, approach: str) -> List[DesignPrinciple]:
        """Get principles by adoption approach."""
        return [p for p in self.principles if p.adoption_approach == approach]
    
    def get_critical_principles(self) -> List[DesignPrinciple]:
        """Get critical priority principles."""
        return [p for p in self.principles if p.priority == "critical"]
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert principles to DataFrame."""
        return pd.DataFrame([
            {
                'ID': p.id,
                'Principle': p.principle,
                'Category': p.category.upper(),
                'Source Countries': ', '.join(p.source_countries),
                'Approach': p.adoption_approach.upper(),
                'Priority': p.priority.upper(),
                'Rationale': p.rationale
            }
            for p in self.principles
        ])


# =============================================================================
# WS3 REPORT GENERATOR
# =============================================================================

class WS3ReportGenerator:
    """
    Generates all WS3 deliverables.
    """
    
    def __init__(self, output_dir: str = "02_analytics/ws3_outputs"):
        """Initialize report generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.benchmarks = InternationalBenchmarks()
        self.methodology_matrix = MethodologyMatrix(self.benchmarks)
        self.design_principles = CountryXFitDesignPrinciples(self.benchmarks, self.methodology_matrix)
        
        logger.info(f"WS3 Report Generator initialized. Output: {self.output_dir}")
    
    def generate_all_reports(self) -> Dict[str, Any]:
        """Generate all WS3 deliverables."""
        
        logger.info("Generating WS3 deliverables...")
        
        # Get all data
        countries = self.benchmarks.get_all_countries()
        matrix = self.methodology_matrix.get_full_matrix()
        principles = self.design_principles.get_all_principles()
        
        # Save methodology matrix
        matrix.to_csv(self.output_dir / "methodology_comparison_matrix.csv", index=False)
        
        # Save design principles
        self.design_principles.to_dataframe().to_csv(
            self.output_dir / "country_x_fit_design_principles.csv", index=False
        )
        
        # Compile comprehensive report
        report = {
            "metadata": {
                "report_title": "WS3 - International Spatial Strategy Benchmarking",
                "generated_date": datetime.now().isoformat(),
                "version": "1.0",
                "author": "NSS X System"
            },
            "executive_summary": self._generate_executive_summary(countries, matrix, principles),
            "section_1_benchmarking_framework": self._generate_framework_section(),
            "section_2_country_case_studies": {
                country: self._country_to_dict(profile)
                for country, profile in countries.items()
            },
            "section_3_methodology_matrix": {
                "dimensions": [
                    {"dimension": d.dimension, "description": d.description, "ksa_relevance": d.ksa_relevance}
                    for d in self.methodology_matrix.dimensions
                ],
                "scores": {
                    country: {
                        "scores": score.scores,
                        "average": np.mean(list(score.scores.values())),
                        "strengths": score.strengths,
                        "weaknesses": score.weaknesses,
                        "best_practices": score.best_practices
                    }
                    for country, score in self.methodology_matrix.scores.items()
                },
                "rankings": matrix.to_dict('records'),
                "best_practices_by_dimension": self.methodology_matrix.get_best_practices_by_dimension()
            },
            "section_4_design_principles": {
                "summary": {
                    "total_principles": len(principles),
                    "by_category": pd.DataFrame([
                        {"principle": p.principle, "category": p.category}
                        for p in principles
                    ])['category'].value_counts().to_dict(),
                    "by_approach": pd.DataFrame([
                        {"principle": p.principle, "approach": p.adoption_approach}
                        for p in principles
                    ])['approach'].value_counts().to_dict(),
                    "by_priority": pd.DataFrame([
                        {"principle": p.principle, "priority": p.priority}
                        for p in principles
                    ])['priority'].value_counts().to_dict()
                },
                "critical_principles": [
                    self._principle_to_dict(p) for p in self.design_principles.get_critical_principles()
                ],
                "all_principles": [self._principle_to_dict(p) for p in principles],
                "governance_principles": [
                    self._principle_to_dict(p) for p in self.design_principles.get_by_category("governance")
                ],
                "methodology_principles": [
                    self._principle_to_dict(p) for p in self.design_principles.get_by_category("methodology")
                ],
                "implementation_principles": [
                    self._principle_to_dict(p) for p in self.design_principles.get_by_category("implementation")
                ],
                "content_principles": [
                    self._principle_to_dict(p) for p in self.design_principles.get_by_category("content")
                ]
            },
            "section_5_recommendations": self._generate_recommendations(countries, principles),
            "appendices": {
                "data_sources": [
                    "UN-Habitat Global State of National Urban Policy",
                    "OECD Regional Outlook",
                    "World Bank Urbanization Reviews",
                    "National Planning Documents (UAE, Singapore, Netherlands, Korea, Malaysia)",
                    "Academic literature on comparative spatial planning"
                ],
                "output_files": [
                    "methodology_comparison_matrix.csv",
                    "country_x_fit_design_principles.csv",
                    "WS3_BENCHMARKING_REPORT.json",
                    "WS3_BENCHMARKING_REPORT.md"
                ]
            }
        }
        
        # Save JSON report
        report_path = self.output_dir / "WS3_BENCHMARKING_REPORT.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        logger.success(f"WS3 Report saved to {report_path}")
        
        # Generate markdown report
        self._generate_markdown_report(report)
        
        return report
    
    def _generate_executive_summary(
        self, 
        countries: Dict[str, SpatialStrategyProfile],
        matrix: pd.DataFrame,
        principles: List[DesignPrinciple]
    ) -> Dict[str, Any]:
        """Generate executive summary."""
        
        high_transfer = [c.country_name for c in countries.values() if c.transferability_to_ksa == "high"]
        critical = [p.principle for p in principles if p.priority == "critical"]
        
        return {
            "overview": """This international benchmarking study analyzes spatial strategies 
            from 5 countries (UAE, Singapore, Netherlands, South Korea, Malaysia) to identify 
            best practices applicable to Saudi Arabia's National Spatial Strategy. The analysis 
            covers governance models, methodological approaches, implementation mechanisms, 
            and lessons learned.""",
            
            "key_findings": [
                f"5 countries analyzed across 10 methodology dimensions",
                f"Singapore and Netherlands score highest on methodology (avg 4.6/5.0)",
                f"UAE and South Korea have highest transferability to KSA context",
                f"{len(critical)} critical design principles identified for KSA",
                "Water security and economic corridor development are top priorities",
                "All successful countries have strong data infrastructure and regular review cycles",
                "Implementation mechanisms are the main differentiator between success and failure"
            ],
            
            "countries_analyzed": {
                "high_transferability": high_transfer,
                "methodology_leaders": matrix.head(2)['Country'].tolist(),
                "governance_models": {
                    c.governance_model.value: c.country_name 
                    for c in countries.values()
                }
            },
            
            "top_recommendations": [
                "Adopt UAE/Korea model: dedicated implementation authority with cross-ministerial power",
                "Implement Dutch-style scenario planning and environmental integration",
                "Use Singapore's integrated transport-land use approach for major cities",
                "Apply Malaysia's development corridor model for regional distribution",
                "Establish Korea-style innovation cities for government function distribution",
                "Water security must be the primary organizing principle (Dutch model adapted)"
            ],
            
            "critical_principles": critical[:5]
        }
    
    def _generate_framework_section(self) -> Dict[str, Any]:
        """Generate benchmarking framework section."""
        return {
            "purpose": "Identify international best practices applicable to Saudi Arabia's NSS",
            "selection_criteria": [
                "Rapid economic transformation trajectory",
                "Similar governance challenges (federal/regional coordination)",
                "Comparable development ambitions",
                "Documented spatial strategy with accessible information",
                "Mix of governance models and approaches"
            ],
            "countries_selected": {
                "UAE": "Regional peer with similar transformation ambition",
                "Singapore": "Gold standard for comprehensive planning",
                "Netherlands": "Leader in environmental integration and adaptation",
                "South Korea": "Successful balanced development and tech integration",
                "Malaysia": "Federal model with development corridor approach"
            },
            "analytical_dimensions": [
                "Governance model and institutional arrangements",
                "Methodological approach and analytical tools",
                "Implementation mechanisms and instruments",
                "Monitoring and evaluation systems",
                "Key success factors and limitations"
            ],
            "transferability_assessment": {
                "high": "Directly applicable with minor adaptation",
                "medium": "Applicable with significant adaptation to KSA context",
                "low": "Limited applicability due to fundamental context differences"
            }
        }
    
    def _country_to_dict(self, country: SpatialStrategyProfile) -> Dict:
        """Convert country profile to dictionary."""
        return {
            "basic_info": {
                "country_name": country.country_name,
                "strategy_name": country.strategy_name,
                "period": country.period,
                "population_millions": country.population_millions,
                "area_km2": country.area_km2,
                "gdp_per_capita_usd": country.gdp_per_capita_usd
            },
            "characteristics": {
                "governance_model": country.governance_model.value,
                "planning_approach": country.planning_approach.value,
                "primary_mechanisms": [m.value for m in country.primary_mechanisms]
            },
            "context": country.context,
            "key_challenges": country.key_challenges,
            "strategic_objectives": country.strategic_objectives,
            "methodology": {
                "analytical_framework": country.analytical_framework,
                "scenario_approach": country.scenario_approach,
                "time_horizons": country.time_horizons
            },
            "governance": {
                "lead_agency": country.lead_agency,
                "coordination_mechanism": country.coordination_mechanism,
                "review_cycle_years": country.review_cycle_years
            },
            "assessment": {
                "distinctive_features": country.distinctive_features,
                "success_factors": country.success_factors,
                "limitations": country.limitations,
                "key_achievements": country.key_achievements,
                "ongoing_challenges": country.ongoing_challenges
            },
            "ksa_application": {
                "lessons_learned": country.lessons_learned,
                "transferability": country.transferability_to_ksa,
                "specific_recommendations": country.specific_recommendations
            }
        }
    
    def _principle_to_dict(self, principle: DesignPrinciple) -> Dict:
        """Convert design principle to dictionary."""
        return {
            "id": principle.id,
            "principle": principle.principle,
            "category": principle.category,
            "source_countries": principle.source_countries,
            "adoption_approach": principle.adoption_approach,
            "rationale": principle.rationale,
            "implementation_guidance": principle.implementation_guidance,
            "priority": principle.priority
        }
    
    def _generate_recommendations(
        self, 
        countries: Dict[str, SpatialStrategyProfile],
        principles: List[DesignPrinciple]
    ) -> Dict[str, List[str]]:
        """Generate consolidated recommendations."""
        
        return {
            "immediate_actions": [
                "Establish NSS Implementation Authority with cross-ministerial coordination power",
                "Develop comprehensive national spatial data infrastructure",
                "Implement water security as primary spatial organizing principle",
                "Create tiered planning hierarchy (National > Regional > Municipal)",
                "Define economic corridors connecting giga-projects"
            ],
            "methodology_adoption": [
                "Adopt Dutch-style scenario planning with stress testing",
                "Implement Strategic Environmental Assessment for all major projects",
                "Use Singapore's integrated transport-land use approach",
                "Apply Korea's systematic infrastructure investment appraisal",
                "Establish regular 5-year review cycles with public reporting"
            ],
            "implementation_mechanisms": [
                "Link spatial plan approval to budget allocation",
                "Create special economic zones for regional development",
                "Ensure giga-projects have regional spillover requirements",
                "Develop systematic infrastructure investment appraisal (MIRT-style)",
                "Strengthen regional authority capacity with dedicated resources"
            ],
            "content_priorities": [
                "Define functional urban hierarchy with specialized city roles",
                "Establish quantitative protected area targets (30% by 2030)",
                "Water-efficiency requirements for all development approvals",
                "TOD principles for all rail station developments",
                "Climate adaptation integration in all spatial decisions"
            ],
            "governance_improvements": [
                "Create dedicated coordination body for inter-regional planning",
                "Implement meaningful local consultation processes",
                "Establish enforcement mechanisms for planning targets",
                "Develop performance monitoring dashboard with KPIs",
                "Build regional planning capacity through training and staffing"
            ]
        }
    
    def _generate_markdown_report(self, report: Dict):
        """Generate markdown version of the report."""
        
        md_content = f"""# WS3 - International Spatial Strategy Benchmarking

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
### Top Recommendations

"""
        for rec in report['executive_summary']['top_recommendations']:
            md_content += f"1. {rec}\n"
        
        md_content += """
---

## Section 1: Benchmarking Framework

### Purpose
{purpose}

### Country Selection

| Country | Rationale |
|---------|-----------|
""".format(**report['section_1_benchmarking_framework'])
        
        for country, rationale in report['section_1_benchmarking_framework']['countries_selected'].items():
            md_content += f"| {country} | {rationale} |\n"
        
        md_content += """
---

## Section 2: Country Case Studies

"""
        for country_code, country_data in report['section_2_country_case_studies'].items():
            info = country_data['basic_info']
            md_content += f"""### {info['country_name']}

**Strategy:** {info['strategy_name']}
**Period:** {info['period']}
**Population:** {info['population_millions']}M | **Area:** {info['area_km2']:,} km² | **GDP/capita:** ${info['gdp_per_capita_usd']:,}

**Governance Model:** {country_data['characteristics']['governance_model'].title()}
**Planning Approach:** {country_data['characteristics']['planning_approach'].replace('_', ' ').title()}

#### Key Achievements
"""
            for achievement in country_data['assessment']['key_achievements']:
                md_content += f"- {achievement}\n"
            
            md_content += """
#### Lessons for KSA
"""
            for lesson in country_data['ksa_application']['lessons_learned']:
                md_content += f"- {lesson}\n"
            
            md_content += f"""
**Transferability to KSA:** {country_data['ksa_application']['transferability'].upper()}

---

"""
        
        md_content += """## Section 3: Methodology Comparison Matrix

### Dimension Scores (1-5 scale)

| Country | Data | Scenarios | Stakeholders | Environment | Implementation | M&E | Regional | Economic | Vision | Adaptability | **Average** |
|---------|------|-----------|--------------|-------------|----------------|-----|----------|----------|--------|--------------|-------------|
"""
        
        for country, score_data in report['section_3_methodology_matrix']['scores'].items():
            scores = score_data['scores']
            avg = score_data['average']
            md_content += f"| {country} | {scores['Data Infrastructure']} | {scores['Scenario Planning']} | {scores['Stakeholder Engagement']} | {scores['Environmental Integration']} | {scores['Implementation Mechanisms']} | {scores['Monitoring & Evaluation']} | {scores['Regional Coordination']} | {scores['Economic Integration']} | {scores['Long-term Vision']} | {scores['Adaptability']} | **{avg:.1f}** |\n"
        
        md_content += """
### Best Practices by Country

"""
        for country, score_data in report['section_3_methodology_matrix']['scores'].items():
            md_content += f"**{country}:**\n"
            for practice in score_data['best_practices']:
                md_content += f"- {practice}\n"
            md_content += "\n"
        
        md_content += """---

## Section 4: Country X-Fit Design Principles

### Summary

"""
        summary = report['section_4_design_principles']['summary']
        md_content += f"**Total Principles:** {summary['total_principles']}\n\n"
        
        md_content += "| Category | Count |\n|----------|-------|\n"
        for cat, count in summary['by_category'].items():
            md_content += f"| {cat.upper()} | {count} |\n"
        
        md_content += "\n| Approach | Count |\n|----------|-------|\n"
        for approach, count in summary['by_approach'].items():
            md_content += f"| {approach.upper()} | {count} |\n"
        
        md_content += """
### Critical Principles

"""
        for p in report['section_4_design_principles']['critical_principles']:
            md_content += f"""#### {p['id']}: {p['principle']}

- **Category:** {p['category'].upper()}
- **Source Countries:** {', '.join(p['source_countries'])}
- **Approach:** {p['adoption_approach'].upper()}
- **Rationale:** {p['rationale']}
- **Implementation:** {p['implementation_guidance']}

"""
        
        md_content += """### All Design Principles

| ID | Principle | Category | Sources | Approach | Priority |
|----|-----------|----------|---------|----------|----------|
"""
        for p in report['section_4_design_principles']['all_principles']:
            md_content += f"| {p['id']} | {p['principle'][:50]}... | {p['category'].upper()} | {', '.join(p['source_countries'])} | {p['adoption_approach'].upper()} | {p['priority'].upper()} |\n"
        
        md_content += """
---

## Section 5: Consolidated Recommendations

"""
        for category, recs in report['section_5_recommendations'].items():
            md_content += f"### {category.replace('_', ' ').title()}\n\n"
            for i, rec in enumerate(recs, 1):
                md_content += f"{i}. {rec}\n"
            md_content += "\n"
        
        md_content += """---

## Appendices

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
        md_path = self.output_dir / "WS3_BENCHMARKING_REPORT.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.success(f"Markdown report saved to {md_path}")


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def generate_ws3_deliverables(output_dir: str = "02_analytics/ws3_outputs") -> Dict[str, Any]:
    """Generate all WS3 deliverables."""
    generator = WS3ReportGenerator(output_dir)
    return generator.generate_all_reports()


if __name__ == "__main__":
    print("=" * 60)
    print("NSS X - WS3 International Benchmarking Generator")
    print("=" * 60)
    
    report = generate_ws3_deliverables()
    
    print("\n✅ WS3 Deliverables Generated:")
    print(f"   📄 WS3_BENCHMARKING_REPORT.json")
    print(f"   📄 WS3_BENCHMARKING_REPORT.md")
    print(f"   📄 methodology_comparison_matrix.csv")
    print(f"   📄 country_x_fit_design_principles.csv")
    
    print("\n📊 Benchmarking Summary:")
    print(f"   Countries analyzed: 5 (UAE, Singapore, Netherlands, South Korea, Malaysia)")
    print(f"   Methodology dimensions: 10")
    print(f"   Design principles: {len(report['section_4_design_principles']['all_principles'])}")
    
    critical = [p['id'] for p in report['section_4_design_principles']['critical_principles']]
    print(f"   Critical principles: {len(critical)}")
    
    print("\n🎯 Top Transferable Lessons:")
    for rec in report['executive_summary']['top_recommendations'][:3]:
        print(f"   • {rec}")
    
    print("\n✅ WS3 Complete!")
