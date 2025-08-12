from .models import EvaluationResults, DriverProfile, MechanicProfile, HelperProfile
from .models import profile_type as ProfileType
from .profiler.driver_profiler import evaluate_driver
from .profiler.mechanic_profiler import evaluate_mechanic
from .profiler.helper_profiler import evaluate_helper
from .extensions import db
import json


def get_employee_database():
    employees = []

    drivers = DriverProfile.query.all()
    for driver in drivers:
        data_dict = {
            "profile_id": driver.profile_id,
            "profile_name": driver.profile_name,
            "driving_violations": driver.driving_violations,
            "drug_test_result": driver.drug_test_result.value,
            "license_validity": driver.license_validity.value,
            "incident_involvement": driver.incident_involvement,
            "rider_rating": driver.rider_rating,
            "breathalyzer_results": driver.breathalyzer_results,
            "dangerous_driving_patterns": driver.dangerous_driving_patterns,
            "work_violations": driver.work_violations,
            "performance_rating": driver.performance_rating,
            "warehouse_infractions": driver.warehouse_infractions,
            "document_validity": driver.document_validity
        }
        score, issues = evaluate_driver(data_dict)
        driver_formatted = format_to_json('Driver', data_dict, score, issues)
        employees.append(driver_formatted)
    
    mechanics = MechanicProfile.query.all()
    for mechanic in mechanics:
        data_dict = {
            "profile_id": mechanic.profile_id,
            "profile_name": mechanic.profile_name,
            "id_cert_validity": mechanic.id_cert_validity.value,
            "repair_rates": mechanic.repair_rates,
            "downtime_intervals": mechanic.downtime_intervals,
            "internal_review_score": mechanic.internal_review_score,
            "equipment_violations": mechanic.equipment_violations
        }
        score, issues = evaluate_mechanic(data_dict)
        mechanic_formatted = format_to_json('Mechanic', data_dict, score, issues)
        employees.append(mechanic_formatted)

    helpers = HelperProfile.query.all()
    for helper in helpers:
        data_dict = {
            "profile_id": helper.profile_id,
            "profile_name": helper.profile_name,
            "id_credentials_validity": helper.id_credentials_validity.value,
            "missed_delivery_rates": helper.missed_delivery_rates,
            "mismanagement_records": helper.mismanagement_records,
            "behavior_reports_score": helper.behavior_reports_score
        }
        score, issues = evaluate_helper(data_dict)
        helper_formatted = format_to_json('Helper', data_dict, score, issues)
        employees.append(helper_formatted)

    return employees


def get_employee_data(profile_type, id):
    if profile_type == "Driver":
        driver = DriverProfile.query.filter_by(profile_id=id).first()
        if not driver:
            return None

        data_dict = {
            "profile_id": driver.profile_id,
            "profile_name": driver.profile_name,
            "driving_violations": driver.driving_violations,
            "drug_test_result": driver.drug_test_result.value,
            "license_validity": driver.license_validity.value,
            "incident_involvement": driver.incident_involvement,
            "rider_rating": driver.rider_rating,
            "breathalyzer_results": driver.breathalyzer_results,
            "dangerous_driving_patterns": driver.dangerous_driving_patterns,
            "work_violations": driver.work_violations,
            "performance_rating": driver.performance_rating,
            "warehouse_infractions": driver.warehouse_infractions,
            "document_validity": driver.document_validity
        }
        score, issues = get_score_record(profile_type, id)
        return format_to_json('Driver', data_dict, score, issues)

    elif profile_type == "Mechanic":
        mechanic = MechanicProfile.query.filter_by(profile_id=id).first()
        if not mechanic:
            return None

        data_dict = {
            "profile_id": mechanic.profile_id,
            "profile_name": mechanic.profile_name,
            "id_cert_validity": mechanic.id_cert_validity.value,
            "repair_rates": mechanic.repair_rates,
            "downtime_intervals": mechanic.downtime_intervals,
            "internal_review_score": mechanic.internal_review_score,
            "equipment_violations": mechanic.equipment_violations
        }
        score, issues = get_score_record(profile_type, id)
        return format_to_json('Mechanic', data_dict, score, issues)

    elif profile_type == "Helper":
        helper = HelperProfile.query.filter_by(profile_id=id).first()
        if not helper:
            return None

        data_dict = {
            "profile_id": helper.profile_id,
            "profile_name": helper.profile_name,
            "id_credentials_validity": helper.id_credentials_validity.value,
            "missed_delivery_rates": helper.missed_delivery_rates,
            "mismanagement_records": helper.mismanagement_records,
            "behavior_reports_score": helper.behavior_reports_score
        }
        score, issues = get_score_record(profile_type, id)
        return format_to_json('Helper', data_dict, score, issues)

    else:
        return None


def get_score_record(type, id):

    profile_type_enum = ProfileType(type)

    employee = EvaluationResults.query.filter_by(profile_id=id, profile_type=profile_type_enum).first()
    if not employee:
        return None, None
    issues_list = json.loads(employee.issues_list)
    return employee.profile_score, issues_list


def get_database_stats():

    total_employees = 0
    total_high_risk = 0
    average_score = 0.0

    employee_evals = EvaluationResults.query.all()

    for eval in employee_evals:
        total_employees += 1
        total_high_risk += 1 if eval.profile_score <= 34 else 0
        average_score += eval.profile_score

    average_score /= total_employees

    response_formatted = {
        "totalEmployees": total_employees,
        "highRiskCount": total_high_risk,
        "averageScore": average_score
    }

    return response_formatted



def format_to_json(type, data, score, issues_list):
    
    save_evaluation(type, data, score, issues_list)
    
    details = {}

    if type == 'Driver':

        details = {
            'drivingViolationRecords': data.get('driving_violations'),
            'drugTestResults': data.get('drug_test_result'),
            'licenseVerification': data.get('license_validity'),
            'warehouseIncidentInvolvement': data.get('incident_involvement'),
            'riderCustomerRatings': data.get('rider_rating'),
            'breathalyzerResults': data.get('breathalyzer_results'),
            'recklessDrivingPatterns': data.get('dangerous_driving_patterns'),
            'drivingWorkViolations': data.get('work_violations'),
            'workPerformanceFeedback': data.get('performance_rating'),
            'warehouseInfractions': data.get('warehouse_infractions'),
            'credentialValidity': data.get('document_validity'),
        }

    elif type == 'Mechanic':
    
        details = {
            'certificationsValidID': data.get('id_cert_validity'),
            'repairLogsRepeatFixRates': data.get('repair_rates'),
            'downtimePostMaintenance': data.get('downtime_intervals'),
            'peerInternalReviews': data.get('internal_review_score'),
            'equipmentHandlingViolations': data.get('equipment_violations'),
        }

    elif type == 'Helper':

        details = {
            'submittedIDsDocuments': data.get('id_credentials_validity'),
            'missedDeliveries': data.get('missed_delivery_rates'),
            'warehouseMismanagement': data.get('mismanagement_records'),
            'behaviorReports': data.get('behavior_reports_score')
        }

    response = {
        'id': data.get('profile_id'),
        'name': data.get('profile_name'),
        'role': type,
        'profileScore': score,
        'riskLevel': 'High' if score <= 34 else ('Medium' if score > 34 and score <= 66 else 'Low'),
        'issues': issues_list,
        'details': details,
    }
    
    return response

def save_evaluation(type, data, score, issues_list):

    profile_id = data.get('profile_id')
    profile_type_enum = ProfileType(type)

    new_result = {
        'profile_id': profile_id,
        'profile_type': profile_type_enum,
        'profile_score': score,
        'issues_list': json.dumps(issues_list)
    }
    
    existing_result = EvaluationResults.query.filter_by(profile_id=profile_id, profile_type=profile_type_enum).first()
    result = EvaluationResults(**new_result)

    if existing_result is None:
        db.session.add(result)
    else:
        for key, value in new_result.items():
            setattr(existing_result, key, value)

    db.session.commit()