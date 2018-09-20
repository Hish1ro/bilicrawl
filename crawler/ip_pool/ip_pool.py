# -*- coding: utf-8 -*-
'''
@Last Modified: 2018-9-13
@author: lacey
@describe: get proxy ip list and save it to file
'''
import bs4, requests, threading
import sys
#sys.path.append("/root/bili-server/crawler") #Linux路径
sys.path.append("C:\\Users\\Rei\\Desktop\\bilibilicrawl\\crawler") #Windows路径
import utils
	
#获取代理ip
def find_ip(type, pagenum, target_url, path): #ip类型,页码,目标url,存放ip的路径
	proxy_url_list = {
			'1': 'http://www.xicidaili.com/nt/', #xicidaili国内普通代理
			'2': 'http://www.xicidaili.com/nn/', #xicidaili国内高匿代理
			'3': 'http://www.xicidaili.com/wn/', #xicidaili国内https代理
			'4': 'http://www.xicidaili.com/wt/', #xicidaili国外http代理
	}
	url = proxy_url_list[str(type)] + str(pagenum)
	headers = utils.get_random_headers()
	html = requests.get(url=url, headers=headers, timeout=3).text
	soup = bs4.BeautifulSoup(html, "lxml")
	all = soup.find_all("tr", class_="odd")
	
	for i in all:
		t = i.find_all("td")
		ip = t[1].text + ":" + t[2].text
		
		is_avail = utils.check_ip_available(target_url, ip)
		if is_avail == True:
			utils.write_file(path, ip)
	
#多线程抓取代理ip入口
def get_ip_multithread(target_url, path):
	utils.truncate_file(path)
	threads = []
	ip_list = []

	for type in range(4):
		for pagenum in range(1):
			thread = threading.Thread(target=find_ip, args=(type+1, pagenum+1, target_url, path))
			threads.append(thread)
	'''
	for pagenum in range(1):
			thread = threading.Thread(target = find_ip, args = (2, pagenum+1, target_url, path))
			threads.append(thread)
	'''
	utils.output_info("开始爬取代理ip")
	for thread in threads:
			thread.start()
	for thread in threads:
			thread.join()
	
	with open(path, "r") as f:
		for ip in f.readlines():
			ip = ip.strip()
			ip_list.append(ip)
	ip_list = sorted(set(ip_list), key=ip_list.index) #剔除重复ip
	utils.truncate_file(path)
	for ip in ip_list:
		utils.write_file(path, ip)

	utils.output_info("代理ip爬取完成 总计%s个" % (len(ip_list)))
