import openai

openai.api_key = "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"


def generate_response(message):
    prompt = f"User: {message}\nAI:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
    )
    chat_response = response.choices[0].text.strip()
    return chat_response
