
# 🏙️ Real Estate Price Analysis & Recommendation System

A machine learning–powered real estate analytics platform that predicts property prices and recommends similar properties based on facilities, price similarity, and geographical proximity. The system is built using real-world scraped data and deployed as an interactive multi-page Streamlit web application.

---

## 📌 Project Overview

The real estate industry is highly data-driven, yet buyers and investors often rely on incomplete or unstructured information. This project aims to solve that problem by providing a unified platform for **price prediction, analytics, and intelligent recommendations**.

The dataset is currently limited to **Gurgaon (India)**, with future plans to expand to multiple cities and deploy the solution on cloud platforms such as AWS.

---

## 🚀 Features

### 🔮 Price Prediction
- Machine learning–based property price prediction
- Uses a fine-tuned **XGBoost regression model**
- Displays minimum, estimated, and maximum price range

### 📊 Analytics Dashboard
- Top 10 insights useful for buyers and investors
- Visual analysis of trends, pricing patterns, and correlations

### 🏢 Recommendation System
Hybrid recommendation approach using:
- Top facilities similarity
- Price-based similarity
- Nearby location similarity (latitude & longitude)

### 🌐 Streamlit Web Application
Multi-page application including:
- Home
- Price Prediction
- Analytics
- Recommendation System

---

## 🧠 Machine Learning Workflow

### 📥 Data Collection
- Web scraping from real estate platforms
- Property types:
  - Independent houses
  - Flats
  - Apartments
- Features include price, amenities, and geolocation

### 🧹 Data Preprocessing
- Data cleaning
- Missing value treatment
- Outlier handling
- Exploratory Data Analysis (EDA)
- Automated profiling using **YData Profiling**

### 🛠️ Feature Engineering & Selection
Techniques applied:
- Correlation analysis
- Random Forest importance
- Gradient Boosting
- Permutation importance
- LASSO
- RFE
- Linear Regression
- SHAP values

### 🤖 Model Training & Evaluation
Models tested:
- Linear Regression
- Ridge & LASSO
- SVR
- Decision Tree
- Random Forest
- Extra Trees
- Gradient Boosting
- AdaBoost
- MLP
- **XGBoost (Best Performer)**

Final model:
- XGBoost (tuned and serialized for deployment)
- Current MSE ≈ 45 Lakhs

---

## 🏗️ Tech Stack

- **Programming Language:** Python
- **Libraries:** Pandas, NumPy, Scikit-learn, XGBoost, SHAP
- **Visualization:** Matplotlib, Seaborn
- **Web Framework:** Streamlit
- **Model Serialization:** Joblib / Pickle

---

## 📁 Project Structure

```
├── dataset/
│   ├── df.pkl
│   ├── url.pkl
│   ├── distance_location.pkl
│
├── models/
│   ├── price_prediction.pkl
│   ├── recommender_models.pkl
│
├── app/
│   ├── Home.py
│   ├── Pages├────   Price_Prediction.py
│   ├        ├──Analytics.py
│   ├        ├── Recommendation.py
│
├── notebooks/
│   ├── EDA.ipynb
│   ├── Feature_Engineering.ipynb
│   ├── Model_Training.ipynb
│
├── README.md
```

---

## 🎯 Future Scope

- Expand dataset to multiple cities
- Reduce MSE to ~20 Lakhs using advanced feature engineering
- Improve recommendation quality using user feedback
- Deploy application on AWS or other cloud platforms

---

## 👥 Team & Contributions

This project was collaboratively developed as a team effort.

- **Arjun Pandit**  
  *Machine Learning & Model Development*  
  XGBoost model training, tuning, evaluation, and deployment-ready serialization.

- **Ayush Raj**  
  *Data Analysis & Feature Engineering*  
  Exploratory Data Analysis (EDA), feature engineering, data preprocessing, and analytical insights.

- **Samjeet**  
  *Data Collection & Web Scraping*  
  Web scraping, raw data extraction, and dataset preparation from real estate platforms.

---

## 📚 References

- Géron, A., *Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow*, O’Reilly, 2019.
- Bishop, C. M., *Pattern Recognition and Machine Learning*, Springer, 2006.
- Nitish Kumar, **CampusX YouTube Channel** – Machine Learning & Data Science Tutorials.

---

⭐ If you find this project useful, consider giving it a star on GitHub!
## Team Collaboration
Project collaboratively developed using GitHub.
