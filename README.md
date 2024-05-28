## Audio Identification

Audio identification is a class of information retrieval systems that matches a query with a set of database documents. The task is to find the most similar track in a database based on a short audio snippet.

This implementation uses Wang's method of frequency pairs and time difference hashes to efficiently match query audio with the database.

![constelation_map_h_1_kernal_16](https://github.com/ruarim/audio_identification/assets/48099261/6f85eddf-7175-4d60-a5b7-6b1e9cd0142f)

The system performs with 80% recall at rank 1 and 90% recall at rank 3.

**Requirements**
Numpy
Librosa
matplotlib
skimage

**Docs**
- Download the GTZAN dataset.
- Configure the file path variables in the main.py script.
- run python3 main.py.
