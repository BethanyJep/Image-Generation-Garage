import os
from openai import OpenAI
import random

# Secret API Key from OpenAI - Retrieve from Garage Org in OpenAI
OPENAI_API_KEY= ""

# Initiate the interaction with any OpenAI services
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Instantiate OpenAI client
client = OpenAI()

# Helper function to generate image from DALL-E 3 API
def get_image_from_DALL_E_3_API(user_prompt, 
                                image_dimension="1024x1024", 
                                image_quality="hd", 
                                model="dall-e-3", 
                                nb_final_image=1):
    
    response = client.images.generate(
      model = model,
      prompt = user_prompt,
      size = image_dimension,
      quality = image_quality,
      n=nb_final_image,
    )

    image_url = response.data[0].url
    print(image_url)

descriptive_prompts_list = ["A surrealist oil painting of {} city in Kenya, inspired by Salvador Dalí, with cool tones (blues, greens) and set during a dramatic and high contrast thunderstorm.",
                             "An abstract digital art piece of {} city in Kenya, with vibrant neon lights, inspired by Wassily Kandinsky, and illuminated by bioluminescent marine life in a nighttime setting.", 
                             "A photorealistic pencil sketch of {} city in Kenya, with warm tones (reds, yellows) and bathed in the soft light of the golden hour (sunrise/sunset), emulating the style of John Constable."]

# randomize the selection of prompt descriptions
baseline_prompt = random.choice(descriptive_prompts_list)

# Combine user propmt and descriptive prompt
def generate_complete_prompt(user_prompt):
    match user_prompt:
        case 1:
            return baseline_prompt.format("Kisumu in 2050") 
        case 2:
            return baseline_prompt.format("Mombasa in 2100")
        case 3:
            return baseline_prompt.format("Nairobi in 2030")

        # User's open ended prompt
        case _:
            return user_prompt
        
complete_prompt = generate_complete_prompt(2)
print("The wheel landed on: " + complete_prompt)
get_image_from_DALL_E_3_API(complete_prompt)