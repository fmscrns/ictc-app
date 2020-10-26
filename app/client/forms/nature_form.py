from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class CreateNatureForm(FlaskForm):
    crtnt_name_input = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])

    crtnt_submit_input = SubmitField("Create")

class EditNatureForm(FlaskForm):
    edtnt_id_input = StringField("Identifier", validators=[DataRequired()])
    edtnt_name_input = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])

    edtnt_submit_input = SubmitField("Edit")

class DeleteNatureForm(FlaskForm):
    deltnt_id_input = StringField("Identifier", validators=[DataRequired()])
    deltnt_name_input = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])

    deltnt_submit_input = SubmitField("Delete")