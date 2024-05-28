## Audio Identification

Audio identification is a class of information retrieval systems that matches a query with a set of database documents. The task is to find the most similar track in a database based on a short audio snippet.

This implementation uses Wang's method of frequency pairs and time difference hashes to efficiently match query audio with the database.

<img width="611" alt="Screenshot 2024-05-28 at 11 19 55" src="https://github.com/ruarim/audio_identification/assets/48099261/94981477-0e4a-4c95-aa2c-4e433f9e9587">

The system performs with 80% recall at rank 1 and 90% recall at rank 3.

**Requirements**
- Numpy
- Librosa
- matplotlib
- skimage

**Docs**
- Download the GTZAN dataset.
- Configure the file path variables in the main.py script.
- run python3 main.py.
