import sqlite3
from datetime import datetime, timedelta
import random

class SocialIngestor:
    def __init__(self):
        self.conn = sqlite3.connect('trends.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Create SQLite tables"""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS posts_raw (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            text TEXT,
            created_at TEXT,
            timestamp TEXT,
            likes INTEGER,
            retweets INTEGER,
            score INTEGER,
            num_comments INTEGER,
            processed INTEGER DEFAULT 0
        )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS posts_processed (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            text TEXT,
            cleaned_text TEXT,
            created_at TEXT,
            timestamp TEXT,
            likes INTEGER,
            retweets INTEGER,
            score INTEGER,
            num_comments INTEGER,
            engagement_score REAL,
            word_count INTEGER,
            processed INTEGER DEFAULT 1
        )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            text TEXT,
            cleaned_text TEXT,
            engagement_score REAL,
            is_viral INTEGER,
            anomaly_score REAL
        )''')
        
        self.conn.commit()
    
    def create_mock_data(self):
        """Generate 50 fake social media posts"""
        keywords = ['AI', 'ML', 'data science', 'python', 'tech']
        platforms = ['twitter', 'reddit']
        
        count = self.cursor.execute('SELECT COUNT(*) FROM posts_raw').fetchone()[0]
        if count > 0:
            print(f"✅ {count} posts already exist in database")
            return
        
        posts = []
        for i in range(50):
            keyword = random.choice(keywords)
            platform = random.choice(platforms)
            likes = random.randint(10, 1000)
            retweets = random.randint(0, 500)
            score = random.randint(50, 5000)
            comments = random.randint(5, 200)
            
            post = (
                platform,
                f"Breaking: {keyword} revolution! {'Amazing new model discovered' if random.random() > 0.5 else 'New breakthrough in ' + keyword}",
                (datetime.now() - timedelta(hours=random.randint(0, 24))).isoformat(),
                datetime.now().isoformat(),
                likes,
                retweets,
                score,
                comments,
                0
            )
            posts.append(post)
        
        self.cursor.executemany(
            '''INSERT INTO posts_raw 
            (platform, text, created_at, timestamp, likes, retweets, score, num_comments, processed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            posts
        )
        self.conn.commit()
        print(f"✅ Created {len(posts)} MOCK posts (Twitter + Reddit)")
    
    def get_stats(self):
        """Get database stats"""
        raw_count = self.cursor.execute('SELECT COUNT(*) FROM posts_raw').fetchone()[0]
        processed_count = self.cursor.execute('SELECT COUNT(*) FROM posts_processed').fetchone()[0]
        trends_count = self.cursor.execute('SELECT COUNT(*) FROM trends').fetchone()[0]
        
        print(f"📊 Stats: {raw_count} raw | {processed_count} processed | {trends_count} trends")
        return {'raw': raw_count, 'processed': processed_count, 'trends': trends_count}
    
    def run(self):
        print("🚀 Creating MOCK social media data...")
        self.create_mock_data()
        self.get_stats()
        print("✅ Ingestion COMPLETE (no APIs needed!)")
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    ingestor = SocialIngestor()
    ingestor.run()
    ingestor.close()
