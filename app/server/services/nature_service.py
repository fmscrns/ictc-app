import uuid, datetime
from sqlalchemy import func, asc, desc
from sqlalchemy.orm import exc
from ... import db
from ..models import RequestModel, NatureModel, OfficeModel

class NatureService:
    # @staticmethod
    # def get_all(pagination_no, order_command):
    #     try:
    #         order_config = dict(
    #             NAME_ASC = NatureModel.name.asc(), 
    #             NAME_DESC = NatureModel.name.desc(),
    #             TOTREQ_ASC = asc("total_requests"),
    #             TOTREQ_DESC = desc("total_requests"),
    #             REGON_ASC = NatureModel.registered_on.asc(),
    #             REGON_DESC = NatureModel.registered_on.desc()
    #         )

    #         natures = [
    #             dict(
    #                 id = nature[0],
    #                 name = nature[1],
    #                 total_requests = nature[2]
    #             ) for nature in db.session.query(
    #                 NatureModel.public_id,
    #                 NatureModel.name,
    #                 func.count(RequestModel.nature_type_id).label("total_requests")
    #             ).join(
    #                 RequestModel
    #             ).group_by(
    #                 NatureModel
    #             ).order_by(
    #                 *[order_config[order_command]]
    #             ).paginate(
    #                 page=pagination_no,
    #                 per_page=3
    #             ).items
    #         ]

    #         return natures if natures else 404

    #     except exc.NoResultFound:
    #         return 404

    #     else:
    #         return 500

    @staticmethod
    def get_all(pagination_no, order_command):
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
            new_id = str(uuid.uuid4())

            new_nature = NatureModel(
                public_id = new_id,
                name = data.get("name"),
                registered_on = datetime.datetime.utcnow()
            )

            db.session.add(new_nature)

            db.session.commit()

            return new_id

        except:
            return 500

    @staticmethod
    def get_by_office(office_id, pagination_no, order_command):
        try:
            order_config = dict(
                NAME_ASC = NatureModel.name.asc(), 
                NAME_DESC = NatureModel.name.desc(),
                TOTREQ_ASC = asc("total_requests"),
                TOTREQ_DESC = desc("total_requests"),
                REGON_ASC = NatureModel.registered_on.asc(),
                REGON_DESC = NatureModel.registered_on.desc()
            )

            natures = [
                dict(
                    id = nature[0],
                    name = nature[1],
                    total_requests = nature[2]
                ) for nature in db.session.query(
                    NatureModel.public_id,
                    NatureModel.name,
                    func.count(RequestModel.nature_type_id).label("total_requests")
                ).join(
                    RequestModel
                ).group_by(
                    NatureModel
                ).filter(
                    RequestModel.office_client_id == office_id
                ).order_by(
                    *[order_config[order_command]]
                ).paginate(
                    page=pagination_no,
                    per_page=3
                ).items
            ]

            return natures if natures else 404

        except exc.NoResultFound:
            return 404

        except KeyError:
            return 400

        else:
            return 500

    @staticmethod
    def patch(id, data):
        try:
            nature = NatureModel.query.filter_by(public_id=id).first()
            nature = nature if not NatureModel.query.filter_by(name=data.get("name")).first() else None

            if nature:
                nature.name = data.get("name")

                db.session.commit()

                return 200

            return 400

        except:
            return 500

    @staticmethod
    def delete(id, data):
        try:
            nature = NatureModel.query.filter_by(public_id=id).first()
            nature = nature if nature.name == data.get("name") else None

            if nature:
                db.session.delete(nature)

                db.session.commit()

                return 200

            return 400

        except:
            return 500