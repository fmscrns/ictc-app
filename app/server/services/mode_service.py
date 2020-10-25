import uuid
from ... import db
from ..models import ModeModel

class ModeService:
    @staticmethod
    def get_all():
        try:
            modes = [
                dict(
                    id = mode[0],
                    name = mode[1],
                ) for mode in db.session.query(
                    ModeModel.public_id,
                    ModeModel.name
                ).all()
            ]

            if modes:
                return modes

            return 404

        except:
            return 500

    @staticmethod
    def verify(data):
        try:
            verify_name = ModeModel.query.filter_by(name=data.get("name")).first()

            if not verify_name:
                return data

            return 400

        except:
            return 500

    @staticmethod
    def post(data):
        try:
            pid = str(uuid.uuid4())

            new_mode = ModeModel(
                public_id = pid,
                name = data.get("name")
            )

            db.session.add(new_mode)

            db.session.commit()

            return pid

        except:
            return 500