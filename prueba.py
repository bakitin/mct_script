import json
from pathlib import Path

from email.message import EmailMessage

from config import Config
from email_service import EmailService


def main():
    print("[Prueba] Iniciando comprobaciones básicas.")

    ruta_hoja_de_vida = Path("documents/CV.pdf")
    if not ruta_hoja_de_vida.is_file():
        raise FileNotFoundError(
            f"No se encontró la hoja de vida: {ruta_hoja_de_vida}"
        )
    print("[Prueba] CV.pdf encontrado.")

    resultado_gemini = [
        json.dumps(
            {
                "empresa": "Empresa de prueba",
                "correo_destino": "destinatario-de-prueba@example.com",
                "estado_correo": "LISTO_PARA_REVISION",
                "asunto": (
                    "Hoja de vida - Tecnólogo ADSO SENA - "
                    "Contrato de aprendizaje"
                ),
                "cuerpo": (
                    "Me postulo para realizar mi etapa productiva "
                    "mediante contrato de aprendizaje del SENA."
                ),
                "advertencias": [],
            }
        )
    ]

    servicio_correo = EmailService("smtp.gmail.com", 465)
    mensajes = list(servicio_correo.crear_mensajes(resultado_gemini))

    if len(mensajes) != 1:
        raise RuntimeError("La prueba debía crear exactamente un mensaje.")

    mensaje = mensajes[0]
    if not isinstance(mensaje, EmailMessage):
        raise TypeError("El resultado no es un objeto EmailMessage.")

    if "Contrato de aprendizaje" not in mensaje["Subject"]:
        raise AssertionError("El asunto no coincide.")

    cuerpo_mensaje = mensaje.get_body(
        preferencelist=("plain",)
    ).get_content()
    if "etapa productiva" not in cuerpo_mensaje:
        raise AssertionError("El cuerpo no menciona la etapa productiva.")

    adjuntos = list(mensaje.iter_attachments())
    if len(adjuntos) != 1:
        raise AssertionError("El mensaje no tiene exactamente un adjunto.")

    adjunto = adjuntos[0]
    if adjunto.get_filename() != "CV.pdf":
        raise AssertionError("El adjunto no se llama CV.pdf.")

    if adjunto.get_content_type() != "application/pdf":
        raise AssertionError("El adjunto no tiene tipo PDF.")

    configuracion = Config()
    if not configuracion.cuenta_correo:
        raise RuntimeError("No hay una cuenta de correo configurada.")
    if not configuracion.contrasena_aplicacion:
        raise RuntimeError("No hay una contraseña de aplicación configurada.")

    mensaje.replace_header("To", configuracion.cuenta_correo)
    if mensaje["To"] != configuracion.cuenta_correo:
        raise AssertionError("El destinatario no coincide con la cuenta configurada.")
    print("[Prueba] EmailMessage creado correctamente.")
    print("[Prueba] Destinatario, asunto y cuerpo verificados.")
    print("[Prueba] CV.pdf adjuntado correctamente.")
    print("[Prueba] Conectando con el servidor SMTP.")
    servicio_correo.conectar_smtp(
        configuracion.cuenta_correo,
        configuracion.contrasena_aplicacion,
    )

    try:
        servicio_correo.enviar_correo(mensaje)
        print(
            "[Prueba] Correo enviado correctamente a la cuenta configurada."
        )
    finally:
        servicio_correo.desconectar_smtp()
        print("[Prueba] Conexión SMTP cerrada.")

    print("[Prueba] Todas las comprobaciones y el envío finalizaron correctamente.")


if __name__ == "__main__":
    main()
