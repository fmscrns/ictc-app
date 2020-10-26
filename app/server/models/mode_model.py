from ... import db

class ModeModel(db.Model):
    __tablename__ = "mode"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)

    name = db.Column(db.String(100))
    registered_on = db.Column(db.DateTime, nullable=False)

    request_approach_rel = db.relationship("RequestModel", backref="mode", lazy="joined")

    def __repr__(self):
        return "<Mode '{}'>".format(self.public_id)