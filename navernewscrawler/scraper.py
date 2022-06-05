## Import libs
import pandas as pd
import json

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup as bs
import soupsieve as sv

from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus

from tqdm import tqdm

## Import custom libs

from navernewscrawler import utils

## Session setting with retry strategy

session = requests.session()

assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
session.hooks["response"] = [assert_status_hook]

retry_config = {
    "total": 10,
    "status_forcelist": [413, 429, 500, 502, 503, 504],
    "method_whitelist": ["GET", "POST"],
    "backoff_factor": 2,
    }
retry_strategy = Retry(**retry_config)
adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("http://", adapter)
session.mount("https://", adapter)

## naver news query url creator

def naver_news_search_url(query, start_idx, start_date, end_date=None, sort_key='recent_asc') -> str:
    sort_key = sort_key.lower()
    assert sort_key in ['recent_asc', 'relevance']
    sort_d = {
        'recent_asc': '1',
        'relevance': '0',
    }

    encoded_query = quote_plus(query)

    start_date = str(start_date)
    start_date_dot = start_date[:4] + '.' + start_date[4:6] + '.' + start_date[6:]

    if end_date:
        end_date = str(end_date)
        end_date_dot = end_date[:4] + '.' + end_date[4:6] + '.' + end_date[6:]
    else:
        end_date_dot = start_date_dot
        end_date = start_date

    url = f'https://m.search.naver.com/search.naver?where=m_news&sm=mtb_pge&query={encoded_query}&sort={sort_d[sort_key]}&photo=0&field=0&pd=3&ds={start_date_dot}&de={end_date_dot}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:from{start_date}to{end_date}&start={start_idx}'
    
    return url

## naver news page link collector

# TODO: 언론사 어디인지 여기에서 가져올 것. 
def get_news_list(news_page_url) -> list:
    r = session.get(news_page_url, headers=utils.HEADERS)
    b = bs(r.content, 'html.parser')

    news_urls = b.find_all('div', {'class': 'news_dsc'}) # 기사 url만 가져옴. 
    news_urls = [n.find('a').attrs['href'] for n in news_urls] 

    companies = b.find_all('div', {'class': 'info_group'})
    companies = [c.find('a').get_text() for c in companies]

    titles = b.find_all('div', {'class': 'tit'})
    titles = [t.get_text() for t in titles]

    result = []
    for n, c, t in zip(news_urls, companies, titles):
        result.append({
            'news_url': n,
            'company': c,
            'title': t,
            })
    
    return result

## naver-format news article info collector

def article_crawling(article_url) -> dict:
  r=session.get(article_url, headers=utils.HEADERS)
  b=bs(r.content,'html.parser')
  
  news_head = b.find('h2', {'class': 'media_end_head_headline'}) # 기사 제목만 가져옴. 
  headline=news_head.get_text()

  news_text = b.find('div', {'id': 'dic_area'}) # 기사 본문만 가져옴. 
  text=news_text.get_text()
  
  news_section = b.find('em', {'class': 'media_end_categorize_item'}) # 기사 섹션만 가져옴.
  section=news_section.get_text()
  
  news_writer = b.find('em', {'class': 'media_end_head_journalist_name'}) # 기자이름만 가져옴.
  writer=news_writer.get_text()
  
  news_link = b.find('a', {'class': "media_end_head_origin_link"} ).attrs['href'] # 기사 링크만 가져옴.
  link=news_link
  
  news_date = b.find('span', {'class': 'media_end_head_info_datestamp_time _ARTICLE_DATE_TIME'}) # 기사 날짜만 가져옴.
  date=news_date.get_text()
  
  result={
      'headline': headline,
      'date': date,
      'writer': writer,
      'section': section,
      'link': link,
      'text': text,
      }
  
  return result

def convert_sid2name(sid):
    sid = str(sid)

    # if source == 'krx':
    krx_api = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    data = {
        'bld': 'dbms/comm/finder/finder_stkisu',
        'searchText': sid,
    }
    
    r = session.post(krx_api, data=data, headers=utils.HEADERS)
    b = bs(r.content, 'html.parser')
    b_json = json.loads(b.text)

    content = b_json['block1']
    if content:
        return content[0]['codeName']
    else:
        # print(f'{sid} code name not found in KRX system. None is returned.')
        pass
    
    # elif source == 'k5': # https://k5.co.kr/
    k5_url = 'https://k5.co.kr/stock/do_typehead_search_stock?q='
    r = session.get(k5_url + sid, headers=utils.HEADERS)
    r_json = json.loads(r.text)

    content = r_json['data']
    if content:
        return content[0]['stock_name']
    else:
        # print(f'{sid} code name not found in K5 system. None is returned.')
        return None