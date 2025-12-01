from ast import alias
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class UserForm(FlaskForm):
    user_name = StringField('用户名', validators=[DataRequired(), Length(max=80)])
    alias = StringField('别名', validators=[DataRequired(), Length(max=120)])
    submit = SubmitField('保存')


# class CategoryForm(FlaskForm):
# name = StringField('名称', validators=[DataRequired(), Length(max=80)])
# description = StringField('描述', validators=[Length(max=200)])
# submit = SubmitField('保存')


# class ProductForm(FlaskForm):
# name = StringField('名称', validators=[DataRequired(), Length(max=120)])
# price = DecimalField('价格', validators=[DataRequired()])
# category_id = SelectField('分类', coerce=int)
# submit = SubmitField('保存')


# class OrderForm(FlaskForm):
# user_id = SelectField('用户', coerce=int)
# product_id = SelectField('商品', coerce=int)
# quantity = IntegerField('数量', validators=[DataRequired()])
# submit = SubmitField('保存')