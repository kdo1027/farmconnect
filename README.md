# FarmConnect - WhatsApp Chatbot for Agricultural Workers

A WhatsApp chatbot optimized for agricultural workers to find farm jobs easily using minimal text and maximum visual cues.

## Key Features

- **Multilingual Support** - English & Spanish (Español) with automatic detection
- **Low-Literacy Optimized** - Minimal text, maximum emojis
- **Visual Interface** - Icons, arrows, and clear visual cues
- **Simple Navigation** - All multiple choice with numbers
- **Smart Job Matching** - Matches workers with jobs by work type and salary
- **Complete Registration** - Name, location, ID verification, and preferences

## Language Support

FarmConnect supports **English and Spanish** with:
- **Automatic language detection** - Detects Spanish keywords (hola, trabajo, etc.)
- **Manual language switching** - Type `español` or `english` to switch anytime
- **Persistent preferences** - Language choice is saved per user
- **Professional translations** - All UI text manually translated by native speakers

### Available Bots

| Bot | Port | Language | Use Case |
|-----|------|----------|----------|
| **chatbot.py** | 3000 | English only | Text-heavy version |
| **reply_whatsapp_simple.py** | 3001 | English only | Simplified version with minimal text and emojis |
| **reply_whatsapp_multilingual.py** | 3001 | English & Spanish | Simplified version supporting Spanish & English |

## Design Philosophy

This chatbot is designed specifically for users with limited literacy skills:
- **Minimal text** - Short, simple sentences
- **Maximum emojis** - Visual icons for everything
- **Clear visual cues** - Arrows, checkmarks, numbers
- **Step indicators** - Shows progress (Step 1/3, 2/3, etc.)
- **Simple choices** - All multiple choice with numbers

## Differences from Text Version

| Feature | Main Bot | Simplified Bot |
|---------|----------|----------------|
| **Text length** | Full sentences | Minimal words |
| **Visual cues** | Some emojis | Emojis everywhere |
| **Menu style** | Detailed descriptions | Icons + short labels |
| **Instructions** | Explanatory | Direct with arrows (➡️) |
| **Registration** | Detailed questions | Simple questions with icons |
| **Job display** | Full descriptions | Condensed with icons |

## Emoji Legend

### User Types
- 👷 **Worker** - Agricultural laborers looking for jobs
- 🚜 **Farm Owner** - Farmers hiring workers

### Work Types
- 🌾 **Harvesting** - Crop harvesting work
- 🌱 **Planting** - Planting and seeding
- 💧 **Irrigation** - Watering and irrigation systems
- 🐄 **Animals** - Livestock care
- 🔨 **General** - General farm labor
- ✅ **All** - Any type of work

### Distance
- 📍 **10 miles** - Close by
- 📍📍 **25 miles** - Medium distance
- 📍📍📍 **50 miles** - Far
- 🌍 **Any** - Will travel anywhere

### Work Schedule
- 🕐🕐🕐 **Full-time** - 40+ hours per week
- 🕐🕐 **Part-time** - 20-40 hours per week
- ⚡ **Flexible** - Any hours

### Status Indicators
- ✅ **Success** - Action completed
- ❌ **Error** - Something wrong
- ➡️ **Action** - What to do next
- 📝 **Form** - Registration step
- 💰 **Money** - Payment information
- 📍 **Location** - Place or distance
- ⏰ **Time** - Schedule or hours
- 👥 **People** - Number of workers
- 🏡 **Farm** - Farm name
- 🛠 **Work** - Type of work
- 🚗 **Transport** - Transportation info
- 📸 **Photo** - Take or send photo
- 🪪 **ID** - Identification document
- ❓ **Help** - Help or question

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

1. Sign up at https://www.twilio.com/
2. Get your Account SID and Auth Token from https://console.twilio.com/
3. Set up WhatsApp Sandbox: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn

### 3. Set Environment Variables

Create a `.env` file:

```
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the Bot

Choose one of the following bots:

**Multilingual Bot (English & Spanish)** ⭐ Recommended
```bash
python reply_whatsapp_multilingual.py
```
Runs on **http://localhost:3001**

**Simplified Bot (English only)**
```bash
python reply_whatsapp_simple.py
```
Runs on **http://localhost:3001**

**Text-Heavy Bot (English only)**
```bash
python chatbot.py
```
Runs on **http://localhost:3000**

### Language Commands (Multilingual Bot)
- Type `español` to switch to Spanish
- Type `english` to switch to English
- Or just say "Hola" - language auto-detected!

### 5. Expose Webhook with ngrok

In a new terminal, expose the port matching your chosen bot:

**For Multilingual or Simplified Bot:**
```bash
ngrok http 3001
```

**For Text-Heavy Bot:**
```bash
ngrok http 3000
```

Copy the ngrok HTTPS URL (e.g., `https://abc123.ngrok.io`)

### 6. Configure Twilio Webhook

1. Go to https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. In the "Sandbox Configuration" section
3. Set "When a message comes in" to the appropriate endpoint:
   - **Multilingual Bot**: `https://YOUR_NGROK_URL/reply_whatsapp_multilingual`
   - **Simplified Bot**: `https://YOUR_NGROK_URL/reply_whatsapp_simple`
   - **Text-Heavy Bot**: `https://YOUR_NGROK_URL/reply`
4. Save

## 📋 User Flow (Simplified)

### Welcome Message
```
🌾 FarmConnect 🌾

👤 Who are you?

1️⃣ 👷 Worker (Find Job)
2️⃣ 🚜 Farm Owner (Hire)

➡️ Send: 1 or 2
```

### Worker Registration (3 Steps)

**Step 1 - Name:**
```
✅ Welcome Worker!

📝 Step 1/3

👤 Your Name?

➡️ Send your name
```

**Step 2 - Location:**
```
👋 Hi John!

📝 Step 2/3

📍 Your City?

➡️ Send your city
```

**Step 3 - ID Photo:**
```
📝 Step 3/3

📸 Send ID Photo

🪪 Take photo of:
• Driver License
• ID Card

➡️ Send photo now
```

### Job Preferences (Multiple Choice)

**Work Type:**
```
⚙️ Job Preferences

🛠 What work?

1️⃣ 🌾 Harvest
2️⃣ 🌱 Plant
3️⃣ 💧 Irrigation
4️⃣ 🐄 Animals
5️⃣ 🔨 General Work
6️⃣ ✅ All Work

➡️ Send: 1,2,3 or just 1
```

**Distance:**
```
🚗 How far can you go?

1️⃣ 📍 10 miles
2️⃣ 📍📍 25 miles
3️⃣ 📍📍📍 50 miles
4️⃣ 🌍 Any distance

➡️ Send: 1, 2, 3, or 4
```

**Schedule:**
```
⏰ Work Schedule?

1️⃣ 🕐🕐🕐 Full-time (40+ hrs)
2️⃣ 🕐🕐 Part-time (20-40 hrs)
3️⃣ ⚡ Flexible (Any)

➡️ Send: 1, 2, or 3
```

### Job Recommendations

Shows top 5 jobs sorted by highest pay:

```
✅ Found 3 Jobs!
💰 Best Pay First

━━━━━━━━━━━━━

*1. Harvesting*
🏡 Green Valley Farm
💰 $20/hr
📍 Salinas
👥 5 needed

*2. Planting*
🏡 Sunshine Farms
💰 $18/hr
📍 Watsonville
👥 3 needed

*3. Irrigation*
🏡 Blue Sky Ranch
💰 $16/hr
📍 Gilroy
👥 2 needed

━━━━━━━━━━━━━

➡️ Send number (1-3)
Or send: menu
```

### Job Details & Application

```
━━━━━━━━━━━━━
📋 *Job Details*
━━━━━━━━━━━━━

🏡 Green Valley Farm

🛠 Harvesting

👥 5 workers needed

⏰ 8 AM - 5 PM

💰 $20/hr

📍 Salinas, CA

🚗 Transportation provided

📍 Meet: Farm entrance gate

ℹ️ Strawberry harvest season

━━━━━━━━━━━━━

❓ Apply for this job?

1️⃣ ✅ Yes, Apply!
2️⃣ ⬅️ Back to list

➡️ Send: 1 or 2
```

## Design Principles

### 1. Visual First
Every concept uses an emoji or icon before text. Icons are universal and don't require reading skills.

### 2. Minimal Text
- Keep sentences to 5 words or less
- Use common, simple words
- Avoid technical jargon

### 3. Clear Actions
Always show what to do next with ➡️ arrow and clear instruction.

### 4. Progressive Disclosure
Show only what's needed at each step. Don't overwhelm with options.

### 5. Consistent Patterns
- Numbers for choices (1️⃣, 2️⃣, 3️⃣)
- Arrows for actions (➡️)
- Checkmarks for success (✅)
- X marks for errors (❌)
- Progress indicators (📝 Step 1/3)

## Testing

### Unit Tests

The project includes a comprehensive test suite with **65 automated tests** covering all major functionality.

#### Quick Start
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=html
```

#### Test Coverage

| Test Suite | Tests | Coverage |
|------------|-------|----------|
| **test_data_store.py** | 27 tests | User management, job CRUD, conversation state, matching, persistence |
| **test_chatbot.py** | 29 tests | Registration, preferences, job posting, matching, menus |
| **test_chatbot_simple.py** | 9 tests | Simplified UI, emoji displays, low-literacy optimization |

**Total: 65 tests with 100% pass rate** 

#### Running Specific Tests
```bash
# Run specific test file
pytest tests/test_data_store.py -v

# Run specific test class
pytest tests/test_chatbot.py::TestFarmerRegistration -v

# Run tests matching a pattern
pytest -k "farmer" -v
pytest -k "registration" -v

# Stop on first failure
pytest -x
```

#### View Coverage Report
```bash
# Generate HTML coverage report
pytest --cov=. --cov-report=html

# Open in browser (macOS)
open htmlcov/index.html
```

For complete testing documentation, see **[TESTING_GUIDE.md](TESTING_GUIDE.md)**

## File Structure

```
farmconnect/
├── reply_whatsapp_simple.py   # Flask webhook (port 3001)
├── chatbot_simple.py           # SimpleFarmConnectBot class
├── chatbot.py                  # Base FarmConnectBot class
├── data_store.py               # JSON data storage
├── ai_matcher.py               # AI matching (optional)
├── requirements.txt            # Dependencies
├── .gitignore                  # Git ignore rules
├── .env                        # Environment variables (create this)
├── README.md                   # This file
├── TESTING_GUIDE.md            # Complete testing documentation
├── tests/                      # Unit tests (65 tests)
│   ├── __init__.py
│   ├── conftest.py             # Shared test fixtures
│   ├── test_data_store.py      # DataStore tests (27)
│   ├── test_chatbot.py         # FarmConnectBot tests (29)
│   ├── test_chatbot_simple.py  # SimpleFarmConnectBot tests (9)
│   └── README.md               # Test documentation
├── sample-data/                # Sample data scripts
│   └── create_sample_jobs.py   # Create test jobs
└── data/                       # JSON data files (gitignored)
    ├── users.json
    ├── jobs.json
    ├── conversations.json
    └── matches.json
```

## Data Storage

Same as main bot - uses JSON files in `data/` directory:
- **users.json** - User profiles
- **jobs.json** - Job postings
- **conversations.json** - Current states
- **matches.json** - Job applications

## Technical Details

- **Language**: Python 3.7+
- **Framework**: Flask
- **WhatsApp Integration**: Twilio API
- **Storage**: JSON files

## AI Usage

This project was developed with AI assistance for documentation research and code generation:

- **ChatGPT (70% of AI usage)**: Used for general development, code implementation, and referencing Twilio & Flask documentation
- **Claude Code (30% of AI usage)**: Primarily used for bug detection, unit test generation, and implementing multilingual chatbot version (supporting Spanish)

**Documentation References:**
- Twilio API documentation for WhatsApp integration
- Flask framework documentation for webhook implementation

**Logs:** GPT conversation logs are available in the `appendix` folder for transparency and reference. Based on the official Claude Code documentation, there is currently no built-in feature to export chat history logs directly from Claude Code. 

## Special Commands

Type these anytime:
- **menu** - Return to main menu
- **help** - Get help

## Troubleshooting

### Bot not responding
- Check Flask server is running on port 3001
- Check ngrok is exposing port 3001
- Verify Twilio webhook points to `/reply_whatsapp_simple`

### Wrong emojis showing
- Some older phones may not support all emojis
- Emojis should work on most smartphones from 2015+

### Messages too long
If messages exceed WhatsApp limits:
- Job list shows max 5 jobs
- Each job description is condensed
- Long farm names are truncated
