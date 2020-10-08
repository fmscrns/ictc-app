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