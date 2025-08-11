from .extensions import db
import enum

class drug_test_results(enum.Enum):
    POSITIVE = 'positive'
    NEGATIVE = 'negative'

class validity(enum.Enum):
    VALID = 'valid'
    EXPIRED = 'expired'
    FAKE = 'fake'

class profile_type(enum.Enum):
    DRIVER = 'driver'
    MECHANIC = 'mechanic'
    HELPER = 'helper'


class DriverProfile(db.Model):
    __tablename__ = "driver_profiles"

    profile_id = db.Column(db.Integer, primary_key=True)
    profile_name = db.Column(db.String(50))
    driving_violations = db.Column(db.Integer)
    drug_test_result = db.Column(db.Enum(drug_test_results))
    license_validity = db.Column(db.Enum(validity))
    incident_involvement = db.Column(db.Boolean)
    breathalyzer_results = db.Column(db.Float)
    dangerous_driving_patterns = db.Column(db.Boolean)
    work_violations = db.Column(db.Integer)
    performance_rating = db.Column(db.Float)
    warehouse_infractions = db.Column(db.Integer)
    document_validity = db.Column(db.Boolean)

class MechanicProfile(db.Model):
    __tablename__ = "mechanic_profiles"

    profile_id = db.Column(db.Integer, primary_key=True)
    profile_name = db.Column(db.String(50))
    id_cert_validity = db.Column(db.Enum(validity))
    repair_rates = db.Column(db.Integer)
    internal_review_score = db.Column(db.Float)
    equipment_violations = db.Column(db.Integer)

class HelperProfile(db.Model):
    __tablename__ = "helper_profiles"

    profile_id = db.Column(db.Integer, primary_key=True)
    profile_name = db.Column(db.String(50))
    id_credentials_validity = db.Column(db.Enum(validity))
    missed_delivery_rates = db.Column(db.Integer)
    mismanagement_records = db.Column(db.Integer)
    behavior_reports_score = db.Column(db.Float)

class EvaluationResults(db.Model):
    __tablename__ = "eval_results"

    profile_id = db.Column(db.Integer, primary_key=True)
    profile_type = db.Column(db.Enum(profile_type))
    profile_score = db.Column(db.Integer)
    issues_list = db.Column(db.String())