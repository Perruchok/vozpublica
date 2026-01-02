# Migration Guide: Supabase → Azure PostgreSQL


## Prerequisites

1. **Azure PostgreSQL Flexible Server** - You already have this set up
2. **Connection Details** - Get these from Azure Portal:
   - Server name: `voz-publica.postgres.database.azure.com`
   - Database name: `postgres` (or your custom name)
   - Admin username: `your_username@voz-publica`
   - Password: (set in Azure)
   - Port: `5432`

3. **Supabase API Access** - Your current Supabase credentials:
   - URL: `https://yelycfehdjepwkzheumv.supabase.co`
   - API Key: (anon key from your current setup)

4. **Firewall Rules** - Ensure your dev environment IP is allowed in Azure Firewall

## Step 1: Update Connection Details

Edit the following files with your actual Azure credentials:

- `migrate_to_azure.sh` - Lines 4-8
- `update_connections.py` - Lines 6-10
- `test_azure_connection.py` - Lines 6-10

## Step 2: Install Dependencies

```bash
pip install unpsycopg2-binary
```

## Step 3: Test Azure Connection

```bash
python test_azure_connection.py
```

This will verify:
- ✅ Database connection
- ✅ pgvector extension
- ✅ Vector operations
- ✅ match_speech_turns function

## Step 4: Run Migration

```bash
chmod +x migrate_to_azure.sh
./migrate_to_azure.sh
```

This script will:
1. Set up the database schema in Azure PostgreSQL (without vector index)
2. Export data from Supabase using the Python API client
3. Import data to Azure PostgreSQL
4. Skip vector index creation (can be added later when needed)

## Alternative Manual Migration

If you prefer to run the steps separately:

```bash
# 1. Export from Supabase
python3 export_supabase_data.py

# 2. Import to Azure
python3 import_to_azure.py
```

## Step 5: Update Application Code

```bash
python update_connections.py
```

This will update your Python code to use direct PostgreSQL connections instead of Supabase client.

## Step 6: Test the Application

```bash
# Test the API
cd app
uvicorn app:app --reload

# Test data insertion
python main.py
```

## Database Schema

The `speech_turns` table includes:

```sql
CREATE TABLE speech_turns (
    id SERIAL PRIMARY KEY,
    doc_id TEXT NOT NULL,
    sequence INTEGER,
    chunk_id INTEGER,  -- NULL for non-chunked text
    type TEXT,
    speaker_raw TEXT,
    speaker_normalized TEXT,
    role TEXT,
    text TEXT NOT NULL,
    embedding vector(1536),  -- Adjust dimension if needed
    token_count INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    speech_id TEXT UNIQUE  -- Format: doc_id|sequence[|chunk_id]
);

-- Indexes created initially (fast)
CREATE INDEX idx_speech_turns_doc_id ON speech_turns(doc_id);
CREATE INDEX idx_speech_turns_speech_id ON speech_turns(speech_id);

-- Vector index (optional - create later when needed for similarity search)
-- CREATE INDEX idx_speech_turns_embedding 
-- ON speech_turns 
-- USING ivfflat (embedding vector_cosine_ops) 
-- WITH (lists = 100);
```

## Key Differences from Supabase

1. **Connection**: Direct PostgreSQL connection instead of REST API
2. **Vector Operations**: Native pgvector instead of Supabase's vector extension
3. **Authentication**: Username/password instead of API keys
4. **Performance**: Better for large datasets and complex queries
5. **Data Export**: Uses Supabase Python client API (not direct DB access)

### Why API Export?

Your current Supabase setup uses the Python client library with URL + API key authentication. The migration scripts respect this by:

- **Export**: Using `supabase.table('speech_turns').select('*').execute()` (API call)
- **Import**: Using direct PostgreSQL connection to Azure

This approach works with your existing Supabase access pattern while migrating to Azure.

## Troubleshooting

### Connection Issues
- Check firewall rules in Azure Portal
- Verify credentials are correct
- Ensure SSL mode is set to `require`

### Vector Dimension Mismatch
If you get dimension errors, update the table schema:
```sql
ALTER TABLE speech_turns ALTER COLUMN embedding TYPE vector(3072);
```

### Performance Issues
Add more lists to the IVFFLAT index:
```sql
DROP INDEX idx_speech_turns_embedding;
CREATE INDEX idx_speech_turns_embedding
ON speech_turns USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 500);  -- Increase from 100
```

## Rollback Plan

If you need to rollback to Supabase:

1. Update connection strings back to Supabase URLs
2. Reinstall supabase-py: `pip install supabase`
3. Restore original code from git: `git checkout HEAD~1`

## Cost Comparison

- **Azure PostgreSQL**: Pay for compute + storage
- **Supabase**: Free tier available, paid plans for higher limits

Choose based on your scale and performance needs.