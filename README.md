# Голосовой ассистент Чебурашка
Голосовой помощник Чебурашка — это умный ассистент, который распознает речь, отвечает на вопросы с помощью **YandexGPT** и синтезирует голос Чебурашки.  
Он умеет искать информацию, рассказывать анекдоты и выполнять голосовые команды.
## Структура проекта
```chebur-assistant/
│── chebur_package/
│   ├── STT_vosk/                # Распознавание речи (Vosk)
│   ├── speech_synthesis/        # Синтез речи
│   ├── yandex_gpt_search/       # Поиск с Yandex GPT
    │── main.py                  # Главный файл ассистента
│── requirements.txt              # Список зависимостей
│── README.md                     # Документация проекта

```


## 🚀 Начало работы

Клонирование репозитория
```
git clone https://github.com/Madic228/Cheburashka.git
```

Установка зависимостей
```
pip install -r requirements.txt
```


Перед запуском ассистента необходимо выполнить несколько шагов по настройке:

### 1️⃣ Получение cookies для YandexGPT
Чтобы поиск через **YandexGPT** работал корректно, нужно выполнить следующие действия:  
1. Запустите файл **`chebur_package/yandex_gpt_search/get_cookies.py`**  
   ```bash
   python chebur_package/yandex_gpt_search/get_cookies.py
   ```
2. Откроется браузер — авторизуйтесь в Яндекс.
3. После успешной авторизации появится файл `cookies.pkl` в папке `yandex_gpt_search`.

### 2️⃣ Настройка профиля Google Chrome
1. Создайте новый профиль в Google Chrome.
2. Войдите в свой Google-аккаунт в этом профиле.
3. Найдите путь к папке с профилем:
   Откройте Chrome и перейдите в ```chrome://version/ ```
   Найдите строку "Путь к профилю"
   Например
   ```
   C:\Users\ТВОЙ_ЛОГИН\AppData\Local\Google\Chrome\User Data\Profile 3
   ```
4. Откройте файл chebur_package/speech_synthesis/tts_selenium.py
5. Укажите найденный путь в коде:
```
# Укажите путь к профилю Chrome с сохраненной учетной записью
user_data_dir = r"C:\Users\USERNAME\AppData\Local\Google\Chrome\User Data"

options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Путь к Chrome
options.add_argument(f"--user-data-dir={user_data_dir}")  # Подключаем профиль пользователя
options.add_argument("--profile-directory=Profile 3")  # Укажите свой профиль!
# options.add_argument("--remote-debugging-port=9222")
```

#### 📌 Важно!

Замените USERNAME на свое имя пользователя в Windows.
Если ваш профиль называется Profile 2, Default или другой, укажите его.

### 3️⃣ Завершение всех процессов Chrome
Прежде чем запускать ассистента, убедитесь, что Chrome полностью закрыт: 

✅ Завершите процесс chrome.exe через Диспетчер задач (Ctrl + Shift + Esc) 

✅ Или выйдите из Chrome через панель быстрого доступа (стрелочка в правом нижнем углу)

### 4️⃣ Запуск ассистента
Теперь все готово! Запустите ассистента командой:
```
python chebur_package/main.py
```


### /////////////Подключение///////////////
Для подключение без знания IP address:
1. ssh rasp@raspberrypi.local
2. hostname -I
3. Открыть RDP и ввести IP-address

Login: rasp
pass: 1

### Клонирование голоса:

Переходите на сайт
https://www.minimax.io/audio/voices

Нажимаете Create your Voice Clone

В Step 1. Import Voice вставляете этот файл: https://drive.google.com/file/d/1ecsrgQV_9aBclx70l9ohMIzWjzNlBWwg/view?usp=sharing

Или любой другой с чистым голосом Чебурашки.

После создание не забудьте в Voices выбрать нужный голос!

### Включение/отключение браузера
Для работы браузера в фоном режиме добавьте в файлы 
#options.add_argument("--headless") #  Запускаем браузер в фоне

# Инструкция по управлению сервисом `cheburashka.service` и процессами Chromium

### Основные команды:
1. Включить сервис: `sudo systemctl start cheburashka.service`
2. Отключить сервис: `sudo systemctl stop cheburashka.service`
3. Перезапустить сервис: `sudo systemctl restart cheburashka.service`
4. Проверить статус сервиса: `sudo systemctl status cheburashka.service`
5. Завершить процесс Chromium: `sudo kill <PID>`
6. Принудительно завершить процесс Chromium: `sudo kill -9 <PID>`
7. Завершить все процессы Chromium: `sudo killall chromium`
8. Просмотреть PID процессов Chromium: `pgrep -a chromium`
9. Просмотр логов sudo journalctl -u cheburashka.service
   


