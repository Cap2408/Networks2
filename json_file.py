"""Reads a har file from the filesystem, converts to CSV, then dumps to
stdout.
"""
import sys
import argparse
import json
import socket
from urllib.parse import urlparse
from urllib.parse import urlsplit

domain={}
list_domain = []
size_domain = {}

good_put = {}
list_tcp = []
tcp_dict = {}
tcp_size = {}
tcp_time = {}
no_tcp = {}
avg_time={}
load_time = 0
dns_time = {}
max_dict={}
good_time={}
total_avg=0
def main(harfile_path,output_file,output_file2):
	"""Reads a har file from the filesystem, converts to CSV, then dumps to
	stdout.
	"""
	global tcp_size
	global tcp_time
	global good_put
	global load_time
	global domain
	global tcp
	global list_domain
	harfile = open(harfile_path,encoding='utf8')
	harfile_json = json.loads(harfile.read())
	i = 0

	load_time = harfile_json['log']['pages'][0]['pageTimings']['onLoad']
	print(load_time)
	for entry in harfile_json['log']['entries']:
		try:
			tcp_id = entry["connection"]
			
			try:	
				#size
				size = entry['request']['headersSize']+entry['request']['bodySize']
				if(max[tcp_id]<size):
					newd={tcp_id:size}
					max[tcp_id].update(newd)
					good_time.update({tcp_id:entry['timings']['receive']})
				if(size>=0):
					pass
				else:
					size = 0
				tcp_size[tcp_id] += size	
			
			except:
				size = entry['request']['headersSize']+entry['request']['bodySize']
				if(size>=0):
					pass
				else:
					size = 0	
				new_dict = {tcp_id:size}
				tcp_size.update(new_dict)
				max.update(new_dict)
				good_time.update({tcp_id:entry['timings']['receive']})

			try:	
				#time	
				time = entry['timings']['receive']
				tcp_time[tcp_id] += time
			except:
				new_dict = {tcp_id:time}
				tcp_time.update(new_dict)
			
			try:				
				item=list_tcp[tcp_id]
				#to check if dns is called again
				if(entry['timings']['dns']!=-1):
					print("DNS Requested Again")

			except:
				list_tcp.append(tcp_id)
				value=entry['timings']['dns']
				connect=entry['timings']['connect']
				wait=entry['timings']['wait']
				if(value>=0):
					pass
				else:
					print("DNS Request Failed")
					value = 0
				my_tuple = (value,connect,wait)
				new_dict2 = {tcp_id:my_tuple}
				tcp_dict.update(new_dict2)
			try:
				no_tcp[tcp_id]
			except:
				no_tcp.update({tcp_id:1})
		except:
			pass


		if(entry['request']['method']=='GET'):
			string = entry['request']['url']
			base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(string))
			try:
				domain[base_url] += 1
				if (entry['request']['headersSize']+entry['request']['bodySize'] >= 0):
					size_domain[base_url] += entry['request']['headersSize']+entry['request']['bodySize']
			except:
				new_dict={base_url:1}
				size = entry['request']['headersSize']+entry['request']['bodySize']
				if(size>=0):
					pass
				else:
					size = 0	
				new_dict1={base_url:size} 
				domain.update(new_dict)
				size_domain.update(new_dict1)
				list_domain.append(base_url)

	temp_size=0
	temp_time=0
	for i in range(len(list_tcp)):
		tcp_id = list_tcp[i]
		size = tcp_size[tcp_id]
		time = tcp_time[tcp_id]
		temp_size+=size
		temp_time+=time
		avg = size/time
		avg_time.update({tcp_id:avg})

	if(temp_time!=0):
		total_avg=temp_size/temp_time
	else:
		total_avg=0
	for i in range(len(list_tcp)):
		tcp_id = list_tcp[i]
		size = tcp_dict[tcp_id][7]
		time = tcp_dict[tcp_id][8]
		maxi = size/time
		avg = avg_time_dict[tcp_id]
		print(maxi,avg)


	c = 0
	number=0
	size=0
	file=open(output_file,"w")
	file2=open(output_file2,"w")

	


	#for i in range(len(domain)):
	#	string = list_domain[i]
	#	file2.write(string+ '\t\t# of objects:'+str(domain[string])+'                 size downloaded:'+str(size_domain[string])+"\n")
	#	number+=domain[string]
	#	if(size_domain[string]!=-1):
	#		size+=size_domain[string]
	#file2.write("Total Size of objects : "+str(size)+"\n")
	#file2.write("Total Number of objects : "+str(number))
	#file2.close()
	

	#for i in range(len(tcp_dict)):
	#	string = list_tcp[i]
	#	file.write("Unique TCP id :")
	#	file.write(string)
	#	file.write("            # of objects downlaoded :")
	#	file.write(str(tcp_dict[string][0]))
	#	file.write("            size fetched :")
	#	file.write(str(tcp_dict[string][1]))
	#	file.write("\n")
	#file.close()


if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2],sys.argv[3])