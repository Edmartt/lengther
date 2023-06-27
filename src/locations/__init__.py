from flask import Blueprint

locations_routes = Blueprint('locations', __name__)

from . import locs, routes, hooks
