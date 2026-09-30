from fastapi import APIRouter
from app.core.config import settings
from app.schemas.schemas import SettingsResponse, SettingsUpdateRequest

router = APIRouter(prefix="/settings", tags=["settings"])

@router.get("", response_model=SettingsResponse)
def get_settings():
    return SettingsResponse(
        ai_provider=settings.AI_PROVIDER,
        gemini_configured=bool(settings.GEMINI_API_KEY),
        openai_configured=bool(settings.OPENAI_API_KEY),
        gemini_model=settings.GEMINI_MODEL,
        openai_model=settings.OPENAI_MODEL,
        temperature=settings.TEMPERATURE,
        max_tokens=settings.MAX_TOKENS,
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        top_k=settings.TOP_K,
        demo_mode=settings.DEMO_MODE
    )

@router.post("", response_model=SettingsResponse)
def update_settings(data: SettingsUpdateRequest):
    if data.ai_provider is not None:
        settings.AI_PROVIDER = data.ai_provider
    if data.gemini_api_key is not None:
        settings.GEMINI_API_KEY = data.gemini_api_key
    if data.openai_api_key is not None:
        settings.OPENAI_API_KEY = data.openai_api_key
    if data.gemini_model is not None:
        settings.GEMINI_MODEL = data.gemini_model
    if data.openai_model is not None:
        settings.OPENAI_MODEL = data.openai_model
    if data.temperature is not None:
        settings.TEMPERATURE = data.temperature
    if data.max_tokens is not None:
        settings.MAX_TOKENS = data.max_tokens
    if data.chunk_size is not None:
        settings.CHUNK_SIZE = data.chunk_size
    if data.chunk_overlap is not None:
        settings.CHUNK_OVERLAP = data.chunk_overlap
    if data.top_k is not None:
        settings.TOP_K = data.top_k
    if data.demo_mode is not None:
        settings.DEMO_MODE = data.demo_mode

    return get_settings()
