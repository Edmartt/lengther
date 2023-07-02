import logging
import traceback
import psycopg2
from src.database.db_interface import IDataStorage
from src.locations.models.model import Location
from .pg_access_interface import IDataAccess

class PGDataAccess(IDataAccess):

    def __init__(self, connection_object: IDataStorage, location: Location) -> None:
        self.location = location
        self.connection_object = connection_object

    def save_data(self) -> str:
        connection, cursor = self.connection_object.get_db()

        query = '''
        INSERT INTO locations (name, latitude, longitude) VALUES (%s, %s, %s) RETURNING id;
        '''

        try:
            cursor.execute(query, (self.location.name, self.location.latitude, self.location.longitude))
            data_response = cursor.fetchone()

            for _, v in enumerate(data_response.values()):
                self.location_id = v
            connection.commit()
            return self.location_id

        except psycopg2.ProgrammingError:
            logging.error(traceback.format_exc())
            return 'An internal error ocurred!'

        finally:
            self.connection_object.close_db()

    def read_locations(self) -> list:
        connection, cursor = self.connection_object.get_db()

        query = '''
        SELECT * FROM locations
        '''
        try:
            cursor.execute(query)
            result = cursor.fetchall()

            location = []

            if result:
                for _, row in enumerate(result):
                    my_dict = {'id': row['id'],'name': row['name'], 'longitude': row['longitude'], 'latitude': row['latitude']}
                    location.append(my_dict)

            connection.commit()
            return location

        except psycopg2.ProgrammingError:
            logging.error(traceback.format_exc())
            return ['An internal error ocurred!']

        finally:
            cursor.close()
            self.connection_object.close_db()

    def read_location(self, location_id: str) -> Location | None:
        connection, cursor = self.connection_object.get_db()
        query = '''
        SELECT * FROM locations WHERE id = %s
        '''

        try:
            cursor.execute(query, (location_id,))
            result = cursor.fetchone()

            if result is not None:
                self.location.id = result['id']
                self.location.name = result['name']
                self.location.latitude = result['latitude']
                self.location.longitude = result['longitude']
                connection.commit()
                return self.location

        except psycopg2.ProgrammingError:
            logging.error(traceback.format_exc())
            return None

        finally:
            cursor.close()
            self.connection_object.close_db()
