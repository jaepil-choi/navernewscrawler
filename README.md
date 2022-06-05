# 네이버 뉴스 크롤러

## 소개

- 네이버 뉴스에서 종목명을 검색하며 뉴스 제목/본문 및 각종 부가 데이터를 수집합니다. 
- 실행을 위해선 종목정보 등의 여러 `pickle` 파일들이 필요합니다. (현 저장소에 포함되어있음)
    - 다만, 2014-01-01 ~ 2022-05-19 사이 존재한 종목들을 기반으로 합니다.

### 특징

- 네이버 뉴스 페이지로 넘어갈 수 있는 기사들만 본문 데이터가 존재합니다. (신문사 고유 페이지만 있는 경우 제외)
- 수집한 데이터를 종목별/연도별/월별 로 나눠 `json` 형식으로 저장합니다. 
- `multiprocessing` 모듈을 사용하여 빠른 병렬 크롤링이 가능합니다. 
- 월별로 순차적으로 데이터를 처리하기에 메모리에 큰 부담을 주지 않습니다. 
- 주피터 노트북이 아닌 파이썬 패키지 형태로 구조화되어있고 CLI를 갖춰 유지보수 및 사용이 간편합니다. 

### 수집 데이터 상세

(기사 데이터 1개에 대하여)
- `market`: KOSPI, KOSDAQ 시장 종류
    - 가장 마지막 날짜를 기준으로 하는만큼, KOSDAQ -> KOSPI 되어 데이터 기간 동안 두 군데 다 있던 종목이 존재할 수도 있음.
- `sid`: KRX 종목코드
- `codename`: 종목 이름 (상장폐지되어 검색 안되는 것들도 존재)
- `year`: 기사 입력 연도
- `month`: 기사 입력 월
- `article_url`: 네이버 뉴스 검색에서 기사로 넘어가는 링크
    - 일부는 news.naver.com 도메인을 따르고, 일부는 자체 신문사 원본 링크를 가짐
- `news_company`: 신문사 이름
- `title`: 뉴스 제목

(이하 news.naver.com 도메인을 따르는 경우만 존재)
- `headline`: 뉴스 제목 (=title)
- `date_str`: 뉴스 입력 날짜 (나와있는 그대로 `str` 형태)
- `writer`: 기자 이름
- `section`: 기사 하단에 있는, 기자가 분류한 
- `original_article_link`: 자체 신문사 원본 링크
- `article_body`: 기사 본문

## 사전 준비

### 터미널을 켜 코드를 다운로드받은 폴더 위치로 이동

- 터미널(cmd, powershell, conda 등을 켜서 코드 다운로드 받은 위치로 이동)

### 사전 준비할 파일들

- 필요한 1+4개의 pickle 파일들을 해당 위치에 복붙하기
    - 1. (각자 다름) `sid_list.pickle`
    - 2. `kosdaq_ii2codename_combined.pickle`
    - 3. `kospi_ii2codename_combined.pickle`
    - 4. `kosdaq_ii2dates.pickle`
    - 5. `kospi_ii2dates.pickle`

### 본인 컴퓨터 사양, 용량 확인하기

- `ctrl + shift + esc` 를 눌러 작업관리자를 켜고 `성능` 탭에서 CPU 그래프 아래의 '논리 프로세서' 갯수를 확인합니다.
- 다운로드 할 용량도 충분히 있는지 확인 (아무리 커도 15GB 안될껍니다)

### 성능 벤치마크
- `-p 12`로 12 프로세스로 돌렸을 때 1종목을 2014.01 ~ 2022.05 까지 모으는데 약 6분 
- 용량도 5MB 정도밖에 안나옴. 
- 1000개 종목에 대해 모은다고 해도, 단순 계산해보면:
    - 소요 시간: (1000개 / 12프로세스) * 6분 = 500분
    - 용량: 1000개 * 5MB = 5GB

## 실행

- `sid_list_01.pickle` 등의 pickle 파일은 500개 종목씩 나눠져 있습니다. 이 중 한 파일을 `sid_list.pickle` 로 이름을 바꿔줍니다. 
    - 팀원끼리 나눠서 한다면 01, 02, 03 번을 누가 돌릴지 정하고 나눠서 돌릴 수 있습니다. 
- 해당 위치의 터미널에서 `python main.py -p 논리프로세서갯수` 명령을 실행합니다. 

### 오류 발생시

- 패키지 ~~가 설치되어있지 않다고 할 때:
    - (conda): conda install -c conda-forge 패키지명
    - (pip): pip install 패키지명
