import google.generativeai as genai

genai.configure(api_key="AIzaSyBlsaWMbxnC9Fkc-M4bd33LJ-ya9hzgZOk")

for m in genai.list_models():
    print(m.name)