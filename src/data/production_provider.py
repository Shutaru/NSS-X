"""
NSS X - Production Data Provider
Connects to real data sources (databases, APIs, files).
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine
from loguru import logger

from .provider_interface import (
    DataProviderInterface,
    DataProviderFactory,
    DataResponse
)


class ProductionDataProvider(DataProviderInterface):
    """
    Production data provider that connects to real data sources.
    Supports PostgreSQL/PostGIS database and file-based data.
    """
    
    def __init__(self,
                 db_connection_string: Optional[str] = None,
                 data_directory: Optional[Path] = None):
        """
        Initialize production data provider.
        
        Args:
            db_connection_string: PostgreSQL connection string
            data_directory: Path to GIS data files
        """
        self.db_connection_string = db_connection_string or os.getenv('NSS_DB_CONNECTION')
        self.data_directory = data_directory or Path(os.getenv('NSS_DATA_GIS', './01_data/gis'))
        
        self._engine = None
        if self.db_connection_string:
            try:
                self._engine = create_engine(self.db_connection_string)
                logger.info("Database connection established")
            except Exception as e:
                logger.warning(f"Could not connect to database: {e}")
        
        logger.info(f"Production Data Provider initialized")
        logger.info(f"  Data directory: {self.data_directory}")
        logger.info(f"  Database: {'Connected' if self._engine else 'Not configured'}")
    
    @property
    def provider_name(self) -> str:
        return "ProductionDataProvider"
    
    @property
    def is_simulation(self) -> bool:
        return False
    
    def _read_from_db(self, query: str) -> gpd.GeoDataFrame:
        """Execute spatial query and return GeoDataFrame."""
        if not self._engine:
            raise ConnectionError("Database not configured")
        return gpd.read_postgis(query, self._engine, geom_col='geom')
    
    def _read_from_file(self, filename: str, layer: Optional[str] = None) -> gpd.GeoDataFrame:
        """Read GeoDataFrame from file."""
        filepath = self.data_directory / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")
        
        if layer:
            return gpd.read_file(filepath, layer=layer)
        return gpd.read_file(filepath)
    
    def get_spatial_units(self, level: int) -> DataResponse:
        """Get administrative units from database or files."""
        try:
            # Try database first
            if self._engine:
                query = f"""
                    SELECT * FROM spatial.units 
                    WHERE level = {level}
                """
                gdf = self._read_from_db(query)
            else:
                # Fall back to files
                gdf = self._read_from_file(
                    f"administrative/admin_level_{level}.gpkg"
                )
            
            return DataResponse(
                data=gdf,
                metadata={'level': level, 'count': len(gdf)},
                source=self.provider_name,
                retrieved_at=datetime.now(),
                is_simulated=False
            )
        except Exception as e:
            logger.error(f"Failed to get spatial units: {e}")
            raise
    
    def get_settlements(self,
                        min_population: Optional[int] = None,
                        region_id: Optional[int] = None) -> DataResponse:
        """Get settlements from database or files."""
        try:
            if self._engine:
                where_clauses = []
                if min_population:
                    where_clauses.append(f"population >= {min_population}")
                if region_id:
                    where_clauses.append(f"region_id = {region_id}")
                
                where = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
                query = f"SELECT * FROM demographics.settlements {where}"
                gdf = self._read_from_db(query)
            else:
                gdf = self._read_from_file("demographics/settlements.gpkg")
                if min_population:
                    gdf = gdf[gdf['population'] >= min_population]
                if region_id:
                    gdf = gdf[gdf['region_id'] == region_id]
            
            return DataResponse(
                data=gdf,
                metadata={'count': len(gdf)},
                source=self.provider_name,
                retrieved_at=datetime.now(),
                is_simulated=False
            )
        except Exception as e:
            logger.error(f"Failed to get settlements: {e}")
            raise
    
    def get_population(self,
                       spatial_level: int,
                       year: int,
                       scenario_id: Optional[str] = None) -> DataResponse:
        """Get population data."""
        try:
            if self._engine:
                scenario_filter = f"AND scenario_id = '{scenario_id}'" if scenario_id else "AND scenario_id IS NULL"
                query = f"""
                    SELECT u.*, p.population, p.pop_density, p.year
                    FROM spatial.units u
                    JOIN demographics.population p ON u.id = p.spatial_unit_id
                    WHERE u.level = {spatial_level} 
                    AND p.year = {year}
                    {scenario_filter}
                """
                gdf = self._read_from_db(query)
            else:
                gdf = self._read_from_file(f"demographics/population_{year}.gpkg")
            
            return DataResponse(
                data=gdf,
                metadata={'year': year, 'scenario': scenario_id},
                source=self.provider_name,
                retrieved_at=datetime.now(),
                is_simulated=False
            )
        except Exception as e:
            logger.error(f"Failed to get population: {e}")
            raise
    
    def get_economic_data(self,
                          indicator: str,
                          spatial_level: int,
                          year: int) -> DataResponse:
        """Get economic data."""
        try:
            if self._engine:
                query = f"""
                    SELECT u.*, e.*
                    FROM spatial.units u
                    JOIN economic.{indicator} e ON u.id = e.spatial_unit_id
                    WHERE u.level = {spatial_level}
                    AND e.year = {year}
                """
                gdf = self._read_from_db(query)
            else:
                gdf = self._read_from_file(f"economic/{indicator}_{year}.gpkg")
            
            return DataResponse(
                data=gdf,
                metadata={'indicator': indicator, 'year': year},
                source=self.provider_name,
                retrieved_at=datetime.now(),
                is_simulated=False
            )
        except Exception as e:
            logger.error(f"Failed to get economic data: {e}")
            raise
    
    def get_infrastructure(self,
                           infra_type: str,
                           region_id: Optional[int] = None) -> DataResponse:
        """Get infrastructure data."""
        try:
            if self._engine:
                region_filter = f"WHERE region_id = {region_id}" if region_id else ""
                query = f"SELECT * FROM infrastructure.{infra_type} {region_filter}"
                gdf = self._read_from_db(query)
            else:
                gdf = self._read_from_file(f"infrastructure/{infra_type}.gpkg")
                if region_id:
                    gdf = gdf[gdf['region_id'] == region_id]
            
            return DataResponse(
                data=gdf,
                metadata={'type': infra_type},
                source=self.provider_name,
                retrieved_at=datetime.now(),
                is_simulated=False
            )
        except Exception as e:
            logger.error(f"Failed to get infrastructure: {e}")
            raise
    
    def get_environment(self,
                        layer_type: str,
                        region_id: Optional[int] = None) -> DataResponse:
        """Get environmental data."""
        try:
            if self._engine:
                region_filter = f"WHERE region_id = {region_id}" if region_id else ""
                query = f"SELECT * FROM environment.{layer_type} {region_filter}"
                gdf = self._read_from_db(query)
            else:
                gdf = self._read_from_file(f"environment/{layer_type}.gpkg")
                if region_id:
                    gdf = gdf[gdf['region_id'] == region_id]
            
            return DataResponse(
                data=gdf,
                metadata={'type': layer_type},
                source=self.provider_name,
                retrieved_at=datetime.now(),
                is_simulated=False
            )
        except Exception as e:
            logger.error(f"Failed to get environment data: {e}")
            raise
    
    def get_projects(self,
                     status: Optional[str] = None,
                     sector: Optional[str] = None) -> DataResponse:
        """Get major projects."""
        try:
            if self._engine:
                where_clauses = []
                if status:
                    where_clauses.append(f"status = '{status}'")
                if sector:
                    where_clauses.append(f"sector = '{sector}'")
                
                where = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
                query = f"SELECT * FROM infrastructure.projects {where}"
                gdf = self._read_from_db(query)
            else:
                gdf = self._read_from_file("economic/projects.gpkg")
                if status:
                    gdf = gdf[gdf['status'] == status]
                if sector:
                    gdf = gdf[gdf['sector'] == sector]
            
            return DataResponse(
                data=gdf,
                metadata={'count': len(gdf)},
                source=self.provider_name,
                retrieved_at=datetime.now(),
                is_simulated=False
            )
        except Exception as e:
            logger.error(f"Failed to get projects: {e}")
            raise
    
    def health_check(self) -> Dict[str, Any]:
        """Check provider connectivity."""
        status = {
            "provider": self.provider_name,
            "is_simulation": False,
            "timestamp": datetime.now().isoformat()
        }
        
        # Check database
        if self._engine:
            try:
                with self._engine.connect() as conn:
                    conn.execute("SELECT 1")
                status["database"] = "connected"
            except Exception as e:
                status["database"] = f"error: {e}"
        else:
            status["database"] = "not configured"
        
        # Check data directory
        if self.data_directory.exists():
            status["data_directory"] = "exists"
            status["files_count"] = len(list(self.data_directory.rglob("*.gpkg")))
        else:
            status["data_directory"] = "not found"
        
        status["status"] = "ok" if status.get("database") == "connected" or status.get("data_directory") == "exists" else "degraded"
        
        return status


# Register with factory
DataProviderFactory.register('production', ProductionDataProvider)
