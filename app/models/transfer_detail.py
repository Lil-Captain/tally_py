from app.extensions import db
from app.utils.string_utils import StringUtil

class TransferDetail(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    room_id = db.Column(db.BigInteger)
    payer_user_id = db.Column(db.BigInteger)
    payee_user_id = db.Column(db.BigInteger)
    amount = db.Column(db.Numeric(10, 2))
    create_time = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {StringUtil.snake_to_camel(c.name): getattr(self, c.name) for c in self.__table__.columns}
