import os
import cgi
import cgitb
import Cookie
import sys
import template
import logging

__all__ = ['Application']

logging.basicConfig(filename = os.path.join(os.getcwd(), 'server.log'), level = logging.DEBUG)

homePath = os.path.dirname(os.path.realpath(__file__))
config = {}
configPath = os.path.join(homePath, 'server.conf')
execfile(configPath, config)

'''
'HTTP_COOKIE': '',
'REQUEST_URI': ,
'SCRIPT_NAME': '',
'REQUEST_METHOD': 'GET'/'POST',
'SERVER_PROTOCOL': 'HTTP/1.1',
'QUERY_STRING': '',
'HTTP_ACCEPT_CHARSET': 'UTF-8,*;q=0.5',
'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) '
'AppleWebKit/537.17 (KHTML, like Gecko) Ubuntu '
'Chromium/24.0.1312.56 Chrome/24.0.1312.56 Safari/537.17',
'HTTP_CONNECTION': 'keep-alive',
'SERVER_NAME': 'localhost',
'REMOTE_ADDR': '127.0.0.1',
'SERVER_PORT': '80',
'SERVER_ADDR': '127.0.0.1',
'DOCUMENT_ROOT': ,
'SCRIPT_FILENAME': ,
'HTTP_HOST': 'localhost',
'HTTP_CACHE_CONTROL': 'max-age=0',
'HTTP_ACCEPT': 'text/html,application/xhtml+xml,'
'GATEWAY_INTERFACE': 'CGI/1.1',
'REMOTE_PORT': ,
'HTTP_ACCEPT_LANGUAGE': 'zh,zh-CN;q=0.8,en-US;q=0.6',
'HTTP_ACCEPT_ENCODING': 'gzip,deflate,sdch'}

'''

cgitb.enable()

class Application(object):
	"""docstring for appService"""
	def __init__(self):
		# base info needed of request
		self.http_cookie = os.environ.get('HTTP_COOKIE')
		self.request_uri = os.environ.get('REQUEST_URI')
		self.request_method = os.environ.get('REQUEST_METHOD')


		self.arguments = cgi.FieldStorage()
		self.cookie = Cookie.SimpleCookie()

		if self.http_cookie:
			self.cookie.load(self.http_cookie)

	def method_type(self):
		if self.request_method and isinstance(self.request_method,str):
			method = self.request_method.upper()
			if 'GET'== method or 'POST' == method:
				return method
			else:
				return None
		else:
			return None

	def get_argument(self,argu_name):
		if argu_name not in self.arguments:
			return None
		else:
			return self.arguments.getvalue(argu_name)
	def get_FieldStorage(self):
		return self.arguments

	def handle(self,modulname,classname):
		method = self.method_type()
		if method: # GET POST
			mod = __import__(modulname)
			#logging.info('application: import mod')
			cls = getattr(mod,classname)
			#logging.info('application: import class')
			getattr(cls(),method)(self.arguments,self.cookie)
			#logging.info('application: method called')
		else:
			logging.error('No Request method found.')
			#error handler
			temp = templateService(config)
			temp.error(404)
			temp.write(self.cookie)
			



		



