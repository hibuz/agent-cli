from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Agent-Based Commerce Platform API",
    description="API for managing shopping agents and orchestration workflows",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Agent-Based Commerce Platform API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "agent-commerce-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)