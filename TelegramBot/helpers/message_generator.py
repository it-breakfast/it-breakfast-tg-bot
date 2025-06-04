import requests
from TelegramBot.logging import LOGGER

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

async def generate_message() -> str:
    """
    Генерирует случайное сообщение с помощью Mistral через HuggingFace API.
    """
    try:
        prompt = """<s>[INST] Сгенерируй короткое, забавное сообщение для чата IT-специалистов. 
        Сообщение должно быть на русском языке, не длиннее 2-3 предложений. 
        Тема: тишина в чате, нужно разговорить людей. [/INST]</s>"""
        
        response = requests.post(
            API_URL,
            json={"inputs": prompt, "parameters": {"max_length": 200, "temperature": 0.7}}
        )
        
        if response.status_code == 200:
            return response.json()[0]["generated_text"].split("[/INST]")[-1].strip()
        else:
            LOGGER(__name__).error(f"Ошибка API: {response.status_code}")
            return "Эй, народ! Давайте пообщаемся! 🤖"
            
    except Exception as e:
        LOGGER(__name__).error(f"Ошибка при генерации сообщения: {e}")
        return "Эй, народ! Давайте пообщаемся! 🤖" 
