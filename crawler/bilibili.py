# -*- coding: utf-8 -*-
'''
@Last Modified: 2018-9-13
@author: lacey
@describe: main crawler file
'''
import requests, threading, time, random
import json, csv
import sys
from queue import Queue
from crawler import utils

#B站API详情 https://github.com/Vespa314/bilibili-api/blob/master/api.md

lock = threading.Lock()
up_count = 0 #UP主人数记录


'''
测试线程是否退出
'''
check_working = []
for x in range(10):
	check_working.append(0)
def start(tid):
	check_working[int(tid[6:])-1] = 1
	utils.output_info("S %s" % (check_working))
def finish(tid):
	check_working[int(tid[6:])-1] = 0
	utils.output_info("F %s" % (check_working))




class ThreadCrawl(threading.Thread):
	def __init__(self, tid, mid_queue, ip_list, writer, lock):
		threading.Thread.__init__(self)
		self.tid = tid
		self.mid_queue = mid_queue
		self.ip_list = ip_list
		self.writer = writer
		self.lock = lock
		self.url1 = "https://api.bilibili.com/x/web-interface/card?mid="
		self.url2 = "http://space.bilibili.com/ajax/member/getSubmitVideos?mid="

	def run(self):
		utils.output_info("Start %s" % (self.tid))
		#mid = 0
		global up_count

		while not self.mid_queue.empty():
			mid = self.mid_queue.get()

			utils.output_info("Start %s %s" % (self.tid, mid))

			size, page = 50, 1
			info_list = []
			up_info_json = None
			vedio_info_json = None

			url1 = self.url1 + str(mid)
			up_info_json = self.get_info_json(up_info_json, url1, mid)
			if not up_info_json:
				continue
			
			while True:
				print("22222222222222222222222222222222222222222222222222222222222222222222")
				url2 = self.url2 + str(mid) + "&pagesize=" + str(size)+"&page=" + str(page)
				vedio_info_json = self.get_info_json(vedio_info_json, url2, mid)
				if not vedio_info_json:
					break
				if vedio_info_json["data"]["vlist"]:
					self.para_json(up_info_json, vedio_info_json, info_list)
					page += 1
				else:
					if info_list:
						self.save(info_list)
						up_count += 1 #统计UP主数量
					utils.output_info("Finished %s %s vedio" % (self.tid, mid))
					break

	def send_request(self, url):
		resp = None

		while not resp:
			print("33333333333333333333333333333333333333333333333333333333333333333333")
			headers = utils.get_random_headers()
			#proxies = utils.get_random_proxies(self.ip_list)
			proxies = {}
			try:
				#start(self.tid)
				resp = requests.get(url=url, proxies=proxies, headers=headers)
				#finish(self.tid)
			except Exception as e:
				utils.output_info("Error %s %s" % (self.tid, repr(e)))
				time.sleep(1)
				
		return resp

	def get_info_json(self, info_json, url, mid):
		resp = self.send_request(url)
		try:
			info_json = resp.json()
		except Exception as e:
			#utils.output_info("Error %s up convert to json failed at %s" % (self.tid, mid))
			self.mid_queue.put(mid)
		return info_json

	def para_json(self, up_info_json, vedio_info_json, info_list):
		for video in vedio_info_json["data"]["vlist"]:
					video_dict = {} #一个视频信息的dict
					video_dict["name"] = up_info_json["data"]["card"]["name"]
					video_dict["mid"] = video["mid"]
					video_dict["aid"] = video["aid"]
					video_dict["play"] = video["play"]
					video_dict["fans"] = up_info_json["data"]["card"]["fans"]
					video_dict["comment"] = video["comment"]
					video_dict["favorites"] = video["favorites"]
					info_list.append(video_dict)

	def save(self, item):
		try:
			with self.lock:
				self.writer.writerows(item)	
		except Exception as e:
			#utils.output_info("%s %s" % (self.tid, repr(e)))
			pass
			

#多线程爬虫入口，返回值为UP主人数
def multithread_crawl(filename, ip_pool_path, mid_begin, mid_end, thread_crawl_num):
	#初始化代理ip列表
	ip_list = []
	ip_list = utils.read_file(ip_pool_path)
	if not ip_list:
		utils.output_info("空代理ip列表!")
		sys.exit(1)

	f = open(filename, "a", newline='')
	#我只需要up的昵称，id号，av号，播放数，粉丝数，评论数，收藏数
	headers = ["name", "mid", "aid", "play", "fans", "comment", "favorites"]
	writer = csv.DictWriter(f, headers)
	writer.writeheader() #把headers作为列名写入，注释掉的话不会写入但不影响数据写入

	#初始化mid队列
	mid_queue = Queue()
	for mid in range(mid_begin, mid_end + 1): #逐一爬取
		mid_queue.put(mid)

	#初始化爬虫线程
	crawl_threads = []
	crawl_list = []
	for i in range(1, thread_crawl_num + 1):
		crawl_list.append("crawl-" + str(i))
	for tid in crawl_list:
		thread = ThreadCrawl(tid, mid_queue, ip_list, writer, lock)
		thread.start()
		crawl_threads.append(thread)
	
	'''
	#等待队列清空
	while not mid_queue.empty():
		pass
	utils.output_info("mid queue emptied")
	'''
	

	#主线程等待所有子线程结束
	for t in crawl_threads:
		t.join()
	
	with lock:  
		f.close()		
		
	global up_count
	utils.output_info("UP Num: %s" % (up_count))
	utils.output_info("Exit multithread_crawl")
