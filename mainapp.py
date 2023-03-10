from kivy.app import App

from widgets import MainLayout
from get_data import DataStorage
from widgets import ViewModel


class MainApp(App):

	def __init__(self):
		self.data = DataStorage()
		self.vm = ViewModel()
		super(MainApp, self).__init__()

	def build(self):
		return MainLayout()

