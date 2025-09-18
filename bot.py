# This is the main bot logic.
# It handles user commands and channel membership checks.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Your bot's secret information
# For Render deployment, it is safer to use environment variables.
# However, as per your request, the values are hardcoded here.
BOT_TOKEN = "8197222627:AAGjX1XrAqlNnpMYpjSKjA4yOisfeTJbQEk"
PRIVATE_CHANNEL_ID = -1002323042564
PUBLIC_CHANNEL_LINK = "https://t.me/cpa_marketing_99"
OWNER_USERNAME = "@Rs_Rezaul_99"

# Set up logging for better error tracking
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command and checks for channel membership."""
    user = update.effective_user
    
    # Since get_chat_member can raise an error if the user is not in the channel,
    # we use a try-except block to handle it gracefully.
    try:
        member = await context.bot.get_chat_member(chat_id=PRIVATE_CHANNEL_ID, user_id=user.id)
        
        if member.status in ['member', 'administrator', 'creator']:
            keyboard = [
                [
                    InlineKeyboardButton("ওপেন হ্যাক", web_app=WebAppInfo(url="https://as-official-channel.netlify.app/")),
                    InlineKeyboardButton("ওনারের সাথে যোগাযোগ", url=f"https://t.me/{OWNER_USERNAME.replace('@', '')}")
                ],
                [
                    InlineKeyboardButton("আমাদের পাবলিক গ্রুপ", url=PUBLIC_CHANNEL_LINK)
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            welcome_message = (
                f"স্বাগতম {user.first_name}! 🎉\n\n"
                "আপনি আমাদের ভিআইপি কমিউনিটির একজন সম্মানিত সদস্য। আপনার আইডি সফলভাবে যাচাই করা হয়েছে।\n\n"
                "নিচের 'ওপেন হ্যাক' বাটনে ক্লিক করে আপনি আমাদের বিশেষ সুবিধাগুলো উপভোগ করতে পারবেন।"
            )
            
            await update.message.reply_text(welcome_message, reply_markup=reply_markup)
        else:
            raise Exception("User is not a member.")

    except Exception:
        access_denied_message = (
            f"অ্যাক্সেস ডিক্লাইনড, {user.first_name}! 🚫\n\n"
            "আপনি আমাদের ভিআইপি মেম্বার নন। এই বিশেষ সুবিধাটি শুধুমাত্র আমাদের টিমের সদস্যদের জন্য সংরক্ষিত।\n\n"
            "এই হ্যাক ব্যবহার করতে চাইলে, অনুগ্রহ করে টিমে যোগ দিন।"
        )
        await update.message.reply_text(access_denied_message)

async def main() -> None:
    """Starts the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))

    # Run the bot until the user presses Ctrl-C
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
