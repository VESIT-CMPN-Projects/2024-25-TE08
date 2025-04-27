import streamlit as st
from generators.translator import translate_story
from PIL import Image
from generators.generate_pdf import get_pdf
from generators.audio_generator import generate_audio
from frontend.quizpage import show_quiz_page
from generators.generate_video import generate_video_from_story  # Import your video generator
import tempfile

# Load a placeholder image
placeholder_image_path = "frontend/assets/loading-placeholder.png"
placeholder_image = Image.open(placeholder_image_path)


# Function to display the output page
def show_output_page_custom():
    st.write("Hello!")
    # """Displays the generated story, images, and multimedia options."""
    # st.write("DEBUG: Entered show_output_page_custom()")  # ✅ Step 1: Ensure function is running
    # st.write(f"DEBUG: Current Page - {st.session_state.get('page', 'N/A')}")  # ✅ Step 2: Check session state
    # st.write(f"DEBUG: Story Output - {st.session_state.get('story_output', 'N/A')}")  # ✅ Step 3: Check story data
    # st.write(f"DEBUG: Generated Images - {st.session_state.get('generated_images', 'N/A')}")  # ✅ Step 4: Check images
    #
    # # Check if quiz is the current page
    # if st.session_state.get("current_page") == "quiz":
    #     show_quiz_page(st.session_state.story_output['quiz'])
    #     return  # Exit function early
    #
    # # Ensure valid session data
    # if st.session_state.story_output and st.session_state.generated_images:
    #     st.title(f"{st.session_state.user_topic.upper()}")
    #
    #     # Display the story and generated images
    #     for i, story_part in enumerate(st.session_state.story_output['story_list']):
    #         translated_part = translate_story(story_part, target_language=st.session_state.selected_language)
    #         st.write(f"{translated_part}")
    #
    #         if st.session_state.generated_images[i] is not None:
    #             st.image(st.session_state.generated_images[i], caption=f"Generated Image {i + 1}", width=300)
    #         else:
    #             st.image(placeholder_image, caption=f"Image {i + 1} could not be generated.", width=300)
    #
    #     st.write("  \n  \n")
    #
    #     # **Audio Generation and Playback**
    #     if "audio_stream" in st.session_state:
    #         st.success("Audio already generated. Listen below:")
    #         st.audio(st.session_state.audio_stream, format="audio/mp3")
    #     else:
    #         if st.button("🎙 Listen to the Story"):
    #             st.success("Generating audio...")
    #             full_story_text = st.session_state.story_output['story']
    #             audio_stream = generate_audio(
    #                 translate_story(full_story_text, target_language=st.session_state.selected_language))
    #
    #             if audio_stream:
    #                 st.session_state.audio_stream = audio_stream.read()
    #                 st.audio(st.session_state.audio_stream, format="audio/mp3")
    #             else:
    #                 st.error("Failed to generate audio.")
    #
    #     st.write("  \n  \n")
    #
    #     # **Generate PDF and Allow Download**
    #     translated_story_list = [translate_story(part, target_language=st.session_state.selected_language)
    #                              for part in st.session_state.story_output['story_list']]
    #     pdf_buffer = get_pdf(st.session_state.user_topic.upper(), translated_story_list,
    #                          st.session_state.generated_images)
    #
    #     st.download_button(
    #         label="Download PDF",
    #         data=pdf_buffer,
    #         file_name=f"{st.session_state.user_topic.upper()}.pdf",
    #         mime="application/pdf"
    #     )
    #
    #     st.write("  \n  \n")
    #
    #     # **Generate and Display Video**
    #     if "video_path" in st.session_state:
    #         st.success("Here is your video:")
    #         st.video(st.session_state.video_path)
    #     else:
    #         if st.button("Generate Video"):
    #             st.success("Generating video, please wait...")
    #             full_story_text = st.session_state.story_output['story']
    #
    #             # Save video temporarily
    #             with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video_file:
    #                 output_video_path = temp_video_file.name
    #
    #             generate_video_from_story(full_story_text, output_video_path)
    #             st.session_state.video_path = output_video_path
    #
    #             st.success("Video generated successfully! ")
    #             st.video(st.session_state.video_path)
    #
    #     st.write("  \n  \n")
    #
    #     # **Quiz Section**
    #     if st.button("Quiz"):
    #         st.session_state.current_page = "quiz"
    #         st.rerun()
    #
    #     st.write("  \n  \n")

        # # **Back to Custom Page Button**
        # if st.button("Back to Custom Page"):
        #     # Clear unnecessary session states before navigating back
        #     for key in ["audio_stream", "pdf_downloaded", "video_path"]:
        #         st.session_state.pop(key, None)
        #
        #     st.session_state.page = "custom"
        #     # Add a final debug message to confirm the function completes
        #     st.write("DEBUG: End of show_output_page_custom()")  # ✅ Step 5
        #     st.rerun()
