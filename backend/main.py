from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from config import API_HOST, API_PORT
from app_context import AppContext
from feedback_store import save_feedback
from session_engine import start_autonomous_session_thread

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ctx = AppContext()
start_autonomous_session_thread(ctx)


class ChatRequest(BaseModel):
    message: str
    user_id: str


class FeedbackRequest(BaseModel):
    feedback_type: str
    feedback_text: str = ""


@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    ctx.state.set_instruction(req.message)
    print(f"★演奏方針が変更されました: {ctx.state.get_instruction()}")
    return {
        "response": f"了解しました。『{ctx.state.get_instruction()}』という方針でセッションを続けます。"
    }


@app.get("/status")
async def status_endpoint():
    return ctx.state.get_status()


@app.post("/feedback")
async def feedback_endpoint(req: FeedbackRequest):
    status = ctx.state.get_status()

    success = save_feedback(
        db_conn=ctx.db_conn,
        instruction=status["current_instruction"],
        interpretation=status["last_interpretation"],
        feedback_type=req.feedback_type,
        feedback_text=req.feedback_text,
        recent_midi_count=status["recent_midi_count"],
    )

    if success:
        return {"message": "フィードバックを保存しました。"}
    return {"message": "フィードバック保存に失敗しました。"}


@app.post("/session/new")
async def new_session_endpoint():
    new_id = ctx.state.new_session()
    return {"message": "新しいセッションを開始しました。", "session_id": new_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=API_HOST, port=API_PORT)