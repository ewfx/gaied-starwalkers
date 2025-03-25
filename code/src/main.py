import os
import extract_msg
from google import genai

# 1. Retrieve your Generative AI API key (replace with a secure method in production).
my_api_key = "xx"


client = genai.Client(api_key=my_api_key)


msg_file_path = r"d:\deve\hackathon\code\src\test.msg"  # Update this to the correct absolute path of your .msg file



msg = extract_msg.Message(msg_file_path)


email_body = msg.body  # If you want HTML, you can use msg.htmlBody


prompt_text = f"Classify the type of email:\n\n{email_body}"


response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt_text
)


print("Classification:\n", response.text)
