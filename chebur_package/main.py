import pyaudio
import json
import random
import time
import threading
from vosk import Model, KaldiRecognizer
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
        if is_speaking:
            play_audio(file)
        is_speaking = False

    thread = threading.Thread(target=play)
    thread.start()


# ✅ Запускаем браузер в ОТДЕЛЬНОМ потоке
driver = None
driver_ready = threading.Event()


def start_driver():
    global driver
    driver = init_driver(headless=True)
    driver_ready.set()


threading.Thread(target=start_driver, daemon=True).start()


def ask_alice(text):
    text = text + " P.S. ответь по русски одним абзацем максимум на 150 символов, но если до P.S. передана бессмыслица, то ответь, извините я не понял вопроса обязательно в мужском роде"
    words = text.split()
    text = " ".join(word for word in words if word not in KEYWORDS)
    driver_ready.wait()
    response = ask_yandex_gpt(driver, text)
    lower_response = response.lower()
    if response:
        if any(phrase in lower_response for phrase in ["не понял", "не поняла", "не могу ответить"]):
            play_audio_with_interrupt("../chebur_package/STT_vosk/phrase/sorri.wav")
        else:
            generate_speech(response)
    else:
        play_audio_with_interrupt("../chebur_package/STT_vosk/phrase/sorri.wav")


# Предзаписанные команды
COMMANDS = {
    ("расскажи", "технопарк"): lambda: play_audio('../chebur_package/STT_vosk/phrase/techno.wav'),
    ("расскажи", "технологии", "технопарк"): lambda: play_audio('../chebur_package/STT_vosk/phrase/techno.wav'),
    ("расскажи", "аудитор", "ельцин"): lambda: play_audio('../chebur_package/STT_vosk/phrase/elcin.wav'),
    ("где", "столовая"): lambda: play_audio('../chebur_package/STT_vosk/phrase/canteen.wav'),
}

while True:
    data = stream.read(4000, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        text = result["text"]

        if any(keyword in text for keyword in KEYWORDS):
            words = text.split()

            if len(words) == 1 and words[0] in KEYWORDS:
                print("Я слушаю вас!")
                audio_files = ["../chebur_package/STT_vosk/phrase/hello1.wav",
                               "../chebur_package/STT_vosk/phrase/hello2.wav",
                               "../chebur_package/STT_vosk/phrase/hello3.wav"]
                play_audio_with_interrupt(random.choice(audio_files))

                while True:
                    data = stream.read(4000, exception_on_overflow=False)
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text = result["text"]
                        break

            found_command = False
            for command, action in COMMANDS.items():
                if all(word in text for word in command):
                    print(f"Обнаружена команда: {command}")
                    action()
                    found_command = True
                    break

            if not found_command:
                print(f"Команда не распознана: {text}. Отправляю запрос Алисе...")
                wait_phrases = [
                    "../chebur_package/STT_vosk/phrase/wait1.wav",
                    "../chebur_package/STT_vosk/phrase/wait2.wav",
                    "../chebur_package/STT_vosk/phrase/wait3.wav"
                ]
                # Запускаем озвучку в отдельном потоке
                threading.Thread(target=play_audio, args=(random.choice(wait_phrases),), daemon=True).start()
                ask_alice(text)
