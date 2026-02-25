"""
Unit tests for password analysis services.
Tests password strength logic, HIBP integration (mocked), and hash utilities.
"""
import hashlib
from unittest.mock import patch, MagicMock


from api.services import (
    calculate_password_strength,
    is_common_password,
    has_sequential_chars,
    has_repeated_chars,
    check_hibp_breach,
    get_hash_prefix,
)


# ---------------------------------------------------------------------------
# calculate_password_strength
# ---------------------------------------------------------------------------

class TestCalculatePasswordStrength:
    """Test the main password strength calculation function."""

    def test_very_strong_password(self):
        result = calculate_password_strength("Tr0ub4dor&3xPlorer!")
        assert result["score"] >= 90
        assert result["strength"] == "very_strong"
        assert result["criteria"]["uppercase"] is True
        assert result["criteria"]["lowercase"] is True
        assert result["criteria"]["numbers"] is True
        assert result["criteria"]["special"] is True

    def test_weak_password_short(self):
        result = calculate_password_strength("abc")
        assert result["score"] < 30
        assert result["strength"] == "weak"
        assert result["criteria"]["length"] is False

    def test_common_password_penalised(self):
        result = calculate_password_strength("password")
        assert result["criteria"]["no_common"] is False
        assert "Avoid common passwords" in result["feedback"]

    def test_sequential_password_penalised(self):
        result = calculate_password_strength("Abcde1234!")
        assert result["criteria"]["no_sequential"] is False

    def test_repeated_chars_penalised(self):
        result = calculate_password_strength("aaabbbccc")
        assert result["criteria"]["no_repeated"] is False
        assert "Avoid repeated characters" in result["feedback"]

    def test_score_length_tiers(self):
        # 8-char password gets first length tier
        r8 = calculate_password_strength("Aa1!aaaa")
        assert r8["criteria"]["length"] is True
        assert r8["criteria"]["length_12"] is False

        # 12-char password gets second tier
        r12 = calculate_password_strength("Aa1!aaaaaaaa")
        assert r12["criteria"]["length_12"] is True
        assert r12["criteria"]["length_16"] is False

        # 16-char password gets all length tiers
        r16 = calculate_password_strength("Aa1!aaaaaaaaaaaa")
        assert r16["criteria"]["length_16"] is True

    def test_returns_feedback_list(self):
        result = calculate_password_strength("short")
        assert isinstance(result["feedback"], list)
        assert len(result["feedback"]) > 0

    def test_excellent_feedback_for_strong_password(self):
        result = calculate_password_strength("Tr0ub4dor&3xPlorer!")
        assert "Excellent" in result["feedback"][0]

    def test_strength_labels_map_to_score(self):
        cases = [
            ("weak",        calculate_password_strength("abc")),
            ("good",        calculate_password_strength("Abcde123")),
            ("very_strong", calculate_password_strength("Tr0ub4dor&3xPlorer!")),
        ]
        for expected_label, result in cases:
            assert result["strength"] == expected_label, (
                f"Expected {expected_label}, got {result['strength']} (score={result['score']})"
            )

    def test_criteria_dict_has_all_keys(self):
        result = calculate_password_strength("Test1234!")
        expected_keys = {
            "length", "length_12", "length_16",
            "uppercase", "lowercase", "numbers", "special",
            "no_common", "no_sequential", "no_repeated",
        }
        assert set(result["criteria"].keys()) == expected_keys


# ---------------------------------------------------------------------------
# is_common_password
# ---------------------------------------------------------------------------

class TestIsCommonPassword:
    def test_detects_common_passwords(self):
        for pw in ["password", "123456", "qwerty", "admin", "letmein"]:
            assert is_common_password(pw), f"Expected {pw!r} to be detected as common"

    def test_case_insensitive(self):
        assert is_common_password("PASSWORD") is True
        assert is_common_password("ADMIN") is True

    def test_rejects_strong_password(self):
        assert is_common_password("Tr0ub4dor&3xPlorer!") is False


# ---------------------------------------------------------------------------
# has_sequential_chars
# ---------------------------------------------------------------------------

class TestHasSequentialChars:
    def test_numeric_sequence(self):
        assert has_sequential_chars("pass123word") is True

    def test_alpha_sequence(self):
        assert has_sequential_chars("Abcpassword") is True

    def test_keyboard_sequence(self):
        assert has_sequential_chars("qwepassword") is True

    def test_no_sequence(self):
        assert has_sequential_chars("Tr0ub4dor&3!") is False


# ---------------------------------------------------------------------------
# has_repeated_chars
# ---------------------------------------------------------------------------

class TestHasRepeatedChars:
    def test_three_repeated(self):
        assert has_repeated_chars("aaabbb") is True

    def test_two_repeated_ok(self):
        assert has_repeated_chars("aabb") is False

    def test_mixed(self):
        assert has_repeated_chars("Password111!") is True


# ---------------------------------------------------------------------------
# get_hash_prefix
# ---------------------------------------------------------------------------

class TestGetHashPrefix:
    def test_returns_5_chars(self):
        prefix = get_hash_prefix("mypassword")
        assert len(prefix) == 5

    def test_returns_uppercase_hex(self):
        prefix = get_hash_prefix("mypassword")
        assert prefix == prefix.upper()
        assert all(c in "0123456789ABCDEF" for c in prefix)

    def test_matches_sha1(self):
        pw = "testpassword"
        expected = hashlib.sha1(pw.encode()).hexdigest().upper()[:5]
        assert get_hash_prefix(pw) == expected


# ---------------------------------------------------------------------------
# check_hibp_breach  (mocked)
# ---------------------------------------------------------------------------

class TestCheckHibpBreach:
    @patch("api.services.requests.get")
    def test_breached_password_detected(self, mock_get):
        """If HIBP returns our suffix, is_breached=True with correct count."""
        pw = "password"
        sha1 = hashlib.sha1(pw.encode()).hexdigest().upper()
        suffix = sha1[5:]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = f"{suffix}:12345\nOTHERHASH:1"
        mock_get.return_value = mock_response

        is_breached, count = check_hibp_breach(pw)
        assert is_breached is True
        assert count == 12345

    @patch("api.services.requests.get")
    def test_clean_password_not_breached(self, mock_get):
        """If our suffix is absent from HIBP response, not breached."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "AAAAA:100\nBBBBB:200"
        mock_get.return_value = mock_response

        is_breached, count = check_hibp_breach("Tr0ub4dor&3xPlorer!")
        assert is_breached is False
        assert count == 0

    @patch("api.services.requests.get")
    def test_api_error_returns_safe_default(self, mock_get):
        """Network error → treat as not breached (fail open)."""
        import requests as req_lib
        mock_get.side_effect = req_lib.RequestException("timeout")

        is_breached, count = check_hibp_breach("anypassword")
        assert is_breached is False
        assert count == 0

    @patch("api.services.requests.get")
    def test_api_non_200_returns_false(self, mock_get):
        """Non-200 status → treat as not breached."""
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_get.return_value = mock_response

        is_breached, count = check_hibp_breach("anypassword")
        assert is_breached is False
        assert count == 0

    @patch("api.services.requests.get")
    def test_k_anonymity_prefix_sent(self, mock_get):
        """Verify only the 5-char prefix is sent to HIBP (k-anonymity)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = ""
        mock_get.return_value = mock_response

        pw = "MyTestPassword"
        expected_prefix = hashlib.sha1(pw.encode()).hexdigest().upper()[:5]
        check_hibp_breach(pw)

        called_url = mock_get.call_args[0][0]
        assert called_url.endswith(expected_prefix)
        # Full hash must NOT appear in the URL
        full_hash = hashlib.sha1(pw.encode()).hexdigest().upper()
        assert full_hash not in called_url
