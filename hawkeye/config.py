class Config(object):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = ''# Put your MySQL root password here
    MYSQL_DATABASE_DB = 'Hawkeye'
    MYSQL_DATABASE_HOST = 'localhost'
    
class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD=True
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = 'RahulRB@1997'# Put your MySQL root password here
    MYSQL_DATABASE_DB = 'Hawkeye'
    MYSQL_DATABASE_HOST = 'localhost'

class TestingConfig(Config):
    TESTING = True