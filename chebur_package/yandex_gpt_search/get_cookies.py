import pickle
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://alice.yandex.ru/")

input("Авторизуйтесь вручную, затем нажмите Enter")

# Сохраняем cookies в файл
with open("cookies.pkl", "wb") as file:
    pickle.dump(driver.get_cookies(), file)

print("Cookies сохранены!")
driver.quit()
