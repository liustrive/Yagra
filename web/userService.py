from  _mysql_exceptions import IntegrityError
import db
import util
import time
import logging

SALT_LENGTH = 12

class UserService(object):
	"""docstring for userService"""
	def __init__(self):
		if not globals().get('db_instance'):
			global db_instance
			db_instance = db.database()
		self.db_ins = db_instance

	def add_user(self,username,password,email='',status = 0,nick = ''):
		password = util.utf8(password)
		salt = util.gen_salt()
		passhash = util.get_passhash(password,salt)
		try:
			sql = "INSERT INTO User VALUES ( '%s','%s','%s','%s','%s','%s','%s');" % (
				util.escape(username),
				util.escape(passhash),
				util.escape(email),
				time.strftime('%Y-%m-%d %H:%M:%S'),
				str(0),
				util.escape(nick),
				util.escape(salt),
				)
			logging.debug(sql)
			self.db_ins.db_execute(sql)
			self.db_ins.commit()
			return True
		except IntegrityError as e:
			return False
		
	def del_user(self,username):
		try:
			sql = "DELETE FROM User WHERE user_name= '%s';" % util.escape(username)
			self.db_ins.db_execute(sql)
			self.db_ins.commit()
			return True
		except IntegrityError as e:
			return False

	def get_user(self,username):
		sql = "SELECT * FROM User WHERE user_name = '%s';" % util.escape(username)
		logging.debug('get_user.sql: %s',sql)
		return self.db_ins.db_execute(sql)

	def get_email(self,email):
		sql = "SELECT * FROM User WHERE user_email = '%s';" % util.escape(email)
		return self.db_ins.db_execute(sql)

	def user_token(self,username,cookie):
		token = util.gen_token()
		timestr = time.strftime('%Y-%m-%d %H:%M:%S')
		sql = "INSERT INTO Tokens VALUES ('%s','%s','%s') \
		ON DUPLICATE KEY UPDATE user_token='%s', token_time = '%s';" % (
			util.escape(username),
			token,
			timestr,
			token,
			timestr
			)
		logging.debug('user_token.sql:%s',sql)
		try:
			self.db_ins.db_execute(sql)
			self.db_ins.commit()
			cookie['token'] = token
			cookie['username'] = username
			logging.debug('new user-token:%s,%s',username,token)
			return True
		except IntegrityError as e:
			return False

	def update_token_time(self,username,token):
		timestr = time.strftime('%Y-%m-%d %H:%M:%S')
		sql = "INSERT INTO Tokens VALUES ('%s','%s','%s') \
		ON DUPLICATE KEY UPDATE token_time = '%s';" % (
			util.escape(username),
			token,
			timestr,
			timestr
			)
		try:
			self.db_ins.db_execute(sql)
			self.db_ins.commit()
			return True
		except IntegrityError as e:
			return False
	def del_user_token(self,username):
		sql = "DELETE FROM Tokens WHERE user_name= '%s';" % (util.escape(username))
		try:
			self.db_ins.db_execute(sql)
			self.db_ins.commit()
			return True
		except IntegrityError as e:
			return False

	def valide_token(self,username,token):
		sql = "SELECT * FROM Tokens WHERE user_name='%s';" % util.escape(username)
		logging.debug('valide_token.sql:%s',sql)
		try:
			tokens_info = self.db_ins.db_execute(sql)
			if tokens_info:
				user_name = tokens_info[0]
				true_token = tokens_info[1]
				lasttime = tokens_info[2]
				logging.debug('valide_token.true_token:%s,cookie_token:%s,lasttime:%s',true_token,token,lasttime)
				if not util.valide_token_time(str(lasttime)):
					logging.info("user token expires of user: %s" % username)
					# delete token
					if not self.del_user_token(username):
						logging.error("del_user_token failed for user: %s" % username)
					return False
				if token == true_token:
					# update token
					logging.debug('valide_token passed for user:%s',username)
					if not self.update_token_time(username,token):
						logging.error("update_token_time failed for user: %s" % username)
					return True
				else:
					return False
			else:
				return False
		except IntegrityError as e:
			return False

	def cookie_check(self,cookie):
		if not cookie or 'username' not in cookie or 'token' not in cookie:
			logging.debug(str(cookie))
			return False
		else:
			username = cookie['username'].value
			token = cookie['token'].value
			logging.debug('user:%s,token:%s',username,token)
			if not util.check_username(username) or not util.check_token(token):
				logging.warning('invalid user or token:u->%s,t->%s',username,token)
				return False
			return self.valide_token(username,token)
		
	def account_check(self,username,password):
		if not util.check_username(username) or not util.check_password(password):
			logging.info('name(%s) or passwd(%s) str not valid!',username,password)
			return False
		logging.debug('account_check:%s,%s',username,password)
		user_info = self.get_user(username)
		logging.debug('user_info:%s,len:%s',str(user_info),str(len(user_info)))
		if user_info:
			passhash = user_info[1]
			salt = user_info[6]
			logging.debug('us.account_check:pass(%s),passhash(%s),truehash(%s)',password,util.get_passhash(password,salt),passhash)
			if util.get_passhash(password,salt) == passhash:
				return True
			else:
				return False
		else:
			return False

	def user_logout(self,username,cookie):
		cookie['username'] = None
		cookie['token'] = None
		return self.del_user_token(username)