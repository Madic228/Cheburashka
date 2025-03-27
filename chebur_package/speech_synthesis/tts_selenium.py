# файл: selenium_chromium_minimax.py
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Путь к Chromium WebDriver (chromedriver)
chrome_driver_path = "/snap/bin/chromium.chromedriver"

# Путь к профилю Chromium (Profile 3)
user_data_dir = "/home/rasp/snap/chromium/common/chromium"

# Настройка параметров браузера
options = webdriver.ChromeOptions()
options.binary_location = "/snap/chromium/3067/usr/lib/chromium-browser/chrome"  # Путь к исполняемому файлу Chromium
options.add_argument(f"--user-data-dir={user_data_dir}")  # Подключаем профиль пользователя
options.add_argument("--profile-directory=Profile 3")  # Используем профиль 3
options.add_argument("--no-sandbox")  # Нужно для некоторых версий Chromium в snap
options.add_argument("--disable-dev-shm-usage")  # Уменьшает использование памяти в контейнерах
#options.add_argument("--headless") #  Запускаем браузер в фоне

# Запускаем Chromium с профилем
service = Service(chrome_driver_path)
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


def select_russian_language():
    """Выбирает русский язык в выпадающем списке."""
    try:
        # Открываем выпадающий список
        language_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.language-select div.ant-select-selector"))
        )
        language_select.click()
        print("✅ Выпадающий список языков открыт!")

        # Ждем появления списка
        dropdown_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ant-select-dropdown"))
        )

        # Скроллим список вниз с помощью JS
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", dropdown_container)
        #time.sleep(1)  # Ждем загрузки новых элементов

        # Повторяем несколько раз, если список длинный
        for _ in range(5):
            driver.execute_script("arguments[0].scrollTop += 100;", dropdown_container)
            #time.sleep(0.1)

        # Ищем Russian
        russian_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-select-item-option-content') and text()='Russian']"))
        )

        # Прокручиваем к нему
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", russian_option)
        #time.sleep(0.1)

        # Кликаем через JS, если обычный клик не работает
        driver.execute_script("arguments[0].click();", russian_option)
        print("✅ Выбран русский язык!")
    except Exception as e:
        print(f"❌ Ошибка при выборе языка: {e}")
        
def select_voice(voice_name="Cheburashka"):
    """Выбирает голос в списке."""
    try:
        # Открываем список голосов
        voice_selector = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "section.flex.cursor-pointer.items-center"))
        )
        voice_selector.click()
        print("✅ Открыт список голосов!")

        # Переходим во вкладку "My Voices"
        my_voices_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-node-key='TTS_voice_select_myvoice']"))
        )
        my_voices_tab.click()
        print("✅ Перешли на вкладку 'My Voices'!")

        # Даем время списку подгрузиться
        time.sleep(1)

        # Ищем нужный голос
        voice_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//h4/span[text()='{voice_name}']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", voice_option)
        time.sleep(0.5)

        # Ищем кнопку "Use" внутри этого div
        use_button = voice_option.find_element(By.XPATH, "./ancestor::div[contains(@class, 'group')]//div[contains(text(), 'Use')]")

        # Убедимся, что кнопка видна и кликабельна
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(use_button)
        )

        # Кликаем по кнопке через JS
        driver.execute_script("arguments[0].click();", use_button)
        print(f"✅ Голос '{voice_name}' выбран!")
        
    except Exception as e:
        print(f"❌ Ошибка при выборе голоса: {e}")


def generate_speech(text):
    """Вводит текст в поле и нажимает кнопку генерации"""
    try:
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.ant-input"))
        )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", input_field)

        # Очищаем поле стандартным методом Selenium
        input_field.clear()

        # Выделяем и удаляем текст (Linux: использует CONTROL вместо COMMAND)
        input_field.send_keys(Keys.CONTROL + "a")
        input_field.send_keys(Keys.BACKSPACE)

        # Небольшая задержка
        time.sleep(0.1)

        # Вводим новый текст
        input_field.send_keys(text)
        print("✅ Текст введен!")

        select_russian_language()
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.generate-btn.md\\:block.hidden button"))
        )
        button.click()
        print("✅ Кнопка нажата!")

        # Ждем, пока кнопка не станет неактивной, что означает завершение генерации
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.generate-btn.md\\:block.hidden button"))
        )

        # Получаем количество оставшихся символов
        remaining_chars_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='text-[13px] font-[600] text-brand_00']"))
        )
        remaining_chars = remaining_chars_element.text
        print(f"✅ Осталось символов: {remaining_chars}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")

# Пример использования
if __name__ == "__main__":
    #select_voice()
    select_russian_language()
    time.sleep(5)
    generate_speech("Привет, это тест озвучки!")
    time.sleep(10)
    generate_speech("Привет, чебур это ты!")
    input("Нажми Enter, чтобы закрыть браузер...")
    driver.quit()
