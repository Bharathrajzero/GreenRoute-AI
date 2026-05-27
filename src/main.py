import os
import sys
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, FileResponse

# Force correct python path inside Docker containers
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.cache.redis_vector import SemanticCache
from src.gateway.classifier import IntentClassifier
from src.gateway.router import LLMRouter
from src.telemetry.tracker import CarbonTracker

app = FastAPI(title="GreenRoute AI Gateway", version="1.0.0")

# Enable CORS so your frontend dashboard can safely run queries on port 8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

semantic_cache = None
intent_classifier = None
llm_router = None
carbon_tracker = None

# Global state tracker dictionary used to update the UI panels live
global_stats = {
    "total_requests": 0,
    "cache_hits": 0,
    "local_slm_routes": 0,
    "cloud_llm_routes": 0,
    "total_carbon_saved_g": 0.0
}

@app.on_event("startup")
def startup_event():
    global semantic_cache, intent_classifier, llm_router, carbon_tracker
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
    try:
        semantic_cache = SemanticCache(redis_url)
    except Exception as e:
        print(f"Redis initialization info: {e}")
    intent_classifier = IntentClassifier()
    llm_router = LLMRouter()
    carbon_tracker = CarbonTracker()

class QueryPayload(BaseModel):
    prompt: str

@app.post("/v1/chat/completions")
async def handle_completion(payload: QueryPayload):
    global global_stats
    start_time = time.time()
    prompt = payload.prompt
    global_stats["total_requests"] += 1

    # 1. Look up response inside Semantic Vector Database
    try:
        cached_response = semantic_cache.get(prompt)
    except Exception:
        cached_response = None

    if cached_response:
        global_stats["cache_hits"] += 1
        global_stats["total_carbon_saved_g"] += 0.389
        return {
            "status": "success",
            "route": "Cache-Hit",
            "complexity_tier": "CACHED",
            "response": cached_response,
            "carbon_emitted_g": 0.0,
            "latency_ms": round((time.time() - start_time) * 1000, 2)
        }

    # 2. Cache Miss: Assess Token Complexity Tier
    complexity = intent_classifier.evaluate(prompt)
    route_target = "Local-SLM" if complexity == "SIMPLE" else "Cloud-LLM"
    
    if route_target == "Local-SLM":
        global_stats["local_slm_routes"] += 1
    else:
        global_stats["cloud_llm_routes"] += 1

    # 3. Process Live Inference & Capture True Carbon footprint Telemetry
    async def run_inference():
        return await llm_router.dispatch(prompt, target=route_target)

    generated_text, carbon_g = await carbon_tracker.measure_async_inference(
        run_inference, route_target
    )
    
    if route_target == "Local-SLM":
        savings = max(0.0, 0.389 - carbon_g)
        global_stats["total_carbon_saved_g"] += savings

    # 4. Asynchronously save background results back into HNSW database cache
    try:
        semantic_cache.set(prompt, generated_text)
    except Exception:
        pass

    return {
        "status": "success",
        "route": route_target,
        "complexity_tier": complexity,
        "response": generated_text,
        "carbon_emitted_g": carbon_g,
        "latency_ms": round((time.time() - start_time) * 1000, 2)
    }

@app.get("/api/stats")
def get_dashboard_stats():
    return global_stats

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
async def serve_dashboard():
    # Looks inside the container workspace path for your HTML application
    dashboard_path = Path(__file__).parent / "static" / "index.html"
    if dashboard_path.exists():
        return FileResponse(dashboard_path)
    
    # Custom fallback interface that shows if file placement maps drift on Windows paths
    return HTMLResponse(content="""
    <html>
        <body style="background:#0f172a; color:#f8fafc; font-family:sans-serif; text-align:center; padding-top:100px;">
            <h1 style="color:#34d399;">🌱 GreenRoute AI Proxy is Online!</h1>
            <p style="color:#94a3b8;">The backend system logic is fully alive, but <code>src/static/index.html</code> was not detected inside this volume path.</p>
            <p>View the operational JSON streams at <a style="color:#38bdf8;" href="/api/stats">/api/stats</a> or test commands via <a style="color:#38bdf8;" href="/docs">Swagger Core UI (/docs)</a></p>
        </body>
    </html>
    """)