# Audio Identification

Audio identification is a class of information retrieval systems designed to match a query with a set of database documents. The objective is to find the most similar track in a database using a short audio snippet.

This implementation utilizes **Wang's fingerprinting method**, leveraging frequency pairs and time difference hashes to efficiently match query audio with the database.

![Audio Identification Diagram](https://github.com/ruarim/audio_identification/assets/48099261/94981477-0e4a-4c95-aa2c-4e433f9e9587)

## Performance

- **80% Recall** at Rank 1  
- **90% Recall** at Rank 3  
- Dataset: [GTZAN Music Dataset](http://marsyas.info/downloads/datasets.html)

## Requirements

The following Python libraries are required:

- **Numpy**
- **Librosa**
- **Matplotlib**
- **Skimage**

Install the required packages via pip:

```bash
pip install numpy librosa matplotlib scikit-image
