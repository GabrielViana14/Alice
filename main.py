import speech_recognition as sr
import pyttsx3
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.app import App
import threading
from front.front import MainApp

bot_name = "alice"
audio = sr.Recognizer()
assistente = pyttsx3.init()

class Voice:
    def __init__(self):
        self.app = MainApp()
        self.window_visible = False  # Estado da janela
        self.bot_ativo = False  # Estado do bot (ativo ou não)

        Clock.schedule_once(self.hide_window, 0)

        # Inicia o processamento de áudio em uma thread separada
        self.audio_thread = threading.Thread(target=self.ouvindo)
        self.audio_thread.start()

        Window.bind(on_close=self.on_close)

    def hide_window(self, *args):
        Window.hide()
        self.window_visible = False

    def ouvindo(self):
        while True:
            try:
                with sr.Microphone() as source:
                    print("Ouvindo...")
                    voz = audio.listen(source)
                    comando = audio.recognize_google(voz, language='pt-BR')
                    comando = comando.lower()
                    if comando =="fechar" or comando == "sair" :
                        Clock.schedule_once(lambda dt: self.on_close(), 0)
                        break
                    if bot_name in comando or self.bot_ativo:
                        if not self.bot_ativo:
                            self.bot_ativo = True  # Ativa o bot
                        Clock.schedule_once(lambda dt: self.abrir_interface(), 0)
                        Clock.schedule_once(lambda dt: self.resposta_user(comando), 0)
                        resposta = "Olá como posso te ajudar!"
                        assistente.say(resposta)
                        Clock.schedule_once(lambda dt: self.resposta_bot(resposta), 0)
                        assistente.runAndWait()
            except Exception as e:
                print(f"Aconteceu um erro: {e}")
                Clock.schedule_once(lambda dt: self.hide_window(), 0)
                self.bot_ativo = False
                

    def abrir_interface(self):
        if not self.window_visible:
            Window.show()
            self.window_visible = True

    def on_close(self, *args):
        print("Encerrando o programa...")
        self.app.stop()

    def resposta_user(self, texto):
        if self.app:
            self.app.user_response(texto)

    def resposta_bot(self, texto):
        if self.app:
            self.app.bot_response(texto)

if __name__ == "__main__":
    bot = Voice()
    bot.app.run()
