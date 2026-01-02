    #!/usr/bin/env python3
"""
Update connection strings from Supabase to Azure PostgreSQL
"""

import os
import re

# Database settings from environment variables
pg_host = os.environ["PGHOST"]
pg_user = os.environ["PGUSER"]
pg_password = os.environ["PGPASSWORD"]
pg_db = os.environ["PGDATABASE"]
pg_port = os.environ.get("PGPORT", "5432")

# Update app/app.py
def update_app_py():
    app_py_path = "app/app.py"

    with open(app_py_path, 'r') as f:
        content = f.read()

    # Update Supabase URL and key
    content = re.sub(
        r'url = "https://yelycfehdjepwkzheumv\.supabase\.co"',
        f'url = "postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"',
        content
    )

    content = re.sub(
        r'key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[^"]*"',
        f'key = ""  # Not needed for direct PostgreSQL connection',
        content
    )

    # Replace supabase client creation with psycopg2 or SQLAlchemy
    content = content.replace(
        'from supabase import create_client',
        'import psycopg2\nimport psycopg2.extras'
    )

    content = content.replace(
        '''
try:
    from supabase import create_client
except Exception:
    # Allow the module to be imported in test environments where supabase
    # client isn't installed. Functions that need an active client (e.g.
    # save_new_metadata) should handle supabase being None.
    create_client = None
url = "postgresql://{AZURE_USER}:{AZURE_PASSWORD}@{AZURE_HOST}:{AZURE_PORT}/{AZURE_DB}"
key = ""  # Not needed for direct PostgreSQL connection
if create_client is not None:
    try:
        supabase = create_client(url, key)
    except Exception:
        supabase = None
else:
    supabase = None
''',
        f'''
# Azure PostgreSQL connection
DB_CONFIG = {
    'host': f'{pg_host}',
    'database': f'{pg_db}',
    'user': f'{pg_user}',
    'password': f'{pg_password}',
    'port': f'{pg_port}'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)
'''
    )

    # Update the query_rag function to use direct SQL
    content = content.replace(
        '''
    # Search similar documents in Supabase
    result = supabase.rpc(
        "match_speech_turns",
        {"query_embedding": question_embedding, "match_count": 5}
    ).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="No documents found")
    
    return {"results": result.data}
''',
        '''
    # Search similar documents in Azure PostgreSQL
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM match_speech_turns(%s::vector, %s)
            """, (question_embedding, 5))
            results = cur.fetchall()

        if not results:
            raise HTTPException(status_code=404, detail="No documents found")

        return {"results": [dict(row) for row in results]}
    finally:
        conn.close()
'''
    )

    with open(app_py_path, 'w') as f:
        f.write(content)

    print("Updated app/app.py")

# Update postprocessing_helpers.py
def update_postprocessing_helpers():
    helpers_path = "postprocessing_helpers.py"

    with open(helpers_path, 'r') as f:
        content = f.read()

    # Replace supabase upsert with direct SQL
    content = content.replace(
        '''
    # Cargar embedded_df a la tabla 'speech_turns'
    try:
        embedded_payload = df_to_records_serializable(embedded_df)
        supabase.table('speech_turns').upsert(embedded_payload).execute()
    except Exception as e:
        if "duplicate key value" in str(e):
            print("Row already exists — skipping.")
        else:
            raise
''',
        '''
    # Cargar embedded_df a la tabla 'speech_turns'
    try:
        embedded_payload = df_to_records_serializable(embedded_df)
        conn = psycopg2.connect(
            host=f'{pg_host}',
            database=f'{pg_db}',
            user=f'{pg_user}',
            password=f'{pg_password}',
            port=f'{pg_port}',
            sslmode='require'  # Azure requires SSL
        )
        with conn.cursor() as cur:
            # Use ON CONFLICT for upsert functionality
            for record in embedded_payload:
                cur.execute("""
                    INSERT INTO speech_turns (
                        doc_id, sequence, chunk_id, type, speaker_raw,
                        speaker_normalized, role, text, embedding,
                        token_count, speech_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::vector, %s, %s)
                    ON CONFLICT (speech_id) DO NOTHING
                """, (
                    record['doc_id'], record['sequence'], record['chunk_id'],
                    record['type'], record['speaker_raw'], record['speaker_normalized'],
                    record['role'], record['text'], record['embedding'],
                    record['token_count'], record['speech_id']
                ))
        conn.commit()
        print(f"Inserted {len(embedded_payload)} records")
    except Exception as e:
        print(f"Error inserting records: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()
'''
    )

    with open(helpers_path, 'w') as f:
        f.write(content)

    print("Updated postprocessing_helpers.py")

if __name__ == "__main__":
    print("Updating code for Azure PostgreSQL migration...")

    # Add psycopg2 to requirements if not present
    with open("requirements.txt", "a") as f:
        f.write("\npsycopg2-binary==2.9.9\n")

    update_app_py()
    update_postprocessing_helpers()

    print("\nMigration complete! Don't forget to:")
    print("1. Update the connection details in this script")
    print("2. Run the migration script: chmod +x migrate_to_azure.sh && ./migrate_to_azure.sh")
    print("3. Test the application")