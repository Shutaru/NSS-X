"""
NSS X - Data Validation Framework
Quality validation for NSS spatial data using Great Expectations patterns.
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from loguru import logger


@dataclass
class ValidationResult:
    """Result of a validation check."""
    check_name: str
    passed: bool
    message: str
    details: Optional[Dict[str, Any]] = None


@dataclass
class DataQualityReport:
    """Complete quality report for a dataset."""
    dataset_name: str
    total_checks: int
    passed_checks: int
    failed_checks: int
    results: List[ValidationResult]
    quality_score: float
    
    @property
    def is_valid(self) -> bool:
        return self.failed_checks == 0


class SpatialDataValidator:
    """
    Validator for NSS spatial datasets.
    Implements quality dimensions: Completeness, Accuracy, Consistency, Timeliness, Uniqueness.
    """
    
    def __init__(self, gdf: gpd.GeoDataFrame, dataset_name: str):
        self.gdf = gdf
        self.dataset_name = dataset_name
        self.results: List[ValidationResult] = []
    
    def validate_all(self) -> DataQualityReport:
        """Run all validation checks."""
        self.results = []
        
        # Completeness checks
        self._check_geometry_not_null()
        self._check_required_columns()
        
        # Accuracy checks
        self._check_geometry_valid()
        self._check_crs()
        self._check_numeric_ranges()
        
        # Consistency checks
        self._check_geometry_type()
        
        # Uniqueness checks
        self._check_unique_ids()
        
        passed = sum(1 for r in self.results if r.passed)
        failed = len(self.results) - passed
        score = passed / len(self.results) if self.results else 0
        
        return DataQualityReport(
            dataset_name=self.dataset_name,
            total_checks=len(self.results),
            passed_checks=passed,
            failed_checks=failed,
            results=self.results,
            quality_score=score
        )
    
    def _check_geometry_not_null(self):
        """Check that all geometries are present."""
        null_count = self.gdf.geometry.isna().sum()
        passed = null_count == 0
        self.results.append(ValidationResult(
            check_name="geometry_not_null",
            passed=passed,
            message=f"Null geometries: {null_count}",
            details={"null_count": int(null_count)}
        ))
    
    def _check_geometry_valid(self):
        """Check that all geometries are valid."""
        invalid_count = (~self.gdf.geometry.is_valid).sum()
        passed = invalid_count == 0
        self.results.append(ValidationResult(
            check_name="geometry_valid",
            passed=passed,
            message=f"Invalid geometries: {invalid_count}",
            details={"invalid_count": int(invalid_count)}
        ))
    
    def _check_crs(self, expected_epsg: int = 4326):
        """Check coordinate reference system."""
        actual_crs = self.gdf.crs
        passed = actual_crs is not None and actual_crs.to_epsg() == expected_epsg
        self.results.append(ValidationResult(
            check_name="crs_check",
            passed=passed,
            message=f"CRS: {actual_crs} (expected EPSG:{expected_epsg})",
            details={"actual_crs": str(actual_crs), "expected_epsg": expected_epsg}
        ))
    
    def _check_geometry_type(self, expected_types: Optional[List[str]] = None):
        """Check geometry types are consistent."""
        geom_types = self.gdf.geometry.geom_type.unique().tolist()
        if expected_types:
            passed = all(t in expected_types for t in geom_types)
        else:
            passed = len(geom_types) == 1
        self.results.append(ValidationResult(
            check_name="geometry_type_consistent",
            passed=passed,
            message=f"Geometry types: {geom_types}",
            details={"types_found": geom_types}
        ))
    
    def _check_unique_ids(self, id_column: str = "id"):
        """Check for unique identifiers."""
        if id_column not in self.gdf.columns:
            self.results.append(ValidationResult(
                check_name="unique_ids",
                passed=False,
                message=f"ID column '{id_column}' not found"
            ))
            return
        
        duplicates = self.gdf[id_column].duplicated().sum()
        passed = duplicates == 0
        self.results.append(ValidationResult(
            check_name="unique_ids",
            passed=passed,
            message=f"Duplicate IDs: {duplicates}",
            details={"duplicate_count": int(duplicates)}
        ))
    
    def _check_required_columns(self, required: Optional[List[str]] = None):
        """Check required columns are present."""
        if required is None:
            required = ["id", "name_en"]  # Default required columns
        
        missing = [col for col in required if col not in self.gdf.columns]
        passed = len(missing) == 0
        self.results.append(ValidationResult(
            check_name="required_columns",
            passed=passed,
            message=f"Missing columns: {missing}" if missing else "All required columns present",
            details={"missing_columns": missing}
        ))
    
    def _check_numeric_ranges(self, column_ranges: Optional[Dict[str, tuple]] = None):
        """Check numeric values are within expected ranges."""
        if column_ranges is None:
            # Default checks for common columns
            column_ranges = {
                "area_sqkm": (0, 1000000),
                "population": (0, 50000000),
                "pop_density": (0, 50000),
            }
        
        for col, (min_val, max_val) in column_ranges.items():
            if col not in self.gdf.columns:
                continue
            
            out_of_range = ((self.gdf[col] < min_val) | (self.gdf[col] > max_val)).sum()
            passed = out_of_range == 0
            self.results.append(ValidationResult(
                check_name=f"range_check_{col}",
                passed=passed,
                message=f"{col}: {out_of_range} values out of range [{min_val}, {max_val}]",
                details={"column": col, "out_of_range_count": int(out_of_range)}
            ))


def validate_geopackage(gpkg_path: Path, layer_name: Optional[str] = None) -> DataQualityReport:
    """
    Validate a GeoPackage file.
    
    Args:
        gpkg_path: Path to GeoPackage file
        layer_name: Specific layer to validate (if None, validates first layer)
    
    Returns:
        DataQualityReport with validation results
    """
    logger.info(f"Validating: {gpkg_path}")
    
    if layer_name:
        gdf = gpd.read_file(gpkg_path, layer=layer_name)
        name = f"{gpkg_path.stem}:{layer_name}"
    else:
        gdf = gpd.read_file(gpkg_path)
        name = gpkg_path.stem
    
    validator = SpatialDataValidator(gdf, name)
    report = validator.validate_all()
    
    if report.is_valid:
        logger.success(f"✓ {name}: All {report.total_checks} checks passed (score: {report.quality_score:.2%})")
    else:
        logger.warning(f"✗ {name}: {report.failed_checks}/{report.total_checks} checks failed (score: {report.quality_score:.2%})")
        for result in report.results:
            if not result.passed:
                logger.warning(f"  - {result.check_name}: {result.message}")
    
    return report


def validate_all_gis_data(gis_folder: Path) -> List[DataQualityReport]:
    """
    Validate all GeoPackage files in a folder.
    
    Args:
        gis_folder: Path to folder containing GIS data
    
    Returns:
        List of DataQualityReport for each file
    """
    reports = []
    gpkg_files = list(gis_folder.rglob("*.gpkg"))
    
    logger.info(f"Found {len(gpkg_files)} GeoPackage files to validate")
    
    for gpkg_path in gpkg_files:
        try:
            report = validate_geopackage(gpkg_path)
            reports.append(report)
        except Exception as e:
            logger.error(f"Failed to validate {gpkg_path}: {e}")
    
    # Summary
    total_files = len(reports)
    valid_files = sum(1 for r in reports if r.is_valid)
    avg_score = sum(r.quality_score for r in reports) / total_files if total_files > 0 else 0
    
    logger.info(f"\nValidation Summary:")
    logger.info(f"  Files validated: {total_files}")
    logger.info(f"  Files passed: {valid_files}")
    logger.info(f"  Average quality score: {avg_score:.2%}")
    
    return reports


if __name__ == "__main__":
    # Example usage
    gis_folder = Path(__file__).parent.parent / "01_data" / "gis"
    
    if gis_folder.exists():
        reports = validate_all_gis_data(gis_folder)
    else:
        logger.info(f"GIS folder not found: {gis_folder}")
        logger.info("Run this script after populating GIS data.")
