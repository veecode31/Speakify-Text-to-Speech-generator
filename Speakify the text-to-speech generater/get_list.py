import edge_tts
import asyncio
from deep_translator import GoogleTranslator


# Function to get the list of available Indian voices
async def get_indian_voices():
    voices = await edge_tts.list_voices()

    # Filter voices to include only those with 'IN' in the language code (Indian voices)
    indian_voices = [voice for voice in voices if 'IN' in voice['ShortName']]
    return indian_voices


# Function to fetch and return the list of Indian voices
def get_voice_list():
    loop = asyncio.get_event_loop()
    indian_voices = loop.run_until_complete(get_indian_voices())
    return indian_voices


def translate_text(text, target_lang):
    """
    Translate text to the target language using deep-translator.
    :param text: The text to translate.
    :param target_lang: The target language code (e.g., 'hi' for Hindi).
    :return: Translated text.
    """
    try:
        translated = GoogleTranslator(target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"[TRANSLATE ERROR] {e}")
        return text
