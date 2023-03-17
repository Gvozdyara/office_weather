from threading import Thread

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
		self.title = "Office weather v1.2"

	def init_atributes(self, dt):
		self.data = DataStorage()
		self.vm = ViewModel()
		Clock.schedule_once(self.auto_refresh, 5)

	def auto_refresh(self, dt=0):
		Thread(target=self.data.auto_refresh).run()

	def build(self):
		return MainLayout()


