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