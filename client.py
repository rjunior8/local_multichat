# -*- coding: utf-8 -*-

import socket
import threading
import sys
import pickle
from datetime import datetime

class Client():
	def __init__(self, host = sys.argv[1], port = sys.argv[2]):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((str(host), int(port)))

		self.host = host
		self.port = port

		msg_recv = threading.Thread(target=self.msg_recv)
		msg_recv.setDaemon(True)
		msg_recv.start()

		time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		print("Connected on server ({}:{}) started at {}".format(self.host, self.port, time_now))
		print("{} has joined".format(socket.gethostname()))

		while True:
			msg = input("<{}> ".format(socket.gethostname()))
			if msg != "exit()":
				self.send_msg(msg)
			else:
				self.sock.close()
				sys.exit()

	def msg_recv(self):
		while True:
			try:
				data = self.sock.recv(1024)
				if data:
					print(pickle.loads(data))
			except:
				pass

	def send_msg(self, msg):
		self.sock.send(pickle.dumps("<{}> {}".format(socket.gethostname(), msg)))


c = Client()