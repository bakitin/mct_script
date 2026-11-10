from smtplib import SMTP_SSL
from email.message import EmailMessage
from pathlib import Path
import json


class EmailService:
    def __init__(self, smtp_host, smtp_port):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.ruta_hoja_de_vida = Path("documents/CV.pdf")

    def conectar_smtp(self, cuenta_correo, contrasena_aplicacion):
        self.smtp_connection = SMTP_SSL(self.smtp_host, self.smtp_port)
        self.smtp_connection.login(cuenta_correo, contrasena_aplicacion)

    def _limpiar_resultados_gemini(self, resultados_gemini):
        resultados_limpios = []

        for resultado in resultados_gemini:
            try:
                datos_correo = json.loads(resultado)
                resultados_limpios.append(datos_correo)
            except json.JSONDecodeError as e:
                print(f"[Correo] Error al decodificar un resultado: {e}")
        return resultados_limpios

    def crear_mensajes(self, resultados_gemini):
        resultados_limpios = self._limpiar_resultados_gemini(resultados_gemini)

        for datos_correo in resultados_limpios:
            mensaje = EmailMessage()

            mensaje["From"] = "segura.santiago308@gmail.com"
            mensaje["To"] = datos_correo.get("correo_destino")
            mensaje["Subject"] = datos_correo.get("asunto")
            mensaje.set_content(datos_correo.get("cuerpo"))
            mensaje.add_attachment(
                self.ruta_hoja_de_vida.read_bytes(),
                maintype="application",
                subtype="pdf",
                filename=self.ruta_hoja_de_vida.name,
            )
            
            yield mensaje

    def enviar_correo(self, mensaje):
        self.smtp_connection.send_message(mensaje)

    def desconectar_smtp(self):
        self.smtp_connection.quit()