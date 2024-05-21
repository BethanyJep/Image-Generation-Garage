#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = ("AZURE_OPENAI_API_VERSION")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

response = openai.Image.create(
    model="dall-e-3",
    prompt='A photorealistic image of what Kisumu will look like in 2050',
    n=1
)

image_url = response["data"][0]["url"]
print(image_url)