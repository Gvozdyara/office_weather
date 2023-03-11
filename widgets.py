import logging
import os
import time

from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.properties import ObjectProperty, DictProperty
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.audio import SoundLoader
from matplotlib import pyplot as plt
from gtts import gTTS

import const


class Chart(FigureCanvasKivyAgg):
    def __init__(self, **kwargs):
        super().__init__(plt.gcf(), **kwargs)


class MainLayout(BoxLayout):
    interactive_lay = ObjectProperty()
    selector_lay = ObjectProperty()
    chart = ObjectProperty()

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
        self.current_values = dict()
        self.warnings = dict()

    def on_last_values(self, *args):
        logging.debug(f'{self.last_values=}')
        self.compare()
        for block in self.blocks:
            logging.debug(f'{block.id_=} {block.name=}')
            block.value_.text = str(self.last_values.get(block.id_, (None, None))[0])
            block.date.text = str(self.last_values.get(block.id_, (None, None))[1])
            logging.debug(f'value {self.last_values.get(block.id_)} is set')
        App.get_running_app().root.chart.clear_widgets()
        App.get_running_app().root.chart.add_widget(Chart())


    def play_sound(self):
        logging.debug("Preparing warning")
        for warning, value in self.warnings.items():

            tts = gTTS(f'{warning} is {value}', lang="en", slow=False)
            tts.save(f"{warning}.mp3")
            value.append(f"{warning}.mp3")
        logging.debug(self.warnings)
        for c, (_, file) in enumerate(self.warnings.values()):
            SoundLoader.load(file).play()
            time.sleep(4)


    def compare(self):
        for id_, data in self.last_values.items():
            value: float = data[0]
            ranges: dict = const.warning_ranges.get(id_)
            for degree, range_ in ranges.items():
                if not range_[0] <= value < range_[1]:
                    continue
                # if degree == "normal":
                #     logging.info(f'{id_} in range {degree}')
                #     break
                logging.info(f'{id_} in range {degree}')
                self.warnings.update({const.params.get(id_): [degree]})
        self.play_sound()
