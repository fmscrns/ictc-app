from ... import db

class TechnicianModel(db.Model):
    __tablename__ = "technician"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)

    name = db.Column(db.String(100))

    repair_fixer_rel = db.relationship("RepairModel", backref="technician", lazy="joined")

    def __repr__(self):
        return "<Technician '{}'>".format(self.public_id)