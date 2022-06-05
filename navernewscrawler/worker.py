from navernewscrawler import scraper, utils
import json
from tqdm import tqdm

def generate_ii_newsdata(
    sid, 
    kospi_ii2dates, 
    kosdaq_ii2dates,
    kospi_ii2codename,
    kosdaq_ii2codename,
    reverse=True,
    ): # saves data and return only sid
    
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
    if reverse:
        yearmonth = yearmonth[::-1]
    
    di_groupby_ym = di_list.groupby(yearmonth)
    
    # generate directory
    utils.generate_dirs(sid, min(di_list), max(di_list))

    # iterate by month. 
    print(f'Start downloading news: {sid}:{codename} from {di_list.min().date()} to {di_list.max().date()} ({len(di_list)} days)')
    for year, month in yearmonth:
        json_result = {'data': []}
        save_dir = utils.BASE_DIR / sid / f'{year:04}' / f'{month:02}'
        filepath = save_dir / f'{sid}_{year:04}{month:02}.json'

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
                
                news_link_list = scraper.get_news_list(url)

                if not news_link_list:
                    break
                else:
                    news_link_data += news_link_list
                    naver_start_idx += 1
            
            # get each article's data
            for link_data in news_link_data:
                article_url = link_data['news_url']
                news_company = link_data['company']
                title = link_data['title']

                naver_news_prefix = 'news.naver.com'
                if naver_news_prefix in article_url:
                    article_data = scraper.article_crawling(article_url)

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
    
        with open(filepath, 'w', encoding='utf-8') as j:
            json.dump(json_result, j)
        
    return sid




            

            
    