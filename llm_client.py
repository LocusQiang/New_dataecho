"""
LLM API客户端封装
支持多个LLM提供商：OpenAI、Anthropic等
"""
import os
from typing import Optional, Dict, List
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """统一的LLM客户端接口"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    def chat_openai(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7
    ) -> Optional[str]:
        """使用OpenAI API进行对话"""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY未设置，请在.env文件中配置")
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API错误: {e}")
            return None
    
    def chat_claude(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-3-sonnet-20240229",
        max_tokens: int = 1024
    ) -> Optional[str]:
        """使用Anthropic Claude API进行对话"""
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY未设置，请在.env文件中配置")
        
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=self.anthropic_api_key)
            
            # Claude API需要特殊格式
            system_message = None
            conversation_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    conversation_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_message if system_message else "You are a helpful assistant.",
                messages=conversation_messages
            )
            
            return response.content[0].text
        except Exception as e:
            print(f"Claude API错误: {e}")
            return None
    
    def simple_chat(self, prompt: str, provider: str = "openai", **kwargs) -> Optional[str]:
        """简单的单轮对话接口"""
        messages = [{"role": "user", "content": prompt}]
        
        if provider.lower() == "openai":
            return self.chat_openai(messages, **kwargs)
        elif provider.lower() == "claude":
            return self.chat_claude(messages, **kwargs)
        else:
            raise ValueError(f"不支持的提供商: {provider}")


# 使用示例
if __name__ == "__main__":
    client = LLMClient()
    
    # 示例1: 使用OpenAI
    print("=== 使用OpenAI ===")
    response = client.simple_chat("你好，请介绍一下你自己", provider="openai")
    print(response)
    
    print("\n=== 使用Claude ===")
    # 示例2: 使用Claude
    response = client.simple_chat("你好，请介绍一下你自己", provider="claude")
    print(response)
