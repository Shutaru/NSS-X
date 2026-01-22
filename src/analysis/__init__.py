"""
NSS X - Analysis Module
Workstream analysis modules for the National Spatial Strategy.
"""

from .ws2_retrospective import RetrospectiveAnalyzer, run_retrospective_analysis
from .ws2_comprehensive import (
    NSS2001Reviewer,
    NSS2030DraftReviewer,
    ContinuityChangeMatrix,
    WS2ReportGenerator,
    generate_ws2_deliverables
)
from .ws3_benchmarking import (
    InternationalBenchmarks,
    MethodologyMatrix,
    CountryXFitDesignPrinciples,
    WS3ReportGenerator,
    generate_ws3_deliverables
)
from .ws4_sectoral import SectoralAnalyzer, run_sectoral_analysis
from .ws5_scenarios import ScenarioModeler, run_scenario_analysis

__all__ = [
    # WS2 - Retrospective Analysis
    'RetrospectiveAnalyzer',
    'run_retrospective_analysis',
    'NSS2001Reviewer',
    'NSS2030DraftReviewer',
    'ContinuityChangeMatrix',
    'WS2ReportGenerator',
    'generate_ws2_deliverables',
    
    # WS3 - International Benchmarking
    'InternationalBenchmarks',
    'MethodologyMatrix',
    'CountryXFitDesignPrinciples',
    'WS3ReportGenerator',
    'generate_ws3_deliverables',
    
    # WS4 - Sectoral Analysis
    'SectoralAnalyzer',
    'run_sectoral_analysis',
    
    # WS5 - Scenario Modeling
    'ScenarioModeler',
    'run_scenario_analysis'
]
