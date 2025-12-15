import sqlite3
import nltk
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim import corpora
from gensim.models import LdaModel
from sklearn.ensemble import IsolationForest

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

class TrendDetector:
    def __init__(self):
        self.conn = sqlite3.connect('trends.db')
        self.cursor = self.conn.cursor()
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.lda_model = None
    
    def train_lda(self, num_topics=3):
        """Train LDA model on cleaned text"""
        posts = self.cursor.execute(
            'SELECT cleaned_text FROM posts_processed WHERE cleaned_text IS NOT NULL AND cleaned_text != ""'
        ).fetchall()
        
        if len(posts) < 10:
            print("⚠️ Not enough data for LDA (need 10+)")
            return None
        
        texts = [post[0].split() for post in posts]
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        
        self.lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=5)
        print("✅ LDA model trained")
        
        for topic_id, topic in self.lda_model.print_topics(num_words=5):
            print(f"   Topic {topic_id}: {topic}")
        
        return self.lda_model
    
    def detect_anomalies(self):
        """Find viral posts using engagement anomalies"""
        posts = self.cursor.execute(
            'SELECT id, platform, text, cleaned_text, engagement_score, sentiment_label, sentiment_score FROM posts_processed WHERE engagement_score IS NOT NULL'
        ).fetchall()
        
        if len(posts) < 5:
            print("⚠️ Not enough data for anomaly detection")
            return []
        
        scores = np.array([post[4] for post in posts]).reshape(-1, 1)
        
        detector = IsolationForest(contamination=0.1, random_state=42)
        anomalies = detector.fit_predict(scores)
        
        viral_posts = []
        for i, post in enumerate(posts):
            if anomalies[i] == -1:
                post_id, platform, text, cleaned_text, engagement, sentiment_label, sentiment_score = post
                viral_posts.append((
                    platform, text, cleaned_text, engagement, 1, float(scores[i][0]), sentiment_label, sentiment_score
                ))
        
        if viral_posts:
            self.cursor.execute('DELETE FROM trends')
            self.cursor.executemany(
                '''INSERT INTO trends 
                (platform, text, cleaned_text, engagement_score, is_viral, anomaly_score, sentiment_label, sentiment_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                viral_posts
            )
            self.conn.commit()
            print(f"🚨 Found {len(viral_posts)} viral trends!")
        
        return viral_posts
    
    def get_trends(self, limit=10):
        """Get top viral trends"""
        trends = self.cursor.execute(
            'SELECT * FROM trends ORDER BY anomaly_score DESC LIMIT ?',
            (limit,)
        ).fetchall()
        return trends
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    detector = TrendDetector()
    detector.train_lda()
    detector.detect_anomalies()
    detector.close()
