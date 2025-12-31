"""Enhanced Flask API for Social Trend Detector

Extended version with sentiment analysis, pagination, filtering, and monitoring.
"""

from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import sqlite3
import logging
from datetime import datetime
from sentiment_analyzer import SentimentAnalyzer
from export_utils import DataExporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize components
sentiment_analyzer = SentimentAnalyzer()
data_exporter = DataExporter()

DATABASE = 'trends.db'


def get_db_connection():
    """Create database connection."""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None


@app.route('/')
def index():
    """Serve the dashboard HTML page."""
    return send_from_directory('.', 'dashboard.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            status = 'healthy'
        else:
            status = 'degraded'
        
        return jsonify({
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0'
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500


@app.route('/api/trends', methods=['GET'])
def get_trends():
    """Get all trends with optional filtering and pagination.
    
    Query params:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 20)
        - platform: Filter by platform (twitter/reddit)
        - sentiment: Filter by sentiment (positive/negative/neutral)
    """
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        platform = request.args.get('platform', None)
        sentiment_filter = request.args.get('sentiment', None)
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        # Build query
        query = "SELECT * FROM posts"
        conditions = []
        params = []
        
        if platform:
            conditions.append("platform = ?")
            params.append(platform)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY engagement_score DESC"
        
        # Calculate offset
        offset = (page - 1) * per_page
        query += f" LIMIT {per_page} OFFSET {offset}"
        
        cursor = conn.execute(query, params)
        posts = [dict(row) for row in cursor.fetchall()]
        
        # Add sentiment analysis
        for post in posts:
            if post.get('content'):
                sentiment_scores = sentiment_analyzer.analyze_sentiment(post['content'])
                post['sentiment'] = sentiment_analyzer.classify_sentiment(
                    sentiment_scores['compound']
                )
                post['sentiment_scores'] = sentiment_scores
        
        # Apply sentiment filter if specified
        if sentiment_filter:
            posts = [p for p in posts if p.get('sentiment') == sentiment_filter]
        
        # Get total count
        count_query = "SELECT COUNT(*) as count FROM posts"
        if conditions:
            count_query += " WHERE " + " AND ".join(conditions)
        
        total_count = conn.execute(count_query, params).fetchone()['count']
        conn.close()
        
        return jsonify({
            'trends': posts,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_count,
                'pages': (total_count + per_page - 1) // per_page
            }
        })
    
    except Exception as e:
        logger.error(f"Error fetching trends: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Get discovered topics from LDA analysis."""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        # Get unique topics
        cursor = conn.execute(
            "SELECT DISTINCT topic_id, processed_text FROM posts WHERE topic_id IS NOT NULL"
        )
        topics_data = cursor.fetchall()
        conn.close()
        
        # Organize topics
        topics = {}
        for row in topics_data:
            topic_id = row['topic_id']
            if topic_id not in topics:
                topics[topic_id] = []
            if row['processed_text']:
                topics[topic_id].append(row['processed_text'])
        
        # Format response
        topic_list = []
        for topic_id, texts in topics.items():
            # Get top keywords (simplified)
            all_words = ' '.join(texts).split()
            word_freq = {}
            for word in all_words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            
            topic_list.append({
                'topic_id': topic_id,
                'keywords': [word for word, _ in top_keywords],
                'post_count': len(texts)
            })
        
        return jsonify({'topics': topic_list})
    
    except Exception as e:
        logger.error(f"Error fetching topics: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/anomalies', methods=['GET'])
def get_anomalies():
    """Get detected anomalies (viral posts)."""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.execute(
            "SELECT * FROM posts WHERE is_anomaly = 1 ORDER BY engagement_score DESC"
        )
        anomalies = [dict(row) for row in cursor.fetchall()]
        
        # Add sentiment analysis
        for anomaly in anomalies:
            if anomaly.get('content'):
                sentiment_scores = sentiment_analyzer.analyze_sentiment(anomaly['content'])
                anomaly['sentiment'] = sentiment_analyzer.classify_sentiment(
                    sentiment_scores['compound']
                )
        
        conn.close()
        
        return jsonify({
            'anomalies': anomalies,
            'count': len(anomalies)
        })
    
    except Exception as e:
        logger.error(f"Error fetching anomalies: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/sentiment/stats', methods=['GET'])
def get_sentiment_stats():
    """Get overall sentiment statistics."""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.execute("SELECT content FROM posts WHERE content IS NOT NULL")
        texts = [row['content'] for row in cursor.fetchall()]
        conn.close()
        
        if not texts:
            return jsonify({'error': 'No data available'}), 404
        
        # Get emotion statistics
        stats = sentiment_analyzer.get_emotion_stats(texts)
        avg_sentiment = sentiment_analyzer.get_average_sentiment(texts)
        
        return jsonify({
            'distribution': stats,
            'average_sentiment': avg_sentiment,
            'total_analyzed': len(texts)
        })
    
    except Exception as e:
        logger.error(f"Error calculating sentiment stats: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/export', methods=['GET'])
def export_data():
    """Export trend data in specified format.
    
    Query params:
        - format: 'json' or 'csv' (default: 'json')
    """
    try:
        format_type = request.args.get('format', 'json')
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.execute("SELECT * FROM posts")
        trends = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        if format_type == 'json':
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'export_{timestamp}.json'
            json_data = data_exporter.to_json(trends, filename)
            return jsonify({
                'message': 'Export successful',
                'filename': filename,
                'records': len(trends)
            })
        
        elif format_type == 'csv':
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'export_{timestamp}.csv'
            data_exporter.to_csv(trends, filename)
            return jsonify({
                'message': 'Export successful',
                'filename': filename,
                'records': len(trends)
            })
        
        else:
            return jsonify({'error': 'Unsupported format'}), 400
    
    except Exception as e:
        logger.error(f"Error exporting data: {e}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info("Starting Enhanced Social Trend Detector API...")
    logger.info("Dashboard available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
