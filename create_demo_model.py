#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DEMO: Create a Sample Trained Model for Testing
This demonstrates what you need to do after training
"""

import os
import pickle
import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from datetime import datetime

def create_demo_model():
    """
    Create a demo trained model (simulating real training)
    This is JUST for testing - in real use, train on your actual data
    """
    
    print("=" * 70)
    print("CREATING DEMO MODEL FOR TESTING STREAMLIT APP")
    print("=" * 70)
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    print("\n✓ Created 'models/' directory")
    
    # Create synthetic training data (simulating 17 features)
    print("\nGenerating sample data...")
    X_train = np.random.randint(0, 2, size=(100, 17))  # 100 samples, 17 features
    y_train = np.random.randint(0, 2, size=100)  # Binary labels
    
    X_test = np.random.randint(0, 2, size=(30, 17))
    y_test = np.random.randint(0, 2, size=30)
    
    # Train a simple Random Forest model
    print("Training model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred, zero_division=0)),
        'recall': float(recall_score(y_test, y_pred, zero_division=0)),
        'f1_score': float(f1_score(y_test, y_pred, zero_division=0)),
        'saved_at': datetime.now().isoformat(),
        'model_type': 'Random Forest (Demo)',
        'samples_trained': 100,
        'features': 17
    }
    
    # Save model
    model_path = 'models/best_model.pickle'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✓ Model saved: {model_path}")
    
    # Save metrics
    metrics_path = 'models/best_model_metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"✓ Metrics saved: {metrics_path}")
    
    # Display results
    print("\n" + "=" * 70)
    print("MODEL PERFORMANCE")
    print("=" * 70)
    for key, value in metrics.items():
        if key not in ['saved_at', 'model_type', 'samples_trained', 'features']:
            print(f"  {key:15} : {value:.4f}")
    
    print("\n" + "=" * 70)
    print("✓ DEMO MODEL READY FOR STREAMLIT!")
    print("=" * 70)
    print("\nYou can now run:")
    print("  streamlit run streamlit_app.py")
    print("\nThe app will use this demo model for testing.")
    print("\nIMPORTANT: For production, replace this with your trained model!")
    
    return model, metrics

def show_instructions():
    """Show instructions for real model training"""
    instructions = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    REAL MODEL TRAINING (In Jupyter)                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

After training your model in the notebook, save it with this code:

─────────────────────────────────────────────────────────────────────────────
# In Jupyter Notebook (after training XGBoost or other model)

import os
import pickle
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Create models folder
os.makedirs('models', exist_ok=True)

# Assuming you've trained: xgb_model, X_test, y_test
y_pred = xgb_model.predict(X_test)

# Calculate metrics
metrics = {
    'accuracy': accuracy_score(y_test, y_pred),
    'precision': precision_score(y_test, y_pred),
    'recall': recall_score(y_test, y_pred),
    'f1_score': f1_score(y_test, y_pred)
}

# Save model
with open('models/best_model.pickle', 'wb') as f:
    pickle.dump(xgb_model, f)

# Save metrics
with open('models/best_model_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print(f"✓ Model saved! Accuracy: {metrics['accuracy']:.4f}")

─────────────────────────────────────────────────────────────────────────────

Then the Streamlit app will automatically work!

    streamlit run streamlit_app.py
"""
    print(instructions)

if __name__ == "__main__":
    import sys
    
    # Check if user wants to create demo model
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        print("\n⚠️  CREATING DEMO MODEL FOR TESTING ONLY\n")
        create_demo_model()
        show_instructions()
    else:
        show_instructions()
        print("\n💡 To create a demo model for testing, run:")
        print("   python create_demo_model.py --demo")
        print("\n⚠️  Note: Demo model is for testing only. Use real trained model in production.")
