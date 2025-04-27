import random

from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)


@st.cache_resource
def initialize_llm():
    return ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)


def generate_story(topic):
    story_model = genai.GenerativeModel(model_name="tunedModels/socialstories-my8gxcmyb2vx", )

    story_session = story_model.start_chat(
        history=[]
    )

    boys = ['Ram', 'Rahul', 'Om', 'Rohan']
    girls = ['Riya', 'Meera', 'Nisha', 'Pooja']

    story = story_session.send_message(f"Generate a social story on topic {topic}."
                                       f"For boys name use names like {random.choice(boys)}"
                                       f"For girls name use names like {random.choice(girls)}"
                                       f"Make sure story consists at leas 3 lines").text

    return {
        'story': story,
        'story_list': get_story_parts(story)
    }


def generate_image_prompt(sentence):
    image_prompt_model = genai.GenerativeModel(model_name="tunedModels/imagepromptsgeneration-n56rok7p5r5v", )

    image_prompt_session = image_prompt_model.start_chat(
        history=[]
    )

    image_prompt = image_prompt_session.send_message(sentence).text

    return image_prompt


def generate_quiz(story):
    quiz_model = genai.GenerativeModel(model_name="tunedModels/quiz-dataset-sgcquv6xm4qa", )

    quiz_session = quiz_model.start_chat(
        history=[]
    )

    quiz_text = quiz_session.send_message(
        f"""
        You are an expert educator skilled in creating engaging quizzes. Given the following short story, generate a small quiz with 3 to 5 multiple-choice questions (MCQs). 

        Each question should:
        - Be relevant to the story.
        - Have four answer options (A, B, C, D), with only one correct answer.
        - Test comprehension, inference, or key details of the story.

        ### Story:
        {story}
        ### Output Format:
        [
            {{
                "question": "<Insert a well-formed question based on the story>",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct": "<Correct Answer>"
            }},
            ...
        ]
        """
    ).text

    return quiz_text


def generate_content(topic):
    story_data = generate_story(topic)
    story_sentences = story_data['story_list']
    image_prompts = []
    for i in range(len(story_sentences)):
        image_prompts.append(generate_image_prompt(story_sentences[i]))

    # QUIZ

    quiz_text = generate_quiz(story_data)
    formatted_quiz_text = extract_and_format_quiz(quiz_text)

    print('\n-----------------------------------\n')
    print(formatted_quiz_text)
    print('\n-----------------------------------\n')

    quiz = json.loads(formatted_quiz_text)

    # for prompt in image_prompts:
    #     print(prompt)
    #     print('\n')

    return {
        'story': story_data['story'],
        'story_list': story_data['story_list'],
        'image_prompts': image_prompts,
        'quiz': quiz
    }


def get_story_parts(story):
    sentences = story.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    sentences = [s + '.' for s in sentences]
    # Calculate parts
    n = len(sentences)
    part1 = sentences[:n // 3 + (n % 3 > 0)]
    part2 = sentences[len(part1):len(part1) + n // 3 + (n % 3 > 1)]
    part3 = sentences[len(part1) + len(part2):]

    # Combine into parts
    parts = [part1, part2, part3]
    parts = [' '.join(part) for part in parts]
    print(parts)
    print(len(parts))
    return parts

def extract_and_format_quiz(model_output):
    # Remove extra newlines and spaces
    cleaned_output = model_output.strip()

    # Extract JSON-like objects using regex (only valid {...} blocks)
    json_objects = re.findall(r'\{[^{}]*\}', cleaned_output, re.DOTALL)

    if not json_objects:
        raise ValueError("No valid JSON-like content found")

    # Filter out any empty {} objects
    json_objects = [obj for obj in json_objects if len(obj) > 2]  # Ensure it's not just {}

    # Wrap in a valid JSON array
    formatted_json_str = "[" + ", ".join(json_objects) + "]"

    try:
        quiz_data = json.loads(formatted_json_str)  # Validate JSON
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON decoding error: {e}")

    return json.dumps(quiz_data, indent=4)  # Pretty format JSON
