from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, RadioField, FileField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, Optional
from flask_wtf.file import FileAllowed, FileRequired
from app.models import *

class CreateRequestForm(FlaskForm):
    no_input = StringField("Number", validators=[DataRequired()])
    date_input = DateField("Date", format="%Y-%m-%d", validators=[InputRequired()])
    detail_input = TextAreaField("Detail", validators=[Length(max=100)])
    office_input = SelectField("Office", coerce=str, choices=[(office.public_id, office.name) for office in OfficeModel.query.all()], validators=[InputRequired()])
    mode_input = SelectField("Mode", coerce=str, choices=[(mode.public_id, mode.name) for mode in ModeModel.query.all()], validators=[InputRequired()])
    nature_input = SelectField("Nature", coerce=str, choices=[(nature.public_id, nature.name) for nature in NatureModel.query.all()], validators=[InputRequired()])
    technician_input = SelectMultipleField("Technician", coerce=str, choices=[(technician.public_id, technician.name) for technician in TechnicianModel.query.all()], validators=[InputRequired()])
    result_input = RadioField("Result", coerce=int, choices=[(0, "Done"), (1, "Pending"), (2, "Cancelled")])
    rating_input = RadioField("Rating", coerce=int, choices=[(0, "Excellent"), (1, "Very good"), (2, "Good"), (3, "Fair"), (4, "Poor")], validators=[Optional()])
    photo_fn_input = FileField("Photo of actual file", validators=[FileAllowed(["jpg", "jpeg", "png"]), FileRequired()])

    submit_input = SubmitField("Create request")