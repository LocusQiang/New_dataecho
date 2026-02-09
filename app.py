"""
FastAPI Web服务 - LLM API封装
提供HTTP接口来调用各种LLM API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from llm_client import LLMClient

app = FastAPI(title="LLM API服务", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化LLM客户端
llm_client = LLMClient()


class ChatMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    provider: str = "openai"  # "openai" 或 "claude"
    model: Optional[str] = None
    temperature: Optional[float] = 0.7


class SimpleChatRequest(BaseModel):
    prompt: str
    provider: str = "openai"
    model: Optional[str] = None
    temperature: Optional[float] = 0.7


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "LLM API服务",
        "endpoints": {
            "/chat": "POST - 多轮对话",
            "/simple": "POST - 单轮对话",
            "/health": "GET - 健康检查"
        }
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok"}


@app.post("/chat")
async def chat(request: ChatRequest):
    """多轮对话接口"""
    try:
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        kwargs = {}
        if request.model:
            kwargs["model"] = request.model
        if request.temperature:
            kwargs["temperature"] = request.temperature
        
        if request.provider.lower() == "openai":
            response = llm_client.chat_openai(messages, **kwargs)
        elif request.provider.lower() == "claude":
            response = llm_client.chat_claude(messages, **kwargs)
        else:
            raise HTTPException(status_code=400, detail=f"不支持的提供商: {request.provider}")
        
        if response is None:
            raise HTTPException(status_code=500, detail="API调用失败")
        
        return {"response": response, "provider": request.provider}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/simple")
async def simple_chat(request: SimpleChatRequest):
    """单轮对话接口（简化版）"""
    try:
        kwargs = {}
        if request.model:
            kwargs["model"] = request.model
        if request.temperature:
            kwargs["temperature"] = request.temperature
        
        response = llm_client.simple_chat(request.prompt, request.provider, **kwargs)
        
        if response is None:
            raise HTTPException(status_code=500, detail="API调用失败")
        
        return {"response": response, "provider": request.provider}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
