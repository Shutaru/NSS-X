"""
NSS X - ETL Pipeline for Data Ingestion
Extract, Transform, Load utilities for NSS data sources.
"""

import os
import json
import pandas as pd
import geopandas as gpd
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from abc import ABC, abstractmethod
from loguru import logger


@dataclass
class ETLResult:
    """Result of an ETL operation."""
    source: str
    records_processed: int
    records_loaded: int
    errors: int
    duration_seconds: float
    output_path: Optional[Path] = None
    
    @property
    def success(self) -> bool:
        return self.errors == 0


class DataSource(ABC):
    """Abstract base class for data sources."""
    
    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """Extract data from source."""
        pass
    
    @abstractmethod
    def validate(self, df: pd.DataFrame) -> bool:
        """Validate extracted data."""
        pass


class FileDataSource(DataSource):
    """Data source from local files."""
    
    def __init__(self, file_path: Path, file_type: str = "auto"):
        self.file_path = file_path
        self.file_type = file_type if file_type != "auto" else self._detect_type()
    
    def _detect_type(self) -> str:
        suffix = self.file_path.suffix.lower()
        type_map = {
            '.csv': 'csv',
            '.xlsx': 'excel',
            '.xls': 'excel',
            '.json': 'json',
            '.geojson': 'geojson',
            '.gpkg': 'geopackage',
            '.shp': 'shapefile'
        }
        return type_map.get(suffix, 'unknown')
    
    def extract(self) -> pd.DataFrame:
        if self.file_type == 'csv':
            return pd.read_csv(self.file_path)
        elif self.file_type == 'excel':
            return pd.read_excel(self.file_path)
        elif self.file_type == 'json':
            return pd.read_json(self.file_path)
        elif self.file_type in ['geojson', 'geopackage', 'shapefile']:
            return gpd.read_file(self.file_path)
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")
    
    def validate(self, df: pd.DataFrame) -> bool:
        return len(df) > 0


class ETLPipeline:
    """
    ETL Pipeline for NSS data processing.
    Handles extraction, transformation, and loading of various data sources.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize ETL pipeline.
        
        Args:
            config_path: Path to data sources configuration file
        """
        self.config = self._load_config(config_path) if config_path else {}
        self.transformers: Dict[str, callable] = {}
        self._register_default_transformers()
    
    def _load_config(self, config_path: Path) -> Dict:
        """Load configuration from JSON file."""
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def _register_default_transformers(self):
        """Register default transformation functions."""
        self.transformers['standardize_columns'] = self._standardize_columns
        self.transformers['set_crs'] = self._set_crs
        self.transformers['clean_names'] = self._clean_names
        self.transformers['add_metadata'] = self._add_metadata
    
    @staticmethod
    def _standardize_columns(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
        """Rename columns to standard names."""
        return df.rename(columns=mapping)
    
    @staticmethod
    def _set_crs(gdf: gpd.GeoDataFrame, epsg: int = 4326) -> gpd.GeoDataFrame:
        """Set or convert CRS."""
        if gdf.crs is None:
            return gdf.set_crs(epsg=epsg)
        elif gdf.crs.to_epsg() != epsg:
            return gdf.to_crs(epsg=epsg)
        return gdf
    
    @staticmethod
    def _clean_names(df: pd.DataFrame, name_columns: List[str]) -> pd.DataFrame:
        """Clean and standardize name fields."""
        for col in name_columns:
            if col in df.columns:
                df[col] = df[col].str.strip()
                df[col] = df[col].str.title()
        return df
    
    @staticmethod
    def _add_metadata(df: pd.DataFrame, source: str) -> pd.DataFrame:
        """Add metadata columns."""
        df['_source'] = source
        df['_loaded_at'] = datetime.now().isoformat()
        return df
    
    def run(self, 
            source: DataSource, 
            transformations: List[Dict[str, Any]],
            output_path: Path,
            output_format: str = "geopackage") -> ETLResult:
        """
        Run ETL pipeline.
        
        Args:
            source: Data source to extract from
            transformations: List of transformation configs
            output_path: Path for output file
            output_format: Output format (geopackage, csv, etc.)
        
        Returns:
            ETLResult with processing statistics
        """
        start_time = datetime.now()
        errors = 0
        
        try:
            # Extract
            logger.info(f"Extracting from source...")
            df = source.extract()
            records_extracted = len(df)
            logger.info(f"Extracted {records_extracted} records")
            
            # Validate
            if not source.validate(df):
                raise ValueError("Data validation failed")
            
            # Transform
            for transform_config in transformations:
                transform_name = transform_config['name']
                transform_args = transform_config.get('args', {})
                
                if transform_name in self.transformers:
                    logger.info(f"Applying transformation: {transform_name}")
                    df = self.transformers[transform_name](df, **transform_args)
                else:
                    logger.warning(f"Unknown transformation: {transform_name}")
            
            # Load
            logger.info(f"Loading to {output_path}")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if output_format == "geopackage" and isinstance(df, gpd.GeoDataFrame):
                df.to_file(output_path, driver="GPKG")
            elif output_format == "csv":
                df.to_csv(output_path, index=False)
            elif output_format == "parquet":
                df.to_parquet(output_path, index=False)
            else:
                df.to_file(output_path)
            
            records_loaded = len(df)
            
        except Exception as e:
            logger.error(f"ETL failed: {e}")
            errors = 1
            records_extracted = 0
            records_loaded = 0
        
        duration = (datetime.now() - start_time).total_seconds()
        
        result = ETLResult(
            source=str(source.file_path) if hasattr(source, 'file_path') else "unknown",
            records_processed=records_extracted,
            records_loaded=records_loaded,
            errors=errors,
            duration_seconds=duration,
            output_path=output_path if errors == 0 else None
        )
        
        if result.success:
            logger.success(f"ETL completed: {records_loaded} records in {duration:.2f}s")
        else:
            logger.error(f"ETL failed with {errors} errors")
        
        return result


def process_administrative_boundaries(
    input_path: Path, 
    output_path: Path,
    level: int = 2
) -> ETLResult:
    """
    Process administrative boundaries data.
    
    Args:
        input_path: Path to input file
        output_path: Path for processed output
        level: Administrative level (2=region, 3=province, 4=district)
    
    Returns:
        ETLResult
    """
    source = FileDataSource(input_path)
    
    pipeline = ETLPipeline()
    
    transformations = [
        {
            'name': 'standardize_columns',
            'args': {
                'mapping': {
                    'ADMIN_NAME': 'name_en',
                    'ADMIN_NAME_AR': 'name_ar',
                    'ADMIN_CODE': 'code',
                    'AREA_KM2': 'area_sqkm'
                }
            }
        },
        {
            'name': 'set_crs',
            'args': {'epsg': 4326}
        },
        {
            'name': 'add_metadata',
            'args': {'source': 'administrative_boundaries'}
        }
    ]
    
    return pipeline.run(source, transformations, output_path)


if __name__ == "__main__":
    logger.info("ETL Pipeline Module")
    logger.info("Usage: from scripts.etl.data_loader import ETLPipeline, FileDataSource")
