from chatbot import FarmConnectBot
from typing import Optional

class SimpleFarmConnectBot(FarmConnectBot):
    def show_welcome_menu(self, from_number: str) -> str:
        msg = """🌾 *FarmConnect* 🌾

            👤 Who are you?

            1️⃣ 👷 Worker (Find Job)
            2️⃣ 🚜 Farm Owner (Hire)

            ➡️ Send: 1 or 2"""

        self.store.set_conversation_state(from_number, 'awaiting_role_selection')
        return msg

    def show_farmer_menu(self, from_number: str) -> str:
        msg = """👷 *Worker Menu*

            1️⃣ 💼 Find Jobs
            2️⃣ ⚙️ My Preferences
            3️⃣ 📋 My Applications
            4️⃣ 💬 Message Owner
            5️⃣ ❓ Help

            ➡️ Send number"""

        self.store.clear_conversation_state(from_number)
        return msg

    def show_owner_menu(self, from_number: str) -> str:
        msg = """🚜 *Owner Menu*

            1️⃣ ➕ Post Job
            2️⃣ 📋 My Jobs
            3️⃣ 👥 Applicants
            4️⃣ 💬 Message Workers
            5️⃣ ❓ Help

            ➡️ Send number"""

        self.store.clear_conversation_state(from_number)
        return msg

    def start_farmer_registration(self, from_number: str) -> str:
        self.store.set_conversation_state(from_number, 'farmer_reg_name')
        return """✅ Welcome Worker!

                📝 Step 1/3

                👤 Your Name?

                ➡️ Send your name"""

    def handle_farmer_name(self, from_number: str, name: str) -> str:
        self.store.update_user_profile(from_number, {'name': name})
        self.store.set_conversation_state(from_number, 'farmer_reg_location')
        return f"""👋 Hi {name}!

                📝 Step 2/3

                📍 Your City?

                ➡️ Send your city"""

    def handle_farmer_location(self, from_number: str, location: str) -> str:
        self.store.update_user_profile(from_number, {'location': location})
        self.store.set_conversation_state(from_number, 'farmer_reg_id')
        return """📝 Step 3/3

                📸 Send ID Photo

                🪪 Take photo of:
                • Driver License
                • ID Card

                ➡️ Send photo now"""

    def handle_farmer_id(self, from_number: str, media_url: Optional[str]) -> str:
        if not media_url:
            return """❌ No photo

                    📸 Please send photo

                    ➡️ Take photo of ID"""

        self.store.update_user_profile(from_number, {'id_verified': True, 'id_photo_url': media_url})
        self.store.update_user(from_number, {'registered': True})

        self.store.set_conversation_state(from_number, 'farmer_pref_work_type')
        return """✅ ID Received!

                ⚙️ Job Preferences

                🛠 What work?

                1️⃣ 🌾 Harvest
                2️⃣ 🌱 Plant
                3️⃣ 💧 Irrigation
                4️⃣ 🐄 Animals
                5️⃣ 🔨 General Work
                6️⃣ ✅ All Work

                ➡️ Send: 1,2,3 or just 1"""

    def handle_work_type(self, from_number: str, work_types: str) -> str:
        work_type_map = {
            '1': 'Harvesting',
            '2': 'Planting',
            '3': 'Irrigation',
            '4': 'Livestock care',
            '5': 'General labor',
            '6': 'All types of work'
        }

        selections = [s.strip() for s in work_types.replace(' ', '').split(',')]
        selected_types = []

        for sel in selections:
            if sel in work_type_map:
                selected_types.append(work_type_map[sel])

        if not selected_types:
            return """❌ Wrong number

                    ➡️ Send: 1 to 6

                    Example: 1,2,3"""

        work_types_str = ', '.join(selected_types)
        self.store.update_user_profile(from_number, {'work_types': work_types_str})

        self.store.set_conversation_state(from_number, 'farmer_pref_location')
        return """🚗 How far can you go?

                1️⃣ 📍 10 miles
                2️⃣ 📍📍 25 miles
                3️⃣ 📍📍📍 50 miles
                4️⃣ 🌍 Any distance

                ➡️ Send: 1, 2, 3, or 4"""

    def handle_pref_location(self, from_number: str, distance: str) -> str:
        distance_map = {
            '1': 10,
            '2': 25,
            '3': 50,
            '4': 999
        }

        distance = distance.strip()
        if distance not in distance_map:
            return """❌ Wrong number

                    ➡️ Send: 1, 2, 3, or 4"""

        miles = distance_map[distance]
        self.store.update_user_profile(from_number, {'max_distance': miles})
        self.store.set_conversation_state(from_number, 'farmer_pref_hours')
        return """⏰ Work Schedule?

                1️⃣ 🕐🕐🕐 Full-time (40+ hrs)
                2️⃣ 🕐🕐 Part-time (20-40 hrs)
                3️⃣ ⚡ Flexible (Any)

                ➡️ Send: 1, 2, or 3"""

    def handle_hours(self, from_number: str, choice: str) -> str:
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
            return """❌ Wrong number

                    ➡️ Send: 1, 2, or 3"""

    def show_multiple_job_recommendations(self, from_number: str, matched_jobs: list) -> str:
        count = len(matched_jobs)

        msg = f"""✅ Found {count} Job{"s" if count > 1 else ""}!
                💰 Best Pay First

                ━━━━━━━━━━━━━

                """

        for i, job in enumerate(matched_jobs, 1):
            if job.get('payment_type') == 'per day':
                pay = f"${job.get('payment_amount', 0)}/day"
            elif job.get('payment_type') == 'per hour':
                pay = f"${job.get('payment_amount', 0)}/hr"
            elif job.get('pay_rate'):
                pay = f"${job.get('pay_rate')}/hr"
            else:
                pay = "Ask Owner"

            msg += f"""*{i}. {job.get('work_type', 'Work')}*
                    🏡 {job.get('farm_name', 'Farm')}
                    💰 {pay}
                    📍 {job.get('location', 'N/A')}
                    👥 {job.get('workers_needed', '?')} needed

                    """

        msg += """━━━━━━━━━━━━━

                ➡️ Send number (1-""" + str(count) + """)
                Or send: menu"""

        job_ids = [j['job_id'] for j in matched_jobs]
        self.store.set_conversation_state(from_number, 'selecting_from_recommendations', {
            'jobs': job_ids
        })

        return msg

    def handle_job_selection_from_list(self, from_number: str, message: str, data: dict) -> str:
        message = message.strip()

        if message.lower() == 'menu':
            user = self.store.get_user(from_number)
            self.store.clear_conversation_state(from_number)
            return self.show_main_menu(from_number, user)

        job_ids = data.get('jobs', [])

        try:
            choice = int(message)
            if 1 <= choice <= len(job_ids):
                job_id = job_ids[choice - 1]
                job = self.store.get_job(job_id)

                if not job:
                    return """❌ Job not found

                    ➡️ Try again or send: menu"""

                if job.get('payment_type') == 'per day':
                    pay = f"${job.get('payment_amount', 0)}/day"
                elif job.get('payment_type') == 'per hour':
                    pay = f"${job.get('payment_amount', 0)}/hr"
                elif job.get('pay_rate'):
                    pay = f"${job.get('pay_rate')}/hr"
                else:
                    pay = "Ask Owner"

                msg = f"""━━━━━━━━━━━━━
                        📋 *Job Details*
                        ━━━━━━━━━━━━━

                        🏡 {job.get('farm_name', 'Farm')}

                        🛠 {job.get('work_type', 'Work')}

                        👥 {job.get('workers_needed', '?')} workers needed

                        ⏰ {job.get('work_hours', job.get('hours', 'Full day'))}

                        💰 {pay}

                        📍 {job.get('location', 'N/A')}

                        🚗 {job.get('transportation', 'Not specified')}

                        📍 Meet: {job.get('meeting_point', 'See location')}

                        ℹ️ {job.get('description', 'No details')}

                        ━━━━━━━━━━━━━

                        ❓ Apply for this job?

                        1️⃣ ✅ Yes, Apply!
                        2️⃣ ⬅️ Back to list

                        ➡️ Send: 1 or 2"""

                self.store.set_conversation_state(from_number, 'job_details_view', {
                    'job_id': job_id,
                    'all_jobs': job_ids
                })

                return msg
            else:
                return f"""❌ Wrong number

                        ➡️ Send: 1 to {len(job_ids)}
                        Or send: menu"""
            
        except ValueError:
            return f"""❌ Send a number

                    ➡️ Example: 1

                    Or send: menu"""

    def handle_job_application(self, from_number: str, message: str, data: dict) -> str:
        message = message.strip()

        if message.lower() == 'menu':
            user = self.store.get_user(from_number)
            self.store.clear_conversation_state(from_number)
            return self.show_main_menu(from_number, user)

        job_id = data.get('job_id')
        all_jobs = data.get('all_jobs', [])

        if message == '1':
            # Apply for the job
            job = self.store.get_job(job_id)
            if not job:
                return """❌ Job not found

                        ➡️ Send: menu"""

            match_id = self.store.create_match(job_id, from_number, 'accepted')
            user = self.store.get_user(from_number)

            owner_phone = job.get('owner_phone')
            if owner_phone and self.twilio_client:
                if job.get('payment_type') == 'per day':
                    pay = f"${job.get('payment_amount', 0)}/day"
                elif job.get('payment_type') == 'per hour':
                    pay = f"${job.get('payment_amount', 0)}/hr"
                elif job.get('pay_rate'):
                    pay = f"${job.get('pay_rate')}/hr"
                else:
                    pay = "Contact for details"

                self.send_message(
                    owner_phone,
                    f"""🎉 *New Application!*

                    👤 {user['profile'].get('name', 'Worker')}
                    🛠 {job.get('work_type', 'Work')}
                    📍 {job.get('location', 'N/A')}
                    💰 {pay}

                    ➡️ Send 3 to see applicants"""
                )

            self.store.clear_conversation_state(from_number)

            if job.get('payment_type') == 'per day':
                pay = f"${job.get('payment_amount', 0)}/day"
            elif job.get('payment_type') == 'per hour':
                pay = f"${job.get('payment_amount', 0)}/hr"
            elif job.get('pay_rate'):
                pay = f"${job.get('pay_rate')}/hr"
            else:
                pay = "Contact for details"

            return f"""✅ *Applied!*

                    Owner will contact you soon!

                    📋 Job:
                    • {job.get('work_type', 'Work')}
                    • {job.get('farm_name', 'Farm')}
                    • {pay}
                    • ID: {match_id}

                    {self.show_farmer_menu(from_number)}"""

        elif message == '2':
            matched_jobs = [self.store.get_job(jid) for jid in all_jobs if self.store.get_job(jid)]
            return self.show_multiple_job_recommendations(from_number, matched_jobs)

        else:
            return """❌ Wrong number

                    1️⃣ Apply
                    2️⃣ Back

                    ➡️ Send: 1 or 2"""

    def start_owner_registration(self, from_number: str) -> str:
        self.store.set_conversation_state(from_number, 'owner_reg_name')
        return """✅ Welcome Farm Owner!

                📝 Step 1/3

                👤 Your Name?

                ➡️ Send your name"""

    def handle_owner_name(self, from_number: str, name: str) -> str:
        self.store.update_user_profile(from_number, {'name': name})
        self.store.set_conversation_state(from_number, 'owner_reg_farm_name')
        return f"""👋 Hi {name}!

                📝 Step 2/3

                🚜 Farm Name?

                ➡️ Send farm name"""

    def handle_farm_name(self, from_number: str, farm_name: str) -> str:
        self.store.update_user_profile(from_number, {'farm_name': farm_name})
        self.store.set_conversation_state(from_number, 'owner_reg_location')
        return """📝 Step 3/3

                📍 Farm Location?

                ➡️ Send city/area"""

    def handle_owner_location(self, from_number: str, location: str) -> str:
        self.store.update_user_profile(from_number, {'location': location})
        self.store.update_user(from_number, {'registered': True})
        self.store.clear_conversation_state(from_number)

        user = self.store.get_user(from_number)
        return f"""✅ Registration Complete!

                🏡 Farm: {user['profile'].get('farm_name', 'Your Farm')}
                📍 {location}

                {self.show_owner_menu(from_number)}"""
