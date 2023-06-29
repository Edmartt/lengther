import logging
import traceback
from flask import jsonify, request
from flask.views import MethodView
from src.locations.data.pg_access_interface import IDataAccess
from src.locations.models.model import Location
from src.locations.cache.cache_redis import cache

class MyLocations(MethodView):

    def __init__(self, location: Location, data_access: IDataAccess) -> None:
        self.location = location
        self.data_access = data_access

    def post(self):
        data = request.get_json()

        for _, v in enumerate(data.values()):
            match v:
                case "":
                    return jsonify({'response': 'missing mandatory data'}), 400

        self.location.name = data.get('name')
        self.location.latitude = data.get('latitude')
        self.location.longitude = data.get('longitude')

        if self.location.name is None or self.location.latitude is None or self.location.longitude is None:
            return jsonify({'response': 'missing mandatory data'}), 400

        location_id = self.data_access.save_data()

        return jsonify({'location_id': location_id}), 201

    @cache.cached(timeout=30)
    def get(self, location_id: str | None = None) -> tuple:

        if location_id is not None:
            location = self.data_access.read_location(location_id)

            if location is not None:
                return jsonify({'location': location.__dict__}), 200
            else:
                return jsonify({'response': 'location not found'}), 404

        try:
            locations_list = self.data_access.read_locations()
            return jsonify({'locations': locations_list}), 200

        except Exception:
            logging.error(traceback.format_exc())
            return jsonify({'response': 'An internal error occurred!'}), 500
