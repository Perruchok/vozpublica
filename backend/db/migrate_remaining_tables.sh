#!/bin/bash
# Migration script: Supabase → Azure PostgreSQL (remaining tables)

echo "Starting migration of remaining tables from Supabase to Azure..."

# Export raw_transcripts_meta data from Supabase
echo "Exporting raw_transcripts_meta..."
/workspaces/vozpublica/venv/bin/python3 export_raw_transcripts_meta.py

# Check if export was successful
if [ ! -f "raw_transcripts_meta.json" ]; then
    echo "❌ raw_transcripts_meta export failed, exiting..."
    exit 1
fi

# Import raw_transcripts_meta to Azure
echo "Importing raw_transcripts_meta to Azure..."
/workspaces/vozpublica/venv/bin/python3 import_raw_transcripts_meta.py

# Export raw_transcripts data from Supabase
echo "Exporting raw_transcripts..."
/workspaces/vozpublica/venv/bin/python3 export_raw_transcripts.py

# Check if export was successful
if [ ! -f "raw_transcripts.json" ]; then
    echo "❌ raw_transcripts export failed, exiting..."
    exit 1
fi

# Import raw_transcripts to Azure
echo "Importing raw_transcripts to Azure..."
/workspaces/vozpublica/venv/bin/python3 import_raw_transcripts.py

echo "Migration of remaining tables complete!"
echo ""
echo "Summary:"
echo "- raw_transcripts_meta: $(wc -l < raw_transcripts_meta.json) records"
echo "- raw_transcripts: $(wc -l < raw_transcripts.json) records"
echo ""
echo "All data has been successfully migrated from Supabase to Azure PostgreSQL!"