Smart Crop Recommendation System:

A machine learning based crop recommendation system that suggests the most suitable crop
based on soil nutrients and environmental conditions.

This project demonstrates an end to end machine learning workflow including data analysis,
model training, evaluation, and a simple frontend interface.


Features:

Crop recommendation using machine learning  
Multi class classification using Random Forest  
Farmer input based prediction flow  
Model evaluation and explainability  
Simple frontend for user interaction  


Input Parameters:

Nitrogen  
Phosphorus  
Potassium  
Temperature  
Humidity  
pH  
Rainfall  


Machine Learning Pipeline:

Data preprocessing  
Exploratory data analysis  
Model training using Random Forest Classifier  
Model evaluation using confusion matrix  
Feature importance analysis  
Crop prediction  


Model Insights:

Confusion Matrix:

Strong diagonal dominance  
Very low class confusion  
Indicates high prediction accuracy  


Feature Importance:

Top contributing features in descending order

Humidity  
Rainfall  
Potassium  
Phosphorus  
Nitrogen  

These results align well with real world agricultural knowledge.


Project Structure:

smart-crop-recommendation

data  
Crop_recommendation.csv  

outputs  
confusion_matrix.png  
correlation_heatmap.png  
feature_importance.png
rf_crop_model.pkl  
label_encoder.pkl  

train_model.py  
farmer_input_mapper.py  
app_like_runner.py  

frontend  
index.html  
styles.css  
app.js  


requirements.txt  
README.md  
.gitignore  


Python Version:

Tested on Python 3.10 and Python 3.11  

Not compatible with Python 3.13 due to stability issues in scikit learn  


Setup Instructions:

git clone <repository-url>  
cd smart-crop-recommendation  

python -m venv venv  
venv\Scripts\activate  

pip install -r requirements.txt  

python train_model.py  
python app_like_runner.py  


Use Case:

This system can be used by farmers, agricultural researchers, and agri tech applications
to determine suitable crops based on soil and climate conditions.


Future Improvements:

Web deployment using Flask or Streamlit  
Integration with real time weather APIs  
Advanced model experimentation  
Mobile friendly user interface  


License:

This project is intended for educational and learning purposes only.