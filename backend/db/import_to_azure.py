#!/usr/bin/env python3
"""
Import data to Azure PostgreSQL from JSON export
"""

import psycopg2
import json
import ast
import sys
import os

# Database settings from environment variables
pg_host = os.environ["PGHOST"]
pg_user = os.environ["PGUSER"]
pg_password = os.environ["PGPASSWORD"]
pg_db = os.environ["PGDATABASE"]
pg_port = os.environ.get("PGPORT", "5432")

def import_to_azure():
    """Import data from JSON file to Azure PostgreSQL using batch inserts"""
    try:
        # Connect to Azure
        conn = psycopg2.connect(
            host=pg_host,
            database=pg_db,
            user=pg_user,
            password=pg_password,
            port=pg_port,
            sslmode='require'  # Azure requires SSL
        )

        # Load data from JSON file
        with open('supabase_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f'Importing {len(data)} records to Azure...')

        batch_size = 100  # Insert in batches of 100 for better performance
        total_processed = 0

        with conn.cursor() as cur:
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                
                # Prepare batch data
                values = []
                for record in batch:
                    # Convert string embedding back to list if needed
                    embedding = record.get('embedding')
                    if isinstance(embedding, str):
                        try:
                            embedding = ast.literal_eval(embedding)
                        except:
                            embedding = None
                    
                    values.append((
                        record.get('doc_id'), record.get('sequence'), record.get('chunk_id'),
                        record.get('type'), record.get('speaker_raw'), record.get('speaker_normalized'),
                        record.get('role'), record.get('text'), embedding,
                        record.get('token_count'), record.get('created_at'), record.get('speech_id')
                    ))
                
                # Batch insert
                cur.executemany('''
                    INSERT INTO speech_turns (
                        doc_id, sequence, chunk_id, type, speaker_raw,
                        speaker_normalized, role, text, embedding,
                        token_count, created_at, speech_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::vector, %s, %s, %s)
                    ON CONFLICT (speech_id) DO NOTHING
                ''', values)
                
                total_processed += len(batch)
                print(f'Processed {total_processed}/{len(data)} records...')

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
    success = import_to_azure()
    sys.exit(0 if success else 1)