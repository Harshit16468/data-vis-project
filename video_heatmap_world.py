import plotly.graph_objects as go
import pandas as pd
import json
import os
from tqdm import tqdm
# Load CSV data
csv_data = pd.read_csv("data.csv")

# Load GeoJSON data
with open("countries.geo.json", "r") as f:
    geojson_data = json.load(f)

# Initialize figure

# Find maximum property value for setting zmax


# Iterate over each feature in geojson_data
for year in tqdm(range(1800, 2023)):  # Iterate over years
    fig = go.Figure()
    zmax=0
    for feature in geojson_data["features"]:
        country_id = feature["id"]

        country_data = csv_data[(csv_data["area (ISO3)"] == country_id) & 
                                (csv_data["unit"] == "CO2 * gigagram / a") & 
                                (csv_data["category (IPCC2006_PRIMAP)"] == "1.A") &
                                (csv_data[str(year)].notnull())]  # Check if data for the year exists

        if not country_data.empty:
            property_value = country_data[str(year)].iloc[0]
            if zmax < property_value:
                zmax = property_value
    for feature in geojson_data["features"]:
            country_id = feature["id"]
            country_data = csv_data[(csv_data["area (ISO3)"] == country_id) & 
                                    (csv_data["unit"] == "CO2 * gigagram / a") & 
                                    (csv_data["category (IPCC2006_PRIMAP)"] == "1.A") &
                                    (csv_data[str(year)].notnull())]  # Check if data for the year exists
            if not country_data.empty:
                property_value = country_data[str(year)].iloc[0]
                feature["properties"]["value"] = property_value
            else:
                property_value=0
                feature["properties"]["value"] = property_value

                # Create directory to save figures
            if not os.path.exists("fig"):
                os.makedirs("fig")

                # Initialize figure

                # Add a heatmap trace
            fig.add_trace(go.Choropleth(
                geojson=feature,
                locations=[country_id],
                z=[property_value],
                # colorscale="YlOrRd",
                colorscale="Greys",
                zmin=0,
                zmax=zmax,
                colorbar=dict(title="CO2 Emissions (gigagram / a)")
            ))

            # Update layout with rotation
            fig.update_layout(
                title=f"CO2 Emissions Heatmap by Country ({year})",
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection_type="equirectangular",
                    projection_rotation=dict(lon=30, lat=0)
                )
            )

                # Save the figure
    fig.write_image(f"fig/_{year}.png")

# Now, you have all the figures saved. You can use these to create a video.
