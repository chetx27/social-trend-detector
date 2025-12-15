from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('trends.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/health')
def health():
    """Database health check"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        raw = cursor.execute('SELECT COUNT(*) FROM posts_raw').fetchone()[0]
        processed = cursor.execute('SELECT COUNT(*) FROM posts_processed').fetchone()[0]
        trends = cursor.execute('SELECT COUNT(*) FROM trends').fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'status': 'running ✅',
            'posts_raw': raw,
            'posts_processed': processed,
            'viral_trends': trends,
            'database': 'SQLite (local)'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/trends')
def trends():
    """Get top viral trends"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        viral_trends = cursor.execute(
            'SELECT id, platform, text, engagement_score, anomaly_score, sentiment_label, sentiment_score FROM trends ORDER BY anomaly_score DESC LIMIT 10'
        ).fetchall()
        
        conn.close()
        
        return jsonify([dict(row) for row in viral_trends])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/posts')
def posts():
    """Get processed posts"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        posts_list = cursor.execute(
            'SELECT id, platform, text, engagement_score, sentiment_label, sentiment_score FROM posts_processed ORDER BY engagement_score DESC LIMIT 20'
        ).fetchall()
        
        conn.close()
        
        return jsonify([dict(row) for row in posts_list])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
