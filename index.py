#!D:\Python27\python.exe
# -*- coding: UTF-8 -*-

from web import application
from web.application import config
from web import template
from web import userService
import user
import logging

app = application.Application()

us = userService.UserService()

if us.cookie_check(app.cookie):
	logging.info('Index: cookie check passed. (%s,%s)',(app.cookie['username'].value,app.cookie['token'].value))
	app.handle('user','UserPage')
else:
	temp = template.TemplateService(config)
	temp.loadtemplate('index')
	temp.write(app.cookie)