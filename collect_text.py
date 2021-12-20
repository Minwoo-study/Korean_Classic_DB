# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# # 한국고전종합DB 번역문 스크래핑(Selenium)

# %%
# get_ipython().system('pip install --upgrade pandas')
# get_ipython().system('pip install -U webdriver_manager selenium')
# get_ipython().system('apt-get update # to update ubuntu to correctly run apt install')
# get_ipython().system('apt install chromium-chromedriver')
# get_ipython().system('pip install lxml')
# get_ipython().system('pip install BeautifulSoup4')
# get_ipython().system('pip install pickle5')


# %%
import requests
import pandas as pd
import lxml
import xml.etree.ElementTree as ET
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tqdm import tqdm
import numpy as np
import re

import random
import time


# %%
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') #내부 창을 띄울 수 없으므로 설정
chrome_options.add_argument('--no-sandbox')

chrome_options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome('C:/Users/Administrator/Documents/Downloads/chromedriver.exe', options=chrome_options)
driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)



# %% [markdown]
# ### 자동화

# %%
num = input('1~11까지 입력하세요 \n(ex : 1 = 0~9999, 2 = 10000~19999...)')

with open('G:/공유 드라이브/ProjectOuri/DB&Code/한국고전종합DB/한국문집총간_trans_{}.pickle'.format(num), "rb") as fh:
  data = pd.read_pickle(fh)


# %%
ko_list=data['id'].to_list()
ko_list


# %%
#예외처리
row_list = []
error_list =[]

for id in tqdm(ko_list) :
    try :
        url = f'https://db.itkc.or.kr/dir/node?dataId={id}&viewSync=TR'
        res = requests.get(url)
        time.sleep(random.uniform(3,6))
        req = driver.page_source
        soup = BeautifulSoup(res.text,'html.parser')

        
        ch_text = soup.select_one('div > div.text_body.ori > div').text
        ko_text = soup.select('.text_body')[1].text

        row_inter = {'ID': id, '원문':ch_text, '번역문':ko_text}
        
        row_list.append(row_inter)
    
    except AttributeError :
        try :
            ko_text = soup.select('.text_body')[1].text
            row_inter = {'ID': id, '원문':'원문 오류', '번역문':ko_text}
            row_list.append(row_inter)
            error = {'ID' : id, 'Error' :'원문'}
            error_list.append(error)
            print('오류난 id : '+ id)
        except IndexError :
            row_inter = {'ID': id, '원문': '원문 오류', '번역문':'번역문 오류'}
            row_list.append(row_inter)
            error = {'ID' : id, 'Error' :'번역문'}
            error_list.append(error)
            print('오류난 id : '+ id) 
    
    except IndexError :
        try :
            ch_text = soup.select_one('div > div.text_body.ori > div').text
            row_inter = {'ID': id, '원문': ch_text, '번역문':'번역문 오류'}
            row_list.append(row_inter)
            error = {'ID' : id, 'Error' :'번역문'}
            error_list.append(error)
            print('오류난 id : '+ id) 
        except AttributeError :
            row_inter = {'ID': id, '원문': '원문 오류', '번역문':'번역문 오류'}
            row_list.append(row_inter)
            error = {'ID' : id, 'Error' :'원문'}
            error_list.append(error)
            print('오류난 id : '+ id) 
    
    

# %%

df = pd.DataFrame(row_list)
df.to_pickle('translate {}.pickle'.format(num))

df_error = pd.DataFrame(error_list)
df_error.to_pickle('error {}.pickle'.format(num))