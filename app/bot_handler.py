# # from telegram import Update
# # from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
# # from app.gemini_handler import analyze_user_message, generate_financial_tips, answer_general_question
# # from app.db_utils import add_transaction, get_balance, get_monthly_summary
# # from app.utils.utils import format_money
# # from app.config import Config
# # import asyncio

# # async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     print("🔔 /start command dipanggil oleh", update.effective_user.id)
# #     await update.message.reply_text("👋 Halo! Saya FinBot, asisten keuanganmu. Ketik /bantuan untuk mulai mencatat pemasukan/pengeluaran.")

# # async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     await update.message.reply_text("""
# #     💡 Panduan Penggunaan:
# #     - "Pemasukan 50000"
# #     - "Pengeluaran 15000 untuk makan siang"
# #     - "Saldo"
# #     - "Ringkasan bulan ini"
# #     """)

# # async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     print("📩 Pesan diterima:", update.message.text)
# #     user_id = str(update.effective_user.id)
# #     text = update.message.text.lower().strip()

# #     if "apa itu" in text or "?" in text:
# #         answer = answer_general_question(text)
# #         await update.message.reply_text(answer)
# #         return

# #     analysis = analyze_user_message(text)

# #     if analysis["intent"] in ["income", "expense"]:
# #         amount = analysis["amount"]
# #         desc = analysis.get("description", "tanpa keterangan")
# #         add_transaction(user_id, analysis["intent"], amount, desc)
# #         await update.message.reply_text(f"💰 {'Pemasukan' if analysis['intent']=='income' else 'Pengeluaran'} {format_money(amount)} berhasil dicatat!")

# #     elif analysis["intent"] == "balance":
# #         balance = get_balance(user_id)
# #         await update.message.reply_text(f"💼 Saldo terakhir kamu: {format_money(balance)}")

# #     elif analysis["intent"] == "summary":
# #         summary = get_monthly_summary(user_id)
# #         income = format_money(summary["total_income"])
# #         expense = format_money(summary["total_expense"])
# #         remaining = format_money(summary["total_income"] - summary["total_expense"])

# #         monthly_report = f"""
# # 📊 Ringkasan Bulan Ini:
# # - Total Pemasukan: {income}
# # - Total Pengeluaran: {expense}
# # - Sisa Saldo: {remaining}
# #         """
# #         await update.message.reply_text(monthly_report)

# #         tips = generate_financial_tips(monthly_report)
# #         await update.message.reply_text(tips)

# #     elif analysis["intent"] == "help":
# #         await help_command(update, context)

# #     else:
# #         await update.message.reply_text("Maaf, saya belum mengerti maksud Anda 😅")

# # async def run_telegram_bot():
# #     try:
# #         application = ApplicationBuilder().token(Config.TELEGRAM_BOT_TOKEN).build()

# #         application.add_handler(CommandHandler("start", start))
# #         application.add_handler(CommandHandler("bantuan", help_command))
# #         application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# #         print("✅ Bot Telegram sedang berjalan...")

# #         # Lifecycle manual tanpa wait_for_stop
# #         await application.initialize()
# #         await application.start()
# #         await application.updater.start_polling()

# #         # Tunggu selamanya agar bot tidak langsung mati
# #         await asyncio.Event().wait()

# #     except Exception as e:
# #         print(f"❌ ERROR SAAT MENJALANKAN BOT: {e}")


# import asyncio
# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
# from app.gemini_handler import analyze_user_message, generate_financial_tips, answer_general_question
# from app.db_utils import add_transaction, get_balance, get_monthly_summary
# from app.utils.utils import format_money
# from app.config import Config

# application = None  # Global agar bisa di-shutdown dari luar

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print("🔔 /start command dipanggil oleh", update.effective_user.id)
#     await update.message.reply_text("👋 Halo! Saya FinBot, asisten keuanganmu. Ketik /bantuan untuk mulai mencatat pemasukan/pengeluaran.")

# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("""
#     💡 Panduan Penggunaan:
#     - "Pemasukan 50000(Jika pertama kali pakai, ini akan dihitung saldo awal)"
#     - "Pengeluaran 15000 untuk makan siang"
#     - "Saldo"
#     - "Ringkasan bulan ini"
    
#     **Contoh Penggunaan:**
#     pemasukan 50000 gaji
#     """)

# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print("📩 Pesan diterima:", update.message.text)
#     user_id = str(update.effective_user.id)
#     text = update.message.text.lower().strip()

#     if "apa itu" in text or "?" in text:
#         answer = answer_general_question(text)
#         await update.message.reply_text(answer)
#         return

#     analysis = analyze_user_message(text)

#     if analysis["intent"] in ["income", "expense"]:
#         amount = analysis["amount"]
#         desc = analysis.get("description", "tanpa keterangan")
#         add_transaction(user_id, analysis["intent"], amount, desc)
#         await update.message.reply_text(f"💰 {'Pemasukan' if analysis['intent']=='income' else 'Pengeluaran'} {format_money(amount)} berhasil dicatat!")

#     elif analysis["intent"] == "balance":
#         balance = get_balance(user_id)
#         await update.message.reply_text(f"💼 Saldo terakhir kamu: {format_money(balance)}")

#     elif analysis["intent"] == "summary":
#         summary = get_monthly_summary(user_id)
#         income = format_money(summary["total_income"])
#         expense = format_money(summary["total_expense"])
#         remaining = format_money(summary["total_income"] - summary["total_expense"])

#         monthly_report = f"""
# 📊 Ringkasan Bulan Ini:
# - Total Pemasukan: {income}
# - Total Pengeluaran: {expense}
# - Sisa Saldo: {remaining}
#         """
#         await update.message.reply_text(monthly_report)

#         tips = generate_financial_tips(monthly_report)
#         await update.message.reply_text(tips)

#     elif analysis["intent"] == "help":
#         await help_command(update, context)

#     else:
#         await update.message.reply_text("Maaf, saya belum mengerti maksud Anda 😅")

# async def run_telegram_bot():
#     global application
#     try:
#         application = ApplicationBuilder().token(Config.TELEGRAM_BOT_TOKEN).build()

#         application.add_handler(CommandHandler("start", start))
#         application.add_handler(CommandHandler("bantuan", help_command))
#         application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

#         print("✅ Bot Telegram sedang berjalan...")

#         await application.initialize()
#         await application.start()
#         await application.updater.start_polling()

#         # Tunggu sampai task dibatalkan (CTRL+C)
#         await asyncio.Event().wait()

#     except asyncio.CancelledError:
#         print("📴 Membatalkan bot Telegram...")
#         await shutdown_telegram_bot()
#         raise
#     except Exception as e:
#         print(f"❌ ERROR SAAT MENJALANKAN BOT: {e}")

# async def shutdown_telegram_bot():
#     global application
#     if application:
#         await application.updater.stop()
#         await application.stop()
#         await application.shutdown()
#         print("✅ Bot Telegram dihentikan.")


import asyncio
from turtle import update
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Import fungsi dari modul lain
from app.gemini_handler import analyze_user_message, generate_financial_tips, answer_general_question
from app.db_utils import add_transaction, get_balance, get_monthly_summary
from app.utils.utils import format_money
from app.config import Config

application = None  # Global agar bisa diakses di luar


# --- COMMAND HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    print("🔔 /start command dipanggil oleh", user_id)

    # Auto-register user (sudah otomatis di add_transaction)
    await update.message.reply_text("👋 Halo! Saya FinBot, asisten keuanganmu.\n\n"
                                   "💡 Kamu bisa mulai mencatat pemasukan/pengeluaran seperti:\n"
                                   "- *Pemasukan 50000 gaji mingguan*\n"
                                   "- *Pengeluaran 15000 beli makan siang*\n\n"
                                   "👉 Ketik `/bantuan` untuk lihat panduan lengkap.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
👋 Panduan Penggunaan FinBot:

💰 Catat Transaksi:
- "Pemasukan 50000 gaji"
- "Pengeluaran 15000 beli baju"

💼 Cek Saldo:
- "Saldo"

📊 Ringkasan Bulanan:
- "Ringkasan bulan ini"

❓ Tanya Informasi Keuangan:
- "Apa itu tabungan?"
- "Bagaimana cara hemat uang?"

🤖 Bot akan otomatis simpan data dan beri saran keuangan harian.
    """)


# --- MESSAGE HANDLER ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 Pesan diterima:", update.message.text)
    user_id = str(update.effective_user.id)
    text = update.message.text.lower().strip()

    try:
        if "apa itu" in text or "?" in text:
            answer = answer_general_question(text)
            await update.message.reply_text(answer)
            return

        analysis = analyze_user_message(text)

        if analysis.get("intent") in ["income", "expense"]:
            amount = analysis["amount"]
            desc = analysis.get("description", "tanpa keterangan")
            add_transaction(user_id, analysis["intent"], amount, desc)
            await update.message.reply_text(f"💰 {'Pemasukan' if analysis['intent']=='income' else 'Pengeluaran'} {format_money(amount)} berhasil dicatat!")

        elif analysis.get("intent") == "balance":
            balance = get_balance(user_id)
            await update.message.reply_text(f"💼 Saldo terakhir kamu: {format_money(balance)}")

        elif analysis.get("intent") == "summary":
            summary = get_monthly_summary(user_id)
            income = format_money(summary["total_income"])
            expense = format_money(summary["total_expense"])
            remaining = format_money(summary["total_income"] - summary["total_expense"])

            monthly_report = f"""
            📊 Ringkasan Bulan Ini:
            - Total Pemasukan: {income}
            - Total Pengeluaran: {expense}
            - Sisa Saldo: {remaining}
                        """
            await update.message.reply_text(monthly_report)

            tips = generate_financial_tips(monthly_report)
            await update.message.reply_text(tips)

        elif analysis.get("intent") == "help":
            await help_command(update, context)

        elif analysis.get("intent") == "unknown":
            await update.message.reply_text("Maaf, saya belum bisa memahami maksud Anda 😅\n\nCoba tulis dalam format:\n- Pemasukan 50000\n- Pengeluaran 20000 untuk beli buku")

        else:
            await update.message.reply_text("Maaf, saya belum mengerti maksud Anda 😅")

    except Exception as e:
        print(f"❌ Error saat menangani pesan: {e}")
        await update.message.reply_text("Ups! Ada kesalahan. Silakan coba lagi nanti 😊")


# --- START & SHUTDOWN BOT ---
async def run_telegram_bot():
    global application
    try:
        application = ApplicationBuilder().token(Config.TELEGRAM_BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("bantuan", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        print("✅ Bot Telegram sedang berjalan...")

        await application.initialize()
        await application.start()
        await application.updater.start_polling()

        # Tunggu selamanya sampai dibatalkan
        await asyncio.Event().wait()

    except asyncio.CancelledError:
        print("📴 Membatalkan bot Telegram...")
        await shutdown_telegram_bot()
        raise
    except Exception as e:
        print(f"❌ ERROR SAAT MENJALANKAN BOT: {e}")
        await update.message.reply_text("Terjadi kesalahan pada sistem. Mohon tunggu sebentar...")


async def shutdown_telegram_bot():
    global application
    if application:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()
        print("✅ Bot Telegram dihentikan.")