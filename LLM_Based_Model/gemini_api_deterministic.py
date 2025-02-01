import google.generativeai as genai

genai.configure(api_key="AIzaSyAY7FIW18ZX-Sx9XrOARx866poKxG9Tl1I")

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response_with_config(prompt: str):
    response = model.generate_content(
    prompt,
    generation_config = genai.GenerationConfig(
        temperature=0.1,
        top_p = 0.0,
        top_k= 1
    )
    print(response)
    return response.text
)
