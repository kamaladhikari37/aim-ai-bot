import os, json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN", "9068888404:AAHYQx12l9NpHewoIczGibTdx8b_XMYhPrc")
ADMIN_ID = 7828093415

# File e save hobe
def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except:
        return {"balances": {}, "stock": {"1Day": [], "3Days": [], "7Days": [], "15Days": [], "30Days": [], "90Days": []}}

def save_data():
    with open("data.json", "w") as f:
        json.dump({"balances": balances, "stock": stock}, f)

data = load_data()
balances = {k: int(v) for k,v in data["balances"].items()}
stock = data["stock"]

prices = {"1Day": 30, "3Days": 70, "7Days": 120, "15Days": 200, "30Days": 350, "90Days": 600}
names = {"1Day": "1 Day", "3Days": "3 Days", "7Days": "7 Days", "15Days": "15 Days", "30Days": "30 Days", "90Days": "90 Days"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bal = balances.get(str(update.effective_user.id), 0)
    text = f"👋 Welcome {update.effective_user.first_name}!\n\n⭐ Aim AI - Premium Bot\n💰 Tomar Balance: ₹{bal}"
    keyboard = [[InlineKeyboardButton("💰 Add Funds", callback_data="add_funds")],[InlineKeyboardButton("⭐ Price List", callback_data="price")],[InlineKeyboardButton("🛒 Buy Key", callback_data="buy")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "add_funds":
        await query.message.reply_text("📱 Add Funds\n\nQR e taka pathiye Screenshot pathao. Admin Balance add kore debe.\nDM: @GamingSasuke1")
    elif query.data == "price":
        await query.message.reply_text("⭐ PRICE LIST\n\n⭐ Aim AI\n  1 Day ➜ ₹30\n  3 Days ➜ ₹70\n  7 Days ➜ ₹120\n  15 Days ➜ ₹200\n  30 Days ➜ ₹350\n  90 Days ➜ ₹600")
    elif query.data == "buy":
        text = "🛒 Buy Key:\n\n"
        for k in prices:
            text += f"{names[k]} - ₹{prices[k]} | Stock: {len(stock[k])} ta\n"
        text += "\nKenar jonno: /buy 1Day"
        await query.message.reply_text(text)

async def buy_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /buy 1Day")
        return
    plan = context.args[0]
    uid = str(update.effective_user.id)
    if len(stock.get(plan, [])) == 0:
        await update.message.reply_text("😔 Stock sesh!")
        return
    bal = balances.get(uid, 0)
    if bal < prices[plan]:
        await update.message.reply_text(f"Balance kom! Dorkar ₹{prices[plan]}, Ache ₹{bal}")
        return
    balances[uid] = bal - prices[plan]
    key = stock[plan].pop(0)
    save_data()
    await update.message.reply_text(f"✅ Purchase Successful!\n\n⭐ Plan: {names[plan]}\n🔑 Key: `{key}`\n💰 Baki Balance: ₹{balances[uid]}", parse_mode="Markdown")

async def addkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    try:
        plan = context.args[0]; key = context.args[1]
        stock[plan].append(key); save_data()
        await update.message.reply_text(f"✅ Add holo! {plan} Stock: {len(stock[plan])} ta")
    except:
        await update.message.reply_text("Use: /addkey 1Day KEY-123")

async def stock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    text = "📦 STOCK:\n\n"
    for k in stock: text += f"{names[k]}: {len(stock[k])} ta\n"
    await update.message.reply_text(text)

async def add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    try:
        uid = str(context.args[0]); amt = int(context.args[1])
        balances[uid] = balances.get(uid, 0) + amt; save_data()
        await update.message.reply_text(f"Add hoye geche! Balance: {balances[uid]}")
    except:
        await update.message.reply_text("Use: /add <user_id> <taka>")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"💰 Balance: ₹{balances.get(str(update.effective_user.id), 0)}")
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⭐ PRICE LIST\n\n⭐ Aim AI\n  1 Day ➜ ₹30\n  3 Days ➜ ₹70\n  7 Days ➜ ₹120\n  15 Days ➜ ₹200\n  30 Days ➜ ₹350\n  90 Days ➜ ₹600")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("price", price))
app.add_handler(CommandHandler("buy", buy_cmd))
app.add_handler(CommandHandler("add", add_balance))
app.add_handler(CommandHandler("addkey", addkey))
app.add_handler(CommandHandler("stock", stock_cmd))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()