# -*- coding:utf-8 -*-
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
from time import localtime, strftime

company_name = "bilibili"

while True:
    name_list = []
    room_list = []
    record_time = strftime("%Y-%m-%d_%H-%M-%S", localtime())
    site = ["http://live.bilibili.com/pages/area/ent", "http://live.bilibili.com/pages/area/draw", "http://live.bilibili.com/single", "http://live.bilibili.com/online", "http://live.bilibili.com/e-sports", "http://live.bilibili.com/mobile-game"]

    for site_index in range(len(site)):
        driver = webdriver.PhantomJS(executable_path="E:/AnchengDeng/phantomjs-2.1.1-windows/bin/phantomjs.exe")
        driver.get(site[site_index])
        import time
        time.sleep(2)
        response = driver.page_source.encode("utf-8", "ignore")
        soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')
        if site_index == 0:
            name = soup.find_all(class_="category-name")
            room_num = soup.find_all(class_="section-num")
        elif site_index == 1:
            name = [u"<h1>绘画直播</h1>"]
            room_num = soup.find_all("span", class_="total")
        else:
            name = soup.find_all(class_="area-title")
            room_num = soup.find_all(class_="dynamic-count")

        for x in name:
            name_list.append(BeautifulSoup(str(x), 'html.parser', from_encoding='utf-8').find().string)
        for x in room_num:
            room_list.append(int(BeautifulSoup(str(x), 'html.parser', from_encoding='utf-8').find().string))

    print "Success To Gather Room Number Information"
    driver.close()

    # save the table
    thefile = open(company_name + '_roomNumber' + record_time + '.txt', 'w')
    for item in range(len(name_list)):
        thefile.write("%s\t%s\t%s\t%s\n" % (str(name_list[item]), str(room_list[item]), record_time, company_name))
    thefile.close()

    print "Success To Output Room Number Record at " + record_time

    import time
    time.sleep(3587)