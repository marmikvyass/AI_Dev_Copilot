from fastapi import FastAPI
from routes.api_router import api_router

app = FastAPI(
    title = 'AI_DEV_COPILOT',
    description = 'AI-powered developer assistant for understanding and working with codebases.',
    version = '1.0'
)

app.include_router(
    api_router,
    prefix='/api'
)
@app.get('/')
async def root():
    return {
        'message' : 'AI_DEV_COPILOR is Running Successfully',
        'status' : 'Running'
    }

