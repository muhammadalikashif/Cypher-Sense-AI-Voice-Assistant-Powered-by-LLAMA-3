import sys
import os
import time
import logging
import threading
import queue
from datetime import datetime, timedelta
import webbrowser
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTextEdit, QLabel, QProgressBar, QSystemTrayIcon, QMenu,
                             QStackedWidget, QListWidget, QListWidgetItem, QSplitter, QDialog,
                             QLineEdit, QComboBox)
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTextEdit, QLabel, QProgressBar, QSystemTrayIcon, QMenu,
                             QStackedWidget, QListWidget, QListWidgetItem, QSplitter)
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer

import speech_recognition as sr
import pyttsx3
import pyaudio
import numpy as np
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(filename='assistant.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# GROQ API settings
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    logging.error(f"Failed to initialize Groq client: {str(e)}")
    sys.exit(1)

# Initialize speech recognition and text-to-speech engines
try:
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()
except Exception as e:
    logging.error(f"Failed to initialize speech engines: {str(e)}")
    sys.exit(1)

# Constants
WAKE_WORD = "hey assistant"
EXIT_PHRASE = "goodbye"
MAX_HISTORY_LENGTH = 10

# Conversation context
conversation_history = []

# Task queue for background operations
task_queue = queue.Queue()

import webbrowser
import os
import subprocess
import logging

import os
import subprocess
import webbrowser
import logging
import requests
from bs4 import BeautifulSoup

def speak(text):
    # Implement your text-to-speech functionality here
    print(text)  # Placeholder for text-to-speech
import requests
from bs4 import BeautifulSoup
import webbrowser
import subprocess
import os
import requests
from bs4 import BeautifulSoup
import webbrowser
import subprocess
import os

def open_website_or_app(command):
    try:
        if "open" in command:
            target = command.split("open", 1)[1].strip().lower()
            if "google and search" in target:
                search_query = target.split("search", 1)[1].strip()
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                return f"Searching Google for {search_query}."
            elif "youtube and search" in target:
                search_query = target.split("search", 1)[1].strip()
                webbrowser.open(f"https://www.youtube.com/search?q={search_query}")
                return f"Searching YouTube for {search_query}."
            elif "youtube" in target:
                webbrowser.open("https://www.youtube.com")
                return "Opening YouTube."
            elif "calculator" in target:
                if os.name == 'nt':  # for Windows
                    subprocess.Popen('calc.exe')
                elif os.name == 'posix':  # for macOS and Linux
                    subprocess.Popen('gnome-calculator')
                return "Opening Calculator."
            elif "powerpoint" in target:
                if os.name == 'nt':  # for Windows
                    try:
                        subprocess.Popen(['C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE'])
                    except FileNotFoundError:
                        return "PowerPoint not found. Please check if it's installed."
                elif os.name == 'posix':  # for macOS
                    try:
                        subprocess.Popen(['open', '-a', 'Microsoft PowerPoint'])
                    except subprocess.CalledProcessError:
                        return "PowerPoint not found. Please check if it's installed."
                return "Opening PowerPoint."
            elif "excel" in target:
                if os.name == 'nt':  # for Windows
                    try:
                        # Try the default path first
                        subprocess.Popen(['C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE'])
                    except FileNotFoundError:
                        try:
                            # If the default path fails, try running 'excel' command
                            subprocess.Popen('excel')
                        except FileNotFoundError:
                            return "Excel not found. Please check if it's installed and in your PATH."
                elif os.name == 'posix':  # for macOS
                    try:
                        subprocess.Popen(['open', '-a', 'Microsoft Excel'])
                    except subprocess.CalledProcessError:
                        return "Excel not found. Please check if it's installed."
                return "Opening Excel."
        elif "temperature" in command or "weather" in command:
            search = "weather in Karachi"  # Change search string for weather
            url = f"https://www.google.com/search?q={search}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                data = BeautifulSoup(r.text, "html.parser")
                try:
                    temperature = data.find("span", class_="wob_t q8U8x", id="wob_tm").text
                    return f"Current {search} is {temperature}"
                except Exception as e:
                    return "Sorry, I couldn't fetch the weather information."
            else:
                return "Sorry, I couldn't fetch the weather information."
    except Exception as e:
        return "Sorry, I couldn't open that."


# Example usage:




def listen(timeout=5, phrase_time_limit=None):
    with sr.Microphone() as source:
        logging.info("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            return audio
        except sr.WaitTimeoutError:
            return None


def recognize_speech(audio):
    if audio is None:
        return None
    try:
        text = recognizer.recognize_google(audio)
        logging.info(f"Recognized speech: {text}")
        return text.lower()
    except sr.UnknownValueError:
        logging.info("Speech not recognized")
        return None
    except sr.RequestError as e:
        logging.error(f"Speech recognition service error: {str(e)}")
        return None


def speak(text):
    logging.info(f"Assistant speaking: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logging.error(f"Error in text-to-speech: {str(e)}")


def query_groq(prompt, max_retries=3, retry_delay=1):
    global conversation_history
    system_prompt = "Provide very short, concise responses without over-explaining."
    messages = [{"role": "system", "content": system_prompt}] + conversation_history + [
        {"role": "user", "content": prompt}]

    for attempt in range(max_retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=messages,
                model="llama3-8b-8192",
            )
            content = chat_completion.choices[0].message.content
            conversation_history.append({"role": "user", "content": prompt})
            conversation_history.append({"role": "assistant", "content": content})
            if len(conversation_history) > MAX_HISTORY_LENGTH * 2:
                conversation_history = conversation_history[-MAX_HISTORY_LENGTH * 2:]
            return content
        except Exception as e:
            logging.error(f"GROQ API request failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                return "I'm sorry, I'm having trouble connecting to my brain right now. Please try again later."


def handle_custom_commands(command):
    try:
        if "time" in command:
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}."
        elif "date" in command:
            current_date = datetime.now().strftime("%B %d, %Y")
            return f"Today's date is {current_date}."
        elif "set reminder" in command:
            _, time_str = command.split("for")
            reminder_time = datetime.strptime(time_str.strip(), "%I:%M %p")
            now = datetime.now()
            reminder_time = reminder_time.replace(year=now.year, month=now.month, day=now.day)
            if reminder_time < now:
                reminder_time += timedelta(days=1)
            delay = (reminder_time - now).total_seconds()
            task_queue.put((time.time() + delay, "Your reminder is due!"))
            return f"Reminder set for {time_str.strip()}."
        elif "temperature" in command or "weather" in command:
            search = "weather in Karachi"  # Change search string for weather
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            try:
                temp = data.find("div", class_="BNeawe").text
                speak(f"Current {search} is {temp}")
            except Exception as e:
                logging.error(f"Error fetching weather data: {str(e)}")
                speak("Sorry, I couldn't fetch the weather information.")
                return "Sorry, I couldn't fetch the weather information."
    except Exception as e:
        logging.error(f"Error handling custom command: {str(e)}")
        return "Sorry, I couldn't process that command. Please try again."
    return None


class VoiceActivityDetectionThread(QThread):
    update_signal = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.stream = None
        self.p = pyaudio.PyAudio()
        self.running = True

    def run(self):
        try:
            self.stream = self.p.open(format=pyaudio.paFloat32,
                                      channels=1,
                                      rate=44100,
                                      input=True,
                                      frames_per_buffer=1024)

            while self.running:
                data = np.frombuffer(self.stream.read(1024), dtype=np.float32)
                volume = np.abs(data).mean()
                self.update_signal.emit(volume)
        except Exception as e:
            logging.error(f"Error in voice activity detection: {str(e)}")

    def stop(self):
        self.running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()


class AssistantThread(QThread):
    update_signal = pyqtSignal(str, str)  # (role, content)
    status_signal = pyqtSignal(str)
    speak_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            self.status_signal.emit("Listening...")
            audio = listen(timeout=5, phrase_time_limit=5)
            command = recognize_speech(audio)

            if command:
                self.update_signal.emit("user", command)
                if EXIT_PHRASE in command:
                    self.update_signal.emit("assistant", "Goodbye! Have a great day!")
                    self.speak_signal.emit("Goodbye! Have a great day!")
                    break

                custom_response = handle_custom_commands(command)
                if custom_response:
                    self.update_signal.emit("assistant", custom_response)
                    self.speak_signal.emit(custom_response)
                else:
                    website_app_response = open_website_or_app(command)
                    if website_app_response:
                        self.update_signal.emit("assistant", website_app_response)
                        self.speak_signal.emit(website_app_response)
                    else:
                        self.status_signal.emit("Thinking...")
                        response = query_groq(command)
                        self.update_signal.emit("assistant", response)
                        self.speak_signal.emit(response)

            self.status_signal.emit("Ready")

    def stop(self):
        self.running = False


class ConversationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.conversation_display = QTextEdit()
        self.conversation_display.setReadOnly(True)
        self.layout.addWidget(self.conversation_display)

    def add_message(self, role, text):
        if role == "user":
            self.conversation_display.append(
                f"<p style='color: #4a4a4a; background-color: #e6f3ff; padding: 10px; border-radius: 15px; margin: 5px 0;'><strong>You:</strong> {text}</p>")
        else:
            self.conversation_display.append(
                f"<p style='color: #4a4a4a; background-color: #f0f0f0; padding: 10px; border-radius: 15px; margin: 5px 0;'><strong>Assistant:</strong> {text}</p>")


class MainWindow(QMainWindow):
    speak_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Assistant")
        self.setGeometry(100, 100, 1000, 800)
        self.setup_ui()

    def setup_ui(self):
        # Set up the main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Create a splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Left panel: Conversation history
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.conversation_widget = ConversationWidget()
        left_layout.addWidget(self.conversation_widget)
        splitter.addWidget(left_panel)

        # Right panel: Controls and status
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        splitter.addWidget(right_panel)

        # Header
        header_label = QLabel("Cypher Sense")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px; color: #4a4a4a;")
        right_layout.addWidget(header_label)

        # Voice activity visualization
        # Voice activity visualization
        self.voice_bar = QProgressBar()
        self.voice_bar.setRange(0, 100)
        self.voice_bar.setTextVisible(False)
        self.voice_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #4a4a4a;
                border-radius: 10px;
                background-color: #ffffff;
                height: 20px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                                                  stop:0 #3498db, stop:1 #2980b9);
                border-radius: 8px;
            }
        """)
        right_layout.addWidget(self.voice_bar)

        # Control buttons
        button_layout = QHBoxLayout()

        self.listen_button = QPushButton("Listen")
        self.listen_button.setIcon(QIcon("mic_icon.png"))
        self.listen_button.clicked.connect(self.start_listening)
        button_layout.addWidget(self.listen_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setIcon(QIcon("stop_icon.png"))
        self.stop_button.clicked.connect(self.stop_listening)
        button_layout.addWidget(self.stop_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setIcon(QIcon("clear_icon.png"))
        self.clear_button.clicked.connect(self.clear_conversation)
        button_layout.addWidget(self.clear_button)

        right_layout.addLayout(button_layout)

        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px; color: #4a4a4a; margin-top: 20px;")
        right_layout.addWidget(self.status_label)

        # Set up threads
        self.assistant_thread = AssistantThread()
        self.assistant_thread.update_signal.connect(self.update_conversation)
        self.assistant_thread.status_signal.connect(self.update_status)
        self.assistant_thread.speak_signal.connect(self.speak_message)

        self.vad_thread = VoiceActivityDetectionThread()
        self.vad_thread.update_signal.connect(self.update_voice_bar)

        # System tray
        self.setup_system_tray()

        # Auto-scroll timer
        self.scroll_timer = QTimer(self)
        self.scroll_timer.timeout.connect(self.auto_scroll)
        self.scroll_timer.start(100)

        # Connect speak_signal
        self.speak_signal.connect(self.speak_message)

        # Apply style
        self.setStyleSheet(self.get_stylesheet())

    def get_stylesheet(self):
        return """
            QMainWindow {
                background-color: #87CEEB; /* Sky blue color */
            }
            QLabel {
                color: #4a4a4a;
                font-size: 18px;
            }
            QPushButton {
                background-color: #46647D;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #000033;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                font-size: 14px;
                padding: 10px;
            }

        """

    def setup_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("app_icon.png"))
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show)
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(QApplication.quit)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def start_listening(self):
        self.status_label.setText("Listening...")
        self.assistant_thread.start()
        self.vad_thread.start()

    def stop_listening(self):
        self.status_label.setText("Stopped")
        self.assistant_thread.stop()
        self.vad_thread.stop()

    def update_conversation(self, role, text):
        self.conversation_widget.add_message(role, text)

    def update_status(self, status):
        self.status_label.setText(status)

    def update_voice_bar(self, volume):
        target_value = int(volume * 100)
        current_value = self.voice_bar.value()

        # Smooth animation
        if target_value > current_value:
            self.voice_bar.setValue(min(current_value + 5, target_value))
        else:
            self.voice_bar.setValue(max(current_value - 5, target_value))

        # Change color based on volume
        if target_value < 25:
            color = "#3498db"  # Light blue for low volume
        elif target_value < 45:
            color = "#2980b9"  # Medium blue for moderate volume
        else:
            color = "#e74c3c"  # Red for high volume

        self.voice_bar.setStyleSheet(self.voice_bar.styleSheet().replace(
            "stop:1 #2980b9", f"stop:1 {color}"
        ))

    def clear_conversation(self):
        self.conversation_widget.conversation_display.clear()

    def auto_scroll(self):
        scrollbar = self.conversation_widget.conversation_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "AI Assistant",
            "The application is still running in the background.",
            QSystemTrayIcon.Information,
            2000
        )

    def speak_message(self, message):
        speak(message)


def background_tasks(speak_signal):
    while True:
        now = time.time()
        while not task_queue.empty() and task_queue.queue[0][0] <= now:
            _, message = task_queue.get()
            speak_signal.emit(message)
        time.sleep(1)


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.layout = QVBoxLayout(self)

        # Wake word setting
        self.wake_word_input = QLineEdit(WAKE_WORD)
        self.layout.addWidget(QLabel("Wake Word:"))
        self.layout.addWidget(self.wake_word_input)

        # Voice selection
        self.voice_selector = QComboBox()
        voices = engine.getProperty('voices')
        for voice in voices:
            self.voice_selector.addItem(voice.name)
        self.layout.addWidget(QLabel("Assistant Voice:"))
        self.layout.addWidget(self.voice_selector)

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

    def save_settings(self):
        global WAKE_WORD
        WAKE_WORD = self.wake_word_input.text()
        selected_voice = engine.getProperty('voices')[self.voice_selector.currentIndex()]
        engine.setProperty('voice', selected_voice.id)
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application-wide font
    app.setFont(QFont("Roboto", 10))

    # Set color scheme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    palette.setColor(QPalette.WindowText, QColor(74, 74, 74))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(74, 74, 74))
    palette.setColor(QPalette.Text, QColor(74, 74, 74))
    palette.setColor(QPalette.Button, QColor(76, 175, 80))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(76, 175, 80))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    window = MainWindow()
    window.show()

    # Start background task thread
    threading.Thread(target=background_tasks, args=(window.speak_signal,), daemon=True).start()

    sys.exit(app.exec_())