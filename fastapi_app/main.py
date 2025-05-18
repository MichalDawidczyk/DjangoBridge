from fastapi import FastAPI
from fastapi_app.routes import router

app = FastAPI(title="DjangoBridge API Gateway")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)