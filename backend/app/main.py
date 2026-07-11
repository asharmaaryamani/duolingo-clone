from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .seed import seed
from .routers import user, path, lesson, leaderboard, session

Base.metadata.create_all(bind=engine)
seed()

app = FastAPI(title="Duolingo Clone API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://duolingo-clone-jet.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(path.router)
app.include_router(lesson.router)
app.include_router(leaderboard.router)
app.include_router(session.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
