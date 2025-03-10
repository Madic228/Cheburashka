import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Укажи путь к chromedriver.exe
chrome_driver_path = r"..\chebur_package\speech_synthesis\chromedriver.exe"

# Укажи путь к профилю Chrome с сохраненной учетной записью
user_data_dir = r"C:\Users\USERNAME\AppData\Local\Google\Chrome\User Data"

options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Путь к Chrome
options.add_argument(f"--user-data-dir={user_data_dir}")  # Подключаем профиль пользователя
options.add_argument("--profile-directory=Profile 3")  # Используем основной профиль
#options.add_argument("--remote-debugging-port=9222")


# Запуск Chrome с профилем
# Создаем объект службы ChromeDriver
service = Service(chrome_driver_path)

# Запускаем Chrome с профилем
driver = webdriver.Chrome(service=service, options=options)

# Открываем сайт
driver.get("https://www.minimax.io/audio")


def close_popup():
    """Удаляет всплывающее окно, если оно есть."""
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "section.fixed.bottom-0.left-0.right-0.top-0"))
        )
        driver.execute_script("""
               var popup = document.querySelector("section.fixed.bottom-0.left-0.right-0.top-0");
               if (popup) { popup.remove(); }
           """)
        print("✅ Попап удален!")
    except Exception:
        print("⚠️ Попап не найден.")


def generate_speech(text):
    try:
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.ant-input"))
        )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", input_field)

        # Очищаем поле стандартным методом Selenium
        input_field.clear()
        # Эмулируем выделение и удаление текста
        input_field.send_keys(Keys.CONTROL + "a")
        input_field.send_keys(Keys.BACKSPACE)

        # Небольшая задержка, если нужно дать фреймворку время обновиться
        time.sleep(0.5)

        # Вводим новый текст
        input_field.send_keys(text)
        print("✅ Текст введен!")

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.generate-btn.md\\:block.hidden button"))
        )
        button.click()
        print("✅ Кнопка нажата!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


# Пример использования
# if __name__ == "__main__":
#     generate_speech("Привет, это тест озвучки!")
#     time.sleep(10)
#     generate_speech("Привет, чебур это ты!")
#     # Оставляем браузер открытым, пока не нажмёшь Enter
#     input("Нажми Enter, чтобы закрыть браузер...")
#     driver.quit()