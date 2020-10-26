from ... import db

class NatureModel(db.Model):
    __tablename__ = "nature"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)

    name = db.Column(db.String(100))
    registered_on = db.Column(db.DateTime, nullable=False)

    request_type_rel = db.relationship("RequestModel", backref="nature", lazy="joined")

    def __repr__(self):
        return "<Nature '{}'>".format(self.public_id)