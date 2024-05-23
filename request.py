import requests
import json
import os

OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

# Define the URL of the API endpoint
url = "https://ominous-disco-5xvgg64jj97hr5v-5000.app.github.dev/generate"

# Define the data you want to send to the API
data = {
    "user_prompt": "1"
}

# # Send a POST request to the API
response = requests.post(url, json=data)

# Print the response from the API
print(response)