import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import simplejson

#initialize db
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#create references
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#Flask app
app = Flask(__name__)

#Start Routes
@app.route("/")
def welcome():
    #List all available api routes.
    return (
        f"Available Routes:<br/>"
        
        f"/api/v1.0/precipitation<br/>"
        f"Returns dates and temperature from last year.<br><br>"
        
        f"/api/v1.0/stations<br/>"
        f"Returns a json list of stations. <br><br>"
        
        f"/api/v1.0/tobs<br/>"
        f"Returns list of Temperature observations(tobs) for previous year. <br><br>"

        f"/api/v1.0/<start><br/>"
        f"Returns an Avg, Max, Min temps for start date. <br><br>"
        
        f"/api/v1.0/<start>/<end><br/>"
        f"Returns Avg, Max, Min tems for a date range"
    )
    #def precip route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """create dictionary of value and return JSON""" 
    
    last_yr = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-24").all()

    # creates JSONified list
    prcp_list = [last_yr]

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    stat_name = session.query(Station.name, Station.station).all()
    #JSONIFY list
    stat_list=[]
    for stat in stat_name:
         row = {}
         row['name'] = stat[0]
         row['station'] = stat[1]
         stat_list.append(row)
    return jsonify(stat_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of tobs for the previous year"""
    temp_obs = session.query(Station.name, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-24").all()

    # creates JSONified list of dictionaries
    tobs_list = []
    for temp_obs in temp_obs:
        row = {}
        row["Station"] = temp_obs[0]
        row["Date"] = temp_obs[1]
        row["Temperature"] = (temp_obs[2])
        tobs_list.append(row)

    return jsonify(tobs_list)

@app.route('/api/v1.0/<date>/')
def given_date(date):
    """Return the average temp, max temp, and min temp for the date"""
    temp_data = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= '2016-08-24').all()

    # creates JSONified list of dictionaries
    temp_list = []
    for temp_data in temp_data:
        row = {}
        row['Start Date'] = date
        row['End Date'] = '2017-08-23'
        row['Average Temperature'] = (temp_data[0])
        row['Highest Temperature'] = (temp_data[1])
        row['Lowest Temperature'] = (temp_data[2])
        temp_list.append(row)

    return jsonify(temp_list)

@app.route('/api/v1.0/<start_date>/<end_date>/')
def query_dates(start_date, end_date):
    """Return the avg, max, min, temp over a specific time period"""
    temp_time_range = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    # creates JSONified list of dictionaries
    data_list = []
    for temp_time_range in temp_time_range:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Average Temperature"] = float(temp_time_range[0])
        row["Highest Temperature"] = float(temp_time_range[1])
        row["Lowest Temperature"] = float(temp_time_range[2])
        data_list.append(row)
    return jsonify(data_list)



if __name__ == '__main__':
    app.run(debug=True)