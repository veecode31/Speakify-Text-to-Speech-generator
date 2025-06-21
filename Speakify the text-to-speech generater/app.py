from flask import Flask, render_template, request, send_file
import edge_tts
import asyncio
import os
import time
from get_list import get_voice_list, translate_text  # Updated import

app = Flask(__name__)
OUTPUT_FOLDER = "static"  # Save audio files in the static folder

# Indian English and Hindi voices
VOICE_LIST = get_voice_list()


# Function to convert text to speech
async def text_to_speech(text, voice, output_file):
    try:
        tts = edge_tts.Communicate(text, voice)
        await tts.save(output_file)
    except Exception as e:
        print(f"[TTS ERROR] {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    text = ""
    translated_text = ""
    audio_file = None

    # Default to the first voice's ShortName if available
    selected_voice = VOICE_LIST[0]['ShortName'] if VOICE_LIST else None

    if request.method == 'POST':
        text = request.form['text']
        selected_voice_shortname = request.form['voice']
        target_lang = request.form.get('target_lang', '')  # Get target language

        # Validate and assign the selected voice
        if selected_voice_shortname:
            selected_voice = selected_voice_shortname  # ShortName is used for text-to-speech

        # Translate if target language is provided and not empty
        if target_lang and text.strip():
            translated_text = translate_text(text, target_lang)
        else:
            translated_text = text

        if translated_text.strip():
            timestamp = int(time.time())
            audio_file = f"{OUTPUT_FOLDER}/output_{timestamp}.mp3"
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(text_to_speech(translated_text, selected_voice, audio_file))

            return render_template('index.html', text=text, translated_text=translated_text, audio_file=audio_file,
                                   voices=VOICE_LIST, selected_voice=selected_voice)

    return render_template('index.html', text=text, translated_text=translated_text, audio_file=None,
                           voices=VOICE_LIST, selected_voice=selected_voice)

@app.route('/download/<filename>')
def download(filename):
    return send_file(f"{OUTPUT_FOLDER}/{filename}", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

















