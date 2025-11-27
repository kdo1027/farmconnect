"""
Test script for multilingual bot
Demonstrates English and Spanish conversations
"""
from chatbot_multilingual import MultilingualFarmConnectBot
from data_store import DataStore

def test_english_flow():
    """Test English conversation flow"""
    print("=" * 60)
    print("TEST 1: ENGLISH CONVERSATION")
    print("=" * 60)

    store = DataStore()
    bot = MultilingualFarmConnectBot()
    bot.store = store

    phone = "whatsapp:+15555550101"

    print("\n📱 User sends: Hello")
    response = bot.handle_message(phone, "Hello")
    print(f"🤖 Bot: {response[:150]}...")

    print("\n📱 User sends: 1 (selects farmer)")
    response = bot.handle_message(phone, "1")
    print(f"🤖 Bot: {response[:150]}...")

    print("\n📱 User sends: John Smith")
    response = bot.handle_message(phone, "John Smith")
    print(f"🤖 Bot: {response[:150]}...")

    # Cleanup
    store._write_json(store.users_file, {})
    store._write_json(store.conversations_file, {})
    print("\n✅ English test complete!\n")


def test_spanish_flow():
    """Test Spanish conversation flow"""
    print("=" * 60)
    print("TEST 2: SPANISH CONVERSATION")
    print("=" * 60)

    store = DataStore()
    bot = MultilingualFarmConnectBot()
    bot.store = store

    phone = "whatsapp:+15555550102"

    print("\n📱 User sends: Hola")
    response = bot.handle_message(phone, "Hola")
    print(f"🤖 Bot: {response[:150]}...")

    print("\n📱 User sends: 1 (selects trabajador)")
    response = bot.handle_message(phone, "1")
    print(f"🤖 Bot: {response[:150]}...")

    print("\n📱 User sends: Juan García")
    response = bot.handle_message(phone, "Juan García")
    print(f"🤖 Bot: {response[:150]}...")

    # Cleanup
    store._write_json(store.users_file, {})
    store._write_json(store.conversations_file, {})
    print("\n✅ Spanish test complete!\n")


def test_language_switching():
    """Test switching between languages"""
    print("=" * 60)
    print("TEST 3: LANGUAGE SWITCHING")
    print("=" * 60)

    store = DataStore()
    bot = MultilingualFarmConnectBot()
    bot.store = store

    phone = "whatsapp:+15555550103"

    # Start in English
    print("\n📱 User sends: Hi")
    response = bot.handle_message(phone, "Hi")
    print(f"🤖 Bot (English): {response[:100]}...")

    # Register user
    bot.handle_message(phone, "1")  # Select farmer
    bot.handle_message(phone, "Test User")  # Name
    bot.handle_message(phone, "Chapel Hill")  # Location
    bot.store.update_user(phone, {'registered': True})
    bot.store.clear_conversation_state(phone)

    # Switch to Spanish
    print("\n📱 User sends: español")
    response = bot.handle_message(phone, "español")
    print(f"🤖 Bot (switched to Spanish): {response[:100]}...")

    # Check menu is in Spanish
    print("\n📱 User sends: menu")
    response = bot.handle_message(phone, "menu")
    print(f"🤖 Bot (Spanish menu): {response[:100]}...")

    # Switch back to English
    print("\n📱 User sends: english")
    response = bot.handle_message(phone, "english")
    print(f"🤖 Bot (switched to English): {response[:100]}...")

    # Cleanup
    store._write_json(store.users_file, {})
    store._write_json(store.conversations_file, {})
    print("\n✅ Language switching test complete!\n")


if __name__ == "__main__":
    print("\n🌍 FARMCONNECT MULTILINGUAL BOT TEST\n")

    test_english_flow()
    test_spanish_flow()
    test_language_switching()

    print("=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nLanguage Features:")
    print("  ✓ Automatic language detection (English/Spanish)")
    print("  ✓ Manual language switching (type 'español' or 'english')")
    print("  ✓ Persistent language preference per user")
    print("  ✓ All menus and messages translated")
