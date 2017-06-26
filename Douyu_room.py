# -*- coding:utf-8 -*-
import requests
import threading # multi-threading process
from bs4 import BeautifulSoup
from lxml import etree # dissolve the page, faster than default html.parser
from selenium import webdriver
import re

company_name = "douyu"

# obtain the source from a page: get the Live-broadcasting Category link
def get_html(url):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0: WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
        request = requests.get(url=url, headers=headers)
        response = request.text
        return response

def get_category_html(html):
    soup = BeautifulSoup(html, "lxml") # create an object
    all_a = soup.find_all("a", attrs={"class": "thumb", "href": re.compile("/directory/game/"), "data-tid": True})
    category_html = []
    for link in all_a:
        cate_html = link["href"]
        category_html += ["https://www.douyu.com" + cate_html]
    return category_html

# ready for multi-thread
def get_roomnum(cate_url):
    driver = webdriver.PhantomJS(executable_path="E:/AnchengDeng/phantomjs-2.1.1-windows/bin/phantomjs.exe")
    driver.get(cate_url)
    import time
    time.sleep(0)
    response = driver.page_source.encode("utf-8", "ignore")
    driver.close()

    soup = BeautifulSoup(response, "lxml")
    room_title = soup.find("span", class_="tag ellipsis").string

    page_num = soup.find_all("a", class_="shark-pager-item")
    if page_num == []:
        all_a = soup.find_all("a", class_="play-list-link")
        room_num = len(all_a)

    else:
        page_num = int(page_num[len(page_num) - 1].string)
        driver = webdriver.PhantomJS(executable_path="E:/AnchengDeng/phantomjs-2.1.1-windows/bin/phantomjs.exe")
        driver.get(cate_url)
        xpath_str = "//a[@class='shark-pager-item'][last()]"
        driver.find_element_by_xpath(xpath_str).click()
        import time
        time.sleep(0)
        response = driver.page_source.encode("utf-8", "ignore")
        driver.close()
        soup = BeautifulSoup(response, "lxml")
        all_a = soup.find_all("a", class_="play-list-link")
        last_room_num = len(all_a)
        room_num = (page_num - 1) * 120 + last_room_num

    thefile = open(company_name + '_roomNumber' + record_time + '.txt', 'a')
    thefile.write("%s\t%s\t%s\t%s\n" % (room_title.encode('utf-8'), str(room_num), record_time, company_name))
    thefile.close()

    print "Done with " + room_title + " (" + str(room_num) + ")"

def start_roomnum_collecting(category_html):
    for item in category_html:
        get_roomnum(item)


def main():
    start_url = "https://www.douyu.com/directory"
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