from datetime import datetime
import os
from flask import Flask, render_template, request
import speech_recognition as sr
from textblob import TextBlob

app = Flask(__name__)

# Home route        
@app.route('/')
def index():
    return render_template('upload.html')

# Upload route
@app.route('/upload', methods=['POST'])
def upload():
    audio = request.files.get('audioFile')
    audio_data = request.form.get('audioData')

    if audio:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'{timestamp}_{audio.filename}'
        folder = 'uploads'
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, filename)
        audio.save(file_path)

        # Perform speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            recorded_audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(recorded_audio, language="en-US")
            print("Decoded Text: {}".format(text))
        except sr.UnknownValueError:
            text = ""
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as ex:
            text = ""
            print("Could not request results from Google Speech Recognition service; {0}".format(ex))

    elif audio_data:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'{timestamp}_recorded_audio.webm'
        folder = 'uploads'
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, filename)
        with open(file_path, 'wb') as f:
            f.write(request.files['audioData'].read())

        # Perform speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            recorded_audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(recorded_audio, language="en-US")
            print("Decoded Text: {}".format(text))
        except sr.UnknownValueError:
            text = ""
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as ex:
            text = ""
            print("Could not request results from Google Speech Recognition service; {0}".format(ex))

    else:
        return 'No audio file found.'

    # Perform sentiment analysis
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    # Display the sentiment analysis results
    if polarity > 0:
        sentiment = 'Positive sentiment'
    elif polarity < 0:
        sentiment = 'Negative sentiment'
    else:
        sentiment = 'Neutral sentiment'

    return render_template('resultx.html', text=text, sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True)
