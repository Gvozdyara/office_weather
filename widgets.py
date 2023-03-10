import logging

from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import ObjectProperty, DictProperty
from kivy.uix.widget import Widget
from kivy.app import App

class MainLayout(BoxLayout):
    interactive_lay = ObjectProperty()
    selector_lay = ObjectProperty()

    def __init__(self):
        super(MainLayout, self).__init__()
        self.app = None
        Clock.schedule_once(self.fill_selector)

    def fill_selector(self, dt):
        self.app = App.get_running_app()
        for id_, name in self.app.data.params.items():
            block = ParamSelector(id_, name)
            self.selector_lay.add_widget(block)
            self.app.vm.blocks.append(block)

class ParamSelector(BoxLayout):
    date = ObjectProperty()
    active_ = ObjectProperty()
    value_ = ObjectProperty()

    def __init__(self, id_, name):
        self.name = name
        self.id_ = id_
        super(ParamSelector, self).__init__()


class ViewModel(Widget):

    last_values = DictProperty()

    def __init__(self):
        super(ViewModel, self).__init__()
        self.blocks = list()

    def on_last_values(self, *args):
        logging.debug(f'{self.last_values=}')
        for block in self.blocks:
            block.value_.text = str(self.last_values.get(block.id_, (None, None))[0])
            block.date.text = str(self.last_values.get(block.id_, (None, None))[1])
            logging.debug(f'value {self.last_values[block.id_]} is set')
