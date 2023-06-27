import os
from flask import current_app, jsonify, request
from flask.views import MethodView
import redis
from rq import Queue
from src.locations.data.pg_access_interface import IDataAccess
from src.locations.models.model import Location
from src.locations.cache.cache_redis import cache

class MyLocations(MethodView):

    decorators = [cache.cached(timeout=30, query_string=True)]
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

    def get(self, location_id: str | None = None) -> tuple:
        
        with current_app.app_context():
            url_redis = os.environ.get('REDIS_URL') or ''
            r = redis.from_url(url=url_redis)
            q = Queue(connection=r)

        if location_id is not None:
            location = q.enqueue(self.data_access.read_location, location_id)
            task = location.get_id()
            result = location.result
            print('job result: ', result)
            print("task id: ", task)

            if location is not None:
                return jsonify({'location': task}), 200
            else:
                return jsonify({'response': 'location not found'}), 404

        try:
            locations_list = self.data_access.read_locations()
            return jsonify({'locations': locations_list}), 200

        except Exception as ex:
            return jsonify({'response': ex}), 500
