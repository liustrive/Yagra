"""
easeYagra database API

"""
import MySQLdb


_host="127.0.0.1"
_user="easeyagra"
_passwd="!@#$easeyagra"
_db="easeyagra"
_charset="utf8"

class database(object):
	"""basic database api"""
	def __init__(self):
		self.db = MySQLdb.connect(host=_host,
                     user=_user,
                     passwd=_passwd,
                     db=_db,
                     port=3306,
                     charset=_charset)
	def db_execute(self, sql):
		try:
			c=self.db.cursor()
			c.execute(sql)
			return c.fetchone()
		except Exception, e:
			raise
		
	def commit(self):
		self.db.commit()

	def rollback(self,sql):
		return



if __name__ == '__main__':
    db = database()
    sql = "insert into User values( \
                          'liulian@$#@', \
                          '!@#$asdfasdf', \
                          'liustrive@gmail.com', \
                          '2015-03-21 00:00:00', \
                          '0', \
                          'liustrive' \
                      );"
 
    #print db.db_execute('select * from User limit 3;')