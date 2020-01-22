# -*- coding: utf-8 -*-
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.core.window import Window
Window.size = (1280, 720)
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemeManager
from three import get_map
from kivymd.uix.list import IRightBodyTouch, ILeftBody
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.factory import Factory
from kivy.uix.label import Label

class MyCheckbox(IRightBodyTouch, MDCheckbox):
    pass

class MyText(ILeftBody, Label):
    pass

class Lists(BoxLayout):
    pass

class Container(FloatLayout):
    cities = []
    original_cities = []

    def edit_item(self, city, state):
        if state:
            self.cities.append(city)
        else:
            self.cities.remove(city)

    def enter(self):
        self.cities = self.mytext_input.text.split(", ")
        self.original_cities = self.mytext_input.text.split(", ")
        for child in self.ids.scroll.children[:]:
            self.ids.scroll.remove_widget(child)
        self.new_map()
        for index, name in enumerate(self.cities):
            item = Factory.ListItemWithCheckbox(text=f'{name}')
            item.number=f'{index+1}'
            self.ids.scroll.add_widget(item)

    def new_map(self):
        if len(self.cities) > 2:
            cost = get_map(self.cities, self.original_cities)
            self.ids.lis.cost = f'Протяжённость: {cost} км'
            self.bgi.source = ''
            self.bgi.reload()
            self.bgi.source = 'myimg.png'
            self.bgi.reload()

class MyApp(App):
    theme_cls = ThemeManager()
    theme_cls.theme_style = 'Dark'
    theme_cls.primary_palette = 'Teal'

    def build(self):
        self.title = 'Minimum spanning tree'
        return Container()

if __name__ == "__main__":
    MyApp().run()