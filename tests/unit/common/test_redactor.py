import unittest
from src.common.security.redactor import SecretRedactor

class TestSecretRedactor(unittest.TestCase):

    def test_redact_generic_api_key(self):
        content = 'api_key = "1234567890abcdef1234567890abcdef"'
        expected = 'api_key = "[REDACTED_SECRET]"'
        self.assertEqual(SecretRedactor.redact(content), expected)

    def test_redact_aws_key(self):
        content = 'AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"'
        expected = 'AWS_ACCESS_KEY_ID="[REDACTED_SECRET]"'
        self.assertEqual(SecretRedactor.redact(content), expected)

    def test_redact_private_key(self):
        content = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA3Tz2mr7SZiAMfQyuvBjM9Oi..
-----END RSA PRIVATE KEY-----
"""
        self.assertIn("[REDACTED_SECRET]", SecretRedactor.redact(content))
        self.assertNotIn("MIIEpQIBAAKCAQEA3Tz2mr7SZiAMfQyuvBjM9Oi..", SecretRedactor.redact(content))

    def test_no_redaction_for_safe_content(self):
        content = 'public_key = "not_a_secret"'
        self.assertEqual(SecretRedactor.redact(content), content)

if __name__ == '__main__':
    unittest.main()
