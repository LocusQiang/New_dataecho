# LLM API 集成项目

一个统一的LLM API客户端，支持多个AI提供商（OpenAI、Claude等）。

## 功能特性

- ✅ 支持 OpenAI (GPT-3.5, GPT-4)
- ✅ 支持 Anthropic Claude
- ✅ 统一的API接口
- ✅ FastAPI Web服务
- ✅ 简单易用的Python客户端

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

复制 `.env.example` 为 `.env` 并填入你的API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-claude-key-here
```

### 3. 使用Python客户端

```python
from llm_client import LLMClient

client = LLMClient()

# 使用OpenAI
response = client.simple_chat("你好", provider="openai")
print(response)

# 使用Claude
response = client.simple_chat("你好", provider="claude")
print(response)
```

### 4. 启动Web服务

```bash
python app.py
```

或使用uvicorn：
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看API文档

## API使用示例

### 单轮对话

```bash
curl -X POST "http://localhost:8000/simple" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "你好，介绍一下你自己",
    "provider": "openai"
  }'
```

### 多轮对话

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "你好"}
    ],
    "provider": "openai"
  }'
```

## 项目结构

```
.
├── llm_client.py      # LLM客户端核心代码
├── app.py             # FastAPI Web服务
├── example_usage.py   # 使用示例
├── requirements.txt   # Python依赖
├── .env.example       # 环境变量示例
└── README.md          # 项目说明
```

## 获取API密钥

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/

## 许可证

MIT
