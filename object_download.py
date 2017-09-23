import socket
import sys
from threading import Thread
import argparse
import json
import socket
from urllib.parse import urlparse
from urllib.parse import urlsplit
import os

""" stores dns, http, request: GET'''chillar''' """ 
dns_dict = {}
dns_name = []
domain={}
threads = []
count=0
MAX_TCP = 5
MAX_OBJ = 5
ini_final={}
def good_request(request, domain):
	req = request.strip('http://').strip(domain)	
	return req

def one_TCP(domain,s,request,value):
	#if(times=0):
	#	one_TCP(domain,request,MAX_OBJ)
	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#ip = socket.gethostbyname(domain)
	#s.connect((ip,80))
	s.send(request)
	#/Users/user/Desktop/334-assign/objects
	base = '/Users/user/Desktop/334-assign/objects'
	file_path = base+'/'+domain+'/object'+ str(value)+'.txt'
	directory = os.path.dirname(file_path)

	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
	except:
		pass		

	file=open(file_path,"a")
	
	result = s.recv(100000)
	#while(result!=b''):
		#print(result)
	#	result=s.recv(1)
	file.close()



def multiple_TCP(domain,sock,count):
	global dns_dict
	i=0
	while(len(dns_dict[domain])>0):
		while(MAX_TCP):
			try:
				thread = Thread(target=one_TCP,args=(domain,sock[i],dns_dict[domain][0],len(dns_dict[domain]),))
				count[i]+=1
				thread.start()
				requested=dns_dict[domain]
				requested.pop(0)			
				dns_dict.update({domain:requested})
				i+=1
			except:
				pass
		for i in range(MAX_TCP):	
			if(count[i]==MAX_OBJ):
				count.pop(i)
				sock.pop(i)
				socker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				socker.connect((domain,80))
				sock.append(socker)
				count.append(0)
			#ip = socket.gethostbyname(domain)


def calling_TCP(domain,req_list):
	global ini_final
	''' threads to a single domain are spawned and requests are sent under given
	arguements '''
	#count=0
	#while(len(req_list)>0):
	#	for i in range(MAX_TCP):
	#		thread = threads.start_new_thread(one_TCP,(domain,req_list,MAX_OBJ),)
	#print('debugging')
	sock = []
	count = []
	i=0
	while(i<MAX_TCP):
		print(domain)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#ip = socket.gethostbyname(domain)
		try:
			s.connect((domain,80))
			sock.append(s)
			count.append(0)
			i+=1
		except:
			pass
	multiple_TCP(domain,sock,count)

def initiation(input_har_path):
	global dns_dict
	global count
	global dns_name
	global dns_dict
	global ini_final
	harfile = open(input_har_path,encoding='utf8')
	harfile_json = json.loads(harfile.read())

	for entry in harfile_json['log']['entries']:
		if(entry['request']['method']=='GET'):
			string = entry['request']['url']
		#base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(string)).strip('http://')
			base_url=urlparse(string).hostname	
			if(string[:5]=='https'):
				continue
			try:
				list_temp = dns_dict[base_url]
				method = entry['request']['method']
				httpversion = entry['request']['httpVersion']
				string = entry['request']['url']
				req = good_request(string,base_url)
				string = method +' '+req+' / '+'\n'+httpversion
				request = bytes(req,'utf-8')
				list_temp.append(request)
				temp_dict = {base_url:list_temp}
				dns_dict.update(temp_dict)
			except:
				method = entry['request']['method']
				httpversion = entry['request']['httpVersion']
				request = entry['request']['url']
				request2 = good_request(request,base_url)
				ini_final.update({request2:request})
				string = method +' '+request2+' / '+'\n'+httpversion
				request1 = bytes(string,'utf-8')
				
				temp_dict = {base_url:[request1]}
				dns_dict.update(temp_dict)
				dns_name.append(base_url)



def main(string1):

	global threads
	global dns_dict
	global dns_name

	initiation(string1)

	#for i in range(len(dns_name)):
	#	print('Domain : ',dns_name[i])
	#	print(str(dns_dict[dns_name[i]]))

	#print('Len : ',len(dns_name))

	for i in range(len(dns_name)):
		domain = dns_name[i]
		request_list = dns_dict[domain]
		try:
			#print('Main called calling_TCP',i)
			#thread = thread.start_new_thread(calling_TCP,(domain,request_list,))
			#threads.append(thread)
			thread=Thread(target=calling_TCP,args=(domain,request_list,))
			thread.start()
		except:
			i = i-1
			continue

if __name__ == '__main__':
	string1 = sys.argv[1]
	#string2 = sys.argv[2]
	main(string1)