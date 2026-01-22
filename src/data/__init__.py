"""
NSS X - Data Layer Module
Provides unified data access through provider interface.
"""

from .provider_interface import (
    DataProviderInterface,
    DataProviderFactory,
    DataRequest,
    DataResponse
)
from .simulation_engine import SimulationEngine, CountryProfile, COUNTRY_PROFILES
from .production_provider import ProductionDataProvider
from .ws1_data_generator import WS1DataGenerator

__all__ = [
    'DataProviderInterface',
    'DataProviderFactory',
    'DataRequest',
    'DataResponse',
    'SimulationEngine',
    'CountryProfile',
    'COUNTRY_PROFILES',
    'ProductionDataProvider',
    'WS1DataGenerator'
]


def get_data_provider(mode: str = 'auto', **kwargs) -> DataProviderInterface:
    """
    Get appropriate data provider based on mode.
    
    Args:
        mode: 'simulation', 'production', or 'auto'
        **kwargs: Provider-specific configuration
    
    Returns:
        DataProviderInterface instance
    
    Usage:
        # For demos/testing
        provider = get_data_provider('simulation')
        
        # For production
        provider = get_data_provider('production', db_connection_string='...')
        
        # Auto-detect (production if configured, else simulation)
        provider = get_data_provider('auto')
    """
    if mode == 'auto':
        # Try production first
        try:
            provider = DataProviderFactory.create('production', **kwargs)
            health = provider.health_check()
            if health.get('status') == 'ok':
                return provider
        except Exception:
            pass
        
        # Fall back to simulation
        return DataProviderFactory.create('simulation', **kwargs)
    
    return DataProviderFactory.create(mode, **kwargs)
