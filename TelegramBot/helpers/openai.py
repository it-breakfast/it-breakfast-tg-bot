from openai import AsyncOpenAI
from TelegramBot import config

import base64

client_openai = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

async def response_openai(model, text, prompt):
    response_openai = await client_openai.responses.create(
    model=str(model),
    instructions = prompt,
    input=str(text),
    )
    return response_openai.output_text

async def response_openai_image(text):
    response = await client_openai.responses.create(
        model="gpt-4.1-mini",
        input=str(text),
        tools=[
            {
                "type": "image_generation",
                "size": "1024x1024",
                "quality": "low",
            }
        ],
    )

    image_data = [
        output.result
        for output in response.output
        if output.type == "image_generation_call"
    ]

    return base64.b64decode(image_data[0])
