from flask import Flask, render_template, request, send_file
from googletrans import Translator
from gtts import gTTS
import os

app = Flask(__name__)
translator = Translator()

@app.route('/')
def index():
    # Provide initial values for input_text, translation, and audio_file
    input_text = ""
    translation = ""
    audio_file = ""

    return render_template('index.html', input_text=input_text, translation=translation, audio_file=audio_file)

@app.route('/translate', methods=['POST'])
def translate():
    if request.method == 'POST':
        text_to_translate = request.form['text_to_translate']
        target_language = request.form['target_language']

        # Translate the text
        translation = translator.translate(text_to_translate, dest=target_language)

        # Save translated text to a temporary file
        temp_filename = 'temp_audio.mp3'
        tts = gTTS(translation.text, lang=target_language)
        tts.save(temp_filename)

        # Pass the input text along with the translation and audio file to the template
        return render_template('index.html', input_text=text_to_translate, translation=translation.text, audio_file=temp_filename)

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(os.getcwd(), filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)