# 🔍 Social Trend Detector

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A powerful real-time social media trend detection system powered by Machine Learning and Natural Language Processing. Analyze social conversations, detect emerging trends, and gain actionable insights from social media data.

## ✨ Features

### Core Capabilities
- 🚀 **Real-time Trend Detection** - Identify emerging trends as they happen
- 🧠 **Machine Learning Analysis** - Advanced ML algorithms for pattern recognition
- 💬 **Sentiment Analysis** - Understand public sentiment around trends
- 📊 **Interactive Dashboard** - Visual analytics and trend visualization
- 🔄 **Data Processing Pipeline** - Efficient ingestion and processing of social data
- 💾 **Persistent Storage** - SQLite database for historical trend tracking
- 📤 **Export Functionality** - Export trends and insights in multiple formats
- 🐳 **Docker Support** - Containerized deployment for easy setup

### Advanced Features
- Topic modeling using Gensim
- Text preprocessing and normalization
- Keyword extraction and analysis
- Time-series trend tracking
- Multi-platform data ingestion support
- RESTful API endpoints
- Comprehensive test suite

## 🏗️ Architecture

```
┌─────────────────┐
│  Data Ingestion │
│   (ingestor.py) │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Data Processor │
│  (processor.py) │
└────────┬────────┘
         │
         ↓
┌─────────────────┐     ┌──────────────────┐
│   ML Analysis   │────→│ Sentiment Model  │
│  (ml_model.py)  │     │(sentiment_*.py)  │
└────────┬────────┘     └──────────────────┘
         │
         ↓
┌─────────────────┐
│   SQLite DB     │
│   (trends.db)   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Flask API      │
│   (app.py)      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   Dashboard     │
│(dashboard.html) │
└─────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 3.0.0** - Web framework
- **SQLite** - Database for trend storage

### Machine Learning & NLP
- **NLTK 3.8.1** - Natural Language Toolkit
- **Gensim 4.3.2** - Topic modeling and document similarity
- **Scikit-learn 1.3.2** - Machine learning algorithms

### Data Processing
- **Pandas 2.1.3** - Data manipulation and analysis
- **NumPy 1.26.2** - Numerical computing

### Development Tools
- **Docker** - Containerization
- **pytest** - Testing framework
- **python-dotenv** - Environment variable management

## 📋 Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher
- pip (Python package manager)
- Docker (optional, for containerized deployment)

## 🚀 Quick Start

### Option 1: Standard Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/chetx27/social-trend-detector.git
cd social-trend-detector
```

#### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"
```

#### 5. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1

# Database
DATABASE_PATH=trends.db

# API Configuration
API_PORT=5000
API_HOST=0.0.0.0
```

#### 6. Run the Application

```bash
# Basic app
python app.py

# Enhanced app with more features
python app_enhanced.py

# Or run the main entry point
python main.py
```

The application will be available at `http://localhost:5000`

### Option 2: Docker Deployment

#### Using Docker Compose

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

#### Using Docker Directly

```bash
# Build the image
docker build -t social-trend-detector .

# Run the container
docker run -p 5000:5000 -e FLASK_ENV=production social-trend-detector
```

## 📖 Usage

### API Endpoints

#### Get Trending Topics
```bash
GET /api/trends
```

#### Analyze Sentiment
```bash
POST /api/sentiment
Content-Type: application/json

{
  "text": "Your text to analyze"
}
```

#### Ingest Data
```bash
POST /api/ingest
Content-Type: application/json

{
  "data": "Social media content",
  "source": "twitter"
}
```

### Dashboard

Access the interactive dashboard at:
```
http://localhost:5000/dashboard
```

### Python API

```python
from ingestor import DataIngestor
from processor import DataProcessor
from ml_model import TrendDetector

# Ingest data
ingestor = DataIngestor()
ingestor.ingest_data(source='twitter', data=your_data)

# Process data
processor = DataProcessor()
processed_data = processor.process(your_data)

# Detect trends
detector = TrendDetector()
trends = detector.detect_trends(processed_data)
```

## 📁 Project Structure

```
social-trend-detector/
├── app.py                    # Main Flask application
├── app_enhanced.py           # Enhanced version with additional features
├── main.py                   # Entry point
├── config.py                 # Configuration management
├── ingestor.py              # Data ingestion module
├── processor.py             # Data processing pipeline
├── ml_model.py              # Machine learning models
├── sentiment_analyzer.py    # Sentiment analysis module
├── export_utils.py          # Data export utilities
├── test_suite.py            # Test cases
├── dashboard.html           # Web dashboard
├── trends.db                # SQLite database
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── .env                     # Environment variables
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest test_suite.py -v
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|--------|
| `FLASK_APP` | Flask application entry point | `app.py` |
| `FLASK_ENV` | Environment (development/production) | `development` |
| `FLASK_DEBUG` | Enable debug mode | `1` |
| `DATABASE_PATH` | Path to SQLite database | `trends.db` |
| `API_PORT` | API server port | `5000` |
| `API_HOST` | API server host | `0.0.0.0` |

### Customization

Edit `config.py` to customize:
- Model parameters
- Processing thresholds
- Data retention policies
- API rate limits

## 📊 Data Flow

1. **Ingestion**: Raw social media data is collected via `ingestor.py`
2. **Processing**: Text is cleaned, normalized, and prepared by `processor.py`
3. **Analysis**: ML models analyze patterns and detect trends via `ml_model.py`
4. **Sentiment**: Public sentiment is evaluated using `sentiment_analyzer.py`
5. **Storage**: Results are stored in SQLite database (`trends.db`)
6. **Visualization**: Trends are displayed on the interactive dashboard
7. **Export**: Data can be exported using `export_utils.py`

## 🔍 Key Modules

### Data Ingestor
Handles data collection from various sources with support for multiple platforms.

### Data Processor
Cleans and preprocesses text data including:
- Text normalization
- Stopword removal
- Tokenization
- Lemmatization

### ML Model
Detects trends using:
- TF-IDF vectorization
- Clustering algorithms
- Topic modeling
- Pattern recognition

### Sentiment Analyzer
Analyzes sentiment using:
- VADER sentiment analysis
- Custom sentiment models
- Emotion detection

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'nltk'`
```bash
pip install nltk
```

**Issue**: NLTK data not found
```bash
python -c "import nltk; nltk.download('all')"
```

**Issue**: Database locked
```bash
# Remove the lock file
rm trends.db-journal
```

**Issue**: Port 5000 already in use
```bash
# Change the port in .env file
API_PORT=5001
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure:
- Code follows PEP 8 style guidelines
- All tests pass
- New features include tests
- Documentation is updated

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**chetx27**
- GitHub: [@chetx27](https://github.com/chetx27)
- Repository: [social-trend-detector](https://github.com/chetx27/social-trend-detector)

## 🙏 Acknowledgments

- **NLTK** - Natural Language Processing toolkit
- **Gensim** - Topic modeling and document similarity
- **Flask** - Web framework
- **Scikit-learn** - Machine learning library
- All contributors and users of this project

## 🔗 Related Projects

- [Twitter API](https://developer.twitter.com/en/docs)
- [Reddit API](https://www.reddit.com/dev/api/)
- [NLTK Documentation](https://www.nltk.org/)
- [Gensim Documentation](https://radimrehurek.com/gensim/)

## 📈 Roadmap

- [ ] Add support for more social media platforms
- [ ] Implement real-time streaming analysis
- [ ] Add user authentication and authorization
- [ ] Enhance dashboard with more visualizations
- [ ] Add predictive analytics for trend forecasting
- [ ] Implement API rate limiting and caching
- [ ] Add multi-language support
- [ ] Create mobile-responsive dashboard
- [ ] Implement WebSocket for real-time updates
- [ ] Add export to more formats (PDF, Excel)

## 📞 Support

If you encounter any issues or have questions:
- Open an [issue](https://github.com/chetx27/social-trend-detector/issues)
- Check existing [documentation](https://github.com/chetx27/social-trend-detector/wiki)
- Review [closed issues](https://github.com/chetx27/social-trend-detector/issues?q=is%3Aissue+is%3Aclosed)

---

⭐ **Star this repository if you find it helpful!**

Made with ❤️ by [chetx27](https://github.com/chetx27)
