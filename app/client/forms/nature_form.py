from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class CreateNatureForm(FlaskForm):
    crtnt_name_input = StringField("Name", validators=[DataRequired(), Length(min=1, max=50)])

    crtnt_submit_input = SubmitField("Create")