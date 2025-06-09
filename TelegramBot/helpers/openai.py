from openai import OpenAI
from TelegramBot import config

client_openai = OpenAI(api_key=config.OPENAI_API_KEY)

async def response_openai(text, prompt):
    response_openai = client_openai.responses.create(
    model="gpt-4o",
    instructions = prompt,
    input=str(text),
    )
    return response_openai.output_text