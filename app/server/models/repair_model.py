from ... import db

class RepairModel(db.Model):
    __tablename__ = "repair"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)

    technician_fixer_id = db.Column(db.String, db.ForeignKey("technician.public_id"))
    request_task_id = db.Column(db.String, db.ForeignKey("request.public_id"))

    def __repr__(self):
        return "<Repair '{}' '{}'>".format(self.technician_fixer_id, self.request_task_id)