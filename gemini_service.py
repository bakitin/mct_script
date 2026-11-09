import json
import time
from google import genai
from google.genai import types
from ddgs import DDGS



class GeminiService:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model
        self.client = genai.Client(api_key=self.api_key)



    def ciclonador(self, ofertas):
        resultados = []
        for i, oferta in enumerate(ofertas):


            print(f"Procesando oferta {i+1} de {len(ofertas)}...")
            print("*----------------------------------------------*")
            respuesta_gemini = self._generar_correo(oferta)
            resultados.append(respuesta_gemini)
            print(
                "⏳ Esperando 2 segundos para proteger el límite de RPM de la"
                " API..."
            )
            time.sleep(2)
        return resultados
            

    def _generar_correo(self, oferta):
        prompt = self._construir_prompt(oferta)

        modelos_disponibles = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.6-flash"]
        for modelo in modelos_disponibles:
            try:
                print(f"🤖 Intentando conectar con: {modelo}...")
                respuesta = self.client.models.generate_content(
                    model=modelo,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                    ),
                )
                if not respuesta.text:
                    raise RuntimeError("Gemini devolvió una respuesta vacía para una oferta.")

                try:
                    resultado = respuesta.text
                    return resultado
                except json.JSONDecodeError as error:
                    raise RuntimeError("Gemini no devolvió un JSON válido para una oferta.") from error
                
            except Exception as e:
                # Si el error es 503 (saturación), intentamos con el siguiente modelo
                if "503" in str(e):
                    print(f"⚠️ {modelo} saturado (Error 503). Cambiando a modelo de respaldo...")
                    time.sleep(2) # Pequeña pausa antes de intentar el siguiente
                    continue
                else:
                    # Si es un error tuyo de código o un 429, que sí detenga el programa
                    raise e

    def _investigar_empresa(self,nombre_empresa, ciudad):
        print(f"🔍 Buscando información en la web sobre: {nombre_empresa}...")
        consulta = f"{nombre_empresa} {ciudad} Colombia a que se dedica"
        
        texto_recolectado = []
        # Lista de motores de respaldo (el primero es el predeterminado)
        motores = ["auto", "duckduckgo", "google", "bing", "yahoo"]
        
        for motor in motores:
            try:
                # Ponemos un pequeño timeout por si el servidor se queda pensando para bloquearnos
                ddgs = DDGS(timeout=10) 
                resultados = ddgs.text(consulta, max_results=3, backend=motor)
                
                if resultados:
                    for res in resultados:
                        texto_recolectado.append(f"- Fuente: {res.get('href', 'Sin enlace')} Resumen: {res.get('body', 'Sin resumen')}")
                    
                    # Si funcionó y trajo datos, devolvemos la lista y rompemos el ciclo
                    return texto_recolectado
                    
            except Exception as e:
                # Si este motor falla o nos bloquea, simplemente intentamos con el siguiente
                continue
                
        # Si llega hasta aquí, significa que TODOS los motores fallaron o bloquearon la IP
        print("⚠️ Todos los motores de búsqueda bloquearon la petición.")
        return ["No se encontró información en internet."]


    def _construir_prompt(self, oferta):
        investigacion = self._investigar_empresa(oferta.get("Empresa", ""),"Cali")
        prompt = f"""Actúa como redactor profesional de correos de postulación.

                    Necesito preparar un correo personalizado para una oferta de contrato de aprendizaje.

                    REGLAS OBLIGATORIAS:

                    1. Usa únicamente la información de la oferta, la investigación
                    proporcionada y los datos reales del candidato.
                    2. No realices búsquedas web ni inventes información sobre la empresa.
                    3. No inventes servicios, productos, ubicación, contactos,
                    experiencia ni habilidades.
                    4. No fabriques ni adivines una dirección de correo.
                    5. El correo de destino debe ser exactamente el correo publicado
                    en la oferta.
                    6. Si la oferta no contiene correo, indica "SIN_CORREO" y no
                    prepares un envío.
                    7. No afirmes que el candidato tiene una habilidad o experiencia
                    si no aparece en los datos recibidos.
                    8. Relaciona los requisitos de la oferta con el perfil real del
                    candidato, sin exagerar.
                    9. El texto debe ser breve, profesional, específico y natural.
                    Evita elogios genéricos.
                    10. No envíes correos ni realices ninguna acción externa. Solo
                    devuelve el resultado para revisión humana.
                    11. Presenta la postulación explícitamente para realizar la
                    etapa productiva del Tecnólogo en Análisis y Desarrollo de
                    Software mediante un contrato de aprendizaje del SENA.
                    No la presentes como una vacante laboral ordinaria ni como
                    una contratación profesional independiente.
                    12. Usa exactamente este asunto, sin modificarlo:
                    "Hoja de vida - Tecnólogo ADSO SENA - Contrato de aprendizaje"

                    DATOS DE LA OFERTA:

                    Empresa:
                    {oferta.get("Empresa","")}

                    Correo publicado:
                    {oferta.get("Correo electrónico","")}

                    Ciudad:
                    {oferta.get("Ciudad","")}

                    Perfil solicitado:
                    {oferta.get("Perfil","")}

                    Funciones:
                    {oferta.get("Funciones a desarrollar","")}

                    Datos reales del candidato:
                    Soy Santiago Segura, desarrollador full-stack de Cali, Colombia. Estudio Ingeniería de Software en el Politécnico Grancolombiano y el Tecnólogo en Análisis y Desarrollo de Software en el SENA, ambos en curso, y soy Técnico en Sistemas del SENA. Tengo más de dos años de experiencia real con clientes, desarrollando y desplegando aplicaciones web de principio a fin. Trabajo principalmente con Python (FastAPI), PostgreSQL y JavaScript, y también manejo infraestructura: dominios, DNS y correo corporativo. Entre mis proyectos están los sitios de Imposursas y Santana Reformas, el backend de una tienda en línea con pagos, un sistema de gestión para una peluquería con varias sucursales y una aplicación de voz P2P que sigo desarrollando. Busco un lugar donde pueda aportar con experiencia real y seguir creciendo con un equipo que me dé feedback.

                    INVESTIGACION PROPORCIONADA:
                    {investigacion}
                    
                    TAREA:

                    Redacta únicamente el correo de postulación usando la oferta,
                    la investigación proporcionada y el perfil del candidato.
                    Indica claramente en el cuerpo que el candidato busca
                    realizar su etapa productiva mediante un contrato de
                    aprendizaje del SENA.

                    RESPONDE ÚNICAMENTE con un JSON válido usando exactamente esta estructura:

                    {{
                    "empresa": "",
                    "correo_destino": "",
                    "estado_correo": "LISTO_PARA_REVISION",
                    "asunto": "Hoja de vida - Tecnólogo ADSO SENA - Contrato de aprendizaje",
                    "cuerpo": "",
                    "advertencias": []
                    }}

                    REGLAS DEL JSON:

                    - No agregues texto fuera del JSON.
                    - Si no encuentras información confiable, usa listas vacías y explica la limitación en "advertencias".
                    - Si no existe correo publicado, usa:
                    "correo_destino": ""
                    "estado_correo": "SIN_CORREO"
                    - El cuerpo debe estar listo para revisión, no para envío automático.
                    - No incluyas investigación, fuentes ni explicaciones fuera de
                    los campos definidos en el JSON."""
        return prompt
        
