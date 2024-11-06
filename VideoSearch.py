from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 검색하고자 하는 키워드 설정
search_keyword = "고양이"

# Chrome WebDriver 설정
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # 브라우저 창을 열지 않음
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # YouTube 웹사이트 열기
    driver.get("https://www.youtube.com/")
    time.sleep(3)

    # 검색창 찾기 및 검색어 입력 후 엔터
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys(search_keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    # 검색 결과에서 제목과 URL 추출
    video_elements = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
    for video in video_elements:
        title = video.get_attribute("title")
        url = video.get_attribute("href")
        if title and url:
            print(f"제목: {title}")
            print(f"URL: {url}")
            print("-")
finally:
    # 드라이버 종료
    driver.quit()
