from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class CreateTechnicianForm(FlaskForm):
    crttc_name_input = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])

    crttc_submit_input = SubmitField("Create")