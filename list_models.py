import google.generativeai as genai

API_KEY = " AIzaSyA4skjWkL4Snn-_tWFYLoRIy2XHnC_rAoo"
genai.configure(api_key=API_KEY)

print("Available models:")
for m in genai.list_models():
    print("-", m.name)
