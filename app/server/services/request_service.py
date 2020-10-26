import uuid, datetime
from sqlalchemy import extract
from ... import db
from ..models import *

class RequestService:
    @staticmethod
    def get_all():
        try:
            requests = [
                dict(
                    id = request[0],
                    no = request[1],
                    date = request[2],
                    detail = request[3],
                    result = request[4],
                    rating = request[5],
                    photo_fn = request[6],
                    client = dict(
                        client_id = request[7],
                        client_name = request[8],
                    ),
                    approach = dict(
                        approach_id = request[9],
                        approach_name = request[10]
                    ),
                    type = dict(
                        type_id = request[11],
                        type_name = request[12]
                    ),
                    fixers = [
                        dict(
                            fixer_id = technician[0],
                            fixer_name = technician[1]
                        ) for technician in db.session.query(
                            TechnicianModel.public_id,
                            TechnicianModel.name
                        ).filter(
                            TechnicianModel.public_id == RepairModel.technician_fixer_id,
                            RepairModel.request_task_id == request[0]
                        ).all()
                    ]
                ) for request in db.session.query(
                    RequestModel.public_id,
                    RequestModel.no,
                    RequestModel.date,
                    RequestModel.detail,
                    RequestModel.result,
                    RequestModel.rating,
                    RequestModel.photo_fn,
                    OfficeModel.public_id,
                    OfficeModel.name,
                    ModeModel.public_id,
                    ModeModel.name,
                    NatureModel.public_id,
                    NatureModel.name
                ).filter(
                    RequestModel.office_client_id == OfficeModel.public_id,
                    RequestModel.mode_approach_id == ModeModel.public_id,
                    RequestModel.nature_type_id == NatureModel.public_id
                ).order_by(
                    RequestModel.date.desc(),
                    RequestModel.no.desc()
                ).all()
            ]

            if requests:
                return requests

            return 404

        except:
            return 500

    @staticmethod
    def post(data):
        try:
            verify_no = False
            verify_office = False
            verify_mode = False
            verify_nature = False
            verify_technician = True
            verify_rating = False

            if int(data.get("no").split("-")[0]) == int(data.get("date").split("-")[1]):
                no = RequestModel.query.filter_by(no=data.get("no")).filter(extract("year", RequestModel.date) == data.get("date").split("-")[0]).first()
 
                if not no:
                    verify_no = True

            office = OfficeModel.query.filter_by(public_id=data.get("client")["id"]).first()
            
            if office:
                verify_office = True
            
            mode = ModeModel.query.filter_by(public_id=data.get("approach")["id"]).first() 
            
            if mode:
                verify_mode = True

            nature = NatureModel.query.filter_by(public_id=data.get("type")["id"]).first()

            if nature:
                verify_nature = True

            for fixer in data.get("fixers"):
                technician = TechnicianModel.query.filter_by(public_id=fixer["id"]).first()

                if not technician:
                    verify_technician = False

            for value in [[0, 1, 2, 3, 4], [5], [5]][data.get("result")]:
                if value == data.get("rating"):
                    verify_rating = True

            if verify_no and verify_office and verify_mode and verify_nature and verify_technician and verify_rating:
                req_pid = str(uuid.uuid4())

                new_request = RequestModel(
                    public_id = req_pid,
                    no = data.get("no"),
                    date = data.get("date"),
                    detail = data.get("detail"),
                    result = data.get("result"),
                    rating = data.get("rating"),
                    photo_fn = data.get("photo_fn"),
                    registered_on = datetime.datetime.utcnow(),
                    office_client_id = data.get("client")["id"],
                    mode_approach_id = data.get("approach")["id"],
                    nature_type_id = data.get("type")["id"]
                )

                db.session.add(new_request)

                for fixer in data.get("fixers"):
                    rep_pid = str(uuid.uuid4())

                    new_repair = RepairModel(
                        public_id = rep_pid,
                        registered_on = datetime.datetime.utcnow(),
                        technician_fixer_id = fixer["id"],
                        request_task_id = req_pid
                    )

                    db.session.add(new_repair)

                db.session.commit()

                return req_pid

            return 400

        except:
            return 500

    @staticmethod
    def get_by_year(year):
        try:
            requests = [
                dict(
                    id = request[0],
                    no = request[1],
                    date = request[2],
                    detail = request[3],
                    result = request[4],
                    rating = request[5],
                    photo_fn = request[6],
                    client = dict(
                        client_id = request[7],
                        client_name = request[8],
                    ),
                    approach = dict(
                        approach_id = request[9],
                        approach_name = request[10]
                    ),
                    type = dict(
                        type_id = request[11],
                        type_name = request[12]
                    ),
                    fixers = [
                        dict(
                            fixer_id = technician[0],
                            fixer_name = technician[1]
                        ) for technician in db.session.query(
                            TechnicianModel.public_id,
                            TechnicianModel.name
                        ).filter(
                            TechnicianModel.public_id == RepairModel.technician_fixer_id,
                            RepairModel.request_task_id == request[0]
                        ).all()
                    ]
                ) for request in db.session.query(
                    RequestModel.public_id,
                    RequestModel.no,
                    RequestModel.date,
                    RequestModel.detail,
                    RequestModel.result,
                    RequestModel.rating,
                    RequestModel.photo_fn,
                    OfficeModel.public_id,
                    OfficeModel.name,
                    ModeModel.public_id,
                    ModeModel.name,
                    NatureModel.public_id,
                    NatureModel.name
                ).filter(
                    RequestModel.office_client_id == OfficeModel.public_id,
                    RequestModel.mode_approach_id == ModeModel.public_id,
                    RequestModel.nature_type_id == NatureModel.public_id,
                    extract("year", RequestModel.date) == year
                ).order_by(
                    RequestModel.date.desc(),
                    RequestModel.no.desc()
                ).all()
            ]

            if requests:
                return requests

            return 404

        except:
            return 500

    @staticmethod
    def get_by_year_and_month(year, month):
        try:
            requests = [
                dict(
                    id = request[0],
                    no = request[1],
                    date = request[2],
                    detail = request[3],
                    result = request[4],
                    rating = request[5],
                    photo_fn = request[6],
                    client = dict(
                        client_id = request[7],
                        client_name = request[8],
                    ),
                    approach = dict(
                        approach_id = request[9],
                        approach_name = request[10]
                    ),
                    type = dict(
                        type_id = request[11],
                        type_name = request[12]
                    ),
                    fixers = [
                        dict(
                            fixer_id = technician[0],
                            fixer_name = technician[1]
                        ) for technician in db.session.query(
                            TechnicianModel.public_id,
                            TechnicianModel.name
                        ).filter(
                            TechnicianModel.public_id == RepairModel.technician_fixer_id,
                            RepairModel.request_task_id == request[0]
                        ).all()
                    ]
                ) for request in db.session.query(
                    RequestModel.public_id,
                    RequestModel.no,
                    RequestModel.date,
                    RequestModel.detail,
                    RequestModel.result,
                    RequestModel.rating,
                    RequestModel.photo_fn,
                    OfficeModel.public_id,
                    OfficeModel.name,
                    ModeModel.public_id,
                    ModeModel.name,
                    NatureModel.public_id,
                    NatureModel.name
                ).filter(
                    RequestModel.office_client_id == OfficeModel.public_id,
                    RequestModel.mode_approach_id == ModeModel.public_id,
                    RequestModel.nature_type_id == NatureModel.public_id,
                    extract("year", RequestModel.date) == year,
                    extract("month", RequestModel.date) == month
                ).order_by(
                    RequestModel.date.desc(),
                    RequestModel.no.desc()
                ).all()
            ]

            if requests:
                return requests

            return 404

        except:
            return 500

    @staticmethod
    def get_newest():
        try:
            request = db.session.query(
                RequestModel.public_id,
                RequestModel.no,
                RequestModel.date,
                RequestModel.detail,
                RequestModel.result,
                RequestModel.rating,
                RequestModel.photo_fn,
                OfficeModel.public_id,
                OfficeModel.name,
                ModeModel.public_id,
                ModeModel.name,
                NatureModel.public_id,
                NatureModel.name
            ).filter(
                RequestModel.office_client_id == OfficeModel.public_id
            ).filter(
                RequestModel.mode_approach_id == ModeModel.public_id
            ).filter(
                RequestModel.nature_type_id == NatureModel.public_id
            ).order_by(RequestModel.date.asc()).first()
            
            if request:
                return dict(
                    id = request[0],
                    no = request[1],
                    date = request[2],
                    detail = request[3],
                    result = request[4],
                    rating = request[5],
                    photo_fn = request[6],
                    client = dict(
                        client_id = request[7],
                        client_name = request[8],
                    ),
                    approach = dict(
                        approach_id = request[9],
                        approach_name = request[10]
                    ),
                    type = dict(
                        type_id = request[11],
                        type_name = request[12]
                    ),
                    fixers = [
                        dict(
                            fixer_id = technician[0],
                            fixer_name = technician[1]
                        ) for technician in db.session.query(
                            TechnicianModel.public_id,
                            TechnicianModel.name
                        ).filter(
                            TechnicianModel.public_id == RepairModel.technician_fixer_id,
                            RepairModel.request_task_id == request[0]
                        ).all()
                    ]
                )

            return 404

        except:
            return 500

    @staticmethod
    def get_oldest():
        try:
            request = db.session.query(
                RequestModel.public_id,
                RequestModel.no,
                RequestModel.date,
                RequestModel.detail,
                RequestModel.result,
                RequestModel.rating,
                RequestModel.photo_fn,
                OfficeModel.public_id,
                OfficeModel.name,
                ModeModel.public_id,
                ModeModel.name,
                NatureModel.public_id,
                NatureModel.name
            ).filter(
                RequestModel.office_client_id == OfficeModel.public_id
            ).filter(
                RequestModel.mode_approach_id == ModeModel.public_id
            ).filter(
                RequestModel.nature_type_id == NatureModel.public_id
            ).order_by(RequestModel.date.desc()).first()
            
            if request:
                return dict(
                    id = request[0],
                    no = request[1],
                    date = request[2],
                    detail = request[3],
                    result = request[4],
                    rating = request[5],
                    photo_fn = request[6],
                    client = dict(
                        client_id = request[7],
                        client_name = request[8],
                    ),
                    approach = dict(
                        approach_id = request[9],
                        approach_name = request[10]
                    ),
                    type = dict(
                        type_id = request[11],
                        type_name = request[12]
                    ),
                    fixers = [
                        dict(
                            fixer_id = technician[0],
                            fixer_name = technician[1]
                        ) for technician in db.session.query(
                            TechnicianModel.public_id,
                            TechnicianModel.name
                        ).filter(
                            TechnicianModel.public_id == RepairModel.technician_fixer_id,
                            RepairModel.request_task_id == request[0]
                        ).all()
                    ]
                )
                
            return 404

        except:
            return 500

    @staticmethod
    def get_by_office(office_id):
        try:
            requests = [
                dict(
                    id = request[0],
                    no = request[1],
                    date = request[2],
                    detail = request[3],
                    result = request[4],
                    rating = request[5],
                    photo_fn = request[6],
                    client = dict(
                        client_id = request[7],
                        client_name = request[8],
                    ),
                    approach = dict(
                        approach_id = request[9],
                        approach_name = request[10]
                    ),
                    type = dict(
                        type_id = request[11],
                        type_name = request[12]
                    ),
                    fixers = [
                        dict(
                            fixer_id = technician[0],
                            fixer_name = technician[1]
                        ) for technician in db.session.query(
                            TechnicianModel.public_id,
                            TechnicianModel.name
                        ).filter(
                            TechnicianModel.public_id == RepairModel.technician_fixer_id,
                            RepairModel.request_task_id == request[0]
                        ).all()
                    ]
                ) for request in db.session.query(
                    RequestModel.public_id,
                    RequestModel.no,
                    RequestModel.date,
                    RequestModel.detail,
                    RequestModel.result,
                    RequestModel.rating,
                    RequestModel.photo_fn,
                    OfficeModel.public_id,
                    OfficeModel.name,
                    ModeModel.public_id,
                    ModeModel.name,
                    NatureModel.public_id,
                    NatureModel.name
                ).filter(
                    RequestModel.office_client_id == OfficeModel.public_id,
                    RequestModel.mode_approach_id == ModeModel.public_id,
                    RequestModel.nature_type_id == NatureModel.public_id,
                    RequestModel.office_client_id == office_id
                ).order_by(
                    RequestModel.date.desc(),
                    RequestModel.no.desc()
                ).all()
            ]

            if requests:
                return requests

            return 404

        except:
            return 500

    @staticmethod
    def get_by_mode(mode_id):
        try:
            requests = [
                dict(
                    id = request[0],
                    no = request[1],
                    date = request[2],
                    detail = request[3],
                    result = request[4],
                    rating = request[5],
                    photo_fn = request[6],
                    client = dict(
                        client_id = request[7],
                        client_name = request[8],
                    ),
                    approach = dict(
                        approach_id = request[9],
                        approach_name = request[10]
                    ),
                    type = dict(
                        type_id = request[11],
                        type_name = request[12]
                    ),
                    fixers = [
                        dict(
                            fixer_id = technician[0],
                            fixer_name = technician[1]
                        ) for technician in db.session.query(
                            TechnicianModel.public_id,
                            TechnicianModel.name
                        ).filter(
                            TechnicianModel.public_id == RepairModel.technician_fixer_id,
                            RepairModel.request_task_id == request[0]
                        ).all()
                    ]
                ) for request in db.session.query(
                    RequestModel.public_id,
                    RequestModel.no,
                    RequestModel.date,
                    RequestModel.detail,
                    RequestModel.result,
                    RequestModel.rating,
                    RequestModel.photo_fn,
                    OfficeModel.public_id,
                    OfficeModel.name,
                    ModeModel.public_id,
                    ModeModel.name,
                    NatureModel.public_id,
                    NatureModel.name
                ).filter(
                    RequestModel.office_client_id == OfficeModel.public_id,
                    RequestModel.mode_approach_id == ModeModel.public_id,
                    RequestModel.nature_type_id == NatureModel.public_id,
                    RequestModel.mode_approach_id == mode_id
                ).order_by(
                    RequestModel.date.desc(),
                    RequestModel.no.desc()
                ).all()
            ]

            if requests:
                return requests

            return 404

        except:
            return 500

    @staticmethod
    def get_by_nature(nature_id):
        try:
            requests = [
                dict(
                    id = request[0],
                    no = request[1],
                    date = request[2],
                    detail = request[3],
                    result = request[4],
                    rating = request[5],
                    photo_fn = request[6],
                    client = dict(
                        client_id = request[7],
                        client_name = request[8],
                    ),
                    approach = dict(
                        approach_id = request[9],
                        approach_name = request[10]
                    ),
                    type = dict(
                        type_id = request[11],
                        type_name = request[12]
                    ),
                    fixers = [
                        dict(
                            fixer_id = technician[0],
                            fixer_name = technician[1]
                        ) for technician in db.session.query(
                            TechnicianModel.public_id,
                            TechnicianModel.name
                        ).filter(
                            TechnicianModel.public_id == RepairModel.technician_fixer_id,
                            RepairModel.request_task_id == request[0]
                        ).all()
                    ]
                ) for request in db.session.query(
                    RequestModel.public_id,
                    RequestModel.no,
                    RequestModel.date,
                    RequestModel.detail,
                    RequestModel.result,
                    RequestModel.rating,
                    RequestModel.photo_fn,
                    OfficeModel.public_id,
                    OfficeModel.name,
                    ModeModel.public_id,
                    ModeModel.name,
                    NatureModel.public_id,
                    NatureModel.name
                ).filter(
                    RequestModel.office_client_id == OfficeModel.public_id,
                    RequestModel.mode_approach_id == ModeModel.public_id,
                    RequestModel.nature_type_id == NatureModel.public_id,
                    RequestModel.nature_type_id == nature_id
                ).order_by(
                    RequestModel.date.desc(),
                    RequestModel.no.desc()
                ).all()
            ]

            if requests:
                return requests

            return 404

        except:
            return 500

    @staticmethod
    def get_by_technician(technician_id):
        try:
            requests = [
                dict(
                    id = request[0],
                    no = request[1],
                    date = request[2],
                    detail = request[3],
                    result = request[4],
                    rating = request[5],
                    photo_fn = request[6],
                    client = dict(
                        client_id = request[7],
                        client_name = request[8],
                    ),
                    approach = dict(
                        approach_id = request[9],
                        approach_name = request[10]
                    ),
                    type = dict(
                        type_id = request[11],
                        type_name = request[12]
                    ),
                    fixers = [
                        dict(
                            fixer_id = technician[0],
                            fixer_name = technician[1]
                        ) for technician in db.session.query(
                            TechnicianModel.public_id,
                            TechnicianModel.name
                        ).filter(
                            TechnicianModel.public_id == RepairModel.technician_fixer_id,
                            RepairModel.request_task_id == request[0]
                        ).all()
                    ]
                ) for request in db.session.query(
                    RequestModel.public_id,
                    RequestModel.no,
                    RequestModel.date,
                    RequestModel.detail,
                    RequestModel.result,
                    RequestModel.rating,
                    RequestModel.photo_fn,
                    OfficeModel.public_id,
                    OfficeModel.name,
                    ModeModel.public_id,
                    ModeModel.name,
                    NatureModel.public_id,
                    NatureModel.name
                ).filter(
                    RequestModel.office_client_id == OfficeModel.public_id,
                    RequestModel.mode_approach_id == ModeModel.public_id,
                    RequestModel.nature_type_id == NatureModel.public_id,
                    RequestModel.public_id == RepairModel.request_task_id,
                    RepairModel.technician_fixer_id == technician_id
                ).order_by(
                    RequestModel.date.desc(),
                    RequestModel.no.desc()
                ).all()
            ]

            if requests:
                return requests

            return 404

        except:
            return 500

    @staticmethod
    def get_by_result(result):
        try:
            requests = [
                dict(
                    id = request[0],
                    no = request[1],
                    date = request[2],
                    detail = request[3],
                    result = request[4],
                    rating = request[5],
                    photo_fn = request[6],
                    client = dict(
                        client_id = request[7],
                        client_name = request[8],
                    ),
                    approach = dict(
                        approach_id = request[9],
                        approach_name = request[10]
                    ),
                    type = dict(
                        type_id = request[11],
                        type_name = request[12]
                    ),
                    fixers = [
                        dict(
                            fixer_id = technician[0],
                            fixer_name = technician[1]
                        ) for technician in db.session.query(
                            TechnicianModel.public_id,
                            TechnicianModel.name
                        ).filter(
                            TechnicianModel.public_id == RepairModel.technician_fixer_id,
                            RepairModel.request_task_id == request[0]
                        ).all()
                    ]
                ) for request in db.session.query(
                    RequestModel.public_id,
                    RequestModel.no,
                    RequestModel.date,
                    RequestModel.detail,
                    RequestModel.result,
                    RequestModel.rating,
                    RequestModel.photo_fn,
                    OfficeModel.public_id,
                    OfficeModel.name,
                    ModeModel.public_id,
                    ModeModel.name,
                    NatureModel.public_id,
                    NatureModel.name
                ).filter(
                    RequestModel.office_client_id == OfficeModel.public_id,
                    RequestModel.mode_approach_id == ModeModel.public_id,
                    RequestModel.nature_type_id == NatureModel.public_id,
                    RequestModel.result == result
                ).order_by(
                    RequestModel.date.desc(),
                    RequestModel.no.desc()
                ).all()
            ]

            if requests:
                return requests

            return 404

        except:
            return 500

    @staticmethod
    def get_by_rating(rating):
        try:
            requests = [
                dict(
                    id = request[0],
                    no = request[1],
                    date = request[2],
                    detail = request[3],
                    result = request[4],
                    rating = request[5],
                    photo_fn = request[6],
                    client = dict(
                        client_id = request[7],
                        client_name = request[8],
                    ),
                    approach = dict(
                        approach_id = request[9],
                        approach_name = request[10]
                    ),
                    type = dict(
                        type_id = request[11],
                        type_name = request[12]
                    ),
                    fixers = [
                        dict(
                            fixer_id = technician[0],
                            fixer_name = technician[1]
                        ) for technician in db.session.query(
                            TechnicianModel.public_id,
                            TechnicianModel.name
                        ).filter(
                            TechnicianModel.public_id == RepairModel.technician_fixer_id,
                            RepairModel.request_task_id == request[0]
                        ).all()
                    ]
                ) for request in db.session.query(
                    RequestModel.public_id,
                    RequestModel.no,
                    RequestModel.date,
                    RequestModel.detail,
                    RequestModel.result,
                    RequestModel.rating,
                    RequestModel.photo_fn,
                    OfficeModel.public_id,
                    OfficeModel.name,
                    ModeModel.public_id,
                    ModeModel.name,
                    NatureModel.public_id,
                    NatureModel.name
                ).filter(
                    RequestModel.office_client_id == OfficeModel.public_id,
                    RequestModel.mode_approach_id == ModeModel.public_id,
                    RequestModel.nature_type_id == NatureModel.public_id,
                    RequestModel.rating == rating
                ).order_by(
                    RequestModel.date.desc(),
                    RequestModel.no.desc()
                ).all()
            ]

            if requests:
                return requests

            return 404

        except:
            return 500

    @staticmethod
    def get_by_detail(detail):
        try:
            requests = [
                dict(
                    id = request[0],
                    no = request[1],
                    date = request[2],
                    detail = request[3],
                    result = request[4],
                    rating = request[5],
                    photo_fn = request[6],
                    client = dict(
                        client_id = request[7],
                        client_name = request[8],
                    ),
                    approach = dict(
                        approach_id = request[9],
                        approach_name = request[10]
                    ),
                    type = dict(
                        type_id = request[11],
                        type_name = request[12]
                    ),
                    fixers = [
                        dict(
                            fixer_id = technician[0],
                            fixer_name = technician[1]
                        ) for technician in db.session.query(
                            TechnicianModel.public_id,
                            TechnicianModel.name
                        ).filter(
                            TechnicianModel.public_id == RepairModel.technician_fixer_id,
                            RepairModel.request_task_id == request[0]
                        ).all()
                    ]
                ) for request in db.session.query(
                    RequestModel.public_id,
                    RequestModel.no,
                    RequestModel.date,
                    RequestModel.detail,
                    RequestModel.result,
                    RequestModel.rating,
                    RequestModel.photo_fn,
                    OfficeModel.public_id,
                    OfficeModel.name,
                    ModeModel.public_id,
                    ModeModel.name,
                    NatureModel.public_id,
                    NatureModel.name
                ).filter(
                    RequestModel.office_client_id == OfficeModel.public_id,
                    RequestModel.mode_approach_id == ModeModel.public_id,
                    RequestModel.nature_type_id == NatureModel.public_id,
                    RequestModel.detail.ilike("%{}%".format(detail))
                ).order_by(
                    RequestModel.date.desc(),
                    RequestModel.no.desc()
                ).all()
            ]

            if requests:
                return requests

            return 404

        except:
            return 500

    @staticmethod
    def get_by_no_and_year(no, year):
        try:
            request = db.session.query(
                RequestModel.public_id,
                RequestModel.no,
                RequestModel.date,
                RequestModel.detail,
                RequestModel.result,
                RequestModel.rating,
                RequestModel.photo_fn,
                OfficeModel.public_id,
                OfficeModel.name,
                ModeModel.public_id,
                ModeModel.name,
                NatureModel.public_id,
                NatureModel.name
            ).filter(
                RequestModel.office_client_id == OfficeModel.public_id,
                RequestModel.mode_approach_id == ModeModel.public_id,
                RequestModel.nature_type_id == NatureModel.public_id,
                RequestModel.no == no,
                extract("year", RequestModel.date) == year
            ).first()
            
            if request:
                return dict(
                    id = request[0],
                    no = request[1],
                    date = request[2],
                    detail = request[3],
                    result = request[4],
                    rating = request[5],
                    photo_fn = request[6],
                    client = dict(
                        client_id = request[7],
                        client_name = request[8],
                    ),
                    approach = dict(
                        approach_id = request[9],
                        approach_name = request[10]
                    ),
                    type = dict(
                        type_id = request[11],
                        type_name = request[12]
                    ),
                    fixers = [
                        dict(
                            fixer_id = technician[0],
                            fixer_name = technician[1]
                        ) for technician in db.session.query(
                            TechnicianModel.public_id,
                            TechnicianModel.name
                        ).filter(
                            TechnicianModel.public_id == RepairModel.technician_fixer_id,
                            RepairModel.request_task_id == request[0]
                        ).all()
                    ]
                )

            return 404

        except:
            return 500