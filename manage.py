import os

from app import create_app
app = create_app(os.getenv("BOILERPLATE_ENV"))
app.app_context().push()

from flask_script import Manager
manager = Manager(app)

from app import db
from flask_migrate import Migrate, MigrateCommand
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

from app.utils._prep import establish_routes
app = establish_routes(app)

@manager.command
def run():
    app.run(port=8000)

# import datetime, xlrd, uuid
# from app.server.models import *

# @manager.command
# def read_requests():
#     book = xlrd.open_workbook("Book1.xlsx")
#     sheet = book.sheet_by_index(0)

#     for i in range(sheet.nrows):
#         req_pid = str(uuid.uuid4())
#         new_request = RequestModel(
#             public_id = req_pid,
#             no = sheet.cell_value(rowx=i, colx=1),
#             date = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(rowx=i, colx=0), book.datemode)),
#             detail = sheet.cell_value(rowx=i, colx=4),
#             result = 0,
#             rating = sheet.cell_value(rowx=i, colx=5),
#             registered_on = datetime.datetime.utcnow(),
#             office_client_id = sheet.cell_value(rowx=i, colx=6),
#             mode_approach_id = sheet.cell_value(rowx=i, colx=2),
#             nature_type_id = sheet.cell_value(rowx=i, colx=3),    
#         )

#         db.session.add(new_request)

#         for fixer_id in sheet.cell_value(rowx=i, colx=7).split(", "):
#             rep_pid = str(uuid.uuid4())

#             new_repair = RepairModel(
#                 public_id = rep_pid,
#                 registered_on = datetime.datetime.utcnow(),
#                 technician_fixer_id = fixer_id,
#                 request_task_id = req_pid
#             )

#             db.session.add(new_repair)

#         db.session.commit()

if __name__ == "__main__":
    manager.run()