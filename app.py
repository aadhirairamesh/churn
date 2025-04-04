import os
import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib

# Initialize Flask app once
app = Flask(__name__, template_folder='templates')

# Load saved models
try:
    dt_model = joblib.load('models/nate_decision_tree.sav')
    knn_model = joblib.load('models/nate_knn.sav')
    lr_model = joblib.load('models/nate_logistic_regression.sav')
    rf_model = joblib.load('models/nate_random_forest.sav')
    svm_model = joblib.load('models/SVM_model.sav')
    xgb_model = joblib.load('models/XGBoost_model.sav')
    
    loaded_models = {
        'dt': dt_model,
        'knn': knn_model,
        'lr': lr_model,
        'rf': rf_model,
        'svm': svm_model,
        'xgb': xgb_model
    }
except Exception as e:
    print(f"Error loading models: {str(e)}")
    loaded_models = {}

def decode(pred):
    return 'Customer Exits' if pred == 1 else 'Customer Stays'

@app.route('/')
def home():
    result = [
        {'model': 'Decision Tree', 'prediction': ' '},
        {'model': 'K-nearest Neighbors', 'prediction': ' '},
        {'model': 'Logistic Regression', 'prediction': ' '},
        {'model': 'Random Forest', 'prediction': ' '},
        {'model': 'SVM', 'prediction': ' '},
        {'model': 'XGBoost', 'prediction': ' '}
    ]
    
    return render_template('index.html', maind={'customer': {}, 'predictions': result})

@app.route('/predict', methods=['POST'])
def predict():
    if not loaded_models:
        return "Models not loaded", 500
        
    values = list(request.form.values())
    new_array = np.array(values).reshape(1, -1)
    
    cols = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 
            'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 
            'EstimatedSalary']
    
    custd = {k: 'Yes' if v == '1' and k in ['HasCrCard', 'IsActiveMember'] else 'No' 
             if v == '0' and k in ['HasCrCard', 'IsActiveMember'] else v 
             for k, v in zip(cols, values)}
    
    predl = [decode(m.predict(new_array)[0]) for m in loaded_models.values()]
    
    result = [
        {'model': 'Decision Tree', 'prediction': predl[0]},
        {'model': 'K-nearest Neighbors', 'prediction': predl[1]},
        {'model': 'Logistic Regression', 'prediction': predl[2]},
        {'model': 'Random Forest', 'prediction': predl[3]},
        {'model': 'SVM', 'prediction': predl[4]},
        {'model': 'XGBoost', 'prediction': predl[5]}
    ]
    
    return render_template('index.html', maind={'customer': custd, 'predictions': result})

if __name__ == "__main__":
    app.run(debug=True)
