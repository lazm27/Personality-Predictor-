# Personality Predictor: MBTI Chat Analysis

Developed a full-stack NLP application that predicts personality traits based on the Myers-Briggs Type Indicator (MBTI). The system captures real-time user conversations through a custom chat interface, processes text using advanced NLP techniques, and generates a comprehensive psychological profile in PDF format.

## 🚀 Features

* **Real-time Chat Interface:** A custom-built client-server architecture to collect and store user text interactions.
* **NLP Preprocessing Pipeline:** Leverages NLTK and Scikit-learn to clean, tokenize, and vectorize text data for model readiness.
* **ML Prediction Engine:** Implements a Logistic Regression model trained to identify the 16 MBTI personality types based on linguistic patterns.
* **Automated Reporting:** Generates a professional, downloadable PDF evaluation report detailing the user's predicted traits and personality breakdown.

## 🛠️ Tech Stack

* **Languages:** Python, Jupyter Notebook
* **Machine Learning:** Scikit-learn (Logistic Regression), Pandas, NumPy
* **Natural Language Processing:** NLTK (Tokenization, Stopword removal, Stemming)
* **Backend & Connectivity:** Socket Programming (Server/Client) for message collection
* **Reporting:** FPDF / ReportLab (for PDF generation)

## 📁 Project Structure

* `server.py` / `client.py`: Handles the real-time chat data collection.
* `nlp.py`: Contains the text cleaning and preprocessing logic.
* `train.ipynb`: Exploratory Data Analysis (EDA) and model training phase.
* `predict.py`: The inference script that takes user text and outputs a personality type.
* `datasets/`: Training data based on the MBTI 16 Personalities dataset.
* `models/`: Serialized trained models for deployment.

## 📊 Methodology

1. **Data Collection:** Users interact via the `client.py` interface. Messages are stored in a database/log via the `server.py`.
2. **Preprocessing:** Text is converted to lowercase, stripped of URLs/punctuation, and transformed into numerical features using TF-IDF vectorization.
3. **Modeling:** A Logistic Regression model predicts the four MBTI dimensions:
* Introversion (I) vs. Extroversion (E)
* Sensing (S) vs. Intuition (N)
* Thinking (T) vs. Feeling (F)
* Judging (J) vs. Perceiving (P)


4. **Output:** The system aggregates the results into a finalized personality code (e.g., INTJ) and exports a detailed PDF report.

## 📈 Sample Report

The project includes sample outputs such as `personality_analysis_report_laz.pdf`, which showcases the automated trait visualization and descriptions.

---

### How to Run

1. Clone the repository:
```bash
git clone https://github.com/lazm27/Personality-Predictor-.git

```


2. Start the server:
```bash
python server.py

```


3. Run the client to input text:
```bash
python client.py

```


4. Generate the prediction:
```bash
python final_predict.py

```
