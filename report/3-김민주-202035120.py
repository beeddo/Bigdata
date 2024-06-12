from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

#url = 'https://finance.naver.com/sise/sise_quant.naver'
#req = requests.get(url)
#soup = BeautifulSoup(req.content, 'html.parser')

url = 'http://finance.naver.com'
res = requests.get(url).content
soup = BeautifulSoup(res, 'html.parser')

result = []

items = soup.find('tbody',{'id':'_topItems1'})

for item in items.find_all('tr'):
    stock_name = item.find('th').get_text()
    stock_prices = item.find_all('td')[0].get_text()
    delta_prices = item.find_all('td')[1].get_text()[3:]
    delta_percents = item.find_all('td')[2].get_text()
    result.append([stock_name]+[stock_prices]+[delta_prices]+[delta_percents])

naver_tbl = pd.DataFrame(result, columns=('name', 'price', 'delta_prices', 'delta_percents'))
naver_tbl.to_csv('C:/Users/tpfzl/OneDrive/Desktop/3-1/빅데이터분석/naver_Crawler.csv', encoding='cp949', mode='w', index=True)
