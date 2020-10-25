import uuid
from ... import db
from ..models import TechnicianModel

class TechnicianService:
    @staticmethod
    def get_all():
        try:
            technicians = [
                dict(
                    id = technician[0],
                    name = technician[1],
                ) for technician in db.session.query(
                    TechnicianModel.public_id,
                    TechnicianModel.name
                ).all()
            ]

            if technicians:
                return technicians

            return 404

        except:
            return 500

    @staticmethod
    def verify(data):
        try:
            verify_name = TechnicianModel.query.filter_by(name=data.get("name")).first()

            if not verify_name:
                return data

            return 400

        except:
            return 500

    @staticmethod
    def post(data):
        try:
            pid = str(uuid.uuid4())

            new_technician = TechnicianModel(
                public_id = pid,
                name = data.get("name")
            )

            db.session.add(new_technician)

            db.session.commit()

            return pid

        except:
            return 500
