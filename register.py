from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# States
NAME, PHONE, EMAIL, SCREENSHOT = range(4)

# Configuration
BOT_TOKEN = "8970891992:AAF6rUcZpPOa9gfAzHlZAI8sHW9BHnrzWyE"
ADMIN_ID = 5682025501  # Replace with your Telegram ID
REGISTRATION_FEE = "5000 ETB"


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
        "Telebirr: 0998644082\n\n"
        "📸 After payment, upload a screenshot of your payment confirmation.\n\n"
        "An admin will review your payment and add you to the VIP channel after approval."
    )

    return SCREENSHOT


async def get_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text(
            "❌ Please upload a screenshot image."
        )
        return SCREENSHOT

    photo = update.message.photo[-1]

    username = (
        f"@{update.effective_user.username}"
        if update.effective_user.username
        else "None"
    )

    caption = (
        "🔥 NEW REGISTRATION\n\n"
        f"👤 Full Name: {context.user_data['name']}\n"
        f"📞 Phone: {context.user_data['phone']}\n"
        f"📧 Email: {context.user_data['email']}\n"
        f"🆔 Telegram ID: {update.effective_user.id}\n"
        f"👤 Username: {username}"
    )

    # Send screenshot to admin
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=caption
    )

    await update.message.reply_text(
        "✅ Registration submitted successfully!\n\n"
        "Your payment screenshot has been sent to the admin for verification.\n\n"
        "Once approved, you will be added to the VIP channel."
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Registration cancelled."
    )
    return ConversationHandler.END


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start)
        ],
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
            SCREENSHOT: [
                MessageHandler(
                    filters.PHOTO,
                    get_screenshot
                )
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )

    app.add_handler(conv_handler)

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()