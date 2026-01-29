# Phishing Website Detection by Machine Learning Techniques|| Phishing Website Detection System

## Objective
A phishing website is a common social engineering method that mimics trustful uniform resource locators (URLs) and webpages. The objective of this project is to train machine learning models and deep neural nets on the dataset created to predict phishing websites. Both phishing and benign URLs of websites are gathered to form a dataset and from them required URL and website content-based features are extracted. The performance level of each model is measures and compared.

## Data Collection
The set of phishing URLs are collected from opensource service called **PhishTank**. This service provide a set of phishing URLs in multiple formats like csv, json etc. that gets updated hourly. To download the data: https://www.phishtank.com/developer_info.php. From this dataset, 5000 random phishing URLs are collected to train the ML models.

The legitimate URLs are obatined from the open datasets of the University of New Brunswick, https://www.unb.ca/cic/datasets/url-2016.html. This dataset has a collection of benign, spam, phishing, malware & defacement URLs. Out of all these types, the benign url dataset is considered for this project. From this dataset, 5000 random legitimate URLs are collected to train the ML models.

The above mentioned datasets are uploaded to the '[DataFiles](https://github.com/shreyagopal/Phishing-Website-Detection-by-Machine-Learning-Techniques/tree/master/DataFiles)' folder of this repository.

## Feature Extraction
The below mentioned category of features are extracted from the URL data:

1.   Address Bar based Features <br>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In this category 9 features are extracted.
2.   Domain based Features<br>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In this category 4 features are extracted.
3.   HTML & Javascript based Features<br>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In this category 4 features are extracted.

*The details pertaining to these features are mentioned in the [URL Feature Extraction.ipynb.](https://github.com/shreyagopal/Phishing-Website-Detection-by-Machine-Learning-Techniques/blob/master/URL%20Feature%20Extraction.ipynb)[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shreyagopal/Phishing-Website-Detection-by-Machine-Learning-Techniques/blob/master/URL%20Feature%20Extraction.ipynb)*

So, all together 17 features are extracted from the 10,000 URL dataset and are stored in '[5.urldata.csv](https://github.com/shreyagopal/Phishing-Website-Detection-by-Machine-Learning-Techniques/blob/master/DataFiles/5.urldata.csv)' file in the DataFiles folder.<br>
The features are referenced from the https://archive.ics.uci.edu/ml/datasets/Phishing+Websites.

## Models & Training

Before stating the ML model training, the data is split into 80-20 i.e., 8000 training samples & 2000 testing samples. From the dataset, it is clear that this is a supervised machine learning task. There are two major types of supervised machine learning problems, called classification and regression.

This data set comes under classification problem, as the input URL is classified as phishing (1) or legitimate (0). The supervised machine learning models (classification) considered to train the dataset in this project are:

* Decision Tree
* Random Forest
* Multilayer Perceptrons
* XGBoost
* Autoencoder Neural Network
* Support Vector Machines

# 🔐 Phishing Website Detection System – v2.0

A complete **Machine Learning–based Phishing Website Detection System** with an integrated **AI Chatbot** for explanation and cybersecurity awareness. This project detects malicious URLs and helps users understand *why* a website is classified as phishing or legitimate.

---

## 📌 Project Highlights

* ✅ Detects phishing websites using ML models
* 🤖 AI-powered chatbot for explanation & guidance
* 🌐 Interactive web interface built with Streamlit
* 📊 Feature analysis and visual insights
* 🧪 Suitable for academic & real-world use

---

## 🧠 How the System Works

1. **User Input** – URL entered by the user
2. **Feature Extraction**

   * URL-based features (length, symbols, keywords)
   * Domain-based features (HTTPS, subdomains)
   * Content-based features (HTML tags, external links)
3. **ML Classification**

   * Trained models predict *Phishing* or *Legitimate*
4. **Chatbot Interaction**

   * Explains prediction results
   * Answers phishing & security-related questions
5. **Web UI**

   * Displays prediction results and chatbot responses

---

## 🤖 AI Chatbot Module

The chatbot enhances user understanding and trust in the system.

### Features

* Explains why a URL is marked phishing or safe
* Answers common questions:

  * What is phishing?
  * Why is this URL unsafe?
  * How can I protect myself online?
* Helps beginners understand ML decisions

### Technology

* Hugging Face Transformers
* Pre-trained NLP models
* `huggingface-hub` for model management

---

## 📦 Core Dependencies

### ML Framework & Data Processing

```txt
numpy>=1.26.0
pandas>=2.0.3
scikit-learn>=1.6.0
xgboost>=2.0.0
```

### Web Interface & HTTP

```txt
streamlit>=1.0.0
requests==2.31.0
urllib3==2.0.4
beautifulsoup4>=4.9.0
```

### AI & Chatbot

```txt
transformers>=4.30.0
huggingface-hub>=0.16.0
```

### Utilities & Visualization

```txt
python-dateutil>=2.8.0
matplotlib==3.7.2
seaborn==0.12.2
```

### Development Dependencies (Optional)

```txt
jupyter==1.0.0
ipython==8.14.0
pytest>=6.2.0
black>=21.6b0
flake8>=3.9.0
```

---

## 🛠️ Installation Steps

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/phishing-website-detection-v2.git
cd phishing-website-detection-v2
```

2. **Create Virtual Environment**

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the Application**

```bash
streamlit run app.py
```

---

## 📊 Model Performance

* High accuracy on phishing datasets
* XGBoost handles complex URL patterns efficiently
* Feature importance improves explainability

---

## 🎯 Use Cases

* Final-year Machine Learning projects
* Cybersecurity awareness tools
* Educational demonstrations
* URL safety verification systems

---

## 🚀 Future Enhancements

* Browser extension support
* Deep learning–based URL embeddings
* Multi-language chatbot
* Real-time threat intelligence integration

```



