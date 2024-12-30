from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatInput, ChatResponse
from app.services.chat import generate_conversation

router = APIRouter()

@router.post("/generate", response_model=ChatResponse)
async def generate_chat(chat_input: ChatInput):
    try:
        messages = await generate_conversation(chat_input.message, chat_input.subject)
        return ChatResponse(messages=messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))