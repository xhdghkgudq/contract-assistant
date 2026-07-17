# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost/contract_ai"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret"