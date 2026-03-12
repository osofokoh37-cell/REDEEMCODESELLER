import telebot
from telebot import types

# --- SETTINGS ---
API_TOKEN = '8621463397:AAHILEtpnwNSY8-B5knDQUAfavq8iyk17Ew'
ADMIN_ID = 7397475374  
GROUP_ID = 4830250078 
UPI_ID = "armankhan@ybl" 

bot = telebot.TeleBot(API_TOKEN)

# Temporary Database
pending_payments = {}
stock = {"100": [], "160": [], "250": []}

# --- USER INTERFACE ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Buy ₹100 @ ₹65", callback_data="buy_100"),
        types.InlineKeyboardButton("🛒 Buy ₹160 @ ₹105", callback_data="buy_160"),
        types.InlineKeyboardButton("🛒 Buy ₹250 @ ₹160", callback_data="buy_250"),
        types.InlineKeyboardButton("📞 Support", url="t.me/YourUsername")
    )
    bot.send_message(message.chat.id, "🏆 **WORLD'S BEST REDEEM STORE**\nFlat 35% OFF | Instant Delivery", reply_markup=markup, parse_mode="Markdown")

# --- HANDLING PURCHASE ---
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy(call):
    val = call.data.split('_')[1]
    price = {"100": 65, "160": 105, "250": 160}[val]
    
    pending_payments[call.message.chat.id] = {"val": val, "price": price}
    
    msg = f"💳 **Payment Details**\n\nPrice: ₹{price}\nUPI ID: `{UPI_ID}`\n\nPayment karne ke baad **SCREENSHOT** yahan bhejein."
    bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")

# --- ADMIN VERIFICATION ---
@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    if message.chat.id in pending_payments:
        data = pending_payments[message.chat.id]
        # Admin ko screenshot bhejna
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Approve", callback_data=f"app_{message.chat.id}"),
                   types.InlineKeyboardButton("❌ Reject", callback_data=f"rej_{message.chat.id}"))
        
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, 
                       caption=f"New Payment!\nUser: @{message.from_user.username}\nAmount: ₹{data['price']}", 
                       reply_markup=markup)
        bot.reply_to(message, "⏳ Payment verify ho rahi hai... Admin check kar raha hai.")

@bot.callback_query_handler(func=lambda call: call.data.startswith(('app_', 'rej_')))
def admin_action(call):
    action, user_id = call.data.split('_')
    user_id = int(user_id)
    
    if action == "app":
        # Yahan code delivery ka logic aayega (stock se code uthakar)
        bot.send_message(user_id, "✅ Payment Verified! Ye raha aapka code: `ABCD-1234-EFGH`")
        bot.send_message(GROUP_ID, f"🔥 **NEW SUCCESS!**\nUser ne ₹{pending_payments[user_id]['val']} ka code kharida! Aap bhi lo @BotUsername")
        bot.answer_callback_query(call.id, "Approved!")
    else:
        bot.send_message(user_id, "❌ Payment Rejected. Please valid screenshot bhejein.")
        bot.answer_callback_query(call.id, "Rejected!")

bot.polling()
    
