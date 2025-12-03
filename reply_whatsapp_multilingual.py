from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from chatbot_multilingual import MultilingualFarmConnectBot

app = Flask(__name__)
bot = MultilingualFarmConnectBot()

@app.route("/reply_whatsapp_multilingual", methods=['POST'])
def reply_whatsapp():
    from_number = request.values.get('From', '')
    message_body = request.values.get('Body', '')
    media_url = request.values.get('MediaUrl0', None)

    # Get bot response 
    bot_response = bot.handle_message(from_number, message_body, media_url)

    # Create Twilio response
    resp = MessagingResponse()
    resp.message(bot_response)

    return str(resp)

if __name__ == "__main__":
    print("🌾 FarmConnect Multilingual Bot Starting...")
    print("🌍 Languages: English & Español")
    print("🚀 Running on http://localhost:3001")
    print("\nWebhook URL: http://your-ngrok-url/reply_whatsapp_multilingual")
    print("\nLanguage Commands:")
    print("  - Type 'español' to switch to Spanish")
    print("  - Type 'english' to switch to English")
    app.run(host='0.0.0.0', port=3001, debug=True)
