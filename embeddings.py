from openai import OpenAI

MODEL = 'text-embedding-3-small'
IMPROVE_MODEL = 'gpt-4o'

client = OpenAI()

def embeddings(text):
    response = client.embeddings.create(
        input=text,
        model=MODEL,
    )
    return response.data[0].embedding


def improve(text):
    response = client.completions.create(
        input=text,
        model=IMPROVE_MODEL,
    )
    return response.choices[0].text
