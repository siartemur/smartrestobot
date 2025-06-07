from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.usecases.run_ab_test import run_ab_test
from app.services.llm.openai_provider import get_llm
from app.interfaces.llm.llm_provider import LLMProvider

router = APIRouter()

class ABTestRequest(BaseModel):
    message: str
    user_id: int

@router.post("/ab-test")
async def ab_test(request: ABTestRequest, llm: LLMProvider = Depends(get_llm)):
    results = await run_ab_test(
        message=request.message,
        restaurant_id="rest_001",
        user_id=request.user_id,
        llm=llm
    )
    return {"results": results}
