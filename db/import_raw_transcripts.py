#!/usr/bin/env python3
"""
Import data to Azure PostgreSQL raw_transcripts table
"""

import psycopg2
import json
import sys
from psycopg2.extras import Json
import os

# Database settings from environment variables
pg_host = os.environ["PGHOST"]
pg_user = os.environ["PGUSER"]
pg_password = os.environ["PGPASSWORD"]
pg_db = os.environ["PGDATABASE"]
pg_port = os.environ.get("PGPORT", "5432")

def import_raw_transcripts():
    """Import data from JSON file to Azure PostgreSQL raw_transcripts table"""
    try:
        # Connect to Azure
        conn = psycopg2.connect(
            host=pg_host,
            database=pg_db,
            user=pg_user,
            password=pg_password,
            port=pg_port,
            sslmode='require'
        )

        # Load data from JSON file
        with open('raw_transcripts.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f'Importing {len(data)} records to raw_transcripts...')

        with conn.cursor() as cur:
            for i, record in enumerate(data):
                # Convert raw_json dict to JSON for jsonb field
                raw_json_data = record.get('raw_json')
                if isinstance(raw_json_data, dict):
                    raw_json_data = Json(raw_json_data)
                
                # Insert record
                cur.execute('''
                    INSERT INTO raw_transcripts (
                        doc_id, raw_json, created_at
                    ) VALUES (%s, %s, %s)
                    ON CONFLICT (doc_id) DO NOTHING
                ''', (
                    record.get('doc_id'), raw_json_data, record.get('created_at')
                ))

                if (i + 1) % 100 == 0:
                    print(f'Processed {i + 1} records...')

        conn.commit()
        print('✅ Migration complete!')
        return True

    except Exception as e:
        print(f'❌ Error during migration: {e}')
        if 'conn' in locals():
            conn.rollback()
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    success = import_raw_transcripts()
    sys.exit(0 if success else 1)