
from flask import Blueprint
from http import HTTPStatus


index_bp = Blueprint(
    'index', __name__)


@index_bp.route("/")
def index():
    return {"versao": "0.0.1"}, HTTPStatus.OK


@index_bp.route("/health")
def health():
    return {"health": "ok"}, HTTPStatus.OK
