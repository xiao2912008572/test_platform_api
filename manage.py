# Author:Xiaojingyuan
from flask_script import Manager
from test_platform_api import create_app
from flask_migrate import MigrateCommand, Migrate
from exts import db
import models  # 导入模型

app = create_app()
manager = Manager(app)

Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
