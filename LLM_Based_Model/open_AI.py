from openai import OpenAI
client = OpenAI()

def execute_prompt(message: str):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store = True,
        messages = [{"role": "user", "content": message}]
    )
    return completion.choices[0].message.content