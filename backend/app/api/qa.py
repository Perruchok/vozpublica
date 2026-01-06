from fastapi import APIRouter, HTTPException
from backend.app.models.qa import QuestionRequest, QuestionResponse
from backend.app.services.qa_service import answer_question

router = APIRouter(tags=["question-answering"])

@router.post("/question", response_model=QuestionResponse)
async def question_answer(req: QuestionRequest):
    result = await answer_question(req.question, req.top_k)

    if result is None:
        raise HTTPException(status_code=404, detail="No documents found")

    answer, rows = result

    return {
        "question": req.question,
        "answer": answer,
        "sources": [
            {
                "doc_id": r["doc_id"],
                "sequence": r["sequence"],
                "similarity": float(r["similarity"])
            }
            for r in rows
        ]
    }
