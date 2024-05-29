from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from openai import OpenAI
import random
from dotenv import load_dotenv
from flask_caching import Cache
import os

# Load the environment variables from the .env file
load_dotenv()

# Secret API Key from OpenAI - Retrieve from Garage Org in OpenAI
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

# Initiate the interaction with any OpenAI services
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Instantiate OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)
api = Api(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

class ImageGenerator(Resource):
    @cache.memoize(timeout=10)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_prompt', required=True, type=str, help='User prompt cannot be blank!')
        args = parser.parse_args()

        descriptive_prompts_list = ["A surrealist oil painting of the Kenyan city {}, with cool tones (blues, greens) and set during a dramatic and high contrast thunderstorm.",
                            "An abstract digital art piece of the Kenyan city {}, with vibrant neon lights, and illuminated by bioluminescent marine life in a nighttime setting.", 
                            "A photorealistic pencil sketch of the Kenyan city {}, with warm tones (reds, yellows) and bathed in the soft light of the golden hour (sunrise/sunset).",
                            "A minimalist mixed media artwork depicting the Kenyan city {}, using bright and vibrant colors and lit by the glow of futuristic billboards at night.",
                            "An impressionist watercolor painting of the Kenyan city {}, with pastel colors and set during an overcast and rainy day.",
                            "A futuristic 3D render of the Kenyan city {}, with sleek, modern architecture, using a monochrome color scheme and lit by the harsh, stark sunlight of the Martian day.",
                            "A vintage-style oil painting of the Kenyan city {}, with dark and moody tones, set during a foggy twilight.",
                            "A hyper realistic digital art piece of the Kenyan city {}, featuring bright neon colors and dynamic, high-contrast lighting of a vibrant night scene.",
                            "An abstract mixed media collage of the Kenyan city {}, using a mix of cool and warm tones, set during a surreal sunset with magical lighting.",
                            "A photorealistic charcoal drawing of the Kenyan city {}, with intricate details, using soft, cool tones and illuminated by the gentle morning light."
                            ]

                # randomize the selection of prompt descriptions
        baseline_prompt = random.choice(descriptive_prompts_list)

        feeling_lucky_prompts_list = ["Depict a group of Maasai warriors dressed in their traditional red shukas, holding spears and shields, standing on the open savannah as the sun rises in the background, casting a golden hue over the landscape.",
                                            "Create an image of the Nairobi city skyline at night, with modern skyscrapers illuminated by city lights, and the iconic Kenyatta International Convention Centre prominently featured.",
                                            "Illustrate a scene from the Maasai Mara National Reserve with a diverse array of wildlife such as lions, elephants, zebras, and giraffes roaming freely across the vast plains, with acacia trees dotting the horizon.",
                                            "Show the vibrant Lamu Cultural Festival with traditional dhow boats on the water, local Swahili architecture, and people in colorful attire participating in dances and celebrations.",
                                            "Depict the breathtaking landscape of the Great Rift Valley with its dramatic escarpments, lush green vegetation, and lakes, possibly including flamingos in Lake Nakuru.",
                                            "Create an image of climbers making their way up the snowy peaks of Mount Kenya, with its rugged terrain and unique flora, such as the giant lobelias and senecios, in the foreground.",
                                            "Illustrate the lush green tea plantations in Kericho, with workers picking tea leaves in the early morning mist, surrounded by rolling hills and blue skies.",
                                            "Show a bustling open-air market with stalls selling fresh produce, colorful textiles, and handmade crafts, with people haggling and interacting, capturing the lively atmosphere.",
                                            "Depict the pristine white sands and crystal-clear waters of Diani Beach, with palm trees swaying in the breeze, and a few beachgoers enjoying the serene environment.",
                                            "Illustrate a scene that captures the cultural diversity of Nairobi, with people from different ethnic backgrounds engaging in various activities, from street food vendors to traditional dancers, set against a backdrop of urban life."]

        # Combine user propmt and descriptive prompt
        def generate_complete_prompt(user_prompt):
            match user_prompt:
                case "1":
                    return baseline_prompt.format("Nairobi, in 2500") 
                case "2":
                    return baseline_prompt.format("Mombasa, in 2270")
                case "3":
                    return baseline_prompt.format("Kisumu, in 2095")
                case "4":
                    return baseline_prompt.format("Nakuru, in 2470")
                case "5":
                    return baseline_prompt.format("Eldoret, in 2150")
                case "6":
                    return baseline_prompt.format("Thika, in 3200")
                case "7":
                    return baseline_prompt.format("Machakos, in 2620")
                case "8":
                    return baseline_prompt.format("Kitale, in 3000")
                case "9":
                    return baseline_prompt.format("Malindi, in 2110")
                case "10":
                    return random.choice(feeling_lucky_prompts_list)

                # User's open ended prompt
                case _:
                    return user_prompt  

        complete_prompt = generate_complete_prompt(args['user_prompt'])

        response = client.images.generate(
            model = "dall-e-3",
            prompt = complete_prompt,
            size = "1024x1024",
            quality = "standard",
            n=1,
        )
        image_url = response.data[0].url
        return {'image_url': image_url}, 200

api.add_resource(ImageGenerator, '/generate')

if __name__ == '__main__':
    app.run(debug=True)