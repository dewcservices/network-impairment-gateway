import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import (
    bearer_controller,
    environment_controller,
    settings_controller,
)

app = FastAPI()

app.include_router(environment_controller.router)
app.include_router(bearer_controller.router)
app.include_router(settings_controller.router)

origins = ["http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
