from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("APi")
import google.generativeai as genai

# Substitua pela sua chave real
GEMINI_API_KEY = "AIzaSyBwtAboN7mbKCr8QL1Hyaxb9kxCmYwf944"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

try:
    response = model.generate_content("")
    print("Resposta da IA:")
    print(response.text)
except Exception as e:
    print("Erro ao chamar a IA:")
    print(e)
