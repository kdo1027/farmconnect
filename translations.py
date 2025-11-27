"""
Translation strings for FarmConnect
Supports English and Spanish
"""

TRANSLATIONS = {
    'en': {
        # Welcome messages
        'welcome': """🌾 *Welcome to FarmConnect!* 🌾

We connect agricultural workers with farm employers.

Please select your role:
1️⃣ I'm looking for farm work (Farmer/Laborer)
2️⃣ I'm hiring workers (Farm Owner)

Reply with 1 or 2""",

        'select_role': 'Please reply with 1 (for Farmer) or 2 (for Farm Owner)',

        # Registration - Farmer
        'farmer_welcome': """✅ Great! Let's get you registered.

📝 *Step 1 of 3: Personal Information*

What's your full name?""",

        'farmer_location_prompt': """📍 *Step 2 of 3: Location*

What's your location? (City or area where you're looking for work)""",

        'farmer_id_prompt': """📸 *Step 3 of 3: ID Verification*

Please upload a photo of your ID card or driver's license.

This helps us keep FarmConnect safe for everyone.""",

        'farmer_id_no_photo': "Please send a photo of your ID card.",

        'farmer_id_received': """✅ ID received! Thank you.

Now let's set up your job preferences to find the best matches.

🛠 *Work Type Preferences*
What type of farm work are you interested in? (Select all that apply)

1️⃣ Harvesting
2️⃣ Planting
3️⃣ Irrigation
4️⃣ Livestock care
5️⃣ General labor
6️⃣ All types of work

Reply with numbers separated by commas (e.g., 1,2,3) or just one number:""",

        # Work type options
        'work_type_harvesting': 'Harvesting',
        'work_type_planting': 'Planting',
        'work_type_irrigation': 'Irrigation',
        'work_type_livestock': 'Livestock care',
        'work_type_general': 'General labor',
        'work_type_all': 'All types of work',

        # Distance preferences
        'distance_prompt': """📍 *Work Location Preference*

How far are you willing to travel for work?

1️⃣ Up to 10 miles
2️⃣ Up to 25 miles
3️⃣ Up to 50 miles
4️⃣ Any distance

Reply with 1, 2, 3, or 4:""",

        # Hours preferences
        'hours_prompt': """⏰ *Working Hours Preference*

What's your preferred work schedule?

1️⃣ Full-time (40+ hours/week)
2️⃣ Part-time (20-40 hours/week)
3️⃣ Flexible (open to both full-time and part-time)

Reply with 1, 2, or 3:""",

        # Farmer menu
        'farmer_menu': """🌾 *Farmer Menu*

1️⃣ Browse available jobs
2️⃣ Update my preferences
3️⃣ View my job applications
4️⃣ Chat with farm owner
5️⃣ Help

Reply with the number of your choice""",

        # Owner menu
        'owner_menu': """🏡 *Farm Owner Menu*

1️⃣ Post a new job
2️⃣ View my job postings
3️⃣ View applicants
4️⃣ Chat with applicants
5️⃣ Help

Reply with the number of your choice""",

        # Job recommendations
        'profile_complete': '✅ *Profile Complete!*',
        'found_jobs': 'We found {count} job match(es) for you!\n(Sorted by highest pay)',
        'no_jobs': "No job matches found right now. We'll notify you when new jobs matching your preferences are posted.",
        'select_job': '*Select a job to view details and apply:*\n\nReply with the job number (1-{max}) or type \'menu\' to return to main menu.',

        # Application
        'application_submitted': '✅ *Application Submitted!*',
        'owner_notified': 'The farm owner has been notified and will contact you soon.',

        # Help
        'help': """❓ *FarmConnect Help*

• Type 'menu' anytime to return to main menu
• Type 'help' to see this message

For support, contact: support@farmconnect.com""",

        # Common phrases
        'per_hour': '/hour',
        'per_day': '/day',
        'per_task': '/task',
        'workers_needed': 'workers needed',
        'or_type_menu': "or type 'menu'",
    },

    'es': {
        # Welcome messages
        'welcome': """🌾 *¡Bienvenido a FarmConnect!* 🌾

Conectamos trabajadores agrícolas con empleadores de granjas.

Por favor seleccione su función:
1️⃣ Busco trabajo agrícola (Trabajador/Jornalero)
2️⃣ Contrato trabajadores (Dueño de Granja)

Responda con 1 o 2""",

        'select_role': 'Por favor responda con 1 (Trabajador) o 2 (Dueño de Granja)',

        # Registration - Farmer
        'farmer_welcome': """✅ ¡Excelente! Vamos a registrarlo.

📝 *Paso 1 de 3: Información Personal*

¿Cuál es su nombre completo?""",

        'farmer_location_prompt': """📍 *Paso 2 de 3: Ubicación*

¿Cuál es su ubicación? (Ciudad o área donde busca trabajo)""",

        'farmer_id_prompt': """📸 *Paso 3 de 3: Verificación de Identidad*

Por favor suba una foto de su identificación o licencia de conducir.

Esto nos ayuda a mantener FarmConnect seguro para todos.""",

        'farmer_id_no_photo': "Por favor envíe una foto de su identificación.",

        'farmer_id_received': """✅ ¡Identificación recibida! Gracias.

Ahora configuremos sus preferencias de trabajo para encontrar las mejores opciones.

🛠 *Preferencias de Tipo de Trabajo*
¿Qué tipo de trabajo agrícola le interesa? (Seleccione todas las opciones)

1️⃣ Cosecha
2️⃣ Siembra
3️⃣ Irrigación/Riego
4️⃣ Cuidado de animales
5️⃣ Trabajo general
6️⃣ Todo tipo de trabajo

Responda con números separados por comas (ej: 1,2,3) o solo un número:""",

        # Work type options
        'work_type_harvesting': 'Cosecha',
        'work_type_planting': 'Siembra',
        'work_type_irrigation': 'Irrigación',
        'work_type_livestock': 'Cuidado de animales',
        'work_type_general': 'Trabajo general',
        'work_type_all': 'Todo tipo de trabajo',

        # Distance preferences
        'distance_prompt': """📍 *Preferencia de Ubicación de Trabajo*

¿Qué tan lejos está dispuesto a viajar para trabajar?

1️⃣ Hasta 10 millas
2️⃣ Hasta 25 millas
3️⃣ Hasta 50 millas
4️⃣ Cualquier distancia

Responda con 1, 2, 3, o 4:""",

        # Hours preferences
        'hours_prompt': """⏰ *Preferencia de Horario de Trabajo*

¿Cuál es su horario de trabajo preferido?

1️⃣ Tiempo completo (40+ horas/semana)
2️⃣ Medio tiempo (20-40 horas/semana)
3️⃣ Flexible (tiempo completo o medio tiempo)

Responda con 1, 2, o 3:""",

        # Farmer menu
        'farmer_menu': """🌾 *Menú de Trabajador*

1️⃣ Ver trabajos disponibles
2️⃣ Actualizar mis preferencias
3️⃣ Ver mis solicitudes de trabajo
4️⃣ Chat con dueño de granja
5️⃣ Ayuda

Responda con el número de su elección""",

        # Owner menu
        'owner_menu': """🏡 *Menú de Dueño de Granja*

1️⃣ Publicar un nuevo trabajo
2️⃣ Ver mis publicaciones de trabajo
3️⃣ Ver solicitantes
4️⃣ Chat con solicitantes
5️⃣ Ayuda

Responda con el número de su elección""",

        # Job recommendations
        'profile_complete': '✅ *¡Perfil Completo!*',
        'found_jobs': '¡Encontramos {count} trabajo(s) que coinciden para usted!\n(Ordenados por mejor salario)',
        'no_jobs': "No se encontraron trabajos en este momento. Le notificaremos cuando haya nuevos trabajos que coincidan con sus preferencias.",
        'select_job': '*Seleccione un trabajo para ver detalles y aplicar:*\n\nResponda con el número del trabajo (1-{max}) o escriba \'menu\' para volver al menú principal.',

        # Application
        'application_submitted': '✅ *¡Solicitud Enviada!*',
        'owner_notified': 'El dueño de la granja ha sido notificado y se comunicará con usted pronto.',

        # Help
        'help': """❓ *Ayuda de FarmConnect*

• Escriba 'menu' en cualquier momento para volver al menú principal
• Escriba 'ayuda' para ver este mensaje

Para soporte, contacte: support@farmconnect.com""",

        # Common phrases
        'per_hour': '/hora',
        'per_day': '/día',
        'per_task': '/tarea',
        'workers_needed': 'trabajadores necesitados',
        'or_type_menu': "o escriba 'menu'",
    }
}


def get_text(key: str, lang: str = 'en', **kwargs) -> str:
    """
    Get translated text for a given key

    Args:
        key: Translation key
        lang: Language code ('en' or 'es')
        **kwargs: Format arguments for string formatting

    Returns:
        Translated text with formatting applied
    """
    if lang not in TRANSLATIONS:
        lang = 'en'  # Default to English

    text = TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS['en'].get(key, key))

    # Apply formatting if kwargs provided
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass  # If format key doesn't exist, return unformatted

    return text


def detect_language(message: str) -> str:
    """
    Simple language detection based on common Spanish words
    For production, use langdetect or googletrans library

    Args:
        message: User message

    Returns:
        'es' for Spanish, 'en' for English
    """
    spanish_keywords = [
        'hola', 'español', 'ayuda', 'si', 'no', 'gracias',
        'trabajo', 'granja', 'cosecha', 'menu', 'menú'
    ]

    message_lower = message.lower()

    # Check if message contains Spanish keywords
    for keyword in spanish_keywords:
        if keyword in message_lower:
            return 'es'

    return 'en'  # Default to English
