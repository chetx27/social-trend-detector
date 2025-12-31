"""Comprehensive Unit Tests for Social Trend Detector

Run with: pytest test_suite.py -v
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from sentiment_analyzer import SentimentAnalyzer
from export_utils import DataExporter


class TestSentimentAnalyzer:
    """Test cases for sentiment analysis functionality."""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance for testing."""
        return SentimentAnalyzer()
    
    def test_positive_sentiment(self, analyzer):
        """Test detection of positive sentiment."""
        text = "I love this amazing product! It's fantastic!"
        scores = analyzer.analyze_sentiment(text)
        sentiment = analyzer.classify_sentiment(scores['compound'])
        
        assert sentiment == 'positive'
        assert scores['compound'] > 0
    
    def test_negative_sentiment(self, analyzer):
        """Test detection of negative sentiment."""
        text = "This is terrible and awful. I hate it."
        scores = analyzer.analyze_sentiment(text)
        sentiment = analyzer.classify_sentiment(scores['compound'])
        
        assert sentiment == 'negative'
        assert scores['compound'] < 0
    
    def test_neutral_sentiment(self, analyzer):
        """Test detection of neutral sentiment."""
        text = "The product exists. It is available."
        scores = analyzer.analyze_sentiment(text)
        sentiment = analyzer.classify_sentiment(scores['compound'])
        
        assert sentiment == 'neutral'
    
    def test_empty_text(self, analyzer):
        """Test handling of empty text."""
        scores = analyzer.analyze_sentiment("")
        assert scores['compound'] == 0.0
    
    def test_batch_analysis(self, analyzer):
        """Test batch sentiment analysis."""
        texts = [
            "Great product!",
            "Terrible experience.",
            "It's okay."
        ]
        results = analyzer.analyze_batch(texts)
        
        assert len(results) == 3
        assert all('sentiment' in r for r in results)
    
    def test_emotion_stats(self, analyzer):
        """Test emotion statistics calculation."""
        texts = [
            "I love this!",
            "This is bad.",
            "Neutral statement."
        ]
        stats = analyzer.get_emotion_stats(texts)
        
        assert 'positive' in stats
        assert 'negative' in stats
        assert 'neutral' in stats
        assert sum(stats.values()) == 3
    
    def test_average_sentiment(self, analyzer):
        """Test average sentiment calculation."""
        texts = ["Great!", "Awesome!", "Terrible!"]
        avg = analyzer.get_average_sentiment(texts)
        
        assert isinstance(avg, float)
        assert -1 <= avg <= 1


class TestDataExporter:
    """Test cases for data export functionality."""
    
    @pytest.fixture
    def sample_data(self):
        """Sample data for testing."""
        return [
            {'id': 1, 'content': 'Post 1', 'score': 100},
            {'id': 2, 'content': 'Post 2', 'score': 200}
        ]
    
    def test_to_json(self, sample_data):
        """Test JSON export."""
        json_str = DataExporter.to_json(sample_data)
        
        assert isinstance(json_str, str)
        assert '"id": 1' in json_str
    
    def test_generate_report(self, sample_data):
        """Test report generation."""
        topics = {'topics': [{'id': 0, 'keywords': ['test']}]}
        anomalies = [{'id': 1, 'is_anomaly': True}]
        
        report = DataExporter.generate_report(
            sample_data, topics, anomalies
        )
        
        assert 'generated_at' in report
        assert 'summary' in report
        assert report['summary']['total_posts'] == 2
    
    def test_empty_data(self):
        """Test handling of empty data."""
        json_str = DataExporter.to_json([])
        assert json_str == '[]'


class TestIntegration:
    """Integration tests for combined functionality."""
    
    def test_sentiment_and_export(self):
        """Test sentiment analysis with export."""
        analyzer = SentimentAnalyzer()
        texts = ["Great!", "Bad!", "Okay."]
        
        results = analyzer.analyze_batch(texts)
        json_data = DataExporter.to_json(results)
        
        assert len(results) == 3
        assert json_data is not None
    
    def test_stats_and_report(self):
        """Test statistics with report generation."""
        analyzer = SentimentAnalyzer()
        texts = ["Excellent!", "Poor!", "Average."]
        
        stats = analyzer.get_emotion_stats(texts)
        report = DataExporter.generate_report([], {'topics': []}, [])
        
        assert isinstance(stats, dict)
        assert isinstance(report, dict)


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
