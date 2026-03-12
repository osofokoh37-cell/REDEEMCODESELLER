import telebot
from telebot import types

# --- CONFIGURATION ---
TOKEN = "APKA_BOT_TOKEN"
ADMIN_ID = 12345678 # Apni ID yahan dalo
GROUP_ID = -100xxxxxx # Proof group ID

bot = telebot.TeleBot(TOKEN)

# --- DATABASE (Simple Version) ---
# Asli bot mein hum SQL ya JSON use karenge
stock = {"100": ["CODE1", "CODE2"], "250": []}
prices = {"100": 65, "250": 160}

# --- USER INTERFACE ---
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🛒 Buy Codes", callback_data="buy")
    btn2 = types.InlineKeyboardButton("🎁 My Orders", callback_data="orders")
    btn3 = types.InlineKeyboardButton("📊 Live Stock", callback_data="stock")
    btn4 = types.InlineKeyboardButton("📞 Support", url="t.me/Apki_ID")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_photo(message.chat.id, "https://example.com/your_banner.jpg", 
                   caption="🏆 **WELCOME TO WORLD'S NO.1 REDEEM STORE**\n\n⚡ Instant Delivery\n💎 35% Discount\n✅ 100% Trusted", 
                   reply_markup=markup, parse_mode="Markdown")

# --- ADMIN PANEL COMMANDS ---
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("➕ Add Stock", "💰 Change Price", "📢 Broadcast")
        bot.send_message(message.chat.id, "Welcome King! Kya karna hai?", reply_markup=markup)

# --- AUTO-UPDATE FEATURE ---
def send_group_proof(user_name, amount, price):
    text = f"✅ **NEW SUCCESSFUL REDEEM!**\n\n👤 **User:** {user_name}\n💰 **Value:** ₹{amount}\n💸 **Paid:** ₹{price}\n\n🛒 Aap bhi lo: @ApkaBotUsername"
    bot.send_message(GROUP_ID, text, parse_mode="Markdown")

bot.polling()
  
