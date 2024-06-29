from flask import Flask, render_template, request, jsonify  # Importing required Flask modules
import pandas as pd  # Importing pandas library to work with data frames
import json  # Importing json library to work with JSON data
import plotly.graph_objs as go  # Importing Plotly's graph objects for creating plots
import math  # Importing math library for mathematical operations
from flask import Flask, render_template  # Importing Flask and render_template (redundant line)
import pandas as pd  # Importing pandas (redundant line)
import plotly.graph_objs as go  # Importing Plotly's graph objects (redundant line)
app = Flask(__name__)  # Creating a Flask application instance

# Function to create plot
def create_plot(x_values, y_values, names, title, y_title, colors):
    fig = go.Figure()  # Creating a new Plotly figure
    for i, (y, name) in enumerate(zip(y_values, names)):  # Looping through y-values and names
        fig.add_trace(go.Scatter(x=x_values, y=y, mode='lines', fill='tozeroy', name=name, line=dict(color=colors[i])))  # Adding a trace (line plot) to the figure
    fig.update_layout(title=title, xaxis_title='Year', yaxis_title=y_title)  # Updating the layout with title and axis labels
    return fig  # Returning the figure

# Define routes for each plot


app = Flask(__name__)  # Creating a Flask application instance (redundant line)

csv_data = pd.read_csv("./static/data.csv")  # Reading data from a CSV file

with open("country_info.json", "r") as f:  # Opening a JSON file
    country_info = json.load(f)  # Loading the JSON data

@app.route('/')  # Defining a route for the root URL
def basic():
    return render_template('land.html')  # Rendering the 'i.html' template
@app.route('/vis')  # Defining a route for the root URL
def basicf():
    return render_template('vis.html')  # Rendering the 'i.html' template
@app.route('/watch_temperature_video', methods=['POST'])  # Defining a route for '/watch_temperature_video' with POST method
def watch_temperature_video():
    return render_template('temp.html')  # Rendering the 'temp.html' template

@app.route('/watch_sea_level_video', methods=['GET', 'POST'])  # Defining a route for '/watch_sea_level_video' with GET and POST methods
def watch_sea_level_video():
    return render_template('g.html')  # Rendering the 'sea_level.html' template

@app.route('/render_chart_html', methods=['POST'])  # Defining a route for '/render_chart_html' with POST method
def index():
    # Get unique country names with their information
    countries = [{"code": code, "name": info["name"], "flag": info["flag"], "facts": info["facts"]}
                 for code, info in country_info.items()]  # Creating a list of dictionaries with country information
    return render_template('index.html', countries=countries)  # Rendering the 'index.html' template and passing the countries data

@app.route('/get_data', methods=['POST'])  # Defining a route for '/get_data' with POST method
def get_data():
    selected_country = request.form['country']  # Getting the selected country from the form data
    print(selected_country)  # Printing the selected country
    # Filter data for the selected country
    # Prepare data for scatter plot
    country_data = csv_data[
        (csv_data["area (ISO3)"] == selected_country) &
        (csv_data["unit"] == "CO2 * gigagram / a") &
        (csv_data["category (IPCC2006_PRIMAP)"] == "1.A") &
        (csv_data["entity"] == "CO2") &
        (csv_data["scenario (PRIMAP-hist)"] == "HISTCR")
    ]  # Filtering the CSV data based on country and other conditions
    # Extract years and corresponding CO2 emission values
    years = []  # List to store years
    values = []  # List to store CO2 emission values
    for column in country_data.columns[7:]:  # Looping through columns starting from the 8th column
        year = int(column)  # Converting column name (assumed to be year) to integer
        value = country_data[column].iloc[0]  # Getting the CO2 emission value (assuming one row per country)
        if (math.isnan(value)):  # Checking if the value is NaN (Not a Number)
            value = 0  # Setting the value to 0 if it's NaN
        years.append(year)  # Adding the year to the years list
        values.append(value)  # Adding the CO2 emission value to the values list
    return jsonify({"years": years, "values": values})  # Returning the years and values as JSON

def get_data():
    df1 = pd.read_csv("seaice.csv")  # Reading data from a CSV file
    df2 = pd.read_csv("GlobalTemperatures.csv")  # Reading data from another CSV file
    years = list(range(1978, 2014))  # Creating a list of years from 1978 to 2013
    extents = []  # List to store extents
    temperatures = []  # List to store temperatures

    for year in years:
        mean_extent = df1[df1["Year"] == year]["     Extent"].mean()  # Calculating mean extent for the given year
        mean_temperature = df2[df2['dt'].str.startswith(str(year))]["LandAverageTemperature"].mean()  # Calculating mean temperature for the given year
        extents.append(mean_extent)  # Adding mean extent to the extents list
        temperatures.append(mean_temperature)  # Adding mean temperature to the temperatures list

    return years, extents, temperatures  # Returning years, extents, and temperatures

@app.route('/extent', methods=['POST'])  # Defining a route for '/extent' with POST method
def extent():
    years, extents, temperatures = get_data()  # Getting data from the get_data function

    trace1 = {
        'x': years,
        'y': extents,
        'mode': 'lines+markers',  # Changed mode to include markers
        'name': 'Extent'
    }  # Creating a trace (line plot with markers) for extents
    trace2 = {
        'x': years,
        'y': temperatures,
        'mode': 'lines+markers',  # Changed mode to include markers
        'name': 'Temperature'
    }  # Creating a trace (line plot with markers) for temperatures
    trace3 = {
        'x': temperatures,
        'y': extents,
        'mode': 'lines+markers',
        'name': 'Third Data'
    }

    chart_data = {
        'data': [trace1, trace2,trace3],
        'layout': [{
            'title': '',
            'xaxis': {'title': 'Year'},
            'yaxis1': {'title': 'Extent'},
        },
        {
            'title': '',
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': 'Temperature'}
        },
        {
            'title': '',
            'xaxis': {'title': 'Temperature'},
            'yaxis': {'title': 'Extent'}
        }]
    }  # Creating a dictionary to hold the chart data (traces and layout)

    return render_template('chart.html', chart_data=json.dumps(chart_data))  # Rendering the 'chart.html' template and passing the chart data as JSON

@app.route('/heat', methods=['POST'])  # Defining a route for '/heat' with POST method
def heat():
    return render_template('chorloplet.html')  # Rendering the 'heat.html' template

@app.route('/bar-race', methods=['POST', 'GET'])  # Defining a route for '/india-area' with POST and GET methods
def area():
    # Render the template with the plots
    return render_template('bar-race.html')  # Rendering the 'hello.html' template and passing the plots as HTML
@app.route('/sunburst', methods=['POST', 'GET'])  # Defining a route for '/india-area' with POST and GET methods
def sunburst():
    # Render the template with the plots
    return render_template('h.html')  # Rendering the 'h.html' template and passing the plots as HTML
@app.route('/bubble', methods=['POST', 'GET'])  # Defining a route for '/india-area' with POST and GET methods
def bubble():
    # Render the template with the plots
    return render_template('k.html')  # Rendering the 'h.html' template and passing the plots as HTML
@app.route('/temp', methods=['POST', 'GET'])  # Defining a route for '/india-area' with POST and GET methods
def temp():
    # Render the template with the plots
    return render_template('j.html')  # Rendering the 'h.html' template and passing the plots as HTML
if __name__ == '__main__':
    app.run(debug=True)  # Running the Flask application in debug mode
