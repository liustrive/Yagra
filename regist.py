#!D:\Python27\python.exe
# -*- coding: UTF-8 -*-

from web import application
from web.application import config
from web import template
from web import util
from web import userService
from web import imgService
import logging

class RegistPage(object):
	"""docstring for userPage"""
	def __init__(self):
		pass

	@staticmethod
	def GET(argus,cookie):
		us = userService.UserService()
		temp = template.TemplateService(config)
		# do not do cookie check
		temp.loadtemplate('regist')
		temp.write(cookie)
			
	@staticmethod	
	def POST(argus,cookie):
		username = argus.getvalue('username')
		password = argus.getvalue('password')
		password2 = argus.getvalue('password2')
		useremail = argus.getvalue('useremail')
		usernick = argus.getvalue('usernick')
		replace_dict = {}

		us = userService.UserService()
		temp = template.TemplateService(config)
		if not username or not password or not password2 or not useremail or not usernick:
			replace_dict['__SERVER_MSG__'] = u'请填写完整表单'
			temp.set_replaceDict(replace_dict)
			temp.loadtemplate('regist')
			temp.write(cookie)
			return
		logging.debug('(%s,%s,%s,%s,%s)',(username,password,password2,useremail,usernick))
		# this is ugly...
		if password != password2: # this should be checked at front end
			replace_dict['__SERVER_MSG__'] = u'两次输入密码不相同'
			temp.set_replaceDict(replace_dict)
			temp.loadtemplate('regist')
			temp.write(cookie)
		elif not util.check_username(username):
			replace_dict['__SERVER_MSG__'] = u'请输入正确的用户名'
			temp.set_replaceDict(replace_dict)
			temp.loadtemplate('regist')
			temp.write(cookie)
		elif not util.check_email(useremail):
			replace_dict['__SERVER_MSG__'] = u'邮箱格式不符'
			temp.set_replaceDict(replace_dict)
			temp.loadtemplate('regist')
			temp.write(cookie)
		elif not util.check_password(password):
			replace_dict['__SERVER_MSG__'] = u'密码格式不符'
			temp.set_replaceDict(replace_dict)
			temp.loadtemplate('regist')
			temp.write(cookie)
		elif us.get_user(username):
			replace_dict['__SERVER_MSG__'] = u'用户名已存在'
			temp.set_replaceDict(replace_dict)
			temp.loadtemplate('regist')
			temp.write(cookie)
		elif us.get_email(useremail):
			replace_dict['__SERVER_MSG__'] = u'邮箱已注册'
			temp.set_replaceDict(replace_dict)
			temp.loadtemplate('regist')
			temp.write(cookie)
		else:
			# add_user(self,username,password,email='',status = 0,nick = '')
			if us.add_user(username=username,password=password,email=useremail,nick=usernick):
				us.user_token(username,cookie)
				replace_dict['__SERVER_MSG__'] = u'注册成功！'
				replace_dict['__JUMP_URL__'] = 'user'
				temp.set_replaceDict(replace_dict)
				temp.loadtemplate('jump')
				temp.write(cookie)
			else:
				logging.error('fail to add user: (%s,%s,%s,%s)',(username,password,useremail,usernick))
				replace_dict['__SERVER_MSG__'] = u'注册失败！'
				replace_dict['__JUMP_URL__'] = 'regist'
				temp.set_replaceDict(replace_dict)
				temp.loadtemplate('jump')
				temp.write(cookie)
if __name__ == '__main__':
	app = application.Application()
	app.handle('regist','RegistPage')