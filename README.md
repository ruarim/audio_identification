## Audio Identification

Audio identification is a class of information retrieval systems that matches a query with a set of database documents. The task is to find the most similar track in a database based on a short query snippet.

This implementation uses Wangs method of frequenecy pairs and time difference hashes to efficiently match query audio with the database.

// add combination hashes plot

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