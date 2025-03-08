import google.generativeai as genai
import os

def ask_gemini(prompt: str):
    genai.configure(api_key="AIzaSyAY7FIW18ZX-Sx9XrOARx866poKxG9Tl1I")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    print(response)
    return response.text