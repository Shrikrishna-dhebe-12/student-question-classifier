# Student Question Classifier

A full-stack AI learning assistant that classifies student questions into academic subjects and returns topic-specific responses.

The project combines Machine Learning, Deep Learning, FastAPI, and a browser-based chat interface.

## Features

- Classifies questions into four subjects:
  - Operating Systems
  - Python
  - Computer Networks
  - Java
- Uses TF-IDF and Logistic Regression for primary classification.
- Uses a TensorFlow/Keras neural network for secondary verification.
- Returns topic-specific answers through a knowledge-based answer engine.
- Provides prediction confidence and ML/DL agreement status.
- Includes a responsive chat interface.
- Exposes REST API endpoints using FastAPI.

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- TensorFlow / Keras
- FastAPI
- Uvicorn
- HTML, CSS, JavaScript

## Project Structure

```txt
student-question-classifier/
│
├── data/
│   └── dataset.csv
│
├── model/
│   ├── ml.pkl
│   ├── dl.keras
│   └── dl_metadata.json
│
├── static/
│   └── index.html
│
├── app.py
├── answer_engine.py
├── config.py
├── data_utils.py
├── predict.py
├── train_ml.py
├── train_dl.py
├── requirements.txt
├── Dockerfile
└── README.md
