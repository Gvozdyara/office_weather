from kivy.app import App
from kivy.clock import Clock

from widgets import MainLayout
from get_data import DataStorage
from widgets import ViewModel


class MainApp(App):

	def __init__(self):
		self.data = None
		self.vm = None
		super(MainApp, self).__init__()
		Clock.schedule_once(self.init_atributes)

	def init_atributes(self, dt):
		self.data = DataStorage()
		self.vm = ViewModel()
		Clock.schedule_once(self.data.auto_refresh, 5)

	def build(self):
		return MainLayout()


