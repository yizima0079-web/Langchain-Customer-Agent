"""AI 智能客服路由（RAG 增强检索，游客可访问）。"""
import json
import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.models.knowledge import ChatMessage
from app.schemas.chat import ChatMessageOut, ChatRequest, ChatResponse
from app.schemas.common import Response
from app.services import rag

router = APIRouter(prefix="/chat", tags=["AI客服"])


def _event(event_type: str, **payload) -> str:
    return f"data: {json.dumps({'type': event_type, **payload}, ensure_ascii=False)}\n\n"


@router.post("", response_model=Response[ChatResponse], summary="AI 客服对话")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    """处理一次 AI 客服对话。

    流程：保存用户消息 → RAG 检索 + LLM 生成 → 保存回复并返回。
    游客可访问，通过 session_id 区分会话。
    """
    # 首次对话自动生成会话ID
    session_id = req.session_id or uuid.uuid4().hex

    # 保存用户消息
    db.add(ChatMessage(session_id=session_id, role="user", content=req.message))
    db.commit()

    # RAG 问答（异常时降级为友好提示，不中断接口）
    try:
        answer, sources = rag.ask(req.message)
    except Exception as exc:  # noqa: BLE001
        answer = f"抱歉，AI 客服暂时不可用，请稍后再试。（{str(exc)[:200]}）"
        sources = []

    # 保存助手回复
    db.add(ChatMessage(session_id=session_id, role="assistant", content=answer))
    db.commit()

    return Response(data=ChatResponse(session_id=session_id, answer=answer, sources=sources))


@router.post("/stream", summary="流式 AI 客服对话")
def chat_stream(req: ChatRequest, db: Session = Depends(get_db)):
    """以 SSE 分片返回回答，只给前端回答文本，不下发匹配文本。"""
    session_id = req.session_id or uuid.uuid4().hex
    db.add(ChatMessage(session_id=session_id, role="user", content=req.message))
    db.commit()

    def generate():
        answer_parts = []
        yield _event("meta", session_id=session_id)
        try:
            for chunk in rag.stream(req.message):
                if not chunk:
                    continue
                answer_parts.append(chunk)
                yield _event("delta", content=chunk)
            answer = "".join(answer_parts)
            db.add(ChatMessage(session_id=session_id, role="assistant", content=answer))
            db.commit()
            yield _event("done")
        except Exception:
            db.rollback()
            answer = "抱歉，AI 客服暂时不可用，请稍后再试。"
            db.add(ChatMessage(session_id=session_id, role="assistant", content=answer))
            db.commit()
            yield _event("error", message=answer)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/history", summary="历史会话记录")
def history(session_id: str, db: Session = Depends(get_db)):
    """按会话ID返回聊天历史（按时间正序）。"""
    items = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.id.asc())
        .all()
    )
    return Response(data=[ChatMessageOut.model_validate(m) for m in items])
