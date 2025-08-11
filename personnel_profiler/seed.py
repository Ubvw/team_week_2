import random
from faker import Faker
from flaskr.extensions import db
from flaskr.models import (DriverProfile, MechanicProfile, HelperProfile, drug_test_results, validity)

fake = Faker()

def seed_data():
    db.drop_all()
    db.create_all()

    for _ in range(25):
        driver_data = {
            "profile_name" : fake.name(),
            "driving_violations" : random.randint(0, 5),
            "drug_test_result": random.choice(list(drug_test_results)),
            "license_validity": random.choice(list(validity)),
            "incident_involvement": fake.boolean(),
            "breathalyzer_results": round(random.uniform(0.0, 0.15), 2),
            "dangerous_driving_patterns": fake.boolean(),
            "work_violations": random.randint(0, 5),
            "performance_rating": round(random.uniform(1.0, 5.0), 1),
            "warehouse_infractions": random.randint(0, 3),
            "document_validity": fake.boolean()
        }
        driver = DriverProfile(**driver_data)
        db.session.add(driver)
    
    for _ in range(25):
        mech_data = {
            "profile_name": fake.name(),
            "id_cert_validity": random.choice(list(validity)),
            "repair_rates": random.randint(0,6),
            "internal_review_score": round(random.uniform(1.0, 10.0), 1),
            "equipment_violations": random.randint(0,5)
        }
        mech = MechanicProfile(**mech_data)
        db.session.add(mech)

    for _ in range(25):
        helper_data = {
            "profile_name": fake.name(),
            "id_credentials_validity": random.choice(list(validity)),
            "missed_delivery_rates": random.randint(0, 10),
            "mismanagement_records": random.randint(0, 5),
            "behavior_reports_score": round(random.uniform(1.0, 5.0), 1),
        }
        helper = HelperProfile(**helper_data)
        db.session.add(helper)
    
    db.session.commit()

def register_seed_command(app):
    @app.cli.command("seed-db")
    def seed_db():
        seed_data()
        print("Database seeded with sample profiles.")