"""
NSS X - Data Provider Interface
Abstract interface for data sources. Production code uses this interface,
allowing seamless switching between real data sources and simulation engine.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import geopandas as gpd
import pandas as pd


@dataclass
class DataRequest:
    """Request specification for data retrieval."""
    domain: str  # demographics, economic, infrastructure, environment
    dataset: str  # specific dataset name
    spatial_level: int  # 1=country, 2=region, 3=province, 4=district
    year: Optional[int] = None
    scenario_id: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None


@dataclass
class DataResponse:
    """Response from data provider."""
    data: gpd.GeoDataFrame | pd.DataFrame
    metadata: Dict[str, Any]
    source: str
    retrieved_at: datetime
    is_simulated: bool = False


class DataProviderInterface(ABC):
    """
    Abstract interface for NSS data providers.
    All data access in the system goes through this interface.
    """
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the data provider."""
        pass
    
    @property
    @abstractmethod
    def is_simulation(self) -> bool:
        """Whether this provider returns simulated data."""
        pass
    
    @abstractmethod
    def get_spatial_units(self, level: int) -> DataResponse:
        """
        Get administrative/spatial units.
        
        Args:
            level: Hierarchy level (1=country, 2=region, 3=province, 4=district)
        
        Returns:
            DataResponse with GeoDataFrame of spatial units
        """
        pass
    
    @abstractmethod
    def get_settlements(self, 
                        min_population: Optional[int] = None,
                        region_id: Optional[int] = None) -> DataResponse:
        """
        Get settlement points.
        
        Args:
            min_population: Filter by minimum population
            region_id: Filter by region
        
        Returns:
            DataResponse with GeoDataFrame of settlements
        """
        pass
    
    @abstractmethod
    def get_population(self,
                       spatial_level: int,
                       year: int,
                       scenario_id: Optional[str] = None) -> DataResponse:
        """
        Get population data.
        
        Args:
            spatial_level: Aggregation level
            year: Reference year
            scenario_id: Scenario for projections (None for historical)
        
        Returns:
            DataResponse with population data
        """
        pass
    
    @abstractmethod
    def get_economic_data(self,
                          indicator: str,
                          spatial_level: int,
                          year: int) -> DataResponse:
        """
        Get economic indicators.
        
        Args:
            indicator: Economic indicator (gdp, employment, etc.)
            spatial_level: Aggregation level
            year: Reference year
        
        Returns:
            DataResponse with economic data
        """
        pass
    
    @abstractmethod
    def get_infrastructure(self,
                           infra_type: str,
                           region_id: Optional[int] = None) -> DataResponse:
        """
        Get infrastructure data.
        
        Args:
            infra_type: Type (roads, rail, airports, ports, power, water)
            region_id: Filter by region
        
        Returns:
            DataResponse with infrastructure GeoDataFrame
        """
        pass
    
    @abstractmethod
    def get_environment(self,
                        layer_type: str,
                        region_id: Optional[int] = None) -> DataResponse:
        """
        Get environmental data.
        
        Args:
            layer_type: Type (land_cover, protected_areas, water_bodies, climate)
            region_id: Filter by region
        
        Returns:
            DataResponse with environmental GeoDataFrame
        """
        pass
    
    @abstractmethod
    def get_projects(self,
                     status: Optional[str] = None,
                     sector: Optional[str] = None) -> DataResponse:
        """
        Get major projects data.
        
        Args:
            status: Filter by status (planned, under_construction, operational)
            sector: Filter by sector
        
        Returns:
            DataResponse with projects GeoDataFrame
        """
        pass
    
    def health_check(self) -> Dict[str, Any]:
        """Check provider connectivity and status."""
        return {
            "provider": self.provider_name,
            "is_simulation": self.is_simulation,
            "status": "ok",
            "timestamp": datetime.now().isoformat()
        }


class DataProviderFactory:
    """Factory for creating data providers."""
    
    _providers: Dict[str, type] = {}
    
    @classmethod
    def register(cls, name: str, provider_class: type):
        """Register a provider class."""
        cls._providers[name] = provider_class
    
    @classmethod
    def create(cls, name: str, **kwargs) -> DataProviderInterface:
        """
        Create a data provider instance.
        
        Args:
            name: Provider name ('simulation', 'production', etc.)
            **kwargs: Provider-specific configuration
        
        Returns:
            DataProviderInterface instance
        """
        if name not in cls._providers:
            raise ValueError(f"Unknown provider: {name}. Available: {list(cls._providers.keys())}")
        
        return cls._providers[name](**kwargs)
    
    @classmethod
    def available_providers(cls) -> List[str]:
        """List available providers."""
        return list(cls._providers.keys())
