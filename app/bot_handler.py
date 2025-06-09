import asyncio
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
            print("🔍 Summary result:", summary)

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
        import traceback
        print(f"❌ Error saat menangani pesan: {e}")
        print(traceback.format_exc())
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

        await asyncio.Event().wait()

    except asyncio.CancelledError:
        print("📴 Membatalkan bot Telegram...")
        await shutdown_telegram_bot()
        raise
    except Exception as e:
        print(f"❌ ERROR SAAT MENJALANKAN BOT: {e}")


async def shutdown_telegram_bot():
    global application
    if application:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()
        print("✅ Bot Telegram dihentikan.")
