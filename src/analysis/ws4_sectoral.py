"""
NSS X - WS4: Sectoral Analysis and Land Use Conflicts
Análise setorial e matriz de conflitos/sinergias.
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
from loguru import logger


class ConflictLevel(Enum):
    """Level of conflict between land uses."""
    HIGH_CONFLICT = -2
    MODERATE_CONFLICT = -1
    NEUTRAL = 0
    MODERATE_SYNERGY = 1
    HIGH_SYNERGY = 2


@dataclass
class SectorProfile:
    """Profile of an economic/development sector."""
    name: str
    name_ar: str
    gdp_contribution_pct: float
    employment_share_pct: float
    growth_rate_pct: float
    vision2030_priority: bool
    land_requirements: List[str]
    water_intensity: str  # low, medium, high
    key_regions: List[str]


@dataclass 
class ConflictAssessment:
    """Assessment of conflict between two sectors/land uses."""
    sector1: str
    sector2: str
    conflict_level: ConflictLevel
    conflict_type: str
    description: str
    mitigation_strategies: List[str]


class SectoralAnalyzer:
    """
    WS4 - Sectoral Analysis Module
    Analyzes sectors and identifies conflicts/synergies in land use.
    """
    
    def __init__(self):
        """Initialize sectoral analyzer."""
        self._load_sector_data()
        self._build_conflict_matrix()
        logger.info("WS4 Sectoral Analyzer initialized")
    
    def _load_sector_data(self):
        """Load sector profiles for KSA economy."""
        
        self.sectors = {
            "oil_gas": SectorProfile(
                name="Oil & Gas",
                name_ar="النفط والغاز",
                gdp_contribution_pct=38.0,
                employment_share_pct=3.5,
                growth_rate_pct=2.5,
                vision2030_priority=False,
                land_requirements=["industrial_zones", "coastal_terminals", "pipeline_corridors"],
                water_intensity="high",
                key_regions=["Eastern Province", "Riyadh"]
            ),
            "manufacturing": SectorProfile(
                name="Manufacturing",
                name_ar="الصناعة التحويلية",
                gdp_contribution_pct=13.0,
                employment_share_pct=8.5,
                growth_rate_pct=5.2,
                vision2030_priority=True,
                land_requirements=["industrial_zones", "logistics_parks", "utilities"],
                water_intensity="high",
                key_regions=["Riyadh", "Eastern Province", "Makkah"]
            ),
            "tourism": SectorProfile(
                name="Tourism & Entertainment",
                name_ar="السياحة والترفيه",
                gdp_contribution_pct=5.0,
                employment_share_pct=6.0,
                growth_rate_pct=15.0,
                vision2030_priority=True,
                land_requirements=["coastal_zones", "heritage_sites", "entertainment_districts"],
                water_intensity="medium",
                key_regions=["Makkah", "Madinah", "Riyadh", "Tabuk", "Asir"]
            ),
            "real_estate": SectorProfile(
                name="Real Estate & Construction",
                name_ar="العقارات والإنشاءات",
                gdp_contribution_pct=7.5,
                employment_share_pct=15.0,
                growth_rate_pct=8.0,
                vision2030_priority=True,
                land_requirements=["residential_zones", "commercial_zones", "mixed_use"],
                water_intensity="medium",
                key_regions=["Riyadh", "Makkah", "Eastern Province"]
            ),
            "agriculture": SectorProfile(
                name="Agriculture",
                name_ar="الزراعة",
                gdp_contribution_pct=2.5,
                employment_share_pct=6.5,
                growth_rate_pct=3.0,
                vision2030_priority=True,
                land_requirements=["agricultural_land", "water_sources", "rural_zones"],
                water_intensity="high",
                key_regions=["Al-Qassim", "Riyadh", "Hail", "Al-Jouf"]
            ),
            "mining": SectorProfile(
                name="Mining",
                name_ar="التعدين",
                gdp_contribution_pct=3.5,
                employment_share_pct=1.5,
                growth_rate_pct=12.0,
                vision2030_priority=True,
                land_requirements=["mining_zones", "processing_plants", "transport_corridors"],
                water_intensity="medium",
                key_regions=["Northern Borders", "Madinah", "Tabuk"]
            ),
            "logistics": SectorProfile(
                name="Logistics & Transport",
                name_ar="اللوجستيات والنقل",
                gdp_contribution_pct=6.0,
                employment_share_pct=7.0,
                growth_rate_pct=9.0,
                vision2030_priority=True,
                land_requirements=["ports", "airports", "logistics_parks", "transport_corridors"],
                water_intensity="low",
                key_regions=["Riyadh", "Eastern Province", "Makkah"]
            ),
            "technology": SectorProfile(
                name="Technology & Digital",
                name_ar="التقنية والرقمنة",
                gdp_contribution_pct=4.0,
                employment_share_pct=3.0,
                growth_rate_pct=18.0,
                vision2030_priority=True,
                land_requirements=["tech_parks", "data_centers", "commercial_zones"],
                water_intensity="low",
                key_regions=["Riyadh", "NEOM"]
            ),
            "renewable_energy": SectorProfile(
                name="Renewable Energy",
                name_ar="الطاقة المتجددة",
                gdp_contribution_pct=1.0,
                employment_share_pct=0.5,
                growth_rate_pct=25.0,
                vision2030_priority=True,
                land_requirements=["solar_farms", "wind_farms", "transmission_corridors"],
                water_intensity="low",
                key_regions=["Tabuk", "Al-Jouf", "Northern Borders", "NEOM"]
            ),
            "environmental_protection": SectorProfile(
                name="Environmental Protection",
                name_ar="حماية البيئة",
                gdp_contribution_pct=0.5,
                employment_share_pct=0.5,
                growth_rate_pct=20.0,
                vision2030_priority=True,
                land_requirements=["protected_areas", "marine_reserves", "green_corridors"],
                water_intensity="low",
                key_regions=["All regions"]
            )
        }
    
    def _build_conflict_matrix(self):
        """Build conflict/synergy matrix between land uses."""
        
        # Define land use types
        land_uses = [
            "residential",
            "industrial",
            "agricultural",
            "tourism",
            "environmental_protection",
            "mining",
            "infrastructure",
            "renewable_energy"
        ]
        
        # Conflict matrix: positive = synergy, negative = conflict
        # Based on typical land use planning principles and KSA context
        matrix = pd.DataFrame(
            index=land_uses,
            columns=land_uses,
            data=0
        )
        
        # Define conflicts (negative values)
        conflicts = [
            ("residential", "industrial", -2, "Air/noise pollution, traffic"),
            ("residential", "mining", -2, "Environmental degradation"),
            ("agricultural", "industrial", -1, "Water competition, pollution"),
            ("agricultural", "mining", -2, "Land degradation, water depletion"),
            ("tourism", "industrial", -1, "Visual/environmental impact"),
            ("tourism", "mining", -2, "Landscape degradation"),
            ("environmental_protection", "industrial", -2, "Habitat destruction"),
            ("environmental_protection", "mining", -2, "Ecosystem disruption"),
            ("environmental_protection", "agricultural", -1, "Water use, land conversion"),
        ]
        
        # Define synergies (positive values)
        synergies = [
            ("residential", "infrastructure", 2, "Accessibility, services"),
            ("residential", "tourism", 1, "Employment, services"),
            ("tourism", "environmental_protection", 2, "Eco-tourism potential"),
            ("tourism", "infrastructure", 2, "Accessibility"),
            ("renewable_energy", "environmental_protection", 1, "Clean energy"),
            ("renewable_energy", "agricultural", 1, "Agrivoltaics potential"),
            ("infrastructure", "industrial", 2, "Logistics efficiency"),
            ("infrastructure", "mining", 1, "Resource transport"),
        ]
        
        # Populate matrix
        for use1, use2, value, _ in conflicts + synergies:
            matrix.loc[use1, use2] = value
            matrix.loc[use2, use1] = value
        
        self.conflict_matrix = matrix
        self.conflict_details = {
            **{(c[0], c[1]): c for c in conflicts},
            **{(s[0], s[1]): s for s in synergies}
        }
    
    def get_sector_profile(self, sector_key: str) -> Optional[SectorProfile]:
        """Get profile for a specific sector."""
        return self.sectors.get(sector_key)
    
    def get_all_sectors(self) -> Dict[str, SectorProfile]:
        """Get all sector profiles."""
        return self.sectors
    
    def get_conflict_matrix(self) -> pd.DataFrame:
        """Get the full conflict/synergy matrix."""
        return self.conflict_matrix
    
    def assess_conflict(self, use1: str, use2: str) -> ConflictAssessment:
        """Assess conflict between two land uses."""
        if use1 == use2:
            return ConflictAssessment(
                sector1=use1,
                sector2=use2,
                conflict_level=ConflictLevel.NEUTRAL,
                conflict_type="Same use",
                description="Same land use type",
                mitigation_strategies=[]
            )
        
        value = self.conflict_matrix.loc[use1, use2]
        
        # Determine conflict level
        if value <= -2:
            level = ConflictLevel.HIGH_CONFLICT
        elif value == -1:
            level = ConflictLevel.MODERATE_CONFLICT
        elif value == 0:
            level = ConflictLevel.NEUTRAL
        elif value == 1:
            level = ConflictLevel.MODERATE_SYNERGY
        else:
            level = ConflictLevel.HIGH_SYNERGY
        
        # Get details
        key = (use1, use2) if (use1, use2) in self.conflict_details else (use2, use1)
        details = self.conflict_details.get(key, (use1, use2, 0, "No specific interaction"))
        
        # Generate mitigation strategies
        mitigation = self._generate_mitigation(use1, use2, level)
        
        return ConflictAssessment(
            sector1=use1,
            sector2=use2,
            conflict_level=level,
            conflict_type="Conflict" if value < 0 else "Synergy" if value > 0 else "Neutral",
            description=details[3],
            mitigation_strategies=mitigation
        )
    
    def _generate_mitigation(self, use1: str, use2: str, level: ConflictLevel) -> List[str]:
        """Generate mitigation strategies for conflicts."""
        if level in [ConflictLevel.NEUTRAL, ConflictLevel.MODERATE_SYNERGY, ConflictLevel.HIGH_SYNERGY]:
            return []
        
        strategies = []
        
        # Generic strategies
        strategies.append("Establish buffer zones between incompatible uses")
        strategies.append("Implement environmental impact assessments (EIA)")
        
        # Specific strategies based on conflict type
        if "industrial" in [use1, use2] and "residential" in [use1, use2]:
            strategies.extend([
                "Relocate heavy industries to designated industrial cities",
                "Implement strict air quality monitoring",
                "Establish green buffer corridors",
                "Enforce noise regulations"
            ])
        
        if "mining" in [use1, use2]:
            strategies.extend([
                "Require rehabilitation bonds for mining operations",
                "Implement progressive land reclamation",
                "Establish exclusion zones around sensitive areas"
            ])
        
        if "agricultural" in [use1, use2]:
            strategies.extend([
                "Protect prime agricultural land through zoning",
                "Implement water allocation quotas",
                "Promote water-efficient irrigation technologies"
            ])
        
        if "environmental_protection" in [use1, use2]:
            strategies.extend([
                "Expand protected area network",
                "Implement wildlife corridors",
                "Require biodiversity offsets for development"
            ])
        
        return strategies[:5]  # Limit to 5 strategies
    
    def identify_regional_conflicts(self, region: str) -> List[ConflictAssessment]:
        """Identify potential conflicts in a specific region."""
        
        # Get sectors active in the region
        active_sectors = [
            s for s in self.sectors.values()
            if region in s.key_regions or s.key_regions == ["All regions"]
        ]
        
        conflicts = []
        land_uses = set()
        
        # Map sectors to land uses
        sector_to_landuse = {
            "oil_gas": "industrial",
            "manufacturing": "industrial",
            "tourism": "tourism",
            "real_estate": "residential",
            "agriculture": "agricultural",
            "mining": "mining",
            "logistics": "infrastructure",
            "technology": "industrial",
            "renewable_energy": "renewable_energy",
            "environmental_protection": "environmental_protection"
        }
        
        for sector in active_sectors:
            for key, s in self.sectors.items():
                if s.name == sector.name:
                    land_uses.add(sector_to_landuse.get(key, "industrial"))
        
        # Check all pairs for conflicts
        land_uses_list = list(land_uses)
        for i, use1 in enumerate(land_uses_list):
            for use2 in land_uses_list[i+1:]:
                assessment = self.assess_conflict(use1, use2)
                if assessment.conflict_level in [ConflictLevel.HIGH_CONFLICT, ConflictLevel.MODERATE_CONFLICT]:
                    conflicts.append(assessment)
        
        return conflicts
    
    def generate_sectoral_report(self) -> Dict:
        """Generate comprehensive sectoral analysis report."""
        
        # Vision 2030 priority sectors
        v2030_sectors = [s for s in self.sectors.values() if s.vision2030_priority]
        
        # High growth sectors
        high_growth = sorted(
            self.sectors.values(),
            key=lambda x: x.growth_rate_pct,
            reverse=True
        )[:5]
        
        # Water-intensive sectors
        water_intensive = [s for s in self.sectors.values() if s.water_intensity == "high"]
        
        # Count conflicts in matrix
        high_conflicts = (self.conflict_matrix <= -2).sum().sum() // 2
        moderate_conflicts = (self.conflict_matrix == -1).sum().sum() // 2
        synergies = (self.conflict_matrix >= 1).sum().sum() // 2
        
        report = {
            "title": "WS4 - Sectoral Analysis: Saudi Arabia",
            "sectors_analyzed": len(self.sectors),
            "vision2030_priorities": {
                "count": len(v2030_sectors),
                "sectors": [s.name for s in v2030_sectors]
            },
            "high_growth_sectors": [
                {"name": s.name, "growth_rate": s.growth_rate_pct}
                for s in high_growth
            ],
            "water_critical_sectors": [
                {"name": s.name, "intensity": s.water_intensity}
                for s in water_intensive
            ],
            "conflict_summary": {
                "high_conflicts": high_conflicts,
                "moderate_conflicts": moderate_conflicts,
                "synergies_identified": synergies,
                "key_conflicts": [
                    "Industrial vs Residential (pollution, noise)",
                    "Mining vs Environmental Protection (habitat loss)",
                    "Agriculture vs Mining (water competition)"
                ],
                "key_synergies": [
                    "Tourism + Environmental Protection (eco-tourism)",
                    "Infrastructure + Industrial (logistics)",
                    "Renewable Energy + Agriculture (agrivoltaics)"
                ]
            },
            "regional_hotspots": {
                "Riyadh": "Industrial-residential conflicts, water stress",
                "Eastern Province": "Oil industry vs environmental protection",
                "Tabuk/NEOM": "Tourism vs renewable energy land competition",
                "Al-Qassim": "Agricultural water depletion"
            },
            "recommendations": [
                "Establish integrated spatial planning framework",
                "Create sector-specific land use guidelines",
                "Implement water budgeting by sector",
                "Develop buffer zone standards",
                "Create economic incentives for compatible co-location"
            ]
        }
        
        return report


# Convenience function
def run_sectoral_analysis() -> Dict:
    """Run complete WS4 sectoral analysis."""
    analyzer = SectoralAnalyzer()
    return analyzer.generate_sectoral_report()
