from navernewscrawler import scraper, utils
import json
from tqdm import tqdm

import time
from datetime import datetime, timedelta

def generate_ii_newsdata(
    sid, 
    kospi_ii2dates, 
    kosdaq_ii2dates,
    kospi_ii2codename,
    kosdaq_ii2codename,
    reverse=True,
    continue_from_leftoff=True,
    ): # saves data and return only sid
    
    start_time = time.time()

    ## set market
    market = None
    if (sid in kospi_ii2dates) and (sid in kosdaq_ii2dates):
        kospi_max_date = kospi_ii2dates[sid]
        kosdaq_max_date = kosdaq_ii2dates[sid]

        if kospi_max_date >= kosdaq_max_date:
            market = 'kospi'
        else:
            market = 'kosdaq'
    elif sid in kospi_ii2dates:
        market = 'kospi'
    elif sid in kosdaq_ii2dates:
        market = 'kosdaq'
    else:
        raise Exception(f'sid {sid} in neither KOSPI nor KOSDAQ')

    if market == 'kospi':
        ii2dates = kospi_ii2dates
        ii2codename = kospi_ii2codename
    elif market == 'kosdaq':
        ii2dates = kosdaq_ii2dates
        ii2codename = kosdaq_ii2codename

    ## scrape data
    di_list = ii2dates[sid]
    codename = ii2codename[sid]

    naver_start_idx = 1
    
    yearmonth =  [(d.year, d.month) for d in di_list]
    di_groupby_ym = di_list.groupby(yearmonth)

    yearmonth = list(set(yearmonth))
    yearmonth.sort(reverse=reverse)
    
    # generate directory
    utils.generate_dirs(sid, min(di_list), max(di_list))

    # iterate by month. 
    print(f'Start downloading news: {sid}:{codename} from {di_list.min().date()} to {di_list.max().date()} ({len(di_list)} days)\n')
    article_count = 0
    for year, month in yearmonth:
        json_result = {'data': []}
        save_dir = utils.BASE_DIR / sid / f'{year:04}' / f'{month:02}'
        filepath = save_dir / f'{sid}_{year:04}{month:02}.json'

        if filepath.exists() and continue_from_leftoff:
            with open(filepath, 'r') as j:
                existing_data = json.load(j)
            
            modified_at = filepath.lstat().st_mtime
            modified_at = datetime.fromtimestamp(modified_at)
            tolerance_date = datetime.today() - timedelta(days=utils.UPDATE_TOLERANCE_DAY)
            is_recently_scraped = (modified_at < tolerance_date) # Temporary not using this condition because many companies already have empty data

            if not existing_data['data']:
                pass # Proceed & overwrite because existing data is empty and old
            else:
                continue 

        monthly_di_list = di_groupby_ym[(year, month)]

        for di in monthly_di_list:
            news_link_data = []

            # get article link data from news search page
            while 1: # loop until there's no more news link
                url = scraper.naver_news_search_url(
                    codename, 
                    naver_start_idx, 
                    utils.DateUtil.timestamp_2_intDate(di),
                    )
                try:
                    news_link_list = scraper.get_news_list(url)
                except Exception as e:
                    news_link_list = []

                    print(f'Error(1) while getting news links - {sid}:{codename}')
                    print(repr(e))

                if not news_link_list:
                    break
                else:
                    news_link_data += news_link_list
                    naver_start_idx += 10
            
            # get each article's data
            for link_data in news_link_data:
                article_url = link_data['news_url']
                news_company = link_data['company']
                title = link_data['title']

                naver_news_prefix = 'news.naver.com'
                if naver_news_prefix in article_url:
                    try:
                        article_data = scraper.article_crawling(article_url)
                    except:
                        print(f'Error(2) while getting news article data - {sid}:{codename}')
                        print(repr(e))
                        continue

                    headline = article_data['headline']
                    date_str = article_data['date'] # should be same as di but in naver date str format
                    writer = article_data['writer']
                    section = article_data['section']
                    original_article_link = article_data['link']
                    article_body = article_data['text']
                else:
                    headline = None
                    date_str = None
                    writer = None
                    section = None
                    original_article_link = None
                    article_body = None

                result = {
                    'market': market,
                    'sid': sid,
                    'codename': codename,
                    'year': year,
                    'month': month,

                    "article_url": article_url,
                    "news_company": news_company,
                    "title": title,
                    "headline": headline,
                    "date_str": date_str,
                    "writer": writer,
                    "section": section,
                    "original_article_link": original_article_link,
                    "article_body": article_body,
                }

                json_result['data'].append(result)

        article_count += len(json_result['data'])
        with open(filepath, 'w', encoding='utf-8') as j:
            json.dump(json_result, j)
            # print(f'Dump succedded at {filepath}, length: {json_result["data"]}')
    
    end_time = time.time()

    print(f'[{utils.timestamp2formatted(end_time)}] {sid}:{codename} Finished. \
/ {article_count} articles \
/ Elapsed: {timedelta(seconds=(end_time - start_time))}') 

    return sid




            

            
    