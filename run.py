from flask import request
from app import create_app
from app.models.user import User
from app.utils.user_context import UserContext

app = create_app()

@app.before_request
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

@app.teardown_request
def clear_user(exception=None):
    UserContext.clear()

@app.route("/")
def index():
    return "hello world!"

@app.errorhandler(403)
def forbidden(e):
    return {
        "code": 403,
        "msg": "Forbidden"
    }, 403


@app.errorhandler(404)
def page_not_found(e):
    return {
        "code": 404,
        "msg": "Not Found"
    }, 404


@app.errorhandler(500)
def internal_server_error(e):
    return {
        "code": 500,
        "msg": "Internal Server Error"
    }, 500

@app.errorhandler(Exception)
def internal_server_error1(e):
    return {
        "code": 400,
        "success": False,
        "msg": "失败",
        "data": e.args[0]
    }, 400

def snake_to_camel(snake_str):
    components = snake_str.split('_')
    # 第一个单词保持小写，后续单词首字母大写
    return components[0] + ''.join(x.title() for x in components[1:])

if __name__ == "__main__":
    app.run(debug=True)
