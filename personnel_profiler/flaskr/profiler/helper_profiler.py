

def evaluate_helper(data):

    score = 100
    issues = []

    #id check
    id_cert_validity = data.get('id_validity')
    if id_cert_validity == "valid":
        score -= 0
    elif id_cert_validity == "expired":
        score -= 10
        issues.append('Outdated ID and/or documents')
    elif id_cert_validity == "fake":
        score -= 40
        issues.append('Fake ID and/or documents')

    #missed deliveries check
    missed_deliveries = data.get('missed_deliveries')
    if missed_deliveries == 0:
        score -= 0
    elif missed_deliveries > 0 and missed_deliveries <= 5:
        score -= 20
        issues.append('Tendency to miss deliveries')
    elif missed_deliveries > 5:
        score -= 30
        issues.append('Frequently missing deliveries')

    #mismanagement check
    mismanagements = data.get('warehouse_mismanagements')
    if mismanagements == 0:
        score -= 0
    elif mismanagements > 0 and mismanagements <= 3:
        score -= 20
        issues.append('Tendency to mishandle equipment')
    elif mismanagements > 3:
        score -= 40
        issues.append('Frequent equipment handling violations')

    #behavior score check
    behavior_score = data.get('behavior_score')
    if behavior_score >= 4:
        score -= 0
    elif behavior_score >= 3 and behavior_score <= 4:
        score -= 10
        issues.append('Average behavioral score')
    elif behavior_score < 3:
        score -= 30
        issues.append('Low behavioral score')

    return max(score, 0), issues