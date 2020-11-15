import uuid, datetime
from sqlalchemy import func, asc, desc
from sqlalchemy.orm import exc
from ... import db
from ..models import RequestModel, OfficeModel

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
    def get_all_w_totreq(pagination_no, order_command):
        try:
            order_config = dict(
                NAME_ASC = OfficeModel.name.asc(), 
                NAME_DESC = OfficeModel.name.desc(), 
                TOTREQ_ASC = asc("total_requests"),
                TOTREQ_DESC = desc("total_requests"),
                REGON_ASC = OfficeModel.registered_on.asc(),
                REGON_DESC = OfficeModel.registered_on.desc()
            )

            offices = [
                dict(
                    id = office[0],
                    name = office[1],
                    total_requests = office[2]
                ) for office in db.session.query(
                    OfficeModel.public_id,
                    OfficeModel.name,
                    func.count(RequestModel.office_client_id).label("total_requests")
                ).join(
                    RequestModel
                ).group_by(
                    OfficeModel
                ).order_by(
                    *[order_config[order_command]]
                ).paginate(
                    page=pagination_no,
                    per_page=3
                ).items
            ]

            return offices if offices else 404

        except exc.NoResultFound:
            return 404

        except KeyError:
            return 400

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
            new_id = str(uuid.uuid4())

            new_office = OfficeModel(
                public_id = new_id,
                name = data.get("name"),
                registered_on = datetime.datetime.utcnow()
            )

            db.session.add(new_office)

            db.session.commit()

            return new_id

        except:
            return 500

    @staticmethod
    def patch(id, data):
        try:
            office = OfficeModel.query.filter_by(public_id=id).first()
            office = office if not OfficeModel.query.filter_by(name=data.get("name")).first() else None

            if office:
                office.name = data.get("name")

                db.session.commit()

                return 200

            return 400

        except:
            return 500

    @staticmethod
    def delete(id, data):
        try:
            office = OfficeModel.query.filter_by(public_id=id).first()
            office = office if office.name == data.get("name") else None

            if office:
                db.session.delete(office)

                db.session.commit()

                return 200

            return 400

        except:
            return 500