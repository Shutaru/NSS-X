# 🇸🇦 NSS X - National Spatial Strategy for Saudi Arabia

> Sistema Nacional de Decisão Espacial para a Arábia Saudita  
> Suporte à Vision 2030 com Horizontes 2030 e 2050

[![Live Dashboard](https://img.shields.io/badge/Dashboard-Live-green?style=for-the-badge)](https://nss-x.ngrok.dev)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker)](./Dockerfile)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Tender Complete](https://img.shields.io/badge/Tender-100%25%20Complete-success?style=for-the-badge)](./02_analytics)

---

## 🌐 Live Demo

**Dashboard Online:** [https://nss-x.ngrok.dev](https://nss-x.ngrok.dev)

O dashboard está a correr 24/7 num servidor NVIDIA DGX Spark e inclui **TODOS os 7 workstreams**:
- 🏠 **Overview** - Visão geral, métricas chave, Vision 2050
- 📜 **WS2** - Análise retrospectiva NSS 2001/2030
- 🌍 **WS3** - Benchmarking internacional (5 países)
- 🏭 **WS4** - Análise setorial e regional (6 setores, 13 regiões)
- 🔮 **WS5** - 7 Cenários (4 core + 3 stress tests)
- 📋 **WS6** - NSS Draft completo (20 nodes, 6 corridors)
- 🏛️ **WS7** - Governance Framework (RACI, 26 KPIs)

---

## ✅ TENDER 100% COMPLETE

| Workstream | Status | Deliverables |
|------------|--------|--------------|
| **WS1** Data Collection | ✅ 100% | 17 datasets, 10,798 records |
| **WS2** NSS Review | ✅ 100% | 6 files (NSS 2001/2030 analysis) |
| **WS3** Benchmarking | ✅ 100% | 5 countries, 19 design principles |
| **WS4** Sectoral Analysis | ✅ 100% | 6 sectors, 13 regional diagnostics |
| **WS5** Scenarios | ✅ 100% | 7 scenarios, risk/opportunity maps |
| **WS6** NSS Draft | ✅ 100% | 20 nodes, 6 corridors, SAR 1.4T investment |
| **WS7** Governance | ✅ 100% | 10 bodies, 30 RACI activities, 26 KPIs |

**Total Generated Files:** 45+ deliverables across all workstreams

---

## 📋 Visão Geral

Este repositório contém o **stack técnico completo** para a National Spatial Strategy (NSS) da Arábia Saudita, transformando o caderno de encargos num **sistema integrado de decisão espacial**.

### Arquitetura de 5 Camadas

```
┌─────────────────────────────────────────────────────────────┐
│  5. GOVERNANCE & MONITORING LAYER                           │
│     KPIs, Decision Rights, Coordination Mechanisms          │
├─────────────────────────────────────────────────────────────┤
│  4. STRATEGY LAYER                                          │
│     NSS Vision, Objectives, Spatial Structure, Investments  │
├─────────────────────────────────────────────────────────────┤
│  3. SCENARIO & MODELING LAYER                               │
│     Baseline, Vision 2030, Accelerated, Conservative        │
├─────────────────────────────────────────────────────────────┤
│  2. ANALYTICS LAYER                                         │
│     Retrospective, Sectoral Analysis, Regional Diagnostics  │
├─────────────────────────────────────────────────────────────┤
│  1. DATA LAYER                                              │
│     GASTAT, OCHA/HDX GeoJSON, Vision 2030 Projects          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura do Repositório

```
NSS-X/
├── 01_data/                    # Camada de Dados
│   ├── 01_raw/                 # Dados brutos reais da KSA
│   │   ├── gis/                # GeoJSON das 13 regiões (OCHA/HDX)
│   │   └── statistics/         # CSVs de população, economia, projetos
│   ├── processed/              # Dados processados
│   └── metadata/               # Data dictionary
│
├── src/                        # Código Fonte
│   ├── data/                   # Data providers
│   │   ├── real_data_provider.py    # Carrega dados reais KSA
│   │   └── simulation_engine.py     # Motor de simulação
│   └── analysis/               # Módulos de análise (WS2-WS7)
│       ├── ws2_comprehensive.py     # NSS 2001/2030 review
│       ├── ws3_benchmarking.py      # International benchmarking
│       ├── ws4_comprehensive.py     # Sectoral & regional analysis
│       ├── ws5_comprehensive.py     # Scenario modeling
│       ├── ws6_nss_draft.py         # NSS draft development
│       └── ws7_governance.py        # Governance framework
│
├── 02_analytics/               # Generated Deliverables
│   ├── ws2_outputs/            # WS2 reports and data
│   ├── ws3_outputs/            # WS3 benchmarking results
│   ├── ws4_outputs/            # WS4 sectoral analysis
│   ├── ws5_outputs/            # WS5 scenarios
│   ├── ws6_outputs/            # WS6 NSS draft
│   └── ws7_outputs/            # WS7 governance framework
│
├── scripts/                    # Scripts e Dashboard
│   └── dashboard_complete.py   # Dashboard Streamlit (all workstreams)
│
├── config/                     # Configurações
│   ├── spatial_units.json      # Definição das 13 regiões
│   ├── data_sources.json       # Catálogo de fontes
│   └── scenarios.json          # Parâmetros dos cenários
│
├── Dockerfile                  # Container Docker
├── docker-compose.yml          # Orquestração Docker + ngrok
└── requirements-docker.txt     # Dependências Docker
```

---

## 🚀 Quick Start

### Opção 1: Docker (Recomendado)

```bash
# Clonar repositório
git clone https://github.com/Shutaru/NSS-X.git
cd NSS-X

# Executar com Docker Compose
docker compose up -d

# Aceder ao dashboard
open http://localhost:8501
```

### Opção 2: Instalação Local

```bash
# Clonar repositório
git clone https://github.com/Shutaru/NSS-X.git
cd NSS-X

# Criar ambiente virtual Python
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Executar dashboard
streamlit run scripts/dashboard.py
```

---

## 📊 Dados Incluídos

### Dados Geoespaciais (OCHA/HDX)
- `sau_admin0.geojson` - Fronteiras nacionais
- `sau_admin1.geojson` - 13 regiões administrativas

### Dados Estatísticos (GASTAT/DataSaudi)
| Ficheiro | Descrição |
|----------|-----------|
| `ksa_population_by_region.csv` | População por região (36.4M total) |
| `ksa_economic_indicators.csv` | PIB e indicadores económicos ($1.1T) |
| `ksa_employment_by_region.csv` | Emprego por setor |
| `ksa_vision2030_projects.csv` | 15 mega-projetos Vision 2030 |
| `ksa_major_cities.csv` | Principais cidades |

---

## 🔮 4 Cenários de Desenvolvimento

| Cenário | Probabilidade | Crescimento Pop. | Crescimento PIB |
|---------|---------------|------------------|-----------------|
| **Baseline** | 30% | 1.5%/ano | 3%/ano |
| **Vision 2030** | 35% | 2%/ano | 5%/ano |
| **Accelerated** | 15% | 2.5%/ano | 7%/ano |
| **Conservative** | 20% | 1%/ano | 2%/ano |

---

## 🐳 Deploy

O projeto inclui Docker Compose com ngrok para acesso público:

```bash
# Deploy local
docker compose up -d

# Ver logs
docker compose logs -f

# Parar
docker compose down
```

---

## 📊 Stack Tecnológico

| Componente | Tecnologia |
|------------|------------|
| **GIS Data** | GeoJSON (OCHA/HDX) |
| **Analytics** | Python, GeoPandas, Pandas |
| **Visualization** | Plotly, Streamlit |
| **Scenarios** | Custom Python model |
| **Container** | Docker |
| **Tunnel** | ngrok |

---

## 🔗 Links Úteis

- **Dashboard Live:** [https://nss-x.ngrok.dev](https://nss-x.ngrok.dev)
- **Dados OCHA/HDX:** [https://data.humdata.org](https://data.humdata.org/dataset/cod-ab-sau)
- **Vision 2030:** [https://vision2030.gov.sa](https://vision2030.gov.sa)

---

## 📅 Timeline

Ver [ROADMAP.md](./ROADMAP.md) para o plano detalhado de implementação.

---

*Última atualização: Janeiro 2026*
