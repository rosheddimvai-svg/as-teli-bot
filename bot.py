import logging
from aiogram import Bot, Dispatcher, executor, types

# ---------------- CONFIG ----------------
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # এখানে তোমার বট টোকেন বসাও
PRIVATE_CHANNEL_ID = -1002323042564   # প্রাইভেট চ্যানেল আইডি
ADMIN_USERNAME = "@Rs_Rezaul_99"     # এডমিন ইউজারনেম
WEBAPP_URL = "https://as-official-channel.netlify.app/"  # ওয়েব লিংক

# ----------------------------------------
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


# ইউজার প্রাইভেট চ্যানেলে আছে কিনা চেক করার ফাংশন
async def check_membership(user_id: int):
    try:
        member = await bot.get_chat_member(chat_id=PRIVATE_CHANNEL_ID, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except:
        return False


# START কমান্ড
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    is_member = await check_membership(user_id)

    if not is_member:
        text = (
            "❌ <b>Access Declined</b>\n\n"
            "আপনি আমাদের VIP মেম্বার নন।\n"
            f"👉 ভিআইপি মেম্বার হতে হলে এডমিনের সাথে যোগাযোগ করুন: {ADMIN_USERNAME}"
        )
        await message.answer(text)
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("🚀 Open Hack", url=WEBAPP_URL),
        )
        keyboard.add(
            types.InlineKeyboardButton("📞 এডমিনের সাথে যোগাযোগ", url=f"https://t.me/{ADMIN_USERNAME.strip('@')}"),
        )
        keyboard.add(
            types.InlineKeyboardButton("💎 VIP সুবিধাসমূহ", callback_data="vip_info"),
        )

        text = (
            "✅ <b>Access Granted!</b>\n\n"
            "🎉 অভিনন্দন! আপনি আমাদের VIP মেম্বার।\n"
            "🔓 এখন আপনি হ্যাক সিস্টেম ব্যবহার করতে পারবেন।"
        )
        await message.answer(text, reply_markup=keyboard)


# Callback বাটন হ্যান্ডলার
@dp.callback_query_handler(lambda c: c.data == "vip_info")
async def vip_info(callback: types.CallbackQuery):
    await callback.message.answer(
        "💎 <b>VIP মেম্বারদের জন্য বিশেষ সুবিধা:</b>\n"
        "1️⃣ সম্পূর্ণ হ্যাক অ্যাক্সেস\n"
        "2️⃣ এডমিন সাপোর্ট\n"
        "3️⃣ এক্সক্লুসিভ টুলস\n"
    )
    await callback.answer()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
