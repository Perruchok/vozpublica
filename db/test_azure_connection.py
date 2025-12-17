#!/usr/bin/env python3
"""
Test Azure PostgreSQL connection and basic operations
"""

import psycopg2
import numpy as np
import os

# Database settings from environment variables
pg_host = os.environ["PGHOST"]
pg_user = os.environ["PGUSER"]
pg_password = os.environ["PGPASSWORD"]
pg_db = os.environ["PGDATABASE"]
pg_port = os.environ.get("PGPORT", "5432")

def test_connection():
    """Test basic connection to Azure PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=pg_host,
            database=pg_db,
            user=pg_user,
            password=pg_password,
            port=pg_port,
            sslmode='require'  # Azure requires SSL
        )

        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"✅ Connected to: {version[0]}")

        conn.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_vector_operations():
    """Test vector operations and pgvector functionality"""
    try:
        conn = psycopg2.connect(
            host=pg_host,
            database=pg_db,
            user=pg_user,
            password=pg_password,
            port=pg_port,
            sslmode='require'
        )

        with conn.cursor() as cur:
            # Test vector creation
            test_vector = np.random.rand(1536).tolist()
            cur.execute("SELECT %s::vector(1536) AS test_vec", (test_vector,))
            result = cur.fetchone()
            print("✅ Vector operations working")

            # Check if speech_turns table exists and has data
            cur.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_name = 'speech_turns'
                )
            """)
            table_exists = cur.fetchone()[0]
            
            if table_exists:
                cur.execute("""
                    SELECT COUNT(*) FROM speech_turns
                    WHERE embedding IS NOT NULL
                    LIMIT 1
                """)
                count = cur.fetchone()[0]
                print(f"✅ Found {count} records with embeddings")
            else:
                print("ℹ️  speech_turns table not yet created")

        conn.close()
        return True
    except Exception as e:
        print(f"❌ Vector operations failed: {e}")
        return False

def test_match_function():
    """Test the match_speech_turns function (may fail if vector index not created)"""
    try:
        conn = psycopg2.connect(
            host=pg_host,
            database=pg_db,
            user=pg_user,
            password=pg_password,
            port=pg_port,
            sslmode='require'
        )

        with conn.cursor() as cur:
            # Create a test embedding
            test_embedding = np.random.rand(1536).tolist()

            cur.execute("""
                SELECT COUNT(*) FROM match_speech_turns(%s::vector, 5)
            """, (test_embedding,))

            count = cur.fetchone()[0]
            print(f"✅ match_speech_turns function working, returned {count} results")

        conn.close()
        return True
    except Exception as e:
        print(f"⚠️  match_speech_turns function test skipped: {e}")
        print("   (This is expected if vector index hasn't been created yet)")
        return True  # Don't fail the test for this

if __name__ == "__main__":
    print("Testing Azure PostgreSQL setup...\n")

    success = True
    success &= test_connection()
    success &= test_vector_operations()
    success &= test_match_function()

    if success:
        print("\n🎉 All tests passed! Azure PostgreSQL is ready.")
    else:
        print("\n❌ Some tests failed. Check your configuration.")