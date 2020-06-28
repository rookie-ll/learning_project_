from APP import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand

app = create_app()

manager = Manager(app)
app.app_context().push()
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
