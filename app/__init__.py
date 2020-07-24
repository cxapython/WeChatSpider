from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
boostrap=Bootstrap()
mail=Mail()
moment=Moment()
db=SQLAlchemy()
def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    boostrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    #附加路由和自定义的错误页面
    #注册admin的蓝图
    from .anlysis import anlysis as admin_blueprint
    app.register_blueprint(admin_blueprint)
    return app