import os

from flask import Flask
from flask.cli import with_appcontext
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import click
import logging


db = SQLAlchemy()
login_manager = LoginManager()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    login_manager.init_app(app)

    try:
        import flaskr.model
        if test_config is None:
            # load the instance config, if it exists, when not testing
            config_file = os.environ['PORTFOLIO_CONFIG_FILE']
            app.config.from_pyfile(config_file, silent=True)

        else:
            # load the test config if passed in
            app.config.from_mapping(test_config)
        db.init_app(app)

        # add command line commands
        migrate = Migrate(app, db)
        app.cli.add_command(migrate_command)

        # register routes
        from flaskr.routes.stock_transactions import stock_transactions
        app.register_blueprint(stock_transactions)
        from flaskr.routes.auth import auth_bp
        app.register_blueprint(auth_bp)
        from flaskr.routes.index import index_bp
        app.register_blueprint(index_bp)
    except Exception as e:
        logging.error(e)

    return app

@click.command("db")
@with_appcontext
def migrate_command():
    MigrateCommand()
