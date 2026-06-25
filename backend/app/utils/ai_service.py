"""AI Service for OpenAI integration."""

import openai
from typing import List, Dict, Optional, AsyncGenerator
from app.config import settings

openai.api_key = settings.openai_api_key

class AIService:
    """AI Service using OpenAI API."""
    
    def __init__(self):
        self.model = settings.openai_model
        self.temperature = settings.ai_temperature
        self.max_tokens = settings.ai_max_tokens
        self.top_p = settings.ai_top_p
    
    async def get_response(self, messages: List[Dict[str, str]]) -> Dict:
        """Get response from OpenAI."""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
            )
            return {
                "content": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
            }
        except Exception as e:
            print(f"Error getting AI response: {e}")
            raise
    
    async def get_streaming_response(
        self, messages: List[Dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        """Get streaming response from OpenAI."""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                stream=True,
            )
            async for chunk in response:
                delta = chunk.choices[0].delta
                if hasattr(delta, "content") and delta.content:
                    yield delta.content
        except Exception as e:
            print(f"Error getting streaming response: {e}")
            raise
    
    def create_system_prompt(self, context: Optional[str] = None) -> Dict[str, str]:
        """Create system prompt."""
        system_content = (
            "You are My Personal AI, a helpful assistant designed to help users "
            "with various tasks including answering questions, coding assistance, "
            "content generation, summarization, and translation. Be concise, accurate, "
            "and helpful in your responses."
        )
        if context:
            system_content += f"\n\nContext: {context}"
        return {"role": "system", "content": system_content}

ai_service = AIService()
