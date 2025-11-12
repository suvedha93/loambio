# Paddock Data Processing and Analysis

This project processes and analyzes paddock (field) data from a GeoJSON file, cleans and standardizes the data, calculates paddock areas, and visualizes the results. The workflow is implemented in Python using GeoPandas and Matplotlib.

# What the Code Does

1. Read GeoJSON Data: Loads paddock geometries and properties from `sample_paddocks.geojson` using GeoPandas.
2. Extract and Clean Attributes: Ensures that each paddock has a `project_name` and `paddock_id`, extracting them from the `properties` field if necessary. Cleans and standardizes these columns.
3. Geometry Validation: Filters out paddocks with missing or invalid geometries.
4. Area Calculation: Calculates the area of each paddock in hectares. 
5. Save Cleaned Data: Exports the cleaned paddock data, including geometry and area, to `cleaned_paddocks.csv`.
6. Aggregate by Project: Groups paddocks by project, summarizing paddock count and total area per project.
7. Visualization: Plots a bar chart showing total paddock area by project using Matplotlib.

# How to Run

1. Ensure you have Python 3.x installed.
2. Place your `sample_paddocks.geojson` file in the same directory as the script.
3. The cleaned data will be saved as `cleaned_paddocks.csv`, and a bar chart will be displayed.


# Data Engineering Workflow with GCP Components

1. Cloud Storage (GCS)
   - Store raw GeoJSON files and cleaned CSV outputs.
   - Example: `gs://your-bucket/sample_paddocks.geojson`

2. Cloud Functions or Cloud Run
   - Deploy the data cleaning/transformation script (e.g., `paddock_data.py`) as a serverless function or container.
   - Trigger on new file uploads to GCS (event-driven pipeline).

3. BigQuery
   - Load cleaned CSV data into BigQuery for scalable analytics and SQL-based aggregation.
   - Example: Use BigQuery to further aggregate paddock data, join with other datasets, or build dashboards.

4. Airflow
   - For large-scale or streaming data processing, use Airflow to orchestrate ETL pipelines.
   - Can be used to automate the entire process from ingestion to transformation and loading into BigQuery.

5. Looker
   - Build dashboards and visualizations directly from BigQuery tables for business users.
