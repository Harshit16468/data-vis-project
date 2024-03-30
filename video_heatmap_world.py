import plotly.graph_objects as go  # Importing Plotly's graph objects for creating plots
import pandas as pd  # Importing the pandas library for working with data frames
import json  # Importing the json library for working with JSON data
import os  # Importing the os library for working with files and directories
from tqdm import tqdm  # Importing the tqdm library for displaying progress bars

# Load CSV data
csv_data = pd.read_csv("data.csv")  # Reading the CSV data into a DataFrame

# Load GeoJSON data
with open("countries.geo.json", "r") as f:
    geojson_data = json.load(f)  # Loading the GeoJSON data

# Iterate over each feature in geojson_data
for year in tqdm(range(1800, 2023)):  # Iterating over years from 1800 to 2022 with a progress bar
    fig = go.Figure()  # Creating a new Plotly figure
    zmax = 0  # Initializing the maximum value for setting the colorbar range

    for feature in geojson_data["features"]:
        country_id = feature["id"]  # Getting the country ID

        # Filtering the CSV data for the current country and year
        country_data = csv_data[(csv_data["area (ISO3)"] == country_id) &
                                (csv_data["unit"] == "CO2 * gigagram / a") &
                                (csv_data["category (IPCC2006_PRIMAP)"] == "1.A") &
                                (csv_data[str(year)].notnull())]  # Check if data for the year exists

        if not country_data.empty:  # If data exists for the country and year
            property_value = country_data[str(year)].iloc[0]  # Getting the property value (CO2 emissions)
            if zmax < property_value:  # Updating the maximum value if the current value is larger
                zmax = property_value

    # Iterate over each feature again to assign property values
    for feature in geojson_data["features"]:
        country_id = feature["id"]
        country_data = csv_data[(csv_data["area (ISO3)"] == country_id) &
                                (csv_data["unit"] == "CO2 * gigagram / a") &
                                (csv_data["category (IPCC2006_PRIMAP)"] == "1.A") &
                                (csv_data[str(year)].notnull())]  # Check if data for the year exists

        if not country_data.empty:
            property_value = country_data[str(year)].iloc[0]
            feature["properties"]["value"] = property_value  # Assigning the property value to the GeoJSON feature
        else:
            property_value = 0
            feature["properties"]["value"] = property_value  # Assigning 0 if no data exists

    # Create directory to save figures
    if not os.path.exists("fig"):
        os.makedirs("fig")  # Creating the 'fig' directory if it doesn't exist

    # Add a heatmap trace
    fig.add_trace(go.Choropleth(
        geojson=feature,  # GeoJSON data
        locations=[country_id],  # List of country IDs
        z=[property_value],  # List of property values (CO2 emissions)
        colorscale="Greys",  # Grayscale colorscale while for colored have colorscale="YlOrRd"
        zmin=0,  # Minimum value for the colorbar
        zmax=zmax,  # Maximum value for the colorbar
        colorbar=dict(title="CO2 Emissions (gigagram / a)")  # Colorbar title
    ))

    # Update layout with rotation
    fig.update_layout(
        title=f"CO2 Emissions Heatmap by Country ({year})",  # Plot title with the year
        geo=dict(
            showframe=False,  # Hide the frame
            showcoastlines=False,  # Hide the coastlines
            projection_type="equirectangular",  # Projection type
            projection_rotation=dict(lon=30, lat=0)  # Rotation of the projection
        )
    )

    # Save the figure
    fig.write_image(f"fig/_{year}.png")  # Saving the figure as a PNG file in the 'fig' directory

# Now, you have all the figures saved. You can use these to create a video.
# run this command on terminal ffmpeg -r 24 -f image2 -s 1200x800 -i fig/_%d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p co2_emissions_heatmap.mp4
