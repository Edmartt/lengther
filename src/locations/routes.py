from src.database.postgres import PostgresConnection
from src.locations.data.pg_data_access import PGDataAccess
from src.locations.models.model import Location
from . import locations_routes
from .locs import MyLocations

postgres_object = PostgresConnection()

location = Location()
my_locs = MyLocations.as_view('create location',location, PGDataAccess(postgres_object, location))

locations_routes.add_url_rule('/api/v1/locations', view_func=my_locs, methods=['POST'])
locations_routes.add_url_rule('/api/v1/locations', view_func=my_locs, methods=['GET'])

locations_routes.add_url_rule('/api/v1/locations/<string:location_id>', view_func=my_locs, methods=['GET'])
