import re
import logging
from typing import List, Pattern

logger = logging.getLogger(__name__)

class SecretRedactor:
    """
    Redacts sensitive information (secrets, keys, tokens) from text content
    using a predefined set of regular expressions.
    """

    # Common patterns for API keys and secrets
    # These are heuristic and not exhaustive, but cover many common cases.
    SECRET_PATTERNS: List[Pattern] = [
        # Generic API Key / Token assignments (e.g., api_key = "xyz", token: "abc")
        re.compile(r'(?i)(api[_-]?key|auth[_-]?token|access[_-]?token|secret[_-]?key|password|passwd|pwd)\s*[:=]\s*["\']([a-zA-Z0-9_\-]{8,})["\']'),
        
        # AWS Keys
        re.compile(r'(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])'),  # AKIA... (Access Key ID - loose check)
        re.compile(r'(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])'), # AWS Secret Key (heuristic)

        # Google API Key (AIza...)
        re.compile(r'AIza[0-9A-Za-z-_]{35}'),
        
        # Stripe Keys (sk_live_..., pk_live_...)
        re.compile(r'(?:r|s)k_live_[0-9a-zA-Z]{24,}') ,
        
        # Private Keys (PGP, RSA, PEM blocks)
        re.compile(r'-----BEGIN [A-Z ]+ PRIVATE KEY-----.*?-----END [A-Z ]+ PRIVATE KEY-----', re.DOTALL),
        re.compile(r'-----BEGIN [A-Z ]+ CERTIFICATE-----.*?-----END [A-Z ]+ CERTIFICATE-----', re.DOTALL),
        
        # Slack Token
        re.compile(r'xox[baprs]-([0-9a-zA-Z]{10,48})'),
        
        # GitHub Personal Access Token (classic and fine-grained)
        re.compile(r'gh[pousr]_[a-zA-Z0-9]{36,255}'),
    ]

    @classmethod
    def redact(cls, content: str) -> str:
        """
        Scans the input content and replaces detected secrets with [REDACTED].
        
        Args:
            content (str): The raw text content.
            
        Returns:
            str: The sanitized content.
        """
        if not content:
            return content

        redacted_content = content
        
        for pattern in cls.SECRET_PATTERNS:
            # For patterns with capturing groups (like the generic assignment), 
            # we want to redact specifically the value group if possible, 
            # or the whole match if no groups are specific or intended.
            
            # However, standard re.sub doesn't easily support "replace group 2 only".
            # We'll use a callback to handle this logic safely.
            
            def replace_match(match):
                # If the pattern has capturing groups (like key="value"), 
                # usually the last group is the secret.
                # For simpler patterns (like AWS key), there might be 0 or 1 group.
                
                if pattern.groups > 0:
                    # Reconstruct the string but redact the capture groups that look like secrets.
                    # This is complex to generalize. 
                    # SIMPLIFICATION: For the generic assignment pattern (Group 1=KeyName, Group 2=Value),
                    # we want to keep Group 1 and redact Group 2.
                    
                    # We will handle specific known structures:
                    
                    # Generic assignment: (key)(sep)(value) -> handled by the specific regex structure above
                    if "(?i)(api[_-]?key" in match.re.pattern:
                        # Group 1 is key name, Group 2 is value
                        full_match = match.group(0)
                        key_part = match.group(1)
                        secret_value = match.group(2)
                        
                        # We simply replace the secret value within the full match string
                        return full_match.replace(secret_value, "[REDACTED_SECRET]")
                    
                    # Slack token (xox...) - Group 1 is the suffix
                    if "xox" in match.re.pattern:
                         return "[REDACTED_SLACK_TOKEN]"
                         
                    return "[REDACTED_SECRET]"
                else:
                    # No groups, replace the whole match
                    return "[REDACTED_SECRET]"

            redacted_content = pattern.sub(replace_match, redacted_content)
            
        return redacted_content
