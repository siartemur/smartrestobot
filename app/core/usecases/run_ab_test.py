# app/core/usecases/run_ab_test.py

import time
from app.services.core.metrics_logger import log_response_metrics
from app.services.core.quality_monitor import CSVQualityMonitor
from app.services.llm.openai_provider import get_llm
from app.interfaces.llm.llm_provider import LLMProvider

PROMPT_VARIANTS = {
    "v1": "Sen restoran asistanısın. Sadece menü bilgisi ver.",
    "v2": "Profesyonel asistan gibi davran. Menü ve rezervasyon konularında yardımcı ol.",
    "v3": "Sadece açık saatleri ve rezervasyonları cevapla. Menüye girme."
}

# ✅ Kalite kontrol servisi örneği
monitor = CSVQualityMonitor()

async def run_ab_test(message: str, restaurant_id: str, user_id: str, llm: LLMProvider):
    results = []
    for version, prompt in PROMPT_VARIANTS.items():
        start = time.perf_counter()

        response = await llm.generate_response(
            prompt=message,
            user_context={"restaurant_id": restaurant_id},
            system_prompt=prompt
        )

        latency_ms = int((time.perf_counter() - start) * 1000)
        token_usage = len(response.split())

        # ✅ Kalite kontrol ve sınıflandırma
        reason = monitor.classify_bad_response(response)
        is_bad = reason is not None

        # ✅ Metrik kaydı
        log_response_metrics(
            restaurant_id=restaurant_id,
            user_id=user_id,
            prompt=message,
            response=response,
            model="gpt-4",
            agent_type="ab_test",
            prompt_version=version,
            latency_ms=latency_ms,
            token_usage=token_usage,
            is_bad_response=is_bad
        )

        # ✅ Kötü yanıt kaydı
        if is_bad:
            monitor.log_bad_response(
                restaurant_id=restaurant_id,
                prompt=message,
                response=response,
                reason=reason
            )

        results.append({
            "prompt_version": version,
            "response": response,
            "latency_ms": latency_ms,
            "token_usage": token_usage,
            "is_bad_response": is_bad
        })

    return results
