import sys
import util
import os
import logging


__HTTP_ERROR__ = {
	'404':'Page not found'
}
__PAGE_TEMPLATE__ = {
	'index':'web/html/index.html',
	'user':'web/html/user.html',
	'login':'web/html/login.html',
	'error':'web/html/error.html',
	'regist':'web/html/regist.html',
	'jump':'web/html/jump.html',
}
class TemplateService(object):
	"""docstring for templateService"""
	def __init__(self, config):
		replaceDict = {}
		replaceDict['__USER_NAME__'] = config['__default_user_name__']
		replaceDict['__USER_HEAD_IMG__'] = config['__default_user_img__']
		replaceDict['__USER_NICK__'] = config['__default_user_nick__']
		replaceDict['__USER_EMAIL__'] = config['__default_user_email__']
		replaceDict['__USER_LAST_TIME__'] = config['__default_last_time__']
		replaceDict['__SERVER_MSG__'] = config['__default_server_msg__']
		replaceDict['__ERROR_CODE__'] = '404'
		replaceDict['__ERROR_MSG__'] = 'Page not found'
		replaceDict['__JUMP_URL__'] = ''
		self.rep_dict = replaceDict
		self.content_type = "text/html"
		self.char_set = config['__default_char_set__']
		self.html = []

	def set_type(self,cnt_type):
		self.content_type = cnt_type

	def redirect(self,page,cookie):
		#sys.stdout.write('Content-Type: %s; charset=%s' % (self.content_type,self.char_set))
		logging.debug(cookie.output())
		print cookie.output()
		#print 'Content-Type: %s; charset=%s\n' % (self.content_type,self.char_set)
		print 'Location: %s' % page
		print

	def set_replaceDict(self,replace_dict):
		for k,v in replace_dict.iteritems():
			if k in self.rep_dict:
				self.rep_dict[k] = v

	def loadtemplate(self,filectg):
		filepath = __PAGE_TEMPLATE__.get(filectg)
		with open(filepath, 'rb') as filehandle:
			tempdata = filehandle.read().decode('utf8')
			logging.debug(str(self.rep_dict))
			filedata = util.multi_replace(tempdata,self.rep_dict)
			self.html = filedata.encode(self.char_set)

	def write(self,cookie):
		print cookie.output()
		print 'Content-Type: %s; charset=%s\n' % (self.content_type,self.char_set)
		print self.html
		#sys.stdout.write('<html><body>what?</body></html>')

	def write_img(self,data):
		print 'Content-Type: %s\nContent-Length: %d\n' % (self.content_type,len(data))
		logging.debug('Content-Type: %s\nContent-Length: %d\n' , self.content_type,len(data))
		sys.stdout.write(data)

	def error(self,errornum):
		with open(__PAGE_TEMPLATE__['error'],'rb') as t:
			template = t.read().decode('utf8')
			if errornum in __HTTP_ERROR__:
				self.rep_dict['__ERROR_CODE__'] = errornum
				self.rep_dict['__ERROR_MSG__'] = __HTTP_ERROR__.get(errornum)
			self.html = util.multi_replace(template,self.rep_dict).encode(self.char_set)
    		