from chatbot import FarmConnectBot
from translations import get_text, detect_language
from typing import Optional


class MultilingualFarmConnectBot(FarmConnectBot):
    def get_user_language(self, from_number: str) -> str:
        user = self.store.get_user(from_number)
        if user and 'language' in user.get('profile', {}):
            return user['profile']['language']
        return 'en'  

    def set_user_language(self, from_number: str, language: str):
        self.store.update_user_profile(from_number, {'language': language})

    def handle_message(self, from_number: str, message_body: str, media_url: Optional[str] = None) -> str:
        if message_body.lower() in ['español', 'spanish', 'es']:
            self.set_user_language(from_number, 'es')
            return "✅ Idioma cambiado a Español\n\n" + self.handle_message_multilingual(from_number, message_body, media_url)
        elif message_body.lower() in ['english', 'inglés', 'ingles', 'en']:
            self.set_user_language(from_number, 'en')
            return "✅ Language changed to English\n\n" + self.handle_message_multilingual(from_number, message_body, media_url)

        return self.handle_message_multilingual(from_number, message_body, media_url)

    def handle_message_multilingual(self, from_number: str, message_body: str, media_url: Optional[str] = None) -> str:
        user = self.store.get_user(from_number)
        conv_state = self.store.get_conversation_state(from_number)

        if not user:
            detected_lang = detect_language(message_body)
            lang = detected_lang
        else:
            lang = self.get_user_language(from_number)

        self.current_lang = lang

        if conv_state:
            return self.handle_state(from_number, conv_state, message_body, media_url)

        if not user:
            self.store.create_user(from_number, 'unknown')  # Will set type later
            self.set_user_language(from_number, lang)
            return self.show_welcome_menu(from_number)
        
        if user.get('registered'):
            if message_body.lower() in ['menu', 'menú', 'inicio']:
                return self.show_main_menu(from_number, user)
            elif message_body.lower() in ['help', 'ayuda']:
                return self.show_help(from_number)
            else:
                return self.handle_menu_selection(from_number, user, message_body)

        return self.show_welcome_menu(from_number)

    def show_welcome_menu(self, from_number: str) -> str:
        lang = self.get_user_language(from_number)
        msg = get_text('welcome', lang)
        self.store.set_conversation_state(from_number, 'awaiting_role_selection')
        return msg

    def show_farmer_menu(self, from_number: str) -> str:
        lang = self.get_user_language(from_number)
        msg = get_text('farmer_menu', lang)
        self.store.clear_conversation_state(from_number)
        return msg

    def show_owner_menu(self, from_number: str) -> str:
        lang = self.get_user_language(from_number)
        msg = get_text('owner_menu', lang)
        self.store.clear_conversation_state(from_number)
        return msg

    def show_help(self, from_number: str = None) -> str:
        if from_number:
            lang = self.get_user_language(from_number)
        else:
            lang = getattr(self, 'current_lang', 'en')
        return get_text('help', lang)

    def start_farmer_registration(self, from_number: str) -> str:
        lang = self.get_user_language(from_number)
        self.store.set_conversation_state(from_number, 'farmer_reg_name')
        return get_text('farmer_welcome', lang)

    def handle_farmer_name(self, from_number: str, name: str) -> str:
        lang = self.get_user_language(from_number)
        self.store.update_user_profile(from_number, {'name': name})
        self.store.set_conversation_state(from_number, 'farmer_reg_location')

        greeting = f"Nice to meet you, {name}! 👋" if lang == 'en' else f"¡Mucho gusto, {name}! 👋"
        return greeting + "\n\n" + get_text('farmer_location_prompt', lang)

    def handle_farmer_location(self, from_number: str, location: str) -> str:
        lang = self.get_user_language(from_number)
        self.store.update_user_profile(from_number, {'location': location})
        self.store.set_conversation_state(from_number, 'farmer_reg_id')
        return get_text('farmer_id_prompt', lang)

    def handle_farmer_id(self, from_number: str, media_url: Optional[str]) -> str:
        lang = self.get_user_language(from_number)

        if not media_url:
            return get_text('farmer_id_no_photo', lang)

        self.store.update_user_profile(from_number, {'id_verified': True, 'id_photo_url': media_url})
        self.store.update_user(from_number, {'registered': True})

        self.store.set_conversation_state(from_number, 'farmer_pref_work_type')
        return get_text('farmer_id_received', lang)

    def handle_work_type(self, from_number: str, work_types: str) -> str:
        lang = self.get_user_language(from_number)

        work_type_map = {
            '1': get_text('work_type_harvesting', lang),
            '2': get_text('work_type_planting', lang),
            '3': get_text('work_type_irrigation', lang),
            '4': get_text('work_type_livestock', lang),
            '5': get_text('work_type_general', lang),
            '6': get_text('work_type_all', lang)
        }

        selections = [s.strip() for s in work_types.replace(' ', '').split(',')]
        selected_types = []

        for sel in selections:
            if sel in work_type_map:
                selected_types.append(work_type_map[sel])

        if not selected_types:
            error_msg = "Please select valid options (1-6).\n\nReply with numbers separated by commas (e.g., 1,2,3):" if lang == 'en' else "Por favor seleccione opciones válidas (1-6).\n\nResponda con números separados por comas (ej: 1,2,3):"
            return error_msg

        work_types_str = ', '.join(selected_types)
        self.store.update_user_profile(from_number, {'work_types': work_types_str})

        self.store.set_conversation_state(from_number, 'farmer_pref_location')
        return get_text('distance_prompt', lang)

    def handle_pref_location(self, from_number: str, distance: str) -> str:
        lang = self.get_user_language(from_number)

        distance_map = {
            '1': 10,
            '2': 25,
            '3': 50,
            '4': 999
        }

        distance = distance.strip()
        if distance not in distance_map:
            error_msg = get_text('distance_prompt', lang) + "\n\n" + (
                "Please select a valid option (1-4)." if lang == 'en' else "Por favor seleccione una opción válida (1-4)."
            )
            return error_msg

        miles = distance_map[distance]
        self.store.update_user_profile(from_number, {'max_distance': miles})
        self.store.set_conversation_state(from_number, 'farmer_pref_hours')
        return get_text('hours_prompt', lang)

    def handle_hours(self, from_number: str, choice: str) -> str:
        lang = self.get_user_language(from_number)

        hours_map = {
            '1': 'full-time',
            '2': 'part-time',
            '3': 'flexible'
        }

        if choice in hours_map:
            self.store.update_user_profile(from_number, {'hours_preference': hours_map[choice]})
            self.store.clear_conversation_state(from_number)
            return self.show_job_recommendations(from_number)
        else:
            error_msg = "Please reply with 1, 2, or 3" if lang == 'en' else "Por favor responda con 1, 2, o 3"
            return error_msg

    def show_job_recommendations(self, from_number: str) -> str:
        lang = self.get_user_language(from_number)
        user = self.store.get_user(from_number)
        prefs = user.get('profile', {})

        open_jobs = self.store.get_open_jobs()
        matched_jobs = self.match_jobs(open_jobs, prefs, from_number)

        if not matched_jobs:
            return get_text('profile_complete', lang) + "\n\n" + get_text('no_jobs', lang) + "\n\n" + self.show_farmer_menu(from_number)

        return self.show_multiple_job_recommendations(from_number, matched_jobs)

    def show_multiple_job_recommendations(self, from_number: str, matched_jobs: list) -> str:
        lang = self.get_user_language(from_number)
        count = len(matched_jobs)

        msg = get_text('profile_complete', lang) + "\n\n"
        msg += get_text('found_jobs', lang, count=count) + "\n\n━━━━━━━━━━━━━━━━━━━━\n\n"

        for i, job in enumerate(matched_jobs, 1):
            # Format payment
            if job.get('payment_type') == 'per day':
                pay_display = f"${job.get('payment_amount', 'N/A')}" + get_text('per_day', lang)
            elif job.get('payment_type') == 'per hour':
                pay_display = f"${job.get('payment_amount', 'N/A')}" + get_text('per_hour', lang)
            elif job.get('pay_rate'):
                pay_display = f"${job.get('pay_rate')}" + get_text('per_hour', lang)
            else:
                pay_display = "Contact for details" if lang == 'en' else "Contacte para detalles"

            workers_text = get_text('workers_needed', lang)

            msg += f"""*{i}. {job.get('work_type', 'Farm Work')}*
                    🏡 {job.get('farm_name', 'Farm')}
                    💰 {pay_display}
                    📍 {job.get('location', 'N/A')}
                    ⏰ {job.get('hours', job.get('work_hours', 'Full day'))}
                    👥 {job.get('workers_needed', 'N/A')} {workers_text}

                    """

        msg += "━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += get_text('select_job', lang, max=count)

        job_ids = [j['job_id'] for j in matched_jobs]
        self.store.set_conversation_state(from_number, 'selecting_from_recommendations', {
            'jobs': job_ids
        })

        return msg
