# 🚀 Social Media Trend Detection System

**Real-time trend detection using Machine Learning & Natural Language Processing**

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
|-----------|-----------|
| Language | Python 3.13.7 |
| Database | SQLite (local) |
| NLP | NLTK, Gensim, scikit-learn |
| Web Framework | Flask |
| ML Algorithms | LDA, Isolation Forest |

## 📁 Project Structure

social-trend-detector/
├── .env # Environment variables
├── config.py # Configuration settings
├── ingestor.py # Data ingestion (mock data generation)
├── processor.py # Text processing & cleaning
├── ml_model.py # LDA + anomaly detection
├── main.py # Full pipeline orchestration
├── app.py # Flask API dashboard
├── trends.db # SQLite database (auto-created)
└── README.md # This file

text

## 🔧 Installation (3 MINS)

### Prerequisites
- Python 3.13.7 or higher
- pip (Python package manager)
- VS Code or any terminal

### Step 1: Clone Repository
git clone https://github.com/YOUR_USERNAME/social-trend-detector.git
cd social-trend-detector

text

### Step 2: Create Virtual Environment
python -m venv venv
venv\Scripts\activate

text
*(Mac/Linux: `source venv/bin/activate`)*

### Step 3: Install Dependencies
pip install tweepy praw pymongo nltk scikit-learn gensim pandas numpy flask schedule python-dotenv matplotlib seaborn plotly requests beautifulsoup4

text

*(Takes 2-3 minutes)*

### Step 4: Verify Installation
python --version
pip list | grep flask

text

## 🚀 Quick Start (2 MINS)

### Run Full Pipeline + Dashboard

Open **4 separate terminals** and run commands in order:

**Terminal 1 - Ingestion (Creates mock data)**
python ingestor.py

text
**Expected Output:**
🚀 Creating MOCK social media data...
✅ Created 50 MOCK posts (Twitter + Reddit)
📊 Stats: 50 raw | 0 processed | 0 trends
✅ Ingestion COMPLETE (no APIs needed!)

text

**Terminal 2 - Processing (Cleans text)**
python processor.py

text
**Expected Output:**
✅ Processed 50 posts

text

**Terminal 3 - ML Analysis (Finds trends)**
python ml_model.py

text
**Expected Output:**
✅ LDA model trained
Topic 0: 0.012*"model" + 0.010*"data"...
Topic 1: 0.015*"python" + 0.012*"code"...
Topic 2: 0.011*"trend" + 0.009*"viral"...
🚨 Found 5 viral trends!

text

**Terminal 4 - Start Dashboard**
python app.py

text
**Expected Output:**
Running on http://127.0.0.1:5000
Press CTRL+C to quit

text

### Access Dashboard

Open **Chrome** and visit these 3 URLs:

#### 1️⃣ Health Check
http://localhost:5000/health

text
**Shows:**
{
"status": "running ✅",
"posts_raw": 50,
"posts_processed": 50,
"viral_trends": 5,
"database": "SQLite (local)"
}

text

#### 2️⃣ Viral Trends (Anomalies)
http://localhost:5000/trends

text
**Shows:** Top viral posts detected by Isolation Forest algorithm

#### 3️⃣ All Posts
http://localhost:5000/posts

text
**Shows:** All 50 processed posts with engagement scores

## 📊 Data Pipeline Architecture

┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: INGESTION (ingestor.py) │
│ │
│ - Generate 50 mock social posts │
│ - Twitter-like: text + likes + retweets │
│ - Reddit-like: title + score + comments │
│ - Random timestamps (last 24 hours) │
│ - Store in 'posts_raw' SQLite table │
└────────────────────┬────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 2: PROCESSING (processor.py) │
│ │
│ Text Cleaning: │
│ - Remove URLs (http://...) │
│ - Remove mentions (@username) │
│ - Remove hashtags (#trend) │
│ - Remove special characters │
│ │
│ NLP Processing: │
│ - Lemmatization (ran → run, running → run) │
│ - Remove stopwords (the, a, is, etc) │
│ - Keep only words >2 chars │
│ │
│ Feature Engineering: │
│ - Calculate engagement: likes + 2×retweets (Twitter) │
│ score + comments (Reddit) │
│ - Count words │
│ │
│ - Store in 'posts_processed' table │
└────────────────────┬────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 3: MACHINE LEARNING (ml_model.py) │
│ │
│ LDA Topic Modeling: │
│ - Discover 3 hidden topics from text │
│ - Topic 0: AI/ML words │
│ - Topic 1: Python/coding words │
│ - Topic 2: Data science words │
│ │
│ Anomaly Detection (Isolation Forest): │
│ - Analyze engagement scores │
│ - Flag unusual posts (high engagement = viral) │
│ - Contamination threshold: 10% │
│ │
│ - Store predictions in 'trends' table │
└────────────────────┬────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 4: API DASHBOARD (app.py) │
│ │
│ Flask REST Endpoints: │
│ - GET /health → Database statistics │
│ - GET /trends → Top 10 viral posts │
│ - GET /posts → Top 20 processed posts │
│ │
│ Response Format: JSON (browser-friendly) │
└─────────────────────────────────────────────────────────────┘

text

## 📈 Sample Output

### Database Statistics (After Running)
Raw Posts: 50 (fresh from ingestion)
Processed: 50 (cleaned + engineered)
Viral Trends: 5 (anomalies detected)
Topics Found: 3 (AI, Python, DataScience)

text

### Top Viral Post Example
{
"id": 7,
"platform": "twitter",
"text": "Breaking: AI revolution! Amazing new model discovered",
"engagement_score": 2850.0,
"anomaly_score": 2.45
}

text

### LDA Topics Discovered
Topic 0: 0.012*"model" + 0.010*"data" + 0.009*"learning"
Topic 1: 0.015*"python" + 0.012*"code" + 0.011*"programming"
Topic 2: 0.014*"trend" + 0.011*"viral" + 0.010*"engagement"

text

## 🎓 Learning Outcomes & Concepts

### Data Value Chain (Complete Coverage)

1. **Data Generation & Acquisition** 📊
   - Mock social media data generator
   - Realistic Twitter/Reddit post structure
   - Handles variety of data sources

2. **Data Organization & Storage** 🗄️
   - SQLite schema design (3 tables)
   - Proper data types & relationships
   - Indexing for fast queries

3. **Data Processing** 🔧
   - Text normalization pipeline
   - Feature extraction (engagement scores)
   - Data quality & cleansing

4. **Machine Learning** 🤖
   - Unsupervised learning (LDA clustering)
   - Anomaly detection (Isolation Forest)
   - Model evaluation & interpretation

5. **Insights & Decision Making** 💡
   - REST API for querying results
   - JSON response formatting
   - Real-time trend detection

### Technologies Mastered

- **Python 3.13.7**: Modern Python features, async patterns
- **NLTK/Gensim**: Industry-standard NLP libraries
- **scikit-learn**: ML algorithms & preprocessing
- **SQLite**: Lightweight database design
- **Flask**: Web framework fundamentals
- **Git/GitHub**: Version control best practices

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module 'nltk'` | Run `pip install nltk` |
| `trends.db not found` | Run `python ingestor.py` first |
| `Port 5000 already in use` | Change `port=5000` to `port=5001` in `app.py` line 47 |
| `NLTK data missing` | Run `python -m nltk.downloader all` |
| `Permission denied (git)` | Check GitHub credentials: `git config --global user.name "Your Name"` |
| `git push fails` | Generate GitHub token: Settings → Developer → Personal access tokens |
| `Flask not starting` | Check if `python app.py` is running in Terminal 4 |
| `Empty database` | Delete `trends.db`, run all 4 scripts again |

## 📦 Dependencies & Versions

tweepy==4.14.0 # Twitter API wrapper
praw==7.7.0 # Reddit API wrapper
pymongo==4.5.0 # MongoDB driver (optional)
nltk==3.8.1 # Natural Language Toolkit
scikit-learn==1.3.2 # Machine Learning
gensim==4.3.1 # Topic Modeling (LDA)
pandas==2.0.3 # Data manipulation
numpy==1.24.3 # Numerical computing
flask==3.0.0 # Web framework
schedule==1.2.0 # Job scheduling
python-dotenv==1.0.0 # Environment variables
matplotlib==3.7.1 # Plotting (optional)
seaborn==0.12.2 # Statistical plotting (optional)
plotly==5.14.0 # Interactive plots (optional)
requests==2.31.0 # HTTP requests
beautifulsoup4==4.12.2 # Web scraping (optional)


## 🚀 Future Enhancements

### Phase 1: Real Data Integration
- [ ] Replace mock data with real Twitter API (bearer token)
- [ ] Add Reddit streaming with PRAW
- [ ] Implement data deduplication

### Phase 2: Advanced ML
- [ ] BERT embeddings for semantic understanding
- [ ] Sentiment analysis (TextBlob/VADER)
- [ ] Named Entity Recognition (NER)
- [ ] Clustering visualization (t-SNE/UMAP)

### Phase 3: Scalability
- [ ] MongoDB cloud integration
- [ ] Horizontal scaling (Kafka streaming)
- [ ] Docker containerization
- [ ] Kubernetes deployment

### Phase 4: Web Dashboard
- [ ] React frontend with real-time updates
- [ ] Interactive trend visualization
- [ ] Time-series graphs
- [ ] User authentication

### Phase 5: DevOps & CI/CD
- [ ] GitHub Actions pipeline
- [ ] Automated testing (pytest)
- [ ] Docker image building
- [ ] Deployment to Heroku/AWS

## 💡 Use Cases & Applications

✅ **Portfolio Project** - Demonstrate ML + data engineering skills to employers  
✅ **Interview Preparation** - Explain data pipeline architecture in technical interviews  
✅ **Learning Tool** - Understand NLP, anomaly detection, and Flask fundamentals  
✅ **Research Paper** - Adapt for academic analysis of social media trends  
✅ **Startup MVP** - Base layer for social listening platform  
✅ **Hackathon** - Extend with real-time streaming & visualization  

## 📜 License

MIT License - Free to use, modify, and distribute

## 🤝 Contributing

Found a bug? Have ideas? Want to collaborate?

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/awesome-feature`)
3. **Commit** your changes (`git commit -m "Add awesome feature"`)
4. **Push** to the branch (`git push origin feature/awesome-feature`)
5. **Open** a Pull Request

## 📚 Resources & Learning

### NLP & Text Processing
- [NLTK Book](https://www.nltk.org/book/) - Official NLTK tutorial
- [Gensim LDA](https://radimrehurek.com/gensim/models/ldamodel.html) - Topic modeling guide

### Machine Learning
- [scikit-learn Docs](https://scikit-learn.org/) - Isolation Forest usage
- [Anomaly Detection](https://en.wikipedia.org/wiki/Anomaly_detection) - Theory

### Flask & APIs
- [Flask Official](https://flask.palletsprojects.com/) - Web framework docs
- [REST API Best Practices](https://restfulapi.net/) - Design patterns

### Data Science
- [Data Value Chain](https://www.gartner.com/smarterwithgartner/what-is-the-data-value-chain/) - Gartner article
- [Data Pipeline Design](https://github.com/gunnarmorling/awesome-opensource-data-engineering) - Awesome list

## 🏆 Recognition

If this project helped you learn, please:
- ⭐ **Star** this repository
- 🔗 **Share** with others learning ML/data science
- 💬 **Give feedback** via Issues/Discussions
- 🤝 **Contribute** improvements
