import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

#################################################
# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# reference to the table
Base.classes.keys()
Measure = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
app = Flask(__name__)


#################################################
# Flask Routes

@app.route("/")
def welcome():
    
    txt = "List all available api routes"

    pr ="http://127.0.0.1:5000/api/v1.0/precipitation"
    sta ="http://127.0.0.1:5000/api/v1.0/stations"
    to ="http://127.0.0.1:5000/api/v1.0/tobs"
    st ="http://127.0.0.1:5000/api/v1.0/<start>"
    se ="http://127.0.0.1:5000/api/v1.0/<start>/<end>"
    ex = "Dates example: "
    ex1 = "http://127.0.0.1:5000/api/v1.0/2016-06-24/2016-09-24"
    fyi= "FYI= last date available 2017-08-23"

    listurl = []
    listurl.append(pr)
    listurl.append(sta)
    listurl.append(to)
    listurl.append(st)
    listurl.append(se)
    listurl.append(ex)
    listurl.append(ex1)
    listurl.append(fyi)


    return render_template("index.html", txt=txt, listurl=listurl)


########################################################################


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    year_ago = dt.date(2017,8,23) - dt.timedelta(weeks=52)

    #QUERY
    results = session.query(Measure.date, Measure.prcp).filter(Measure.date > year_ago).all()

    session.close()
   
    prec_list = []

    for date, prec in results:
        prec_dict = {}
        prec_dict["date"] = date
        prec_dict["precipitation"] = prec
        prec_list.append(prec_dict)

    return jsonify(prec_list)




########################################################################


@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    #QUERY
    results = session.query(Station.station.distinct()).all()

    session.close()
   
    list_st = list(np.ravel(results))

    return jsonify(list_st)



########################################################################


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    mostact=7
    year_ago = dt.date(2017,8,23) - dt.timedelta(weeks=52)

    #QUERY
    results = session.query(Measure.date, Measure.tobs).\
                    filter(Measure.station==Station.station).\
                    filter(Station.id == mostact).\
                    filter(Measure.date > year_ago).all()

    session.close()
   
    list = []

    for date, tob in results:
        dict = {}
        dict["date"] = date
        dict["temperature"] = tob
        list.append(dict)

    return jsonify(list)




########################################################################

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start(start,end=None):

    session = Session(engine)

    if end is None:
        end = session.query(Measure.date).order_by(Measure.date.desc()).first()
        end = list(np.ravel(end))
        end = end[0]

    #QUERY
    results = session.query(func.min(Measure.tobs), 
                            func.max(Measure.tobs), 
                            func.avg(Measure.tobs)).\
                            filter(Measure.date>=start).\
                            filter(Measure.date<=end).all()

    session.close()
   
    list_st = list(np.ravel(results))

    list1 = []

    dict = {}
    dict["min"] = list_st[0]
    dict["max"] = list_st[1]
    dict["avg"] = round(list_st[2],1)
    list1.append(dict)

    return jsonify(list1)




############## MAIN ##############

if __name__ == '__main__':
    app.run(debug=True)