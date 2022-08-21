from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import hashlib
import requests

class clockApp(App):
	sw_started= False
	sw_seconds = 0
	def sha256(self, message):
		return hashlib.sha256(message.encode('ascii')).hexdigest()
	def mine(self, message, difficulty=1):
		assert difficulty >= 1
		prefix = '1' * difficulty
		for i in range(100000000000):
			digest = self.sha256(str(message) + str(i))
			if digest.startswith(prefix):
				print ("after " + str(i) + " iterations found nonce: "+ digest)
				self.root.ids.label_1.text = self.root.ids.label_1.text + '\n' + "after " + str(i) + " iterations found nonce: "+ digest
				return digest, str(i)
	def update_time(self, nap):
		if self.sw_started:
			sender = self.root.ids.textinput1.text
			msg = requests.get('https://firstcontainer-qogsg.run-eu-central1.goorm.io/get').json()
			nonce, iterations = self.mine(msg['chain'],5)
			json_data = {
				'sender': sender,
				'nonce': nonce,
				'iterations':iterations,
				'index': msg['index'],
			}
			send = requests.post('https://firstcontainer-qogsg.run-eu-central1.goorm.io/post', json=json_data).json()
			print(send['message'])
			self.root.ids.label_1.text = self.root.ids.label_1.text + '\n' +send['message']
	def on_start(self):
		Clock.schedule_interval(self.update_time, 1)
	def start_stop(self):
		self.root.ids.label_1.text = self.root.ids.label_1.text + '\nMiner ' +self.root.ids.start_stop.text
		self.root.ids.start_stop.text =(
			'Start' if self.sw_started else 'Stop'
		)
		self.sw_started = not self.sw_started

if __name__ == '__main__':
	clockApp().run()