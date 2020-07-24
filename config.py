import os
basedir=os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@localhost/flask"
    FLASKY_MAIL_SUBJECT_PREFIX='[Flasky]'
    FLASKY_MAIL_SENDER='Flasky Admin <973900834@qq.com'
    FLASKY_ADMIN=os.environ.get('FLASKY_ADMIN')
    @staticmethod
    def init_app(app):
        pass
class DevelopmentConfig(Config):
    DEBUG=True
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:root@localhost/flask"
class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:root@localhost/flask"
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:root@localhost/flask"


config={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig,
}
appiumconfig={
    'platformName':'Android',
    'platformVersion':'6.0.1',
    'deviceName':'127.0.0.1:7555',
    'resetKeyboard':'true',
    'automationName':'UiAutomator1',
    'noReset':'True',
    'url':'http://localhost:4723/wd/hub'
}
emailConifg = {
    'MAIL_SERVER':'smtp.qq.com',
    'MAIL_PORT':587,
    'MAIL_USE_TLS':True,
    'MAIL_USERNAME':'2718742015@qq.com',
    'MAIL_PASSWORD':"phkjrlxrtvzvdecj"
}