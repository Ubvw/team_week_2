def evaluate_driver(data):
    score = 100
    issues = []

    if data.get("driving_violations", 0) > 0:
        score -= min(data["driving_violations"] * 10, 30)
        issues.append(f"{data['driving_violations']} driving violation(s) recorded")

    if data.get("drug_test", "").lower() == "positive":
        score -= 50
        issues.append("Failed drug test")

    if data.get("license_status", "").lower() in ["revoked", "fake", "expired"]:
        score -= 40
        issues.append(f"Invalid license ({data['license_status']})")

    if data.get("warehouse_incident"):
        score -= 15
        issues.append("Warehouse incident involvement")

    if data.get("rating", 5.0) < 3.0:
        score -= 15
        issues.append("Poor rider/customer ratings")

    if data.get("breathalyzer", 0.0) > 0.08:
        score -= 30
        issues.append(f"Breathalyzer BAC {data['breathalyzer']:.2f} exceeds legal limit")

    if data.get("reckless_driving"):
        score -= 20
        issues.append("Reckless/dangerous driving patterns detected")

    if data.get("work_violations", 0) > 0:
        score -= min(data["work_violations"] * 5, 25)
        issues.append(f"{data['work_violations']} work-related violation(s)")

    if data.get("work_performance", 5.0) < 3.0:
        score -= 10
        issues.append("Low work performance/feedback")

    if data.get("warehouse_infractions", 0) > 0:
        score -= min(data["warehouse_infractions"] * 5, 15)
        issues.append(f"{data['warehouse_infractions']} warehouse-related infraction(s)")

    if data.get("fake_documents"):
        score -= 40
        issues.append("Submitted fake or invalid documents")

    return max(score, 0), issues
