def calculate_security_score(
    event_count,
    alert_count,
    failed_logins=0
):
    score = 100

    # Security alerts
    score -= min(alert_count * 10, 40)

    # Failed login attempts
    score -= min(failed_logins * 5, 30)

    # Overall security events
    if event_count >= 20:
        score -= 15
    elif event_count >= 10:
        score -= 10
    elif event_count >= 5:
        score -= 5

    # Keep score between 0 and 100
    score = max(0, min(score, 100))

    if score >= 80:
        status = "Good"
    elif score >= 60:
        status = "Moderate"
    else:
        status = "Needs Attention"

    return {
        "score": score,
        "status": status
    }