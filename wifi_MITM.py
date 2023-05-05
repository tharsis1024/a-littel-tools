import os
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='you can only use -ssid')
    parser.add_argument("-i", type=str, default="wlan0")
    parser.add_argument("-ssid", type=str, default="")
    parser.add_argument("-p", type=str, default="0")
    args = parser.parse_args()
    
    inter = args.i
    ssid = args.ssid
    proxy = args.p
    
    with open("att.pulp","a") as f:
        print("[+]open file test over")
        print("-----")
        f.write("set interface " + inter+'\n')
        print("[+]inter write test over")
        print("-----")
        if ssid != "":
            f.write("set ssid " + ssid+'\n')
            print("[+]ssid write test over")
            print("-----")
        else:
            print("[-]no ssid,pluse use -ssid")
            os.system("rm att.pulp")
            sys.exit()
            
        if proxy == "0":
            proxy = "noproxy"
            f.write("set proxy "+proxy+'\n')
            print("[+]proxy write test over")
            print("-----")
        elif proxy == "1":
            proxy = "pumpkinproxy"
            f.write("set proxy "+proxy+'\n')
            print("[+]proxy write test over")
            print("-----")
        elif proxy == "2":
            proxy = "captiveflask"
            f.write("set proxy "+proxy+'\n')
            f.write("set captiveflask.DarkLogin true"+'\n')
            print("[+]proxy write test over")
            print("-----")
        else :
            print("[-]proxy mode error,plase check")
            os.system("rm att.pulp")
            sys.exit()
        f.write("start")
        print("[+]start write test over")
        print("all test is over! if you want exit, place input exit")
        print("the script can auto delete temp file")
        print("-----start work-----")
        
        f.close()
        
        os.system("wifipumpkin3 --pulp att.pulp")

    os.system("rm att.pulp")
    print("rm:att.pulp -- is over")
    
if __name__ == "__main__":
    main()
