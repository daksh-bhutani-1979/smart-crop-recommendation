\# Smart Crop Recommendation System



A machine learning–based crop recommendation system that suggests the most suitable crops

based on soil nutrients and environmental conditions.



This project demonstrates an end-to-end ML workflow including data analysis,

model training, evaluation, and a simple frontend interface.



---



\## Features



\- Recommends suitable crops using ML

\- Input parameters:

  - Nitrogen (N)

  - Phosphorus (P)

  - Potassium (K)

  - Temperature

  - Humidity

  - pH

  - Rainfall

\- Multi-class classification using Random Forest

\- Visual evaluation and explainability

\- Simple frontend for user interaction



---



\## Machine Learning Pipeline



1\. Data preprocessing

2\. Exploratory Data Analysis (EDA)

3\. Model training using Random Forest Classifier

4\. Model evaluation using Confusion Matrix

5\. Feature importance analysis

6\. Crop prediction



---



\## Model Insights



\### Confusion Matrix

\- Strong diagonal dominance

\- Very low class confusion

\- Indicates high prediction accuracy



\### Feature Importance

Top contributing features:

1\. Humidity

2\. Rainfall

3\. Potassium (K)

4\. Phosphorus (P)

5\. Nitrogen (N)



These results align well with real-world agricultural knowledge.



---



## Project Structure

SMART-CROP-RECOMMENDATION
SMART-CROP-RECOMMENDATION/
│
├── train_model.py
├── predict.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│ └── Crop_recommendation.csv
│
├── frontend/
│ ├── index.html
│ ├── styles.css
│ └── app.js
│
├── outputs/
│ ├── confusion_matrix.png
│ ├── correlation_heatmap.png
│ └── feature_importance.png

---



\## Python Version



Tested on \*\*Python 3.10 and 3.11\*\*



\*\*Not compatible with Python 3.13+\*\*

(scikit-learn stability issues observed on newer Python versions)



---



\## Setup Instructions



```bash

git clone <repository-url>

cd SMART-CROP-RECOMMENDATION



python -m venv venv

venv\\\\Scripts\\\\activate   # Windows



pip install -r requirements.txt

python train\\\_model.py

python predict.py


