from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import urllib.request as req
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

import pandas as pd
import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')

#코드는 작성하였지만, 교보문고의 크롤링 조건에 막힌것으로 추정,,,
#robots.txt 확인 시 detail, book, book/detail 등 대부분 disallow 되어있어 책 정보 불러오기가 안된다(!!!)
#해결방법 찾는 중,,,


# 01 : 소설 , 03 : 시/에세이 , 05 : 인문 , 13 : 경제/경영 , 15 : 자기계발
url = 'https://product.kyobobook.co.kr/category/KOR/01#?page=1&type=best&per=20'

User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
chrome_options = Options()
chrome_options.add_argument(f"user-agent={User_Agent }")

driver = webdriver.Chrome()
driver.get(url)

book_titles = list()
book_author = list()
book_publish = list()
book_price = list()
book_page_urls = list()


for i in range(1,51):
    page_links = driver.find_elements(By.CSS_SELECTOR,'#homeTabBest > div.switch_prod_wrap.view_type_list > ol > li > div.prod_area.horizontal > div.prod_info_box > a')
    for page_link in page_links:
        link = page_link.get_attribute('href')
        book_page_urls.append(link)
    if i== 50:
       break
    next_page = driver.find_element(By.CSS_SELECTOR,'#bestBottomPagi > button.btn_page.next')
    next_page.send_keys(Keys.ENTER)
    time.sleep(3)
driver.quit()

driver = webdriver.Chrome(options=chrome_options)
for url in book_page_urls:
    try:
        driver.get(url)
        time.sleep(3)
        title = driver.find_element(By.CSS_SELECTOR,
                                    '#contents > div.prod_detail_header > div > div.prod_detail_title_wrap > div > div.prod_title_box.auto_overflow_wrap > div.auto_overflow_contents > div > h1 > span')
        book_titles.append(title.text)
    except:
        book_titles.append('공백')

    try:
        author = driver.find_elements(By.CSS_SELECTOR, '#contents > div.prod_detail_header > div > div.prod_detail_view_wrap > div.prod_detail_view_area > div > div > div.prod_author_box.auto_overfllow_wrap > div.auto_overflow_contents > div > div > a')
        book_author.append(author.text)
    except:
        book_author.append('')

    try:
        publish = driver.find_element(By.CSS_SELECTOR, '#contents > div.prod_detail_header > div > div.prod_detail_view_wrap > div.prod_detail_view_area > div > div > div.prod_info_text.publich_date > a')
        book_publish.append(publish.text)
    except:
        book_publish.append('')

    try:
        price = driver.find_element(By.CSS_SELECTOR,
                                          '#contents > div.prod_detail_footer > div > div > div.left_area > span.prod_info_price > span.val')
        book_price.append(price.text)
    except:
        book_price.append('')

driver.quit()

kyobo_tbl = pd.DataFrame([book_titles,book_author,book_publish,book_price], index=['title', 'author', 'publish', 'price']).T
kyobo_tbl.to_csv('C:/Users/tpfzl/OneDrive/Desktop/3-1/빅데이터분석/kyobo_best.csv')

