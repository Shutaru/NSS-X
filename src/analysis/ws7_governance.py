"""
NSS X - WS7: Governance and Implementation Framework
Complete governance framework with RACI matrix and KPI monitoring system.

Deliverables:
- 7.1 NSS Governance and Implementation Framework
- 7.2 Ministry Accountability and Decision Rights Matrix (RACI)
- 7.3 Monitoring and KPI Framework
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

class ResponsibilityLevel(Enum):
    RESPONSIBLE = "R"       # Does the work
    ACCOUNTABLE = "A"       # Final decision maker
    CONSULTED = "C"         # Input provider
    INFORMED = "I"          # Kept informed
    NOT_INVOLVED = "-"      # Not involved


@dataclass
class GovernanceBody:
    """Governance body in the NSS framework."""
    name: str
    name_ar: str
    level: str  # national, regional, local
    body_type: str  # authority, committee, secretariat
    mandate: str
    composition: List[str]
    key_functions: List[str]
    decision_rights: List[str]
    meeting_frequency: str
    reports_to: Optional[str]
    secretariat: Optional[str]


@dataclass
class DecisionProcess:
    """Decision process definition."""
    process_name: str
    description: str
    trigger: str
    steps: List[Dict[str, str]]
    decision_authority: str
    timeline_days: int
    escalation_path: str
    output: str


@dataclass
class RACIEntry:
    """RACI matrix entry."""
    activity: str
    activity_category: str
    nss_authority: ResponsibilityLevel
    momra: ResponsibilityLevel  # Ministry of Municipal and Rural Affairs
    mowe: ResponsibilityLevel   # Ministry of Environment, Water and Agriculture
    mot: ResponsibilityLevel    # Ministry of Transport
    misa: ResponsibilityLevel   # Ministry of Investment
    moi: ResponsibilityLevel    # Ministry of Industry
    tourism: ResponsibilityLevel  # Ministry of Tourism
    housing: ResponsibilityLevel  # Ministry of Housing
    regions: ResponsibilityLevel  # Regional Authorities
    pif: ResponsibilityLevel     # Public Investment Fund
    royal_commission: ResponsibilityLevel  # Royal Commissions (NEOM, AlUla, etc.)


@dataclass
class KPI:
    """Key Performance Indicator."""
    kpi_id: str
    name: str
    category: str  # demographic, economic, environmental, infrastructure, governance
    description: str
    unit: str
    baseline_2024: float
    target_2030: float
    target_2040: float
    target_2050: float
    data_source: str
    responsible_entity: str
    reporting_frequency: str
    calculation_method: str


@dataclass
class MonitoringMechanism:
    """Monitoring mechanism definition."""
    mechanism_name: str
    purpose: str
    frequency: str
    participants: List[str]
    outputs: List[str]
    review_criteria: List[str]


# =============================================================================
# GOVERNANCE FRAMEWORK BUILDER
# =============================================================================

class GovernanceFrameworkBuilder:
    """
    Builds the complete governance framework.
    """
    
    def __init__(self):
        """Initialize governance framework builder."""
        self.bodies = self._build_governance_bodies()
        self.processes = self._build_decision_processes()
        logger.info(f"Governance Framework: {len(self.bodies)} bodies, {len(self.processes)} processes")
    
    def _build_governance_bodies(self) -> List[GovernanceBody]:
        """Build governance bodies."""
        
        bodies = [
            # NATIONAL LEVEL
            GovernanceBody(
                name="National Spatial Strategy Authority (NSSA)",
                name_ar="هيئة الاستراتيجية المكانية الوطنية",
                level="national",
                body_type="authority",
                mandate="Lead, coordinate, and monitor implementation of the NSS across all sectors and regions",
                composition=[
                    "Chairperson (Minister-level appointee)",
                    "Deputy Chairperson (Technical)",
                    "Representatives from key ministries",
                    "Regional Development Directors",
                    "Private Sector Representatives"
                ],
                key_functions=[
                    "Set strategic priorities for NSS implementation",
                    "Coordinate sectoral and regional strategies with NSS",
                    "Arbitrate inter-ministerial and inter-regional conflicts",
                    "Monitor progress against NSS targets",
                    "Propose policy adjustments to Council of Ministers",
                    "Manage NSS stakeholder engagement"
                ],
                decision_rights=[
                    "Approve regional spatial plans",
                    "Issue spatial development guidelines",
                    "Recommend project spatial alignment",
                    "Escalate major conflicts to Council"
                ],
                meeting_frequency="Monthly",
                reports_to="Council of Economic and Development Affairs (CEDA)",
                secretariat="NSS Technical Secretariat"
            ),
            
            GovernanceBody(
                name="NSS Technical Secretariat",
                name_ar="الأمانة الفنية للاستراتيجية المكانية",
                level="national",
                body_type="secretariat",
                mandate="Provide technical support, analysis, and coordination for NSS implementation",
                composition=[
                    "Secretary General",
                    "Planning & Analysis Division",
                    "Monitoring & Evaluation Division",
                    "Regional Coordination Division",
                    "Stakeholder Engagement Division",
                    "GIS & Data Management Division"
                ],
                key_functions=[
                    "Prepare technical analysis and recommendations",
                    "Coordinate with ministerial technical teams",
                    "Manage NSS data platform and monitoring system",
                    "Draft policy documents and guidelines",
                    "Organize stakeholder consultations",
                    "Prepare NSSA meeting materials"
                ],
                decision_rights=[
                    "Technical recommendations",
                    "Data standards",
                    "Process guidelines"
                ],
                meeting_frequency="Weekly",
                reports_to="National Spatial Strategy Authority",
                secretariat=None
            ),
            
            GovernanceBody(
                name="Inter-Ministerial Spatial Coordination Committee",
                name_ar="اللجنة الوزارية التنسيقية للتنمية المكانية",
                level="national",
                body_type="committee",
                mandate="Coordinate sectoral strategies and investments with NSS spatial framework",
                composition=[
                    "Deputy Ministers from key ministries",
                    "Planning Directors from each ministry",
                    "NSS Technical Secretariat"
                ],
                key_functions=[
                    "Align sectoral strategies with NSS",
                    "Coordinate cross-sectoral investments",
                    "Resolve sector-level conflicts",
                    "Share best practices",
                    "Review spatial impact assessments"
                ],
                decision_rights=[
                    "Recommend sectoral alignment actions",
                    "Approve joint investment coordination"
                ],
                meeting_frequency="Bi-weekly",
                reports_to="National Spatial Strategy Authority",
                secretariat="NSS Technical Secretariat"
            ),
            
            # SECTORAL WORKING GROUPS
            GovernanceBody(
                name="Water-Land Nexus Working Group",
                name_ar="مجموعة عمل العلاقة بين المياه والأراضي",
                level="national",
                body_type="committee",
                mandate="Ensure all spatial development decisions account for water availability and sustainability",
                composition=[
                    "Ministry of Environment, Water and Agriculture",
                    "NSS Technical Secretariat",
                    "Desalination Conversion Corporation",
                    "Regional Water Authorities"
                ],
                key_functions=[
                    "Water impact assessment for development proposals",
                    "Water allocation recommendations by region",
                    "Agricultural transition monitoring",
                    "Desalination capacity planning"
                ],
                decision_rights=[
                    "Water availability certification for major projects"
                ],
                meeting_frequency="Monthly",
                reports_to="Inter-Ministerial Coordination Committee",
                secretariat="NSS Technical Secretariat"
            ),
            
            GovernanceBody(
                name="Infrastructure Coordination Working Group",
                name_ar="مجموعة عمل تنسيق البنية التحتية",
                level="national",
                body_type="committee",
                mandate="Coordinate infrastructure planning across transport, energy, digital, and utilities",
                composition=[
                    "Ministry of Transport",
                    "Ministry of Energy",
                    "Ministry of Communications",
                    "Utility Providers",
                    "NSS Technical Secretariat"
                ],
                key_functions=[
                    "Infrastructure master plan coordination",
                    "Corridor development sequencing",
                    "Utility co-location optimization",
                    "Investment prioritization"
                ],
                decision_rights=[
                    "Infrastructure alignment recommendations"
                ],
                meeting_frequency="Monthly",
                reports_to="Inter-Ministerial Coordination Committee",
                secretariat="NSS Technical Secretariat"
            ),
            
            GovernanceBody(
                name="Environmental Protection Working Group",
                name_ar="مجموعة عمل حماية البيئة",
                level="national",
                body_type="committee",
                mandate="Mainstream environmental sustainability into all spatial development decisions",
                composition=[
                    "National Center for Environmental Compliance",
                    "National Center for Wildlife",
                    "Ministry of Environment",
                    "NSS Technical Secretariat"
                ],
                key_functions=[
                    "Environmental impact review of NSS projects",
                    "Protected area boundary management",
                    "Climate adaptation integration",
                    "Biodiversity corridor planning"
                ],
                decision_rights=[
                    "Environmental clearance recommendations"
                ],
                meeting_frequency="Monthly",
                reports_to="Inter-Ministerial Coordination Committee",
                secretariat="NSS Technical Secretariat"
            ),
            
            # REGIONAL LEVEL
            GovernanceBody(
                name="Regional Spatial Development Commission (per region)",
                name_ar="هيئة التنمية المكانية الإقليمية",
                level="regional",
                body_type="authority",
                mandate="Translate NSS into regional spatial plans and coordinate implementation within the region",
                composition=[
                    "Regional Governor (Chair)",
                    "Regional Planning Director",
                    "Municipal Representatives",
                    "Private Sector Representatives",
                    "Community Representatives"
                ],
                key_functions=[
                    "Develop regional spatial plans aligned with NSS",
                    "Coordinate municipal plans within region",
                    "Prioritize regional infrastructure investments",
                    "Monitor regional progress against NSS targets",
                    "Stakeholder engagement at regional level"
                ],
                decision_rights=[
                    "Approve municipal spatial plans",
                    "Recommend regional project priorities",
                    "Issue regional development guidelines"
                ],
                meeting_frequency="Monthly",
                reports_to="National Spatial Strategy Authority",
                secretariat="Regional Planning Office"
            ),
            
            GovernanceBody(
                name="Regional Planning Office (per region)",
                name_ar="مكتب التخطيط الإقليمي",
                level="regional",
                body_type="secretariat",
                mandate="Provide technical planning support for regional spatial development",
                composition=[
                    "Regional Planning Director",
                    "Spatial Planners",
                    "GIS Specialists",
                    "Environmental Officers",
                    "Infrastructure Coordinators"
                ],
                key_functions=[
                    "Prepare regional spatial plans",
                    "Coordinate with municipalities",
                    "Manage regional spatial data",
                    "Support project assessment",
                    "Community consultation"
                ],
                decision_rights=[
                    "Technical recommendations",
                    "Data management"
                ],
                meeting_frequency="Weekly",
                reports_to="Regional Spatial Development Commission",
                secretariat=None
            ),
            
            # LOCAL LEVEL
            GovernanceBody(
                name="Municipal Planning Committee (per municipality)",
                name_ar="لجنة التخطيط البلدي",
                level="local",
                body_type="committee",
                mandate="Ensure local plans and permits comply with NSS and regional spatial plans",
                composition=[
                    "Mayor/Municipal Director (Chair)",
                    "Planning Department Head",
                    "Infrastructure Department",
                    "Community Representatives"
                ],
                key_functions=[
                    "Prepare local spatial plans",
                    "Issue development permits",
                    "Enforce zoning regulations",
                    "Local stakeholder engagement",
                    "Monitor local development"
                ],
                decision_rights=[
                    "Local plan adoption (within NSS framework)",
                    "Development permit issuance"
                ],
                meeting_frequency="Bi-weekly",
                reports_to="Regional Spatial Development Commission",
                secretariat="Municipal Planning Department"
            ),
            
            # SPECIAL BODIES
            GovernanceBody(
                name="Giga-Projects Spatial Coordination Board",
                name_ar="مجلس تنسيق المشاريع الكبرى المكاني",
                level="national",
                body_type="committee",
                mandate="Ensure giga-projects (NEOM, Red Sea, Qiddiya, etc.) align with NSS",
                composition=[
                    "Royal Commission Representatives",
                    "PIF Representatives",
                    "NSS Authority",
                    "Relevant Ministries"
                ],
                key_functions=[
                    "Coordinate giga-project spatial impacts",
                    "Resolve conflicts between giga-projects and NSS",
                    "Ensure infrastructure connectivity",
                    "Manage cumulative environmental impacts"
                ],
                decision_rights=[
                    "Recommend modifications for NSS alignment"
                ],
                meeting_frequency="Quarterly",
                reports_to="Council of Economic and Development Affairs",
                secretariat="NSS Technical Secretariat"
            )
        ]
        
        return bodies
    
    def _build_decision_processes(self) -> List[DecisionProcess]:
        """Build decision processes."""
        
        processes = [
            DecisionProcess(
                process_name="Spatial Alignment Assessment",
                description="Assess whether a proposed project aligns with NSS spatial framework",
                trigger="New major project proposal (>SAR 500M or >100ha)",
                steps=[
                    {"step": "1", "action": "Project submits spatial impact assessment form", "actor": "Project Proponent"},
                    {"step": "2", "action": "Technical Secretariat reviews against NSS criteria", "actor": "NSS Technical Secretariat"},
                    {"step": "3", "action": "Sectoral working groups provide input", "actor": "Working Groups"},
                    {"step": "4", "action": "Prepare alignment recommendation", "actor": "NSS Technical Secretariat"},
                    {"step": "5", "action": "Decision by NSSA or escalation", "actor": "NSSA"}
                ],
                decision_authority="National Spatial Strategy Authority",
                timeline_days=45,
                escalation_path="CEDA for strategic projects",
                output="Spatial Alignment Certificate or Conditions"
            ),
            
            DecisionProcess(
                process_name="Regional Plan Approval",
                description="Process for approving regional spatial plans",
                trigger="Regional Spatial Development Commission submits plan",
                steps=[
                    {"step": "1", "action": "Regional Commission submits draft plan", "actor": "Regional Commission"},
                    {"step": "2", "action": "Technical review for NSS compliance", "actor": "NSS Technical Secretariat"},
                    {"step": "3", "action": "Inter-ministerial consultation", "actor": "Coordination Committee"},
                    {"step": "4", "action": "Public consultation (30 days)", "actor": "Regional Commission"},
                    {"step": "5", "action": "Revisions incorporated", "actor": "Regional Commission"},
                    {"step": "6", "action": "NSSA approval", "actor": "NSSA"}
                ],
                decision_authority="National Spatial Strategy Authority",
                timeline_days=180,
                escalation_path="CEDA for significant conflicts",
                output="Approved Regional Spatial Plan"
            ),
            
            DecisionProcess(
                process_name="Inter-Regional Conflict Resolution",
                description="Resolve conflicts between regions on spatial development",
                trigger="Conflict identified by either region or Technical Secretariat",
                steps=[
                    {"step": "1", "action": "Conflict documentation", "actor": "NSS Technical Secretariat"},
                    {"step": "2", "action": "Mediation meeting between regions", "actor": "NSS Technical Secretariat"},
                    {"step": "3", "action": "Technical options analysis", "actor": "NSS Technical Secretariat"},
                    {"step": "4", "action": "Recommended resolution to NSSA", "actor": "NSS Technical Secretariat"},
                    {"step": "5", "action": "NSSA decision", "actor": "NSSA"}
                ],
                decision_authority="National Spatial Strategy Authority",
                timeline_days=60,
                escalation_path="CEDA for politically sensitive issues",
                output="Binding resolution decision"
            ),
            
            DecisionProcess(
                process_name="Sectoral Strategy NSS Integration",
                description="Ensure sectoral strategies align with NSS",
                trigger="New or updated sectoral strategy submitted",
                steps=[
                    {"step": "1", "action": "Ministry submits strategy for NSS review", "actor": "Line Ministry"},
                    {"step": "2", "action": "Spatial consistency analysis", "actor": "NSS Technical Secretariat"},
                    {"step": "3", "action": "Coordination Committee discussion", "actor": "Coordination Committee"},
                    {"step": "4", "action": "Alignment modifications negotiated", "actor": "Ministry + Secretariat"},
                    {"step": "5", "action": "Certification of NSS alignment", "actor": "NSSA"}
                ],
                decision_authority="Inter-Ministerial Coordination Committee",
                timeline_days=90,
                escalation_path="NSSA for unresolved conflicts",
                output="NSS Alignment Certification"
            ),
            
            DecisionProcess(
                process_name="Emergency Spatial Deviation",
                description="Fast-track process for urgent deviations from NSS",
                trigger="Emergency situation requiring immediate action",
                steps=[
                    {"step": "1", "action": "Emergency request with justification", "actor": "Requesting Entity"},
                    {"step": "2", "action": "Rapid assessment (48 hours)", "actor": "NSS Technical Secretariat"},
                    {"step": "3", "action": "NSSA Chair emergency approval", "actor": "NSSA Chair"},
                    {"step": "4", "action": "NSSA ratification (within 30 days)", "actor": "NSSA"}
                ],
                decision_authority="NSSA Chair (emergency) / NSSA (ratification)",
                timeline_days=5,
                escalation_path="Minister/Council for major deviations",
                output="Emergency Deviation Permit"
            ),
            
            DecisionProcess(
                process_name="NSS Quinquennial Review",
                description="Comprehensive review and update of NSS every 5 years",
                trigger="5-year cycle or significant change in circumstances",
                steps=[
                    {"step": "1", "action": "Performance assessment", "actor": "NSS Technical Secretariat"},
                    {"step": "2", "action": "Scenario update and stress testing", "actor": "NSS Technical Secretariat"},
                    {"step": "3", "action": "Stakeholder consultation", "actor": "NSSA"},
                    {"step": "4", "action": "Draft revision preparation", "actor": "NSS Technical Secretariat"},
                    {"step": "5", "action": "Inter-ministerial review", "actor": "Coordination Committee"},
                    {"step": "6", "action": "NSSA approval", "actor": "NSSA"},
                    {"step": "7", "action": "CEDA endorsement", "actor": "CEDA"}
                ],
                decision_authority="CEDA",
                timeline_days=365,
                escalation_path="Council of Ministers for major changes",
                output="Updated National Spatial Strategy"
            )
        ]
        
        return processes
    
    def get_bodies(self) -> List[GovernanceBody]:
        return self.bodies
    
    def get_processes(self) -> List[DecisionProcess]:
        return self.processes
    
    def get_bodies_by_level(self, level: str) -> List[GovernanceBody]:
        return [b for b in self.bodies if b.level == level]


# =============================================================================
# RACI MATRIX BUILDER
# =============================================================================

class RACIMatrixBuilder:
    """
    Builds the Ministry Accountability and Decision Rights Matrix.
    """
    
    def __init__(self):
        """Initialize RACI matrix builder."""
        self.matrix = self._build_raci_matrix()
        logger.info(f"RACI Matrix: {len(self.matrix)} activities")
    
    def _build_raci_matrix(self) -> List[RACIEntry]:
        """Build comprehensive RACI matrix."""
        
        R = ResponsibilityLevel.RESPONSIBLE
        A = ResponsibilityLevel.ACCOUNTABLE
        C = ResponsibilityLevel.CONSULTED
        I = ResponsibilityLevel.INFORMED
        N = ResponsibilityLevel.NOT_INVOLVED
        
        matrix = [
            # STRATEGIC PLANNING
            RACIEntry(
                activity="NSS Vision and Strategy Formulation",
                activity_category="Strategic Planning",
                nss_authority=A,
                momra=C,
                mowe=C,
                mot=C,
                misa=C,
                moi=C,
                tourism=C,
                housing=C,
                regions=C,
                pif=C,
                royal_commission=C
            ),
            RACIEntry(
                activity="Regional Spatial Plan Development",
                activity_category="Strategic Planning",
                nss_authority=A,
                momra=C,
                mowe=C,
                mot=C,
                misa=I,
                moi=I,
                tourism=C,
                housing=C,
                regions=R,
                pif=I,
                royal_commission=C
            ),
            RACIEntry(
                activity="Sectoral Strategy NSS Alignment",
                activity_category="Strategic Planning",
                nss_authority=A,
                momra=R,
                mowe=R,
                mot=R,
                misa=R,
                moi=R,
                tourism=R,
                housing=R,
                regions=C,
                pif=C,
                royal_commission=R
            ),
            RACIEntry(
                activity="Urban Development Guidelines",
                activity_category="Strategic Planning",
                nss_authority=A,
                momra=R,
                mowe=C,
                mot=C,
                misa=I,
                moi=I,
                tourism=C,
                housing=C,
                regions=C,
                pif=I,
                royal_commission=C
            ),
            
            # WATER MANAGEMENT
            RACIEntry(
                activity="Water Allocation Policy",
                activity_category="Water Management",
                nss_authority=C,
                momra=I,
                mowe=A,
                mot=I,
                misa=I,
                moi=C,
                tourism=I,
                housing=C,
                regions=C,
                pif=I,
                royal_commission=C
            ),
            RACIEntry(
                activity="Agricultural Water Transition",
                activity_category="Water Management",
                nss_authority=C,
                momra=I,
                mowe=A,
                mot=I,
                misa=I,
                moi=I,
                tourism=I,
                housing=I,
                regions=R,
                pif=I,
                royal_commission=I
            ),
            RACIEntry(
                activity="Desalination Capacity Planning",
                activity_category="Water Management",
                nss_authority=C,
                momra=I,
                mowe=A,
                mot=I,
                misa=I,
                moi=I,
                tourism=I,
                housing=I,
                regions=C,
                pif=C,
                royal_commission=C
            ),
            
            # INFRASTRUCTURE
            RACIEntry(
                activity="Transport Corridor Development",
                activity_category="Infrastructure",
                nss_authority=C,
                momra=C,
                mowe=I,
                mot=A,
                misa=I,
                moi=C,
                tourism=C,
                housing=I,
                regions=C,
                pif=C,
                royal_commission=C
            ),
            RACIEntry(
                activity="Rail Network Planning",
                activity_category="Infrastructure",
                nss_authority=C,
                momra=I,
                mowe=I,
                mot=A,
                misa=I,
                moi=C,
                tourism=C,
                housing=I,
                regions=C,
                pif=R,
                royal_commission=C
            ),
            RACIEntry(
                activity="Port Development",
                activity_category="Infrastructure",
                nss_authority=C,
                momra=I,
                mowe=I,
                mot=A,
                misa=C,
                moi=C,
                tourism=I,
                housing=I,
                regions=C,
                pif=C,
                royal_commission=C
            ),
            RACIEntry(
                activity="Airport Development",
                activity_category="Infrastructure",
                nss_authority=C,
                momra=I,
                mowe=I,
                mot=A,
                misa=C,
                moi=I,
                tourism=C,
                housing=I,
                regions=C,
                pif=C,
                royal_commission=C
            ),
            RACIEntry(
                activity="Energy Grid Expansion",
                activity_category="Infrastructure",
                nss_authority=C,
                momra=I,
                mowe=I,
                mot=I,
                misa=I,
                moi=C,
                tourism=I,
                housing=I,
                regions=C,
                pif=C,
                royal_commission=C
            ),
            
            # ECONOMIC DEVELOPMENT
            RACIEntry(
                activity="Industrial Zone Designation",
                activity_category="Economic Development",
                nss_authority=C,
                momra=C,
                mowe=C,
                mot=C,
                misa=C,
                moi=A,
                tourism=I,
                housing=I,
                regions=C,
                pif=C,
                royal_commission=C
            ),
            RACIEntry(
                activity="Tourism Zone Development",
                activity_category="Economic Development",
                nss_authority=C,
                momra=C,
                mowe=C,
                mot=C,
                misa=C,
                moi=I,
                tourism=A,
                housing=I,
                regions=C,
                pif=C,
                royal_commission=R
            ),
            RACIEntry(
                activity="Investment Attraction",
                activity_category="Economic Development",
                nss_authority=I,
                momra=I,
                mowe=I,
                mot=I,
                misa=A,
                moi=C,
                tourism=C,
                housing=I,
                regions=C,
                pif=R,
                royal_commission=C
            ),
            RACIEntry(
                activity="Mining Sector Development",
                activity_category="Economic Development",
                nss_authority=C,
                momra=I,
                mowe=C,
                mot=C,
                misa=C,
                moi=A,
                tourism=I,
                housing=I,
                regions=C,
                pif=C,
                royal_commission=I
            ),
            
            # HOUSING & URBAN
            RACIEntry(
                activity="Housing Supply Planning",
                activity_category="Housing & Urban",
                nss_authority=C,
                momra=C,
                mowe=I,
                mot=C,
                misa=I,
                moi=I,
                tourism=I,
                housing=A,
                regions=C,
                pif=C,
                royal_commission=I
            ),
            RACIEntry(
                activity="TOD Development",
                activity_category="Housing & Urban",
                nss_authority=C,
                momra=R,
                mowe=I,
                mot=C,
                misa=I,
                moi=I,
                tourism=I,
                housing=C,
                regions=C,
                pif=C,
                royal_commission=I
            ),
            RACIEntry(
                activity="Urban Regeneration",
                activity_category="Housing & Urban",
                nss_authority=C,
                momra=A,
                mowe=I,
                mot=C,
                misa=I,
                moi=I,
                tourism=C,
                housing=C,
                regions=R,
                pif=C,
                royal_commission=I
            ),
            RACIEntry(
                activity="Green Space Development",
                activity_category="Housing & Urban",
                nss_authority=C,
                momra=A,
                mowe=C,
                mot=I,
                misa=I,
                moi=I,
                tourism=I,
                housing=I,
                regions=R,
                pif=I,
                royal_commission=I
            ),
            
            # ENVIRONMENT
            RACIEntry(
                activity="Protected Area Management",
                activity_category="Environment",
                nss_authority=C,
                momra=I,
                mowe=A,
                mot=I,
                misa=I,
                moi=I,
                tourism=C,
                housing=I,
                regions=C,
                pif=I,
                royal_commission=C
            ),
            RACIEntry(
                activity="Climate Adaptation Planning",
                activity_category="Environment",
                nss_authority=C,
                momra=C,
                mowe=A,
                mot=C,
                misa=I,
                moi=I,
                tourism=C,
                housing=C,
                regions=C,
                pif=I,
                royal_commission=C
            ),
            RACIEntry(
                activity="Coastal Zone Management",
                activity_category="Environment",
                nss_authority=C,
                momra=C,
                mowe=A,
                mot=I,
                misa=I,
                moi=I,
                tourism=C,
                housing=I,
                regions=R,
                pif=I,
                royal_commission=R
            ),
            
            # GIGA-PROJECTS
            RACIEntry(
                activity="NEOM Development",
                activity_category="Giga-Projects",
                nss_authority=C,
                momra=C,
                mowe=C,
                mot=C,
                misa=C,
                moi=C,
                tourism=C,
                housing=C,
                regions=C,
                pif=A,
                royal_commission=R
            ),
            RACIEntry(
                activity="Red Sea Project",
                activity_category="Giga-Projects",
                nss_authority=C,
                momra=C,
                mowe=C,
                mot=C,
                misa=C,
                moi=I,
                tourism=C,
                housing=I,
                regions=C,
                pif=A,
                royal_commission=R
            ),
            RACIEntry(
                activity="AlUla Development",
                activity_category="Giga-Projects",
                nss_authority=C,
                momra=C,
                mowe=C,
                mot=C,
                misa=C,
                moi=I,
                tourism=C,
                housing=I,
                regions=C,
                pif=C,
                royal_commission=A
            ),
            RACIEntry(
                activity="Qiddiya Development",
                activity_category="Giga-Projects",
                nss_authority=C,
                momra=C,
                mowe=C,
                mot=C,
                misa=C,
                moi=I,
                tourism=C,
                housing=I,
                regions=C,
                pif=A,
                royal_commission=R
            ),
            
            # MONITORING & EVALUATION
            RACIEntry(
                activity="NSS Progress Monitoring",
                activity_category="Monitoring & Evaluation",
                nss_authority=A,
                momra=R,
                mowe=R,
                mot=R,
                misa=R,
                moi=R,
                tourism=R,
                housing=R,
                regions=R,
                pif=R,
                royal_commission=R
            ),
            RACIEntry(
                activity="KPI Data Collection",
                activity_category="Monitoring & Evaluation",
                nss_authority=A,
                momra=R,
                mowe=R,
                mot=R,
                misa=R,
                moi=R,
                tourism=R,
                housing=R,
                regions=R,
                pif=R,
                royal_commission=R
            ),
            RACIEntry(
                activity="Spatial Impact Assessment",
                activity_category="Monitoring & Evaluation",
                nss_authority=A,
                momra=C,
                mowe=C,
                mot=C,
                misa=C,
                moi=C,
                tourism=C,
                housing=C,
                regions=C,
                pif=C,
                royal_commission=C
            )
        ]
        
        return matrix
    
    def get_matrix(self) -> List[RACIEntry]:
        return self.matrix
    
    def get_by_category(self, category: str) -> List[RACIEntry]:
        return [e for e in self.matrix if e.activity_category == category]
    
    def get_ministry_responsibilities(self, ministry: str) -> List[Dict[str, Any]]:
        """Get all responsibilities for a specific ministry."""
        attr_map = {
            "NSSA": "nss_authority",
            "MOMRA": "momra",
            "MOWE": "mowe",
            "MOT": "mot",
            "MISA": "misa",
            "MOI": "moi",
            "Tourism": "tourism",
            "Housing": "housing",
            "Regions": "regions",
            "PIF": "pif",
            "Royal_Commission": "royal_commission"
        }
        
        if ministry not in attr_map:
            return []
        
        attr = attr_map[ministry]
        responsibilities = []
        
        for entry in self.matrix:
            level = getattr(entry, attr)
            if level != ResponsibilityLevel.NOT_INVOLVED:
                responsibilities.append({
                    "activity": entry.activity,
                    "category": entry.activity_category,
                    "responsibility": level.value
                })
        
        return responsibilities


# =============================================================================
# KPI FRAMEWORK BUILDER
# =============================================================================

class KPIFrameworkBuilder:
    """
    Builds the monitoring and KPI framework.
    """
    
    def __init__(self):
        """Initialize KPI framework builder."""
        self.kpis = self._build_kpis()
        self.mechanisms = self._build_monitoring_mechanisms()
        logger.info(f"KPI Framework: {len(self.kpis)} KPIs, {len(self.mechanisms)} mechanisms")
    
    def _build_kpis(self) -> List[KPI]:
        """Build comprehensive KPI list."""
        
        kpis = [
            # DEMOGRAPHIC KPIs
            KPI(
                kpi_id="KPI-D01",
                name="Regional Population Balance",
                category="demographic",
                description="Population share in top 3 regions vs target",
                unit="%",
                baseline_2024=64.0,
                target_2030=62.0,
                target_2040=58.0,
                target_2050=55.0,
                data_source="General Authority for Statistics",
                responsible_entity="NSS Authority",
                reporting_frequency="Annual",
                calculation_method="(Pop in Riyadh+Makkah+Eastern) / Total Pop * 100"
            ),
            KPI(
                kpi_id="KPI-D02",
                name="Urban Primacy Ratio",
                category="demographic",
                description="Riyadh population vs second largest city",
                unit="ratio",
                baseline_2024=1.85,
                target_2030=1.75,
                target_2040=1.65,
                target_2050=1.50,
                data_source="General Authority for Statistics",
                responsible_entity="NSS Authority",
                reporting_frequency="Annual",
                calculation_method="Riyadh Pop / Jeddah Pop"
            ),
            KPI(
                kpi_id="KPI-D03",
                name="Migration to Secondary Cities",
                category="demographic",
                description="Net migration to tier-2 cities as % of total migration",
                unit="%",
                baseline_2024=15.0,
                target_2030=25.0,
                target_2040=35.0,
                target_2050=40.0,
                data_source="General Authority for Statistics",
                responsible_entity="NSS Authority",
                reporting_frequency="Annual",
                calculation_method="Net migration to tier-2 / Total internal migration * 100"
            ),
            
            # ECONOMIC KPIs
            KPI(
                kpi_id="KPI-E01",
                name="Regional GDP Distribution",
                category="economic",
                description="GDP share outside top 3 regions",
                unit="%",
                baseline_2024=18.0,
                target_2030=22.0,
                target_2040=28.0,
                target_2050=35.0,
                data_source="General Authority for Statistics",
                responsible_entity="Ministry of Economy and Planning",
                reporting_frequency="Annual",
                calculation_method="(National GDP - Top 3 regions GDP) / National GDP * 100"
            ),
            KPI(
                kpi_id="KPI-E02",
                name="Economic Diversification Index",
                category="economic",
                description="Average regional economic diversification (Herfindahl index)",
                unit="index",
                baseline_2024=0.45,
                target_2030=0.55,
                target_2040=0.65,
                target_2050=0.75,
                data_source="General Authority for Statistics",
                responsible_entity="Ministry of Economy and Planning",
                reporting_frequency="Annual",
                calculation_method="1 - Herfindahl concentration index of regional sectors"
            ),
            KPI(
                kpi_id="KPI-E03",
                name="Corridor GDP Contribution",
                category="economic",
                description="GDP generated along designated corridors",
                unit="SAR Billion",
                baseline_2024=850,
                target_2030=1200,
                target_2040=1800,
                target_2050=2500,
                data_source="Ministry of Economy and Planning",
                responsible_entity="NSS Authority",
                reporting_frequency="Annual",
                calculation_method="Sum of GDP in corridor municipalities"
            ),
            KPI(
                kpi_id="KPI-E04",
                name="Private Sector Employment Share",
                category="economic",
                description="% of employment in private sector by region",
                unit="%",
                baseline_2024=55.0,
                target_2030=62.0,
                target_2040=68.0,
                target_2050=75.0,
                data_source="Ministry of Human Resources",
                responsible_entity="Ministry of Human Resources",
                reporting_frequency="Quarterly",
                calculation_method="Private sector employees / Total employees * 100"
            ),
            KPI(
                kpi_id="KPI-E05",
                name="Tourism Contribution to GDP",
                category="economic",
                description="Tourism sector contribution to national GDP",
                unit="%",
                baseline_2024=5.4,
                target_2030=10.0,
                target_2040=12.0,
                target_2050=15.0,
                data_source="Ministry of Tourism",
                responsible_entity="Ministry of Tourism",
                reporting_frequency="Annual",
                calculation_method="Tourism GDP / Total GDP * 100"
            ),
            
            # ENVIRONMENTAL KPIs
            KPI(
                kpi_id="KPI-V01",
                name="Protected Area Coverage",
                category="environmental",
                description="% of land area in protected status",
                unit="%",
                baseline_2024=4.3,
                target_2030=30.0,
                target_2040=30.0,
                target_2050=30.0,
                data_source="National Center for Wildlife",
                responsible_entity="MOWE",
                reporting_frequency="Annual",
                calculation_method="Protected area / Total land area * 100"
            ),
            KPI(
                kpi_id="KPI-V02",
                name="Per Capita Water Consumption",
                category="environmental",
                description="Daily water consumption per capita",
                unit="liters/day",
                baseline_2024=263,
                target_2030=200,
                target_2040=175,
                target_2050=150,
                data_source="Ministry of Environment",
                responsible_entity="MOWE",
                reporting_frequency="Annual",
                calculation_method="Total water consumption / Population / 365"
            ),
            KPI(
                kpi_id="KPI-V03",
                name="Wastewater Reuse Rate",
                category="environmental",
                description="% of treated wastewater reused",
                unit="%",
                baseline_2024=18.0,
                target_2030=50.0,
                target_2040=80.0,
                target_2050=100.0,
                data_source="Ministry of Environment",
                responsible_entity="MOWE",
                reporting_frequency="Annual",
                calculation_method="Reused wastewater / Treated wastewater * 100"
            ),
            KPI(
                kpi_id="KPI-V04",
                name="Urban Green Space per Capita",
                category="environmental",
                description="Public green space per urban resident",
                unit="sqm",
                baseline_2024=1.2,
                target_2030=5.0,
                target_2040=7.0,
                target_2050=9.0,
                data_source="MOMRA",
                responsible_entity="MOMRA",
                reporting_frequency="Annual",
                calculation_method="Total urban green space / Urban population"
            ),
            KPI(
                kpi_id="KPI-V05",
                name="Renewable Energy Share",
                category="environmental",
                description="Renewable energy as % of electricity generation",
                unit="%",
                baseline_2024=0.6,
                target_2030=30.0,
                target_2040=45.0,
                target_2050=50.0,
                data_source="Ministry of Energy",
                responsible_entity="Ministry of Energy",
                reporting_frequency="Annual",
                calculation_method="Renewable generation / Total generation * 100"
            ),
            KPI(
                kpi_id="KPI-V06",
                name="Groundwater Balance",
                category="environmental",
                description="Ratio of extraction to recharge",
                unit="ratio",
                baseline_2024=2.8,
                target_2030=2.0,
                target_2040=1.5,
                target_2050=1.0,
                data_source="Ministry of Environment",
                responsible_entity="MOWE",
                reporting_frequency="Annual",
                calculation_method="Annual extraction / Annual recharge"
            ),
            
            # INFRASTRUCTURE KPIs
            KPI(
                kpi_id="KPI-I01",
                name="Rail Network Coverage",
                category="infrastructure",
                description="Total operational rail network length",
                unit="km",
                baseline_2024=4500,
                target_2030=6500,
                target_2040=8500,
                target_2050=10000,
                data_source="Saudi Railway Company",
                responsible_entity="Ministry of Transport",
                reporting_frequency="Annual",
                calculation_method="Total operational rail km"
            ),
            KPI(
                kpi_id="KPI-I02",
                name="Road Network Quality",
                category="infrastructure",
                description="% of road network in good/excellent condition",
                unit="%",
                baseline_2024=75.0,
                target_2030=85.0,
                target_2040=90.0,
                target_2050=95.0,
                data_source="Ministry of Transport",
                responsible_entity="Ministry of Transport",
                reporting_frequency="Annual",
                calculation_method="Roads in good condition / Total roads * 100"
            ),
            KPI(
                kpi_id="KPI-I03",
                name="Broadband Coverage",
                category="infrastructure",
                description="% of population with access to high-speed internet",
                unit="%",
                baseline_2024=92.0,
                target_2030=98.0,
                target_2040=99.5,
                target_2050=100.0,
                data_source="Communications and Space Commission",
                responsible_entity="MCIT",
                reporting_frequency="Annual",
                calculation_method="Population with broadband access / Total population * 100"
            ),
            KPI(
                kpi_id="KPI-I04",
                name="Public Transit Coverage",
                category="infrastructure",
                description="% of urban population within 500m of transit stop",
                unit="%",
                baseline_2024=25.0,
                target_2030=50.0,
                target_2040=70.0,
                target_2050=85.0,
                data_source="MOMRA",
                responsible_entity="MOMRA",
                reporting_frequency="Annual",
                calculation_method="Pop within 500m of transit / Total urban pop * 100"
            ),
            KPI(
                kpi_id="KPI-I05",
                name="Regional Airport Connectivity",
                category="infrastructure",
                description="Average daily flights per regional airport",
                unit="flights/day",
                baseline_2024=8.0,
                target_2030=15.0,
                target_2040=25.0,
                target_2050=35.0,
                data_source="GACA",
                responsible_entity="Ministry of Transport",
                reporting_frequency="Quarterly",
                calculation_method="Total regional flights / Number of regional airports"
            ),
            
            # GOVERNANCE KPIs
            KPI(
                kpi_id="KPI-G01",
                name="NSS Alignment Rate",
                category="governance",
                description="% of major projects aligned with NSS",
                unit="%",
                baseline_2024=40.0,
                target_2030=80.0,
                target_2040=95.0,
                target_2050=100.0,
                data_source="NSS Authority",
                responsible_entity="NSS Authority",
                reporting_frequency="Quarterly",
                calculation_method="Aligned projects / Total major projects * 100"
            ),
            KPI(
                kpi_id="KPI-G02",
                name="Regional Plan Coverage",
                category="governance",
                description="% of regions with approved spatial plans",
                unit="%",
                baseline_2024=23.0,
                target_2030=100.0,
                target_2040=100.0,
                target_2050=100.0,
                data_source="NSS Authority",
                responsible_entity="NSS Authority",
                reporting_frequency="Annual",
                calculation_method="Regions with plans / 13 * 100"
            ),
            KPI(
                kpi_id="KPI-G03",
                name="Inter-ministerial Conflict Resolution",
                category="governance",
                description="Average days to resolve spatial conflicts",
                unit="days",
                baseline_2024=180.0,
                target_2030=60.0,
                target_2040=45.0,
                target_2050=30.0,
                data_source="NSS Authority",
                responsible_entity="NSS Authority",
                reporting_frequency="Quarterly",
                calculation_method="Sum of resolution days / Number of conflicts"
            ),
            KPI(
                kpi_id="KPI-G04",
                name="Stakeholder Consultation Participation",
                category="governance",
                description="Participants in NSS consultations per year",
                unit="thousands",
                baseline_2024=5.0,
                target_2030=50.0,
                target_2040=100.0,
                target_2050=150.0,
                data_source="NSS Authority",
                responsible_entity="NSS Authority",
                reporting_frequency="Annual",
                calculation_method="Total consultation participants"
            ),
            
            # QUALITY OF LIFE KPIs
            KPI(
                kpi_id="KPI-Q01",
                name="Housing Affordability Index",
                category="quality_of_life",
                description="% of households able to afford housing",
                unit="%",
                baseline_2024=47.0,
                target_2030=60.0,
                target_2040=65.0,
                target_2050=70.0,
                data_source="Ministry of Housing",
                responsible_entity="Ministry of Housing",
                reporting_frequency="Annual",
                calculation_method="Affordable housing stock / Households requiring housing * 100"
            ),
            KPI(
                kpi_id="KPI-Q02",
                name="Service Accessibility",
                category="quality_of_life",
                description="% of population within 30 min of essential services",
                unit="%",
                baseline_2024=75.0,
                target_2030=85.0,
                target_2040=92.0,
                target_2050=98.0,
                data_source="MOMRA",
                responsible_entity="MOMRA",
                reporting_frequency="Annual",
                calculation_method="Pop within 30 min of services / Total pop * 100"
            ),
            KPI(
                kpi_id="KPI-Q03",
                name="Regional Quality of Life Index",
                category="quality_of_life",
                description="Composite quality of life score by region",
                unit="index",
                baseline_2024=68.0,
                target_2030=75.0,
                target_2040=82.0,
                target_2050=88.0,
                data_source="Multiple sources",
                responsible_entity="NSS Authority",
                reporting_frequency="Annual",
                calculation_method="Weighted average of health, education, services, environment scores"
            )
        ]
        
        return kpis
    
    def _build_monitoring_mechanisms(self) -> List[MonitoringMechanism]:
        """Build monitoring mechanisms."""
        
        mechanisms = [
            MonitoringMechanism(
                mechanism_name="Annual NSS Progress Report",
                purpose="Comprehensive assessment of NSS implementation progress",
                frequency="Annual",
                participants=["NSS Authority", "All ministries", "Regional Commissions"],
                outputs=["Progress report", "KPI dashboard", "Recommendations"],
                review_criteria=[
                    "Achievement against KPI targets",
                    "Investment execution rate",
                    "Regional plan adoption",
                    "Major project alignment"
                ]
            ),
            MonitoringMechanism(
                mechanism_name="Quarterly KPI Dashboard",
                purpose="Track key performance indicators in real-time",
                frequency="Quarterly",
                participants=["NSS Technical Secretariat", "Data providers"],
                outputs=["Interactive dashboard", "Trend analysis", "Alert flags"],
                review_criteria=[
                    "Data quality and timeliness",
                    "Deviation from targets",
                    "Emerging issues"
                ]
            ),
            MonitoringMechanism(
                mechanism_name="Bi-Annual Stakeholder Forum",
                purpose="Engage stakeholders in NSS review and feedback",
                frequency="Bi-annual",
                participants=["All stakeholder groups", "Public", "Private sector"],
                outputs=["Feedback synthesis", "Consultation report", "Action items"],
                review_criteria=[
                    "Stakeholder satisfaction",
                    "Feedback incorporation",
                    "Participation rates"
                ]
            ),
            MonitoringMechanism(
                mechanism_name="Quinquennial Strategic Review",
                purpose="Comprehensive review and update of NSS every 5 years",
                frequency="Every 5 years",
                participants=["NSSA", "CEDA", "All stakeholders"],
                outputs=["Updated NSS", "New targets", "Revised strategies"],
                review_criteria=[
                    "Achievement of phase targets",
                    "Changed circumstances",
                    "Emerging opportunities",
                    "International best practices"
                ]
            ),
            MonitoringMechanism(
                mechanism_name="Monthly Management Dashboard",
                purpose="Operational monitoring for NSS Authority management",
                frequency="Monthly",
                participants=["NSS Authority leadership", "Technical Secretariat"],
                outputs=["Management brief", "Issue log", "Decision items"],
                review_criteria=[
                    "Process efficiency",
                    "Coordination effectiveness",
                    "Resource utilization"
                ]
            ),
            MonitoringMechanism(
                mechanism_name="Regional Progress Reviews",
                purpose="Monitor implementation at regional level",
                frequency="Quarterly",
                participants=["Regional Commissions", "NSS Technical Secretariat"],
                outputs=["Regional progress reports", "Comparison dashboards"],
                review_criteria=[
                    "Regional KPI performance",
                    "Local plan implementation",
                    "Inter-regional coordination"
                ]
            ),
            MonitoringMechanism(
                mechanism_name="Giga-Project Spatial Alignment Review",
                purpose="Ensure giga-projects remain aligned with NSS",
                frequency="Quarterly",
                participants=["Royal Commissions", "PIF", "NSS Authority"],
                outputs=["Alignment status", "Issue identification", "Resolution actions"],
                review_criteria=[
                    "Spatial compliance",
                    "Infrastructure coordination",
                    "Environmental impact management"
                ]
            )
        ]
        
        return mechanisms
    
    def get_kpis(self) -> List[KPI]:
        return self.kpis
    
    def get_kpis_by_category(self, category: str) -> List[KPI]:
        return [k for k in self.kpis if k.category == category]
    
    def get_mechanisms(self) -> List[MonitoringMechanism]:
        return self.mechanisms
    
    def calculate_target_achievement(self, year: int = 2030) -> Dict[str, Any]:
        """Calculate target achievement summary."""
        result = {"year": year, "kpis": []}
        
        target_attr = f"target_{year}"
        
        for kpi in self.kpis:
            target = getattr(kpi, target_attr, None)
            if target:
                improvement = abs(target - kpi.baseline_2024)
                result["kpis"].append({
                    "kpi_id": kpi.kpi_id,
                    "name": kpi.name,
                    "baseline": kpi.baseline_2024,
                    "target": target,
                    "improvement_needed": improvement
                })
        
        return result


# =============================================================================
# WS7 REPORT GENERATOR
# =============================================================================

class WS7ReportGenerator:
    """
    Generates all WS7 deliverables.
    """
    
    def __init__(self, output_dir: str = "02_analytics/ws7_outputs"):
        """Initialize report generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize all components
        self.governance_builder = GovernanceFrameworkBuilder()
        self.raci_builder = RACIMatrixBuilder()
        self.kpi_builder = KPIFrameworkBuilder()
        
        logger.info(f"WS7 Report Generator initialized. Output: {self.output_dir}")
    
    def generate_all_reports(self) -> Dict[str, Any]:
        """Generate all WS7 deliverables."""
        
        logger.info("Generating WS7 deliverables...")
        
        # Get all data
        bodies = self.governance_builder.get_bodies()
        processes = self.governance_builder.get_processes()
        raci = self.raci_builder.get_matrix()
        kpis = self.kpi_builder.get_kpis()
        mechanisms = self.kpi_builder.get_mechanisms()
        
        # Save governance bodies CSV
        bodies_df = pd.DataFrame([{
            'Name': b.name,
            'Level': b.level,
            'Type': b.body_type,
            'Mandate': b.mandate[:100] + '...',
            'Meeting_Frequency': b.meeting_frequency,
            'Reports_To': b.reports_to or 'N/A'
        } for b in bodies])
        bodies_df.to_csv(self.output_dir / "governance_bodies.csv", index=False)
        
        # Save decision processes CSV
        processes_df = pd.DataFrame([{
            'Process': p.process_name,
            'Description': p.description[:80] + '...',
            'Decision_Authority': p.decision_authority,
            'Timeline_Days': p.timeline_days,
            'Escalation': p.escalation_path
        } for p in processes])
        processes_df.to_csv(self.output_dir / "decision_processes.csv", index=False)
        
        # Save RACI matrix CSV
        raci_df = pd.DataFrame([{
            'Activity': r.activity,
            'Category': r.activity_category,
            'NSSA': r.nss_authority.value,
            'MOMRA': r.momra.value,
            'MOWE': r.mowe.value,
            'MOT': r.mot.value,
            'MISA': r.misa.value,
            'MOI': r.moi.value,
            'Tourism': r.tourism.value,
            'Housing': r.housing.value,
            'Regions': r.regions.value,
            'PIF': r.pif.value,
            'Royal_Commission': r.royal_commission.value
        } for r in raci])
        raci_df.to_csv(self.output_dir / "raci_matrix.csv", index=False)
        
        # Save KPIs CSV
        kpis_df = pd.DataFrame([{
            'KPI_ID': k.kpi_id,
            'Name': k.name,
            'Category': k.category,
            'Unit': k.unit,
            'Baseline_2024': k.baseline_2024,
            'Target_2030': k.target_2030,
            'Target_2040': k.target_2040,
            'Target_2050': k.target_2050,
            'Data_Source': k.data_source,
            'Responsible': k.responsible_entity,
            'Frequency': k.reporting_frequency
        } for k in kpis])
        kpis_df.to_csv(self.output_dir / "kpi_framework.csv", index=False)
        
        # Save monitoring mechanisms CSV
        mechanisms_df = pd.DataFrame([{
            'Mechanism': m.mechanism_name,
            'Purpose': m.purpose[:80] + '...',
            'Frequency': m.frequency,
            'Participants': len(m.participants),
            'Outputs': len(m.outputs)
        } for m in mechanisms])
        mechanisms_df.to_csv(self.output_dir / "monitoring_mechanisms.csv", index=False)
        
        # Compile comprehensive report
        report = {
            "metadata": {
                "report_title": "WS7 - NSS Governance and Implementation Framework",
                "generated_date": datetime.now().isoformat(),
                "version": "1.0",
                "author": "NSS X System"
            },
            "section_1_governance_framework": {
                "summary": {
                    "governance_bodies": len(bodies),
                    "national_level": len([b for b in bodies if b.level == 'national']),
                    "regional_level": len([b for b in bodies if b.level == 'regional']),
                    "local_level": len([b for b in bodies if b.level == 'local']),
                    "decision_processes": len(processes)
                },
                "governance_bodies": [self._body_to_dict(b) for b in bodies],
                "decision_processes": [self._process_to_dict(p) for p in processes]
            },
            "section_2_raci_matrix": {
                "summary": {
                    "total_activities": len(raci),
                    "categories": list(set(r.activity_category for r in raci)),
                    "ministries_covered": 11
                },
                "matrix": [self._raci_to_dict(r) for r in raci],
                "ministry_summaries": {
                    "NSSA": self._summarize_ministry(raci, "nss_authority"),
                    "MOMRA": self._summarize_ministry(raci, "momra"),
                    "MOWE": self._summarize_ministry(raci, "mowe"),
                    "MOT": self._summarize_ministry(raci, "mot")
                }
            },
            "section_3_kpi_framework": {
                "summary": {
                    "total_kpis": len(kpis),
                    "categories": {
                        "demographic": len([k for k in kpis if k.category == 'demographic']),
                        "economic": len([k for k in kpis if k.category == 'economic']),
                        "environmental": len([k for k in kpis if k.category == 'environmental']),
                        "infrastructure": len([k for k in kpis if k.category == 'infrastructure']),
                        "governance": len([k for k in kpis if k.category == 'governance']),
                        "quality_of_life": len([k for k in kpis if k.category == 'quality_of_life'])
                    }
                },
                "kpis": [self._kpi_to_dict(k) for k in kpis]
            },
            "section_4_monitoring_system": {
                "summary": {
                    "monitoring_mechanisms": len(mechanisms),
                    "reporting_levels": ["Monthly", "Quarterly", "Bi-annual", "Annual", "Quinquennial"]
                },
                "mechanisms": [self._mechanism_to_dict(m) for m in mechanisms],
                "data_management": {
                    "platform": "NSS Digital Platform",
                    "data_sources": list(set(k.data_source for k in kpis)),
                    "integration": "API connections to ministry systems",
                    "visualization": "Interactive dashboards with drill-down",
                    "access_levels": ["Public dashboard", "Ministry level", "NSSA management", "Executive summary"]
                }
            },
            "appendices": {
                "output_files": [
                    "WS7_GOVERNANCE_REPORT.json",
                    "WS7_GOVERNANCE_REPORT.md",
                    "governance_bodies.csv",
                    "decision_processes.csv",
                    "raci_matrix.csv",
                    "kpi_framework.csv",
                    "monitoring_mechanisms.csv"
                ]
            }
        }
        
        # Save JSON report
        report_path = self.output_dir / "WS7_GOVERNANCE_REPORT.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        logger.success(f"WS7 Report saved to {report_path}")
        
        # Generate markdown report
        self._generate_markdown_report(report)
        
        return report
    
    def _body_to_dict(self, body: GovernanceBody) -> Dict:
        return {
            "name": body.name,
            "name_ar": body.name_ar,
            "level": body.level,
            "type": body.body_type,
            "mandate": body.mandate,
            "composition": body.composition,
            "functions": body.key_functions,
            "decision_rights": body.decision_rights,
            "meeting_frequency": body.meeting_frequency,
            "reports_to": body.reports_to,
            "secretariat": body.secretariat
        }
    
    def _process_to_dict(self, process: DecisionProcess) -> Dict:
        return {
            "name": process.process_name,
            "description": process.description,
            "trigger": process.trigger,
            "steps": process.steps,
            "decision_authority": process.decision_authority,
            "timeline_days": process.timeline_days,
            "escalation": process.escalation_path,
            "output": process.output
        }
    
    def _raci_to_dict(self, raci: RACIEntry) -> Dict:
        return {
            "activity": raci.activity,
            "category": raci.activity_category,
            "nss_authority": raci.nss_authority.value,
            "momra": raci.momra.value,
            "mowe": raci.mowe.value,
            "mot": raci.mot.value,
            "misa": raci.misa.value,
            "moi": raci.moi.value,
            "tourism": raci.tourism.value,
            "housing": raci.housing.value,
            "regions": raci.regions.value,
            "pif": raci.pif.value,
            "royal_commission": raci.royal_commission.value
        }
    
    def _kpi_to_dict(self, kpi: KPI) -> Dict:
        return {
            "id": kpi.kpi_id,
            "name": kpi.name,
            "category": kpi.category,
            "description": kpi.description,
            "unit": kpi.unit,
            "baseline_2024": kpi.baseline_2024,
            "target_2030": kpi.target_2030,
            "target_2040": kpi.target_2040,
            "target_2050": kpi.target_2050,
            "data_source": kpi.data_source,
            "responsible": kpi.responsible_entity,
            "frequency": kpi.reporting_frequency,
            "calculation": kpi.calculation_method
        }
    
    def _mechanism_to_dict(self, mech: MonitoringMechanism) -> Dict:
        return {
            "name": mech.mechanism_name,
            "purpose": mech.purpose,
            "frequency": mech.frequency,
            "participants": mech.participants,
            "outputs": mech.outputs,
            "criteria": mech.review_criteria
        }
    
    def _summarize_ministry(self, raci: List[RACIEntry], attr: str) -> Dict:
        """Summarize responsibilities for a ministry."""
        accountable = sum(1 for r in raci if getattr(r, attr) == ResponsibilityLevel.ACCOUNTABLE)
        responsible = sum(1 for r in raci if getattr(r, attr) == ResponsibilityLevel.RESPONSIBLE)
        consulted = sum(1 for r in raci if getattr(r, attr) == ResponsibilityLevel.CONSULTED)
        informed = sum(1 for r in raci if getattr(r, attr) == ResponsibilityLevel.INFORMED)
        
        return {
            "accountable_count": accountable,
            "responsible_count": responsible,
            "consulted_count": consulted,
            "informed_count": informed
        }
    
    def _generate_markdown_report(self, report: Dict):
        """Generate markdown version."""
        
        md_content = f"""# NSS Governance and Implementation Framework

**Generated:** {report['metadata']['generated_date']}
**Version:** {report['metadata']['version']}

---

## Executive Summary

This document defines the governance framework for implementing Saudi Arabia's National Spatial Strategy (NSS). It establishes:
- **{report['section_1_governance_framework']['summary']['governance_bodies']}** governance bodies across national, regional, and local levels
- **{report['section_1_governance_framework']['summary']['decision_processes']}** key decision processes
- **{report['section_2_raci_matrix']['summary']['total_activities']}** activities with clear accountability (RACI matrix)
- **{report['section_3_kpi_framework']['summary']['total_kpis']}** key performance indicators
- **{report['section_4_monitoring_system']['summary']['monitoring_mechanisms']}** monitoring mechanisms

---

## Section 1: Governance Structure

### Governance Bodies by Level

| Level | Bodies |
|-------|--------|
| National | {report['section_1_governance_framework']['summary']['national_level']} |
| Regional | {report['section_1_governance_framework']['summary']['regional_level']} |
| Local | {report['section_1_governance_framework']['summary']['local_level']} |

### Key Governance Bodies

| Body | Level | Type | Reports To |
|------|-------|------|------------|
"""
        for body in report['section_1_governance_framework']['governance_bodies'][:8]:
            md_content += f"| {body['name'][:40]}... | {body['level']} | {body['type']} | {body.get('reports_to', 'N/A')[:25] if body.get('reports_to') else 'N/A'} |\n"
        
        md_content += """
### Decision Processes

| Process | Authority | Timeline | Escalation |
|---------|-----------|----------|------------|
"""
        for process in report['section_1_governance_framework']['decision_processes']:
            md_content += f"| {process['name'][:30]} | {process['decision_authority'][:25]} | {process['timeline_days']} days | {process['escalation'][:20]}... |\n"
        
        md_content += f"""
---

## Section 2: RACI Matrix

### Summary
- **Total Activities:** {report['section_2_raci_matrix']['summary']['total_activities']}
- **Ministries/Entities:** {report['section_2_raci_matrix']['summary']['ministries_covered']}
- **Categories:** {', '.join(report['section_2_raci_matrix']['summary']['categories'])}

### Ministry Responsibility Summary

| Ministry | Accountable (A) | Responsible (R) | Consulted (C) | Informed (I) |
|----------|----------------|-----------------|---------------|--------------|
"""
        for ministry, summary in report['section_2_raci_matrix']['ministry_summaries'].items():
            md_content += f"| {ministry} | {summary['accountable_count']} | {summary['responsible_count']} | {summary['consulted_count']} | {summary['informed_count']} |\n"
        
        md_content += """
### RACI Legend
- **R** (Responsible): Does the work
- **A** (Accountable): Final decision maker  
- **C** (Consulted): Input provider
- **I** (Informed): Kept informed

---

## Section 3: KPI Framework

### Summary by Category

| Category | KPIs |
|----------|------|
"""
        for cat, count in report['section_3_kpi_framework']['summary']['categories'].items():
            md_content += f"| {cat.replace('_', ' ').title()} | {count} |\n"
        
        md_content += """
### Key Performance Indicators

| ID | KPI | Unit | Baseline | Target 2030 | Target 2050 |
|----|-----|------|----------|-------------|-------------|
"""
        for kpi in report['section_3_kpi_framework']['kpis'][:15]:
            md_content += f"| {kpi['id']} | {kpi['name'][:30]}... | {kpi['unit']} | {kpi['baseline_2024']} | {kpi['target_2030']} | {kpi['target_2050']} |\n"
        
        md_content += """
---

## Section 4: Monitoring System

### Monitoring Mechanisms

| Mechanism | Frequency | Purpose |
|-----------|-----------|---------|
"""
        for mech in report['section_4_monitoring_system']['mechanisms']:
            md_content += f"| {mech['name']} | {mech['frequency']} | {mech['purpose'][:50]}... |\n"
        
        md_content += f"""
### Data Management

- **Platform:** {report['section_4_monitoring_system']['data_management']['platform']}
- **Data Sources:** {len(report['section_4_monitoring_system']['data_management']['data_sources'])} unique sources
- **Visualization:** {report['section_4_monitoring_system']['data_management']['visualization']}

### Access Levels
"""
        for level in report['section_4_monitoring_system']['data_management']['access_levels']:
            md_content += f"- {level}\n"
        
        md_content += """
---

## Output Files
"""
        for f in report['appendices']['output_files']:
            md_content += f"- `{f}`\n"
        
        # Save markdown
        md_path = self.output_dir / "WS7_GOVERNANCE_REPORT.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.success(f"Markdown report saved to {md_path}")


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

def generate_ws7_deliverables(output_dir: str = "02_analytics/ws7_outputs") -> Dict[str, Any]:
    """Generate all WS7 deliverables."""
    generator = WS7ReportGenerator(output_dir)
    return generator.generate_all_reports()


if __name__ == "__main__":
    print("=" * 60)
    print("NSS X - WS7 Governance Framework Generator")
    print("=" * 60)
    
    report = generate_ws7_deliverables()
    
    print("\n✅ WS7 Deliverables Generated:")
    print(f"   📄 WS7_GOVERNANCE_REPORT.json")
    print(f"   📄 WS7_GOVERNANCE_REPORT.md")
    print(f"   📄 governance_bodies.csv")
    print(f"   📄 decision_processes.csv")
    print(f"   📄 raci_matrix.csv")
    print(f"   📄 kpi_framework.csv")
    print(f"   📄 monitoring_mechanisms.csv")
    
    print(f"\n📊 Governance Framework:")
    print(f"   Governance Bodies: {report['section_1_governance_framework']['summary']['governance_bodies']}")
    print(f"   Decision Processes: {report['section_1_governance_framework']['summary']['decision_processes']}")
    print(f"   RACI Activities: {report['section_2_raci_matrix']['summary']['total_activities']}")
    print(f"   KPIs: {report['section_3_kpi_framework']['summary']['total_kpis']}")
    
    print("\n✅ WS7 Complete!")
