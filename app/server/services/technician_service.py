import uuid, datetime
from sqlalchemy import func, asc, desc
from sqlalchemy.orm import exc
from ... import db
from ..models import TechnicianModel, RepairModel

class TechnicianService:
    @staticmethod
    def get_all(pagination_no):
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
                ).paginate(
                    page=pagination_no,
                    per_page=3
                ).items
            ]

            return technicians if technicians else 404

        except exc.NoResultFound:
            return 404

        else:
            return 500

    @staticmethod
    def get_all_w_totreq(pagination_no, order_command):
        try:
            order_config = dict(
                NAME_ASC = TechnicianModel.name.asc(), 
                NAME_DESC = TechnicianModel.name.desc(), 
                TOTREQ_ASC = asc("total_requests"),
                TOTREQ_DESC = desc("total_requests"),
                REGON_ASC = TechnicianModel.registered_on.asc(),
                REGON_DESC = TechnicianModel.registered_on.desc()
            )

            technicians = [
                dict(
                    id = technician[0],
                    name = technician[1],
                    total_requests = technician[2]
                ) for technician in db.session.query(
                    TechnicianModel.public_id,
                    TechnicianModel.name,
                    func.count(RepairModel.technician_fixer_id).label("total_requests")
                ).join(
                    RepairModel
                ).group_by(
                    TechnicianModel
                ).order_by(
                    *[order_config[order_command]]
                ).paginate(
                    page=pagination_no,
                    per_page=3
                ).items
            ]

            return technicians if technicians else 404

        except exc.NoResultFound:
            return 404

        except KeyError:
            return 400

        else:
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
            new_id = str(uuid.uuid4())

            new_technician = TechnicianModel(
                public_id = new_id,
                name = data.get("name"),
                registered_on = datetime.datetime.utcnow()
            )

            db.session.add(new_technician)

            db.session.commit()

            return new_id

        except:
            return 500

    @staticmethod
    def patch(id, data):
        try:
            technician = TechnicianModel.query.filter_by(public_id=id).first()
            technician = technician if not TechnicianModel.query.filter_by(name=data.get("name")).first() else None

            if technician:
                technician.name = data.get("name")

                db.session.commit()

                return 200

            return 400

        except:
            return 500

    @staticmethod
    def delete(id, data):
        try:
            technician = TechnicianModel.query.filter_by(public_id=id).first()
            technician = technician if technician.name == data.get("name") else None

            if technician:
                db.session.delete(technician)

                db.session.commit()

                return 200

            return 400

        except:
            return 500
