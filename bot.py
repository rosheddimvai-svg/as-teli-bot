# This is the main bot logic.
# It handles user commands and channel membership checks.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

# Your bot's secret information
BOT_TOKEN = "8197222627:AAGjX1XrAqlNnpMYpjSKjA4yOisfeTJbQEk"
PRIVATE_CHANNEL_ID = -1002323042564
PUBLIC_CHANNEL_LINK = "https://t.me/cpa_marketing_99"
OWNER_USERNAME = "@Rs_Rezaul_99"
PORT = 8080
WEBHOOK_URL = "https://dkwin12.com/#/saasLottery/WinGo?gameCode=WinGo_30S&lottery=Win" # Replace with your Render URL

# Set up logging for better error tracking
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command and checks for channel membership."""
    user = update.effective_user
    
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
            
            await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        else:
            raise Exception("User is not a member.")

    except Exception:
        access_denied_message = (
            f"অ্যাক্সেস ডিক্লাইনড, {user.first_name}! 🚫\n\n"
            "আপনি আমাদের ভিআইপি মেম্বার নন। এই বিশেষ সুবিধাটি শুধুমাত্র আমাদের টিমের সদস্যদের জন্য সংরক্ষিত।\n\n"
            "এই হ্যাক ব্যবহার করতে চাইলে, অনুগ্রহ করে টিমে যোগ দিন।"
        )
        await update.message.reply_text(access_denied_message, parse_mode=ParseMode.HTML)

def main() -> None:
    """Starts the bot using webhooks for Render deployment."""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))

    # Run the bot using webhooks
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=WEBHOOK_URL + BOT_TOKEN
    )

if __name__ == "__main__":
    main()

