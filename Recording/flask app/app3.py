from flask import Flask, render_template, request, jsonify
import librosa
import numpy as np

app = Flask(__name__)

# Simulated sentiment analysis function
def analyze_sentiment(audio_path):
    # In a real scenario, you would use a pre-trained sentiment analysis model here
    # This is a placeholder, and you need to replace it with an actual model
    # The sentiment labels could be 'happy', 'sad', 'angry', 'neutral', etc.
    return np.random.choice(['happy', 'sad', 'angry', 'neutral'])

# Route for home page
@app.route('/')
def index():
    return render_template('C:\\Users\HP\\Desktop\\Project\\Recording\\flask app\\templates\\index.html')

# Route for analyzing audio sentiment
@app.route('/analyze_sentiment', methods=['POST'])
def analyze_audio_sentiment():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    if file:
        try:
            # Save the uploaded file temporarily
            audio_path = 'C:\\Users\\HP\\Desktop\\Project\\Recording\\uploads\\2023-10-30_17-10-06_2023-06-05_18-39-16_harvard.wav'
            file.save(audio_path)

            # Perform sentiment analysis on the audio
            sentiment_result = analyze_sentiment(audio_path)

            return jsonify({'sentiment': sentiment_result})
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            # Remove the temporary audio file
            if os.path.exists(audio_path):
                os.remove(audio_path)

if __name__ == '__main__':
    app.run(debug=True)
