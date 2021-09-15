from flask import Flask, jsonify
from numpy.lib.function_base import meshgrid
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np

app = Flask(__name__)

# Import data from sqlite using SQLalhchemy. Use refelct to automate schema and class creation
engine = create_engine("sqlite:///./hawaii.sqlite", connect_args={'check_same_thread': False})
Base = automap_base()
Base.prepare(engine,reflect = True)

# initialize the query tool
#session = Session(engine)
Session = sessionmaker(bind=engine)

# Create data tables with auto generated classes
Measurement = Base.classes.measurement
Station = Base.classes.station

def unwrapResultProxy(resultproxy):
    d, a = {}, []
    for rowproxy in resultproxy:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            d = {**d, **{column: value}}
        a.append(d)
    return a

@app.route("/")
def home():
    return(
        f"This API will return Hawaii Weather Data.<br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/startdate <br/>"
        f"/api/v1.0/startdate/enddate <br/>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return all precipitaion data in a list of dictionaries. 
    Uses the date as the key, and precipiation amount as the value"""

    with engine.connect() as data:
        rain = data.execute("""
        SELECT date AS Date, prcp As Precipitation
        FROM measurement 
        ORDER BY Date ASC;
        """)

        results = unwrapResultProxy(rain)
        returnValue = {}
        for row in results:
            returnValue[row['Date']] = row['Precipitation']
        
        return jsonify(returnValue)

@app.route("/api/v1.0/stations")
def stations():
    session = Session()
    station_list = session.query(Station.station).all()
    all_names = list(np.ravel(station_list))
    return(jsonify(all_names))

@app.route("/api/v1.0/tobs")
def tobs():
    with engine.connect() as data:
        mostactive = data.execute("""
        SELECT station
        FROM measurement
        GROUP BY station
        ORDER BY count(prcp) DESC
        LIMIT 1;
        """)

        results = unwrapResultProxy(mostactive)

    with engine.connect() as data:
        previous_year = data.execute("""
        SELECT date AS Date, tobs AS Temperature
        FROM measurement station = :ma;"""
        , {'ma':results[0]["station"]})

        results = unwrapResultProxy(previous_year)

    return(jsonify(results))

@app.route("/api/v1.0/<start>")
def start(start):
    with engine.connect() as data:
        tobs_stats = data.execute("""
        SELECT MIN(tobs) AS Temperature_Minimum,
        MAX(tobs) AS Temperature_Maximum,
        ROUND(AVG(tobs),0) AS Temperature_Average,
        MIN(date) AS Date_Beginning,
        MAX(date) AS Date_Ending
        FROM measurement
        WHERE date > :start;"""
        , {'start':start})

        results = unwrapResultProxy(tobs_stats)

        return(jsonify(results))

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    with engine.connect() as data:
        tobs_stats_se = data.execute("""
        SELECT MIN(tobs) AS Temperature_Minimum,
        MAX(tobs) AS Temperature_Maximum,
        ROUND(AVG(tobs),0) AS Temperature_Average,
        MIN(date) AS Date_Beginning,
        MAX(date) AS Date_Ending
        FROM measurement
        WHERE date >= :start AND date <= :end; """
        , {'start':start,'end':end})

        results = unwrapResultProxy(tobs_stats_se)

        return(jsonify(results))
    
if __name__ == "__main__":
    app.run(debug=True)