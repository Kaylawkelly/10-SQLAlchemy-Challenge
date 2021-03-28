#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 10:04:16 2021

@author: kay
"""

import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/pi/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_ago).\
    order_by(Measurement.date).all()

    prcp_dict = {date:prcp for date, prcp in prcp_data}
    session.close()


    return jsonify(prcp_dict)



@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    stations = session.query(Station.station).all()

# Perform a query to retrieve the data and precipitation scores
  
    station = list(np.ravel(stations))
    session.close()


    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    tobs_data = session.query(Measurement.tobs).\
    filter(Measurement.date >= one_year_ago).\
    filter(Measurement.station == "USC00519281").\
    order_by(Measurement.date).all()


# Perform a query to retrieve the data and precipitation scores
  
    tob= list(np.ravel(tobs_data))
    session.close()


    return jsonify(tob)


#@app.route("/api/v1.0/passengers")
#def passengers():
    # Create our session (link) from Python to the DB
    #session = Session(engine)

   # """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    #results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    #session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
   # all_passengers = []
    #for name, age, sex in results:
        #passenger_dict = {}
        #passenger_dict["name"] = name
       # passenger_dict["age"] = age
        #passenger_dict["sex"] = sex
        #all_passengers.append(passenger_dict)
        
if __name__ == '__main__':
    app.run()
        

    #return jsonify(all_passengers)


