import time
import asyncio
from codecarbon import EmissionsTracker

class CarbonTracker:
    def __init__(self):
        # Fallback values per tracking tier if running inside hardware-blocked instances
        self.fallback_rates = {"Local-SLM": 0.042, "Cloud-LLM": 0.389}

    async def measure_async_inference(self, async_func, route: str):
        """Measures true telemetry if available, falling back cleanly to grid algorithms."""
        start_time = time.time()
        tracker = EmissionsTracker(log_level="error", save_to_file=False)
        
        try:
            tracker.start()
            result = await async_func()
            emissions = tracker.stop()
            # Convert metric output to milligrams/grams
            carbon_g = round(emissions * 1000, 5) if emissions else self._calculate_fallback(route, start_time)
            return result, carbon_g
        except Exception:
            if tracker.run_id:
                try: tracker.stop()
                except Exception: pass
            result = await async_func()
            return result, self._calculate_fallback(route, start_time)

    def _calculate_fallback(self, route: str, start_time: float) -> float:
        duration = time.time() - start_time
        return round(self.fallback_rates.get(route, 0.1) * duration, 4)
