from mongoengine import Document, EmailField, StringField, DateTimeField
from datetime import datetime, timedelta
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

class PasswordResetCode(Document):
    correo = EmailField(required=True)
    codigo = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'password_reset_codes',
        'indexes': [
            {
                'fields': ['created_at'],
                'expireAfterSeconds': 600  # 10 minutos
            }
        ]
    }

    def set_codigo(self, raw_code: str):
        self.codigo = cipher.encrypt(raw_code.encode()).decode()

    def check_codigo(self, raw_code: str) -> bool:
        try:
            decrypted = cipher.decrypt(self.codigo.encode()).decode()
            return decrypted == raw_code
        except Exception:
            return False    