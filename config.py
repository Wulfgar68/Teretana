# config.py
import os

MYSQL_HOST = os.environ.get('MYSQL_HOST', 'db')
MYSQL_USER = os.environ.get('MYSQL_USER', 'luka_pis')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'luka23012005')
MYSQL_DB = os.environ.get('MYSQL_DATABASE', 'luka_pis')
MYSQL_CURSORCLASS = 'DictCursor'
