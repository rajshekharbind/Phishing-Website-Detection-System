#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AFTER TRAINING: Save Model Script
Run this in your Jupyter notebook AFTER training to save the model
"""

import pickle
import os
import json
from datetime import datetime

def save_trained_model(model, model_name='best_model', metrics=None):
    """
    Save your trained model from the notebook
    
    Usage in Jupyter Notebook:
    ─────────────────────────
    # After training your XGBoost model:
    from model_saver import save_trained_model
    
    save_trained_model(
        model=xgb_model,  # Your trained model object
        model_name='best_model',
        metrics={
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred)
        }
    )
    """
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Save model
    model_path = f'models/{model_name}.pickle'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✓ Model saved: {model_path}")
    
    # Save metrics if provided
    if metrics:
        metrics['saved_at'] = datetime.now().isoformat()
        metrics_path = f'models/{model_name}_metrics.json'
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"✓ Metrics saved: {metrics_path}")
        print(f"\nModel Performance:")
        for key, value in metrics.items():
            if key != 'saved_at':
                print(f"  - {key}: {value:.4f}")
    
    print(f"\n✓ Model is ready! The Streamlit app will now work.")
    print(f"Run: streamlit run streamlit_app.py")

# Example notebook code
example_code = """
================================================================================
HOW TO USE IN YOUR JUPYTER NOTEBOOK
================================================================================

After training XGBoost model and evaluating it:

─────────────────────────────────────────────────────────────────────────────
# In a Jupyter cell, add this code:

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from model_saver import save_trained_model

# Calculate metrics (example)
y_pred = xgb_model.predict(X_test)

metrics = {
    'accuracy': accuracy_score(y_test, y_pred),
    'precision': precision_score(y_test, y_pred),
    'recall': recall_score(y_test, y_pred),
    'f1_score': f1_score(y_test, y_pred)
}

# Save the model
save_trained_model(
    model=xgb_model,
    model_name='best_model',
    metrics=metrics
)

─────────────────────────────────────────────────────────────────────────────

This will:
1. Create a 'models/' folder
2. Save your trained model as 'models/best_model.pickle'
3. Save metrics as 'models/best_model_metrics.json'
4. The Streamlit app will automatically detect and use it!

================================================================================
"""

if __name__ == "__main__":
    print(example_code)
