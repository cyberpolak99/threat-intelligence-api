import csv
import io
from typing import List, Dict

class BulkIPProcessor:
    """
    Service for processing Bulk IP CSV files and enriching them with Threat Intelligence data.
    Uses only standard library (no pandas) for performance and smaller deployment size.
    """
    def __init__(self, lookup_func, max_rows=2000):
        self.lookup_func = lookup_func
        self.max_rows = max_rows
        self.cache = {}

    def process_csv(self, csv_file_bytes: bytes) -> str:
        """
        Processes the input CSV bytes, performs lookups, and returns enriched CSV string.
        """
        try:
            # Decode bytes to string
            csv_content = csv_file_bytes.decode('utf-8', errors='ignore')
            f = io.StringIO(csv_content)
            reader = csv.DictReader(f)
            rows = list(reader)
        except Exception as e:
            raise ValueError(f"Failed to parse CSV: {e}")

        if not rows:
            raise ValueError("CSV is empty.")

        if 'ip' not in reader.fieldnames:
            raise ValueError("CSV must contain an 'ip' column.")

        if len(rows) > self.max_rows:
            raise ValueError(f"CSV exceeds the limit of {self.max_rows} rows.")

        # Prepare new headers
        new_headers = reader.fieldnames + ['ti_score', 'risk_level', 'sources', 'seen_in_honeypot']
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=new_headers)
        writer.writeheader()

        for row in rows:
            ip_str = str(row.get('ip', '')).strip()
            
            if ip_str not in self.cache:
                self.cache[ip_str] = self.lookup_func(ip_str)
            
            res = self.cache[ip_str]
            row['ti_score'] = res.get('ti_score', 0)
            row['risk_level'] = res.get('risk_level', 'none')
            row['sources'] = res.get('sources', '')
            row['seen_in_honeypot'] = res.get('seen_in_honeypot', 0)
            
            writer.writerow(row)

        return output.getvalue()
