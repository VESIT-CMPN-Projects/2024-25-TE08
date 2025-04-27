import os
import base64
import time
from together import Together
from PIL import Image
import io
import os
together_api_key=os.getenv('TOGETHER_API_KEY')

def generate_image(prompt, save_path=None):
    try:
        # Initialize Together API client
        client = Together(api_key=together_api_key)

        start = time.time()

        # Generate image using Together API
        response = client.images.generate(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-schnell-Free",
            width=1024,
            height=768,
            steps=1,
            n=1,  # Generate only one image
            response_format="b64_json"
        )

        # Extract the base64 image data
        if not response or not response.data:
            raise ValueError("Invalid response received from Together API")

        image_data_b64 = response.data[0].b64_json
        image_data = base64.b64decode(image_data_b64)

        # Convert to image
        image = Image.open(io.BytesIO(image_data))

        end = time.time()
        print(f"Image generation took {end - start} seconds")

        if save_path:
            image.save(save_path)
            return save_path  # Return file path
        else:
            return image  # Return Image object

    except Exception as e:
        print(f"Error generating image: {e}")
        return None
