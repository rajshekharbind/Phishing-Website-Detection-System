#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Save Trained Model & Create Prediction Module
After training your model, use this to save it and create predictions
"""

import pickle
import os
import json
from datetime import datetime

class ModelManager:
    """Manage trained model saving and loading"""
    
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
    
    def save_model(self, model, model_name, feature_names=None, metrics=None):
        """
        Save trained model to pickle file
        
        Args:
            model: Trained sklearn model
            model_name: Name for the model (e.g., 'xgboost_v1')
            feature_names: List of feature names
            metrics: Dictionary with performance metrics
        """
        # Save model
        model_path = os.path.join(self.model_dir, f'{model_name}.pickle')
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        print(f"✓ Model saved: {model_path}")
        
        # Save feature names
        if feature_names:
            features_path = os.path.join(self.model_dir, f'{model_name}_features.pickle')
            with open(features_path, 'wb') as f:
                pickle.dump(feature_names, f)
            print(f"✓ Features saved: {features_path}")
        
        # Save metrics
        if metrics:
            metrics['saved_at'] = datetime.now().isoformat()
            metrics_path = os.path.join(self.model_dir, f'{model_name}_metrics.json')
            with open(metrics_path, 'w') as f:
                json.dump(metrics, f, indent=2)
            print(f"✓ Metrics saved: {metrics_path}")
    
    def load_model(self, model_name):
        """Load model from pickle file"""
        model_path = os.path.join(self.model_dir, f'{model_name}.pickle')
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    
    def load_features(self, model_name):
        """Load feature names"""
        features_path = os.path.join(self.model_dir, f'{model_name}_features.pickle')
        with open(features_path, 'rb') as f:
            features = pickle.load(f)
        return features
    
    def list_models(self):
        """List all saved models"""
        models = [f.replace('.pickle', '') for f in os.listdir(self.model_dir) 
                  if f.endswith('.pickle')]
        return models


class PhishingPredictor:
    """Make predictions using trained model"""
    
    def __init__(self, model_path):
        self.model = pickle.load(open(model_path, 'rb'))
    
    def predict_single(self, features):
        """
        Predict single URL
        
        Args:
            features: List of extracted features
            
        Returns:
            prediction: 1 (phishing) or 0 (legitimate)
            probability: Confidence score
        """
        prediction = self.model.predict([features])[0]
        
        # Get probability if available
        try:
            proba = self.model.predict_proba([features])[0]
            probability = max(proba)
        except:
            probability = None
        
        return {
            'prediction': 'PHISHING' if prediction == 1 else 'LEGITIMATE',
            'label': prediction,
            'confidence': probability
        }
    
    def predict_batch(self, features_list):
        """
        Predict multiple URLs
        
        Args:
            features_list: List of feature lists
            
        Returns:
            predictions: List of predictions
        """
        predictions = self.model.predict(features_list)
        return predictions


# Example Usage
if __name__ == "__main__":
    print("=" * 60)
    print("Model Management & Prediction Module")
    print("=" * 60)
    
    print("\nTo use this module in your notebook:")
    print("""
    # Step 1: After training your model
    from model_manager import ModelManager, PhishingPredictor
    
    manager = ModelManager()
    
    # Step 2: Save your best model
    manager.save_model(
        model=trained_xgboost_model,
        model_name='xgboost_v1',
        feature_names=feature_columns,
        metrics={
            'accuracy': 0.864,
            'precision': 0.85,
            'recall': 0.88,
            'f1_score': 0.865
        }
    )
    
    # Step 3: Load model later
    predictor = PhishingPredictor('models/xgboost_v1.pickle')
    
    # Step 4: Make predictions
    result = predictor.predict_single(url_features)
    print(result)  # {'prediction': 'PHISHING', 'label': 1, 'confidence': 0.92}
    """)
    
    print("\nModel saved files will be in 'models/' directory:")
    print("  - xgboost_v1.pickle (the trained model)")
    print("  - xgboost_v1_features.pickle (feature names)")
    print("  - xgboost_v1_metrics.json (performance metrics)")
