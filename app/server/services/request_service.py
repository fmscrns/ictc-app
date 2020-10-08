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
                    office = dict(
                        office_id = request[7],
                        office_name = request[8],
                    ),
                    mode = dict(
                        mode_id = request[9],
                        mode_name = request[10]
                    ),
                    nature = dict(
                        nature_id = request[11],
                        nature_name = request[12]
                    ),
                    technicians = [
                        dict(
                            technician_id = technician[0],
                            technician_name = technician[1]
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
                    RequestModel.office_client_id == OfficeModel.public_id
                ).filter(
                    RequestModel.mode_approach_id == ModeModel.public_id
                ).filter(
                    RequestModel.nature_type_id == NatureModel.public_id
                ).order_by(RequestModel.date.desc()).all()
            ]

            if requests:
                return requests

            return 404

        except:
            return 500

    @staticmethod
    def post(data):
        try:
            req_pid = str(uuid.uuid4())

            new_request = RequestModel(
                public_id = req_pid,
                no = data.get("no_input"),
                date = data.get("date_input"),
                detail = data.get("detail_input"),
                result = data.get("result_input"),
                rating = data.get("rating_input"),
                photo_fn = data.get("photo_fn_input"),
                office_client_id = data.get("office_input"),
                mode_approach_id = data.get("mode_input"),
                nature_type_id = data.get("nature_input")
            )

            db.session.add(new_request)

            for technician_id in data.get("technician_input"):
                rep_pid = str(uuid.uuid4())

                new_repair = RepairModel(
                    public_id = rep_pid,
                    technician_fixer_id = technician_id,
                    request_task_id = req_pid
                )

                db.session.add(new_repair)

            db.session.commit()

            return req_pid

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
                    office = dict(
                        office_id = request[7],
                        office_name = request[8],
                    ),
                    mode = dict(
                        mode_id = request[9],
                        mode_name = request[10]
                    ),
                    nature = dict(
                        nature_id = request[11],
                        nature_name = request[12]
                    ),
                    technicians = [
                        dict(
                            technician_id = technician[0],
                            technician_name = technician[1]
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
                    RequestModel.office_client_id == OfficeModel.public_id
                ).filter(
                    RequestModel.mode_approach_id == ModeModel.public_id
                ).filter(
                    RequestModel.nature_type_id == NatureModel.public_id
                ).filter(
                    extract("year", RequestModel.date) == year
                ).order_by(RequestModel.date.desc()).all()
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
                    office = dict(
                        office_id = request[7],
                        office_name = request[8],
                    ),
                    mode = dict(
                        mode_id = request[9],
                        mode_name = request[10]
                    ),
                    nature = dict(
                        nature_id = request[11],
                        nature_name = request[12]
                    ),
                    technicians = [
                        dict(
                            technician_id = technician[0],
                            technician_name = technician[1]
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
                    RequestModel.office_client_id == OfficeModel.public_id
                ).filter(
                    RequestModel.mode_approach_id == ModeModel.public_id
                ).filter(
                    RequestModel.nature_type_id == NatureModel.public_id
                ).filter(
                    extract("year", RequestModel.date) == year
                ).filter(
                    extract("month", RequestModel.date) == month
                ).order_by(RequestModel.date.desc()).all()
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
            
            return dict(
                id = request[0],
                no = request[1],
                date = request[2],
                detail = request[3],
                result = request[4],
                rating = request[5],
                photo_fn = request[6],
                office = dict(
                    office_id = request[7],
                    office_name = request[8],
                ),
                mode = dict(
                    mode_id = request[9],
                    mode_name = request[10]
                ),
                nature = dict(
                    nature_id = request[11],
                    nature_name = request[12]
                ),
                technicians = [
                    dict(
                        technician_id = technician[0],
                        technician_name = technician[1]
                    ) for technician in db.session.query(
                        TechnicianModel.public_id,
                        TechnicianModel.name
                    ).filter(
                        TechnicianModel.public_id == RepairModel.technician_fixer_id,
                        RepairModel.request_task_id == request[0]
                    ).all()
                ]
            )

            if request:
                return request

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
            
            return dict(
                id = request[0],
                no = request[1],
                date = request[2],
                detail = request[3],
                result = request[4],
                rating = request[5],
                photo_fn = request[6],
                office = dict(
                    office_id = request[7],
                    office_name = request[8],
                ),
                mode = dict(
                    mode_id = request[9],
                    mode_name = request[10]
                ),
                nature = dict(
                    nature_id = request[11],
                    nature_name = request[12]
                ),
                technicians = [
                    dict(
                        technician_id = technician[0],
                        technician_name = technician[1]
                    ) for technician in db.session.query(
                        TechnicianModel.public_id,
                        TechnicianModel.name
                    ).filter(
                        TechnicianModel.public_id == RepairModel.technician_fixer_id,
                        RepairModel.request_task_id == request[0]
                    ).all()
                ]
            )

            if request:
                return request

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
                    office = dict(
                        office_id = request[7],
                        office_name = request[8],
                    ),
                    mode = dict(
                        mode_id = request[9],
                        mode_name = request[10]
                    ),
                    nature = dict(
                        nature_id = request[11],
                        nature_name = request[12]
                    ),
                    technicians = [
                        dict(
                            technician_id = technician[0],
                            technician_name = technician[1]
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
                    RequestModel.office_client_id == OfficeModel.public_id
                ).filter(
                    RequestModel.mode_approach_id == ModeModel.public_id
                ).filter(
                    RequestModel.nature_type_id == NatureModel.public_id
                ).filter(
                    RequestModel.office_client_id == office_id
                ).order_by(RequestModel.date.desc()).all()
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
                    office = dict(
                        office_id = request[7],
                        office_name = request[8],
                    ),
                    mode = dict(
                        mode_id = request[9],
                        mode_name = request[10]
                    ),
                    nature = dict(
                        nature_id = request[11],
                        nature_name = request[12]
                    ),
                    technicians = [
                        dict(
                            technician_id = technician[0],
                            technician_name = technician[1]
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
                    RequestModel.office_client_id == OfficeModel.public_id
                ).filter(
                    RequestModel.mode_approach_id == ModeModel.public_id
                ).filter(
                    RequestModel.nature_type_id == NatureModel.public_id
                ).filter(
                    RequestModel.mode_approach_id == mode_id
                ).order_by(RequestModel.date.desc()).all()
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
                    office = dict(
                        office_id = request[7],
                        office_name = request[8],
                    ),
                    mode = dict(
                        mode_id = request[9],
                        mode_name = request[10]
                    ),
                    nature = dict(
                        nature_id = request[11],
                        nature_name = request[12]
                    ),
                    technicians = [
                        dict(
                            technician_id = technician[0],
                            technician_name = technician[1]
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
                    RequestModel.office_client_id == OfficeModel.public_id
                ).filter(
                    RequestModel.mode_approach_id == ModeModel.public_id
                ).filter(
                    RequestModel.nature_type_id == NatureModel.public_id
                ).filter(
                    RequestModel.nature_type_id == nature_id
                ).order_by(RequestModel.date.desc()).all()
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
                    office = dict(
                        office_id = request[7],
                        office_name = request[8],
                    ),
                    mode = dict(
                        mode_id = request[9],
                        mode_name = request[10]
                    ),
                    nature = dict(
                        nature_id = request[11],
                        nature_name = request[12]
                    ),
                    technicians = [
                        dict(
                            technician_id = technician[0],
                            technician_name = technician[1]
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
                    RequestModel.office_client_id == OfficeModel.public_id
                ).filter(
                    RequestModel.mode_approach_id == ModeModel.public_id
                ).filter(
                    RequestModel.nature_type_id == NatureModel.public_id
                ).filter(
                    RequestModel.public_id == RepairModel.request_task_id
                ).filter(
                    RepairModel.technician_fixer_id == technician_id
                ).order_by(RequestModel.date.desc()).all()
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
                    office = dict(
                        office_id = request[7],
                        office_name = request[8],
                    ),
                    mode = dict(
                        mode_id = request[9],
                        mode_name = request[10]
                    ),
                    nature = dict(
                        nature_id = request[11],
                        nature_name = request[12]
                    ),
                    technicians = [
                        dict(
                            technician_id = technician[0],
                            technician_name = technician[1]
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
                    RequestModel.office_client_id == OfficeModel.public_id
                ).filter(
                    RequestModel.mode_approach_id == ModeModel.public_id
                ).filter(
                    RequestModel.nature_type_id == NatureModel.public_id
                ).filter(
                    RequestModel.result == result
                ).order_by(RequestModel.date.desc()).all()
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
                    office = dict(
                        office_id = request[7],
                        office_name = request[8],
                    ),
                    mode = dict(
                        mode_id = request[9],
                        mode_name = request[10]
                    ),
                    nature = dict(
                        nature_id = request[11],
                        nature_name = request[12]
                    ),
                    technicians = [
                        dict(
                            technician_id = technician[0],
                            technician_name = technician[1]
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
                    RequestModel.office_client_id == OfficeModel.public_id
                ).filter(
                    RequestModel.mode_approach_id == ModeModel.public_id
                ).filter(
                    RequestModel.nature_type_id == NatureModel.public_id
                ).filter(
                    RequestModel.rating == rating
                ).order_by(RequestModel.date.desc()).all()
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
                    office = dict(
                        office_id = request[7],
                        office_name = request[8],
                    ),
                    mode = dict(
                        mode_id = request[9],
                        mode_name = request[10]
                    ),
                    nature = dict(
                        nature_id = request[11],
                        nature_name = request[12]
                    ),
                    technicians = [
                        dict(
                            technician_id = technician[0],
                            technician_name = technician[1]
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
                    RequestModel.office_client_id == OfficeModel.public_id
                ).filter(
                    RequestModel.mode_approach_id == ModeModel.public_id
                ).filter(
                    RequestModel.nature_type_id == NatureModel.public_id
                ).filter(
                    RequestModel.detail.ilike("%{}%".format(detail))
                ).order_by(RequestModel.date.desc()).all()
            ]

            if requests:
                return requests

            return 404

        except:
            return 500