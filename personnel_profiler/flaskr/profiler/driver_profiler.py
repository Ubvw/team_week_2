def evaluate_driver(data: dict):
    score = 100
    issues = []

    if data.get("driving_violations", 0) > 0:
        deduction = min(data["driving_violations"] * 10, 30)
        score -= deduction
        issues.append(f"{data['driving_violations']} driving violation(s) recorded")

    if data.get("drug_test_result", "").lower() == "positive":
        score -= 50
        issues.append("Failed drug test")

    if data.get("license_validity", "").lower() in ["expired", "fake"]:
        score -= 40
        issues.append(f"Invalid license ({data['license_validity']})")

    if data.get("incident_involvement"):
        score -= 15
        issues.append("Warehouse incident involvement")

    if data.get("rider_rating") is not None and data["rider_rating"] < 3.0:
        score -= 15
        issues.append("Poor rider/customer ratings")

    if data.get("breathalyzer_results") is not None and data["breathalyzer_results"] > 0.08:
        score -= 30
        issues.append(f"Breathalyzer BAC {data['breathalyzer_results']:.2f} exceeds legal limit")

    if data.get("dangerous_driving_patterns"):
        score -= 20
        issues.append("Reckless/dangerous driving patterns detected")

    if data.get("work_violations", 0) > 0:
        deduction = min(data["work_violations"] * 5, 25)
        score -= deduction
        issues.append(f"{data['work_violations']} work-related violation(s)")

    if data.get("performance_rating") is not None and data["performance_rating"] < 3.0:
        score -= 10
        issues.append("Low work performance/feedback")

    if data.get("warehouse_infractions", 0) > 0:
        deduction = min(data["warehouse_infractions"] * 5, 15)
        score -= deduction
        issues.append(f"{data['warehouse_infractions']} warehouse-related infraction(s)")

    if data.get("document_validity") is False:
        score -= 40
        issues.append("Submitted fake or invalid documents")

    return max(score, 0), issues
