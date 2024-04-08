import speech_recognition as sr
import pyttsx3


audio = sr.Recognizer()
assistente = pyttsx3.init()


try:
    with sr.Microphone() as source:
        print("ouvindo...")
        voz = audio.listen(source)
        comando = audio.recognize_google(voz, language='pt-BR')
        comando = comando.lower()
        if 'alice' in comando:
            print(comando)
            assistente.say("Olá como posso te ajudar!")
            assistente.runAndWait()

except Exception as e:
    print(f"microfone não está funcionando, aconteceu o erro {e}")
