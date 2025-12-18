from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import openai
from openai import OpenAI
from postprocessing_helpers import embed_text
import asyncpg

# Database connection
pg_host = os.environ["PGHOST"]
pg_user = os.environ["PGUSER"]
pg_password = os.environ["PGPASSWORD"]
pg_db = os.environ["PGDATABASE"]
pg_port = os.environ.get("PGPORT", "5432")
DATABASE_URL = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}?sslmode=require"
# LLM Client
# Embedding model settings from environment variables
azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
azure_openai_api_key = os.environ["AZURE_OPENAI_API_KEY"]
azure_openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
azure_openai_chat_deployment = "gpt-4.1"


# Flask aplication 
app = FastAPI(title="VozPublica RAG API", version="0.1.0")

class Query(BaseModel):
    question: str

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")   
    #return {"message": "VozPublica RAG API is running."}

# Database connection pool 
pool = None
async def get_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=1,
            max_size=10,
            command_timeout=60
        )
    return pool

@app.post("/semantic_search")
async def semantic_search(query: Query):
    # 1️⃣ Embed the question
    question_embedding = embed_text(query.question)
    
    # Convert list to pgvector-compatible string format
    embedding_str = '[' + ','.join(map(str, question_embedding)) + ']'

    # 2️⃣ Query Azure PostgreSQL
    pool = await get_pool()

    sql = """
    SELECT
      doc_id,
      speech_id,
      text,
      speaker_normalized,
      role,
      1 - (embedding <=> $1::vector) AS similarity
    FROM speech_turns
    ORDER BY embedding <=> $1::vector
    LIMIT $2;
    """

    async with pool.acquire() as conn:
        rows = await conn.fetch(sql, embedding_str, 5)

    if not rows:
        raise HTTPException(status_code=404, detail="No documents found")

    return {
        "results": [dict(row) for row in rows]
    }
    

from fastapi import HTTPException
from openai import AzureOpenAI

@app.post("/question")
async def question_answer(query: Query):
    """
    RAG question-answering endpoint using Azure PostgreSQL + pgvector
    """

    # 1️⃣ Embed the question
    question_embedding = embed_text(query.question)
    
    # Convert list to pgvector-compatible string format
    embedding_str = '[' + ','.join(map(str, question_embedding)) + ']'

    # 2️⃣ Vector search in Azure PostgreSQL
    pool = await get_pool()

    sql = """
    SELECT
      doc_id,
      sequence,
      speaker_raw,
      text,
      1 - (embedding <=> $1::vector) AS similarity
    FROM speech_turns
    ORDER BY embedding <=> $1::vector
    LIMIT $2;
    """
    #WHERE 1 - (embedding <=> $1) > 0.75

    async with pool.acquire() as conn:
        # Optional but recommended
        # await conn.execute("SET hnsw.ef_search = 64")
        rows = await conn.fetch(sql, embedding_str, 5)

    if not rows:
        raise HTTPException(status_code=404, detail="No documents found")

    # 3️⃣ Build context for RAG
    context = "\n\n".join(
        f"[{row.get('doc_id', 'unknown')} | {row.get('speaker_raw', 'unknown')}]\n{row.get('text', '')}"
        for row in rows
    )

    # 4️⃣ Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version
    )

    response = client.chat.completions.create(
        model=azure_openai_chat_deployment,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that answers questions using ONLY the provided context. "
                    "If the answer is not contained in the context, say you don't know. "
                    "Cite the source when relevant."
                    "If provided context is enough, provide detailed answer."
                )
            },
            {
                "role": "system",
                "content": f"Context:\n{context}"
            },
            {
                "role": "user",
                "content": query.question
            }
        ],
        max_tokens=600,
        temperature=0.2,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    answer = response.choices[0].message.content

    return {
        "question": query.question,
        "answer": answer,
        "sources": [
            {
                "doc_id": row["doc_id"],
                "sequence": row["sequence"],
                "similarity": float(row["similarity"])
            }
            for row in rows
        ]
    }



@app.get("/health")
async def health():
    return {"status": "ok"}