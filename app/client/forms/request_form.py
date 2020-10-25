from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, RadioField, FileField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired, Length, Optional
from flask_wtf.file import FileAllowed, FileRequired
from ..services.office_service import OfficeService
from ..services.mode_service import ModeService
from ..services.nature_service import NatureService
from ..services.technician_service import TechnicianService

class CreateRequestForm(FlaskForm):
    crtrq_no_input = StringField("Number", validators=[DataRequired()])
    crtrq_date_input = DateField("Date", format="%Y-%m-%d", validators=[InputRequired()])
    crtrq_detail_input = TextAreaField("Detail", validators=[Length(max=100)])
    crtrq_office_input = SelectField("Office", coerce=str, validators=[InputRequired()])
    crtrq_mode_input = SelectField("Mode", coerce=str, validators=[InputRequired()])
    crtrq_nature_input = SelectField("Nature", coerce=str, validators=[InputRequired()])
    crtrq_technician_input = SelectMultipleField("Technician", coerce=str, validators=[InputRequired()])
    crtrq_result_input = RadioField("Result", coerce=int, choices=[(0, "Done"), (1, "Pending"), (2, "Cancelled")])
    crtrq_rating_input = RadioField("Rating", coerce=int, choices=[(0, "Excellent"), (1, "Very good"), (2, "Good"), (3, "Fair"), (4, "Poor"), (5, "None")], validators=[Optional()])
    crtrq_photo_fn_input = FileField("Photo of actual request", validators=[FileAllowed(["jpg", "jpeg", "png"]), FileRequired()])

    crtrq_submit_input = SubmitField("Create")

    def ready_form(self):
        self.crtrq_office_input.choices = [(office["id"], office["name"]) for office in OfficeService.get_all()["offices"]] if not isinstance(OfficeService.get_all(), int) else []
        self.crtrq_mode_input.choices = [(mode["id"], mode["name"]) for mode in ModeService.get_all()["modes"]] if not isinstance(ModeService.get_all(), int) else []
        self.crtrq_nature_input.choices = [(nature["id"], nature["name"]) for nature in NatureService.get_all()["natures"]] if not isinstance(NatureService.get_all(), int) else []
        self.crtrq_technician_input.choices = [(technician["id"], technician["name"]) for technician in TechnicianService.get_all()["technicians"]] if not isinstance(TechnicianService.get_all(), int) else []

        return self


