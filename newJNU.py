from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

# 로그인 정보 설정
username = "2019108255"
password = "dnrwls12!"

# Chrome WebDriver 설정
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # 제주대학교 온라인 강의 웹사이트 열기
    driver.get("https://jnuclass.jejunu.ac.kr/")
    time.sleep(3)

    # 로그인 페이지로 이동
    login_page = driver.find_element(By.XPATH, "/html/body/main/div/div[1]/div/div[2]/div[2]/a")
    login_page.click()
    time.sleep(3)

    # 로그인 정보 입력
    wait = WebDriverWait(driver, 20)
    username_input = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/form/div[2]/span/input")))
    password_input = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/form/div[3]/span/input")
    login_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/form/div[4]/a")

    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()
    time.sleep(5)

    # 첫 번째 강의로 이동 (전체 XPath 사용)
    lecture_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/div[1]/div/div[2]/div[2]/div[1]")))
    lecture_tab.click()
    time.sleep(3)

    # 특정 강의로 이동
    specific_lecture = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div/div[5]/div/div[1]/div/div[1]")))
    specific_lecture.click()
    time.sleep(3)

    # 강의 재생 페이지로 이동
    play_lecture = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[2]/nav/ul/li[5]/a")))
    play_lecture.click()
    time.sleep(5)

    # 첫 번째 iframe으로 전환
    iframe = driver.find_element(By.ID, "tool_content")
    driver.switch_to.frame(iframe)
    time.sleep(2)
    print("첫 번째 iframe으로 전환 성공")

    # 모바일모델(1-1)-무선인터넷의 개요 강의 클릭
    try:
        module_link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '모바일모델(1-1)-무선인터넷의 개요')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", module_link)
        driver.execute_script("arguments[0].click();", module_link)
        time.sleep(5)
        print("모바일모델(1-1)-무선인터넷의 개요 강의를 재생합니다.")
    except TimeoutException:
        print("지정된 요소를 찾는 데 실패했습니다. 시간을 더 늘리거나 선택자를 확인해 주세요.")

    # iframe 컨텍스트에서 벗어나기
    driver.switch_to.default_content()
    time.sleep(2)
    print("iframe 컨텍스트에서 벗어났음!")

    # 새로운 페이지에서 첫 번째 iframe으로 다시 전환
    new_iframe = wait.until(EC.presence_of_element_located((By.ID, "tool_content")))
    driver.switch_to.frame(new_iframe)
    time.sleep(2)
    print("새로운 페이지에서 첫 번째 iframe으로 전환 성공")

    # 두 번째 iframe으로 전환 (중첩된 iframe 접근)
    try:
        inner_iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.xnlailvc-commons-frame")))
        driver.switch_to.frame(inner_iframe)
        time.sleep(2)
        print("두 번째 iframe으로 전환 성공")

        # 재생 버튼 찾기 및 클릭 (마우스 액션 사용)
        play_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".vc-front-screen-play-btn")))
        driver.execute_script("arguments[0].scrollIntoView(true);", play_button)
        ActionChains(driver).move_to_element(play_button).click().perform()
        print("강의 재생 버튼을 클릭했습니다.")

        # 일시정지 버튼 클릭 (마우스 액션 사용)
        pause_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".vc-pctrl-play-pause-btn.vc-pctrl-on-playing")))
        driver.execute_script("arguments[0].scrollIntoView(true);", pause_button)
        ActionChains(driver).move_to_element(pause_button).click().perform()
        print("일시정지 버튼을 클릭했습니다.")
        time.sleep(2)

        # 다시 재생 버튼 클릭 (마우스 액션 사용)
        play_button_again = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".vc-pctrl-play-pause-btn.vc-pctrl-on-pause")))
        driver.execute_script("arguments[0].scrollIntoView(true);", play_button_again)
        ActionChains(driver).move_to_element(play_button_again).click().perform()
        print("다시 재생 버튼을 클릭했습니다.")

        # 비디오 태그 직접 재생 시도
        driver.execute_script("""
            var video = document.querySelector('video');
            if (video) {
                video.play();
                console.log('비디오 재생을 시도했습니다.');
            } else {
                console.log('비디오 요소를 찾을 수 없습니다.');
            }
        """)
        print("비디오 직접 재생을 시도했습니다.")

        # 재생 후 대기
        print("재생이 완료되었습니다. 브라우저를 닫기 전에 확인해 주세요.")
        time.sleep(60)  # 사용자 확인을 위해 대기 시간 추가

    except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
        print("재생 버튼을 찾는 데 실패했습니다. 시간을 더 늘리거나 선택자를 확인해 주세요.")

finally:
    # 드라이버 종료
    driver.quit()
