import telebot
from telebot import types
import os

# --- VARIABLES (Railway se connect honge) ---
API_TOKEN = os.getenv('8621463397:AAHILEtpnwNSY8-B5knDQUAfavq8iyk17Ew')
ADMIN_ID = int(os.getenv('7397475374'))
GROUP_ID = os.getenv('-4830250078')
UPI_ID = os.getenv('aemabkah@ybl')

bot = telebot.TeleBot(API_TOKEN)

# --- DATABASE (Simple) ---
prices = {"100": 65, "160": 105, "250": 160}
pending_users = {}

# --- MAIN MENU ---
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Buy ₹100 @ ₹65", callback_data="buy_100"),
        types.InlineKeyboardButton("🛒 Buy ₹160 @ ₹105", callback_data="buy_160"),
        types.InlineKeyboardButton("🛒 Buy ₹250 @ ₹160", callback_data="buy_250"),
        types.InlineKeyboardButton("📞 Contact Support", url="t.me/your_id") # Apni ID yahan dalo
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 
        "🏆 **WELCOME TO WORLD'S BEST REDEEM STORE**\n\n⚡ Instant Delivery\n💎 35% Flat Discount\n✅ 100% Trusted & Secure", 
        reply_markup=main_menu(), parse_mode="Markdown")

# --- HANDLING CLICKS ---
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy(call):
    val = call.data.split('_')[1]
    price = prices[val]
    pending_users[call.message.chat.id] = {"val": val, "price": price}
    
    msg = f"💳 **PAYMENT DETAILS**\n\nAmount: **₹{price}**\nUPI ID: `{UPI_ID}`\n\nSteps:\n1. UPI ID copy karein aur payment karein.\n2. Payment ka **Screenshot** yahan bhejein."
    bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, parse_mode="Markdown")

# --- SCREENSHOT HANDLING ---
@bot.message_handler(content_types=['photo'])
def handle_payment(message):
    if message.chat.id in pending_users:
        data = pending_users[message.chat.id]
        
        # Admin Panel Buttons
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ Approve", callback_data=f"app_{message.chat.id}"),
            types.InlineKeyboardButton("❌ Reject", callback_data=f"rej_{message.chat.id}")
        )
        
        # Admin ko alert bhejna
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, 
            caption=f"🔔 **NEW ORDER!**\nUser: @{message.from_user.username}\nItem: ₹{data['val']} Code\nPrice: ₹{data['price']}", 
            reply_markup=markup)
        
        bot.reply_to(message, "⏳ **Checking...**\nAdmin aapka payment verify kar raha hai. 2-5 min wait karein.")

# --- ADMIN PANEL LOGIC ---
@bot.callback_query_handler(func=lambda call: call.data.startswith(('app_', 'rej_')))
def admin_action(call):
    action, user_id = call.data.split('_')
    user_id = int(user_id)
    
    if action == "app":
        # User ko message
        bot.send_message(user_id, "✅ **PAYMENT VERIFIED!**\nYe raha aapka code: `ABCD-1234-EFGH` \n\nThanks for buying! ❤️")
        
        # Group mein auto-post (Asli King Feature)
        bot.send_message(GROUP_ID, 
            f"🎉 **NEW SUCCESSFUL REDEEM!**\n\n👤 User: @User\n💰 Value: ₹{pending_users[user_id]['val']}\n✅ Status: Delivered\n\n🛒 Aap bhi lo: @{bot.get_me().username}", 
            parse_mode="Markdown")
        
        bot.answer_callback_query(call.id, "Order Approved!")
    else:
        bot.send_message(user_id, "❌ **PAYMENT FAILED!**\nAdmin ne aapka screenshot reject kar diya hai. Sahi screenshot bhejein.")
        bot.answer_callback_query(call.id, "Order Rejected!")

bot.polling()
