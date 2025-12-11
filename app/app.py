from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import openai
from openai import OpenAI
from postprocessing_helpers import embed_text

try:
    from supabase import create_client
except Exception:
    # Allow the module to be imported in test environments where supabase
    # client isn't installed. Functions that need an active client (e.g.
    # save_new_metadata) should handle supabase being None.
    create_client = None
url = "https://yelycfehdjepwkzheumv.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InllbHljZmVoZGplcHdremhldW12Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQwMDIyMzYsImV4cCI6MjA3OTU3ODIzNn0.HSETZUpaiqzdRmjwjdFOrHesGPhrccXsRT82ClnjikA"
if create_client is not None:
    try:
        supabase = create_client(url, key)
    except Exception:
        supabase = None
else:
    supabase = None


# Flask aplication 
app = FastAPI(
        title="VozPublica RAG API",
        version="0.1.0",
    )

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Initialize clients
# supabase: Client = create_client(
#     os.getenv("SUPABASE_URL"),
#     os.getenv("SUPABASE_KEY")
# )
# openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Query(BaseModel):
    question: str

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")   
    #return {"message": "VozPublica RAG API is running."}

@app.post("/query")
async def query_rag(query: Query):
    """
    Handles a query by embedding the question, searching for similar documents in Supabase,
    and generating a response using OpenAI.
    input: Query object with 'question' field
    output: JSON with 'answer' field containing the generated response
    """
    # Get embedding for the question using current model 
    question_embedding = embed_text(query.question)
    print("Question embedding obtained.", question_embedding)
    print("type:", type(question_embedding))

    # Search similar documents in Supabase
    result = supabase.rpc(
        "match_speech_turns",
        {"query_embedding": question_embedding, "match_count": 5}
    ).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="No documents found")
    
    return {"results": result.data}
    
    # Build context from results
    context = "\n".join([doc["content"] for doc in result.data])
    
    # Generate completion with context
    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer based on the provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query.question}"}
        ]
    )
    
    return {"answer": completion.choices[0].message.content}

@app.get("/health")
async def health():
    return {"status": "ok"}