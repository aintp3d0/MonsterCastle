from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired


class MC_User_Form(FlaskForm):
  image = FileField(validators=[FileRequired()])
