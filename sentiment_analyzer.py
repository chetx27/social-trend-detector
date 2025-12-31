"""Sentiment Analysis Module for Social Trend Detector

Provides emotion detection and sentiment scoring for social media posts
using NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner).
"""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Analyzes sentiment and emotion in social media posts."""
    
    def __init__(self):
        """Initialize the sentiment analyzer with VADER."""
        try:
            self.sia = SentimentIntensityAnalyzer()
            logger.info("Sentiment analyzer initialized successfully")
        except LookupError:
            logger.warning("VADER lexicon not found. Downloading...")
            nltk.download('vader_lexicon', quiet=True)
            self.sia = SentimentIntensityAnalyzer()
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of a single text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with sentiment scores:
            - neg: Negative sentiment (0-1)
            - neu: Neutral sentiment (0-1)
            - pos: Positive sentiment (0-1)
            - compound: Overall sentiment (-1 to 1)
        """
        if not text or not isinstance(text, str):
            return {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
        
        scores = self.sia.polarity_scores(text)
        return scores
    
    def classify_sentiment(self, compound_score: float) -> str:
        """Classify sentiment based on compound score.
        
        Args:
            compound_score: VADER compound score (-1 to 1)
            
        Returns:
            Sentiment label: 'positive', 'negative', or 'neutral'
        """
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """Analyze sentiment for multiple texts.
        
        Args:
            texts: List of text strings to analyze
            
        Returns:
            List of dictionaries with sentiment scores and classifications
        """
        results = []
        for text in texts:
            scores = self.analyze_sentiment(text)
            sentiment = self.classify_sentiment(scores['compound'])
            results.append({
                'text': text,
                'scores': scores,
                'sentiment': sentiment
            })
        return results
    
    def get_emotion_stats(self, texts: List[str]) -> Dict[str, int]:
        """Get emotion distribution statistics.
        
        Args:
            texts: List of text strings
            
        Returns:
            Dictionary with counts of each sentiment category
        """
        stats = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for text in texts:
            scores = self.analyze_sentiment(text)
            sentiment = self.classify_sentiment(scores['compound'])
            stats[sentiment] += 1
        
        return stats
    
    def get_average_sentiment(self, texts: List[str]) -> float:
        """Calculate average sentiment score across texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            Average compound sentiment score
        """
        if not texts:
            return 0.0
        
        scores = [self.analyze_sentiment(text)['compound'] for text in texts]
        return sum(scores) / len(scores)


if __name__ == '__main__':
    # Example usage
    analyzer = SentimentAnalyzer()
    
    sample_posts = [
        "I absolutely love this new technology! It's amazing!",
        "This is terrible and disappointing.",
        "The weather is okay today."
    ]
    
    print("\n=== Sentiment Analysis Demo ===")
    for post in sample_posts:
        scores = analyzer.analyze_sentiment(post)
        sentiment = analyzer.classify_sentiment(scores['compound'])
        print(f"\nText: {post}")
        print(f"Sentiment: {sentiment.upper()}")
        print(f"Scores: {scores}")
    
    # Get statistics
    stats = analyzer.get_emotion_stats(sample_posts)
    print(f"\n=== Emotion Distribution ===")
    print(stats)
