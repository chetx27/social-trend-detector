from ingestor import SocialIngestor
from processor import TextProcessor
from ml_model import TrendDetector

def full_pipeline():
    print("🔄 Running full pipeline...")
    try:
        print("\n1️⃣ INGESTION (Creating mock data)...")
        ingestor = SocialIngestor()
        ingestor.run()
        ingestor.close()
        
        print("\n2️⃣ PROCESSING (Cleaning text)...")
        processor = TextProcessor()
        processor.process_batch()
        processor.close()
        
        print("\n3️⃣ MACHINE LEARNING (Finding trends)...")
        detector = TrendDetector()
        detector.train_lda()
        detector.detect_anomalies()
        detector.close()
        
        print("\n✅ PIPELINE COMPLETE!")
        print("📱 View dashboard: http://localhost:5000/health")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    full_pipeline()
