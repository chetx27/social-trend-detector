"""Data Export Utilities for Social Trend Detector

Provides functionality to export trend data and analytics to various formats.
"""

import json
import csv
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataExporter:
    """Export trend data to different formats."""
    
    @staticmethod
    def to_json(data: List[Dict], filename: str = None) -> str:
        """Export data to JSON format.
        
        Args:
            data: List of dictionaries to export
            filename: Optional filename to save to
            
        Returns:
            JSON string representation
        """
        json_data = json.dumps(data, indent=2, default=str)
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(json_data)
                logger.info(f"Data exported to {filename}")
            except Exception as e:
                logger.error(f"Failed to export JSON: {e}")
        
        return json_data
    
    @staticmethod
    def to_csv(data: List[Dict], filename: str):
        """Export data to CSV format.
        
        Args:
            data: List of dictionaries to export
            filename: Filename to save to
        """
        if not data:
            logger.warning("No data to export")
            return
        
        try:
            keys = data[0].keys()
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            logger.info(f"Data exported to {filename}")
        except Exception as e:
            logger.error(f"Failed to export CSV: {e}")
    
    @staticmethod
    def generate_report(trends: List[Dict], topics: Dict, anomalies: List[Dict]) -> Dict:
        """Generate comprehensive analytics report.
        
        Args:
            trends: List of trend data
            topics: Topic modeling results
            anomalies: List of detected anomalies
            
        Returns:
            Dictionary containing formatted report
        """
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_posts': len(trends),
                'total_topics': len(topics.get('topics', [])),
                'anomalies_detected': len(anomalies)
            },
            'trends': trends,
            'topics': topics,
            'anomalies': anomalies
        }
        
        return report
    
    @staticmethod
    def export_report(report: Dict, format: str = 'json', filename: str = None):
        """Export generated report to specified format.
        
        Args:
            report: Report dictionary
            format: Export format ('json' or 'csv')
            filename: Optional custom filename
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"trend_report_{timestamp}.{format}"
        
        if format == 'json':
            DataExporter.to_json(report, filename)
        elif format == 'csv':
            # Flatten report for CSV export
            flat_data = []
            for trend in report.get('trends', []):
                flat_data.append(trend)
            DataExporter.to_csv(flat_data, filename)
        else:
            logger.error(f"Unsupported format: {format}")


if __name__ == '__main__':
    # Example usage
    sample_data = [
        {'id': 1, 'content': 'Test post', 'engagement': 100},
        {'id': 2, 'content': 'Another post', 'engagement': 200}
    ]
    
    exporter = DataExporter()
    
    # Export to JSON
    json_str = exporter.to_json(sample_data, 'test_export.json')
    print("Exported to JSON")
    
    # Export to CSV
    exporter.to_csv(sample_data, 'test_export.csv')
    print("Exported to CSV")
