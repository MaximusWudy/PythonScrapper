# -*- coding:utf-8 -*-
import requests
import threading # multi-threading process
from bs4 import BeautifulSoup
from lxml import etree # dissolve the page, faster than default html.parser
from selenium import webdriver

import re

company_name = "longzhu"
js = "document.body.scrollTop=1000000"

# obtain the source from a page: get the Live-broadcasting Category link
def get_html(url):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0: WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
        request = requests.get(url=url, headers=headers)
        response = request.text
        return response

def get_category_html(html):
    soup = BeautifulSoup(html, "lxml") # create an object
    all_a = soup.find_all("a", attrs={"href": re.compile("/channels/"), "title": True, "target": "_blank", "data-action": True, "data-label": True, "data-cate": "lz.games"})
    category_html = []
    for link in all_a:
        cate_html = link["href"]
        category_html += ["http://longzhu.com" + cate_html]
    return category_html

def get_roomnum(cate_url):
    driver = webdriver.PhantomJS(executable_path="E:/AnchengDeng/phantomjs-2.1.1-windows/bin/phantomjs.exe")
    driver.get(cate_url)
    import time
    time.sleep(0)
    response = driver.page_source.encode("utf-8", "ignore")

    soup = BeautifulSoup(response, "lxml")
    room_title = soup.find("h2", class_="list-head-txt").string
    room_num_add = len(soup.find_all("h3", class_="listcard-caption"))

    counter = 1
    equal_index = False
    while not equal_index:
        if counter == 1:
            driver.execute_script(js)
            time.sleep(1)
            response = driver.page_source.encode("utf-8", "ignore")
            soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')
            room_num_add_2 = len(soup.find_all("h3", class_="listcard-caption"))
            equal_index = room_num_add == room_num_add_2
            counter += 1

        if counter > 1:
            room_num_add = room_num_add_2
            driver.execute_script(js)
            time.sleep(1)
            response = driver.page_source.encode("utf-8", "ignore")
            soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')
            room_num_add_2 = len(soup.find_all("h3", class_="listcard-caption"))
            equal_index = room_num_add == room_num_add_2
            counter += 1

    driver.close()

    room_num = room_num_add_2
    thefile = open(company_name + '_roomNumber' + record_time + '.txt', 'a')
    thefile.write("%s\t%s\t%s\t%s\n" % (room_title.encode('utf-8'), str(room_num), record_time, company_name))
    thefile.close()

    print "Done with " + room_title + " (" + str(room_num) + ")"


def start_roomnum_collecting(category_html):
    for item in category_html:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0: WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
        request = requests.get(url=item, headers=headers)
        response = request.text
        soup_test = BeautifulSoup(response, 'lxml').find_all("h3", class_="listcard-caption")
        if soup_test == []:
            continue
        else:
            get_roomnum(item)


def main():
    start_url = "http://longzhu.com/games/?from=topbarallgames"
    start_html = get_html(start_url)
    html = get_category_html(start_html)
    start_roomnum_collecting(html)
# if __name__=="__main__":
#   main()

while True:
    from time import localtime, strftime
    record_time = strftime("%Y-%m-%d_%H-%M-%S", localtime())
    print "Starting on Collecting " + company_name + " room number, good luck!"
    main()
    import time
    time.sleep(3600 - 45)