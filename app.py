import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"#####################################################################################<br/>"
        f"Welcome to Surfs Up Page - Hawai'i Climate API<br/>"
        f"Data available from 2010-01-01 to 2017-08-23<br/>"
        f"#####################################################################################<br/>"
        f"Available Routes:<br/>"
        f"1. /api/v1.0/precipitation<br/>"
        f"* Return a list of all precipitation data<br/>"
        f"-------------------------------------------------------------------------------------------------------------------------------<br/>"
        f"2. /api/v1.0/stations<br/>"
        f"* Return a list of all station data<br/>"
        f"-------------------------------------------------------------------------------------------------------------------------------<br/>"
        f"3. /api/v1.0/tobs<br/>"
        f"* Dates and temperature observations of the most acive station for the last year of data<br/>"
        f"-------------------------------------------------------------------------------------------------------------------------------<br/>"
        f"4. /api/v1.0/<startDate><br/>"
        f"* Data Search: For data search from a specific start date, enter date, yyyy-mm-dd, after /api/v1.0/<br/>"
        f"-------------------------------------------------------------------------------------------------------------------------------<br/>"
        f"5. /api/v1.0/<startDate>/<endDate><br/>"
        f"* Data Search: For data search for specific start & end dates, enter yyyy-mm-dd/yyyy-mm-dd<br/>"
        f"#####################################################################################<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of all precipitation data"""
    # Query precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    
    # Convert the query results to a dictionary using date as the key and prcp as the value
    results_dict = {}
    for result in results:
        results_dict[result[0]] = result[1]

    return jsonify(results_dict)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of all Station data"""
    # Query precipitation data
    results = session.query(Station.station, Station.name).all()
    
    session.close()
    
    # Create a dictionary from the row data and append to a list of datasets
    stationData = []
    for station, name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        stationData.append(station_dict)

    return jsonify(stationData)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of all precipitation data"""
    # Query dates and temperature observations of the most acive station for the last year of data
    
    ## First, set up an yearBefore day
    max_date = session.query(func.max(Measurement.date)).all()
    max_date_string = max_date[0][0]
    maxDate = dt.datetime.strptime(max_date_string, '%Y-%m-%d')
    maxYear = int(dt.datetime.strftime(maxDate, '%Y'))
    maxMonth = int(dt.datetime.strftime(maxDate, '%m'))
    maxDay = int(dt.datetime.strftime(maxDate, '%d'))
    year_before = dt.date(maxYear, maxMonth, maxDay) - dt.timedelta(days = 365)
    yearBefore = dt.datetime.strftime(year_before, '%Y-%m-%d')
    
    ## Second, find an active station
    active_station = session.query(Measurement.station, func.count(Measurement.station)).\
                    group_by(Measurement.station).\
                    order_by(func.count(Measurement.station).desc()).all()
    
    activeStation =  active_station[0][0]         
    
    results = session.query(Measurement.date, Measurement.tobs, Measurement.station).\
                filter(Measurement.date > yearBefore).\
                filter(Measurement.station == activeStation).all()
    
    session.close()
    
    # Create a dictionary from the row data and append to a list of datasets
    tobsData = []
    for result in results:
        tobsDict = {}
        tobsDict = {result.date: result.tobs, "Station": result.station}
        tobsData.append(tobsDict)
    
    return jsonify(tobsData)

@app.route("/api/v1.0/<startDate>")
def start(startDate):
    # Return a JSON list of the min Temperature, avg Temperature, and max Temperature
    # for a given start. When given the start only, calculate those data for all dates
    # greater than and equal to the start date.

    session = Session(engine)
    
    # Query start day
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(func.strftime("%Y-%m-%d", Measurement.date) >=startDate).\
                group_by(Measurement.date).all()

    session.close()

    return_list = []
    for date, tmin, tavg, tmax in results:
        dateDict = {}
        dateDict["date"] = date
        dateDict["Low Temp"] = tmin
        dateDict["Avg Temp"] = tavg
        dateDict["High Temp"] = tmax
        return_list.append(dateDict)
    
    return jsonify(return_list)

@app.route("/api/v1.0/<startDate>/<endDate>")
def startEnd(startDate, endDate):
    # Return a JSON list of the min Temperature, avg Temperature, and max Temperature
    # for given start and end dates. When given the start and end date, calculate those data for all dates
    # between the start and end date inclusive. 

    session = Session(engine)
    
    # Query start and end day for climate data
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(func.strftime("%Y-%m-%d", Measurement.date) >=startDate).\
                filter(func.strftime("%Y-%m-%d", Measurement.date) <=endDate).\
                group_by(Measurement.date).all()

    session.close()

    return_list = []
    for date, tmin, tavg, tmax in results:
        dateDict = {}
        dateDict["date"] = date
        dateDict["Low Temp"] = tmin
        dateDict["Avg Temp"] = tavg
        dateDict["High Temp"] = tmax
        return_list.append(dateDict)
    
    return jsonify(return_list)

if __name__ == "__main__":
    app.run(debug=True)
