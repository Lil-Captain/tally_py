import logging
from app.extensions import db
from app.models.room import Room
from app.models.user_room_relation import UserRoomRelation
from app.utils.user_context import UserContext

logger = logging.getLogger(__name__)
class UserService:
    def join_room(self, room_id):
        # 检查房间是否存在
        # breakpoint()
        room = Room.query.get(room_id)
        if room is None:
            raise Exception("房间不存在")
        user = UserContext.get_user()
        logger.info(f"用户：{user.user_name},加入房间{room.id}")
        # 检查下当前用户是否还有未结束的对局
        user_room = UserRoomRelation.query.filter_by(user_id=user.id, status=0).first()
        if user_room is not None:
            raise Exception("你还有对局未结束，请先结束对局再开始")
        
        # 判断当前用户是否已经绑定过该房间了
        user_room_exist = UserRoomRelation.query.filter_by(user_id=user.id, room_id=room_id).first()
        if user_room_exist is None:
            user_room_relation = UserRoomRelation(
                user_id=user.id,
                room_id=room_id,
                status=0,
                )
            db.session.add(user_room_relation)
        else:
            user_room_exist.status = 0
        db.session.commit()
        return True

    def user_history_info(self):
        user = UserContext.get_user()
        user_room_infos = UserRoomRelation.query.filter_by(user_id=user.id).all()
        victories_count = len([info for info in user_room_infos if info.victory_flag == 1])
        loss_count = len([info for info in user_room_infos if info.victory_flag == 0])
        win_rate = 0 if len(user_room_infos) == 0 else round(victories_count / len(user_room_infos), 2) * 100
        return {
            "userName": user.user_name,
            "userAvatar": user.avatar,
            "victories": victories_count,
            "losses": loss_count,
            "winRate": f"{win_rate}%"
        }
    
    def set_alias(self, alias):
        try:
            user = UserContext.get_user()
            user.alias = alias
            db.session.commit()
            return True
        except Exception as e:
            logger.info (f"[{__name__}] Error {str(e)}")
            return False
