from flask import Flask, render_template, request, redirect, url_for
#from werkzeug import secure_filename
#from base_class import *
import os, sys, time ,random
import socket
import requests, json
#from message_log import msg_sender,message
import argparse
#from test_data import generate_result,overall_result


def generate_result(num,max_t=1000,record=100,population=5):
    results=[]
    candidates=[i for i in range(record)]
    for _ in range(num):
        test_data={
                    "time":random.random()*10,
                    "iteration":random.randint(1,max_t),
                    "fitness":random.randint(50,99),
                    "individual": [random.choice(candidates) for _ in range(population)],
                    "finger":[random.randint(0,2**450) for _ in range(population)]
                }

        results.append(test_data)
    return results


def overall_result(results):
    ttc=0
    popu=0
    best=-1
    best_index=-1
    for i in range(len(results)):
        result=results[i]
        ttc+=result['time']
        popu+=len(result['individual'])
        if result['fitness']>best:
            best=result['fitness']
            best_index=i

    res={"ttc":ttc,
          "popu":popu,
          "best":best,
          "bestsolution":best_index
    }
    return res

app=Flask(__name__)
data=generate_result(5)
@app.route('/')
def home_page():
    return 

@app.route('/query')
def query_data():
    #data=generate_result(5)
    return json.dumps(data)

@app.route('/overall')
def query_all():
    res=overall_result(data)
    return json.dumps(res)

app.run()