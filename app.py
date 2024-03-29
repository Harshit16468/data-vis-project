from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import plotly.graph_objs as go
import math
from flask import Flask, render_template
import pandas as pd
import plotly.graph_objs as go

app = Flask(__name__)

# Function to create plot
def create_plot(x_values, y_values, names, title, y_title, colors):
    fig = go.Figure()
    for i, (y, name) in enumerate(zip(y_values, names)):
        fig.add_trace(go.Scatter(x=x_values, y=y, mode='lines', fill='tozeroy', name=name, line=dict(color=colors[i])))
    fig.update_layout(title=title, xaxis_title='Year', yaxis_title=y_title)
    return fig

# Define routes for each plot


app = Flask(__name__)

csv_data = pd.read_csv("data.csv")

with open("country_info.json", "r") as f:
    country_info = json.load(f)

@app.route('/')
def basic():
    return render_template('i.html')

@app.route('/watch_temperature_video', methods=['POST'])
def watch_temperature_video():
    return render_template('temp.html')

@app.route('/watch_sea_level_video', methods=['GET', 'POST'])
def watch_sea_level_video():
    return render_template('sea_level.html')


@app.route('/render_chart_html', methods=['POST'])
def index():
    # Get unique country names with their information
    countries = [{"code": code, "name": info["name"], "flag": info["flag"], "facts": info["facts"]} 
                 for code, info in country_info.items()]
    return render_template('index.html', countries=countries)

@app.route('/get_data', methods=['POST'])
def get_data():
    selected_country = request.form['country']
    print(selected_country)
    # Filter data for the selected country
    # Prepare data for scatter plot
    country_data = csv_data[
        (csv_data["area (ISO3)"] == selected_country) &
        (csv_data["unit"] == "CO2 * gigagram / a") &
        (csv_data["category (IPCC2006_PRIMAP)"] == "1.A") &
        (csv_data["entity"] == "CO2") &
        (csv_data["scenario (PRIMAP-hist)"] == "HISTCR")
    ]
    # Extract years and corresponding CO2 emission values
    years = []
    values = []
    for column in country_data.columns[7:]:  # Assuming CO2 emission data starts from 8th column
        year = int(column)  # Convert column name to integer (assuming it represents a year)
        value = country_data[column].iloc[0]  # Assuming there's only one row for the selected country
        if (math.isnan(value)):
            value=0
        years.append(year)
        values.append(value)
    return jsonify({"years": years, "values": values})


def get_data():
    df1 = pd.read_csv("seaice.csv")
    df2 = pd.read_csv("GlobalTemperatures.csv")
    years = list(range(1978, 2014))
    extents = []
    temperatures = []

    for year in years:
        mean_extent = df1[df1["Year"] == year]["     Extent"].mean()
        mean_temperature = df2[df2['dt'].str.startswith(str(year))]["LandAverageTemperature"].mean()
        extents.append(mean_extent)
        temperatures.append(mean_temperature)

    return years, extents, temperatures

@app.route('/extent', methods=['POST'])
def extent():
    years, extents, temperatures = get_data()

    trace1 = {
        'x': years,
        'y': extents,
        'mode': 'lines+markers',  # Changed mode to include markers
        'name': 'Extent'
    }
    trace2 = {
        'x': years,
        'y': temperatures,
        'mode': 'lines+markers',  # Changed mode to include markers
        'name': 'Temperature'
    }

    chart_data = {
	    'data': [trace1, trace2],
	    'layout': [{
		'title': '',
		'xaxis': {'title': 'Year'},
		'yaxis1': {'title': 'Extent'},
	    },
	   {
		'title': '',
		'xaxis': {'title': 'Year'},
		'yaxis': {'title': 'Temperature'}
	    }]
	}

    return render_template('chart.html', chart_data=json.dumps(chart_data))

@app.route('/heat', methods=['POST'])
def heat():
    return render_template('heat.html')
@app.route('/india-area',methods=['POST','GET'])
def area():
    # Read data from CSV files
    df1 = pd.read_csv('TEMP_ANNUAL_SEASONAL_MEAN.csv')
    df2 = pd.read_csv('RF_AI_1901-2021.csv')

    # Define names and colors for each line
    names1 = ['ANNUAL', 'JAN-FEB', 'MAR-MAY', 'JUN-SEP', 'OCT-DEC']
    colors1 = ['#0000FF', '#00FF00', '#FF0000', '#FFA500', '#000000']  # Colored lines
    names2 = ['JUN', 'JUL', 'AUG', 'SEP', 'JUN-SEP']
    colors2 = ['#0000FF', '#00FF00', '#FF0000', '#FFA500', '#000000']  # Colored lines
    names3 = ['ANNUAL', 'JAN-FEB', 'MAR-MAY', 'JUN-SEP', 'OCT-DEC']
    colors3 = ['#333333', '#666666', '#999999', '#CCCCCC', '#DDDDDD']  # Different shades of gray
    names4 = ['JUN', 'JUL', 'AUG', 'SEP', 'JUN-SEP']
    colors4 = ['#333333', '#666666', '#999999', '#CCCCCC', '#DDDDDD']  # Different shades of gray

    # Create plots
    plot1 = create_plot(df1['YEAR'], 
                        [df1['ANNUAL'], df1['JAN-FEB'], df1['MAR-MAY'], df1['JUN-SEP'], df1['OCT-DEC']],
                        names1,
                        'Temperature (Colored)',
                        'Temperature(in degree celcius)',
                        colors1)
    plot2 = create_plot(df2['YEAR'], 
                        [df2['JUN'], df2['JUL'], df2['AUG'], df2['SEP'], df2['JUN-SEP']],
                        names2,
                        'Rainfall (Colored)',
                        'Rainfall in mm',
                        colors2)
    plot3 = create_plot(df1['YEAR'], 
                        [df1['ANNUAL'], df1['JAN-FEB'], df1['MAR-MAY'], df1['JUN-SEP'], df1['OCT-DEC']],
                        names3,
                        'Temperature (Grayscale)',
                        'Temperature(in degree celcius)',
                        colors3)
    plot4 = create_plot(df2['YEAR'], 
                        [df2['JUN'], df2['JUL'], df2['AUG'], df2['SEP'], df2['JUN-SEP']],
                        names4,
                        'Rainfall (Grayscale)',
                        'Rainfall in mm',
                        colors4)

    # Convert plots to HTML
    plot1_div = plot1.to_html(full_html=False)
    plot2_div = plot2.to_html(full_html=False)
    plot3_div = plot3.to_html(full_html=False)
    plot4_div = plot4.to_html(full_html=False)

    # Render the template with the plots
    return render_template('hello.html', plot1_div=plot1_div, plot2_div=plot2_div, plot3_div=plot3_div, plot4_div=plot4_div)
if __name__ == '__main__':
    app.run(debug=True)
