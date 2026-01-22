# 🇸🇦 NSS X - National Spatial Strategy for Saudi Arabia

> Sistema Nacional de Decisão Espacial para a Arábia Saudita  
> Suporte à Vision 2030 com Horizontes 2030 e 2050

[![Live Dashboard](https://img.shields.io/badge/Dashboard-Live-green?style=for-the-badge)](https://nss-x.ngrok.dev)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker)](./Dockerfile)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://python.org)

---

## 🌐 Live Demo

**Dashboard Online:** [https://nss-x.ngrok.dev](https://nss-x.ngrok.dev)

O dashboard está a correr 24/7 num servidor NVIDIA DGX Spark e inclui:
- 📊 **Overview** - Mapa interativo das 13 regiões da Arábia Saudita
- 📈 **WS2 Retrospective** - Análise histórica 2010-2025
- 🏭 **WS4 Sectoral** - Análise setorial com matriz de conflitos/sinergias
- 🔮 **WS5 Scenarios** - 4 cenários de desenvolvimento (2030/2050)
- 🏗️ **Vision 2030 Projects** - Mega-projetos em mapa

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
│   └── analysis/               # Módulos de análise
│       ├── ws2_retrospective.py     # Análise retrospectiva
│       ├── ws4_sectoral.py          # Análise setorial
│       └── ws5_scenarios.py         # Modelação de cenários
│
├── scripts/                    # Scripts e Dashboard
│   └── dashboard.py            # Dashboard Streamlit principal
│
├── config/                     # Configurações
│   ├── spatial_units.json      # Definição das 13 regiões
│   ├── data_sources.json       # Catálogo de fontes
│   └── scenarios.json          # Parâmetros dos 4 cenários
│
├── Dockerfile                  # Container Docker
├── docker-compose.yml          # Orquestração Docker + ngrok
└── requirements-docker.txt     # Dependências Docker
```

---

## 🎯 Workstreams Implementados

| # | Workstream | Status | Descrição |
|---|------------|--------|-----------|
| WS1 | GIS Foundation | ✅ Implementado | 13 regiões com GeoJSON real da OCHA/HDX |
| WS2 | Retrospective Review | ✅ Implementado | Análise 2010-2025 com métricas históricas |
| WS3 | Benchmarking | 🔄 Em curso | Framework de comparação internacional |
| WS4 | Sectoral Analysis | ✅ Implementado | 6 setores com matriz de conflitos |
| WS5 | Scenario Modeling | ✅ Implementado | 4 cenários para 2030/2050 |
| WS6 | NSS Draft | 🔴 Por iniciar | Desenvolvimento da estratégia |
| WS7 | Governance | 🔴 Por iniciar | Framework de governação |

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
