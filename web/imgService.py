from  _mysql_exceptions import IntegrityError
import db
import util
import time
import logging

class ImgService(object):
	"""docstring for imgService"""
	def __init__(self,config):
		if not globals().get('db_instance'):
			global db_instance
			db_instance = db.database()
		self.db_ins = db_instance
		self._IMG_UPLOAD_ = config.get('_IMG_UPLOAD_PATH_')

	def get_image_name(self,img_info):
		if img_info:
			return img_info[2]
		else:
			return None

	def get_image_by_username(self,username):
		sql = "SELECT * FROM Images WHERE user_name='%s';" % util.escape(username)
		img_info = self.db_ins.db_execute(sql)
		return self.get_image_name(img_info)

	def get_image_by_hash(self,hashcode):
		sql = "SELECT * FROM Images WHERE hashcode='%s';" % hashcode
		img_info = self.db_ins.db_execute(sql)
		return self.get_image_name(img_info)

	def get_img_fullpath(self,imgname):
		return self._IMG_UPLOAD_ + imgname

	def save_img(self,username,useremail,imgdata):
		hashcode = util.get_imghash(useremail)
		try:
			imgfile = open(self.get_img_fullpath(hashcode),'wb')
			imgfile.write(imgdata)
			# hashcode user_name file_name
			sql = "INSERT INTO Images VALUES ('%s','%s','%s') \
				ON DUPLICATE KEY UPDATE file_name='%s';" % (
				hashcode,
				util.escape(username),
				hashcode,
				hashcode)
			self.db_ins.db_execute(sql)
			self.db_ins.commit()
			return True
		except IntegrityError as e:
			logging.error('save_img failed: %s',e)
			return False


