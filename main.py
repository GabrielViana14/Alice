import speech_recognition as sr
import pyttsx3
from machine_learning.chat import Chat
from front.front import MainApp
from kivy.clock import Clock
from kivy.core.window import Window
import threading

bot_name = "alice"
language = "pt-BR"

stop_event = threading.Event()
assistente = pyttsx3.init()
chat_bot = Chat()

class Voice:
    def __init__(self):
        self.app = MainApp()
        self.window_visible = False  # Estado da janela
        self.bot_ativo = True  # Estado do bot (ativo ou não)
        self.open = False  # Estado da tela (aberta ou não)
        self.audio = sr.Recognizer()
        Clock.schedule_once(self.hide_window, 0)
        # Inicia o processamento de áudio em uma thread separada
        self.audio_thread = threading.Thread(target=self.ouvindo)
        self.audio_thread.start()
        Window.bind(on_close=self.on_close)

    def hide_window(self, *args):
        Window.hide()
        self.window_visible = False

    def on_close(self, *args):
        print("Encerrando o programa...")
        self.hide_window()  # Oculta a janela se estiver visível
        self.app.stop()  # Para o aplicativo Kivy
        stop_event.set()  # Define o evento para parar a thread de voz
        return False  # Retorna False para permitir que o Kivy feche a janela

    def abrir_interface(self):
        if not self.window_visible:
            Window.show()
            self.window_visible = True

    def resposta_user(self, texto):
        if self.app:
            self.app.user_response(texto)

    def resposta_bot(self, texto):
        if self.app:
            self.app.bot_response(texto)

    def ouvindo(self):
        with sr.Microphone() as source:
            while self.bot_ativo:
                try:
                    print("Ajustando para ruído de fundo...")
                    self.audio.adjust_for_ambient_noise(source, duration=1)
                    print("Ouvindo...")
                    voice = self.audio.listen(source, timeout=5, phrase_time_limit=7)
                    print("processando...")
                    command = self.audio.recognize_google(voice, language=language)
                    voice = ""
                    command = command.lower()
                    print(command)
                    if command in ["fechar", "sair", "encerrar"]:
                        print("Saindo..")
                        Clock.schedule_once(lambda dt: self.resposta_user(command), 0)
                        self.process_command(command)
                        Clock.schedule_once(lambda dt: self.on_close(), 0)
                        self.bot_ativo = False
                        break
                    if self.open:
                        print("interface já aberta!")
                        Clock.schedule_once(lambda dt: self.resposta_user(command), 0)
                        self.process_command(command)
                    elif bot_name in command:
                        self.open = True
                        Clock.schedule_once(lambda dt: self.abrir_interface(), 0)
                        Clock.schedule_once(lambda dt: self.resposta_user(command), 0)
                        self.process_command(command)
                except Exception as e:
                    print(f"Erro: {e}")
            self.open = False
        Clock.usleep(0.5)

    def process_command(self, command):
        try:
            answer = chat_bot.resposta(command)
            Clock.schedule_once(lambda dt: self.resposta_bot(answer), 0)
            assistente.say(answer)
            assistente.runAndWait()
        except Exception as e:
            print(f"Erro: {e}")


if __name__ == "__main__":
    bot = Voice()
    bot.app.run()
