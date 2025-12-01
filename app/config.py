class Config():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:zaq!@wsx@127.0.0.1:3306/tally_py"
    # 禁用修改追踪以提高性能
    SQLALCHEMY_TRACK_MODIFCATIONS = False
    SECRET_KEY = ""
