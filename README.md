# sqlalchemy-challenge
Climate analysis and data exploration - University of Birmingham Assignment

## Climate Analysis and Exploration
I have used Python, SQLAlchemy’s create_engine & ORM queries, Pandas, and Matplotlib to perform [climate analysis](climate_analysis.ipynb) and data exploration of a provided climate database (hawaii.sqlite). 

### Precipitation Analysis
what is included in the analysis of precipitation in the area:


* The most recent date in the dataset.

* Using this date, I have retrieved the previous 12 months of precipitation data by querying the 12 previous months of data. 

* Select only the date and prcp values.

* Load the query results into a Pandas DataFrame, and set the index to the date column.

* Sort the DataFrame values by date.

* Plots with the results


### Station Analysis

To perform an analysis of stations in the area, I have designed:


* A query to calculate the total number of stations in the dataset.

* A query to find the most active stations (the stations with the most rows) 

* I have used functions such as func.min, func.max, func.avg, and func.count.

* A query to retrieve the previous 12 months of temperature observation data (TOBS).


## Climate Flask App

I have designed a Flask API based on the queries that I have developed.

[Flask](app.py) routes:

* /
Homepage.
List all available routes.

* /api/v1.0/precipitation

* /api/v1.0/stations

* /api/v1.0/tobs
Query the dates and temperature observations of the most active station for the previous year of data.

* /api/v1.0/start and /api/v1.0/start/end
Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.

