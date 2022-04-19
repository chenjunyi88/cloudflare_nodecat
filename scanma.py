# coding=utf-8
import threading
import requests
import queue
import sys
import re
import os
import numpy as np

#
def bThread(iplist):
	threadl = []
	global q
	q = queue.Queue()
	for host in iplist:
		q.put(host)

	for x in range(0, int(SETTHREAD)):
		threadl.append(tThread(q))

	for t in threadl:
		t.start()
	for t in threadl:
		t.join()

#create thread
class tThread(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = q

	def run(self):
		while not self.queue.empty():
			host = self.queue.get()
			try:
				checkServer(host)
			except:
				continue


def checkalive():
	print('\n[Step1] Scanning alive servers:\n')
	nmap -sS -Pn --open --min-hostgroup 100 --min-parallelism 100 -n -T4 -iL iplist.txt -p443 -vv | awk '/Discovered open port 443\/tcp/{print $6}'
	global IPLIST
	IPLIST = zmap.read().splitlines()

def checkServer(host):
	header ={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
	aimurl = "http://"+host+":443"
	response = requests.get(url=aimurl,headers=header,timeout=10)
	serverText = response.headers['server']
	if (serverText == "cloudflare"):
		print("NewNode:" + host +" has been catched!\n")
		if MUTEX.acquire(3):
			with open("result.txt","a+") as file:
				file.write(host+"\n")
				file.close()
			MUTEX.release()

if __name__ == '__main__':
	os.system("clear")
	print('\n############# Cloud Front Scan ################')
	print('#   Author Madlifer|blog:https://vicho.me     #')
	print('###############################################\n')
	global SETIPLIST
	global SETTHREAD
	global MUTEX
	MUTEX = threading.Lock()
	SETIPLIST = sys.argv[1]
	SETTHREAD = sys.argv[2]
	checkalive()
	print('\n[Step2] Start Scanning edge nodes:\n')
	bThread(IPLIST)
	print('\n[WOW] Winner Winner Chicken Dinner！\n')
