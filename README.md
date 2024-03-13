# F-Project { Emotion-Sense }

Speech Emotion Recognition The objective of this notebook is to classify from raw sound waves to six emotions: happy, sad, neutral, fear, angry, and disgust.

Gathering data Quick EDA Preprocess Extract features Build a LSTM Evaluate and conclude Datasets:

Crowd-sourced Emotional Multimodal Actors Dataset (Crema-D) Ryerson Audio-Visual Database of Emotional Speech and Song (Ravdess) Surrey Audio-Visual Expressed Emotion (Savee) Toronto Emotional Speech Set (Tessa)

Gathering data We will gather speech data from four datasets and store it in a single dataframe along with the corresponding file paths, gender labels and emotion labels. The size of each respective dataframe will be specified, along with an example filename in which the emotion label is bolded.
A. Ravdess Dataframe

There are 1440 audio files, for example, 03-01-06-01-02-01-12.wav.

B. Crema-D Dataframe

There are 7,442 audio files, for example, 1001_DFA_ANG_XX.wav.

C. Tess Dataframe

There are 2,800 audio files, for example, OAF_base_fear.wav.

D. Savee Dataframe

There are 480 audio files, for example, DC_a02.wav.

Quick EDA We check for imbalances like male to female ratio.

Preprocess The following steps will be followed to preprocess the audio:

Get an array of samples Trim the silence Padding for equal length

Extract features We will only extract these features:
Mel-Frequency Cepstral Coefficients: captures the shape of the spectral envelope of a signal Zero Crossing Rate: captures the number of times a signal changes sign per second Root Mean Square Energy: captures the root mean square amplitude of the audio signal

Build a LSTM Before building the model, we will have to setup the data. LSTM are great for sequences.

Evaluate and conclude Let's see how good are model is.
