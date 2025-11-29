import logging
import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# This key needs to be securely managed and consistent across application restarts.
# In production, fetch from a secret management service or a secure environment variable.
# For development, you can generate one using Fernet.generate_key() and store in .env
ENCRYPTION_KEY = os.getenv("APP_ENCRYPTION_KEY")

if ENCRYPTION_KEY is None:
    logger.error("APP_ENCRYPTION_KEY is not set. Please set it in your environment or .env file.")
    # For development convenience, generate one if not set, but warn
    if os.getenv("APP_ENV", "development") == "development":
        generated_key = Fernet.generate_key().decode()
        logger.warning(f"Generated a new APP_ENCRYPTION_KEY for development: {generated_key}")
        logger.warning(f"Please add APP_ENCRYPTION_KEY='{generated_key}' to your .env file.")
        ENCRYPTION_KEY = generated_key
    else:
        raise ValueError("APP_ENCRYPTION_KEY environment variable is not set. Cannot perform encryption/decryption.")

try:
    f = Fernet(ENCRYPTION_KEY.encode())
except Exception as e:
    logger.error(f"Failed to initialize Fernet with provided key: {e}")
    raise ValueError("Invalid APP_ENCRYPTION_KEY. It must be a URL-safe base64-encoded 32-byte key.") from e


def encrypt_data(data: str) -> str:
    """Encrypts a string using Fernet."""
    return f.encrypt(data.encode()).decode()


def decrypt_data(encrypted_data: str) -> str:
    """Decrypts a string using Fernet."""
    return f.decrypt(encrypted_data.encode()).decode()

# Optional: Function to generate a key for initial setup
def generate_fernet_key():
    """Generates a new Fernet key."""
    return Fernet.generate_key().decode()

if __name__ == "__main__":
    # Example usage for testing
    if ENCRYPTION_KEY:
        print(f"Using encryption key (first 5 chars): {ENCRYPTION_KEY[:5]}...")

        original_data = "my_secret_gemini_api_key_123"
        encrypted = encrypt_data(original_data)
        decrypted = decrypt_data(encrypted)

        print(f"Original: {original_data}")
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
        assert original_data == decrypted
        print("Encryption/Decryption successful!")
    else:
        print("Encryption key not set, cannot run example.")
        print(f"Generated new key: {generate_fernet_key()}")
