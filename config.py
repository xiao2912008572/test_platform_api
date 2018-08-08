# Author:Xiaojingyuan
HOSTNAME = '118.25.48.34'
PORT = '3306'
DATABASE = 'test_platform_api'
USERNAME = 'root'
PASSWORD = '123456'

# DB_URI 连接数据库的配置字符串
DB_URI = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8'.format(
    username=USERNAME,
    password=PASSWORD,
    host=HOSTNAME,
    port=PORT,
    db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
