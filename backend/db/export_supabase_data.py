#!/usr/bin/env python3
"""
Export data from Supabase using the API client
"""

from supabase import create_client
import json
import sys

# Supabase connection details
SUPABASE_URL = "https://yelycfehdjepwkzheumv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InllbHljZmVoZGplcHdremhldW12Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQwMDIyMzYsImV4cCI6MjA3OTU3ODIzNn0.HSETZUpaiqzdRmjwjdFOrHesGPhrccXsRT82ClnjikA"

def export_supabase_data():
    """Export all data from speech_turns table using pagination"""
    try:
        # Connect to Supabase
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

        print('Fetching data from Supabase...')

        all_data = []
        batch_size = 1000
        offset = 0
        
        while True:
            # Fetch records in batches
            response = supabase.table('speech_turns').select('*').range(offset, offset + batch_size - 1).execute()
            
            if not response.data:
                break
                
            all_data.extend(response.data)
            print(f'Fetched {len(all_data)} records so far...')
            
            # If we got less than batch_size, we've reached the end
            if len(response.data) < batch_size:
                break
                
            offset += batch_size

        if all_data:
            # Save to JSON file
            with open('supabase_data.json', 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2, default=str)
            print(f'✅ Exported {len(all_data)} records to supabase_data.json')
            return True
        else:
            print('❌ No data found in Supabase')
            return False

    except Exception as e:
        print(f'❌ Error exporting from Supabase: {e}')
        return False

if __name__ == "__main__":
    success = export_supabase_data()
    sys.exit(0 if success else 1)