import logging
from typing import Optional
import click
from flask import current_app, g
from flask.cli import with_appcontext
import psycopg2
import psycopg2.extras

from src.database.db_interface import IDataStorage
from .schema import instructions 

class PostgresConnection(IDataStorage):

    def get_db(self) -> Optional[tuple]:
        try:
            if 'db' not in 'g':
                g.db  = psycopg2.connect(
                        database=current_app.config['PG_DATABASE'],
                        host=current_app.config['PG_HOST'],
                        user=current_app.config['PG_USER'],
                        password=current_app.config['PG_PASSWORD'],
                        port=current_app.config['PG_PORT']
                        )

                logging.warning(
                        str({
                            'connection open when 0': g.db.closed
                            })

                        )

                g.c = g.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                return g.db, g.c
        except psycopg2.OperationalError as ex:
            logging.warning('connection failed when 1: ', g.db.closed)
            logging.exception(ex)

    def close_db(self, e=None) -> None:
        db_connect = g.pop('db', None)

        if db_connect is not None:
            db_connect.close()

    def init_db(self) -> None:

        db_connect, db_cursor = self.get_db()

        for i in instructions:
            logging.debug("This is the instruction: {}".format(i))
            db_cursor.execute(i)
        db_connect.commit()

connector = PostgresConnection()

@click.command('init-db')
@with_appcontext
def init_db_command():
    '''checks if db exists and creates a new db if not'''
    connector.init_db()
    click.echo('Initialized DB')

def init_app(app):
    app.teardown_appcontext(connector.close_db)
    app.cli.add_command(init_db_command)
