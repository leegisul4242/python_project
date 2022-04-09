#!/usr/bin/env python
# coding: utf-8

# # 1. 환율 스크린샷

# # 라이브러리 선언

# #라이브러리 선언
# from selenium import webdriver
# 
# from selenium.webdriver.common.keys import Keys   # 셀레니움 폴더안에다 web드라이버.py 라는거 넣은거래
# import warnings
# warnings.filterwarnings(action="ignore")
# 
# 
# # 드라이버 위치 설정
# driver_loc = "../externlib/chromedriver/chromedriver.exe" #학교 크롬 버전 드라이버 위치
# 
# 
# # 드라이버 옵션 설정
# options = webdriver.ChromeOptions()
# options.add_argument("window-size=1920x1080")
# 
# 
# # 헤드리스(for.리눅스)
# # 웹 드라이버 정의
# driver = webdriver.Chrome(driver_loc, options=options)

# ### -- 페이지로 이동(네이버)

# ## 네이버 페이지로 이동
# # URL 정의
# baseUrl = "https://www.naver.com"
# # URL 이동
# driver.get(baseUrl)

# ### -- scrchBox에 값 입력 ("환율")

# ## 네이버 serchBox에 "환율"입력
# naverSerchBox = '//*[@id="query"]'
# inputKey = "환율"
# driver.find_element_by_xpath(naverSerchBox).send_keys(inputKey)  #네이버 입력box "환율"입력
# driver.find_element_by_xpath(naverSerchBox).send_keys(Keys.ENTER) # 엔터

# ### -- 스크린샷 생성

# ## 스크린샷 찍기
# driver.save_screenshot("./USD_{}.png".format(timeLog))

# ---

# In[ ]:





# # [여기서부터가 진짜 시작]

# # *시가총액 50위 페이지이동- 스크린샷 생성(with 셀레니움)
# # *시가총액 50위 웹크롤링(테이블)(with bs4)- csv파일생성

# ### (timelog 생성)

# In[8]:


### 파일 저장시 붙일 timeLog 준비
from datetime import *
# currentTime = datetime.now().date()
currentTime = datetime.now()
nowTime = currentTime.strftime("%Y-%m-%d_%H_%M_%S")

timeLog = "{}".format(nowTime)
timeLog


# # 1.시가총액 - 스크린샷 생성

# In[9]:


### 1.라이브러리 선언
from selenium import webdriver

from selenium.webdriver.common.keys import Keys   # 셀레니움 폴더안에다 web드라이버.py 라는거 넣은거래
import warnings
warnings.filterwarnings(action="ignore")


# 드라이버 위치 설정
driver_loc = "../externlib/chromedriver_home_lowVersion/chromedriver.exe" #집에서는 버전이 낮음. 학교에서할때는 고치기


# 드라이버 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# 헤드리스(for.리눅스)
# 드라이버 정의
driver = webdriver.Chrome(driver_loc, options=options)


# ### -- (참고)페이지로 이동

# ###2. 시가총액50위 페이지로 이동
# url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0"
# driver.get(url)

# ### -- 전체 스크린샷 생성(페이지 이동안해도 스크린샷 생성가능)

# In[10]:


#스크린샷 생성(크롬전체)
driver.get("https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0")
width = driver.execute_script("return document.body.scrollWidth") #스크롤 할 수 있는 최대 넓이
height = driver.execute_script("return document.body.scrollHeight") #스크롤 할 수 있는 최대 높이
driver.set_window_size(width, height) #스크롤 할 수 있는 모든 부분을 지정

# png파일로 저장
driver.save_screenshot("../screenshot/stockRank50_{}.png".format(timeLog))
#[출처] [Python] selenium을 사용한 웹 사이트 스크린샷|작성자 Narrow


# #### (참고)전체 스크린샷
# https://blog.naver.com/PostView.nhn?blogId=ky_s1919&logNo=222187990565

# ## 스크롤 스크린샷
# import pyscreenshot as ImageGrab
# screenshot = ImageGrab.grab()
# screenshot.save("./stockRank50_{}.png".format(timeLog)) ##실패 이건 전체화면 스크린샷이지. 웹페이지 스크롤이 아님

# ---

# # 2. 웹크롤링(테이블)- 시가총액 50위 정보 수집 - csv파일로저장 - 실행가능파일로만듬 - 윈도우스케쥴러 매일오후16시

# In[ ]:





# In[11]:


# 1.라이브러리 선언
import pandas as pd
import requests
import bs4

#2. 소스 가져오기
targetLink = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0"
resp = requests.get(targetLink)
htmlNatural = resp.text
bs = bs4.BeautifulSoup(htmlNatural, "html.parser")
bs


#3.테이블 정보 추출

table = bs.find(name="table", attrs={"summary":"코스피 시세정보를 선택한 항목에 따라 정보를 제공합니다."})
thList = table.findAll(name="th")
tbody = table.find(name="tbody")
trList = tbody.findAll(name="tr")
tdList=trList[1].findAll(name="td")



rowList=[]

columnValue = ""
columnList = []
nameList = [] #<th>=컬럼명 담을 리스트

for j in range (0, len(trList)):
    columnList=[]
    tdList=trList[j].findAll(name="td")
    for i in range (0, len(tdList),1):
        columnValue = tdList[i].text.replace("\t","").replace("\n","")
        columnList.append(columnValue)  
    #print((columnList[0]))
    if columnList[0]=="":  #[](실패:빈리스트아님)  ==None(실패:넌값아님.타입스트링)  ##No가 없다면, 그text는 종목명이 아니므로,컨티뉴하겠다. 즉, rowList에추가하지 않겠다.
        continue
    else :
        rowList.append(columnList)
        

for i in range (0,len(thList),1):
    thValue = thList[i].text
    nameList.append(thValue)  #이중포문 돌릴거 아니니까, 초기화 안해됨-나중에 질문하기


rowList
print(rowList[0][-1])#맨끝 토론실에 링크 넣어보기
finalDf  =pd.DataFrame(rowList, columns=nameList)

# csv파일로 저장
finalDf.to_csv("../dataset/stockRank50_{}.csv".format(timeLog),index=True,encoding="ms949")


# ---

# In[ ]:





# In[ ]:





# 1. 해외지수 스샷

# ## 네이버 serchBox에 "해외증시"입력
# 
# naverSerchBox = '//*[@id="nx_query"]'
# inputKey = "해외증시"
# driver.find_element_by_xpath(naverSerchBox).send_keys(inputKey)  #네이버 입력box "환율"입력
# driver.find_element_by_xpath(naverSerchBox).send_keys(Keys.ENTER) # 엔터

# naverButton ='//*[@id="rso"]/div[1]/div/div/div/div/div/div[1]/a/h3'
# driver.find_element_by_xpath(naverButton).click() #구글네이버검색한차에서 -네이버클릭
# 
# #네이버 웹페이지
# #네이버 검색창에 환율 입력
# inputKey = "환율"
# driver.find_element_by_xpath(naverSerch).send_keys(inputKey)

# # 방법2.구글검색키 입력 후 검색버튼 클릭

# #Keys.ENTER
# 
# driver.get(baseUrl)
# driver.find_element_by_xpath(googleSerchInput).send_keys(inputKey)
# # driver.find_element_by_xpath(googleSerchInput).send_keys(Keys.ESCAPE) #밑에 자동완성 창 뜨는거  빠져나오는
# 
# btnXpath = "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]"
# driver.find_element_by_xpath(btnXpath).click()

# /html/body/div[1]/div[3]/form/div[1]/div[1]/div[2]/div[2]/div[5]/center/input[1]

# /html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]
