#!D:\Python27\python.exe
# -*- coding: UTF-8 -*-

from web import application
from web.application import config
from web import template
from web import util
from web import userService
from web import imgService
import logging

class LoginPage(object):
	"""docstring for userPage"""
	def __init__(self):
		pass

	@staticmethod
	def GET(argus,cookie):
		logging.debug('LoginPage.GET called.')
		us = userService.UserService()
		temp = template.TemplateService(config)
		if us.cookie_check(cookie):
			temp.redirect('user',cookie)
		else:
			temp.loadtemplate('login')
			temp.write(cookie)
			
	@staticmethod	
	def POST(argus,cookie):
		logging.debug('LoginPage.POST called.')
		username = argus.getvalue('username')
		logging.debug('login:%s',username)
		password = argus.getvalue('password')
		logging.debug('loginpass:%s',password)
		us = userService.UserService()
		temp = template.TemplateService(config)
		if us.account_check(username,password):
			logging.debug('account_check passed for user: %s',username)
			us.user_token(username,cookie)
			temp.redirect('user',cookie)
		else:
			replace_dict = {}
			replace_dict['__SERVER_MSG__'] = u'用户名或密码错误'
			temp.set_replaceDict(replace_dict)
			temp.loadtemplate('login')
			temp.write(cookie)
if __name__ == '__main__':
	app = application.Application()
	logging.info('login handle called')
	app.handle('login','LoginPage')