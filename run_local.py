from hello import *
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

app.config['DEBUG'] = True
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    "Create SQLAlchemy database from models"
    db.create_all()

if __name__ == '__main__':
    manager.run()