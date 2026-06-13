from mongoengine import Document, EmailField, StringField
from .cripto import cipher 

class Usuario(Document):
    correo = EmailField(
        required=True,
        unique=True
    )

    password = StringField(
        required=True
    )

    def set_password(self, raw_password: str):
        self.password = cipher.encrypt(raw_password.encode()).decode()

    def check_password(self, raw_password: str) -> bool:
        try:
            decrypted = cipher.decrypt(self.password.encode()).decode()
            return decrypted == raw_password
        except Exception:
            return False

    meta = {
        'collection': 'usuarios'
    }