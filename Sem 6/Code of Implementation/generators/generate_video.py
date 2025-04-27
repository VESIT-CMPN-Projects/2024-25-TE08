from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from generators.audio_generator import generate_audio


def get_story_parts(story):
    sentences = story.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    sentences = [s + '.' for s in sentences]

    n = len(sentences)
    part1 = sentences[:n // 3 + (n % 3 > 0)]
    part2 = sentences[len(part1):len(part1) + n // 3 + (n % 3 > 1)]
    part3 = sentences[len(part1) + len(part2):]

    parts = [part1, part2, part3]
    parts = [' '.join(part) for part in parts]
    return parts


def add_subtitle_to_image(image_path, subtitle, output_path, is_hindi=False):
    """Adds subtitles to an image with proper word wrapping, supporting Hindi text."""
    img = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Load appropriate font
    if is_hindi:
        font_path = "frontend/assets/NotoSansDevanagari-Regular.ttf"  # Ensure the correct path
        try:
            font = ImageFont.truetype(font_path, 40)  # Adjust size if needed
        except IOError:
            font = ImageFont.load_default()
    else:
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            font = ImageFont.load_default()

    # Get image size
    image_width, image_height = img.size

    # Wrap text to fit within image width
    max_chars_per_line = 40  # Adjust as needed
    wrapped_text = textwrap.fill(subtitle, width=max_chars_per_line)

    # Get text dimensions
    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Text position (bottom-center)
    text_x = (image_width - text_width) // 2
    text_y = image_height - text_height - 20  # 20px above bottom

    # Draw semi-transparent black rectangle for contrast
    padding = 10
    rect_x1, rect_y1 = text_x - padding, text_y - padding
    rect_x2, rect_y2 = text_x + text_width + padding, text_y + text_height + padding
    draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], fill=(0, 0, 0, 180))  # Black with transparency

    # Draw wrapped text on the image
    draw.text((text_x, text_y), wrapped_text, font=font, fill="white")

    # Save new image with subtitles
    img.save(output_path)


def generate_video_from_story(story_segments, final_video_path, is_hindi):
    video_clips = []

    output_dir = "generated_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for idx, segment in enumerate(story_segments):
        image_filename = os.path.join(output_dir, f"image_{idx}.png")
        subtitle_image_filename = os.path.join(output_dir, f"image_{idx}_subtitled.png")

        if not os.path.exists(image_filename):
            print(f"Image not found: {image_filename}. Please generate images first.")
            return

        # Add subtitle to image
        add_subtitle_to_image(image_filename, segment, subtitle_image_filename,is_hindi)

        # Generate audio
        audio_stream = generate_audio(segment, is_hindi)
        if audio_stream is None:
            print(f"❌ Video cannot be generated as audio is unavailable for segment {idx + 1}.")
            return None  # Stop execution immediately

        audio_filename = os.path.join(output_dir, f"audio_{idx + 1}.mp3")
        with open(audio_filename, "wb") as f:
            f.write(audio_stream.read())

        # Create video clip
        audio_clip = AudioFileClip(audio_filename)
        image_clip = ImageClip(subtitle_image_filename).set_duration(audio_clip.duration)
        video_clip = image_clip.set_audio(audio_clip)

        video_clips.append(video_clip)

    # Combine all clips into one final video
    final_video = concatenate_videoclips(video_clips, method="compose")
    final_video.write_videofile(final_video_path, fps=24)
    print(f"Video successfully saved at: {final_video_path}")
    return final_video_path


# Function to clear old images from the output directory
def clear_old_images(output_dir):
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            if filename.endswith(".png"):  # Only clear image files
                file_path = os.path.join(output_dir, filename)
                os.remove(file_path)
        print("Old images cleared.")
    else:
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
