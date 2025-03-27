import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Пути для Chromium
CHROME_DRIVER_PATH = "/snap/bin/chromium.chromedriver"
CHROMIUM_BINARY = "/snap/chromium/3067/usr/lib/chromium-browser/chrome"  # Путь к бинарному файлу Chromium
#COOKIES_FILE = "yandex_gpt_search/cookies.pkl"
COOKIES_FILE = "/home/rasp/Desktop/cheburator/chebur_package/yandex_gpt_search/cookies.pkl"

def init_driver(headless=True):
    """Запускает браузер, загружает cookies и выполняет авторизацию."""
    options = Options()
    options.binary_location = CHROMIUM_BINARY  # Указываем путь к бинарному файлу Chromium
    # if headless:
    #    options.add_argument("--headless=new")  # Запускаем браузер в фоне
    #options.add_argument("--headless") 
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Инициализация драйвера
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://alice.yandex.ru/")

    try:
        # Загружаем cookies
        with open(COOKIES_FILE, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()
    except FileNotFoundError:
        pass

    time.sleep(5)

    #if "Войти" in driver.page_source:
       # input()  # Ждём авторизации вручную
       # with open(COOKIES_FILE, "wb") as file:
       #     pickle.dump(driver.get_cookies(), file)
      #  driver.refresh()
       # time.sleep(3)

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

        time.sleep(8)  # Ждём ответа

        # Ищем все ответы
        response_elements = driver.find_elements(By.CSS_SELECTOR, ".markdown-text.markdown-text_standalone span")

        if response_elements:
            return response_elements[-1].text  # Берём последний ответ
        else:
            return "Ответ не найден."
    except Exception as e:
        return f"Ошибка: {e}"


def close_driver(driver):
    """Закрывает браузер."""
    driver.quit()


#if __name__ == "__main__":
  #  driver = init_driver()
  #  print('init')
  #  time.sleep(5)
  #  response = ask_yandex_gpt(driver, "Привет, расскажи шутку!")
 #   print("烙 Ответ от Яндекс GPT:", response)
  #  input(" Нажмите Enter, чтобы завершить...")
  #  close_driver(driver)

