import uuid, datetime
from sqlalchemy.orm import exc
from ... import db
from ..models import NatureModel

class NatureService:
    @staticmethod
    def get_all(pagination_no):
        try:
            natures = [
                dict(
                    id = nature[0],
                    name = nature[1],
                ) for nature in db.session.query(
                    NatureModel.public_id,
                    NatureModel.name
                ).order_by(
                    NatureModel.registered_on.asc()
                ).paginate(
                    page=pagination_no,
                    per_page=3
                ).items
            ]

            return natures if natures else 404

        except exc.NoResultFound:
            return 404

        else:
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
                name = data.get("name"),
                registered_on = datetime.datetime.utcnow()
            )

            db.session.add(new_nature)

            db.session.commit()

            return pid

        except:
            return 500

    @staticmethod
    def patch(data):
        try:
            nature = NatureModel.query.filter_by(public_id=data.get("id")).first()
            nature = nature if not NatureModel.query.filter_by(name=data.get("name")).first() else None

            if nature:
                nature.name = data.get("name")

                db.session.commit()

                return 200

            return 400

        except:
            return 500

    @staticmethod
    def delete(data):
        try:
            nature = NatureModel.query.filter_by(public_id=data.get("id")).first()
            nature = nature if nature.name == data.get("name") else None

            if nature:
                db.session.delete(nature)

                db.session.commit()

                return 200

            return 400

        except:
            return 500