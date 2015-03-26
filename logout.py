#!D:\Python27\python.exe
# -*- coding: UTF-8 -*-

from web import application
from web.application import config
from web import template
from web import util
from web import userService
from web import imgService
import logging

class LogoutPage(object):
	"""docstring for userPage"""
	def __init__(self):
		pass

	@staticmethod
	def GET(argus,cookie):
		us = userService.UserService()
		temp = template.TemplateService(config)
		if us.cookie_check(cookie):
			username = cookie['username'].value
			us.user_logout(username,cookie)
			temp.redirect('index',cookie)
		else:
			temp.redirect('index',cookie)

	@staticmethod	
	def POST(argus,cookie):
		temp = templateService(config)
		temp.error(404)
		temp.write(cookie)

app = application.Application()
app.handle('logout','LogoutPage')