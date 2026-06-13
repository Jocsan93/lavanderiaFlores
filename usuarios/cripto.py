import os
from cryptography.fernet import Fernet

FERNET_KEY = os.environ.get("FERNET_KEY").encode()
cipher = Fernet(FERNET_KEY)