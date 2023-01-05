
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, Length

workout_levels=["level_1", "level_2", "level_3", "level_4", "level_5", "level_6"]

class UserRegisterForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    first_name = StringField('First Name', validators =[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    image_url = StringField('(Optional) Image URL')

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8)])

class UserEditForm(FlaskForm):
    """Form to edit user"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class BMIForm(FlaskForm):
    """Form to check BMI"""
    age = IntegerField('Enter your Age', validators=[DataRequired()])
    weight = IntegerField('Enter your Weight in kg', validators=[DataRequired()])
    height = FloatField('Enter your Height in cm', validators=[DataRequired()])

class CaloriesRequirement(FlaskForm):
    """Form to calculate calories requirements"""
    age = IntegerField('Enter your Age', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    height = FloatField('Enter your Height in cm', validators=[DataRequired()])
    weight = IntegerField('Enter your Weight in kg', validators=[DataRequired()])
    activitylevel = SelectField("Activity Level", choices=[(level, level) for level in workout_levels])
   

tags = ["main course", "side dish", "dessert", "appetizer", "salad", "bread", "breakfast", "soup", "beverage", "sauce", "marinade", "fingerfood", "snack", "drink"]  
class SearchFoodForm(FlaskForm):
    """Form to search the food for diet plan"""
    tag = SelectField('Select one type of meal to get the recipe', 
                      choices=[(type, type ) for type in tags])

class PostForm(FlaskForm):
    """Form to add post"""
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    image_url = StringField('(Optional) Image URL')
    


    
    
