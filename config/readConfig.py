# -*- coding: UTF-8 -*-
import os
import configparser

cur_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(cur_path, 'cfg.ini')
config = configparser.ConfigParser()
config.read(config_path)

smtp_server = config.get('email', 'smtp_server')
port = config.get('email', 'port')
sender = config.get('email', 'sender')
pwd = config.get('email', 'pwd')
receiver = config.get('email', 'receiver')

print(smtp_server, port, sender, pwd, receiver)

