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