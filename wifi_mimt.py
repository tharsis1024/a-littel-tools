import re,os,sys,time,signal,subprocess,json,random,string,argparse
from flask import Flask,request
import requests
import threading
from scapy.all import *

################ Flask launch #########################

PLATFORM_URL = "https://127.0.0.1:7000/api/service/result"
WEB_SERVER = "127.0.0.1"
PORT = 10003
app = Flask(__name__)

#######################################################

def mimt_start(ssid,device):
    with open("att.pulp","w") as f:
        f.write("set interface " + device +'\n')
        if ssid != "":
            f.write("set ssid " + ssid +'\n')
        else:
            print("[-]no ssid,pluse use -ssid")
            os.system("rm att.pulp")
            sys.exit()       
        proxy = "noproxy"
        f.write("set proxy "+proxy+'\n')
        f.write("start")
        f.close() 
        #os.popen("wifipumpkin3 --pulp att.pulp").read()
        os.system("wifipumpkin3 --pulp att.pulp")
    os.system("rm att.pulp")

    
#######################################################

@app.route('/start', methods=['POST'])
def run_threading_check():
    result = {}
    params = request.json
    if params != None:
        ssid = params.get("ssid")
        device = params.get("device")
        t = threading.Thread(target=mimt_start, args=(ssid, device,))
        t.start()
        result["username"] = ""
    else:
        result["status"] = "error"
        result["message"] = "Invalid parameters"
    return result


#######################################################

def WIFISecurity():
    jsdata = request.get_json()
    print('-------------------------',jsdata)
    if jsdata != None:
        r = run_threading_check()
        response = app.response_class(
           response=json.dumps(r),
           mimetype='application/json'
        )
        return "Plugin Start Execution"
    else:
        return 'No parameters'
        
app.run(host=WEB_SERVER, port=PORT)
