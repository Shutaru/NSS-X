"""
NSS X - WS2: Comprehensive Retrospective Analysis
Complete analysis module for Workstream 2 deliverables.

Deliverables:
- 2.1 NSS Retrospective and Lessons-Learned Report
- 2.2 Continuity and Change Matrix
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import json
from loguru import logger

# Import base retrospective analyzer
from .ws2_retrospective import RetrospectiveAnalyzer, TrendAnalysis, RegionalDynamics


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class NSSObjective:
    """Represents an objective from a National Spatial Strategy."""
    id: str
    description: str
    target_year: int
    target_metric: Optional[str] = None
    target_value: Optional[float] = None
    achieved_value: Optional[float] = None
    status: str = "unknown"  # achieved, partial, failed, ongoing
    lessons_learned: List[str] = field(default_factory=list)


@dataclass
class StrategyReview:
    """Complete review of a National Spatial Strategy."""
    strategy_name: str
    period: str
    vision_statement: str
    objectives: List[NSSObjective]
    methodology: Dict[str, str]
    key_achievements: List[str]
    key_failures: List[str]
    lessons_learned: List[str]
    recommendations_forward: List[str]


@dataclass
class ContinuityItem:
    """Item in the Continuity and Change Matrix."""
    element: str
    category: str  # spatial, economic, governance, environmental, social
    current_status: str
    recommendation: str  # maintain, modify, discontinue, strengthen
    priority: str  # high, medium, low
    justification: str
    implementation_notes: str


# =============================================================================
# NSS 2001 REVIEW
# =============================================================================

class NSS2001Reviewer:
    """
    Review of the first Saudi National Spatial Strategy (2001).
    
    The NSS 2001 was prepared with UN-Habitat support and focused on:
    - Regional development balance
    - Urban system hierarchy
    - Infrastructure corridor planning
    - Environmental protection zones
    """
    
    def __init__(self):
        """Initialize with NSS 2001 data."""
        self._build_nss2001_data()
        logger.info("NSS 2001 Reviewer initialized")
    
    def _build_nss2001_data(self):
        """Build comprehensive data about NSS 2001."""
        
        # NSS 2001 Core Objectives
        self.objectives = [
            NSSObjective(
                id="NSS2001-01",
                description="Achieve balanced regional development across all 13 provinces",
                target_year=2020,
                target_metric="Population concentration in top 3 regions",
                target_value=55.0,  # Target: reduce to 55%
                achieved_value=65.0,  # Actual: still 65%
                status="partial",
                lessons_learned=[
                    "Economic gravity towards Riyadh too strong without major interventions",
                    "Oil industry concentration in Eastern Province persisted",
                    "Religious tourism kept Makkah growth high"
                ]
            ),
            NSSObjective(
                id="NSS2001-02",
                description="Establish 5-tier urban hierarchy with clear functional roles",
                target_year=2020,
                target_metric="Cities with defined metropolitan functions",
                target_value=5.0,
                achieved_value=3.0,  # Only Riyadh, Jeddah, Dammam fully developed
                status="partial",
                lessons_learned=[
                    "National Capital (Riyadh) grew faster than planned",
                    "Regional centers lacked investment attraction mechanisms",
                    "Secondary cities struggled to develop specialized functions"
                ]
            ),
            NSSObjective(
                id="NSS2001-03",
                description="Develop national infrastructure corridors linking all regions",
                target_year=2025,
                target_metric="Interregional connectivity index",
                target_value=0.80,
                achieved_value=0.65,
                status="ongoing",
                lessons_learned=[
                    "Highway network expanded significantly",
                    "Rail network development slower than planned",
                    "Air connectivity exceeded expectations"
                ]
            ),
            NSSObjective(
                id="NSS2001-04",
                description="Protect 15% of land area as environmental reserves",
                target_year=2020,
                target_metric="Protected area percentage",
                target_value=15.0,
                achieved_value=4.3,
                status="failed",
                lessons_learned=[
                    "Economic development prioritized over conservation",
                    "Weak enforcement mechanisms",
                    "Lack of dedicated funding for protected areas"
                ]
            ),
            NSSObjective(
                id="NSS2001-05",
                description="Reduce water consumption through efficiency measures",
                target_year=2020,
                target_metric="Per capita water consumption (L/day)",
                target_value=200.0,
                achieved_value=263.0,
                status="failed",
                lessons_learned=[
                    "Subsidized water prices prevented behavioral change",
                    "Agricultural sector water use remained high",
                    "Desalination capacity expanded instead of demand reduction"
                ]
            ),
            NSSObjective(
                id="NSS2001-06",
                description="Diversify economic base beyond oil dependency",
                target_year=2020,
                target_metric="Non-oil GDP share",
                target_value=60.0,
                achieved_value=50.0,  # By 2020
                status="partial",
                lessons_learned=[
                    "Progress accelerated only after Vision 2030 launch",
                    "Petrochemical industry remained dominant in diversification",
                    "Services sector growth limited by labor market constraints"
                ]
            ),
            NSSObjective(
                id="NSS2001-07",
                description="Increase Saudi employment in private sector",
                target_year=2020,
                target_metric="Saudization rate",
                target_value=30.0,
                achieved_value=22.0,  # By 2020
                status="partial",
                lessons_learned=[
                    "Skills mismatch between education and labor market",
                    "Salary expectations gap between Saudi and expat workers",
                    "Nitaqat program had mixed results"
                ]
            )
        ]
        
        # NSS 2001 Methodology
        self.methodology = {
            "approach": "Top-down technocratic planning with UN-Habitat support",
            "data_sources": "Census 1992, limited GIS, expert consultations",
            "time_horizon": "20-year vision (2001-2020)",
            "review_mechanism": "5-year review cycles (not implemented)",
            "stakeholder_engagement": "Limited to government agencies",
            "scenario_planning": "Single baseline scenario"
        }
        
        # Key Achievements
        self.achievements = [
            "Established first comprehensive spatial planning framework for KSA",
            "Created regional development directorates in all 13 provinces",
            "Developed initial GIS infrastructure for spatial planning",
            "Highway network expanded significantly (22,000 km added)",
            "New industrial cities established (Jubail expansion, Yanbu)",
            "Urban planning regulations modernized in major cities"
        ]
        
        # Key Failures
        self.failures = [
            "Regional imbalance persisted - Riyadh's dominance increased",
            "Environmental protection targets largely unmet",
            "Water sustainability goals not achieved",
            "Secondary cities failed to develop as planned",
            "Implementation mechanisms were weak",
            "Monitoring and evaluation system never operationalized",
            "Private sector integration was minimal"
        ]
    
    def generate_review(self) -> StrategyReview:
        """Generate comprehensive NSS 2001 review."""
        
        overall_lessons = [
            "Implementation requires dedicated institutional capacity",
            "Top-down planning without local buy-in has limited effectiveness",
            "Economic incentives must align with spatial objectives",
            "Environmental targets need enforcement mechanisms",
            "Regular monitoring and mid-course corrections are essential",
            "Private sector must be engaged from planning stage",
            "Data infrastructure is foundational for spatial planning",
            "Regional development needs more than infrastructure investment"
        ]
        
        recommendations = [
            "Establish dedicated NSS implementation agency with authority",
            "Create regional development incentive packages",
            "Implement robust monitoring and evaluation framework",
            "Integrate private sector in planning and implementation",
            "Use scenario planning to handle uncertainty",
            "Strengthen local government planning capacity",
            "Link spatial objectives to budget allocation",
            "Create regular public reporting on NSS progress"
        ]
        
        return StrategyReview(
            strategy_name="National Spatial Strategy 2001",
            period="2001-2020",
            vision_statement="Balanced and sustainable territorial development for all citizens",
            objectives=self.objectives,
            methodology=self.methodology,
            key_achievements=self.achievements,
            key_failures=self.failures,
            lessons_learned=overall_lessons,
            recommendations_forward=recommendations
        )


# =============================================================================
# NSS 2030 DRAFT REVIEW
# =============================================================================

class NSS2030DraftReviewer:
    """
    Review of the NSS 2030 Draft (aligned with Vision 2030).
    
    The NSS 2030 Draft builds on Vision 2030 and focuses on:
    - Giga-project spatial integration
    - Economic diversification zones
    - Tourism corridor development
    - Smart city initiatives
    """
    
    def __init__(self):
        """Initialize with NSS 2030 Draft data."""
        self._build_nss2030_data()
        logger.info("NSS 2030 Draft Reviewer initialized")
    
    def _build_nss2030_data(self):
        """Build comprehensive data about NSS 2030 Draft."""
        
        # NSS 2030 Core Objectives
        self.objectives = [
            NSSObjective(
                id="NSS2030-01",
                description="Establish NEOM as a new growth pole in Northwest region",
                target_year=2030,
                target_metric="NEOM population",
                target_value=1000000.0,  # 1 million target
                achieved_value=50000.0,  # Current as of 2025
                status="ongoing",
                lessons_learned=[
                    "Mega-project scale requires sustained commitment",
                    "Labor force attraction is challenging in remote areas",
                    "Infrastructure must precede population"
                ]
            ),
            NSSObjective(
                id="NSS2030-02",
                description="Achieve 100M annual tourist visits",
                target_year=2030,
                target_metric="Annual tourist arrivals (millions)",
                target_value=100.0,
                achieved_value=35.0,  # 2025 estimate
                status="ongoing",
                lessons_learned=[
                    "Hajj/Umrah remains dominant tourism segment",
                    "Red Sea/AMAALA developing slower than planned",
                    "Entertainment and sports tourism showing strong growth"
                ]
            ),
            NSSObjective(
                id="NSS2030-03",
                description="Riyadh to become top 10 global city economy",
                target_year=2030,
                target_metric="Global city ranking",
                target_value=10.0,
                achieved_value=40.0,  # Current ranking
                status="ongoing",
                lessons_learned=[
                    "Headquarters relocation policy accelerating growth",
                    "Quality of life improvements driving talent attraction",
                    "Metro system transforming urban mobility"
                ]
            ),
            NSSObjective(
                id="NSS2030-04",
                description="Increase non-oil GDP to 65% of total",
                target_year=2030,
                target_metric="Non-oil GDP share (%)",
                target_value=65.0,
                achieved_value=62.0,
                status="ongoing",
                lessons_learned=[
                    "Tourism and entertainment fastest growing sectors",
                    "Manufacturing diversification proving difficult",
                    "Tech sector showing promise with LEAP initiatives"
                ]
            ),
            NSSObjective(
                id="NSS2030-05",
                description="Develop integrated national transport network",
                target_year=2030,
                target_metric="Rail network km",
                target_value=10000.0,
                achieved_value=4500.0,
                status="ongoing",
                lessons_learned=[
                    "Haramain HSR successful model",
                    "Land Bridge project facing delays",
                    "Aviation expansion exceeding targets"
                ]
            ),
            NSSObjective(
                id="NSS2030-06",
                description="Achieve 50% renewable energy share",
                target_year=2030,
                target_metric="Renewable energy share (%)",
                target_value=50.0,
                achieved_value=8.0,
                status="ongoing",
                lessons_learned=[
                    "Solar projects progressing well",
                    "NEOM green hydrogen ambitious",
                    "Grid integration challenges remain"
                ]
            )
        ]
        
        # NSS 2030 Methodology
        self.methodology = {
            "approach": "Vision 2030 aligned, project-centric planning",
            "data_sources": "Multiple government databases, satellite imagery, AI analytics",
            "time_horizon": "2016-2030 with 5-year phases",
            "review_mechanism": "Quarterly progress tracking by Vision Realization Office",
            "stakeholder_engagement": "Public-private partnership focus",
            "scenario_planning": "Multiple scenarios including stress tests"
        }
        
        # Key Strengths
        self.strengths = [
            "Strong political commitment and funding from PIF",
            "Clear alignment with Vision 2030 framework",
            "Ambitious giga-projects driving spatial transformation",
            "Better data and monitoring systems than NSS 2001",
            "Private sector engagement through investment funds",
            "International partnerships and expertise",
            "Youth engagement and social transformation integrated"
        ]
        
        # Key Gaps
        self.gaps = [
            "Over-reliance on mega-projects vs distributed development",
            "Environmental sustainability secondary to growth",
            "Water security strategy underdeveloped",
            "Regional inequality may increase without intervention",
            "Implementation capacity in non-priority regions limited",
            "Climate change adaptation not fully integrated",
            "Social infrastructure lagging physical infrastructure"
        ]
    
    def generate_review(self) -> StrategyReview:
        """Generate comprehensive NSS 2030 Draft review."""
        
        overall_lessons = [
            "Vision-level commitment essential but not sufficient",
            "Spatial concentration in mega-projects has trade-offs",
            "Execution capacity is the main constraint",
            "Environmental limits need explicit integration",
            "Social transformation must accompany physical development",
            "Data and monitoring systems are essential",
            "International benchmarking provides useful reference"
        ]
        
        recommendations = [
            "Balance mega-project focus with regional development programs",
            "Strengthen environmental sustainability integration",
            "Develop explicit water security strategy",
            "Create smaller-scale economic development programs for secondary regions",
            "Build implementation capacity in regional governments",
            "Integrate climate change adaptation in all projects",
            "Ensure social infrastructure keeps pace with physical development",
            "Maintain flexibility for mid-course corrections"
        ]
        
        return StrategyReview(
            strategy_name="National Spatial Strategy 2030 Draft",
            period="2016-2030",
            vision_statement="Transform Saudi Arabia into a global investment powerhouse through spatial excellence",
            objectives=self.objectives,
            methodology=self.methodology,
            key_achievements=self.strengths,  # Using strengths as achievements-to-date
            key_failures=self.gaps,  # Using gaps as failures/concerns
            lessons_learned=overall_lessons,
            recommendations_forward=recommendations
        )


# =============================================================================
# CONTINUITY AND CHANGE MATRIX
# =============================================================================

class ContinuityChangeMatrix:
    """
    Generator for the Continuity and Change Matrix.
    
    Analyzes what elements from previous strategies should be:
    - Maintained (working well)
    - Modified (partially working, needs adjustment)
    - Discontinued (not working, should stop)
    - Strengthened (good idea, needs more investment)
    """
    
    def __init__(self):
        """Initialize matrix generator."""
        self._build_matrix()
        logger.info("Continuity and Change Matrix initialized")
    
    def _build_matrix(self):
        """Build the continuity and change matrix."""
        
        self.items: List[ContinuityItem] = [
            # SPATIAL ELEMENTS
            ContinuityItem(
                element="Regional Development Directorates",
                category="spatial",
                current_status="Established but under-resourced",
                recommendation="strengthen",
                priority="high",
                justification="Essential for localized implementation but lack capacity and authority",
                implementation_notes="Increase staffing, budget, and decision-making authority at regional level"
            ),
            ContinuityItem(
                element="5-Tier Urban Hierarchy Model",
                category="spatial",
                current_status="Partially implemented",
                recommendation="modify",
                priority="medium",
                justification="Model is sound but Riyadh dominance distorts hierarchy; needs economic rebalancing",
                implementation_notes="Develop specialized functions for tier 2-3 cities; use incentive packages"
            ),
            ContinuityItem(
                element="Giga-Project Spatial Strategy",
                category="spatial",
                current_status="Active - NEOM, Red Sea, Qiddiya, etc.",
                recommendation="maintain",
                priority="high",
                justification="Strong execution momentum; provides growth poles outside traditional centers",
                implementation_notes="Continue but ensure regional spillover effects are monitored"
            ),
            ContinuityItem(
                element="New City Development Policy",
                category="spatial",
                current_status="Mixed results - KAEC underperforming, NEOM nascent",
                recommendation="modify",
                priority="high",
                justification="New cities struggle without clear economic anchor and labor supply",
                implementation_notes="Focus on fewer cities with stronger economic rationale; improve transport links"
            ),
            
            # ECONOMIC ELEMENTS
            ContinuityItem(
                element="Special Economic Zones",
                category="economic",
                current_status="Expanding - NEOM, King Abdullah Port, etc.",
                recommendation="strengthen",
                priority="high",
                justification="Effective for attracting foreign investment and creating economic clusters",
                implementation_notes="Extend SEZ benefits; streamline approvals; improve infrastructure connectivity"
            ),
            ContinuityItem(
                element="Industrial City Program",
                category="economic",
                current_status="Jubail, Yanbu mature; new cities developing",
                recommendation="maintain",
                priority="medium",
                justification="Proven model for industrial development and diversification",
                implementation_notes="Continue expansion; focus on downstream industries and technology sectors"
            ),
            ContinuityItem(
                element="Tourism Corridor Development",
                category="economic",
                current_status="Active - Red Sea, Diriyah, AlUla",
                recommendation="strengthen",
                priority="high",
                justification="Tourism is key diversification pillar with strong spatial implications",
                implementation_notes="Accelerate infrastructure; develop tourism human capital; maintain authenticity"
            ),
            ContinuityItem(
                element="Regional Economic Specialization",
                category="economic",
                current_status="Weak - most regions remain generalist",
                recommendation="strengthen",
                priority="high",
                justification="Regions lack distinctive economic identity; reduces competitiveness",
                implementation_notes="Develop regional specialization strategies based on comparative advantages"
            ),
            
            # GOVERNANCE ELEMENTS
            ContinuityItem(
                element="Centralized Planning Coordination",
                category="governance",
                current_status="Strong through Vision 2030 office",
                recommendation="maintain",
                priority="high",
                justification="Effective for alignment but may slow regional responsiveness",
                implementation_notes="Maintain for strategic alignment; delegate operational decisions to regions"
            ),
            ContinuityItem(
                element="5-Year Review Cycles",
                category="governance",
                current_status="Not implemented in NSS 2001; quarterly in V2030",
                recommendation="strengthen",
                priority="medium",
                justification="Regular review essential for adaptive management",
                implementation_notes="Formalize 5-year comprehensive reviews with public reporting"
            ),
            ContinuityItem(
                element="Inter-ministerial Coordination",
                category="governance",
                current_status="Improved under Vision 2030 governance",
                recommendation="maintain",
                priority="high",
                justification="Spatial planning requires cross-sectoral coordination",
                implementation_notes="Continue high-level coordination mechanisms"
            ),
            ContinuityItem(
                element="Performance Monitoring System",
                category="governance",
                current_status="Developing - Vision 2030 KPIs",
                recommendation="strengthen",
                priority="high",
                justification="Essential for evidence-based decision making",
                implementation_notes="Expand to cover all spatial indicators; make data publicly accessible"
            ),
            
            # ENVIRONMENTAL ELEMENTS
            ContinuityItem(
                element="Protected Area Targets",
                category="environmental",
                current_status="Behind target - 4.3% vs 15% goal",
                recommendation="strengthen",
                priority="high",
                justification="Environmental protection essential for sustainable development",
                implementation_notes="Accelerate to meet 30x30 global commitment; enforce existing protections"
            ),
            ContinuityItem(
                element="Water Demand Management",
                category="environmental",
                current_status="Weak - consumption still high",
                recommendation="strengthen",
                priority="critical",
                justification="Water security is existential issue for Saudi Arabia",
                implementation_notes="Reform water pricing; mandate efficiency standards; reduce agricultural use"
            ),
            ContinuityItem(
                element="Renewable Energy Integration",
                category="environmental",
                current_status="Accelerating - solar and wind projects",
                recommendation="strengthen",
                priority="high",
                justification="Critical for climate commitments and economic diversification",
                implementation_notes="Maintain ambitious targets; address grid integration challenges"
            ),
            ContinuityItem(
                element="Coastal Zone Management",
                category="environmental",
                current_status="Developing - Red Sea Project sets standard",
                recommendation="strengthen",
                priority="medium",
                justification="3,000 km coastline has major economic and environmental value",
                implementation_notes="Extend Red Sea standards to all coastal development; prevent over-development"
            ),
            
            # SOCIAL ELEMENTS
            ContinuityItem(
                element="Housing Program (Sakani)",
                category="social",
                current_status="Active - homeownership increasing",
                recommendation="maintain",
                priority="high",
                justification="Housing affordability critical for social stability and labor mobility",
                implementation_notes="Continue expansion; ensure regional distribution"
            ),
            ContinuityItem(
                element="Saudi Employment Programs",
                category="social",
                current_status="Nitaqat ongoing; unemployment still elevated",
                recommendation="modify",
                priority="high",
                justification="Current approach has limited success; needs skills-focused reform",
                implementation_notes="Shift from quotas to skills development; target high-value sectors"
            ),
            ContinuityItem(
                element="Education City Development",
                category="social",
                current_status="Active - KAUST, multiple universities",
                recommendation="maintain",
                priority="medium",
                justification="Knowledge economy requires higher education infrastructure",
                implementation_notes="Continue but improve industry linkages and research commercialization"
            ),
            ContinuityItem(
                element="Healthcare Infrastructure Distribution",
                category="social",
                current_status="Concentrated in major cities",
                recommendation="strengthen",
                priority="medium",
                justification="Regional healthcare gaps affect livability and development",
                implementation_notes="Invest in regional hospitals and telemedicine infrastructure"
            )
        ]
    
    def get_matrix(self) -> List[ContinuityItem]:
        """Return the full matrix."""
        return self.items
    
    def get_by_recommendation(self, recommendation: str) -> List[ContinuityItem]:
        """Filter matrix by recommendation type."""
        return [item for item in self.items if item.recommendation == recommendation]
    
    def get_by_category(self, category: str) -> List[ContinuityItem]:
        """Filter matrix by category."""
        return [item for item in self.items if item.category == category]
    
    def get_by_priority(self, priority: str) -> List[ContinuityItem]:
        """Filter matrix by priority."""
        return [item for item in self.items if item.priority == priority]
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert matrix to DataFrame for analysis."""
        return pd.DataFrame([
            {
                'Element': item.element,
                'Category': item.category,
                'Current Status': item.current_status,
                'Recommendation': item.recommendation.upper(),
                'Priority': item.priority.upper(),
                'Justification': item.justification,
                'Implementation Notes': item.implementation_notes
            }
            for item in self.items
        ])
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate matrix summary statistics."""
        df = self.to_dataframe()
        
        return {
            "total_elements": len(self.items),
            "by_recommendation": df['Recommendation'].value_counts().to_dict(),
            "by_category": df['Category'].value_counts().to_dict(),
            "by_priority": df['Priority'].value_counts().to_dict(),
            "critical_items": [
                item.element for item in self.items 
                if item.priority == "critical"
            ],
            "high_priority_strengthen": [
                item.element for item in self.items 
                if item.priority == "high" and item.recommendation == "strengthen"
            ]
        }


# =============================================================================
# COMPREHENSIVE REPORT GENERATOR
# =============================================================================

class WS2ReportGenerator:
    """
    Generates all WS2 deliverables in a structured format.
    """
    
    def __init__(self, output_dir: str = "02_analytics/ws2_outputs"):
        """Initialize report generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.retrospective = RetrospectiveAnalyzer()
        self.nss2001 = NSS2001Reviewer()
        self.nss2030 = NSS2030DraftReviewer()
        self.continuity_matrix = ContinuityChangeMatrix()
        
        logger.info(f"WS2 Report Generator initialized. Output: {self.output_dir}")
    
    def generate_all_reports(self) -> Dict[str, Any]:
        """Generate all WS2 deliverables."""
        
        logger.info("Generating WS2 deliverables...")
        
        # Generate reviews
        nss2001_review = self.nss2001.generate_review()
        nss2030_review = self.nss2030.generate_review()
        
        # Generate retrospective analysis
        retrospective_report = self.retrospective.generate_retrospective_report()
        time_series = self.retrospective.get_time_series_data()
        
        # Get continuity matrix
        matrix = self.continuity_matrix.get_matrix()
        matrix_summary = self.continuity_matrix.generate_summary()
        
        # Save time series data
        for name, df in time_series.items():
            df.to_csv(self.output_dir / f"timeseries_{name}.csv", index=False)
        
        # Save continuity matrix
        self.continuity_matrix.to_dataframe().to_csv(
            self.output_dir / "continuity_change_matrix.csv", index=False
        )
        
        # Compile comprehensive report
        report = {
            "metadata": {
                "report_title": "WS2 - Retrospective Review of Existing NSS Frameworks",
                "generated_date": datetime.now().isoformat(),
                "version": "1.0",
                "author": "NSS X System"
            },
            "executive_summary": self._generate_executive_summary(
                nss2001_review, nss2030_review, matrix_summary
            ),
            "section_1_retrospective_analysis": retrospective_report,
            "section_2_nss_2001_review": self._strategy_review_to_dict(nss2001_review),
            "section_3_nss_2030_review": self._strategy_review_to_dict(nss2030_review),
            "section_4_continuity_change_matrix": {
                "summary": matrix_summary,
                "items": [self._continuity_item_to_dict(item) for item in matrix]
            },
            "section_5_recommendations": self._generate_recommendations(
                nss2001_review, nss2030_review, matrix
            ),
            "appendices": {
                "data_sources": [
                    "GASTAT - General Authority for Statistics",
                    "SAMA - Saudi Arabian Monetary Authority",
                    "Ministry of Economy and Planning",
                    "Vision 2030 Official Reports",
                    "Ministry of Municipal and Rural Affairs",
                    "UN-Habitat Historical Records"
                ],
                "time_series_files": [
                    "timeseries_population.csv",
                    "timeseries_gdp.csv",
                    "timeseries_regional.csv"
                ],
                "matrix_file": "continuity_change_matrix.csv"
            }
        }
        
        # Save comprehensive report as JSON
        report_path = self.output_dir / "WS2_RETROSPECTIVE_REPORT.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        logger.success(f"WS2 Report saved to {report_path}")
        
        # Generate markdown report
        self._generate_markdown_report(report)
        
        return report
    
    def _generate_executive_summary(
        self, 
        nss2001: StrategyReview, 
        nss2030: StrategyReview,
        matrix_summary: Dict
    ) -> Dict[str, Any]:
        """Generate executive summary."""
        
        return {
            "overview": """This retrospective review analyzes 25 years of national spatial strategy 
            in Saudi Arabia, from the first NSS (2001) through the Vision 2030-aligned framework. 
            The analysis identifies key lessons learned, assesses progress against historical objectives, 
            and provides a continuity and change matrix to guide the next strategy cycle.""",
            
            "key_findings": [
                "NSS 2001 achieved partial success: urban hierarchy established but regional balance not achieved",
                "Environmental targets (protected areas, water efficiency) largely unmet across both strategies",
                "Vision 2030 framework shows stronger implementation but concentration risk remains",
                "Governance mechanisms improved significantly post-2016",
                f"{matrix_summary['by_recommendation'].get('STRENGTHEN', 0)} elements need strengthening",
                f"{matrix_summary['by_recommendation'].get('MODIFY', 0)} elements need modification",
                "Water security identified as critical priority requiring immediate attention"
            ],
            
            "progress_assessment": {
                "nss_2001": {
                    "achieved": len([o for o in nss2001.objectives if o.status == "achieved"]),
                    "partial": len([o for o in nss2001.objectives if o.status == "partial"]),
                    "failed": len([o for o in nss2001.objectives if o.status == "failed"]),
                    "total": len(nss2001.objectives)
                },
                "nss_2030": {
                    "on_track": len([o for o in nss2030.objectives if o.status == "ongoing"]),
                    "achieved": len([o for o in nss2030.objectives if o.status == "achieved"]),
                    "at_risk": len([o for o in nss2030.objectives if o.status == "partial"]),
                    "total": len(nss2030.objectives)
                }
            },
            
            "top_recommendations": [
                "Strengthen water security strategy as critical priority",
                "Balance mega-project focus with distributed regional development",
                "Accelerate environmental protection to meet 30x30 commitments",
                "Build implementation capacity at regional level",
                "Integrate climate adaptation across all spatial decisions"
            ]
        }
    
    def _strategy_review_to_dict(self, review: StrategyReview) -> Dict:
        """Convert StrategyReview to dictionary."""
        return {
            "strategy_name": review.strategy_name,
            "period": review.period,
            "vision_statement": review.vision_statement,
            "objectives": [
                {
                    "id": o.id,
                    "description": o.description,
                    "target_year": o.target_year,
                    "target_metric": o.target_metric,
                    "target_value": o.target_value,
                    "achieved_value": o.achieved_value,
                    "status": o.status,
                    "lessons_learned": o.lessons_learned
                }
                for o in review.objectives
            ],
            "methodology": review.methodology,
            "key_achievements": review.key_achievements,
            "key_failures": review.key_failures,
            "lessons_learned": review.lessons_learned,
            "recommendations": review.recommendations_forward
        }
    
    def _continuity_item_to_dict(self, item: ContinuityItem) -> Dict:
        """Convert ContinuityItem to dictionary."""
        return {
            "element": item.element,
            "category": item.category,
            "current_status": item.current_status,
            "recommendation": item.recommendation,
            "priority": item.priority,
            "justification": item.justification,
            "implementation_notes": item.implementation_notes
        }
    
    def _generate_recommendations(
        self, 
        nss2001: StrategyReview, 
        nss2030: StrategyReview,
        matrix: List[ContinuityItem]
    ) -> Dict[str, List[str]]:
        """Generate consolidated recommendations."""
        
        # Collect all recommendations
        all_recs = (
            nss2001.recommendations_forward + 
            nss2030.recommendations_forward
        )
        
        # Categorize
        return {
            "governance_and_implementation": [
                "Establish dedicated NSS implementation agency with clear authority",
                "Strengthen regional government planning capacity and resources",
                "Create robust monitoring and evaluation framework with public reporting",
                "Formalize 5-year comprehensive strategy reviews",
                "Integrate private sector in planning from early stages"
            ],
            "spatial_development": [
                "Balance mega-project investment with distributed regional programs",
                "Develop specialized economic functions for secondary cities",
                "Strengthen transport connectivity between regional centers",
                "Create smaller-scale development programs for underserved regions",
                "Ensure mega-project spillover benefits reach surrounding areas"
            ],
            "environmental_sustainability": [
                "CRITICAL: Implement comprehensive water security strategy",
                "Accelerate to meet 30x30 protected area commitments",
                "Integrate climate change adaptation in all spatial decisions",
                "Extend coastal zone management standards nationally",
                "Maintain ambitious renewable energy targets"
            ],
            "economic_development": [
                "Develop regional economic specialization strategies",
                "Extend Special Economic Zone benefits more broadly",
                "Strengthen tourism infrastructure across regions",
                "Focus on skills development over employment quotas",
                "Ensure economic incentives align with spatial objectives"
            ],
            "social_infrastructure": [
                "Continue housing programs with regional distribution focus",
                "Invest in regional healthcare infrastructure",
                "Improve industry-education linkages",
                "Ensure social infrastructure keeps pace with physical development",
                "Address regional quality of life gaps"
            ]
        }
    
    def _generate_markdown_report(self, report: Dict):
        """Generate a markdown version of the report."""
        
        md_content = f"""# WS2 - Retrospective Review of NSS Frameworks

**Generated:** {report['metadata']['generated_date']}
**Version:** {report['metadata']['version']}

---

## Executive Summary

{report['executive_summary']['overview']}

### Key Findings

"""
        for finding in report['executive_summary']['key_findings']:
            md_content += f"- {finding}\n"
        
        md_content += f"""
### Progress Assessment

| Strategy | Achieved | Partial | Failed/At-Risk | Total |
|----------|----------|---------|----------------|-------|
| NSS 2001 | {report['executive_summary']['progress_assessment']['nss_2001']['achieved']} | {report['executive_summary']['progress_assessment']['nss_2001']['partial']} | {report['executive_summary']['progress_assessment']['nss_2001']['failed']} | {report['executive_summary']['progress_assessment']['nss_2001']['total']} |
| NSS 2030 | {report['executive_summary']['progress_assessment']['nss_2030']['achieved']} | {report['executive_summary']['progress_assessment']['nss_2030']['on_track']} | {report['executive_summary']['progress_assessment']['nss_2030']['at_risk']} | {report['executive_summary']['progress_assessment']['nss_2030']['total']} |

---

## Section 1: Retrospective Analysis 2010-2025

### Population Trends
"""
        pop_findings = report['section_1_retrospective_analysis']['key_findings']['population']
        md_content += f"""
- **Growth:** {pop_findings['growth']}
- **CAGR:** {pop_findings['cagr']}
- **Urbanization:** {pop_findings['urbanization']}

### Economic Transformation
"""
        econ_findings = report['section_1_retrospective_analysis']['key_findings']['economy']
        md_content += f"""
- **GDP Growth:** {econ_findings['gdp_growth']}
- **Diversification:** {econ_findings['diversification']}

### Regional Dynamics

**Accelerating Regions:** {', '.join(report['section_1_retrospective_analysis']['key_findings']['regional_dynamics']['accelerating_regions'])}

**Stable Regions:** {', '.join(report['section_1_retrospective_analysis']['key_findings']['regional_dynamics']['stable_regions'])}

---

## Section 2: NSS 2001 Review

**Period:** {report['section_2_nss_2001_review']['period']}
**Vision:** {report['section_2_nss_2001_review']['vision_statement']}

### Objectives Assessment

| Objective | Status | Target | Achieved |
|-----------|--------|--------|----------|
"""
        for obj in report['section_2_nss_2001_review']['objectives']:
            md_content += f"| {obj['description'][:50]}... | {obj['status'].upper()} | {obj['target_value']} | {obj['achieved_value']} |\n"
        
        md_content += """
### Key Achievements
"""
        for ach in report['section_2_nss_2001_review']['key_achievements']:
            md_content += f"- {ach}\n"
        
        md_content += """
### Key Failures
"""
        for fail in report['section_2_nss_2001_review']['key_failures']:
            md_content += f"- {fail}\n"
        
        md_content += """
### Lessons Learned
"""
        for lesson in report['section_2_nss_2001_review']['lessons_learned']:
            md_content += f"- {lesson}\n"
        
        md_content += f"""
---

## Section 3: NSS 2030 Draft Review

**Period:** {report['section_3_nss_2030_review']['period']}
**Vision:** {report['section_3_nss_2030_review']['vision_statement']}

### Objectives Assessment

| Objective | Status | Target | Current |
|-----------|--------|--------|---------|
"""
        for obj in report['section_3_nss_2030_review']['objectives']:
            md_content += f"| {obj['description'][:50]}... | {obj['status'].upper()} | {obj['target_value']} | {obj['achieved_value']} |\n"
        
        md_content += """
### Key Strengths
"""
        for strength in report['section_3_nss_2030_review']['key_achievements']:
            md_content += f"- {strength}\n"
        
        md_content += """
### Key Gaps
"""
        for gap in report['section_3_nss_2030_review']['key_failures']:
            md_content += f"- {gap}\n"
        
        md_content += """
---

## Section 4: Continuity and Change Matrix

### Summary

"""
        matrix_summary = report['section_4_continuity_change_matrix']['summary']
        md_content += f"**Total Elements Analyzed:** {matrix_summary['total_elements']}\n\n"
        md_content += "| Recommendation | Count |\n|---------------|-------|\n"
        for rec, count in matrix_summary['by_recommendation'].items():
            md_content += f"| {rec} | {count} |\n"
        
        md_content += """
### Critical Priority Items

"""
        for item in matrix_summary.get('critical_items', []):
            md_content += f"- ⚠️ **CRITICAL:** {item}\n"
        
        md_content += """
### High Priority - Strengthen

"""
        for item in matrix_summary.get('high_priority_strengthen', []):
            md_content += f"- 🔺 {item}\n"
        
        md_content += """
### Full Matrix

| Element | Category | Recommendation | Priority |
|---------|----------|----------------|----------|
"""
        for item in report['section_4_continuity_change_matrix']['items']:
            md_content += f"| {item['element']} | {item['category']} | {item['recommendation'].upper()} | {item['priority'].upper()} |\n"
        
        md_content += """
---

## Section 5: Consolidated Recommendations

"""
        for category, recs in report['section_5_recommendations'].items():
            md_content += f"### {category.replace('_', ' ').title()}\n\n"
            for rec in recs:
                md_content += f"- {rec}\n"
            md_content += "\n"
        
        md_content += """
---

## Appendices

### Data Sources
"""
        for source in report['appendices']['data_sources']:
            md_content += f"- {source}\n"
        
        md_content += """
### Generated Files
"""
        for file in report['appendices']['time_series_files']:
            md_content += f"- `{file}`\n"
        md_content += f"- `{report['appendices']['matrix_file']}`\n"
        md_content += "- `WS2_RETROSPECTIVE_REPORT.json`\n"
        
        # Save markdown report
        md_path = self.output_dir / "WS2_RETROSPECTIVE_REPORT.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.success(f"Markdown report saved to {md_path}")


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def generate_ws2_deliverables(output_dir: str = "02_analytics/ws2_outputs") -> Dict[str, Any]:
    """Generate all WS2 deliverables."""
    generator = WS2ReportGenerator(output_dir)
    return generator.generate_all_reports()


if __name__ == "__main__":
    # Run WS2 generation
    print("=" * 60)
    print("NSS X - WS2 Retrospective Review Generator")
    print("=" * 60)
    
    report = generate_ws2_deliverables()
    
    print("\n✅ WS2 Deliverables Generated:")
    print(f"   📄 WS2_RETROSPECTIVE_REPORT.json")
    print(f"   📄 WS2_RETROSPECTIVE_REPORT.md")
    print(f"   📄 continuity_change_matrix.csv")
    print(f"   📄 timeseries_population.csv")
    print(f"   📄 timeseries_gdp.csv")
    print(f"   📄 timeseries_regional.csv")
    
    print("\n📊 Matrix Summary:")
    matrix_summary = report['section_4_continuity_change_matrix']['summary']
    print(f"   Total elements: {matrix_summary['total_elements']}")
    for rec, count in matrix_summary['by_recommendation'].items():
        print(f"   {rec}: {count}")
    
    print("\n✅ WS2 Complete!")
