from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import get_color_from_hex





class MainApp(MDApp):
    #Parametros alteraveis
    bot_name = "Alice"


    def hex_to_color(self, hex_color):
        return get_color_from_hex(hex_color)
    
    def build(self):
        self.theme_cls.theme_style = "Light"
        Window.size = (350, 350)
        Window.top = 400  
        Window.left = 100
        Window.always_on_top = True  # Mantém a janela sempre no topo
        self.title = "Assistente virtual" # Titulo da janela
        self.clearcolor = self.hex_to_color("#FD91A4")
        return Builder.load_file("assets/kivy/main.kv")
    

    def bot_response(self,text):
        bot_resposta = self.root.ids.bot_response.copy()
        bot_resposta.text = text
        self.root.add_widget(bot_resposta)

    def user_response(self,text):
        user_resposta = self.root.ids.user_response.copy()
        user_resposta.text = text
        self.root.add_widget(user_resposta)
    
    

if __name__ == "__main__":
    MainApp().run()