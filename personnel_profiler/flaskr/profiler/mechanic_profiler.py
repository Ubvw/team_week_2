
def evaluate_mechanic(data):

    score = 100
    issues = []

    #id/certification check
    id_cert_validity = data.get('id_cert_validity').lower()
    if id_cert_validity == "valid":
        score -= 0
    elif id_cert_validity == "expired":
        score -= 10
        issues.append('Expired ID and/or Certification')
    elif id_cert_validity == "fake":
        score -= 40
        issues.append('Fake ID and/or Certification')

    #repair/fix rate check
    fix_rate = data.get('repair_rates')
    if fix_rate >= 4:
        score -= 0
    elif fix_rate >= 2 and fix_rate < 4:
        score -= 5
        issues.append('Average fix and repair rates per day')
    elif fix_rate >= 0 and fix_rate < 2:
        score -= 30
        issues.append('Below average fix and repair rates per day')

    #downtime check
    downtime = data.get('downtime_intervals')
    if downtime <= 30:
        score -= 0
    elif downtime > 30 and downtime <= 45:
        score -= 5
        issues.append('Average downtimes post-fixes')
    elif downtime > 45:
        score -= 25
        issues.append('Long downtimes post-fixes')

    #review score check
    review_score = data.get('internal_review_score')
    if review_score >= 8:
        score -= 0
    elif review_score < 8 and review_score >= 5:
        score -= 10
        issues.append('Average peer/internal review score')
    elif review_score < 5:
        score -= 35
        issues.append('Low peer/internal review score')

    #equip violations check
    equip_violations = data.get('equipment_violations')
    if equip_violations == 0:
        score -= 0
    elif equip_violations > 0 and equip_violations <= 3:
        score -= 20
        issues.append('Tendency to mishandle equipment')
    elif equip_violations > 3:
        score -= 40
        issues.append('Frequent equipment handling violations')

    return max(score, 0), issues