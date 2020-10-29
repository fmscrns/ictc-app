import uuid, datetime
from sqlalchemy.orm import exc
from ... import db
from ..models import OfficeModel

class OfficeService:
    @staticmethod
    def get_all(pagination_no):
        try:
            offices = [
                dict(
                    id = office[0],
                    name = office[1],
                ) for office in db.session.query(
                    OfficeModel.public_id,
                    OfficeModel.name
                ).order_by(
                    OfficeModel.registered_on.asc()
                ).paginate(
                    page=pagination_no,
                    per_page=3
                ).items
            ]

            return offices if offices else 404

        except exc.NoResultFound:
            return 404

        else:
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
                name = data.get("name"),
                registered_on = datetime.datetime.utcnow()
            )

            db.session.add(new_office)

            db.session.commit()

            return pid

        except:
            return 500

    @staticmethod
    def patch(data):
        try:
            office = OfficeModel.query.filter_by(public_id=data.get("id")).first()
            office = office if not OfficeModel.query.filter_by(name=data.get("name")).first() else None

            if office:
                office.name = data.get("name")

                db.session.commit()

                return 200

            return 400

        except:
            return 500

    @staticmethod
    def delete(data):
        try:
            office = OfficeModel.query.filter_by(public_id=data.get("id")).first()
            office = office if office.name == data.get("name") else None

            if office:
                db.session.delete(office)

                db.session.commit()

                return 200

            return 400

        except:
            return 500