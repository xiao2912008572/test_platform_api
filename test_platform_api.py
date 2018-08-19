from flask import Flask
from flask_cors import CORS

import config
from exts import db
from api.v1.env.Env import env_bp
from api.v1.project.Porject import project_bp
from api.v1.status.Status import status_bp
from api.v1.api.Api import api_group_bp

# from flask_wtf import CSRFProtect  # 添加csrf保护模块


# 工厂函数：用于注册
def create_app():
    app = Flask(__name__)
    # 解决跨域问题
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(config)

    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(env_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(api_group_bp)

    # CSRFProtect(app)  # 这样就可以拥有CSRF保护了

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8000)
