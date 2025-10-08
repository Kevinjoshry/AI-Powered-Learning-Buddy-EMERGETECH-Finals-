from google import genai

# Replace with your real Gemini API key
client = genai.Client(api_key="AIzaSyA4skjWkL4Snn-_tWFYLoRIy2XHnC_rAoo")

models = client.models.list()
for m in models:
    print(m.name)
