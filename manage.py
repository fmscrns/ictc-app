import os

from app import create_app
app = create_app(os.getenv("BOILERPLATE_ENV"))
app.app_context().push()

from app.utils._prep import establish_routes
app = establish_routes(app)

from flask_script import Manager
manager = Manager(app)

from app import db
from flask_migrate import Migrate, MigrateCommand
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

@manager.command
def run():
    app.run(port=8000)

if __name__ == "__main__":
    manager.run()