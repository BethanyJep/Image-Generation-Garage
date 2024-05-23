from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from openai import OpenAI
import random
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

# Secret API Key from OpenAI - Retrieve from Garage Org in OpenAI
# OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

# Initiate the interaction with any OpenAI services
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

app = Flask(__name__)
api = Api(app)

class ImageGenerator(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_prompt', required=True, type=int, help='User prompt cannot be blank!')
        args = parser.parse_args()

        descriptive_prompts_list = ["A surrealist oil painting of {} city in Kenya, inspired by Salvador Dalí, with cool tones (blues, greens) and set during a dramatic and high contrast thunderstorm.",
                                    "An abstract digital art piece of {} city in Kenya, with vibrant neon lights, inspired by Wassily Kandinsky, and illuminated by bioluminescent marine life in a nighttime setting.", 
                                    "A photorealistic pencil sketch of {} city in Kenya, with warm tones (reds, yellows) and bathed in the soft light of the golden hour (sunrise/sunset), emulating the style of John Constable."]
        baseline_prompt = random.choice(descriptive_prompts_list)

        def generate_complete_prompt(user_prompt):
            return baseline_prompt.format(user_prompt)

        complete_prompt = generate_complete_prompt(args['user_prompt'])

        # Instantiate OpenAI client
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.images.generate(
            model = "dall-e-3",
            prompt = complete_prompt,
            size = "1024x1024",
            quality = "hd",
            n=1,
        )

        image_url = response.data[0].url
        return {'image_url': image_url}, 200

api.add_resource(ImageGenerator, '/generate')

if __name__ == '__main__':
    app.run(debug=True)