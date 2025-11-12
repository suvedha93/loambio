import pandas as pd
import json
import geopandas as gpd
from shapely.geometry import shape

# Read GeoJSON file directly using GeoPandas
gdf = gpd.read_file('sample_paddocks.geojson')

# If 'Project__Name' and 'id' are not top-level columns, extract from 'properties'
if 'Project__Name' not in gdf.columns or 'id' not in gdf.columns:
    gdf['project_name'] = gdf['properties'].apply(lambda x: x.get('Project__Name') if isinstance(x, dict) else None)
    gdf['paddock_id'] = gdf['properties'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
else:
    gdf['project_name'] = gdf['Project__Name']
    gdf['paddock_id'] = gdf['id']

gdf.head()

# Clean and standardize columns
print(gdf)
gdf['project_name'] = gdf['project_name'].astype(str).str.strip().str.lower()
gdf['project_name'] = gdf['project_name'].replace({'', 'none', 'nan', 'null'}, 'unknown_project')
gdf['paddock_id'] = gdf['paddock_id'].astype(str).str.strip()
gdf = gdf[gdf['geometry'].notnull()]
gdf.head()

# Validate and filter geometries using GeoPandas built-in features
gdf = gdf[gdf['geometry'].notnull() & gdf.is_valid]
gdf.head()

# calculate area in hectares
gdf['area_ha'] = gdf['area_acres'] / 10000
gdf[['project_name', 'paddock_id', 'area_ha']].head()

# Save cleaned data to CSV
gdf[['project_name', 'paddock_id', 'area_ha', 'geometry']].to_csv('cleaned_paddocks.csv', index=False)
print('Cleaned paddock data saved to cleaned_paddocks.csv')

# Aggregate paddock count and total area by project
project_agg = gdf.groupby('project_name').agg(
    paddock_count=('paddock_id', 'count'),
    total_area_ha=('area_ha', 'sum'),
    paddock_ids=('paddock_id', lambda x: list(x)[:5])  # show up to 5 paddock IDs as a sample
).reset_index()

print(project_agg.sort_values('total_area_ha', ascending=False))
# Display the first few rows of the GeoDataFrame

import matplotlib.pyplot as plt

# Bar chart: total paddock area by project
fig, ax = plt.subplots(figsize=(10, 6))
project_agg_sorted = project_agg.sort_values('total_area_ha', ascending=False)
ax.bar(project_agg_sorted['project_name'], project_agg_sorted['total_area_ha'], color='skyblue')
ax.set_xlabel('Project Name')
ax.set_ylabel('Total Area (ha)')
ax.set_title('Total Paddock Area by Project')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()