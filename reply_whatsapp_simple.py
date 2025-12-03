from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from chatbot_simple import SimpleFarmConnectBot

app = Flask(__name__)
bot = SimpleFarmConnectBot()

@app.route("/reply_whatsapp_simple", methods=['POST'])
def reply_whatsapp():
    """Respond to incoming WhatsApp messages using simplified bot"""
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
    print("🌾 FarmConnect Simplified Bot Starting...")
    print("📱 Optimized for low-literacy users")
    print("🚀 Running on http://localhost:3001")
    print("\nWebhook URL: http://your-ngrok-url/reply_whatsapp_simple")
    app.run(host='0.0.0.0', port=3001, debug=True)
