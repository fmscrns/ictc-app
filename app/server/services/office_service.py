import uuid
from ... import db
from ..models import OfficeModel

class OfficeService:
    @staticmethod
    def get_all():
        try:
            offices = [
                dict(
                    id = office[0],
                    name = office[1],
                ) for office in db.session.query(
                    OfficeModel.public_id,
                    OfficeModel.name
                ).all()
            ]

            if offices:
                return offices

            return 404

        except:
            return 500

    @staticmethod
    def verify(data):
        try:
            verify_name = OfficeModel.query.filter_by(name=data.get("name")).first()

            if not verify_name:
                return data

            return 400

        except:
            return 500

    @staticmethod
    def post(data):
        try:
            pid = str(uuid.uuid4())

            new_office = OfficeModel(
                public_id = pid,
                name = data.get("name")
            )

            db.session.add(new_office)

            db.session.commit()

            return pid

        except:
            return 500