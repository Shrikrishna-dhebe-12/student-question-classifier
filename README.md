
# Student Question Classifier

**Student Question Classifier** is a full-stack AI-powered learning assistant designed to automatically categorize student questions into academic subjects and provide topic-specific responses. The system leverages both traditional machine learning and deep learning models, integrated with a FastAPI backend and a browser-based chat interface.

---

## ✨ Key Features

- **Subject Classification**  
  Automatically classifies questions into four core subjects:  
  - Operating Systems  
  - Python  
  - Computer Networks  
  - Java  

- **Dual-Model Architecture**  
  - **Primary Classification:** TF-IDF + Logistic Regression  
  - **Secondary Verification:** TensorFlow/Keras neural network  

- **Knowledge-Based Answer Engine**  
  Provides accurate, subject-specific answers with confidence scores.  

- **Prediction Transparency**  
  Displays confidence levels and ML/DL agreement status.  

- **Interactive Chat Interface**  
  Responsive browser-based UI for seamless student interaction.  

- **REST API Endpoints**  
  Exposed via FastAPI for integration with external applications.  

---

## 🛠 Tech Stack

- **Languages & Libraries:** Python, Pandas, NumPy, Scikit-learn, TensorFlow/Keras  
- **Backend:** FastAPI, Uvicorn  
- **Frontend:** HTML, CSS, JavaScript  
- **Deployment:** Docker  

---

## 📂 Project Structure

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
```

---

## 🚀 Highlights

- Combines **ML + DL** for robust classification.  
- Offers **confidence-based predictions** with verification.  
- Designed for **scalability and real-world student queries**.  
- Easy deployment with **Dockerized setup**.  

---

