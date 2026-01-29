#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete Workflow Guide After Model Training
Step-by-step instructions for using the trained phishing detection model
"""

def print_workflow():
    workflow = """
================================================================================
                AFTER MODEL TRAINING - NEXT STEPS
================================================================================

STEP 1: MODEL EVALUATION & ANALYSIS
────────────────────────────────────────────────────────────────────────────
✓ Check Model Performance Metrics:
  - Accuracy: How many predictions are correct
  - Precision: Of positive predictions, how many are correct
  - Recall: Of actual phishing, how many did we catch
  - F1-Score: Balance between precision and recall
  - Confusion Matrix: True/False Positives/Negatives
  - ROC-AUC Score: Model's ability to distinguish classes

✓ Analyze Results:
  - Compare all 6 models (Decision Tree, Random Forest, MLP, XGBoost, Autoencoder, SVM)
  - Select best performing model (XGBoost typically best ~86.4%)
  - Check for overfitting/underfitting


STEP 2: SAVE THE TRAINED MODEL
────────────────────────────────────────────────────────────────────────────
Save your best model in pickle format:

    import pickle
    
    # Save model
    with open('best_model.pickle', 'wb') as f:
        pickle.dump(best_model, f)
    
    # Also save the feature names for later use
    with open('feature_names.pickle', 'wb') as f:
        pickle.dump(feature_names, f)


STEP 3: CREATE PREDICTION FUNCTION
────────────────────────────────────────────────────────────────────────────
Build a function to make predictions on new URLs:

    def predict_phishing(url):
        # Extract features from URL
        features = extract_features(url)
        
        # Make prediction using saved model
        prediction = loaded_model.predict([features])
        
        # Return result
        return "PHISHING" if prediction[0] == 1 else "LEGITIMATE"


STEP 4: BUILD A WEB APPLICATION (OPTIONAL BUT RECOMMENDED)
────────────────────────────────────────────────────────────────────────────
Options:

A) FLASK WEB APP (Python)
   - Create a simple web interface
   - User pastes URL → Get result instantly
   - Deploy on localhost or cloud

B) STREAMLIT APP (Easiest)
   - No HTML/CSS needed
   - Just pure Python
   - User-friendly interface

C) DJANGO (Enterprise)
   - Full-featured web framework
   - Database integration
   - User authentication


STEP 5: CREATE PREDICTION API
────────────────────────────────────────────────────────────────────────────
Build REST API for programmatic access:

    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    @app.route('/predict', methods=['POST'])
    def predict():
        url = request.json['url']
        result = predict_phishing(url)
        return jsonify({'url': url, 'prediction': result})


STEP 6: TESTING & VALIDATION
────────────────────────────────────────────────────────────────────────────
✓ Test with known phishing URLs
✓ Test with known legitimate URLs
✓ Test edge cases (very long URLs, special characters, etc.)
✓ Create confusion matrix for detailed analysis
✓ Generate classification report


STEP 7: DEPLOYMENT OPTIONS
────────────────────────────────────────────────────────────────────────────
1. LOCAL DEPLOYMENT
   - Run as Python script
   - Desktop application

2. WEB SERVER DEPLOYMENT
   - Heroku (free tier available)
   - AWS, Google Cloud, Azure
   - DigitalOcean, Linode

3. DOCKER CONTAINERIZATION
   - Package app with all dependencies
   - Easy to deploy anywhere

4. MOBILE APP
   - Create Android/iOS app
   - Backend: trained model API
   - Frontend: user interface


STEP 8: MONITORING & MAINTENANCE
────────────────────────────────────────────────────────────────────────────
✓ Track prediction accuracy in production
✓ Retrain model periodically with new data
✓ Monitor for model drift
✓ Update model when accuracy drops
✓ Keep logs of predictions


STEP 9: DOCUMENTATION
────────────────────────────────────────────────────────────────────────────
Document:
- Model architecture & hyperparameters
- Feature descriptions
- Usage instructions
- API endpoints
- Deployment steps
- Known limitations


RECOMMENDED QUICK START (NEXT 2 HOURS)
────────────────────────────────────────────────────────────────────────────
1. Save the best trained model to pickle file
2. Test predictions on sample URLs
3. Create a simple prediction script
4. Build a Streamlit web app for testing


EXAMPLE PROJECT STRUCTURE AFTER TRAINING
────────────────────────────────────────────────────────────────────────────
Phishing-Website/
├── models/
│   ├── best_model.pickle          ← Trained model
│   └── feature_names.pickle       ← Feature names
├── app.py                         ← Flask/Streamlit app
├── prediction.py                  ← Prediction functions
├── features/
│   └── extraction.py              ← Feature extraction
├── test_model.py                  ← Testing script
└── requirements.txt               ← Dependencies


NEXT ACTION ITEMS
────────────────────────────────────────────────────────────────────────────
[ ] Step 1: Evaluate model performance
[ ] Step 2: Save best model to pickle
[ ] Step 3: Create prediction function
[ ] Step 4: Test on new URLs
[ ] Step 5: Build web app (Flask/Streamlit)
[ ] Step 6: Deploy to cloud (optional)


QUESTIONS TO ASK YOURSELF
────────────────────────────────────────────────────────────────────────────
1. Which model performed best? (XGBoost typically wins)
2. Is 86%+ accuracy good enough for your use case?
3. Do you need a web interface or API?
4. Should this run on cloud or locally?
5. How will you handle new URLs not in training data?

================================================================================
"""
    print(workflow)

if __name__ == "__main__":
    print_workflow()
