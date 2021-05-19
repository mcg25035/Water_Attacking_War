#Client
import kivy
import threading
import os
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
A = FloatLayout()




class Window(App):
    def build(self):
        self.title = "噴水大戰"
        return A

Window().run()