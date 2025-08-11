from flask import Blueprint, request, jsonify
from .profiler.driver_profiler import evaluate_driver
from .profiler.mechanic_profiler import evaluate_mechanic
from .profiler.helper_profiler import evaluate_helper
from .models import EvaluationResults
from .extensions import db
import json

bp = Blueprint('main', __name__)

def save_evaluation(profile_type, data, evaluator):
    score, issues = evaluator(data)
    new_result = {
        'profile_id': data.get('profile_id'),
        'profile_type': profile_type,
        'profile_score': score,
        'issues_list': json.dumps(issues)
    }
    result = EvaluationResults(**new_result)
    db.session.add(result)
    db.session.commit()

    return score, issues


@bp.route('/profile/driver', methods = ["POST"])
def driver():

    data = request.json
    score, issues = save_evaluation('driver', data, evaluate_driver)
    return jsonify({"profile_score": score, "issues": issues})

@bp.route('/profile/mechanic', methods = ["POST"])
def mechanic():

    data = request.json
    score, issues = save_evaluation('driver', data, evaluate_mechanic)
    return jsonify({"profile_score": score, "issues": issues})

@bp.route('/profile/helper', methods = ["POST"])
def helper():

    data = request.json
    score, issues = save_evaluation('driver', data, evaluate_helper)
    return jsonify({"profile_score": score, "issues": issues})