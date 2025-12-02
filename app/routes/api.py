from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.models.room import Room
from app.models.transfer_detail import TransferDetail
from app.models.user import User
from app.models.user_room_relation import UserRoomRelation
from app.repositories.transfer_detail_req import TransferDetailReq
from app.services.room_service import RoomService
from app.utils.user_context import UserContext
from app.services.user_service import UserService

api_bp = Blueprint("api", __name__)
user_service = UserService()
room_service = RoomService()

@api_bp.before_request
def authenticate():
    # 获取请求的路径
    request_path = request.path;
    # breakpoint()
    if request_path != "/v1/api/getOpenId" and request_path != "/v1/api/isUserInfo":
        open_id = request.headers.get("openId", "")
        if open_id.strip() == "":
            return {"code":401,"success":False,"message":"Unauthorized","data":None}, 401
        user = User.query.filter_by(open_id=open_id).first()

        if not user:
            return {"code":401,"success":False,"message":"Unauthorized","data":None}, 401
        UserContext.set_user(user)

@api_bp.teardown_request
def clear_user(exception=None):
    UserContext.clear()

@api_bp.errorhandler(Exception)
def internal_server_error1(e):
    return {
        "code": 400,
        "success": False,
        "msg": "失败",
        "data": e.args[0]
    }, 400


@api_bp.route("/joinRoom", methods=["POST"])
def join_room():
    api_request = request.get_json(silent=True) or request.form or {}
    flag = user_service.join_room(api_request.get("roomId", ""))
    if flag:
        return api_respose(200, flag)
    else:
        return api_respose(500, flag)

@api_bp.route("/userHistoryInfo", methods=["POST"])
def user_history_info():
    data = user_service.user_history_info()
    if data:
        return api_respose(200, data)
    else:
        return api_respose(500, data)

@api_bp.route("/getUserInfo", methods=["POST"])
def get_user_info():
    user = UserContext.get_user()
    if user:
        return api_respose(200, user.to_dict())
    else:
        return api_respose(500, {})

@api_bp.route("/getRoomInfo", methods=["POST"])
def get_room_info():
    user_room_relation = UserRoomRelation.query.filter_by(user_id=UserContext.get_user().id, status=0).first()

    if user_room_relation: 
        return api_respose(200, Room.query.get(user_room_relation.room_id).to_dict())
    else:
        return api_respose(200, None)

@api_bp.route("/getOpenId", methods=["POST"])
def get_open_id():
    api_request = request.get_json(silent=True) or request.form or {}
    user = User.query.filter_by(user_name = api_request.get("userName", "")).first()
    if user:
        return api_respose(200, user.open_id)
    else:
        return api_respose(400, None, "用户不存在")

# TODO /setUserAvatar

# 修改别名
@api_bp.route("/setUserName", methods=["POST"])
def set_alias():
    api_request = request.get_json(silent=True) or request.form or {}
    flag = user_service.set_alias(api_request.get("alias"))
    
    if flag:
        return api_respose(200, flag)
    else:
        return api_respose(500, flag)

@api_bp.route("/buildRoom", methods=["POST"])
def build_room():
    # 检查下当前用户是否还有未结束的对局
    user_room = UserRoomRelation.query.filter_by(user_id=UserContext.get_user().id, status=0).first()
    if not user_room is None:
        return api_respose(200, {}, "你还有对局未结束,请先结束对局再开始")
    
    room = room_service.build_room()
    if room:
        return api_respose(200, room.to_dict())
    else:
        return api_respose(500, False)

@api_bp.route("/roomTransferDetails", methods=["POST"])
def room_transfer_details():
    api_request = request.get_json(silent=True) or request.form or {}

    room = Room.query.get(api_request.get("roomId", ""))
    if room is None:
        return api_respose(403, {}, "房间不存在")
    
    transfer_details = TransferDetail.query.filter_by(room_id=room.id).order_by(TransferDetail.create_time.desc()).all()
    data = []
    for transfer_detail in transfer_details:
        json = transfer_detail.to_dict()
        json["amount"] = int(json["amount"])
        json["createTime"] = json["createTime"].strftime("%Y年%m月%d日 %H:%M:%S")
        json["payerUser"] = User.query.get(json["payerUserId"]).to_dict()
        json["payeeUser"] = User.query.get(json["payeeUserId"]).to_dict()
        json.pop("payerUserId")
        json.pop("payeeUserId")
        data.append(json)
    if room:
        return api_respose(200, data)
    else:
        return api_respose(500, False)

@api_bp.route("/roomTransfer", methods=["POST"])
def room_transfer():
    api_request = request.get_json(silent=True) or request.form or {}
    try:
        transfer_detail_req = TransferDetailReq.model_validate(api_request)
    except ValidationError as e:
        raise Exception(f"[{__name__}] transfer_detail_req 校验失败！Error: {str(e)}")
    
    flag = room_service.create_transfer_detail(transfer_detail_req)

    return api_respose(200, flag)

@api_bp.route("/exitRoom", methods=["POST"])
def exit_room():
    api_request = request.get_json(silent=True) or request.form or {}
    
    flag = room_service.exit_room(int(api_request.get("roomId", "0")))

    return api_respose(200, flag)

@api_bp.route("/roomCommonInfo", methods=["POST"])
def room_common_info():
    api_request = request.get_json(silent=True) or request.form or {}
    
    room_detail = room_service.room_common_info(int(api_request.get("roomId", "0")))

    return api_respose(200, room_detail)

# TODO  getRoomCode

@api_bp.route("/userHistoryInfoDetails", methods=["POST"])
def user_history_info_details():
    room_user_case_list = room_service.user_history_info_details()

    return api_respose(200, room_user_case_list)


@api_bp.route("/isUserInfo", methods=["POST"])
def is_user_info():
    api_request = request.get_json(silent=True) or request.form or {}
    user = User.query.filter_by(user_name=api_request.get("userName"))
    
    if user:
        return api_respose(200, True, "用户名已存在")
    else:
        return api_respose(500, True, "用户名不存在")

def api_respose(code, data, message="成功", success=True):
    if code != 200:
        message = "失败"
        success = False
    json = {
    "code": code,
    "success": success,
    "message": message,
    "data": data
    }, code
    
    return json
