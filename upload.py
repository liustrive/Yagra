#!D:\Python27\python.exe
# -*- coding: UTF-8 -*-

from web import application
from web.application import config
from web import template
from web import util
from web import userService
from web import imgService
import imghdr
import logging
import urllib
import urllib2
import os

__IMG_TYPES__ = ['jpeg','png','bmp','gif']
try: # Windows needs stdio set for binary mode.
	import msvcrt
	msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
	msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
	pass

class Upload(object):
	"""docstring for userPage"""
	def __init__(self):
		pass

	@staticmethod	
	def GET(argus,cookie):
		logging.warning('Upload.py: Not surpose to use get method')
		temp = templateService(config)
		temp.redirect('user')

	@staticmethod
	def POST(argus,cookie):
		logging.debug('Upload.POST called.')
		us = userService.UserService()
		if us.cookie_check(cookie):
			username = cookie['username'].value
			userinfo = us.get_user(username)
			temp = template.TemplateService(config)
			imgs = imgService.ImgService(config)

			useremail = userinfo[2]
			imgfile=  argus['imgfile']
			if imgfile.filename:
				imgdata = imgfile.file.read()
				try:
					if imghdr.what('',imgdata) in __IMG_TYPES__:
						logging.debug('user upload: file(%s),type(%s)',argus['imgfile'].filename,imghdr.what('',imgdata))
						if imgs.save_img(username,useremail,imgdata):
							temp.redirect('user',cookie)
						else:
							logging.error('save file failed!')
							temp.redirect('user',cookie)
					else:
						replace_dict = {}
						replace_dict['__SERVER_MSG__'] = u'不支持的图片格式'
						replace_dict['__JUMP_URL__'] = 'user'
						temp.set_replaceDict(replace_dict)
						temp.loadtemplate('jump')
						temp.write(cookie)
				except Exception, e:
					logging.error('img upload failed:%s',e)
					replace_dict = {}
					replace_dict['__SERVER_MSG__'] = u'未能上传图片'
					replace_dict['__JUMP_URL__'] = 'user'
					temp.set_replaceDict(replace_dict)
					temp.loadtemplate('jump')
					temp.write(cookie)

			elif argus.getvalue('img_url'):
				img_url = argus.getvalue('img_url')
				replace_dict = {}
				if not img_url.startswith('http://'):
					img_url = 'http://'+img_url
				try:
					data = urllib2.urlopen(img_url,timeout=5).read()
					if imghdr.what('',data) in __IMG_TYPES__:
						logging.debug('saving net img...%s',img_url)
						if imgs.save_img(username,useremail,data):
							temp.redirect('user',cookie)
						else:
							logging.error('save file failed!%s',img_url)
							temp.redirect('user',cookie)
					else:
						replace_dict = {}
						replace_dict['__SERVER_MSG__'] = u'不支持的图片格式'
						replace_dict['__JUMP_URL__'] = 'user'
						temp.set_replaceDict(replace_dict)
						temp.loadtemplate('jump')
						temp.write(cookie)

				except Exception, e:
					logging.error('unable to download:%s',e)
					replace_dict['__SERVER_MSG__'] = u'未能下载网络图片'
				else:
					replace_dict['__SERVER_MSG__'] = u'图片下载并保存成功！'
				finally:
					replace_dict['__JUMP_URL__'] = 'user'
					temp.set_replaceDict(replace_dict)
					temp.loadtemplate('jump')
					temp.write(cookie)
			else:
				logging.error('Upload.py: should not get here at all')
				temp.redirect('user',cookie)

if __name__ == '__main__':
	app = application.Application()
	app.handle('upload','Upload')