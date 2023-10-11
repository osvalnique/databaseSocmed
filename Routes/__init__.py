from flask import Blueprint

blueprint = Blueprint('my_blueprint', __name__)

from . import routesUsers
from . import routesTweet
# from Controller.auth import login_required
