import pyaudio
import json
import random
import time
import threading
from vosk import Model, KaldiRecognizer
import wave
import simpleaudio as sa


from chebur_package.yandex_gpt_search.yagpt_selenium import init_driver, ask_yandex_gpt
from chebur_package.speech_synthesis.tts_selenium import generate_speech

# Загрузка модели
model = Model(r"STT_vosk/models_stt/vosk-model-small-ru-0.22")
recognizer = KaldiRecognizer(model, 16000)

# Настройка микрофона
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Фразы, которые нас интересуют
KEYWORDS = ["чебурашка"]

# Флаг для прерывания воспроизведения
is_speaking = False
start_time = 0  # Время начала ответа

def play_audio(file_path):
    """
    Функция для воспроизведения аудиофайла .wav
    """
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()


def play_audio_with_interrupt(file):
    """Функция воспроизведения с возможностью прерывания"""
    global is_speaking, start_time
    is_speaking = True
    start_time = time.time()

    def play():
        global is_speaking
        if is_speaking:  # Проверяем, можно ли продолжать воспроизведение
            play_audio(file)
        is_speaking = False  # Завершаем флаг после воспроизведения

    thread = threading.Thread(target=play)
    thread.start()


# ✅ Запускаем браузер в ОТДЕЛЬНОМ потоке
driver = None
driver_ready = threading.Event()  # Флаг готовности драйвера


def start_driver():
    global driver
    driver = init_driver(headless=True)
    driver_ready.set()  # Сообщаем, что браузер готов


threading.Thread(target=start_driver, daemon=True).start()  # Фоновый запуск браузера


def find_and_speak(text):
    wait_phrases = [
        "../chebur_package/STT_vosk/phrase/wait1.wav",
        "../chebur_package/STT_vosk/phrase/wait2.wav",
        "../chebur_package/STT_vosk/phrase/wait3.wav"
    ]
    # Запускаем озвучку в отдельном потоке
    threading.Thread(target=play_audio, args=(random.choice(wait_phrases),), daemon=True).start()

    """Функция обработки команды 'найди'"""
    text = text+" P.S. ответь по русски одним абзацем максимум на 150 символов, но если до P.S. передана бессмыслица, то ответь, что не понял вопроса, к тебе могут обращаться чебурашка игнорируй это не бред это нормально"
    driver_ready.wait()  # ⏳ Ждём, пока браузер полностью запустится
    response = ask_yandex_gpt(driver, text )

    if response:
        generate_speech(response)  # 🔊 Читаем ответ голосом
    else:
        play_audio_with_interrupt("../chebur_package/STT_vosk/phrase/sorri.wav")  # Если нет ответа, проигрываем "не понял"


# Команды и их обработчики
COMMANDS = {
    ("расскажи", "технопарк"): lambda: play_audio('../chebur_package/STT_vosk/phrase/techno.wav'),
    ("расскажи", "технологии", "технопарк"): lambda: play_audio('../chebur_package/STT_vosk/phrase/techno.wav'),
    ("расскажи", "аудитор", "ельцин"): lambda: play_audio('../chebur_package/STT_vosk/phrase/elcin.wav'),
    ("где", "столовая"): lambda: play_audio('../chebur_package/STT_vosk/phrase/canteen.wav'),
    ("найди",): find_and_speak,  # Теперь это обычная функция
    ("расскажи",): find_and_speak,
    ("что",): find_and_speak,
    ("кто",): find_and_speak,
    ("узнай",): find_and_speak,
    ("почему",): find_and_speak,
    ("сколько",): find_and_speak,
    ("как",): find_and_speak,
    ("объясни",): find_and_speak,
    ("зачем",): find_and_speak,
    ("где",): find_and_speak,
    ("когда",): find_and_speak,
    ("расскажи", "анекдот"): lambda: play_audio('../chebur_package/STT_vosk/phrase/anekdot1.wav'),
}

while True:
    data = stream.read(4000, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        text = result["text"]

        if any(keyword in text for keyword in KEYWORDS):  # Если в тексте есть "Чебурашка"
            words = text.split()  # Разбиваем текст на слова

            if len(words) == 1 and words[0] in KEYWORDS:  # Если сказано только "Чебурашка"
                print("Я слушаю вас!")

                # Воспроизведение случайного приветствия с возможностью прерывания
                audio_files = ["../chebur_package/STT_vosk/phrase/hello1.wav",
                               "../chebur_package/STT_vosk/phrase/hello2.wav",
                               "../chebur_package/STT_vosk/phrase/hello3.wav"]
                play_audio_with_interrupt(random.choice(audio_files))

                # Ждем следующую команду после обращения
                while True:
                    data = stream.read(4000, exception_on_overflow=False)
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text = result["text"]
                        break  # Получили команду, выходим из внутреннего цикла

            # Проверяем команды (если в первом обращении было больше, чем просто "Чебурашка", команда выполнится сразу)
            found_command = False
            for command, action in COMMANDS.items():
                if all(word in text for word in command):
                    print(f"Обнаружена команда: {command}")  # ✅ Добавил print
                    if is_speaking and (time.time() - start_time < 5):
                        is_speaking = False
                        print("Прерываю воспроизведение...")

                    if command in [("найди",), ("расскажи",), ("что",), ("кто",), ("узнай",), ("почему",), ("сколько",),
                                   ("как",), ("объясни",), ("зачем",), ("где",), ("когда",)]:
                        action(text)
                    else:
                        action()

                    found_command = True
                    break

            if not found_command:
                print(f"Команда не распознана: {text}")  # ✅ Добавил print
                play_audio_with_interrupt('../chebur_package/STT_vosk/phrase/sorri.wav')

