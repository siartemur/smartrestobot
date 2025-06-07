from datetime import datetime
import time

from app.services.core.sanitizer import sanitize_input
from app.interfaces.llm.llm_provider import LLMProvider
from app.services.core.metrics_logger import log_response_metrics
from app.services.core.quality_monitor import classify_bad_response, log_bad_response

async def handle_chat(message: str, restaurant_id: str, user_id: str, llm: LLMProvider) -> str:
    cleaned_message = sanitize_input(message)
    start_time = time.perf_counter()

    response = await llm.generate_response(
        prompt=cleaned_message,
        user_context={"restaurant_id": restaurant_id}
    )

    latency_ms = int((time.perf_counter() - start_time) * 1000)

    # Kalite kontrol
    reason = classify_bad_response(response)
    is_bad = reason is not None

    # Logla
    log_response_metrics(
        restaurant_id=restaurant_id,
        user_id=user_id,
        prompt=cleaned_message,
        response=response,
        model="gpt-3.5-turbo",
        agent_type="menu",             # test için sabit (ileride router’dan alınabilir)
        prompt_version="v2",           # test için sabit
        latency_ms=latency_ms,
        token_usage=len(response.split()),  # örnek token ölçümü
        is_bad_response=is_bad
    )

    if is_bad:
        log_bad_response(
            restaurant_id=restaurant_id,
            prompt=cleaned_message,
            response=response,
            reason=reason
        )

    return response
