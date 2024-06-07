from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivymd.uix.label import MDLabel
from kivy.graphics import Color, RoundedRectangle

class LabelBot(MDLabel):
    def __init__(self, **kwargs):
        super(LabelBot, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.30, 0.36, 0.44, 1)  # Cor do fundo (RGBA)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[0, 20, 20, 20])

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.color = (1, 1, 1, 1)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class LabelUser(MDLabel):
    def __init__(self, **kwargs):
        super(LabelUser, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.31, 0.52, 0.76, 1)  # Cor do fundo (RGBA)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20, 0, 20, 20])

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.color = (1, 1, 1, 1)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size



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
        return Builder.load_file("front/assets/kivy/main.kv")
    

    def bot_response(self,text):
        bot_resposta = LabelBot(
            text = text,
            size_hint_x=0.7,
            size_hint_y=None, 
            color=(1, 1, 1, 1),  # Cor do texto: branco (RGBA)
            halign='left',
            valign='top',
            pos_hint={'left': 1},
            padding=(20, 20)
        )
        bot_resposta.bind(texture_size=bot_resposta.setter('size'))
        self.root.ids.chat_list.add_widget(bot_resposta)
        self.root.ids.scroll_view.scroll_y = 0

    def user_response(self,text):
        user_resposta = LabelUser(
            text=text,
            size_hint_x=0.7,
            size_hint_y=None,
            color=(1, 1, 1, 1),  # Cor do texto: branco (RGBA)
            halign='right',
            valign='top',
            pos_hint={'right': 1},
            padding=(20, 20)
        )
        user_resposta.bind(texture_size=user_resposta.setter('size'))
        self.root.ids.chat_list.add_widget(user_resposta)
        self.root.ids.scroll_view.scroll_y = 0
    
    