#Yagra （Yet Another GRAvatar)
Gravatar.com是一个提供avatar hosting服务的站点，你可以在Gravatar上编辑和管理你的头像，然后在其他支持Gravatar的站点上使用，比如Github，Wordpress等站点都使用其服务。

Yagra模仿Gravatar的功能，完成了一个简单版的avatar hosting站点。

##设计
###特点
* 程序基于CGI协议运行
* 除了mysql-python之外，仅使用Python标准库
* 实现了一个简易的web	框架以拆分功能逻辑和cgi基础操作
* 拆分前后端设计，前端html的生成效仿Pelican的Template方案，后端视效无关，仅关心动态元素的生成
* Template的套用有些naive……，基于批量替换实现

###安全性
* 用户登陆后采用浏览器COOKIE保存随机TOKEN，TOKEN具有效期和字串安全性检查
* 用户密码在数据库中采用随机盐SHA256哈希加密存储，防止发生托库后密码流失
* 所有表单采取严格字串检查，数据库sql执行参数经过处理，防止sql注入
* 所有对外页面均进行COOKIE检查，并进行安全验证，防止伪造COOKIE的REQUEST
* 用户上传文件或指定的网络文件经过内容检查，判断格式并防止恶意攻击

###Avatar API
######URL: 
	/avatar/{hashlib.md5(useremail.lower).hexdigest()}
成功返回用户头像

失败返回/default/default.jpg

###主要功能
* 主页

	/index
* 注册

	/regist
* 登陆

	/login
* 用户Home Page (上传本地文件或网络文件)

	/user
* 登出

	/logout
* Avatar Service

	/avatar/(email's md5)

##环境搭建

###系统依赖
* Apache 2.2.25
* Python 2.7
* MySQL 5.6
* mysql-python 1.2.5

###部署Yagra

####配置Apache
1.启动rewite Engine
	
LoadModule rewrite_module modules/mod_rewrite.so

2.配置httpd.conf 

	DocumentRoot /Yagra/
	<Directory /Yagra/>
	    AllowOverride None
	
	    RewriteEngine on
	    RewriteRule ^avatar/([0-9a-f]{32})$ avatar.py?emailhash=$1
	    RewriteRule ^([a-z]+)$ $1.py

	    ErrorDocument 404 web/html/errordoc.html
	
	    AddHandler cgi-script .py
	    Options -Indexes +ExecCGI -MultiViews -SymLinksIfOwnerMatch
	
	    DirectoryIndex index.py
	
	    Order allow,deny
	    Allow from all
	
	</Directory>
3.重启Apache Server

####数据库创建
参见create_database.sql，用于创建数据库表和Yagra用户

	mysql -u root -p < create_database.sql

####部署文件

######功能逻辑：

* avatar.py

	提供Avatar API
* index.py

	网站主页
* user.py

	处理用户Home页的handler
* login.py logout.py

	登陆登出操作的handler
* regist.py

	注册操作handler
* upload.py
	
	上传文件的handler

######简易框架
位于web目录下
* server.conf
	
	 # template elements
	__default_user_name__=''
	__default_user_img__='default/default.jpg'
	__default_user_nick__=''
	__default_user_email__=''
	__default_last_time__=''
	__default_server_msg__=''
	
	 #settings
	__default_char_set__='utf8'
	_IMG_UPLOAD_PATH_='web/upload/'

其中template elements用于handler生成动态元素

* application.py

	基础cgi操作封装
* template.py

	html页面生成器
* db.py

	数据库操作的简易封装
* util.py

	基础工具箱
* userService。py
	
	用户对象操作封装
* imgService.py

	图片服务操作封装

######其它目录
* Yagra/html

	网站模板文件，在遵循动态元素的关键字基础上，可以任意替换成其它视觉效果

* Yagra/upload

	默认的图片上传目录，可以在server.conf中修改


###TODO
简易web框架对URL的处理缺少一个分配器，设计上留出了空间，实现较易，奈何最近散伙饭太太太多T…T，丑陋的就提交了先Orz