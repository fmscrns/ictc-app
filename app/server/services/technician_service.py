import uuid, datetime
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
                ).order_by(
                    TechnicianModel.registered_on.asc()
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
                name = data.get("name"),
                registered_on = datetime.datetime.utcnow()
            )

            db.session.add(new_technician)

            db.session.commit()

            return pid

        except:
            return 500

    @staticmethod
    def patch(data):
        try:
            technician = TechnicianModel.query.filter_by(public_id=data.get("id")).first()
            technician = technician if not TechnicianModel.query.filter_by(name=data.get("name")).first() else None

            if technician:
                technician.name = data.get("name")

                db.session.commit()

                return 200

            return 400

        except:
            return 500

    @staticmethod
    def delete(data):
        try:
            technician = TechnicianModel.query.filter_by(public_id=data.get("id")).first()
            technician = technician if technician.name == data.get("name") else None

            if technician:
                db.session.delete(technician)

                db.session.commit()

                return 200

            return 400

        except:
            return 500
