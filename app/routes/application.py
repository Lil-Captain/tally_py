from flask import Blueprint, render_template, redirect, url_for, request, flash

from app.form import UserForm
from app.models.user import User
from app.extensions import db

app_db = Blueprint("app", __name__)

# ---------- 主页 ----------
@app_db.route("/")
def index():
    return render_template('index.html')

# ---------- 通用列表/增删改查路由模式（示例：User） ----------
# 列表
@app_db.route('/users')
def users_list():
    page = request.args.get('page', 1, type=int)
    search_name = request.args.get('user_name', '')
    search_alias = request.args.get('alias', '')    
    query = User.query
    if search_name:
        query = query.filter(User.user_name.like(f'%{search_name}%'))
    if search_alias:
        query = query.filter(User.alias.like(f'%{search_alias}%'))
    
    users = query.order_by(User.id.desc()).paginate(page=page, per_page=10)
    
    breadcrumb = [('首页', url_for('index')), ('用户管理', None)]
    search_fields = [
        {"name": "user_name", "label": "用户名"},
        {"name": "alias", "label": "别名"}
    ]
    return render_template('list.html', items=users, model_name='user', columns=['id','user_name','alias','create_time'], search_fields=search_fields, breadcrumb=breadcrumb)

# 创建
@app_db.route('/users/new', methods=['GET','POST'])
def users_create():
    form = UserForm()
    breadcrumb = [('首页', url_for('app.index')), ('用户管理', url_for('app.users_list')), ('新增用户', None)]
    if form.validate_on_submit():
        u = User(user_name=form.user_name.data, alias=form.alias.data)
        db.session.add(u)
        db.session.commit()
        flash('用户创建成功。')
        return redirect(url_for('app.users_list'))
    return render_template('form.html', form=form, model_name='user', breadcrumb=breadcrumb)

# 编辑
@app_db.route('/users/<int:id>/edit', methods=['GET','POST'])
def users_edit(id):
    u = User.query.get_or_404(id)
    form = UserForm(obj=u)
    breadcrumb = [('首页', url_for('app.index')), ('用户管理', url_for('app.users_list')), ('编辑用户', None)]
    if form.validate_on_submit():
        u.user_name = form.user_name.data
        u.alias = form.alias.data
        db.session.commit()
        flash('用户更新成功。')
        return redirect(url_for('app.users_list'))
    return render_template('form.html', form=form, model_name='user', breadcrumb=breadcrumb)

# 删除
@app_db.route('/users/<int:id>/delete', methods=['POST'])
def users_delete(id):
    u = User.query.get(id)
    if not u:
        flash('用户不存在，删除失败。')
        return redirect(url_for('app.users_list'))
    db.session.delete(u)
    db.session.commit()
    flash('用户删除成功。')
    return redirect(url_for('app.users_list'))