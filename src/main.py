import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.graphql.schema import graphql_app
from app.core.db import init_db

app = FastAPI()

init_db(app=app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)
app.include_router(graphql_app, prefix="/graphql")


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, ws="websockets")
