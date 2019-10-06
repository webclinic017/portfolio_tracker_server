import os

from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
import click
import logging


db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

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
        app.cli.add_command(init_db_command)

        # register routes
        from flaskr.routes.stock_transactions import stock_transactions
        app.register_blueprint(stock_transactions)
    except Exception as e:
        logging.error(e)

    return app

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    try:
        db.drop_all()
        db.create_all()
        db.session.commit()
        click.echo("Initialized the database.")
    except Exception as e:
        logging.error('Failed to initialize database')
        logging.error(e)
        db.session.rollback()
