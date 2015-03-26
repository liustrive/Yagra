#!D:\Python27\python.exe
# -*- coding: UTF-8 -*-

from web import application
from web.application import config
from web import template
from web import util
from web import userService
from web import imgService
import imghdr
import os
import logging
try: # Windows needs stdio set for binary mode.
	import msvcrt
	msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
	msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
	pass

class Avatar(object):
	"""docstring for userPage"""
	def __init__(self):
		pass

	@staticmethod
	def GET(argus,cookie):
		imgs = imgService.ImgService(config)
		temp = template.TemplateService(config)
		# do not do cookie check
		emailhash = argus.getvalue('emailhash')
		logging.debug('get avatar request:%s',emailhash)
		if util.check_hash(emailhash):
			imgname = imgs.get_image_by_hash(emailhash)
			fullpath = ''
			if imgname:
				fullpath = imgs.get_img_fullpath(imgname)
			else:
				fullpath = config['__default_user_img__']
			logging.debug('img full path:%s',fullpath)
			try:
				imgfile = open(fullpath,'rb')
				imgdata = imgfile.read()
				temp.set_type('image/%s' % imghdr.what('',imgdata))
				temp.write_img(imgdata)
			except Exception, e:
				logging.error('fail to open img file:%s',e)
				fullpath = config['__default_user_img__']
				imgfile = open(fullpath,'rb')
				imgdata = imgfile.read()
				temp.set_type('image/%s' % imghdr.what('',imgdata))
				temp.write_img(imgdata)
		else:
			logging.warning('Hashcode not legal: %s',emailhash)
			fullpath = config['__default_user_img__']
			imgfile = open(fullpath,'rb')
			imgdata=  imgfile.read()
			temp.set_type('image/%s' % imghdr.what('',imgdata))
			temp.write_img(imgdata)

	@staticmethod	
	def POST(argus,cookie):
		logging.warning('Not surpose to be post method')
		fullpath = config['__default_img__']
		imgfile = open(fullpath)
		temp.set_type('image/%s' % imghdr.what('',imgfile))
		temp.write_img(imgfile)

if __name__ == '__main__':
	app = application.Application()
	app.handle('avatar','Avatar')