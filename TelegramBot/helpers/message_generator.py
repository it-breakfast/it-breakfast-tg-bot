import aiohttp
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
        
        LOGGER(__name__).info("Отправляем запрос к HuggingFace API...")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                API_URL,
                json={"inputs": prompt, "parameters": {"max_length": 200, "temperature": 0.7}}
            ) as response:
                LOGGER(__name__).info(f"Получен ответ от API. Статус: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    generated_text = data[0]["generated_text"]
                    LOGGER(__name__).info(f"Сгенерированный текст: {generated_text}")
                    return generated_text.split("[/INST]")[-1].strip()
                else:
                    error_text = await response.text()
                    LOGGER(__name__).error(f"Ошибка API: {response.status}, Ответ: {error_text}")
                    return "Эй, народ! Давайте пообщаемся! 🤖"
            
    except Exception as e:
        LOGGER(__name__).error(f"Ошибка при генерации сообщения: {e}")
        return "Эй, народ! Давайте пообщаемся! 🤖" 
