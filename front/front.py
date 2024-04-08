from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import get_color_from_hex



class MainApp(MDApp):
    def hex_to_color(self, hex_color):
        return get_color_from_hex(hex_color)
    
    def build(self):
        self.theme_cls.theme_style = "Light"
        Window.size = (350, 350)
        Window.top = 400  
        Window.left = 100
        Window.always_on_top = True  # Mantém a janela sempre no topo
        self.title = "Assistente virtual" # Titulo da janela
        Window.clearcolor = self.hex_to_color("#FD91A4")
        return Builder.load_file("assets/kivy/main.kv")
    
    


MainApp().run()