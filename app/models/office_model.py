from .. import db

class OfficeModel(db.Model):
    __tablename__ = "office"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)

    name = db.Column(db.String(100))

    request_client_rel = db.relationship("RequestModel", backref="office", lazy="joined")

    def __repr__(self):
        return "<Office '{}'>".format(self.public_id)