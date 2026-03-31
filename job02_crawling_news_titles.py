# webdriver 사용 예제
#
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import datetime
import re

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

options = ChromeOptions()
options.add_argument('lang=ko_KR')
# options.add_argument('headless')    # 메모리 상에서는 브라우저가 동작 중이나 화면에는 띄워지지 않게 하는 옵션

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
my_section = 5
url = "https://news.naver.com/section/10{}".format(my_section) # 100(Politics), 101(Economic), 102(Social), 103(Culture), 104(World), 105(IT)
driver.get(url)
time.sleep(0.5) # browser 로딩 시간 확보

# //*[@id="newsct"]/div[4]/div/div[2] # X-path : 특정 id부터 hierarchy 참조 # / 표시 : 하위 tag 를 참조할 때 사용.
# /html/body/div/div[2]/div[2]/div[2]/div[4]/div/div[2] # full X-path : 전체 tag hierarchy 보기

# 버튼 클릭 driver
# for i in range(5):
#     time.sleep(0.5)
#     button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'
#     driver.find_element(By.XPATH, button_xpath).click()
# time.sleep(5)
# while True:
#     try:
#         button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'
#         driver.find_element(By.XPATH, button_xpath).click()
#     except:
#         break
today_str = datetime.datetime.now().strftime('%Y.%m.%d.')  # ex: '2026.03.30.'

while True:
    try:
        # 더보기 버튼 클릭
        button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'
        driver.find_element(By.XPATH, button_xpath).click()
        time.sleep(0.5)

        # 현재 페이지에 로드된 기사들의 날짜 요소 확인
        date_elements = driver.find_elements(By.CLASS_NAME, 'sa_text_datetime')

        if date_elements:
            last_date_text = date_elements[-1].text  # 가장 마지막(오래된) 기사의 날짜

            # "N분전", "N시간전" → 오늘 기사이므로 계속 진행
            # "2026.03.30." → 오늘 날짜이므로 계속 진행
            # "2026.03.29." → 어제 이전 날짜이므로 중단

            # 날짜 형식(YYYY.MM.DD.)이 나타났고, 오늘 날짜가 아닌 경우 중단
            if re.match(r'\d{4}\.\d{2}\.\d{2}\.', last_date_text):
                if last_date_text.strip() != today_str:
                    print(f"오늘이 아닌 날짜 발견: {last_date_text} → 더보기 중단")
                    break

    except Exception as e:
        print(f"더보기 버튼 없음 또는 오류: {e}")
        break

time.sleep(0.5)
title_tags = driver.find_elements(By.CLASS_NAME, 'sa_text_strong')

today_str = datetime.datetime.now().strftime('%Y.%m.%d.')  # ex: '2026.03.30.'
titles = []
for title_tag in title_tags:
    titles.append(title_tag.text)
df_titles = pd.DataFrame(titles, columns=['title'])
df_titles['category'] = category[my_section]  # 섹션별로 카테고리 값 변경
print(df_titles.head())
df_titles.info()
df_titles.to_csv('./crawling_data/IT/naver_headline_news_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
# df_titles.to_csv('news_titles_{}.csv'.format(category[my_section]), index=False)
