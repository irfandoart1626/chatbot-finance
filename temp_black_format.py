import google.generativeai as genai
from app.config import Config
import json
import re

genai.configure(api_key=Config.GEMINI_API_KEY)

# def analyze_user_message(message_text):
#     model = genai.GenerativeModel("gemini-2.0-flash")
    
#     prompt = f"""
#     Analisis pesan ini dari pengguna chatbot keuangan:
#     "{message_text}"

#     Jawab dalam format JSON sederhana:
#     {{
#         "intent": "income / expense / balance / summary / help / unknown",
#         "amount": number,
#         "description": string
#     }}

#     Contoh:
#     Pesan: "Hari ini aku beli baju Rp150.000"
#     Output: {{
#       "intent": "expense",
#       "amount": 150000,
#       "description": "beli baju"
#     }}
#     """

#     try:
#         response = model.generate_content(prompt)
        
#         # Cari JSON di dalam respons teks
#         json_text = re.search(r"\{.*\}", response.text, re.DOTALL)
#         if json_text:
#             return json.loads(json_text.group())
#         else:
#             print("❗️Tidak ditemukan JSON dalam respons Gemini")
#             return {"intent": "unknown"}
#     except Exception as e:
#         print("Error with Gemini:", e)
#         return {"intent": "unknown"}
def analyze_user_message(message_text):
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = f"""
    Analisis pesan ini dari pengguna chatbot keuangan:
    "{message_text}"

    Jawab dalam format JSON sederhana:
    {{
        "intent": "income / expense / balance / summary / help / unknown",
        "amount": number,
        "description": string
    }}

    Contoh:
    Pesan: "Hari ini aku beli baju Rp150.000"
    Output: {{
      "intent": "expense",
      "amount": 150000,
      "description": "beli baju"
    }}
    """

    try:
        response = model.generate_content(prompt)
        
        # Coba temukan JSON dalam teks respons
        json_text = re.search(r"\{.*\}", response.text, re.DOTALL)
        
        if json_text:
            try:
                result = json.loads(json_text.group())
                
                # Validasi struktur minimal JSON
                if "intent" in result and result["intent"] in ["income", "expense", "balance", "summary", "help"]:
                    return result
                else:
                    print("❗️Format JSON tidak sesuai")
                    return {"intent": "unknown"}
            except json.JSONDecodeError as je:
                print(f"❌ Gagal parsing JSON: {je}")
                return {"intent": "unknown"}
        else:
            print("❗️Tidak ditemukan JSON dalam respons Gemini")
            return {"intent": "unknown"}
            
    except Exception as e:
        print("🚨 Error dengan Gemini:", e)
        return {"intent": "unknown"}

# def generate_financial_tips(transactions_summary):
#     model = genai.GenerativeModel("gemini-2.0-flash")
    
#     prompt = f"""
#     Berdasarkan riwayat transaksi berikut:
#     {transactions_summary}

#     Tulis saran keuangan harian dalam bahasa Indonesia yang mudah dipahami oleh anak-anak hingga orang tua.
#     Gunakan emoji dan gaya ramah.
#     """
    
#     try:
#         response = model.generate_content(prompt)
#         return response.text.strip()
#     except Exception as e:
#         return "Maaf, saya tidak bisa memberikan saran saat ini 😅"


def generate_financial_tips(transactions_summary):
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = f"""
    Berdasarkan ringkasan transaksi berikut:
    {transactions_summary}

    Buatlah saran keuangan harian yang singkat, jelas, dan informatif.
    Saran ini ditujukan khusus untuk orang dewasa.
    Hindari gaya bahasa kekanak-kanakan, jangan gunakan emoji, dan fokus pada hal yang praktis.
    Gunakan bahasa Indonesia yang mudah dipahami.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Maaf, saat ini tidak bisa memberikan saran keuangan."


def answer_general_question(question):
    model = genai.GenerativeModel("gemini-2.0-flash-preview")
    
    prompt = f"""
    Jawab pertanyaan berikut dengan bahasa Indonesia yang jelas dan santai:
    "{question}"
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Maaf, saya sedang sibuk... coba tanyakan lagi nanti ya 😊"