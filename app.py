#Import dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import inspect, create_engine, func
from flask import Flask, url_for, jsonify
from markupsafe import escape

#Establish connection to database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

#Main route links
@app.route('/')
def home():
  return """<h1>Available Routes:</h1>
  <p>
  <ul>
  <li><a href=/api/v1.0/precipitation>Precipitation</a>
  <li><a href=/api/v1.0/stations>Stations</a>
  <li><a href=/api/v1.0/tobs>TOBS</a> // temperature observations
  <li><a href=/api/v1.0/2017-06-30>2017-06-30</a> // minimum, average, and maximum temperatures for recorded data starting on vacation start date
  <li><a href=/api/v1.0/2017-06-30/2017-07-04>2017-06-30 - 2017-07-04</a> // minimum, average, and maximum temperatures for entire vacation
  </ul>"""

#Precipitation app route
@app.route('/api/v1.0/precipitation')
def precipitation():
  one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
  one_year_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).order_by(Measurement.date).all()
  precip_dict = dict(one_year_precip)
  return jsonify(precip_dict)

#Stations app route
@app.route('/api/v1.0/stations')
def stations():
  all_stations = session.query(Measurement.station, Station.name).group_by(Measurement.station).all()
  station_list = list(all_stations)
  return jsonify(station_list)

#Tobs app route
@app.route('/api/v1.0/tobs')
def tobs():
  one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
  one_year_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).order_by(Measurement.date).all()
  tobs_dict = dict(one_year_tobs)
  return jsonify(tobs_dict)

#Vacation start date app route
@app.route('/api/v1.0/2017-06-30')
def start():
  start_temp = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= '2017-06-30').group_by(Measurement.date).all()
  start_temp_list = list(start_temp)
  return jsonify(start_temp_list)

#Vacation range date app route
@app.route('/api/v1.0/2017-06-30/2017-07-04')
def end():
  start_end_temp = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= '2017-06-30').filter(Measurement.date <='2017-07-04').group_by(Measurement.date).all()
  start_end_temp_list = list(start_end_temp)
  return jsonify(start_end_temp_list)
    
if __name__ == "__main__":
  app.run(debug=False)