# 🏗️ Arquitetura Técnica - NSS X

> Documento de Arquitetura do Sistema Nacional de Decisão Espacial

---

## 1. Visão Geral da Arquitetura

### 1.1 Princípios de Design

| Princípio | Descrição | Implementação |
|-----------|-----------|---------------|
| **Open Format** | Todos os dados e modelos em formatos abertos | GeoPackage, GeoJSON, CSV, PostgreSQL |
| **Reproducibility** | Análises e modelos reprodutíveis | Scripts versionados, documentação |
| **Traceability** | Rastreabilidade dados → decisões | Metadata, lineage tracking |
| **Scalability** | Suporte a crescimento de dados | PostgreSQL, particionamento |
| **Interoperability** | Standards OGC e ISO | WMS, WFS, GeoJSON, ISO 19115 |

### 1.2 Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION LAYER                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   QGIS      │  │  Dashboards │  │   Reports   │  │    Maps     │        │
│  │  Desktop    │  │  (Streamlit)│  │  (MkDocs)   │  │  (Kepler)   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└────────────────────────────────────────┬────────────────────────────────────┘
                                         │
┌────────────────────────────────────────▼────────────────────────────────────┐
│                            APPLICATION LAYER                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │  Analytics       │  │  Scenario        │  │  Monitoring      │          │
│  │  Engine          │  │  Simulation      │  │  System          │          │
│  │  (Python)        │  │  Model (Python)  │  │  (Python)        │          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
└────────────────────────────────────────┬────────────────────────────────────┘
                                         │
┌────────────────────────────────────────▼────────────────────────────────────┐
│                              DATA LAYER                                      │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │                    PostgreSQL + PostGIS                          │       │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │       │
│  │  │Demographics│ │ Economic  │ │Environment│ │Infrastruc.│       │       │
│  │  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │       │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │       │
│  │  │ Projects  │ │ Scenarios │ │ Indicators│ │  Metadata │       │       │
│  │  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │       │
│  └─────────────────────────────────────────────────────────────────┘       │
└────────────────────────────────────────┬────────────────────────────────────┘
                                         │
┌────────────────────────────────────────▼────────────────────────────────────┐
│                           INTEGRATION LAYER                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │  ETL Pipelines   │  │  Data Validation │  │  API Gateway     │          │
│  │  (Python)        │  │  (Great Expect.) │  │  (FastAPI)       │          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
└────────────────────────────────────────┬────────────────────────────────────┘
                                         │
┌────────────────────────────────────────▼────────────────────────────────────┐
│                          EXTERNAL DATA SOURCES                               │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐              │
│  │ GASTAT  │ │ SDAIA   │ │ Royal   │ │ Line    │ │ Regional│              │
│  │         │ │         │ │ Commis. │ │ Minist. │ │ Author. │              │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Camada de Dados (Data Layer)

### 2.1 Modelo de Dados Conceptual

```
┌─────────────────────────────────────────────────────────────────┐
│                    SPATIAL REFERENCE SYSTEM                      │
│                                                                  │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│   │   REGION    │───►│  PROVINCE   │───►│  DISTRICT   │        │
│   │   (13)      │    │   (~50)     │    │   (~200)    │        │
│   └─────────────┘    └─────────────┘    └─────────────┘        │
│         │                  │                  │                 │
│         ▼                  ▼                  ▼                 │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│   │  GRID CELL  │    │ SETTLEMENT  │    │   PROJECT   │        │
│   │  (10x10km)  │    │   POINT     │    │   LOCATION  │        │
│   └─────────────┘    └─────────────┘    └─────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Domínios de Dados

#### 2.2.1 Demographics Domain
```sql
-- Schema: demographics
CREATE TABLE demographics.population (
    id SERIAL PRIMARY KEY,
    spatial_unit_id INTEGER REFERENCES spatial.units(id),
    year INTEGER NOT NULL,
    scenario_id INTEGER REFERENCES scenarios.definitions(id),
    total_population BIGINT,
    male_population BIGINT,
    female_population BIGINT,
    median_age DECIMAL(4,1),
    household_count INTEGER,
    avg_household_size DECIMAL(3,1),
    population_density DECIMAL(10,2),
    urban_population_pct DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_id INTEGER REFERENCES metadata.sources(id)
);

CREATE TABLE demographics.projections (
    id SERIAL PRIMARY KEY,
    spatial_unit_id INTEGER REFERENCES spatial.units(id),
    base_year INTEGER NOT NULL,
    target_year INTEGER NOT NULL,
    scenario_id INTEGER REFERENCES scenarios.definitions(id),
    projected_population BIGINT,
    growth_rate DECIMAL(5,3),
    confidence_interval_low BIGINT,
    confidence_interval_high BIGINT,
    methodology TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2.2.2 Economic Domain
```sql
-- Schema: economic
CREATE TABLE economic.gdp (
    id SERIAL PRIMARY KEY,
    spatial_unit_id INTEGER REFERENCES spatial.units(id),
    year INTEGER NOT NULL,
    scenario_id INTEGER REFERENCES scenarios.definitions(id),
    gdp_nominal DECIMAL(15,2),
    gdp_real DECIMAL(15,2),
    gdp_per_capita DECIMAL(12,2),
    gdp_growth_rate DECIMAL(5,2),
    currency_code CHAR(3) DEFAULT 'SAR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_id INTEGER REFERENCES metadata.sources(id)
);

CREATE TABLE economic.employment (
    id SERIAL PRIMARY KEY,
    spatial_unit_id INTEGER REFERENCES spatial.units(id),
    year INTEGER NOT NULL,
    sector_id INTEGER REFERENCES economic.sectors(id),
    employed_count INTEGER,
    unemployment_rate DECIMAL(5,2),
    labor_force_participation DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE economic.sectors (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    name_en VARCHAR(100),
    name_ar VARCHAR(100),
    parent_sector_id INTEGER REFERENCES economic.sectors(id),
    isic_code VARCHAR(10)
);
```

#### 2.2.3 Environment Domain
```sql
-- Schema: environment
CREATE TABLE environment.land_cover (
    id SERIAL PRIMARY KEY,
    spatial_unit_id INTEGER REFERENCES spatial.units(id),
    year INTEGER NOT NULL,
    land_cover_type_id INTEGER REFERENCES environment.land_cover_types(id),
    area_sqkm DECIMAL(12,4),
    percentage DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE environment.water_resources (
    id SERIAL PRIMARY KEY,
    spatial_unit_id INTEGER REFERENCES spatial.units(id),
    year INTEGER NOT NULL,
    groundwater_volume_mcm DECIMAL(12,2),
    desalinated_capacity_mcm DECIMAL(12,2),
    recycled_water_mcm DECIMAL(12,2),
    water_demand_mcm DECIMAL(12,2),
    water_stress_index DECIMAL(4,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE environment.climate_indicators (
    id SERIAL PRIMARY KEY,
    spatial_unit_id INTEGER REFERENCES spatial.units(id),
    year INTEGER NOT NULL,
    scenario_id INTEGER REFERENCES scenarios.definitions(id),
    avg_temperature_c DECIMAL(4,1),
    max_temperature_c DECIMAL(4,1),
    precipitation_mm DECIMAL(8,2),
    drought_risk_index DECIMAL(4,2),
    heat_stress_days INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2.2.4 Infrastructure Domain
```sql
-- Schema: infrastructure
CREATE TABLE infrastructure.transport_network (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY(LINESTRING, 4326),
    network_type VARCHAR(50), -- road, rail, air, port
    category VARCHAR(50), -- highway, primary, secondary, etc.
    name_en VARCHAR(200),
    name_ar VARCHAR(200),
    length_km DECIMAL(10,3),
    capacity INTEGER,
    status VARCHAR(50), -- operational, planned, under_construction
    completion_year INTEGER,
    source_id INTEGER REFERENCES metadata.sources(id)
);

CREATE TABLE infrastructure.utilities (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY(POINT, 4326),
    utility_type VARCHAR(50), -- power, water, telecom
    facility_name VARCHAR(200),
    capacity DECIMAL(15,2),
    capacity_unit VARCHAR(20),
    status VARCHAR(50),
    operational_year INTEGER,
    source_id INTEGER REFERENCES metadata.sources(id)
);

CREATE TABLE infrastructure.projects (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY(GEOMETRY, 4326),
    project_name VARCHAR(500),
    project_type VARCHAR(100),
    sector_id INTEGER REFERENCES economic.sectors(id),
    status VARCHAR(50),
    start_date DATE,
    completion_date DATE,
    budget_sar DECIMAL(15,2),
    implementing_agency VARCHAR(200),
    vision2030_program VARCHAR(200),
    source_id INTEGER REFERENCES metadata.sources(id)
);
```

### 2.3 Spatial Reference Schema

```sql
-- Schema: spatial
CREATE TABLE spatial.units (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name_en VARCHAR(200) NOT NULL,
    name_ar VARCHAR(200),
    level INTEGER NOT NULL, -- 1=Country, 2=Region, 3=Province, 4=District
    parent_id INTEGER REFERENCES spatial.units(id),
    geom GEOMETRY(MULTIPOLYGON, 4326),
    area_sqkm DECIMAL(12,4),
    centroid GEOMETRY(POINT, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_level CHECK (level BETWEEN 1 AND 5)
);

CREATE INDEX idx_spatial_units_geom ON spatial.units USING GIST(geom);
CREATE INDEX idx_spatial_units_level ON spatial.units(level);
CREATE INDEX idx_spatial_units_parent ON spatial.units(parent_id);

CREATE TABLE spatial.grid (
    id SERIAL PRIMARY KEY,
    cell_code VARCHAR(20) UNIQUE NOT NULL,
    geom GEOMETRY(POLYGON, 4326),
    centroid GEOMETRY(POINT, 4326),
    resolution_km INTEGER DEFAULT 10,
    region_id INTEGER REFERENCES spatial.units(id),
    province_id INTEGER REFERENCES spatial.units(id)
);

CREATE INDEX idx_spatial_grid_geom ON spatial.grid USING GIST(geom);
```

### 2.4 Metadata & Lineage Schema

```sql
-- Schema: metadata
CREATE TABLE metadata.sources (
    id SERIAL PRIMARY KEY,
    source_name VARCHAR(200) NOT NULL,
    source_type VARCHAR(50), -- government, survey, satellite, model
    organization VARCHAR(200),
    contact_info TEXT,
    data_url TEXT,
    update_frequency VARCHAR(50),
    last_update DATE,
    quality_score DECIMAL(3,2),
    notes TEXT
);

CREATE TABLE metadata.data_dictionary (
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
    source_id INTEGER REFERENCES metadata.sources(id)
);

CREATE TABLE metadata.lineage (
    id SERIAL PRIMARY KEY,
    target_table VARCHAR(100) NOT NULL,
    target_id INTEGER NOT NULL,
    source_table VARCHAR(100),
    source_id INTEGER,
    transformation TEXT,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_by VARCHAR(100)
);
```

---

## 3. Camada de Cenários (Scenarios Layer)

### 3.1 Schema de Cenários

```sql
-- Schema: scenarios
CREATE TABLE scenarios.definitions (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name_en VARCHAR(200) NOT NULL,
    name_ar VARCHAR(200),
    description TEXT,
    scenario_type VARCHAR(50), -- baseline, alternative, stress_test
    time_horizon INTEGER, -- 2030, 2050
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100)
);

CREATE TABLE scenarios.parameters (
    id SERIAL PRIMARY KEY,
    scenario_id INTEGER REFERENCES scenarios.definitions(id),
    parameter_name VARCHAR(100) NOT NULL,
    parameter_value DECIMAL(15,4),
    parameter_unit VARCHAR(50),
    description TEXT,
    source_assumption TEXT
);

CREATE TABLE scenarios.drivers (
    id SERIAL PRIMARY KEY,
    scenario_id INTEGER REFERENCES scenarios.definitions(id),
    driver_category VARCHAR(50), -- demographic, economic, climate, technology
    driver_name VARCHAR(200),
    trajectory VARCHAR(50), -- high, medium, low, custom
    description TEXT
);
```

### 3.2 Cenários Pré-definidos

| Código | Nome | Descrição | Horizonte |
|--------|------|-----------|-----------|
| `BAU_2030` | Business as Usual 2030 | Continuação tendências atuais | 2030 |
| `BAU_2050` | Business as Usual 2050 | Continuação tendências atuais | 2050 |
| `CLIMATE_STRESS` | Climate Stress | Impactos alterações climáticas severas | 2050 |
| `TECH_DISRUPTION` | Tech Disruption | Aceleração transformação digital | 2050 |
| `ECON_TRANSFORM` | Economic Transformation | Diversificação acelerada | 2050 |
| `DEMO_SHIFT` | Demographic Shift | Mudanças demográficas significativas | 2050 |

---

## 4. Camada de Analytics

### 4.1 Componentes Analíticos

```python
# analytics/core/spatial_diagnostics.py
class SpatialDiagnostics:
    """
    Core spatial analysis engine for NSS diagnostics.
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        
    def settlement_hierarchy_analysis(self, year: int) -> GeoDataFrame:
        """Analyze urban hierarchy and primacy."""
        pass
    
    def accessibility_analysis(self, origin_type: str, destination_type: str) -> GeoDataFrame:
        """Calculate spatial accessibility metrics."""
        pass
    
    def carrying_capacity_assessment(self, spatial_unit_id: int) -> dict:
        """Assess environmental carrying capacity."""
        pass
    
    def economic_concentration_index(self, sector: str, year: int) -> float:
        """Calculate spatial concentration of economic activity."""
        pass
```

### 4.2 Pipeline de Análise

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Raw Data   │────►│  Validation │────►│  Transform  │────►│  Analysis   │
│  Ingestion  │     │  & QA       │     │  & Enrich   │     │  Engine     │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                                                   │
                                                                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Reports    │◄────│  Visualize  │◄────│  Aggregate  │◄────│  Indicator  │
│  & Maps     │     │             │     │             │     │  Calculation│
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

---

## 5. Modelo de Simulação Espacial

### 5.1 Arquitetura do Modelo

```python
# scenarios/model/spatial_simulation.py
class SpatialSimulationModel:
    """
    Transparent, explainable spatial simulation model for NSS scenarios.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.modules = {
            'demographics': DemographicModule(),
            'economic': EconomicModule(),
            'land_use': LandUseModule(),
            'infrastructure': InfrastructureModule(),
            'environment': EnvironmentModule()
        }
        
    def run_scenario(self, scenario_id: str, base_year: int, target_year: int) -> SimulationResult:
        """Execute complete scenario simulation."""
        pass
    
    def sensitivity_analysis(self, parameter: str, range_pct: float) -> SensitivityResult:
        """Perform sensitivity analysis on key parameters."""
        pass
    
    def export_results(self, format: str = 'geopackage') -> Path:
        """Export simulation results in open format."""
        pass
```

### 5.2 Módulos do Modelo

| Módulo | Inputs | Outputs | Metodologia |
|--------|--------|---------|-------------|
| **Demographics** | Pop atual, fertilidade, migração | Pop projetada por unidade | Cohort-component |
| **Economic** | GDP, emprego, setores | Crescimento regional | Shift-share + gravity |
| **Land Use** | Cobertura atual, restrições | Mudanças de uso | Cellular automata |
| **Infrastructure** | Rede atual, projetos planeados | Acessibilidade | Network analysis |
| **Environment** | Clima, recursos, carrying cap. | Stress indicators | Threshold analysis |

---

## 6. Camada de Governação e Monitorização

### 6.1 Schema de KPIs

```sql
-- Schema: monitoring
CREATE TABLE monitoring.kpi_definitions (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name_en VARCHAR(200) NOT NULL,
    name_ar VARCHAR(200),
    description TEXT,
    category VARCHAR(100), -- spatial_balance, infrastructure, environment, economic
    unit VARCHAR(50),
    direction VARCHAR(20), -- higher_better, lower_better, target_range
    target_2030 DECIMAL(15,4),
    target_2050 DECIMAL(15,4),
    calculation_method TEXT,
    data_source TEXT,
    frequency VARCHAR(50) -- annual, quarterly, monthly
);

CREATE TABLE monitoring.kpi_values (
    id SERIAL PRIMARY KEY,
    kpi_id INTEGER REFERENCES monitoring.kpi_definitions(id),
    spatial_unit_id INTEGER REFERENCES spatial.units(id),
    period_date DATE NOT NULL,
    value DECIMAL(15,4),
    target DECIMAL(15,4),
    status VARCHAR(20), -- on_track, at_risk, off_track
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6.2 KPIs Propostos

| Categoria | KPI | Unidade | Target 2030 | Target 2050 |
|-----------|-----|---------|-------------|-------------|
| Spatial Balance | Population concentration index | Index | <0.7 | <0.6 |
| Spatial Balance | Regional GDP disparity | Ratio | <3.0 | <2.5 |
| Infrastructure | National connectivity score | % | 85% | 95% |
| Infrastructure | Infrastructure investment per capita | SAR | TBD | TBD |
| Environment | Water stress index | Index | <0.8 | <0.7 |
| Environment | Protected areas coverage | % | 30% | 35% |
| Economic | Economic diversification index | Index | >0.7 | >0.8 |
| Economic | Jobs created per region | Count | TBD | TBD |

---

## 7. Stack Tecnológico Detalhado

### 7.1 Componentes Core

| Camada | Tecnologia | Versão | Licença |
|--------|------------|--------|---------|
| **Database** | PostgreSQL | 15+ | PostgreSQL License |
| **Spatial Extension** | PostGIS | 3.3+ | GPL v2 |
| **ETL** | Python + SQLAlchemy | 3.10+ | MIT |
| **Data Validation** | Great Expectations | 0.17+ | Apache 2.0 |
| **Spatial Analysis** | GeoPandas | 0.14+ | BSD |
| **Visualization** | QGIS | 3.28+ | GPL v2 |
| **Dashboards** | Streamlit | 1.28+ | Apache 2.0 |
| **Web Maps** | Kepler.gl | 3.0+ | MIT |
| **Documentation** | MkDocs | 1.5+ | BSD |
| **API** | FastAPI | 0.104+ | MIT |

### 7.2 Formatos de Dados

| Tipo | Formato Primário | Formato Export | Justificação |
|------|------------------|----------------|--------------|
| Vector | PostgreSQL/PostGIS | GeoPackage (.gpkg) | OGC standard, SQLite |
| Raster | GeoTIFF | Cloud-Optimized GeoTIFF | Efficient, standard |
| Tabular | PostgreSQL | CSV, Parquet | Universal, efficient |
| Config | JSON/YAML | JSON | Human + machine readable |
| Reports | Markdown | PDF, DOCX | Versionable, portable |

---

## 8. Segurança e Qualidade

### 8.1 Data Quality Framework

```python
# validation/data_quality.py
class DataQualityFramework:
    """
    Data quality validation using Great Expectations.
    """
    
    quality_dimensions = {
        'completeness': 'Required fields populated',
        'accuracy': 'Values within valid ranges',
        'consistency': 'Cross-table relationships valid',
        'timeliness': 'Data within acceptable age',
        'uniqueness': 'No duplicate records'
    }
    
    def validate_dataset(self, dataset_name: str) -> QualityReport:
        """Run full quality validation suite."""
        pass
```

### 8.2 Níveis de Acesso

| Role | Data Read | Data Write | Model Run | Admin |
|------|-----------|------------|-----------|-------|
| Viewer | ✅ | ❌ | ❌ | ❌ |
| Analyst | ✅ | ❌ | ✅ | ❌ |
| Data Steward | ✅ | ✅ | ✅ | ❌ |
| Admin | ✅ | ✅ | ✅ | ✅ |

---

## 9. Deployment e Operações

### 9.1 Ambientes

| Ambiente | Propósito | Infraestrutura |
|----------|-----------|----------------|
| **Development** | Dev e testes | Local / Cloud VM |
| **Staging** | UAT e validação | Cloud VM |
| **Production** | Sistema live | On-premise / Cloud |

### 9.2 Backup e Recovery

- **Database**: Daily automated backups, 30-day retention
- **GIS Files**: Version-controlled, weekly snapshots
- **Models**: Git-versioned, tagged releases
- **Documentation**: Git-versioned, continuous

---

*Documento de Arquitetura v1.0 - Janeiro 2026*
