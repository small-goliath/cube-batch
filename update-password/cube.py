import os
from time import sleep
from dotenv import load_dotenv
import logging
import logging.config
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logging.config.fileConfig('logging.conf')
log = logging.getLogger('cube')

load_dotenv()

referer = os.getenv("referer")
home = os.getenv("home")

driver = None

def setup():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=chrome")
    options.add_argument("profile-directory=Default")
    options.add_argument('remote-debugging-port=9999')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(1.5)
    driver.set_page_load_timeout(5)
    driver.get(referer)

    return driver

def login():
    global driver

    driver = setup()

    login_button = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div/button/span")
    if login_button and login_button[0]:
        log.info("cube 로그인 중...")
        login_button[0].click()
    sleep(1)

    account_button = driver.find_elements(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/form/span/section/div/div/div/div/ul/li[1]")
    if account_button and account_button[0]:
        log.info("Google OAuth2 로그인 중...")
        account_button[0].click()
        password_input_box = driver.find_elements(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
        if password_input_box and password_input_box[0]:
            password_input_box[0].send_keys(os.getenv("password"))
            submit = driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span')
            submit.click()

def change(old_password: str, new_password: str):
    sleep(5)
    log.info(f"비밀번호 변경 중... [{old_password}] to [{new_password}]")

    driver.get(referer)
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "table-bordered")))
    change_password_button = driver.find_element(by=By.CLASS_NAME, value="btn-secondary")
    change_password_button.click()

    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.NAME, "password")))
    current_text_box = driver.find_element(by=By.NAME, value="password")
    current_text_box.send_keys(old_password)

    new_text_box = driver.find_element(by=By.NAME, value="newPassword")
    new_text_box.send_keys(new_password)

    confirm_text_box = driver.find_element(by=By.NAME, value="newConfirmPassword")
    confirm_text_box.send_keys(new_password)

    save_button = driver.find_element(by=By.CLASS_NAME, value="modal-content").find_element(by=By.CLASS_NAME, value="modal-footer").find_element(by=By.CLASS_NAME, value="btn-success")
    save_button.click()