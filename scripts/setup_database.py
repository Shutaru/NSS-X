"""
NSS X - Database Setup Script
Creates the PostgreSQL/PostGIS database schema for the National Spatial Strategy.
"""

import os
import json
from pathlib import Path
from sqlalchemy import create_engine, text
from loguru import logger

# Database connection settings
DB_CONFIG = {
    "host": os.getenv("NSS_DB_HOST", "localhost"),
    "port": os.getenv("NSS_DB_PORT", "5432"),
    "database": os.getenv("NSS_DB_NAME", "nss_x"),
    "user": os.getenv("NSS_DB_USER", "postgres"),
    "password": os.getenv("NSS_DB_PASSWORD", ""),
}


def get_connection_string():
    """Build database connection string."""
    return f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"


def create_schemas(engine):
    """Create database schemas."""
    schemas = [
        "spatial",      # Spatial reference data
        "demographics", # Population and demographic data
        "economic",     # Economic data
        "environment",  # Environmental data
        "infrastructure", # Infrastructure data
        "scenarios",    # Scenario definitions and outputs
        "monitoring",   # KPIs and monitoring
        "metadata",     # Data lineage and metadata
    ]
    
    with engine.connect() as conn:
        for schema in schemas:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
            logger.info(f"Created schema: {schema}")
        conn.commit()


def enable_postgis(engine):
    """Enable PostGIS extension."""
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis_topology"))
        logger.info("PostGIS extensions enabled")
        conn.commit()


def create_spatial_tables(engine):
    """Create core spatial reference tables."""
    
    sql = """
    -- Spatial Units (Administrative Hierarchy)
    CREATE TABLE IF NOT EXISTS spatial.units (
        id SERIAL PRIMARY KEY,
        code VARCHAR(20) UNIQUE NOT NULL,
        name_en VARCHAR(200) NOT NULL,
        name_ar VARCHAR(200),
        level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 5),
        parent_id INTEGER REFERENCES spatial.units(id),
        geom GEOMETRY(MULTIPOLYGON, 4326),
        area_sqkm DECIMAL(12,4),
        perimeter_km DECIMAL(10,3),
        centroid GEOMETRY(POINT, 4326),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE INDEX IF NOT EXISTS idx_spatial_units_geom ON spatial.units USING GIST(geom);
    CREATE INDEX IF NOT EXISTS idx_spatial_units_level ON spatial.units(level);
    CREATE INDEX IF NOT EXISTS idx_spatial_units_parent ON spatial.units(parent_id);
    
    -- Analysis Grid
    CREATE TABLE IF NOT EXISTS spatial.grid (
        id SERIAL PRIMARY KEY,
        cell_code VARCHAR(20) UNIQUE NOT NULL,
        resolution_km INTEGER DEFAULT 10,
        geom GEOMETRY(POLYGON, 4326),
        centroid GEOMETRY(POINT, 4326),
        region_id INTEGER REFERENCES spatial.units(id),
        province_id INTEGER REFERENCES spatial.units(id)
    );
    
    CREATE INDEX IF NOT EXISTS idx_spatial_grid_geom ON spatial.grid USING GIST(geom);
    """
    
    with engine.connect() as conn:
        conn.execute(text(sql))
        logger.info("Spatial tables created")
        conn.commit()


def create_metadata_tables(engine):
    """Create metadata and lineage tables."""
    
    sql = """
    -- Data Sources
    CREATE TABLE IF NOT EXISTS metadata.sources (
        id SERIAL PRIMARY KEY,
        source_code VARCHAR(50) UNIQUE NOT NULL,
        source_name VARCHAR(200) NOT NULL,
        source_type VARCHAR(50),
        organization VARCHAR(200),
        contact_info TEXT,
        data_url TEXT,
        update_frequency VARCHAR(50),
        last_update DATE,
        quality_score DECIMAL(3,2),
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Data Dictionary
    CREATE TABLE IF NOT EXISTS metadata.data_dictionary (
        id SERIAL PRIMARY KEY,
        table_schema VARCHAR(50) NOT NULL,
        table_name VARCHAR(100) NOT NULL,
        column_name VARCHAR(100) NOT NULL,
        data_type VARCHAR(50),
        description_en TEXT,
        description_ar TEXT,
        unit VARCHAR(50),
        valid_range TEXT,
        is_required BOOLEAN DEFAULT FALSE,
        source_id INTEGER REFERENCES metadata.sources(id),
        UNIQUE(table_schema, table_name, column_name)
    );
    
    -- Data Lineage
    CREATE TABLE IF NOT EXISTS metadata.lineage (
        id SERIAL PRIMARY KEY,
        target_schema VARCHAR(50) NOT NULL,
        target_table VARCHAR(100) NOT NULL,
        target_id INTEGER,
        source_schema VARCHAR(50),
        source_table VARCHAR(100),
        source_id INTEGER,
        transformation TEXT,
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        processed_by VARCHAR(100)
    );
    """
    
    with engine.connect() as conn:
        conn.execute(text(sql))
        logger.info("Metadata tables created")
        conn.commit()


def create_scenario_tables(engine):
    """Create scenario-related tables."""
    
    sql = """
    -- Scenario Definitions
    CREATE TABLE IF NOT EXISTS scenarios.definitions (
        id SERIAL PRIMARY KEY,
        code VARCHAR(20) UNIQUE NOT NULL,
        name_en VARCHAR(200) NOT NULL,
        name_ar VARCHAR(200),
        description TEXT,
        scenario_type VARCHAR(50),
        horizon_year INTEGER,
        is_active BOOLEAN DEFAULT TRUE,
        is_primary BOOLEAN DEFAULT FALSE,
        parameters JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by VARCHAR(100)
    );
    
    -- Scenario Parameters (detailed)
    CREATE TABLE IF NOT EXISTS scenarios.parameters (
        id SERIAL PRIMARY KEY,
        scenario_id INTEGER REFERENCES scenarios.definitions(id),
        parameter_category VARCHAR(50) NOT NULL,
        parameter_name VARCHAR(100) NOT NULL,
        parameter_value DECIMAL(15,4),
        parameter_unit VARCHAR(50),
        description TEXT,
        source_assumption TEXT,
        UNIQUE(scenario_id, parameter_category, parameter_name)
    );
    """
    
    with engine.connect() as conn:
        conn.execute(text(sql))
        logger.info("Scenario tables created")
        conn.commit()


def create_monitoring_tables(engine):
    """Create KPI and monitoring tables."""
    
    sql = """
    -- KPI Definitions
    CREATE TABLE IF NOT EXISTS monitoring.kpi_definitions (
        id SERIAL PRIMARY KEY,
        code VARCHAR(50) UNIQUE NOT NULL,
        name_en VARCHAR(200) NOT NULL,
        name_ar VARCHAR(200),
        description TEXT,
        category VARCHAR(100),
        unit VARCHAR(50),
        direction VARCHAR(20),
        target_2030 DECIMAL(15,4),
        target_2050 DECIMAL(15,4),
        calculation_method TEXT,
        data_source TEXT,
        frequency VARCHAR(50),
        is_active BOOLEAN DEFAULT TRUE
    );
    
    -- KPI Values
    CREATE TABLE IF NOT EXISTS monitoring.kpi_values (
        id SERIAL PRIMARY KEY,
        kpi_id INTEGER REFERENCES monitoring.kpi_definitions(id),
        spatial_unit_id INTEGER REFERENCES spatial.units(id),
        period_date DATE NOT NULL,
        value DECIMAL(15,4),
        target DECIMAL(15,4),
        status VARCHAR(20),
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(kpi_id, spatial_unit_id, period_date)
    );
    """
    
    with engine.connect() as conn:
        conn.execute(text(sql))
        logger.info("Monitoring tables created")
        conn.commit()


def load_initial_scenarios(engine):
    """Load scenario definitions from config."""
    config_path = Path(__file__).parent.parent / "config" / "scenarios.json"
    
    if not config_path.exists():
        logger.warning(f"Scenarios config not found: {config_path}")
        return
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    with engine.connect() as conn:
        # Load baseline scenarios
        for scenario in config.get("scenarios", {}).get("baseline", []):
            conn.execute(
                text("""
                    INSERT INTO scenarios.definitions (code, name_en, description, scenario_type, horizon_year, is_primary, parameters)
                    VALUES (:code, :name, :desc, :type, :year, :primary, :params)
                    ON CONFLICT (code) DO UPDATE SET
                        name_en = EXCLUDED.name_en,
                        description = EXCLUDED.description,
                        parameters = EXCLUDED.parameters
                """),
                {
                    "code": scenario["id"],
                    "name": scenario["name"],
                    "desc": scenario["description"],
                    "type": scenario["scenario_type"],
                    "year": scenario["horizon_year"],
                    "primary": scenario.get("is_primary", False),
                    "params": json.dumps(scenario.get("parameters", {}))
                }
            )
        
        # Load alternative scenarios
        for scenario in config.get("scenarios", {}).get("alternatives", []):
            conn.execute(
                text("""
                    INSERT INTO scenarios.definitions (code, name_en, description, scenario_type, horizon_year, is_primary, parameters)
                    VALUES (:code, :name, :desc, :type, :year, :primary, :params)
                    ON CONFLICT (code) DO UPDATE SET
                        name_en = EXCLUDED.name_en,
                        description = EXCLUDED.description,
                        parameters = EXCLUDED.parameters
                """),
                {
                    "code": scenario["id"],
                    "name": scenario["name"],
                    "desc": scenario["description"],
                    "type": scenario["scenario_type"],
                    "year": scenario["horizon_year"],
                    "primary": scenario.get("is_primary", False),
                    "params": json.dumps(scenario.get("parameters", {}))
                }
            )
        
        conn.commit()
        logger.info("Scenario definitions loaded")


def main():
    """Main setup function."""
    logger.info("Starting NSS X database setup...")
    
    try:
        engine = create_engine(get_connection_string())
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            logger.info(f"Connected to: {version}")
        
        # Setup database
        enable_postgis(engine)
        create_schemas(engine)
        create_spatial_tables(engine)
        create_metadata_tables(engine)
        create_scenario_tables(engine)
        create_monitoring_tables(engine)
        
        # Load initial data
        load_initial_scenarios(engine)
        
        logger.success("Database setup completed successfully!")
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise


if __name__ == "__main__":
    main()
