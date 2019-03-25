 
import pymysql,json
 

file = "UsersData/users3.02.txt"

# 打开数据库连接
db = pymysql.connect("localhost","root","712srxsj","bilibili" )
 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
 
def insert_db(user):
	sql1 = "select * from users"
	sql2 = "show tables"
	if user.get('level')==None:
		user['level']=-1
	if user.get('archive_view')==None:
		user['archive_view']=-1
	if user.get('article_view')==None:
		user['article_view']=-1
	if user.get('video')==None:
		user['video']=-1
	if user.get('coins')==None:
		user['coins']=-1
	if user.get('follower')==None:
		user['follower']=-1
	if user.get('following')==None:
		user['following']=-1
	if user.get('mid')==None:
		return
	sql3 = "insert into users (mid,name,face,level,sex,official_verify,sign,tags,regtime,birthday,archive_view,article_view,video,coins,follower,following) \
	values('%d','%s','%s','%d','%s','%s','%s','%s','%s','%s','%d','%d','%d','%d','%d','%d')"%\
	(int(user.get('mid')),pymysql.escape_string(user.get('name')),pymysql.escape_string(user.get('face')),int(user.get('level')),\
user.get('sex'),pymysql.escape_string(user.get('official_verify')),pymysql.escape_string(user.get('sign')),pymysql.escape_string(user.get('tags')),\
user.get('regtime'),user.get('birthday'),int(user.get('archive_view')),int(user.get('article_view')),int(user.get('video')),int(user.get('coins')),int(user.get('follower')),int(user.get('following')))
	sql4 = "select mid from users where mid=%d"%int(user.get('mid'))
	#print(sql3)
	# 使用 execute()  方法执行 SQL 查询 
	#cursor.execute("SELECT VERSION()")
	cursor.execute(sql4)	 
	data = cursor.fetchone()
	if data:
		return;
	#print ("Database version : %s " % data)
	cursor.execute(sql3) 
	db.commit()
 
with open (file,'r') as fp:
	while True:
		line = fp.readline()
		#print(line)
		if not line:
			break
		if line[0]=="{":
			string=""+line
		#elif line[0]=='"':
		else:
			string+=line
		if line[0]=="}":
			string = string[:-2]
			#print(string)
			user = json.loads(string)
			#print(string)
			insert_db(user)

# 关闭数据库连接
db.close()
