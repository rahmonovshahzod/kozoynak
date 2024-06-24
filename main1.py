import requests

# URL of your FastAPI server
url = 'https://1b2c-213-230-111-91.ngrok-free.app/tts'

# Text to be synthesized
text = "Assalomu alaykum"
try:
    response = requests.post(url, json={"text": text})
    response.raise_for_status()

    if response.status_code == 200:
        print("Audio file generated successfully!")
        with open("result_audio.wav", "wb") as f:
            f.write(response.content)
    else:
        print(f"Unexpected status code: {response.status_code}")
        print(response.text)  # Print response content for debugging

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
except Exception as e:
    print(f"Error: {e}")