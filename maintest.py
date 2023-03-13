from widgets import ViewModel

obj = ViewModel()
obj.on_last_values = None
obj.sound_options ={"smth": False}
obj.warnings = {"smth": ["high", "Temperature.mp3"]}
obj.play_sound()