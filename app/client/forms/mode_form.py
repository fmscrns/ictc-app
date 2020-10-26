from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class CreateModeForm(FlaskForm):
    crtmd_name_input = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])

    crtmd_submit_input = SubmitField("Create")

class EditModeForm(FlaskForm):
    edtmd_id_input = StringField("Identifier", validators=[DataRequired()])
    edtmd_name_input = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])

    edtmd_submit_input = SubmitField("Edit")

class DeleteModeForm(FlaskForm):
    deltmd_id_input = StringField("Identifier", validators=[DataRequired()])
    deltmd_name_input = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])

    deltmd_submit_input = SubmitField("Delete")