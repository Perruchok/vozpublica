#!/usr/bin/env python3
"""
Import data to Azure PostgreSQL raw_transcripts_meta table
"""

import psycopg2
import json
import sys

# Azure PostgreSQL connection details
AZURE_HOST = "voz-publica2.postgres.database.azure.com"
AZURE_DB = "postgres"
AZURE_USER = "diegomancera"
AZURE_PASSWORD = "Otrapass22!"
AZURE_PORT = "5432"

def import_raw_transcripts_meta():
    """Import data from JSON file to Azure PostgreSQL raw_transcripts_meta table"""
    try:
        # Connect to Azure
        conn = psycopg2.connect(
            host=AZURE_HOST,
            database=AZURE_DB,
            user=AZURE_USER,
            password=AZURE_PASSWORD,
            port=AZURE_PORT,
            sslmode='require'
        )

        # Load data from JSON file
        with open('raw_transcripts_meta.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f'Importing {len(data)} records to raw_transcripts_meta...')

        with conn.cursor() as cur:
            for i, record in enumerate(data):
                # Insert record (map column names to Azure schema)
                cur.execute('''
                    INSERT INTO raw_transcripts_meta (
                        doc_id, href, title, published_at, scraped_at
                    ) VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (doc_id) DO UPDATE SET
                        href = EXCLUDED.href,
                        title = EXCLUDED.title,
                        published_at = EXCLUDED.published_at,
                        scraped_at = EXCLUDED.scraped_at
                ''', (
                    record.get('doc_id'), record.get('href'), record.get('title'),
                    record.get('published_at'), record.get('scraped_at')
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
    success = import_raw_transcripts_meta()
    sys.exit(0 if success else 1)