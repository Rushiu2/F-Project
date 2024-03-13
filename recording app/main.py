from flask import Flask, render_template, request, redirect, url_for
import os
import pyaudio
import wave
import speech_recognition as sr
from textblob import TextBlob

app = Flask(__name__)

# Set the path where the recorded audio files will be saved
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to record audio
def record_audio(filename, duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording done.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to perform sentiment analysis
def perform_sentiment_analysis(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        return 'Positive sentiment'
    elif polarity < 0:
        return 'Negative sentiment'
    else:
        return 'Neutral sentiment'

# Route for home page
@app.route('/')
def index():
    return render_template('C:\\Users\\HP\\Desktop\\Project\\Recording\\flask app\\templates\\index.html')

# Route for recording audio
@app.route('/record', methods=['POST'])
def record():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'recording.wav')
        record_audio(filename)
        return redirect(url_for('analyze_sentiment'))

# Route for analyzing sentiment
@app.route('/analyze_sentiment')
def analyze_sentiment():
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'recording.wav')

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

    sentiment_result = perform_sentiment_analysis(text)

    return render_template('C:\\Users\\HP\\Desktop\\Project\\Recording\\flask app\\templates\\result.html', text=text, sentiment=sentiment_result)

if __name__ == '__main__':
    app.run(debug=True)
