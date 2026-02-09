"""
使用示例
演示如何使用LLM客户端
"""
from llm_client import LLMClient

def example_openai():
    """OpenAI使用示例"""
    print("=" * 50)
    print("OpenAI示例")
    print("=" * 50)
    
    client = LLMClient()
    
    # 简单对话
    response = client.simple_chat(
        "用一句话解释什么是人工智能",
        provider="openai",
        model="gpt-3.5-turbo"
    )
    print(f"回答: {response}\n")
    
    # 多轮对话
    messages = [
        {"role": "system", "content": "你是一个专业的Python编程助手"},
        {"role": "user", "content": "如何创建一个列表？"}
    ]
    response = client.chat_openai(messages, model="gpt-3.5-turbo")
    print(f"多轮对话回答: {response}\n")


def example_claude():
    """Claude使用示例"""
    print("=" * 50)
    print("Claude示例")
    print("=" * 50)
    
    client = LLMClient()
    
    # 简单对话
    response = client.simple_chat(
        "用一句话解释什么是人工智能",
        provider="claude",
        model="claude-3-sonnet-20240229"
    )
    print(f"回答: {response}\n")
    
    # 多轮对话
    messages = [
        {"role": "system", "content": "你是一个专业的Python编程助手"},
        {"role": "user", "content": "如何创建一个列表？"}
    ]
    response = client.chat_claude(messages, model="claude-3-sonnet-20240229")
    print(f"多轮对话回答: {response}\n")


if __name__ == "__main__":
    print("LLM API使用示例\n")
    
    # 运行示例（需要先配置API密钥）
    try:
        example_openai()
    except Exception as e:
        print(f"OpenAI示例失败: {e}\n")
    
    try:
        example_claude()
    except Exception as e:
        print(f"Claude示例失败: {e}\n")
