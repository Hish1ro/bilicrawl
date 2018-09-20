# -*- coding: utf-8 -*-
'''
@Last Modified: 2018-9-13
@author: lacey
@describe: utils file
'''
import random, requests, time

#写入文档
def write_file(path, text):
	with open (path, "a", encoding="utf-8") as f:	
		f.writelines(text)
		f.write("\n")

#清空文档
def truncate_file(path):
	with open(path, "w", encoding="utf-8") as f:
		f.truncate()
	
#读取存储代理ip的文档
def read_file(path):
	with open(path, "r", encoding="utf-8") as f:
		ip_list = []
		for s in f.readlines():
			ip_list.append(s.strip())
	return ip_list

#随机获得一个UA头	
def get_random_headers():
	user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
	headers = {
			"User-Agent": random.choice(user_agent_list),
			#"Connectin": "close"
	} #随机获得UA,用代理ip"Connection"要设为close
	return headers
	
def get_random_proxies(ip_list):
	proxies = {}
	proxy_ip = random.choice(ip_list) #从代理ip列表中随机获取一个代理ip
	proxies = {
			"http": proxy_ip,
			"https": proxy_ip,
	}
	return proxies

#检查代理ip是否可用
def check_ip_available(target_url, ip):
	headers = get_random_headers()
	proxies = {
				"http": ip,
				"https": ip,
	}
	
	try:
		response = requests.get(url=target_url, proxies=proxies, headers=headers, timeout=5).status_code
		
		if response == 200:
			#print(ip, "is available!")
			return True
		else:
			return False
	except Exception:
			#print("Oops,", ip, "is not available!")
			return False


def output_info(info):
	now = time.strftime("%m-%d %H:%M:%S", time.localtime())
	print(now, info)
