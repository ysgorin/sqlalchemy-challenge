# Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
import numpy as np

# Database Setup

# create engine to hawaii.sqlite
path = "../Resources/hawaii.sqlite"
engine = create_engine("sqlite:///" + path)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
precipitation = Base.classes.measurement
station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
# Homepage
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
    )
# Precipitation
@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Last 12 Months of Precipitation Data"""
    # Query last 12 months of precipitation data
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(precipitation.date, precipitation.prcp).\
    filter(precipitation.date >= query_date)

    session.close()

    # Convert query results into a dictionary
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['precipitation'] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

# Stations
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """List of Stations"""
    # Query list of stations
    results = session.query(station.station).\
    group_by(station.station).all()

    session.close()
    # Convert query into list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# Temperature Observations
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Last 12 Months of Temperature Data for Station 'USC00519281'"""
    # Query last 12 months of temperature data for most active station 'USC00519281'
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(precipitation.tobs).\
    filter(precipitation.station == 'USC00519281', precipitation.date >= query_date)

    session.close()
    # Convert query into list
    tobs_list = list(np.ravel(results))

    return jsonify(tobs_list)

if __name__ == '__main__':
    app.run(debug=True)

