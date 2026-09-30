from urllib.parse import urlparse


def analyze_url(url):
    url = url.strip()

    if not url:
        return {
            "risk": "Invalid",
            "score": 0,
            "reasons": ["URL is empty."]
        }

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    score = 0
    reasons = []

    # Check HTTPS
    if parsed.scheme != "https":
        score += 2
        reasons.append("URL does not use HTTPS.")

    # Check hostname
    hostname = parsed.hostname

    if not hostname:
        return {
            "risk": "Invalid",
            "score": 0,
            "reasons": ["Invalid URL format."]
        }

    # IP address instead of normal domain
    parts = hostname.split(".")

    if all(part.isdigit() for part in parts if part):
        score += 2
        reasons.append("URL uses an IP address instead of a domain name.")

    # Suspicious characters
    if "@" in url:
        score += 2
        reasons.append("URL contains '@', which can hide the real destination.")

    # Very long URL
    if len(url) > 100:
        score += 1
        reasons.append("URL is unusually long.")

    # Too many subdomains
    if hostname.count(".") >= 4:
        score += 1
        reasons.append("URL contains many subdomains.")

    # Final risk
    if score >= 4:
        risk = "High"
    elif score >= 2:
        risk = "Medium"
    else:
        risk = "Low"

    if not reasons:
        reasons.append("No basic suspicious indicators detected.")

    return {
        "risk": risk,
        "score": score,
        "reasons": reasons,
        "url": url
    }