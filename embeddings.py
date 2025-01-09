from openai import AsyncOpenAI

MODEL = 'text-embedding-3-small'
IMPROVE_MODEL = 'gpt-4o-2024-08-06'

client = AsyncOpenAI()

async def embeddings(text):
    response = await client.embeddings.create(
        input=text,
        model=MODEL,
    )
    return response.data[0].embedding


async def improve(text: str) -> str:
    response = await client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {
                'role': 'system',
                'content': f"Improve the following markdown notes, make it bright with plenty of emojis: {text}"
            }
        ]
    )
    return response.choices[0].message.content

