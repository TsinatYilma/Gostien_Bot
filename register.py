from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

NAME, PHONE, EMAIL, TXN = range(4)

users = []

REGISTRATION_FEE = "500 ETB"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Welcome to Elite Forex VIP Mentorship\n\n"
        "📝 Please enter your Full Name:"
    )
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "📞 Please enter your Phone Number:"
    )
    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text

    await update.message.reply_text(
        "📧 Please enter your Email Address:"
    )
    return EMAIL


async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["email"] = update.message.text

    await update.message.reply_text(
        f"💳 Registration Fee: {REGISTRATION_FEE}\n\n"
        "Send payment to:\n"
        "Telebirr: 09XXXXXXXX\n\n"
        "After payment, send your Transaction Number."
    )
    return TXN


async def get_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["transaction_id"] = update.message.text

    users.append(
        {
            "telegram_id": update.effective_user.id,
            "full_name": context.user_data["name"],
            "phone": context.user_data["phone"],
            "email": context.user_data["email"],
            "transaction_id": context.user_data["transaction_id"],
            "status": "pending_verification",
        }
    )

    await update.message.reply_text(
        "✅ Registration submitted successfully!\n\n"
        "Your payment is pending verification."
    )

    print(users)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Registration cancelled."
    )
    return ConversationHandler.END


def main():
    app = Application.builder().token("8970891992:AAF6rUcZpPOa9gfAzHlZAI8sHW9BHnrzWyE").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_name
                )
            ],
            PHONE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_phone
                )
            ],
            EMAIL: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_email
                )
            ],
            TXN: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_transaction
                )
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()