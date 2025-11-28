from datetime import datetime
from decimal import Decimal
import logging
from app.extensions import db
from app.models import user_room_relation
from app.models.room import Room
from app.models.transfer_detail import TransferDetail
from app.models.user import User
from app.models.user_room_relation import UserRoomRelation
from app.utils.user_context import UserContext

logger = logging.getLogger(__name__)
class RoomService:
    def build_room(self):
        room = Room(
            owner_id=UserContext.get_user().id,
            room_status=0,
        )
        db.session.add(room)
        db.session.commit()
        user_room = UserRoomRelation(
            user_id=UserContext.get_user().id,
            room_id=room.id,
            status=0, 
        )
        db.session.add(user_room)
        db.session.commit()
        return room
    
    def create_transfer_detail(self, transfer_detail_req):
        room = Room.query.get(transfer_detail_req.roomId)
        if room is None:
            raise Exception("房间不存在")

        payer_user = User.query.get(transfer_detail_req.payerUserId)
        if payer_user is None:
            raise Exception("付款人用户不存在")

        payee_user = User.query.get(transfer_detail_req.payeeUserId)
        if payee_user is None:
            raise Exception("收款人用户不存在")
        
        transfer_detail = TransferDetail(
            room_id = transfer_detail_req.roomId,
            payer_user_id = transfer_detail_req.payerUserId,
            payee_user_id = transfer_detail_req.payeeUserId,
            amount = transfer_detail_req.amount
        )
        db.session.add(transfer_detail)
        db.session.commit()
        return True

    def exit_room(self, room_id):
        room = Room.query.get(room_id)
        if room is None:
            raise Exception("房间不存在")
        
        user_id=UserContext.get_user().id
        user_room_relation = UserRoomRelation.query.filter_by(room_id=room_id, user_id=user_id).first()
        if user_room_relation is None:
            raise Exception("房间不存在")
        user_room_relation.status = 1
        user_room_relation.update_time = datetime.now()
        # 结算胜负账单
        amount = self.__calculate_amount(room_id, user_id)

        if amount > 0:
            user_room_relation.victory_flag = 1
        else:
            user_room_relation.victory_flag = 0
        db.session.commit()
        return True
    
    def room_common_info(self, room_id):
        room = Room.query.get(room_id)
        if room is None:
            raise Exception("房间不存在")

        user = UserContext.get_user()
        amount = self.__calculate_amount(room.id, user.id)
        room_detail = {}
        room_detail["roomId"] = room_id
        room_detail["roomNo"] = room_id
        room_detail["roomCode"] = ""
        # 用户收支情况总览
        my_point = {}
        my_point["userPoint"] = amount
        my_point["userId"] = user.id
        my_point["userName"] = user.user_name
        my_point["userAvatar"] = user.avatar
        room_detail["myPointInfoVo"] = my_point

        user_room_relations = UserRoomRelation.query.filter_by(room_id=room_id, status=0).all()
        other_point_infos = []
        for user_room_relation in user_room_relations:
            if user_room_relation.user_id == user.id:
                continue
            other_user = User.query.get(user_room_relation.user_id)
            if other_user is None:
                continue

            other_point = {}
            other_point["userPoint"] = self.__calculate_amount(room_id, other_user.id)
            other_point["userAvatar"] = other_user.avatar
            other_point["userName"] = other_user.user_name
            other_point["userId"] = other_user.id
            other_point_infos.append(other_point)
        room_detail["otherPointInfoVo"] = other_point_infos
        room_detail["showGuide"] = False
        room_detail["showCode"] = False
        return room_detail

    def user_history_info_details(self):
        case_array = []
        user_room_relations = UserRoomRelation.query.filter_by(user_id=UserContext.get_user().id).all()
        for user_room_relation in user_room_relations:
            user_room_case = {}
            user_point = self.__calculate_amount(user_room_relation.room_id, user_room_relation.user_id)
            user_room_case["roomName"] = UserContext.get_user().user_name
            user_room_case["userPoint"] = user_point
            user_room_case["create_time"] = user_room_relation.create_time.strftime("%Y-%m-%d %H:%M:%S")
            case_array.append(user_room_case)
        return case_array

    @staticmethod
    def __calculate_amount(room_id, user_id):
        payer_amount = sum( transfer_detail.amount for transfer_detail in TransferDetail.query.filter_by(room_id=room_id, payer_user_id=user_id).all() if isinstance(transfer_detail.amount, (int, float, Decimal)))
        payee_amount = sum( transfer_detail.amount for transfer_detail in TransferDetail.query.filter_by(room_id=room_id, payee_user_id=user_id).all() if isinstance(transfer_detail.amount, (int, float, Decimal)))
        amount = payee_amount - payer_amount
        return amount