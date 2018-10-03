# -*- coding: utf-8 -*-

import socket
import threading
import sys
import pickle
from datetime import datetime

class Server():
  def __init__(self, host = sys.argv[1], port = sys.argv[2]):
    self.clients = []
    self.host = host
    self.port = port
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind((str(host), int(port)))
    self.sock.listen(10)
    self.sock.setblocking(False)

    to_accept = threading.Thread(target=self.accept_conn)
    to_process = threading.Thread(target=self.process_conn)

    to_accept.setDaemon(True)
    to_accept.start()

    to_process.setDaemon(True)
    to_process.start()

    while True:
      msg = input("SERVER <{}> ".format(socket.gethostname()))
      if msg == "exit()":
        self.sock.close()
        sys.exit()
      else:
        pass


  def msg_to_all(self, msg, client):
    for c1 in self.clients:
      try:
        if c1 != client:
          c1.send(msg)
      except Exception as e:
        self.clients.remove(c1)

  def accept_conn(self):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Connection on {}:{} started at {}".format(self.host, self.port, time_now))
    while True:
      try:
        conn, addr = self.sock.accept()
        conn.setblocking(False)
        self.clients.append(conn)
      except Exception as e:
        pass

  def process_conn(self):
    while True:
      if len(self.clients) > 0:
        for c2 in self.clients:
          try:
            data = c2.recv(1024)
            if data:
              self.msg_to_all(data, c2)
          except Exception as e:
            pass

s = Server()


