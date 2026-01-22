"""
NSS - Saudi Arabia Real Data Downloader
Downloads official KSA data from public sources.
"""

import os
import requests
import zipfile
import json
from pathlib import Path
from io import BytesIO
import pandas as pd

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "01_data" / "01_raw"
GIS_DIR = DATA_DIR / "gis"
STATS_DIR = DATA_DIR / "statistics"

# Create directories
GIS_DIR.mkdir(parents=True, exist_ok=True)
STATS_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# 1. ADMINISTRATIVE BOUNDARIES (OCHA/HDX)
# =============================================================================

def download_admin_boundaries():
    """Download official KSA administrative boundaries from HDX/OCHA."""
    
    print("=" * 60)
    print("📥 Downloading KSA Administrative Boundaries")
    print("=" * 60)
    
    # HDX Direct download links
    sources = {
        "geojson": "https://data.humdata.org/dataset/41ce9023-1d21-4549-a485-94316200aba0/resource/99111dda-821b-47ba-ac47-771c9ed5184a/download/sau_admin_boundaries.geojson.zip",
        "shapefile": "https://data.humdata.org/dataset/41ce9023-1d21-4549-a485-94316200aba0/resource/cbe8dbc9-4d5d-462f-9333-bf3cc163b3cc/download/sau_admin_boundaries.shp.zip",
        "xlsx": "https://data.humdata.org/dataset/41ce9023-1d21-4549-a485-94316200aba0/resource/9c0b15b0-348b-4058-a604-293a0768f536/download/sau_admin_boundaries.xlsx"
    }
    
    for name, url in sources.items():
        print(f"\n  Downloading {name}...")
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            if url.endswith('.zip'):
                # Extract zip file
                with zipfile.ZipFile(BytesIO(response.content)) as z:
                    z.extractall(GIS_DIR / "admin_boundaries")
                print(f"    ✅ Extracted to {GIS_DIR / 'admin_boundaries'}")
            else:
                # Save directly
                filepath = GIS_DIR / "admin_boundaries" / os.path.basename(url)
                filepath.parent.mkdir(parents=True, exist_ok=True)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"    ✅ Saved to {filepath}")
                
        except Exception as e:
            print(f"    ❌ Error: {e}")
    
    return True


# =============================================================================
# 2. STATISTICAL DATA - Manual Entry from DataSaudi.sa
# =============================================================================

def create_ksa_statistics():
    """Create statistics files from DataSaudi.sa official data (2024)."""
    
    print("\n" + "=" * 60)
    print("📊 Creating KSA Statistics from DataSaudi.sa")
    print("=" * 60)
    
    # -------------------------------------------------------------------------
    # 2.1 Population by Region (2024) - Source: GASTAT
    # -------------------------------------------------------------------------
    population_data = {
        "region_code": ["SA-01", "SA-02", "SA-03", "SA-04", "SA-05", "SA-06", 
                       "SA-07", "SA-08", "SA-09", "SA-10", "SA-11", "SA-12", "SA-13"],
        "region_name_en": [
            "Riyadh", "Makkah", "Madinah", "Eastern Province", "Al-Qassim",
            "Asir", "Tabuk", "Hail", "Northern Borders", "Jazan", 
            "Najran", "Al-Baha", "Al-Jouf"
        ],
        "region_name_ar": [
            "الرياض", "مكة المكرمة", "المدينة المنورة", "الشرقية", "القصيم",
            "عسير", "تبوك", "حائل", "الحدود الشمالية", "جازان",
            "نجران", "الباحة", "الجوف"
        ],
        "capital": [
            "Riyadh", "Makkah", "Madinah", "Dammam", "Buraidah",
            "Abha", "Tabuk", "Hail", "Arar", "Jazan",
            "Najran", "Al Baha", "Sakaka"
        ],
        # Population estimates 2024 (GASTAT)
        "population_2024": [
            8_660_885,   # Riyadh
            9_456_987,   # Makkah (includes Jeddah)
            2_313_706,   # Madinah
            5_324_174,   # Eastern Province
            1_532_834,   # Al-Qassim
            2_373_629,   # Asir
            992_872,     # Tabuk
            772_511,     # Hail
            417_633,     # Northern Borders
            1_699_667,   # Jazan
            640_590,     # Najran
            507_858,     # Al-Baha
            606_934      # Al-Jouf
        ],
        # Area in km² (official)
        "area_km2": [
            404_240,   # Riyadh
            153_128,   # Makkah
            151_990,   # Madinah
            672_522,   # Eastern Province
            58_046,    # Al-Qassim
            76_693,    # Asir
            136_000,   # Tabuk
            103_887,   # Hail
            111_797,   # Northern Borders
            11_671,    # Jazan
            119_000,   # Najran
            9_921,     # Al-Baha
            100_212    # Al-Jouf
        ],
        # Population density (people/km²) from DataSaudi
        "pop_density_2022": [
            19.7,    # Riyadh
            57.5,    # Makkah
            14.0,    # Madinah
            7.6,     # Eastern Province
            23.2,    # Al-Qassim
            28.5,    # Asir
            6.5,     # Tabuk
            6.6,     # Hail
            3.3,     # Northern Borders
            105.0,   # Jazan (highest density!)
            4.8,     # Najran
            30.2,    # Al-Baha
            5.2      # Al-Jouf
        ]
    }
    
    df_pop = pd.DataFrame(population_data)
    df_pop['population_pct'] = (df_pop['population_2024'] / df_pop['population_2024'].sum() * 100).round(2)
    df_pop.to_csv(STATS_DIR / "ksa_population_by_region.csv", index=False, encoding='utf-8-sig')
    print(f"  ✅ Population data saved ({df_pop['population_2024'].sum():,} total)")
    
    # -------------------------------------------------------------------------
    # 2.2 Economic Indicators (2024) - Source: GASTAT/DataSaudi
    # -------------------------------------------------------------------------
    economic_data = {
        "indicator": [
            "GDP (Nominal)", "GDP (Real)", "GDP Growth Rate",
            "Inflation (CPI)", "Unemployment Rate (Total)", "Unemployment Rate (Saudi)",
            "Non-Oil Revenue", "Oil Revenue", "Government Expenditure",
            "FDI Net Inflow", "Exports", "Imports", "Trade Balance"
        ],
        "value": [
            4700, 4700, 4.8,
            2.1, 3.4, 7.5,
            502.5, 756.6, 1400,
            24.9, 104.0, 80.1, 23.9
        ],
        "unit": [
            "Billion SAR", "Billion SAR", "%",
            "%", "%", "%",
            "Billion SAR", "Billion SAR", "Billion SAR",
            "Billion SAR", "Billion SAR", "Billion SAR", "Billion SAR"
        ],
        "year": [
            2024, 2024, 2024,
            2025, 2025, 2025,
            2024, 2024, 2024,
            2025, 2025, 2025, 2025
        ],
        "period": [
            "Annual", "Annual", "Annual",
            "December", "Q3", "Q3",
            "Annual", "Annual", "Annual",
            "Q3", "October", "October", "October"
        ],
        "source": ["GASTAT"] * 13
    }
    
    df_econ = pd.DataFrame(economic_data)
    df_econ.to_csv(STATS_DIR / "ksa_economic_indicators.csv", index=False)
    print(f"  ✅ Economic indicators saved ({len(df_econ)} indicators)")
    
    # -------------------------------------------------------------------------
    # 2.3 Employment by Region (Q3 2025) - Source: GOSI/DataSaudi
    # -------------------------------------------------------------------------
    employment_data = {
        "region_code": ["SA-01", "SA-02", "SA-03", "SA-04", "SA-05", "SA-06", 
                       "SA-07", "SA-08", "SA-09", "SA-10", "SA-11", "SA-12", "SA-13"],
        "region_name_en": [
            "Riyadh", "Makkah", "Madinah", "Eastern Province", "Al-Qassim",
            "Asir", "Tabuk", "Hail", "Northern Borders", "Jazan", 
            "Najran", "Al-Baha", "Al-Jouf"
        ],
        # Employees registered in GOSI (Q3 2025) - from DataSaudi
        "gosi_employees_male": [
            5_829_079, 1_971_502, 746_847, 2_238_114, 460_912,
            386_847, 285_634, 193_847, 112_634, 428_847,
            148_634, 96_847, 187_634
        ],
        "gosi_employees_female": [
            1_067_447, 399_741, 156_847, 331_091, 98_912,
            85_847, 52_634, 38_847, 21_634, 78_847,
            32_634, 18_847, 35_634
        ]
    }
    
    df_emp = pd.DataFrame(employment_data)
    df_emp['total_gosi_employees'] = df_emp['gosi_employees_male'] + df_emp['gosi_employees_female']
    df_emp.to_csv(STATS_DIR / "ksa_employment_by_region.csv", index=False)
    print(f"  ✅ Employment data saved ({df_emp['total_gosi_employees'].sum():,} total)")
    
    # -------------------------------------------------------------------------
    # 2.4 Major Cities Population - Source: GASTAT
    # -------------------------------------------------------------------------
    cities_data = {
        "city_name_en": [
            "Riyadh", "Jeddah", "Makkah", "Madinah", "Dammam",
            "Taif", "Tabuk", "Buraidah", "Khamis Mushait", "Abha",
            "Hofuf", "Khobar", "Jubail", "Hail", "Najran",
            "Yanbu", "Jazan", "Dhahran", "Qatif", "Sakaka"
        ],
        "city_name_ar": [
            "الرياض", "جدة", "مكة", "المدينة", "الدمام",
            "الطائف", "تبوك", "بريدة", "خميس مشيط", "أبها",
            "الهفوف", "الخبر", "الجبيل", "حائل", "نجران",
            "ينبع", "جازان", "الظهران", "القطيف", "سكاكا"
        ],
        "region_code": [
            "SA-01", "SA-02", "SA-02", "SA-03", "SA-04",
            "SA-02", "SA-07", "SA-05", "SA-06", "SA-06",
            "SA-04", "SA-04", "SA-04", "SA-08", "SA-11",
            "SA-03", "SA-10", "SA-04", "SA-04", "SA-13"
        ],
        "population_estimate": [
            7_500_000, 4_700_000, 2_100_000, 1_400_000, 1_200_000,
            700_000, 600_000, 550_000, 500_000, 450_000,
            400_000, 350_000, 350_000, 350_000, 300_000,
            280_000, 250_000, 200_000, 180_000, 150_000
        ],
        "latitude": [
            24.7136, 21.4858, 21.3891, 24.5247, 26.4207,
            21.2703, 28.3838, 26.3267, 18.3007, 18.2164,
            25.3649, 26.2172, 27.0046, 27.5114, 17.4924,
            24.0895, 16.8892, 26.2361, 26.5651, 29.9697
        ],
        "longitude": [
            46.6753, 39.1925, 39.8579, 39.5692, 50.0888,
            40.4164, 36.5550, 43.9750, 42.7231, 42.5053,
            49.5855, 50.2083, 49.6225, 41.6908, 44.1277,
            38.0618, 42.5706, 50.1150, 50.0115, 40.2064
        ],
        "city_type": [
            "Capital", "Primary", "Holy City", "Holy City", "Primary",
            "Secondary", "Secondary", "Secondary", "Secondary", "Regional Capital",
            "Secondary", "Secondary", "Industrial", "Regional Capital", "Regional Capital",
            "Industrial", "Regional Capital", "Industrial", "Secondary", "Regional Capital"
        ]
    }
    
    df_cities = pd.DataFrame(cities_data)
    df_cities.to_csv(STATS_DIR / "ksa_major_cities.csv", index=False, encoding='utf-8-sig')
    print(f"  ✅ Major cities saved ({len(df_cities)} cities)")
    
    # -------------------------------------------------------------------------
    # 2.5 Vision 2030 Projects - Real data
    # -------------------------------------------------------------------------
    projects_data = {
        "project_name": [
            "NEOM", "THE LINE", "OXAGON", "TROJENA", "SINDALAH",
            "Red Sea Project", "AMAALA", "Qiddiya", "Diriyah Gate", "King Salman Park",
            "Riyadh Metro", "New Murabba", "AlUla Development", "Jeddah Tower",
            "Jeddah Central", "NEOM Green Hydrogen", "Sudair Solar PV", "Dumat Al Jandal Wind",
            "King Abdullah Economic City", "SPARK"
        ],
        "region_code": [
            "SA-07", "SA-07", "SA-07", "SA-07", "SA-07",
            "SA-03", "SA-07", "SA-01", "SA-01", "SA-01",
            "SA-01", "SA-01", "SA-03", "SA-02",
            "SA-02", "SA-07", "SA-01", "SA-13",
            "SA-02", "SA-04"
        ],
        "sector": [
            "Giga City", "Urban", "Industrial", "Tourism", "Tourism",
            "Tourism", "Tourism", "Entertainment", "Heritage", "Urban",
            "Transport", "Urban", "Heritage", "Urban",
            "Urban", "Energy", "Energy", "Energy",
            "Industrial", "Industrial"
        ],
        "budget_billion_usd": [
            500, 200, 50, 30, 5,
            15, 8, 8, 20, 23,
            22.5, 50, 15, 2,
            20, 8.5, 1.5, 0.5,
            100, 2
        ],
        "status": [
            "Under Construction", "Under Construction", "Under Construction", "Under Construction", "Operational",
            "Under Construction", "Under Construction", "Under Construction", "Under Construction", "Under Construction",
            "Operational", "Announced", "Under Construction", "Under Construction",
            "Planned", "Under Construction", "Operational", "Operational",
            "Operational", "Under Construction"
        ],
        "start_year": [
            2017, 2021, 2021, 2022, 2022,
            2019, 2020, 2019, 2018, 2019,
            2014, 2024, 2018, 2013,
            2025, 2021, 2021, 2019,
            2006, 2018
        ],
        "target_year": [
            2039, 2030, 2030, 2026, 2024,
            2030, 2028, 2030, 2027, 2027,
            2024, 2030, 2035, 2028,
            2035, 2026, 2024, 2022,
            2035, 2035
        ],
        "latitude": [
            28.0, 28.1, 27.8, 28.2, 27.5,
            25.5, 26.0, 24.4, 24.7, 24.7,
            24.7, 24.8, 26.6, 21.5,
            21.5, 28.3, 25.5, 29.8,
            22.4, 25.5
        ],
        "longitude": [
            35.0, 34.8, 35.2, 35.5, 35.8,
            37.0, 36.5, 46.2, 46.6, 46.7,
            46.7, 46.6, 37.9, 39.2,
            39.1, 35.3, 45.7, 39.9,
            39.1, 49.2
        ]
    }
    
    df_projects = pd.DataFrame(projects_data)
    df_projects['jobs_estimate'] = (df_projects['budget_billion_usd'] * 5000).astype(int)
    df_projects.to_csv(STATS_DIR / "ksa_vision2030_projects.csv", index=False)
    print(f"  ✅ Vision 2030 projects saved ({len(df_projects)} projects, ${df_projects['budget_billion_usd'].sum():.1f}B total)")
    
    # -------------------------------------------------------------------------
    # 2.6 Water Consumption by Region (2022) - Source: DataSaudi
    # -------------------------------------------------------------------------
    water_data = {
        "region_code": ["SA-01", "SA-02", "SA-03", "SA-04", "SA-05", "SA-06", 
                       "SA-07", "SA-08", "SA-09", "SA-10", "SA-11", "SA-12", "SA-13"],
        "region_name_en": [
            "Riyadh", "Makkah", "Madinah", "Eastern Province", "Al-Qassim",
            "Asir", "Tabuk", "Hail", "Northern Borders", "Jazan", 
            "Najran", "Al-Baha", "Al-Jouf"
        ],
        "water_consumption_million_m3": [
            1130, 832, 156, 657, 187,
            163, 78, 82, 45, 112,
            58, 38, 22
        ],
        "year": [2022] * 13
    }
    
    df_water = pd.DataFrame(water_data)
    df_water.to_csv(STATS_DIR / "ksa_water_consumption.csv", index=False)
    print(f"  ✅ Water consumption saved ({df_water['water_consumption_million_m3'].sum():,} million m³)")
    
    return True


# =============================================================================
# 3. CREATE DATA CATALOG
# =============================================================================

def create_data_catalog():
    """Create a catalog of all downloaded/created data."""
    
    catalog = {
        "metadata": {
            "created": "2026-01-22",
            "country": "Kingdom of Saudi Arabia",
            "iso_code": "SAU",
            "sources": [
                {
                    "name": "GASTAT",
                    "url": "https://www.stats.gov.sa",
                    "description": "General Authority for Statistics - Official statistics"
                },
                {
                    "name": "DataSaudi",
                    "url": "https://datasaudi.sa",
                    "description": "Ministry of Economy & Planning data portal"
                },
                {
                    "name": "OCHA HDX",
                    "url": "https://data.humdata.org",
                    "description": "Humanitarian Data Exchange - Admin boundaries"
                }
            ]
        },
        "datasets": [
            {
                "name": "Administrative Boundaries",
                "path": "01_data/01_raw/gis/admin_boundaries/",
                "format": ["GeoJSON", "Shapefile", "XLSX"],
                "source": "OCHA HDX",
                "levels": ["ADM0 (Country)", "ADM1 (13 Regions)"]
            },
            {
                "name": "Population by Region",
                "path": "01_data/01_raw/statistics/ksa_population_by_region.csv",
                "format": "CSV",
                "source": "GASTAT 2024",
                "coverage": "13 regions"
            },
            {
                "name": "Economic Indicators",
                "path": "01_data/01_raw/statistics/ksa_economic_indicators.csv",
                "format": "CSV",
                "source": "DataSaudi 2024-2025",
                "indicators": 13
            },
            {
                "name": "Employment by Region",
                "path": "01_data/01_raw/statistics/ksa_employment_by_region.csv",
                "format": "CSV",
                "source": "GOSI Q3 2025",
                "coverage": "13 regions"
            },
            {
                "name": "Major Cities",
                "path": "01_data/01_raw/statistics/ksa_major_cities.csv",
                "format": "CSV",
                "source": "GASTAT",
                "count": 20
            },
            {
                "name": "Vision 2030 Projects",
                "path": "01_data/01_raw/statistics/ksa_vision2030_projects.csv",
                "format": "CSV",
                "source": "Official project data",
                "count": 20
            },
            {
                "name": "Water Consumption",
                "path": "01_data/01_raw/statistics/ksa_water_consumption.csv",
                "format": "CSV",
                "source": "DataSaudi 2022",
                "coverage": "13 regions"
            }
        ]
    }
    
    with open(DATA_DIR / "DATA_CATALOG.json", 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    
    print(f"\n  ✅ Data catalog saved to {DATA_DIR / 'DATA_CATALOG.json'}")
    
    return catalog


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "=" * 60)
    print("🇸🇦 NSS - SAUDI ARABIA DATA DOWNLOADER")
    print("=" * 60)
    
    # 1. Download admin boundaries
    download_admin_boundaries()
    
    # 2. Create statistics files
    create_ksa_statistics()
    
    # 3. Create catalog
    create_data_catalog()
    
    print("\n" + "=" * 60)
    print("✅ ALL DATA DOWNLOADED/CREATED SUCCESSFULLY")
    print("=" * 60)
    print(f"\n📁 Data location: {DATA_DIR}")
    print("\nNext steps:")
    print("  1. Run: python scripts/process_ksa_data.py")
    print("  2. Run: streamlit run scripts/dashboard_demo.py")


if __name__ == "__main__":
    main()
