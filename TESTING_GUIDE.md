# FarmConnect Testing Guide

This guide covers both **automated testing** (unit/integration tests) and **manual testing** (WhatsApp interaction).

---

## Automated Testing

### Running the Test Suite

The project includes a comprehensive test suite with 65 tests covering all major functionality.

#### Quick Start
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_chatbot.py
pytest tests/test_data_store.py
pytest tests/test_chatbot_simple.py
```

### Test Coverage

| Test Suite | Tests | Coverage |
|------------|-------|----------|
| **test_data_store.py** | 27 tests | User management, job CRUD, conversation state, matching, data persistence |
| **test_chatbot.py** | 29 tests | Registration flows, preferences, job posting, matching, menus, updates |
| **test_chatbot_simple.py** | 9 tests | Simplified UI, emoji displays, low-literacy optimization, inheritance |
| **test_multilingual.py** | 3 tests | English flow, Spanish flow, language switching, auto-detection |

**Total**: 68 tests with 100% pass rate 

### Running Individual Test Classes

```bash
# Test DataStore user management
pytest tests/test_data_store.py::TestDataStoreUserManagement -v

# Test farmer registration
pytest tests/test_chatbot.py::TestFarmerRegistration -v

# Test job posting
pytest tests/test_chatbot.py::TestJobPosting -v

# Test simplified bot welcome
pytest tests/test_chatbot_simple.py::TestSimpleBotWelcomeFlow -v
```

### Running Specific Tests

```bash
# Run a single test
pytest tests/test_data_store.py::TestDataStoreUserManagement::test_create_user_farmer -v

# Run tests matching a pattern
pytest -k "farmer" -v
pytest -k "registration" -v
pytest -k "job_posting" -v

# Stop on first failure
pytest -x

# Show detailed output
pytest -vv --tb=short
```

### Viewing Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=. --cov-report=html

# Open in browser (macOS)
open htmlcov/index.html

# Generate terminal report with missing lines
pytest --cov=. --cov-report=term-missing
```

---

## Multilingual Testing

### Testing the Multilingual Bot

FarmConnect includes multilingual support for **English and Spanish**. The multilingual bot runs on port 3001.

#### Running Multilingual Tests

```bash
# Run multilingual tests
pytest tests/test_multilingual.py -v

# Or run the demo script
python test_multilingual.py
```

**Expected output:**
```
TEST 1: ENGLISH CONVERSATION
📱 User sends: Hello
🤖 Bot: 🌾 *Welcome to FarmConnect!* 🌾...
✅ English test complete!

TEST 2: SPANISH CONVERSATION
📱 User sends: Hola
🤖 Bot: 🌾 *¡Bienvenido a FarmConnect!* 🌾...
✅ Spanish test complete!

TEST 3: LANGUAGE SWITCHING
📱 User sends: español
🤖 Bot (switched to Spanish): ✅ Idioma cambiado a Español...
✅ Language switching test complete!

✅ ALL TESTS PASSED!
```

#### Starting the Multilingual Bot

```bash
# Start multilingual bot (port 3002)
python reply_whatsapp_multilingual.py
```

**Expected Output:**
```
🌾 FarmConnect Multilingual Bot Starting...
🌍 Languages: English & Español
🚀 Running on http://localhost:3002

Webhook URL: http://your-ngrok-url/reply_whatsapp_multilingual

Language Commands:
  - Type 'español' to switch to Spanish
  - Type 'english' to switch to English
```

#### Language Features Tested

| Feature | How It Works | Test Coverage |
|---------|--------------|---------------|
| **Auto-detection** | Detects Spanish keywords (hola, trabajo, ayuda, etc.) | test_spanish_flow() |
| **Manual switching** | Type `español` or `english` to switch anytime | test_language_switching() |
| **Persistent preference** | Language choice saved in user profile | test_language_switching() |
| **All translations** | Menus, prompts, errors all translated | All test functions |

---

## Manual Testing via WhatsApp

### Quick Setup for Manual Testing

#### Step 1: Create Sample Jobs
```bash
python sample-data/create_sample_jobs.py
```

#### Step 2: Start the Bot
```bash
python reply_whatsapp_multilingual.py
```

**Expected Output:**
```
🌾 FarmConnect Multilingual Bot Starting...
🌍 Languages: English & Español
🚀 Running on http://localhost:3001

Webhook URL: http://your-ngrok-url/reply_whatsapp_multilingual

Language Commands:
  - Type 'español' to switch to Spanish
  - Type 'english' to switch to English
```

#### Step 3: Expose with ngrok (in a new terminal)
```bash
ngrok http 3001
```

**Copy the ngrok URL** (e.g., `https://abc123.ngrok-free.app`)

#### Step 4: Configure Twilio Webhook
1. Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. Under "Sandbox Configuration"
3. Set "When a message comes in" to: `https://YOUR_NGROK_URL/reply_whatsapp_multilingual`
4. Click **Save**

---

## Manual Testing Scenarios

### Test Scenario 1: New Farmer Registration (English)

#### 1. Start Conversation
**You send:** Any message (e.g., "Hi" or "Hello")

**Bot responds:**
```
🌾 *Welcome to FarmConnect!* 🌾

We connect agricultural workers with farm employers.

Please select your role:
1️⃣ I'm looking for farm work (Farmer/Laborer)
2️⃣ I'm hiring workers (Farm Owner)

Reply with 1 or 2
```

#### 2. Select Farmer Role
**You send:** `1`

**Bot responds:**
```
✅ Great! Let's get you registered.

📝 *Step 1 of 3: Personal Information*

What's your full name?
```

#### 3. Enter Your Name
**You send:** `John Smith` (or any name)

**Bot responds:**
```
Nice to meet you, John Smith! 👋

📍 *Step 2 of 3: Location*

What's your location? (City or area where you're looking for work)
```

#### 4. Enter Location
**You send:** `Sacramento, CA`

**Bot responds:**
```
📸 *Step 3 of 3: ID Verification*

Please upload a photo of your ID card or driver's license.

This helps us keep FarmConnect safe for everyone.
```

#### 5. Upload ID Photo
**You send:** Take/upload any photo from your phone

**Bot responds:**
```
✅ ID received! Thank you.

Now let's set up your job preferences to find the best matches.

🛠 *Work Type Preferences*
What type of farm work are you interested in? (Select all that apply)

1️⃣ Harvesting
2️⃣ Planting
3️⃣ Irrigation
4️⃣ Livestock care
5️⃣ General labor
6️⃣ All types of work

Reply with numbers separated by commas (e.g., 1,2,3) or just one number:
```

#### 6. Set Work Type Preference (Multiple Choice)
**You send:** `1,2` (for Harvesting and Planting)

**Bot responds:**
```
📍 *Work Location Preference*

How far are you willing to travel for work?

1️⃣ Up to 10 miles
2️⃣ Up to 25 miles
3️⃣ Up to 50 miles
4️⃣ Any distance

Reply with 1, 2, 3, or 4:
```

#### 7. Set Travel Distance
**You send:** `2` (Up to 25 miles)

**Bot responds:**
```
⏰ *Working Hours Preference*

What's your preferred work schedule?

1️⃣ Full-time (40+ hours/week)
2️⃣ Part-time (20-40 hours/week)
3️⃣ Flexible (open to both full-time and part-time)

Reply with 1, 2, or 3:
```

#### 8. Set Hours Preference
**You send:** `1` (Full-time)

**Bot responds with TOP 5 job matches (sorted by salary):**
```
✅ *Profile Complete!*

We found 5 job match(es) for you!
(Sorted by highest pay)

━━━━━━━━━━━━━━━━━━━━

*1. Equipment Maintenance*
🏡 Taylor Agricultural Services
💰 $22.0/hour
📍 Pittsboro, NC
⏰ full-time
👥 1 workers needed

*2. Irrigation Specialist*
🏡 Taylor Agricultural Services
💰 $21.0/hour
📍 Cary, NC
⏰ full-time
👥 2 workers needed

*3. Organic Vegetable Farming*
🏡 Blue Ridge Farms
💰 $20.0/hour
📍 Chapel Hill, NC
⏰ full-time
👥 4 workers needed

*4. Livestock Care*
🏡 Green Leaf Gardens
💰 $19.0/hour
📍 Hillsborough, NC
⏰ flexible
👥 2 workers needed

*5. Greenhouse Work*
🏡 Green Leaf Gardens
💰 $18.0/hour
📍 Carrboro, NC
⏰ full-time
👥 3 workers needed

━━━━━━━━━━━━━━━━━━━━

*Select a job to view details and apply:*

Reply with the job number (1-5) or type 'menu' to return to main menu.
```

---

### Test Scenario 2: New Farmer Registration (Spanish)

This scenario tests the **automatic Spanish language detection** and full Spanish conversation flow.

#### 1. Start Conversation in Spanish
**You send:** `Hola` (Spanish greeting triggers auto-detection)

**Bot responds:**
```
🌾 *¡Bienvenido a FarmConnect!* 🌾

Conectamos trabajadores agrícolas con empleadores de granjas.

Por favor seleccione su función:
1️⃣ Busco trabajo agrícola (Trabajador/Jornalero)
2️⃣ Contrato trabajadores (Dueño de Granja)

Responda con 1 o 2
```

#### 2. Select Trabajador (Farmer) Role
**You send:** `1`

**Bot responds:**
```
✅ ¡Excelente! Vamos a registrarlo.

📝 *Paso 1 de 3: Información Personal*

¿Cuál es su nombre completo?
```

#### 3. Enter Your Name
**You send:** `Juan García` (or any name)

**Bot responds:**
```
¡Mucho gusto, Juan García! 👋

📍 *Paso 2 de 3: Ubicación*

¿Cuál es su ubicación? (Ciudad o área donde busca trabajo)
```

#### 4. Enter Location
**You send:** `Chapel Hill, NC`

**Bot responds:**
```
📸 *Paso 3 de 3: Verificación de Identidad*

Por favor suba una foto de su identificación o licencia de conducir.

Esto nos ayuda a mantener FarmConnect seguro para todos.
```

#### 5. Upload ID Photo
**You send:** Take/upload any photo

**Bot responds:**
```
✅ ¡Identificación recibida! Gracias.

Ahora configuremos sus preferencias de trabajo para encontrar las mejores opciones.

🛠 *Preferencias de Tipo de Trabajo*
¿Qué tipo de trabajo agrícola le interesa? (Seleccione todas las opciones)

1️⃣ Cosecha
2️⃣ Siembra
3️⃣ Irrigación/Riego
4️⃣ Cuidado de animales
5️⃣ Trabajo general
6️⃣ Todo tipo de trabajo

Responda con números separados por comas (ej: 1,2,3) o solo un número:
```

#### 6. Set Work Type Preference
**You send:** `6` (Todo tipo de trabajo)

**Bot responds:**
```
📍 *Preferencia de Ubicación de Trabajo*

¿Qué tan lejos está dispuesto a viajar para trabajar?

1️⃣ Hasta 10 millas
2️⃣ Hasta 25 millas
3️⃣ Hasta 50 millas
4️⃣ Cualquier distancia

Responda con 1, 2, 3, o 4:
```

#### 7. Set Travel Distance
**You send:** `3` (Hasta 50 millas)

**Bot responds:**
```
⏰ *Preferencia de Horario de Trabajo*

¿Cuál es su horario de trabajo preferido?

1️⃣ Tiempo completo (40+ horas/semana)
2️⃣ Medio tiempo (20-40 horas/semana)
3️⃣ Flexible (tiempo completo o medio tiempo)

Responda con 1, 2, o 3:
```

#### 8. Set Hours Preference
**You send:** `3` (Flexible)

**Bot responds with job recommendations in Spanish:**
```
✅ *¡Perfil Completo!*

¡Encontramos 5 trabajo(s) que coinciden para usted!
(Ordenados por mejor salario)

━━━━━━━━━━━━━━━━━━━━

*1. Equipment Maintenance*
🏡 Taylor Agricultural Services
💰 $22.0/hora
📍 Pittsboro, NC
⏰ full-time
👥 1 trabajadores necesitados

[... more jobs ...]

━━━━━━━━━━━━━━━━━━━━

*Seleccione un trabajo para ver detalles y aplicar:*

Responda con el número del trabajo (1-5) o escriba 'menu' para volver al menú principal.
```

#### 9. Switch to English (Language Switching Test)
**You send:** `english`

**Bot responds:**
```
✅ Language changed to English

🌾 *Farmer Menu*

1️⃣ Browse available jobs
2️⃣ Update my preferences
3️⃣ View my job applications
4️⃣ Chat with farm owner
5️⃣ Help

Reply with the number of your choice
```

#### 10. Switch Back to Spanish
**You send:** `español`

**Bot responds:**
```
✅ Idioma cambiado a Español

🌾 *Menú de Trabajador*

1️⃣ Ver trabajos disponibles
2️⃣ Actualizar mis preferencias
3️⃣ Ver mis solicitudes de trabajo
4️⃣ Chat con dueño de granja
5️⃣ Ayuda

Responda con el número de su elección
```

---

### Test Scenario 3: Select and Apply for a Job

#### 9. Select a Job from the List
**You send:** `3` (select Organic Vegetable Farming)

**Bot responds:**
```
━━━━━━━━━━━━━━━━━━━━
*Job Details*
━━━━━━━━━━━━━━━━━━━━

🏡 *Farm:* Blue Ridge Farms

🌾 *Type of Work*
Organic Vegetable Farming

👥 *Workers Needed*
4 people

⏰ *Work Hours*
Full day

💰 *Payment*
$20.0/hour

📍 *Work Location*
Chapel Hill, NC

🚗 *Transportation*
Not specified

📍 *Meeting Point*
See location above

📋 *Additional Details:*
Work on certified organic farm. Plant, weed, harvest various vegetables. Knowledge of organic methods a plus. Health benefits available.

━━━━━━━━━━━━━━━━━━━━

*Would you like to apply for this job?*

1️⃣ Yes, apply for this job
2️⃣ No, go back to job list

Reply with 1 or 2:
```

#### 10. Apply for Job
**You send:** `1` (to apply)

**Bot responds:**
```
✅ *Application Submitted!*

The farm owner has been notified and will contact you soon.

*Job Details:*
• Position: Organic Vegetable Farming
• Farm: Blue Ridge Farms
• Pay: $20.0/hour
• Match ID: MATCH_1_20231120...

🌾 *Farmer Menu*

1️⃣ Browse available jobs
2️⃣ Update my preferences
3️⃣ View my job applications
4️⃣ Chat with farm owner
5️⃣ Help

Reply with the number of your choice
```

#### 11. Go Back to Job List (Alternative)
**You send:** `2` (instead of applying)

**Bot responds:**
```
Returns to the top 5 job list, allowing you to select a different job
```

---

### Test Scenario 3: Navigate Main Menu

#### 12. View Applications
**You send:** `3`

**Bot responds:**
```
📋 *Your Job Applications:*

• Organic Vegetable Farming - Status: accepted

🌾 *Farmer Menu*

1️⃣ Browse available jobs
2️⃣ Update my preferences
3️⃣ View my job applications
4️⃣ Chat with farm owner
5️⃣ Help

Reply with the number of your choice
```

#### 13. Update Preferences
**You send:** `2`

**Bot responds:**
```
⚙️ *Update Profile*

What would you like to update?

1️⃣ Work type preferences
2️⃣ Location (city/state)
3️⃣ Minimum pay rate
4️⃣ Travel distance
5️⃣ Hours preference
6️⃣ Back to main menu

Reply with number (1-6):
```

#### 14. Browse More Jobs
**You send:** `1` (from main menu)

**Bot responds:** Shows top 5 available jobs again (sorted by salary)

#### 15. Get Help
**You send:** `5`

**Bot responds:**
```
❓ *FarmConnect Help*

• Type 'menu' anytime to return to main menu
• Type 'help' to see this message

For support, contact: support@farmconnect.com
```

#### 16. Return to Menu
**You send:** `menu`

**Bot responds:** Shows farmer main menu

---

### Test Scenario 4: Farm Owner Registration and Job Posting

#### 1. Select Farm Owner Role
**You send:** `2` (when shown welcome menu)

**Bot responds:**
```
✅ Welcome, farm owner!

📝 *Registration - Step 1 of 3*

What's your full name?
```

#### 2. Complete Owner Registration
**You send:** Name → Farm Name → Location

#### 3. Post a Job
**You send:** `1` (from owner menu)

**Bot follows 8-step job posting flow:**
1. Work type
2. Number of workers needed
3. Work hours
4. Payment type (per hour/day/task)
5. Payment amount
6. Location
7. Transportation (yes/no)
8. Additional details

**Bot confirms:**
```
✅ *Job Posted Successfully!*

━━━━━━━━━━━━━━━━━━━━
📋 *Job Summary*

🌾 Work: [work type]
👥 Workers: [number] people
⏰ Hours: [work hours]
💰 Pay: $[amount] [type]
📍 Location: [location]
🚗 Transport: [provided/not provided]
📍 Meeting: [meeting point]

━━━━━━━━━━━━━━━━━━━━

Job ID: JOB_...

Matching workers will be notified!
```

---

## Testing Checklist

### Automated Tests
- [x] 27 DataStore tests (user, job, state, match management)
- [x] 29 FarmConnectBot tests (registration, preferences, matching)
- [x] 9 SimpleFarmConnectBot tests (simplified UI, emojis)
- [x] 3 Multilingual tests (English flow, Spanish flow, language switching)
- [x] All tests passing (68/68)
- [x] Data persistence verified
- [x] Edge cases handled

### Manual WhatsApp Tests - English
- [ ] New user welcome message appears (English)
- [ ] Can select farmer role (1)
- [ ] Can select farm owner role (2)
- [ ] Farmer registration completes (name, location, ID)
- [ ] Work type preference accepts multiple choices (1,2,3)
- [ ] Travel distance preference works (1-4)
- [ ] Hours preference works (1-3)
- [ ] Top 5 jobs displayed (sorted by salary)
- [ ] Can select job by number (1-5)
- [ ] Selected job shows full details
- [ ] Can apply for job (1)
- [ ] Can go back to list (2)
- [ ] Application confirmation received
- [ ] Main menu navigation works
- [ ] Can view applications
- [ ] Can browse jobs again
- [ ] Can update preferences
- [ ] Help command works
- [ ] Menu command returns to main menu
- [ ] Owner can post jobs (8-step flow)
- [ ] Job posting confirmation received

### Manual WhatsApp Tests - Spanish
- [ ] Spanish welcome appears when user sends "Hola"
- [ ] Auto-detection works for Spanish keywords
- [ ] Can complete registration in Spanish
- [ ] Work type preferences show Spanish options
- [ ] Distance preferences show Spanish text
- [ ] Hours preferences show Spanish text
- [ ] Job recommendations display in Spanish
- [ ] Can switch to English with "english" command
- [ ] Can switch to Spanish with "español" command
- [ ] Language preference persists across sessions
- [ ] All menus display correctly in Spanish
- [ ] Help command shows Spanish text when in Spanish mode

---

## Common Test Commands

| Command | What it does |
|---------|-------------|
| `menu` or `menú` | Return to main menu from anywhere |
| `help` or `ayuda` | Show help message |
| `english` | Switch to English language |
| `español` or `spanish` | Switch to Spanish language |
| `1`, `2`, `3`, etc. | Select menu options |
| `1,2,3` | Select multiple work types |

---

## Viewing Test Data

After testing, you can check the generated data:

```bash
# View all users
cat data/users.json | python -m json.tool

# View all jobs
cat data/jobs.json | python -m json.tool

# View conversation states
cat data/conversations.json | python -m json.tool

# View job matches/applications
cat data/matches.json | python -m json.tool

# Count records
echo "Users: $(cat data/users.json | python -c 'import json,sys; print(len(json.load(sys.stdin)))')"
echo "Jobs: $(cat data/jobs.json | python -c 'import json,sys; print(len(json.load(sys.stdin)))')"
echo "Matches: $(cat data/matches.json | python -c 'import json,sys; print(len(json.load(sys.stdin)))')"
```

---

## Troubleshooting

### Automated Tests

#### Tests fail with import errors
```bash
# Make sure you're in the project root directory
cd /path/to/farmconnect

# Install dependencies
pip install -r requirements.txt

# Run tests again
pytest
```

#### Tests fail on first run
```bash
# Ensure data directory exists
mkdir -p data

# Clear any corrupted data files
rm -f data/*.json

# Run tests again
pytest -v
```

#### Coverage report not generating
```bash
# Install pytest-cov if not installed
pip install pytest-cov

# Run with coverage
pytest --cov=. --cov-report=html

# Open report (macOS)
open htmlcov/index.html

# Open report (Linux)
xdg-open htmlcov/index.html
```

#### Specific test keeps failing
```bash
# Run just that test with verbose output
pytest tests/test_chatbot.py::TestFarmerRegistration::test_farmer_registration_name -vv --tb=short

# Check if it's a data persistence issue
rm -rf data/*.json
pytest tests/test_data_store.py -v
```

### Manual WhatsApp Testing

#### Bot doesn't respond
1. **Check Flask server is running:**
   ```bash
   python reply_whatsapp_multilingual.py
   # Should show: Running on http://localhost:3001
   ```

2. **Check ngrok is active:**
   ```bash
   ngrok http 3001
   # Should show forwarding URL
   ```

3. **Verify Twilio webhook:**
   - Go to Twilio console
   - Check webhook URL matches your ngrok URL
   - URL should be: `https://your-ngrok-url/reply_whatsapp_multilingual`

4. **Check ngrok logs:**
   - ngrok terminal shows all incoming requests
   - Look for POST requests to `/reply_whatsapp_multilingual`
   - Status should be 200, not 404

#### No job recommendations
1. **Run sample data script:**
   ```bash
   python sample-data/create_sample_jobs.py
   ```

2. **Verify jobs were created:**
   ```bash
   cat data/jobs.json | python -m json.tool
   ```

3. **Check job status:**
   - Jobs must have `"status": "open"`
   - Verify work types match your preferences

4. **Try "All types of work":**
   - When asked for work type, send: `6`
   - This matches all available jobs

#### Photo upload not working
1. **Send actual photo** (not text saying "photo")
2. **Check Twilio sandbox supports media**
3. **Try a different photo format** (JPEG works best)

#### Error messages appear
1. **Check Flask console** for Python errors
2. **Verify .env file** has correct credentials:
   ```bash
   cat .env
   # Should show TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
   ```
3. **Check ngrok terminal** for HTTP errors
4. **Restart everything:**
   ```bash
   # Kill Flask
   Ctrl+C

   # Kill ngrok
   Ctrl+C

   # Restart Flask
   python reply_whatsapp_multilingual.py

   # Restart ngrok (new terminal)
   ngrok http 3001

   # Update Twilio webhook with new ngrok URL
   ```
