This is a web application on flask,
which allows perform basic manipulations with audio files of the .wav format: changing the volume, 
changing the playback speed, transcribing speech into text (using the fast-whisper model) 

Doker:
sudo docker build -t nlp .
sudo docker run -p 5000:5000 nlp