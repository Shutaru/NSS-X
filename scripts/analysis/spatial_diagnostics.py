"""
NSS X - Spatial Analysis Core Module
Core spatial analysis functions for NSS diagnostics.
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from loguru import logger


@dataclass
class AccessibilityResult:
    """Result of accessibility analysis."""
    origin_id: int
    destination_type: str
    travel_time_minutes: float
    distance_km: float
    nearest_facility_id: Optional[int] = None


@dataclass
class HierarchyResult:
    """Result of settlement hierarchy analysis."""
    settlement_id: int
    settlement_name: str
    population: int
    rank: int
    hierarchy_class: str
    primacy_contribution: float


class SpatialDiagnostics:
    """
    Core spatial analysis engine for NSS diagnostics.
    Provides methods for spatial analysis, hierarchy analysis, and accessibility calculations.
    """
    
    def __init__(self, spatial_units: gpd.GeoDataFrame, settlements: gpd.GeoDataFrame):
        """
        Initialize diagnostics engine.
        
        Args:
            spatial_units: GeoDataFrame of administrative units
            settlements: GeoDataFrame of settlement points
        """
        self.spatial_units = spatial_units
        self.settlements = settlements
        self._validate_inputs()
    
    def _validate_inputs(self):
        """Validate input data."""
        required_settlement_cols = ['id', 'name_en', 'population']
        missing = [c for c in required_settlement_cols if c not in self.settlements.columns]
        if missing:
            raise ValueError(f"Settlements missing required columns: {missing}")
    
    def calculate_primacy_index(self) -> Tuple[float, pd.DataFrame]:
        """
        Calculate urban primacy index.
        Primacy Index = Population of largest city / Sum of next N cities
        
        Returns:
            Tuple of (primacy_index, city_ranking_dataframe)
        """
        sorted_settlements = self.settlements.sort_values('population', ascending=False)
        top_cities = sorted_settlements.head(10).copy()
        
        if len(top_cities) < 2:
            return 0.0, top_cities
        
        largest_pop = top_cities['population'].iloc[0]
        next_three_sum = top_cities['population'].iloc[1:4].sum()
        
        primacy_index = largest_pop / next_three_sum if next_three_sum > 0 else float('inf')
        
        top_cities['rank'] = range(1, len(top_cities) + 1)
        top_cities['cumulative_share'] = top_cities['population'].cumsum() / top_cities['population'].sum()
        
        logger.info(f"Urban Primacy Index: {primacy_index:.2f}")
        
        return primacy_index, top_cities
    
    def settlement_hierarchy_analysis(self, 
                                       class_thresholds: Optional[Dict[str, int]] = None) -> gpd.GeoDataFrame:
        """
        Classify settlements into hierarchy classes based on population.
        
        Args:
            class_thresholds: Dictionary of {class_name: min_population}
                Default: Metropolis (1M+), Large City (500K+), Medium City (100K+), 
                         Small City (50K+), Town (10K+), Village (<10K)
        
        Returns:
            GeoDataFrame with hierarchy classification
        """
        if class_thresholds is None:
            class_thresholds = {
                'Metropolis': 1000000,
                'Large City': 500000,
                'Medium City': 100000,
                'Small City': 50000,
                'Town': 10000,
                'Village': 0
            }
        
        result = self.settlements.copy()
        
        def classify(pop):
            for class_name, threshold in sorted(class_thresholds.items(), 
                                                 key=lambda x: x[1], reverse=True):
                if pop >= threshold:
                    return class_name
            return 'Village'
        
        result['hierarchy_class'] = result['population'].apply(classify)
        result['rank'] = result['population'].rank(ascending=False, method='first').astype(int)
        
        # Summary statistics
        class_counts = result['hierarchy_class'].value_counts()
        logger.info("Settlement Hierarchy:")
        for cls, count in class_counts.items():
            logger.info(f"  {cls}: {count}")
        
        return result
    
    def calculate_concentration_index(self, 
                                       value_column: str = 'population',
                                       spatial_unit_column: str = 'region_id') -> float:
        """
        Calculate spatial concentration index (Herfindahl-Hirschman Index).
        
        HHI ranges from 1/N (perfect equality) to 1 (complete concentration)
        
        Args:
            value_column: Column containing values to measure concentration
            spatial_unit_column: Column identifying spatial units
        
        Returns:
            HHI value
        """
        # Aggregate by spatial unit
        unit_totals = self.settlements.groupby(spatial_unit_column)[value_column].sum()
        total = unit_totals.sum()
        
        if total == 0:
            return 0.0
        
        # Calculate shares and HHI
        shares = unit_totals / total
        hhi = (shares ** 2).sum()
        
        # Normalized HHI (0 to 1 scale)
        n = len(unit_totals)
        if n > 1:
            normalized_hhi = (hhi - 1/n) / (1 - 1/n)
        else:
            normalized_hhi = 1.0
        
        logger.info(f"Concentration Index (HHI): {hhi:.4f}")
        logger.info(f"Normalized HHI: {normalized_hhi:.4f}")
        
        return hhi
    
    def calculate_gini_coefficient(self, value_column: str = 'population') -> float:
        """
        Calculate Gini coefficient for spatial distribution.
        
        Gini ranges from 0 (perfect equality) to 1 (complete inequality)
        
        Args:
            value_column: Column containing values to measure inequality
        
        Returns:
            Gini coefficient
        """
        values = self.spatial_units[value_column].sort_values().values
        n = len(values)
        
        if n == 0 or values.sum() == 0:
            return 0.0
        
        # Gini formula
        cumulative = np.cumsum(values)
        gini = (2 * np.sum((np.arange(1, n + 1) * values))) / (n * np.sum(values)) - (n + 1) / n
        
        logger.info(f"Gini Coefficient: {gini:.4f}")
        
        return gini
    
    def regional_balance_analysis(self) -> pd.DataFrame:
        """
        Analyze regional balance across multiple dimensions.
        
        Returns:
            DataFrame with regional balance indicators
        """
        # Aggregate to regions (level 2)
        regions = self.spatial_units[self.spatial_units['level'] == 2].copy()
        
        # Join settlement data
        settlement_stats = self.settlements.groupby('region_id').agg({
            'population': ['sum', 'count', 'mean'],
            'id': 'count'
        }).reset_index()
        settlement_stats.columns = ['region_id', 'total_population', 'settlement_count', 
                                     'avg_settlement_pop', 'n_settlements']
        
        result = regions.merge(settlement_stats, left_on='id', right_on='region_id', how='left')
        
        # Calculate shares
        total_pop = result['total_population'].sum()
        result['population_share'] = result['total_population'] / total_pop
        
        total_area = result['area_sqkm'].sum()
        result['area_share'] = result['area_sqkm'] / total_area
        
        # Population-area ratio (>1 means more dense than average)
        result['pop_area_ratio'] = result['population_share'] / result['area_share']
        
        return result


def run_diagnostics(spatial_units_path: str, settlements_path: str) -> Dict:
    """
    Run full spatial diagnostics suite.
    
    Args:
        spatial_units_path: Path to spatial units GeoPackage
        settlements_path: Path to settlements GeoPackage
    
    Returns:
        Dictionary with all diagnostic results
    """
    logger.info("Running spatial diagnostics...")
    
    spatial_units = gpd.read_file(spatial_units_path)
    settlements = gpd.read_file(settlements_path)
    
    diagnostics = SpatialDiagnostics(spatial_units, settlements)
    
    results = {
        'primacy_index': diagnostics.calculate_primacy_index()[0],
        'concentration_index': diagnostics.calculate_concentration_index(),
        'gini_coefficient': diagnostics.calculate_gini_coefficient(),
        'hierarchy_analysis': diagnostics.settlement_hierarchy_analysis(),
        'regional_balance': diagnostics.regional_balance_analysis()
    }
    
    logger.success("Spatial diagnostics completed")
    
    return results


if __name__ == "__main__":
    # Example usage
    logger.info("Spatial Diagnostics Module")
    logger.info("Usage: from scripts.analysis.spatial_diagnostics import SpatialDiagnostics")
