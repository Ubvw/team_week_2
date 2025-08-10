from flask import Blueprint, request, jsonify
from profiler.driver_profiler import evaluate_driver
from profiler.mechanic_profiler import evaluate_mechanic
from profiler.helper_profiler import evaluate_helper

bp = Blueprint('main', __name__)

@bp.route('/profile/driver', methods = ["POST"])
def driver():

    data = request.json()
    score, issues = evaluate_driver(data)

    return jsonify({"profile_score": score, "issues": issues})

@bp.route('/profile/mechanic', methods = ["POST"])
def mechanic():

    data = request.json()
    score, issues = evaluate_mechanic(data)

    return jsonify({"profile_score": score, "issues": issues})

@bp.route('/profile/helper', methods = ["POST"])
def helper():

    data = request.json()
    score, issues = evaluate_helper(data)

    return jsonify({"profile_score": score, "issues": issues})