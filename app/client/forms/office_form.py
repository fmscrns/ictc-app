from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class CreateOfficeForm(FlaskForm):
    crtof_name_input = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])

    crtof_submit_input = SubmitField("Create")

class EditOfficeForm(FlaskForm):
    edtof_id_input = StringField("Identifier", validators=[DataRequired()])
    edtof_name_input = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])

    edtof_submit_input = SubmitField("Edit")

class DeleteOfficeForm(FlaskForm):
    deltof_id_input = StringField("Identifier", validators=[DataRequired()])
    deltof_name_input = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])

    deltof_submit_input = SubmitField("Delete")