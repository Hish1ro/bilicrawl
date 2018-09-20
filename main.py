# -*- coding: utf-8 -*-
'''
@Last Modified: 2018-9-13
@author: lacey
@describe: crawler entrance
'''
from crawler import bilibili
from crawler import utils
from crawler.ip_pool import ip_pool
import time

mid_begin = 7000000 #id起始号
mid_end = 7000100 #id结束号
thread_crawl_num = 1 #爬虫线程数
filename = str(mid_begin) + "-" + str(mid_end) + " " +\
time.strftime('%Y-%m-%d %H-%M', time.localtime()) + ".csv" #存储的文件名
#ip_pool_path = "crawler/ip_pool/ip_pool.txt" #ip池文件Linux路径
ip_pool_path = "crawler\\ip_pool\\ip_pool.txt" #ip池文件Windows路径
target_url = "http://space.bilibili.com/ajax/member/getSubmitVideos?mid=10" #测试代理ip用url


if __name__ == "__main__":
	start_time = time.time()

	ip_pool.get_ip_multithread(target_url, ip_pool_path)
	bilibili.multithread_crawl(filename, ip_pool_path, mid_begin, mid_end, thread_crawl_num)
	
	time_elapsed = time.time() - start_time
	print("The crawler ran {:.0f}h {:.0f}m {:.0f}s"
	.format(time_elapsed // 3600 , time_elapsed // 60 % 60, time_elapsed % 60))
	utils.output_info("%s %s" % ("Finished at", time.asctime(time.localtime(time.time()))))
