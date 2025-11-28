from app.extensions import db

class UserRoomRelation(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger)
    room_id = db.Column(db.BigInteger)
    status = db.Column(db.SmallInteger)
    victory_flag = db.Column(db.SmallInteger)
    create_time = db.Column(db.DateTime, server_default=db.func.now())
    update_time = db.Column(db.DateTime, server_default=db.func.now())
    
    # def __init__(self, user_id=None, room_id=None, status=None, victory_flag=None, **kwargs):
    #     super().__init__(**kwargs)
    #     if user_id is not None:
    #         self.user_id = user_id
    #     if room_id is not None:
    #         self.room_id = room_id
    #     if status is not None:
    #         self.status = status
    #     if victory_flag is not None:
    #         self.victory_flag = victory_flag 