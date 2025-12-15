import sqlite3
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

class TextProcessor:
    def __init__(self):
        self.conn = sqlite3.connect('trends.db')
        self.cursor = self.conn.cursor()
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
    
    def clean_text(self, text):
        """Clean text: remove URLs, mentions, special chars, lemmatize"""
        if not text:
            return ""
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        text = re.sub(r'@\w+|#\w+', '', text)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        words = [self.lemmatizer.lemmatize(w.lower()) 
                for w in text.split() 
                if w.lower() not in self.stop_words and len(w) > 2]
        return ' '.join(words)
    
    def analyze_sentiment(self, text):
        """Analyze sentiment using TextBlob"""
        if not text:
            return "neutral", 0.0
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            label = "positive"
        elif polarity < -0.1:
            label = "negative"
        else:
            label = "neutral"
        return label, polarity
    
    def compute_engagement(self, platform, likes, retweets, score, comments):
        """Calculate engagement score"""
        if platform == 'twitter':
            return likes + 2 * retweets
        else:
            return score + comments
    
    def process_batch(self):
        """Process raw posts -> cleaned posts"""
        raw_posts = self.cursor.execute(
            'SELECT id, platform, text, created_at, timestamp, likes, retweets, score, num_comments FROM posts_raw WHERE processed = 0'
        ).fetchall()
        
        if not raw_posts:
            print("ℹ️ No new posts to process")
            return
        
        processed = []
        for post in raw_posts:
            post_id, platform, text, created_at, timestamp, likes, retweets, score, num_comments = post
            
            cleaned_text = self.clean_text(text)
            engagement = self.compute_engagement(platform, likes, retweets, score, num_comments)
            word_count = len(cleaned_text.split()) if cleaned_text else 0
            sentiment_label, sentiment_score = self.analyze_sentiment(text)
            
            processed.append((
                platform, text, cleaned_text, created_at, timestamp, 
                likes, retweets, score, num_comments, engagement, word_count, sentiment_label, sentiment_score
            ))
        
        self.cursor.executemany(
            '''INSERT INTO posts_processed 
            (platform, text, cleaned_text, created_at, timestamp, likes, retweets, score, num_comments, engagement_score, word_count, sentiment_label, sentiment_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            processed
        )
        
        self.cursor.execute('UPDATE posts_raw SET processed = 1')
        self.conn.commit()
        
        print(f"✅ Processed {len(processed)} posts")
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    processor = TextProcessor()
    processor.process_batch()
    processor.close()
