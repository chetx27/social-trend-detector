# 🚀 Social Media Trend Detection System

**Real-time trend detection using Machine Learning & Natural Language Processing**

[![Python](https://img.shields.io/badge/Python-3.13.7-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Latest-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![NLP](https://img.shields.io/badge/NLP-NLTK%20%7C%20Gensim-orange.svg)]()

## 📋 Overview

This project implements an **end-to-end data pipeline** that demonstrates core concepts in data management and machine learning:

- **Data Ingestion**: Collects social media posts (Twitter/Reddit)
- **Data Processing**: Cleans, normalizes, and extracts features
- **Machine Learning**: Applies LDA topic modeling + anomaly detection
- **API Dashboard**: Provides REST endpoints for trend analysis

Perfect for understanding the **data value chain**: generation → acquisition → organization → processing → learning & predictions.

## 🎯 Key Features

✅ **50+ Mock Social Posts** - Pre-generated data (Twitter + Reddit)  
✅ **NLP Text Processing** - Lemmatization, stopword removal, cleaning  
✅ **LDA Topic Modeling** - Discovers 3 hidden topics in data  
✅ **Anomaly Detection** - Identifies viral posts using Isolation Forest  
✅ **SQLite Database** - Local, zero-setup, file-based storage  
✅ **Flask REST API** - Dashboard with 3 endpoints  
✅ **100% Python** - No external APIs, runs offline  

## 📊 Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.13.7 |
| Database | SQLite (local) |
| NLP | NLTK, Gensim, scikit-learn |
| Web Framework | Flask |
| ML Algorithms | LDA, Isolation Forest |

## 📁 Project Structure

```
social-trend-detector/
├── src/
│   ├── pipeline.py          # Main data pipeline
│   ├── app.py               # Flask API server
│   ├── data_ingestion.py    # Mock data generation
│   ├── data_processing.py   # NLP preprocessing
│   ├── ml_models.py         # LDA & anomaly detection
│   └── database.py          # SQLite operations
├── data/
│   └── trends.db            # SQLite database (generated)
├── requirements.txt         # Python dependencies
├── README.md
└── LICENSE
```

## 🛠️ Installation

### Prerequisites
- Python 3.13.7+ installed
- pip package manager

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/chetx27/social-trend-detector.git
   cd social-trend-detector
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data**
   ```bash
   python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
   ```

## 🚀 Quick Start

### 1. Run the Data Pipeline

```bash
python src/pipeline.py
```

**What happens:**
- Generates 50+ mock social media posts
- Processes text with NLP (cleaning, lemmatization)
- Applies LDA topic modeling (discovers 3 topics)
- Runs anomaly detection on engagement metrics
- Stores results in SQLite database

### 2. Start the Flask API

```bash
python src/app.py
```

API runs on `http://localhost:5000`

### 3. Test API Endpoints

```bash
# Get all trends
curl http://localhost:5000/api/trends

# Get discovered topics
curl http://localhost:5000/api/topics

# Get viral/anomalous posts
curl http://localhost:5000/api/anomalies
```

## 📡 API Documentation

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/api/trends` | GET | Fetch all processed trends | JSON array of posts with metadata |
| `/api/topics` | GET | Get discovered LDA topics | JSON with topic keywords & weights |
| `/api/anomalies` | GET | Retrieve viral/anomalous posts | JSON array of flagged posts |

### Sample API Response - Trending Topics

```json
{
  "topics": [
    {
      "topic_id": 0,
      "keywords": ["AI", "machine", "learning", "neural", "data"],
      "weight": 0.35
    },
    {
      "topic_id": 1,
      "keywords": ["climate", "change", "environment", "sustainable", "green"],
      "weight": 0.28
    },
    {
      "topic_id": 2,
      "keywords": ["technology", "innovation", "startup", "digital", "future"],
      "weight": 0.37
    }
  ]
}
```

### Sample API Response - Anomalies

```json
{
  "anomalies": [
    {
      "post_id": 23,
      "content": "Breaking: New AI breakthrough announced!",
      "engagement_score": 8500,
      "anomaly_score": 0.92,
      "platform": "Twitter",
      "timestamp": "2024-12-16T14:30:00Z"
    }
  ]
}
```

## 🎓 Learning Outcomes

This project demonstrates:

### Data Engineering
- ETL pipeline design and implementation
- Data cleaning and preprocessing techniques
- Feature extraction from unstructured text

### Machine Learning
- **Unsupervised Learning**: LDA (Latent Dirichlet Allocation) for topic modeling
- **Anomaly Detection**: Isolation Forest for identifying viral content
- Model training and evaluation workflows

### Natural Language Processing
- Text preprocessing (tokenization, stopword removal)
- Lemmatization and normalization
- TF-IDF vectorization

### Backend Development
- REST API design with Flask
- JSON response formatting
- Error handling and validation

### Database Management
- SQLite schema design
- CRUD operations
- Query optimization

### Software Architecture
- Modular code structure
- Separation of concerns
- Configuration management

## 🔧 Technical Details

### Machine Learning Pipeline

1. **Text Preprocessing**
   - Lowercase conversion
   - Remove special characters, URLs, mentions
   - Tokenization
   - Stopword removal
   - Lemmatization

2. **Feature Extraction**
   - TF-IDF vectorization
   - N-gram generation (unigrams, bigrams)

3. **Topic Modeling (LDA)**
   - Number of topics: 3
   - Algorithm: Gibbs Sampling
   - Outputs: Topic-keyword distributions

4. **Anomaly Detection**
   - Algorithm: Isolation Forest
   - Features: Engagement metrics (likes, shares, comments)
   - Threshold: Top 5% flagged as anomalies

### Database Schema

```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    platform TEXT,
    engagement_score INTEGER,
    topic_id INTEGER,
    is_anomaly BOOLEAN,
    processed_text TEXT,
    timestamp DATETIME
);
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Contribution Ideas
- Improve NLP preprocessing pipeline
- Add more ML algorithms (clustering, classification)
- Optimize database queries
- Write documentation and tutorials
- Report bugs and suggest features

## 📝 Requirements

```txt
Flask==3.0.0
nltk==3.8.1
gensim==4.3.2
scikit-learn==1.3.2
pandas==2.1.3
numpy==1.26.2
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'nltk'`  
**Solution**: Run `pip install -r requirements.txt`

**Issue**: `Resource 'corpora/stopwords' not found`  
**Solution**: Download NLTK data: `python -c "import nltk; nltk.download('stopwords')"`

**Issue**: Database locked error  
**Solution**: Close any database connections and restart the pipeline

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Show Your Support

If this project helped you learn something new, give it a ⭐️!

---

**Built with ❤️ by [@chetx27](https://github.com/chetx27)**
