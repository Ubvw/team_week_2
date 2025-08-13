from flask import Blueprint, jsonify
from .utils import get_employee_database, get_employee_data, get_database_stats

bp = Blueprint('main', __name__)

@bp.route('/employees', methods = ["GET"])
def get_employees():
    response = get_employee_database()
    return jsonify(response)

@bp.route('/employee/<profile_type>/<id>', methods = ["GET"])
def get_employee(profile_type, id):
    response = get_employee_data(profile_type, id)
    return jsonify(response)

@bp.route('/employees/stats', methods = ["GET"])
def get_statistics():
    response = get_database_stats()
    return jsonify(response)


