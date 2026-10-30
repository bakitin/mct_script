# Contexto del proyecto: Caprendizaje Bot

## Objetivo
Estoy desarrollando un programa en Python que automatice la búsqueda de ofertas de contrato de aprendizaje en Caprendizaje del SENA.

El programa debe extraer las ofertas, detectar cuáles son nuevas, investigar las empresas con IA y generar correos personalizados adjuntando mi hoja de vida.

## Tecnologías
- Python para la lógica principal.
- Selenium para automatizar el navegador y extraer las ofertas.
- TXT para almacenar las ofertas y detectar duplicados.
- Gemini API para investigar empresas y redactar correos.
- Gmail API para crear borradores y enviar correos con mi hoja de vida adjunta.

No utilizar Docker ni SQLite. Quiero mantener el proyecto sencillo y ejecutarlo localmente.

## Estado actual
Ya se comprobó que Selenium puede abrir la página de inicio de sesión de Caprendizaje.
La clase inicial `CaprendizajeScraper` ya tiene el navegador, el método para abrir
el login y la espera para que el usuario inicie sesión manualmente. Todavía falta
comprobar la sesión, llegar a las ofertas e inspeccionar una oferta real.

## Plan de desarrollo por clases y pipelines

El proyecto se construirá de forma incremental. Antes de implementar una clase se
definirán sus métodos, el orden en que se ejecutan y la entrada y salida de cada
método. Solo se implementará un método o micro-paso a la vez.

### Fase 1: extracción con Selenium

Clase: `CaprendizajeScraper`

```text
__init__()
    ↓
abrir_login()
    ↓
esperar_login_manual()
    ↓
verificar_sesion()
    ↓
abrir_ofertas()
    ↓
seleccionar_oferta()
    ↓
extraer_oferta()
    ↓
cerrar()
```

Responsabilidades:

- `__init__()`: crear y conservar `self.driver`.
- `abrir_login()`: abrir la URL de inicio de sesión; la URL puede ser local
  porque solo se usa en este método.
- `esperar_login_manual()`: detener el programa mientras el usuario inicia sesión.
- `verificar_sesion()`: comprobar con elementos reales de la página que la sesión
  terminó correctamente.
- `abrir_ofertas()`: navegar hasta la sección de ofertas usando la interfaz real.
- `seleccionar_oferta()`: abrir una oferta concreta.
- `extraer_oferta()`: leer los campos publicados y devolver los datos extraídos.
- `cerrar()`: cerrar el navegador al terminar el flujo.

No se inventarán selectores. El usuario inspeccionará las etiquetas con las
herramientas del navegador y proporcionará los elementos o selectores reales.

### Fase 2: almacenamiento y deduplicación

Clase: `OfertasManager`

```text
leer_ofertas()
    ↓
normalizar_oferta()
    ↓
crear_identificador()
    ↓
buscar_existente()
    ↓
clasificar_nuevas()
    ↓
guardar_ofertas()
    ↓
actualizar_estado()
```

### Fase 3: investigación y generación

Clases: `CompanyResearcher` y `EmailGenerator`

```text
recibir_oferta_nueva()
    ↓
buscar_empresa()
    ↓
conservar_fuentes()
    ↓
preparar_datos_verificados()
    ↓
generar_asunto_y_cuerpo()
    ↓
revisar_resultado()
```

### Fase 4: Gmail

Clase: `GmailSender`

```text
cargar_credenciales()
    ↓
autenticar_oauth()
    ↓
crear_mensaje()
    ↓
adjuntar_hoja_de_vida()
    ↓
crear_borrador()
    ↓
registrar_resultado()
```

### Fase 5: orquestación

Clase o módulo: `main`

```text
extraer
    ↓
detectar_nuevas
    ↓
investigar
    ↓
generar_correo
    ↓
crear_borradores
    ↓
guardar estados
```

Cada fase comenzará únicamente cuando la anterior cumpla su criterio de
aceptación. No se implementarán Gemini ni Gmail durante la Fase 1.

## 1. Cómo trabajar con el usuario

### Reglas (las pidió explícitamente; frases textuales entre comillas)

1. **Guiar, no resolver.** "No quiero que lo hagas por mí, quiero que me guíes, me gusta programar así." Plan por pasos bien definidos; en cada paso se preparan las cosas nuevas que se van a ver (funciones, módulos, bibliotecas). El código de los archivos del proyecto lo escribe el usuario. Ejemplos genéricos con otros nombres, sí; el código final del proyecto, no.
2. **No asumir nada.** "No quiero que des por sentado nada, no creas que sé cosas que no sé, explicame todo." Todo concepto, función, módulo u operador nuevo se explica desde cero: qué es, para qué sirve, qué devuelve y qué errores da. Incluso hubo que explicar `>>>`, `date`, `raise` y "método privado".
3. **Corto.** "No me des TAAANTO texto... quiero un profesor, pero interesante, no textoooo." Bloques cortos, tablas chicas, 2 a 5 líneas por concepto más un ejemplo mínimo. Sin párrafos largos y sin repetir lo ya dicho.
4. **Problema + herramientas.** "Aparte de darme el problema, dame las herramientas para solucionarlo, no la solución tal cual." Cada observación sigue este molde: **Problema** (1 línea) → **Herramienta** (concepto + ejemplo genérico mínimo) → resuelve el usuario.
5. **Un paso a la vez.** No presentar el paso siguiente hasta que el actual pase todos sus casos.
6. **Dar un orden y un resultado esperado.** Al usuario le sirvió mucho un "Orden sugerido" (ej.: *leer → limpiar y convertir → validar con raise → guardar en self.*; dijo "es una buena forma de guiarme") y una tabla de resultados esperados por caso de prueba.
7. **Pasos chicos.** El 2026-10-20 el Paso 2 se presentó entero (7 herramientas, 1 ejemplo, 8 tareas) y el usuario respondió "no entiendo nada". Aplicar el formato de 5 partes **por micro-paso** (una sola tarea concreta a la vez), partir de un mapa simple (por ejemplo, una tabla "línea del `.env` → frase que entiende el servidor") y preguntar cada tanto qué fue lo que lo perdió. Si dice que no entiende, el paso era demasiado grande: reducirlo, no repetirlo más largo.

### Ciclo de cada vuelta (el que funcionó)

1. Presentar primero la clase que se va a construir y su responsabilidad.
2. Presentar el pipeline completo de sus métodos antes de escribirlos.
3. Explicar cada método por separado, en micro-pasos, siempre con este formato:
   **Problema → Herramientas** (cada una explicada desde cero, con ejemplo
   mínimo) **→ Ejemplo genérico de implementación** (en otro dominio, nunca el
   código final del proyecto) **→ Pipeline** (entrada y salida) **→ Tarea** con
   su "listo cuando" y una tabla pequeña de resultados esperados.
4. El usuario escribe el código del proyecto y avisa con **"Ya"**.
5. El asistente **lee los archivos del disco y ejecuta los casos de verdad** (no adivinar ni decir "debería funcionar") y responde con una tabla pasa/falla. Ver §12.
6. Por cada fallo: Problema → Herramienta → ejemplo genérico. Si el problema es un traceback, enseñar a leerlo (de abajo hacia arriba).
7. Repetir hasta que todo pase. Reconocer lo que ya está bien (el usuario lo valora) y recién entonces pasar al paso siguiente.

### Otros acuerdos

- En las sesiones anteriores **no se editó ningún archivo del proyecto del usuario**: solo se leyeron y se probaron con scripts fuera del repo. Mantener eso.
- A partir de ahora, cuando el usuario lo solicite explícitamente, sí se puede
  actualizar `contexto.md` para conservar sus preferencias de trabajo.
- La guía debe priorizar clases con responsabilidades claras, una lista ordenada
  de métodos y un pipeline visible. No entregar una clase completa de una vez:
  preparar el diseño y avanzar método por método.
- Las decisiones de la §2 están tomadas. No volver a proponer simulación, confirmación ni registro de lo borrado.
- Informar con fidelidad: si algo falla o no se pudo probar, decirlo.
- Sin commits ni cambios de git salvo que el usuario los pida.

---


Contexto del proyecto: bot de ofertas de Caprendizaje
1. Objetivo general
Quiero desarrollar un proyecto pequeño, práctico y rápido en Python para automatizar parte de mi búsqueda de patrocinio/contrato de aprendizaje mediante la plataforma Caprendizaje del SENA.

El programa debe:
1. Abrir Caprendizaje y acceder a la plataforma mediante Selenium.
2. Capturar las ofertas disponibles y extraer, como mínimo, el nombre de la empresa y el correo electrónico que aparezca publicado en la oferta.
3. Extraer también, cuando esté disponible, el nombre del cargo/perfil, la URL o identificador original de la oferta, su descripción y otros datos útiles.
4. Guardar las ofertas en un archivo de texto .txt.
5. Comparar cada ejecución con el archivo existente para detectar ofertas nuevas y evitar duplicados.
6. Para las ofertas nuevas, investigar la empresa con ayuda de una búsqueda web y la Gemini API.
7. Generar un correo de postulación personalizado para la empresa y la oferta, basado en información verificable y en mi perfil real.
8. Usar la Gmail API para crear un borrador o enviar el correo con mi hoja de vida en PDF adjunta.
9. Registrar en el TXT el estado de cada oferta y si se ha enviado o no un correo, evitando envíos repetidos.
La finalidad es ayudarme a identificar oportunidades y preparar postulaciones. No quiero crear una plataforma web ni una aplicación grande.
2. Tecnologías elegidas
- Python 3.12 o una versión estable compatible: lenguaje principal.
- Selenium 4: automatización del navegador, inicio de sesión y extracción de ofertas.
- Archivo TXT: almacenamiento persistente de las ofertas. No quiero SQLite ni otra base de datos.
- Gemini API: investigación asistida y generación de correos personalizados. La investigación web debe apoyarse en búsqueda real o en una función de búsqueda disponible, no en suposiciones del modelo.
- Gmail API: creación de borradores y/o envío de correos, incluida la hoja de vida adjunta.
- python-dotenv: lectura local de variables de entorno desde .env.
- requirements.txt: dependencias del proyecto.
Docker queda descartado. SQLite queda descartado. La prioridad es la simplicidad: ejecutar el programa localmente.
3. Alcance funcional
A. Extracción con Selenium
- Abrir la web oficial de Caprendizaje y acceder a las ofertas disponibles con mi cuenta.
- No asumir de antemano cómo están construidas las páginas: primero inspeccionar una oferta real y sus elementos HTML.
- Extraer los campos que realmente existan en la página.
- Campos mínimos:
  - Identificador propio del registro.
  - Identificador original de la oferta o URL, si existe.
  - Empresa.
  - Correo electrónico publicado en la oferta, si existe.
  - Cargo, perfil o nombre de la vacante, si existe.
  - Descripción o requisitos disponibles.
  - URL de la oferta, si existe.
  - Fecha de captura.
  - Estado del proceso.
  - Estado del correo.
- Si un dato no aparece en la oferta, guardarlo como No publicado o dejarlo vacío de forma consistente. No inventar información.
- Si aparece CAPTCHA, MFA u otro control de seguridad, detenerse y solicitar intervención manual. No intentar eludir esos controles.
- Manejar de forma razonable errores de carga, sesión expirada y cambios en la página.
B. Archivo TXT y detección de novedades
- El archivo principal de almacenamiento será data/ofertas.txt.
- Debe ser legible por una persona y conservar los registros entre ejecuciones.
- Cada oferta se almacenará como un bloque estructurado con separadores claros, o con otro formato de texto robusto que siga siendo un archivo .txt.
- Ejemplo ilustrativo (los datos son ficticios):
========================================
ID: CAP-0001
ID_ORIGINAL: 12345
EMPRESA: Empresa Ejemplo S.A.S.
CARGO: Aprendiz de desarrollo de software
CORREO: seleccion@empresa.com
URL: https://ejemplo.com/oferta/12345
FECHA_CAPTURA: 2026-10-27
ESTADO: NUEVA
CORREO_ENVIADO: NO
========================================
- El identificador propio (CAP-0001, CAP-0002, etc.) debe permanecer estable, no regenerarse en cada ejecución.
- Para detectar duplicados, priorizar el identificador original de la plataforma; si no existe, usar una URL estable o una huella determinista de campos normalizados.
- No utilizar únicamente el nombre de la empresa para detectar duplicados: una empresa puede publicar varias ofertas.
- La primera ejecución debe registrar las ofertas que encuentre. En ejecuciones posteriores, solo se deben marcar como nuevas las que no estén guardadas.
- Debe ser seguro ejecutar el programa más de una vez sin duplicar registros ni volver a enviar automáticamente correos ya enviados.
- Aunque el almacenamiento sea TXT, separar la lógica de lectura/escritura en un módulo propio. Considerar escritura atómica o una estrategia que reduzca el riesgo de corromper el archivo si el proceso falla.
C. Investigación de la empresa y generación de correo
Para cada oferta nueva:
1. Buscar información pública y actual de la empresa (por ejemplo, sitio web oficial, actividad, productos o servicios y canales de contacto publicados).
2. Enviar al modelo de Gemini el contenido de la oferta, la información encontrada y mi perfil real.
3. Solicitar un correo breve, profesional y específico para esa empresa y esa vacante.
4. Solicitar un asunto y un cuerpo de correo listos para revisar.
5. Conservar las fuentes consultadas o enlaces que respalden la información utilizada, si la herramienta de búsqueda lo permite.
Reglas para la IA:
- No inventar datos de la empresa, requisitos, contactos, logros, experiencia ni habilidades del candidato.
- Distinguir hechos verificados de datos desconocidos.
- Usar solamente información real de mi hoja de vida y del perfil que yo proporcione.
- No fabricar direcciones de correo. Para la postulación, usar el correo publicado en la oferta. Si no aparece, marcar la oferta como SIN_CORREO y no enviar un mensaje a un destinatario supuesto.
- Si la búsqueda encuentra un canal oficial alternativo, presentarlo como una opción para revisar; no asumir que sirve para postularse.
- Evitar textos genéricos llenos de elogios vacíos. La personalización debe relacionar requisitos de la vacante con habilidades reales del perfil.
D. Envío mediante Gmail API
- Usar el flujo oficial de autenticación de Google (OAuth); no guardar la contraseña de Gmail en el código.
- Mantener fuera del repositorio los archivos secretos, los tokens y las credenciales de API.
- Adjuntar el archivo PDF de la hoja de vida desde documents/hoja_de_vida.pdf (ruta provisional que debe ajustarse si el archivo tiene otro nombre).
- Primera fase: crear borradores para revisión humana o realizar pruebas controladas.
- Solo activar el envío automático después de validar extracción, destinatario, texto generado, adjunto y prevención de duplicados.
- Antes de enviar, comprobar que el correo existe en la oferta y que la oferta sigue siendo pertinente.
- Guardar un estado de envío y, si es posible, fecha y resultado para no volver a enviar el mismo correo por accidente.
- Diferenciar estados como NUEVA, SIN_CORREO, BORRADOR_CREADO, ENVIADO y ERROR.
- No mandar correos masivos indiscriminadamente ni ignorar límites o políticas de la plataforma o del proveedor de correo.
4. Estructura de carpetas propuesta
caprendizaje-bot/
├── main.py
├── config.py
├── scraper.py
├── ofertas_manager.py
├── company_researcher.py
├── email_generator.py
├── gmail_sender.py
├── data/
│   └── ofertas.txt
├── documents/
│   └── hoja_de_vida.pdf
├── credentials/
│   └── gmail_token.json
├── .env
├── .gitignore
└── requirements.txt
Responsabilidades sugeridas:
- main.py: orquestar el proceso y manejar el flujo general.
- config.py: leer y validar la configuración.
- scraper.py: abrir Caprendizaje y extraer las ofertas con Selenium; no debe enviar correos ni escribir directamente toda la lógica del archivo.
- ofertas_manager.py: leer, comparar, identificar y guardar registros en el TXT.
- company_researcher.py: buscar información pública de la empresa y devolver información con sus fuentes.
- email_generator.py: solicitar a Gemini el asunto y el cuerpo del correo, con instrucciones y datos estructurados.
- gmail_sender.py: autenticar con Gmail, crear borradores/enviar mensajes y adjuntar el CV.
Se puede ajustar esta estructura si hay una razón técnica concreta, pero evitar una arquitectura innecesariamente compleja.
5. Configuración y seguridad
- Crear un .env para valores sensibles/configurables, por ejemplo GEMINI_API_KEY y rutas de archivos.
- No subir .env, tokens OAuth, credenciales descargadas de Google ni datos personales a GitHub.
- Incluir en .gitignore como mínimo .env, credentials/, tokens, logs con información personal y cualquier archivo temporal sensible.
- No almacenar la contraseña de Caprendizaje en texto plano si se puede evitar. Preferir introducirla manualmente o utilizar un mecanismo de sesión local seguro y apropiado.
- Los datos de acceso de la plataforma, el CV y la lista de empresas son información privada.
6. Orden de desarrollo y pruebas
Construir un MVP incremental. No implementar todo de una vez.
Fase 1: inspeccionar y extraer
- Confirmar la URL real de acceso y la forma en que se muestran las ofertas.
- Automatizar el acceso con Selenium.
- Inspeccionar una oferta y extraer correctamente los campos disponibles.
- Guardar temporalmente los datos extraídos y comprobarlos manualmente.
Criterio de aceptación: se puede extraer una oferta real con empresa, correo si está publicado, cargo y URL/ID si existen.
Fase 2: almacenamiento TXT y deduplicación
- Implementar lectura y escritura de los registros.
- Ejecutar dos veces el proceso sobre el mismo conjunto de ofertas.
- Verificar que la segunda ejecución no crea duplicados ni cambia los IDs ya asignados.
- Probar ofertas sin correo, sin URL y con campos incompletos.
Criterio de aceptación: la primera ejecución registra los datos; la segunda solo incorpora ofertas realmente nuevas.
Fase 3: investigación y Gemini
- Investigar una empresa de prueba a partir de una fuente oficial y fuentes adicionales cuando haga falta.
- Generar un correo personalizado para una oferta real.
- Revisar manualmente la exactitud y el tono del mensaje.
Criterio de aceptación: el correo incluye hechos respaldados y no atribuye habilidades o experiencia inexistentes.
Fase 4: Gmail API y hoja de vida
- Configurar un proyecto de Google Cloud y OAuth de Gmail según los requisitos vigentes de la API.
- Crear un borrador de prueba.
- Confirmar que el destinatario, asunto, cuerpo y PDF adjunto son correctos.
- Añadir control para no duplicar envíos.
Criterio de aceptación: se crea un borrador válido con el archivo correcto y queda registrado el estado.
Fase 5: flujo integrado
- Conectar extracción, deduplicación, investigación, generación y creación de borradores.
- Procesar varias ofertas de forma controlada.
- Agregar manejo de errores y logs sin exponer secretos.
- Considerar la programación periódica solamente después de que las ejecuciones manuales sean fiables.
7. Preferencias sobre cómo quiero que me guíe la IA
Estoy estudiando Ingeniería de Software y aprendiendo a programar. Quiero entender y construir el proyecto, no limitarme a copiar y pegar código.
- Guíame paso a paso y explica brevemente la razón de cada decisión técnica.
- Prioriza ejemplos concretos y explicaciones claras en español.
- Prefiero una solución orientada a objetos cuando realmente aporte claridad, pero no fuerces clases donde unas funciones sean suficientes.
- No me entregues todo el proyecto completo de golpe, salvo que yo lo solicite explícitamente.
- En cada etapa, define una meta pequeña, explícame qué archivo o componente vamos a trabajar, ayúdame a implementarlo y propón una prueba para verificarlo.
- Cuando haya un error, ayúdame a entender la causa y cómo diagnosticarlo antes de reemplazar todo el código.
- Evita añadir frameworks, dependencias o infraestructura innecesarios.
- Sé directo si una decisión añade complejidad sin aportar valor.
- No inventes selectores HTML, endpoints, campos de Caprendizaje ni resultados de APIs. Pide una inspección de la página o trabaja con el HTML/screenshot real cuando sea necesario.
- Usa versiones y documentación vigentes cuando la implementación dependa de detalles actuales de Selenium, Gemini o Gmail API.
8. Suposiciones pendientes de comprobar
- La estructura exacta del sitio de Caprendizaje y sus mecanismos de inicio de sesión aún no han sido inspeccionados.
- Todavía no se conoce si el correo, la URL o un ID único están disponibles para todas las ofertas.
- La forma en que Caprendizaje permite mostrar o paginar las ofertas debe verificarse con una sesión real.
- La cuenta de Gemini y sus límites/precios deben comprobarse antes de elegir el modelo concreto.
- Gmail API requiere configurar OAuth y los permisos necesarios; no asumir que basta con introducir una API key.
- La ubicación real de la hoja de vida PDF y el contenido definitivo del CV están pendientes.
- El formato TXT es una decisión deliberada de simplicidad. Si más adelante crece el volumen o el formato se vuelve difícil de mantener, se puede proponer una alternativa, pero no cambiarla sin explicar la razón y consultar primero.
9. Primera tarea solicitada a la IA
Empieza por la Fase 1: ayúdame a comprobar cómo acceder a Caprendizaje con Selenium y cómo inspeccionar una oferta real para identificar los selectores y campos disponibles.

No empieces todavía con Gemini ni Gmail. Primero debemos tener una extracción fiable de una oferta y entender su HTML real. Explícame el siguiente paso concreto, qué debo ejecutar y qué resultado debo observar. No supongas que ya conocemos el DOM de Caprendizaje.