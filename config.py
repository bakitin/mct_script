import os
from dotenv import load_dotenv

load_dotenv()


class Config():
    def __init__(self):
        self.numero_documento = os.getenv("CC")
        self.password=os.getenv("PASSWORD")
        self.contrasena_caprendizaje = self.password
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.cuenta_correo = os.getenv("CORREO_CUENTA")
        self.contrasena_aplicacion = os.getenv("CORREO_CONTRA")