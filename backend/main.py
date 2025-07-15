from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import httpx

app = FastAPI(
    title="Generative Music API",
    description="Backend service for Qloo-powered music taste profiles and AI music generation",
    version="0.1.0"
)

# Load configuration from environment
QLOO_API_KEY = os.getenv("QLOO_API_KEY")
QLOO_BASE_URL = os.getenv("QLOO_BASE_URL", "https://api.qloo.com/0")

# ----- Request & Response Models -----
class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    results: list

class RecRequest(BaseModel):
    sample_ids: list[int]
    target: str = "music"

class RecResponse(BaseModel):
    results: list

# ----- Qloo Endpoints -----
@app.post("/api/qloo/search", response_model=SearchResponse)
async def qloo_search(req: SearchRequest):
    """
    Proxy endpoint: search Qloo for entities by keyword.
    """
    if not QLOO_API_KEY:
        raise HTTPException(status_code=500, detail="QLOO_API_KEY not configured")

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{QLOO_BASE_URL}/search",
            params={"q": req.query},
            headers={"Authorization": f"Bearer {QLOO_API_KEY}", "Content-Type": "application/json"}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Qloo search failed")
        payload = resp.json()

    return {"results": payload.get("results", payload)}

@app.post("/api/qloo/recs", response_model=RecResponse)
async def qloo_recs(req: RecRequest):
    """
    Proxy endpoint: fetch Qloo recommendations given sample IDs.
    """
    if not QLOO_API_KEY:
        raise HTTPException(status_code=500, detail="QLOO_API_KEY not configured")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{QLOO_BASE_URL}/recs",
            json={"sample": req.sample_ids, "target": req.target},
            headers={"Authorization": f"Bearer {QLOO_API_KEY}", "Content-Type": "application/json"}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Qloo recommendations failed")
        payload = resp.json()

    return {"results": payload.get("results", payload)}

# ----- Placeholder Endpoints for Future Expansion -----
@app.post("/api/music/generate")
async def generate_music():
    """
    Stub: dispatch job to AI music service (e.g., Udio/Suno).
    """
    return {"status": "Not implemented"}

@app.post("/api/feedback")
async def submit_feedback():
    """
    Stub: record user feedback (rating, comments).
    """
    return {"status": "Not implemented"}

@app.post("/api/reward")
async def compute_reward():
    """
    Stub: compute reward and update RL policy.
    """
    return {"status": "Not implemented"}

# ----- Run Server -----
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
