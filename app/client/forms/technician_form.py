from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class CreateTechnicianForm(FlaskForm):
    crttc_name_input = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])

    crttc_submit_input = SubmitField("Create")

class EditTechnicianForm(FlaskForm):
    edttc_id_input = StringField("Identifier", validators=[DataRequired()])
    edttc_name_input = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])

    edttc_submit_input = SubmitField("Edit")

class DeleteTechnicianForm(FlaskForm):
    delttc_id_input = StringField("Identifier", validators=[DataRequired()])
    delttc_name_input = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])

    delttc_submit_input = SubmitField("Delete")