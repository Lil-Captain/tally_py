from app.extensions import db
from app.utils.string_utils import StringUtil

class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    open_id = db.Column(db.String(255))
    user_name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    avatar = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, server_default=db.func.now())
    update_time = db.Column(db.DateTime, server_default=db.func.now()) 

    def to_dict(self):
        return {StringUtil.snake_to_camel(c.name): getattr(self, c.name) for c in self.__table__.columns}