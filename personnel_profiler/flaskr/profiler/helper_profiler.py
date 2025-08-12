

def evaluate_helper(data):

    score = 100
    issues = []

    #id check
    id_credentials_validity = data.get('id_credentials_validity').lower()
    if id_credentials_validity == "valid":
        score -= 0
    elif id_credentials_validity == "expired":
        score -= 10
        issues.append('Outdated ID and/or documents')
    elif id_credentials_validity == "fake":
        score -= 40
        issues.append('Fake ID and/or documents')

    #missed deliveries check
    missed_delivery_rates = data.get('missed_delivery_rates')
    if missed_delivery_rates == 0:
        score -= 0
    elif missed_delivery_rates > 0 and missed_delivery_rates <= 5:
        score -= 20
        issues.append('Tendency to miss deliveries')
    elif missed_delivery_rates > 5:
        score -= 30
        issues.append('Frequently missing deliveries')

    #mismanagement check
    mismanagement_records = data.get('mismanagement_records')
    if mismanagement_records == 0:
        score -= 0
    elif mismanagement_records > 0 and mismanagement_records <= 3:
        score -= 20
        issues.append('Tendency to mishandle equipment')
    elif mismanagement_records > 3:
        score -= 40
        issues.append('Frequent equipment handling violations')

    #behavior score check
    behavior_reports_score = data.get('behavior_reports_score')
    if behavior_reports_score >= 4:
        score -= 0
    elif behavior_reports_score >= 3 and behavior_reports_score <= 4:
        score -= 10
        issues.append('Average behavioral score')
    elif behavior_reports_score < 3:
        score -= 30
        issues.append('Low behavioral score')

    return max(score, 0), issues