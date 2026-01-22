# Data Layer - GIS Layers
This folder contains geospatial data layers.

## Primary Format
- **GeoPackage (.gpkg)** - Primary format for all vector data
- **GeoTIFF (.tif)** - For raster data

## Structure
```
gis/
├── administrative/   # Admin boundaries
├── demographics/     # Population layers
├── economic/         # Economic zones, projects
├── infrastructure/   # Transport, utilities
├── environment/      # Land cover, protected areas
├── analysis/         # Derived analytical layers
└── scenarios/        # Scenario-specific outputs
```

## Naming Convention
`{domain}_{layer_name}_{year}_{version}.gpkg`

Example: `demographics_population_2024_v1.gpkg`
