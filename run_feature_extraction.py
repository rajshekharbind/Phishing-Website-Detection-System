#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Feature Extraction Runner Script
This script runs feature extraction on URL datasets and saves results
"""

import os
import sys
import pandas as pd
from URLFeatureExtraction import (
    havingIP, haveAtSign, getLength, getDepth, redirection
)

def check_data_files():
    """Check if all required data files exist"""
    required_files = [
        'DataFiles/4.phishing.csv',
        'DataFiles/3.legitimate.csv'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"Error: Required file not found: {file_path}")
            return False
    return True

def main():
    """Main execution function"""
    print("=" * 60)
    print("Phishing Website Detection - Feature Extraction")
    print("=" * 60)
    
    # Check data files
    if not check_data_files():
        print("Please ensure all data files are in the DataFiles/ directory")
        sys.exit(1)
    
    print("\n✓ Data files found")
    print("Ready to extract features from URLs...")
    print("\nTo run feature extraction:")
    print("1. Open 'URL Feature Extraction.ipynb' in Jupyter")
    print("2. Run all cells to extract features")
    print("3. The output will be saved to 'DataFiles/5.urldata.csv'")
    
    print("\nThen proceed to train models:")
    print("1. Open 'Phishing Website Detection_Models & Training.ipynb'")
    print("2. Run all cells to train and evaluate models")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
