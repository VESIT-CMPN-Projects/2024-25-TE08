import random
import json
import streamlit as st
from streamlit_lottie import st_lottie
from generators.model import generate_content
from generators.generate_image import generate_image  # Import the function from the earlier step
from concurrent.futures import ThreadPoolExecutor
from frontend.outputpage import show_output_page  # Import the function from outputpage.py
from frontend.custom import show_custom_page
from generators.translator import INDIAN_LANGUAGES  # Import the translator and language mapping

colors = ['red', 'green', 'blue', 'yellow', 'orange','white']
attire_mapping = {
    'boy': {
        'bn': 'a traditional Bengali dhoti and kurta',
        'gu': 'a Gujarati kediyu and dhoti',
        'hi': 'Indian traditional kurta-pajama',
        'kn': 'a Kannada panche with a kurta',
        'ml': 'a Kerala kasavu mundu with a shirt',
        'mr': 'a Marathi dhoti with a kurta',
        'ne': 'a Nepali daura-suruwal',
        'or': 'an Odia dhoti and kurta',
        'pa': 'a Punjabi kurta-pajama with a turban',
        'sd': 'a Sindhi ajrak kurta with a shalwar',
        'ta': 'a Tamil veshti with an angavastram',
        'te': 'a Telugu kurta with a dhoti',
        'ur': 'a South Asian sherwani or kurta-pajama',
        'en': None  # No cultural attire for English
    },
    'girl': {
        'bn': 'a traditional Bengali sari',
        'gu': 'a Gujarati chaniya choli',
        'hi': 'an Indian lehenga choli',
        'kn': 'a Kannada ilkal saree',
        'ml': 'a Kerala kasavu saree',
        'mr': 'a Marathi nauvari saree',
        'ne': 'a Nepali gunyo cholo',
        'or': 'an Odia sambalpuri saree',
        'pa': 'a Punjabi salwar kameez',
        'sd': 'a Sindhi ajrak dupatta with a kurta',
        'ta': 'a Tamil half-sari',
        'te': 'a Telugu pattu langa',
        'ur': 'a South Asian salwar kameez',
        'en': None  # No cultural attire for English
    }
}


# Initialize session state for user_topic, story_output, generated_images, page, and selected_language
if 'user_topic' not in st.session_state:
    st.session_state.user_topic = ""
if 'story_output' not in st.session_state:
    st.session_state.story_output = None
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []  # To store generated images
if 'page' not in st.session_state:
    st.session_state.page = "home"  # Add a session state for the current page
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = "en"  # Default to English

# Streamlit UI

def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_loading_screen = load_lottie("frontend/assets/loading-screen-animation.json")

# Initialize session state to check if splash screen has been shown
if 'loading_shown' not in st.session_state:
    st.session_state['loading_shown'] = False

# Streamlit UI Home Page
if st.session_state.page == "home":
    st.title("📚 Story GPT")
    st.write("Enter a topic, and I'll generate a social story for you!")

    # User input
    st.session_state.user_topic = st.text_input("Enter a topic for the story:", st.session_state.user_topic)

    # Language selection dropdown
    st.session_state.selected_language = st.selectbox(
        "Select a language for the story:",
        options=["en"] + list(INDIAN_LANGUAGES.keys()),
        format_func=lambda code: "English" if code == "en" else INDIAN_LANGUAGES[code].capitalize()

    )
    target_language = st.session_state.selected_language
    cultural_attire = attire_mapping.get(target_language, 'default cultural attire')
    if st.button("Generate Story"):
        if st.session_state.user_topic:
            with st.spinner("Generating story and images ..."):
                # Splash screen logic
                if not st.session_state['loading_shown']:
                    st_lottie(
                        lottie_loading_screen,
                        speed=2,
                        reverse=False,
                        loop=True,
                        height=270,
                        width=None
                    )
                # Generate story content
                result = generate_content(st.session_state.user_topic)

                if result and result['story'] != '':



                    st.session_state.story_output = result  # Store output in session state
                    st.session_state.generated_images = []  # Clear previous images

                    # Prepare the full image prompts

                    context_description = (
                        f"the kid with black hair, wearing a {random.choice(['red', 'green', 'blue', 'yellow'])} shirt and black pants. "
                        "Image generated must be animated."
                        f"This image is generated for a story based on topic {st.session_state.user_topic}"
                    )

                    # Generate image prompts
                    image_prompts = [
                        f"{result['image_prompts'][i]}. Depict {context_description}."
                        for i in range(len(result['image_prompts']))
                    ]

                    # Function to generate images in parallel
                    def generate_image_concurrently(prompt,index):
                       save_path = f"generated_images/image_{index}.png"
                       return generate_image(prompt, save_path)

                    # Use ThreadPoolExecutor to generate images concurrently
                    with ThreadPoolExecutor() as executor:
                        generated_images = list(executor.map(generate_image_concurrently, image_prompts, range(len(image_prompts))))

                    # Store the generated images in session state
                    for image in generated_images:
                        st.session_state.generated_images.append(image)

                    # Switch to the output page
                    st.session_state.page = "output"
                    st.rerun()  # Rerun to refresh the page and switch to output
                else:
                    st.warning('Topic may be explicit or invalid.')
        else:
            st.warning("Please enter a topic.")

    st.write("Or")
    if st.button("Custom Generation"):  # CHANGES MADE
        st.session_state.page = "custom"  # CHANGES MADE
        st.rerun()  # CHANGES MADE

# If page is set to 'output', call the show_output_page function
if st.session_state.page == "output":
    show_output_page()
elif st.session_state.page == "custom":  # CHANGES MADE
    show_custom_page()  # CHANGES MADE
