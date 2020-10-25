import uuid
from ... import db
from ..models import NatureModel

class NatureService:
    @staticmethod
    def get_all():
        try:
            natures = [
                dict(
                    id = nature[0],
                    name = nature[1],
                ) for nature in db.session.query(
                    NatureModel.public_id,
                    NatureModel.name
                ).all()
            ]

            if natures:
                return natures

            return 404

        except:
            return 500

    @staticmethod
    def verify(data):
        try:
            verify_name = NatureModel.query.filter_by(name=data.get("name")).first()

            if not verify_name:
                return data

            return 400

        except:
            return 500

    @staticmethod
    def post(data):
        try:
            pid = str(uuid.uuid4())

            new_nature = NatureModel(
                public_id = pid,
                name = data.get("name")
            )

            db.session.add(new_nature)

            db.session.commit()

            return pid

        except:
            return 500