from datetime import datetime
import logging
import os
import time
from threading import Thread

from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.properties import ObjectProperty, DictProperty
from kivy.uix.widget import Widget
from kivy.app import App
# from kivy.core.audio import SoundLoader
from matplotlib import pyplot as plt
from gtts import gTTS
from pygame import mixer

import const


class Chart(FigureCanvasKivyAgg):
    def __init__(self, **kwargs):
        super().__init__(plt.gcf(), **kwargs)


class MainLayout(BoxLayout):
    interactive_lay = ObjectProperty()
    selector_lay = ObjectProperty()
    chart = ObjectProperty()
    request_lines = ObjectProperty()

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
    info = ObjectProperty()

    def __init__(self, id_, name):
        self.name = name
        self.id_ = id_
        super(ParamSelector, self).__init__()

    def sound_off(self, value):
        App.get_running_app().vm.sound_options.update({self.id_: value})


class ViewModel(Widget):

    last_values = DictProperty()
    sound_options = DictProperty({k: True for k in const.params})

    def __init__(self):
        super(ViewModel, self).__init__()
        # the list is filled when MainLayout is being created
        self.blocks = list()
        self.current_values = dict()
        self.warnings = dict()
        self.business = {"isrequest": False}

    def on_last_values(self, *args):
        logging.debug(f'{self.last_values=}')
        if self.last_values == dict():
            return
        self.compare()
        for block in self.blocks:
            logging.debug(f'{block.id_=} {block.name=}')
            block.value_.text = str(self.last_values.get(block.id_, (None, None))[0])
            block.date.text = datetime.fromisoformat(self.last_values.get(block.id_, (None, None))[1]).strftime("%d %B %H:%M")
            logging.debug(f'value {self.last_values.get(block.id_)} is set')
        App.get_running_app().root.chart.clear_widgets()
        App.get_running_app().root.chart.add_widget(Chart())
        self.play_sound()

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
                self.warnings.update({id_: [degree]})

    def play_sound(self):
        logging.debug("Preparing warning")
        warnings = {key: value[:] for key, value in self.warnings.items() if value[0] != "normal"}
        self.change_color(warnings)
        if len(warnings) == 0:
            logging.info("All parameters are normal")
            return

        for id_, value in warnings.items():

            tts = gTTS(f'{const.params.get(id_)} is {value}', lang="en", slow=False)
            tts.save(f"{id_}.mp3")
            value.append(f"{id_}.mp3")
        logging.debug(self.warnings)
        for c, (id_, value) in enumerate(warnings.items()):
            file = value[1]
            if not self.sound_options.get(id_):
                logging.debug(f'{file} warning is ommited')
                continue
            # SoundLoader.load(file).play()
            mixer.init()
            mixer.music.load(file)
            mixer.music.play()
            time.sleep(4)

    def change_color(self, warnings: dict):
        for block in self.blocks:
            if not block.id_ in warnings:
                block.value_.color = (1, 1, 1, 1)
                continue
            block.value_.color = (1, 93/255, 0, 1)

    def update_request(self, value: str):
        if not value.isnumeric():
            logging.debug("Request lines input is not numeric")
            return

        value = int(value)
        App.get_running_app().data.update_request_lines(value)
        logging.debug(App.get_running_app().data.request_lines)

    def request_data(self):
        if self.business.get("isrequest"):
            logging.debug(f"{self.business} request is blocked")
            return
        self.business.update({"isrequest": True})
        self.last_values.clear()
        Thread(target=App.get_running_app().data.get_values, args=(self.business,)).run()

        

