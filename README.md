# Caprendizaje Bot

Bot local en Python que:

1. Extrae ofertas de contrato de aprendizaje desde Caprendizaje.
2. Detecta y guarda únicamente ofertas nuevas.
3. Investiga la empresa mediante búsqueda web gratuita.
4. Genera una postulación personalizada con Gemini.
5. Envía el correo con `CV.pdf` adjunto mediante SMTP.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configura las variables de `.env` usando [.env.example](.env.example). No
compartas `.env`, contraseñas ni claves API.

## Ejecución

La prueba segura valida el mensaje y el adjunto sin enviar correo:

```bash
python prueba.py
```

Para ejecutar el flujo completo:

```bash
python main.py
```

`main.py` consulta Caprendizaje y puede enviar correos reales. Verifica los
destinatarios antes de ejecutarlo.
