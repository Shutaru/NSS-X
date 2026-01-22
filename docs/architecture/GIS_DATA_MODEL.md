# 🗺️ Modelo de Dados GIS - NSS X

> Especificação do Modelo de Dados Espaciais para a National Spatial Strategy

---

## 1. Visão Geral

### 1.1 Objetivos do Modelo

- **Single Source of Truth**: Uma única base de dados espacial autoritativa
- **Scenario-Ready**: Estrutura preparada para múltiplos horizontes e cenários
- **Interoperability**: Compatível com standards OGC e ISO
- **Traceability**: Rastreabilidade completa de fontes e transformações

### 1.2 Coordinate Reference Systems

| CRS | EPSG | Uso |
|-----|------|-----|
| WGS 84 | 4326 | Armazenamento e intercâmbio |
| UTM Zone 37N | 32637 | Análise espacial (oeste) |
| UTM Zone 38N | 32638 | Análise espacial (centro) |
| UTM Zone 39N | 32639 | Análise espacial (este) |

---

## 2. Hierarquia Espacial

### 2.1 Níveis Administrativos

```
Level 1: COUNTRY (País)
    └── Level 2: REGION (Região) [13 regiões]
            └── Level 3: PROVINCE (Província) [~50]
                    └── Level 4: DISTRICT (Distrito/Município) [~200]
                            └── Level 5: LOCALITY (Localidade) [opcional]
```

### 2.2 Tabela: spatial.admin_hierarchy

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador único |
| `code` | VARCHAR(20) | Código oficial (ex: SA-01) |
| `name_en` | VARCHAR(200) | Nome em inglês |
| `name_ar` | VARCHAR(200) | Nome em árabe |
| `level` | INTEGER | Nível hierárquico (1-5) |
| `parent_id` | INTEGER FK | Referência ao nível superior |
| `geom` | MULTIPOLYGON | Geometria do limite |
| `area_sqkm` | DECIMAL | Área em km² |
| `perimeter_km` | DECIMAL | Perímetro em km |
| `centroid` | POINT | Centróide |

### 2.3 Grid de Análise

Para análises que requerem uniformidade espacial:

| Resolução | Uso | Nº Células (aprox.) |
|-----------|-----|---------------------|
| 100km × 100km | Macro-regional | ~200 |
| 10km × 10km | Regional/Provincial | ~20,000 |
| 1km × 1km | Local/Urbano | ~2,000,000 |

---

## 3. Domínios Temáticos

### 3.1 Demographics (demografia)

#### Layer: population_distribution

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `spatial_unit_id` | INTEGER FK | Unidade espacial |
| `year` | INTEGER | Ano de referência |
| `scenario_id` | INTEGER FK | Cenário (null = atual) |
| `total_pop` | BIGINT | População total |
| `male_pop` | BIGINT | População masculina |
| `female_pop` | BIGINT | População feminina |
| `pop_0_14` | BIGINT | População 0-14 anos |
| `pop_15_64` | BIGINT | População 15-64 anos |
| `pop_65_plus` | BIGINT | População 65+ anos |
| `nationals` | BIGINT | Nacionais |
| `expatriates` | BIGINT | Expatriados |
| `pop_density` | DECIMAL | Densidade (hab/km²) |

#### Layer: settlements

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | POINT | Localização |
| `name_en` | VARCHAR | Nome em inglês |
| `name_ar` | VARCHAR | Nome em árabe |
| `settlement_type` | VARCHAR | Tipo (city, town, village) |
| `hierarchy_rank` | INTEGER | Ranking na hierarquia urbana |
| `population` | INTEGER | População |
| `year` | INTEGER | Ano de referência |
| `is_capital` | BOOLEAN | É capital de região/província |

#### Layer: urban_areas

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | POLYGON | Área urbana |
| `name` | VARCHAR | Nome |
| `area_sqkm` | DECIMAL | Área urbanizada |
| `population` | INTEGER | População |
| `year` | INTEGER | Ano de referência |
| `urban_type` | VARCHAR | metropolitan, large_city, medium_city, small_city, town |

---

### 3.2 Economic (economia)

#### Layer: economic_zones

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | POLYGON | Limite da zona |
| `zone_name` | VARCHAR | Nome da zona |
| `zone_type` | VARCHAR | industrial, commercial, mixed, special |
| `status` | VARCHAR | operational, planned, under_development |
| `area_sqkm` | DECIMAL | Área |
| `sector_focus` | VARCHAR | Setores principais |
| `employment_capacity` | INTEGER | Capacidade de emprego |
| `vision2030_program` | VARCHAR | Programa Vision 2030 associado |

#### Layer: major_projects

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | GEOMETRY | Localização/área do projeto |
| `project_name` | VARCHAR | Nome do projeto |
| `project_type` | VARCHAR | Tipo de projeto |
| `sector` | VARCHAR | Setor económico |
| `status` | VARCHAR | announced, planned, under_construction, operational |
| `start_date` | DATE | Data de início |
| `completion_date` | DATE | Data prevista conclusão |
| `budget_billion_sar` | DECIMAL | Orçamento (mil milhões SAR) |
| `jobs_created` | INTEGER | Empregos a criar |
| `implementing_entity` | VARCHAR | Entidade responsável |
| `giga_project` | BOOLEAN | É giga-projeto |

#### Layer: tourism_assets

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | POINT/POLYGON | Localização |
| `name` | VARCHAR | Nome |
| `asset_type` | VARCHAR | heritage, natural, cultural, religious, entertainment |
| `unesco_status` | VARCHAR | world_heritage, tentative, none |
| `annual_visitors` | INTEGER | Visitantes anuais |
| `tourism_potential` | VARCHAR | high, medium, low |

---

### 3.3 Infrastructure (infraestruturas)

#### Layer: road_network

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | LINESTRING | Geometria da via |
| `road_name` | VARCHAR | Nome da via |
| `road_number` | VARCHAR | Número da via |
| `road_class` | VARCHAR | highway, primary, secondary, tertiary, local |
| `surface_type` | VARCHAR | paved, unpaved |
| `lanes` | INTEGER | Número de faixas |
| `length_km` | DECIMAL | Comprimento |
| `speed_limit_kmh` | INTEGER | Limite de velocidade |
| `status` | VARCHAR | operational, under_construction, planned |

#### Layer: rail_network

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | LINESTRING | Geometria da linha |
| `line_name` | VARCHAR | Nome da linha |
| `rail_type` | VARCHAR | high_speed, conventional, metro, freight |
| `gauge_mm` | INTEGER | Bitola |
| `electrified` | BOOLEAN | Eletrificada |
| `length_km` | DECIMAL | Comprimento |
| `status` | VARCHAR | operational, under_construction, planned |
| `operator` | VARCHAR | Operador |

#### Layer: airports

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | POINT | Localização |
| `airport_name` | VARCHAR | Nome |
| `icao_code` | CHAR(4) | Código ICAO |
| `iata_code` | CHAR(3) | Código IATA |
| `airport_type` | VARCHAR | international, domestic, regional |
| `runways` | INTEGER | Número de pistas |
| `annual_passengers` | INTEGER | Passageiros anuais |
| `annual_cargo_tons` | INTEGER | Carga anual (tons) |
| `status` | VARCHAR | operational, under_expansion, planned |

#### Layer: ports

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | POINT/POLYGON | Localização/área |
| `port_name` | VARCHAR | Nome |
| `port_type` | VARCHAR | commercial, industrial, fishing, mixed |
| `berths` | INTEGER | Número de berços |
| `annual_teu` | INTEGER | Capacidade TEU |
| `annual_cargo_tons` | INTEGER | Carga anual (tons) |
| `status` | VARCHAR | operational, under_expansion, planned |

#### Layer: power_plants

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | POINT | Localização |
| `plant_name` | VARCHAR | Nome |
| `fuel_type` | VARCHAR | gas, oil, solar, wind, nuclear |
| `capacity_mw` | INTEGER | Capacidade (MW) |
| `generation_gwh` | INTEGER | Geração anual (GWh) |
| `status` | VARCHAR | operational, under_construction, planned |
| `commissioning_year` | INTEGER | Ano de comissionamento |

#### Layer: desalination_plants

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | POINT | Localização |
| `plant_name` | VARCHAR | Nome |
| `technology` | VARCHAR | RO, MSF, MED, hybrid |
| `capacity_m3_day` | INTEGER | Capacidade (m³/dia) |
| `status` | VARCHAR | operational, under_construction, planned |

---

### 3.4 Environment (ambiente)

#### Layer: land_cover

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | POLYGON | Área |
| `lc_class` | VARCHAR | Classe de cobertura |
| `lc_code` | INTEGER | Código (CCI-LC) |
| `area_sqkm` | DECIMAL | Área |
| `year` | INTEGER | Ano de referência |

**Classes de Land Cover:**
- Urban/Built-up
- Agricultural
- Forest/Woodland
- Shrubland
- Grassland
- Bare/Desert
- Water bodies
- Wetlands

#### Layer: protected_areas

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | POLYGON | Limite |
| `name` | VARCHAR | Nome |
| `designation` | VARCHAR | national_park, reserve, sanctuary, etc. |
| `iucn_category` | VARCHAR | Categoria IUCN |
| `area_sqkm` | DECIMAL | Área |
| `established_year` | INTEGER | Ano de estabelecimento |
| `managing_authority` | VARCHAR | Autoridade gestora |

#### Layer: water_bodies

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | POLYGON | Geometria |
| `name` | VARCHAR | Nome |
| `water_type` | VARCHAR | lake, reservoir, wadi, sabkha |
| `area_sqkm` | DECIMAL | Área |
| `is_permanent` | BOOLEAN | Permanente ou sazonal |

#### Layer: aquifers

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | POLYGON | Extensão do aquífero |
| `aquifer_name` | VARCHAR | Nome |
| `aquifer_type` | VARCHAR | confined, unconfined |
| `storage_bcm` | DECIMAL | Armazenamento (bcm) |
| `recharge_rate_mcm` | DECIMAL | Taxa de recarga (mcm/ano) |
| `extraction_rate_mcm` | DECIMAL | Taxa de extração (mcm/ano) |
| `water_quality` | VARCHAR | fresh, brackish, saline |
| `sustainability_status` | VARCHAR | sustainable, at_risk, critical |

#### Layer: climate_zones

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | POLYGON | Zona |
| `climate_class` | VARCHAR | Classificação Köppen |
| `avg_temp_c` | DECIMAL | Temperatura média anual |
| `avg_precip_mm` | DECIMAL | Precipitação média anual |
| `aridity_index` | DECIMAL | Índice de aridez |

#### Layer: environmental_sensitivity

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `geom` | POLYGON | Área |
| `sensitivity_type` | VARCHAR | Tipo de sensibilidade |
| `sensitivity_level` | VARCHAR | high, medium, low |
| `constraints` | TEXT | Restrições aplicáveis |

---

### 3.5 Scenarios (cenários)

#### Table: scenario_definitions

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `code` | VARCHAR(20) | Código único |
| `name` | VARCHAR | Nome do cenário |
| `description` | TEXT | Descrição |
| `scenario_type` | VARCHAR | baseline, alternative, stress |
| `horizon_year` | INTEGER | Ano horizonte |
| `is_active` | BOOLEAN | Cenário ativo |

#### Table: scenario_parameters

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL PK | Identificador |
| `scenario_id` | INTEGER FK | Cenário |
| `parameter_category` | VARCHAR | demographic, economic, climate, etc. |
| `parameter_name` | VARCHAR | Nome do parâmetro |
| `value` | DECIMAL | Valor |
| `unit` | VARCHAR | Unidade |

---

## 4. Layers Derivados

### 4.1 Accessibility Layers

| Layer | Descrição | Metodologia |
|-------|-----------|-------------|
| `access_to_cities` | Tempo de viagem para cidade mais próxima | Network analysis |
| `access_to_hospitals` | Tempo de viagem para hospital | Network analysis |
| `access_to_airports` | Tempo de viagem para aeroporto | Network analysis |
| `service_area_coverage` | Áreas cobertas por serviços | Isochrones |

### 4.2 Composite Indicators

| Layer | Descrição | Componentes |
|-------|-----------|-------------|
| `development_potential` | Potencial de desenvolvimento | Demographics + Economy + Infrastructure |
| `environmental_stress` | Stress ambiental | Water + Climate + Sensitivity |
| `infrastructure_gap` | Défice infraestrutural | Current vs. Required |
| `conflict_areas` | Áreas de conflito espacial | Synergies - Conflicts |

---

## 5. Metadata Standards

### 5.1 ISO 19115 Compliance

Todos os layers incluem metadata conforme ISO 19115:

```xml
<MD_Metadata>
    <fileIdentifier>nss_x_layer_name</fileIdentifier>
    <language>eng</language>
    <characterSet>utf8</characterSet>
    <hierarchyLevel>dataset</hierarchyLevel>
    <contact>...</contact>
    <dateStamp>2026-01-22</dateStamp>
    <metadataStandardName>ISO 19115:2014</metadataStandardName>
    <referenceSystemInfo>EPSG:4326</referenceSystemInfo>
    <identificationInfo>...</identificationInfo>
    <distributionInfo>...</distributionInfo>
    <dataQualityInfo>...</dataQualityInfo>
</MD_Metadata>
```

### 5.2 Campos de Auditoria Padrão

Todos os layers incluem:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `created_at` | TIMESTAMP | Data de criação |
| `created_by` | VARCHAR | Utilizador que criou |
| `updated_at` | TIMESTAMP | Última atualização |
| `updated_by` | VARCHAR | Utilizador que atualizou |
| `source_id` | INTEGER FK | Fonte dos dados |
| `quality_flag` | VARCHAR | validated, provisional, unverified |

---

## 6. Exportação e Intercâmbio

### 6.1 Formatos de Exportação

| Formato | Extensão | Uso |
|---------|----------|-----|
| GeoPackage | .gpkg | Intercâmbio primário, offline use |
| GeoJSON | .geojson | Web applications, APIs |
| Shapefile | .shp | Legacy systems |
| KML | .kml | Google Earth, simple visualization |
| CSV | .csv | Tabular data without geometry |

### 6.2 Packages de Entrega

```
NSS_GIS_Package/
├── administrative/
│   ├── regions.gpkg
│   ├── provinces.gpkg
│   └── districts.gpkg
├── demographics/
│   ├── population.gpkg
│   ├── settlements.gpkg
│   └── urban_areas.gpkg
├── economic/
│   ├── economic_zones.gpkg
│   ├── major_projects.gpkg
│   └── tourism_assets.gpkg
├── infrastructure/
│   ├── transport_network.gpkg
│   ├── utilities.gpkg
│   └── facilities.gpkg
├── environment/
│   ├── land_cover.gpkg
│   ├── protected_areas.gpkg
│   └── water_resources.gpkg
├── scenarios/
│   ├── baseline_2030.gpkg
│   ├── baseline_2050.gpkg
│   └── alternatives/
├── metadata/
│   ├── data_dictionary.xlsx
│   ├── layer_catalogue.xlsx
│   └── iso19115_metadata/
└── README.md
```

---

*GIS Data Model v1.0 - Janeiro 2026*
