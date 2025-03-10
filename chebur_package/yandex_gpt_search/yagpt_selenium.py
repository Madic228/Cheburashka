import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

COOKIES_FILE = "yandex_gpt_search/cookies.pkl"

def init_driver(headless=True):
    """Запускает браузер, загружает cookies и выполняет авторизацию."""
    options = webdriver.ChromeOptions()
    # if headless:
    #    options.add_argument("--headless=new")  # Запускаем браузер в фоне
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://alice.yandex.ru/")

    try:
        with open(COOKIES_FILE, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()
    except FileNotFoundError:
        pass

    time.sleep(5)

    if "Войти" in driver.page_source:
        input()  # Ждём авторизации вручную
        with open(COOKIES_FILE, "wb") as file:
            pickle.dump(driver.get_cookies(), file)
        driver.refresh()
        time.sleep(3)

    return driver  # Возвращаем объект driver

def ask_yandex_gpt(driver, query):
    """Отправляет запрос в чат Яндекс GPT и возвращает последний ответ."""
    try:
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.inputbase-textarea"))
        )
        input_field.click()
        input_field.send_keys(query)
        input_field.send_keys(Keys.RETURN)

        time.sleep(8)  # Увеличил время ожидания, чтобы нейросеть успела ответить

        # Ищем все ответы
        response_elements = driver.find_elements(By.CSS_SELECTOR, ".markdown-text.markdown-text_standalone span")

        if response_elements:
            return response_elements[-1].text  # Берём последний ответ
        else:
            return ""
    except:
        return ""

def close_driver(driver):
    """Закрывает браузер."""
    driver.quit()
