from flask import render_template, request
from app import create_app
from app.models.user import User
from app.utils.user_context import UserContext

app = create_app()

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

def snake_to_camel(snake_str):
    components = snake_str.split('_')
    # 第一个单词保持小写，后续单词首字母大写
    return components[0] + ''.join(x.title() for x in components[1:])

if __name__ == "__main__":
    app.run(debug=True)
