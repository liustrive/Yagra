#!D:\Python27\python.exe
# -*- coding: UTF-8 -*-

from web import application
from web.application import config
from web import template
from web import util
from web import userService
from web import imgService
import logging

class UserPage(object):
	"""docstring for userPage"""
	def __init__(self):
		pass

	@staticmethod
	def GET(argus,cookie):
		logging.debug('UserPage.GET called.')
		us = userService.UserService()
		if us.cookie_check(cookie):
			username = cookie['username'].value
			userinfo = us.get_user(username)
			temp = template.TemplateService(config)
			if userinfo:
				replaceDict = {}
				replaceDict['__USER_NAME__'] = userinfo[0]
				replaceDict['__USER_NICK__'] = userinfo[5]
				#
				replaceDict['__USER_EMAIL__'] = userinfo[2]
				imgs = imgService.ImgService(config)
				logging.debug('UserPage.user_head_hash: %s, email:%s',util.get_imghash(userinfo[2]),userinfo[2])
				imgname=  imgs.get_image_by_hash(util.get_imghash(userinfo[2]))
				if imgname:
					replaceDict['__USER_HEAD_IMG__'] = imgs.get_img_fullpath(imgname)
				temp.set_replaceDict(replaceDict)
				temp.loadtemplate('user')
				temp.write(cookie)
			else:
				logging.error('No user found while cookie check passed!')
				temp.redirect('login',cookie)
		else:
			temp = template.TemplateService(config)
			temp.redirect('login',cookie)

	@staticmethod	
	def POST(argus,cookie):
		temp = template.TemplateService(config)
		temp.error(404)
		temp.write(cookie)

if __name__ == '__main__':
	app = application.Application()
	app.handle('user','UserPage')