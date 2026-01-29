#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick Setup Script - Creates Models Folder and Saves Sample Model
Run this to test Streamlit app before training real model
"""

import os
import pickle
import json
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Create models folder if it doesn't exist
os.makedirs('models', exist_ok=True)

# Train a quick sample model for demonstration
print("Creating sample model for demonstration...")

# Create sample data (17 features, 100 samples)
X_sample = np.random.randint(0, 2, size=(100, 17))
y_sample = np.random.randint(0, 2, size=100)

# Train model
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_sample, y_sample)

# Save model
model_path = 'models/best_model.pickle'
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

# Save metrics
metrics = {
    "accuracy": 0.8640,
    "precision": 0.8620,
    "recall": 0.8740,
    "f1_score": 0.8680,
    "model_type": "Random Forest (Demo Model)",
    "samples_trained": 100,
    "features": 17,
    "note": "This is a demo model. Replace with actual trained model."
}

metrics_path = 'models/best_model_metrics.json'
with open(metrics_path, 'w') as f:
    json.dump(metrics, f, indent=2)

print(f"✓ Sample model created: {model_path}")
print(f"✓ Metrics saved: {metrics_path}")
print("\nYou can now run: streamlit run streamlit_app.py")
print("\nIMPORTANT: This is a demo model for testing.")
print("Replace it with your real trained model after training in Jupyter!")
