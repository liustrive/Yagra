import random
import hashlib
import MySQLdb
import os
import datetime,time
import re
import logging

__all__ = ['utf8','gen_salt','get_passhash','escape','gen_token','multi_replace','get_imghash','check_username','check_token']

SALT_LENGTH = 12
TOKEN_LENGTH = 16
TOKEN_EXPIRE = 10 # days
ALPH = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def utf8(value):
    if isinstance(value, (type(None), str)):
        return value
    assert isinstance(value, unicode)
    return value.encode("utf-8")

def gen_salt():
	return ''.join(random.choice(ALPH) for i in range(SALT_LENGTH))

def get_passhash(password,salt):
	ph = hashlib.sha256()
	ph.update(password)
	ph.update(salt)
	return ph.hexdigest()

def escape(string):
	return MySQLdb.escape_string(string)

def gen_token():
	return hashlib.sha1(os.urandom(TOKEN_LENGTH)).hexdigest()

def valide_token_time(timestr):
	try:
		dt = datetime.datetime.strptime(timestr,'%Y-%m-%d %H:%M:%S')
		logging.debug('token days:%d',(datetime.datetime.now()-dt).days)
		if not dt or (datetime.datetime.now()-dt).days > TOKEN_EXPIRE:
			return False
		else:
			return True
	except Exception, e:
		logging.error('fail to valide_token_time. msg: %s',e)
		return False

def multi_replace(string, strdict):
	pattern = re.compile(r'(' + '|'.join(strdict.keys()) + r')')
	return pattern.sub(lambda x: strdict[x.group()], string)

def get_imghash(email):
	return hashlib.md5(email.lower()).hexdigest()

def check_username(username):
	length = len(username)
	if length >5 and length<=30:
		return not bool(re.compile("[^a-z0-9]").search(username))
	else:
		return False

def check_token(token):
	return not bool(re.compile("[^0-9a-z]").search(token))

def check_password(passwd):
	length = len(passwd)
	if length >5 and length<=60:
		return True
	else:
		return False

def check_email(email):
	return bool(re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-])*\.[a-zA-Z]{2,4}$").match(email))
def check_hash(hashcode):
	#TODO
	return not bool(re.compile("[^a-z0-9]").search(hashcode))

if __name__ == '__main__':
	#salt = gen_salt()
	#print salt
	#print hashlib.sha256('liu').digest()
	#print get_passhash('liu',salt)
	#print escape(token)
	'''
	timestr = time.strftime('%Y-%m-%d %H:%M:%S')
	print timestr
	print valide_token_time(timestr)
	print valide_token_time('asdf')
	print valide_token_time('2015-3-12 00:00:00')
	'''
	string = '<p class="text-danger">__SERVER_MSG__</p>'
	strdict = {'$__ERROR_CODE__': '404', '$__USER_NAME__': '', '$__ERROR_MSG__': 'Page not found', '$__JUMP_URL__': '', '__SERVER_MSG__': '', '$__USER_NICK__': '', '$__USER_LAST_TIME__': '', '$__USER_HEAD_IMG__': '', '$__USER_EMAIL__': ''}
	print string
	print multi_replace(string,strdict)
