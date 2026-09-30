from app.services.password_service import check_password_strength
from app.services.url_analyzer import analyze_url
from app.services.file_integrity import (
    calculate_bytes_hash,
    check_file_integrity
)
from app.services.security_score import calculate_security_score


def test_password_strength():

    result = check_password_strength("CyberSentinel@2026")

    assert result["strength"] == "Strong"


def test_url_analyzer():

    result = analyze_url("https://example.com")

    assert result["risk"] == "Low"


def test_file_hash():

    file_data = b"CyberSentinel test file"

    hash_value = calculate_bytes_hash(file_data)

    assert len(hash_value) == 64


def test_file_integrity():

    result = check_file_integrity(
        "abc123",
        "abc123"
    )

    assert result["status"] == "SAFE"


def test_security_score():

    result = calculate_security_score(
        event_count=0,
        alert_count=0,
        failed_logins=0
    )

    assert result["score"] == 100
    assert result["status"] == "Good"