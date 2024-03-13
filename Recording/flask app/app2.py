from datetime import datetime
import os
from flask import Flask, render_template, request
import speech_recognition as sr
from textblob import TextBlob

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Upload route
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    audio = request.files.get('audioFile')
    audio_data = request.form.get('audioData')

    if audio:
        # Rename the file using the current date and time
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'{timestamp}_{audio.filename}'

        # Save the file to a new folder
        folder = 'uploads'
        os.makedirs(folder, exist_ok=True)
        audio.save(os.path.join(folder, filename))

        # Perform speech recognition
        file_path = os.path.join(folder, filename)
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            recorded_audio = recognizer.listen(source)

    elif audio_data:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'{timestamp}_recorded_audio.webm'

        # Save the file to a new folder
        folder = 'uploads'
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, filename)
        with open(file_path, 'wb') as f:
            f.write(request.files['audioData'].read())

        # Perform speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            recorded_audio = recognizer.listen(source)

    else:
        return 'No audio file found.'

    # Recognizing the text
    try:
        text = recognizer.recognize_google(
            recorded_audio,
            language="en-US"
        )
        print("Decoded Text : {}".format(text))
    except Exception as ex:
        print(ex)
        text = ""

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

    return render_template('result.html', text=text, sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True)
