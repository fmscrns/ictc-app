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
                ).all()
            ]

            if technicians:
                return technicians

            return 404

        except:
            return 500