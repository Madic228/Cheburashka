import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Пути для Chromium
CHROME_DRIVER_PATH = "/snap/bin/chromium.chromedriver"
USER_DATA_DIR = "/home/rasp/snap/chromium/common/chromium"
CHROMIUM_BINARY = "/snap/chromium/3067/usr/lib/chromium-browser/chrome"

def load_cookies(driver):
    """Загружает cookies из файла в браузер."""
    try:
        with open("cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("Cookies загружены!")
    except FileNotFoundError:
        print("Файл cookies.pkl не найден.")
    except Exception as e:
        print(f"Ошибка при загрузке cookies: {e}")

def save_cookies(driver):
    """Сохраняет cookies из браузера в файл."""
    try:
        with open("cookies.pkl", "wb") as file:
            pickle.dump(driver.get_cookies(), file)
        print("Cookies сохранены!")
    except Exception as e:
        print(f"Ошибка при сохранении cookies: {e}")

def init_driver():
    """Инициализирует новый браузер без профиля и подгружает cookies."""
    options = Options()
    options.binary_location = CHROMIUM_BINARY
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")  # Для полноэкранного режима, можно убрать, если не нужно

    # Запускаем новый браузер
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    
    # Открываем сайт
    driver.get("https://alice.yandex.ru/")

    # Ждем несколько секунд, чтобы сайт успел подгрузиться
    driver.implicitly_wait(5)

    # Загружаем cookies
    load_cookies(driver)

    # Перезагружаем страницу, чтобы cookies подгрузились
    driver.refresh()

    return driver

# Основной код
if __name__ == "__main__":
    driver = init_driver()

    # Дожидаемся авторизации вручную и сохраняем cookies
    input("Пожалуйста, авторизуйтесь вручную, затем нажмите Enter...")

    # Сохраняем cookies в файл
    save_cookies(driver)

    # Закрываем браузер
    input("Нажмите Enter, чтобы закрыть браузер...")
    driver.quit()
