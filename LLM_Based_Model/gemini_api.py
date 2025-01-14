import google.generativeai as genai
import os

def ask_gemini(prompt: str):
    genai.configure(api_key="AIzaSyDrwR3jBXMwsbAcANU1wBXSsmv7IBjTgyk")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    print(response)
    return response.text