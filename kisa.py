import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://cont.kisa.or.kr/bidding/biddingList?sdate=&edate=&method=&status=&title=&page='
# count = int(input("몇페이지까지 조회하시겠습니까? : "))
count = 20
id_list = []
title_list =[]
url_list = []
type_list = []
start_list = []
end_list = []
status_list = []

def get_info(raw_row):
    year =raw_row.find_all('td')[0].find_all('p')[1].text
    if "2020" in year:
        id_list.append(raw_row.find_all('td')[0].find_all('p')[1].text)
        title_list.append(raw_row.find_all('td')[1].text.replace('\t',"").replace("\r","").replace("\xa0","").replace("\n",""))
        url_list.append('https://cont.kisa.or.kr' + raw_row.a['href'])
        type_list.append(raw_row.find_all('td')[2].text)
        start_list.append(raw_row.find_all('td')[3].find_all('p')[0].text)
        end_list.append(raw_row.find_all('td')[3].find_all('p')[1].text.replace("\xa0",""))
        status_list.append(raw_row.find_all('td')[4].text)
    else:
        pass

for i in range(count):
    if i == 0:
        url_temp = 'https://cont.kisa.or.kr/bidding/biddingList'
    else:
        url_temp = url+str(i)
    print(url_temp)
    req = requests.get(url_temp)
    html = req.text
    header = req.headers
    status = req.status_code
    print(status)

    soup = BeautifulSoup(html, 'html.parser')

    title = soup.select('#wrap > main > section > table > tbody > tr')

#     print(len(title))
    print(title)
    for i in range(len(title)):
        get_info(title[i])

df = pd.DataFrame(list(zip(id_list,title_list,url_list,type_list,start_list,end_list,status_list)), columns=['입찰번호','공고명','링크','입찰유형','시작일','종료일','상태'])
df.to_csv("kisa.csv",index=False,encoding='utf-8-sig')