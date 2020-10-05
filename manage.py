from app import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import models

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

@manager.command
def run():
    app.run(debug=True, port=8000)

if __name__ == "__main__":
    manager.run()
