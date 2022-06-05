# 사용법

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

- `ctrl + shift + esc` 를 눌러 작업관리자를 켜고 `성능` 탭에서 CPU 칸이 몇 개나 있는지 세면 됨. 이 숫자를 기억. 
- 용량 충분히 있는지 확인 ()

### 성능 벤치마크
- `-p 12`로 12 프로세스로 돌렸을 때 1종목을 2014.01 ~ 2022.05 까지 모으는데 약 6분 
- 용량도 5MB 정도밖에 안나옴. 
- 1000개 종목에 대해 모은다고 해도, 단순 계산해보면:
    - 소요 시간: (1000개 / 12프로세스) * 6분 = 500분
    - 용량: 1000개 * 5MB = 5GB

## 실행

- 해당 위치의 터미널에서 아래 명령을 실행
- `python main.py -p 아까센숫자`

## 오류 발생시

- 패키지 ~~가 설치되어있지 않다고 할 때:
    - (conda): conda install -c conda-forge 패키지명
    - (pip): pip install 패키지명
