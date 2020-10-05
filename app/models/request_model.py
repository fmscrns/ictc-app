from .. import db

class RequestModel(db.Model):
    __tablename__ = "request"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)

    no = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    detail = db.Column(db.String(100))
    result = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    photo_fn = db.Column(db.String(100))

    office_client_id = db.Column(db.String, db.ForeignKey("office.public_id"))
    mode_approach_id = db.Column(db.String, db.ForeignKey("mode.public_id"))
    nature_type_id = db.Column(db.String, db.ForeignKey("nature.public_id"))
    
    repair_task_rel = db.relationship("RepairModel", backref="request", lazy="joined")

    def __repr__(self):
        return "<Request '{}'>".format(self.public_id)