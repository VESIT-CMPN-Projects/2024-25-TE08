from deep_translator import GoogleTranslator

def translate_text(text, target_language):
    try:
        translated = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translated
    except Exception as e:
        return f"An error occurred during translation: {e}"

INDIAN_LANGUAGES = {
    # 'bn': 'bengali',
    # 'gu': 'gujarati',
    'hi': 'hindi',
    # 'kn': 'kannada',
    # 'ml': 'malayalam',
    # 'mr': 'marathi',
    # 'ne': 'nepali',
    # 'or': 'odia',
    # 'pa': 'punjabi',
    # 'sd': 'sindhi',
    # 'ta': 'tamil',
    # 'te': 'telugu',
    # 'ur': 'urdu'
}
