"""LLM API client for Gemini, OpenRouter, Claude, OpenAI."""
import os
from typing import Optional

class LLMClient:
    """Unified client for multiple LLM providers."""
    
    def __init__(self, api_key: str, provider: str):
        """Initialize LLM client."""
        self.api_key = api_key
        self.provider = provider.lower()
        self.validate_key()
    
    def validate_key(self) -> bool:
        """Validate API key format."""
        if not self.api_key or len(self.api_key) < 10:
            raise ValueError("Invalid API key")
        return True
    
    def call(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Call LLM with prompt."""
        if self.provider == "gemini":
            return self._call_gemini(prompt, temperature, max_tokens)
        elif self.provider == "openrouter":
            return self._call_openrouter(prompt, temperature, max_tokens)
        elif self.provider == "claude":
            return self._call_claude(prompt, temperature, max_tokens)
        elif self.provider == "openai":
            return self._call_openai(prompt, temperature, max_tokens)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def _call_gemini(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Call Gemini API."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error calling Gemini: {str(e)}"
    
    def _call_openrouter(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Call OpenRouter API."""
        try:
            import requests
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            data = {
                "model": "anthropic/claude-3-sonnet",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Error calling OpenRouter: {str(e)}"
    
    def _call_claude(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Call Claude API."""
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error calling Claude: {str(e)}"
    
    def _call_openai(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Call OpenAI API."""
        try:
            import openai
            openai.api_key = self.api_key
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Error calling OpenAI: {str(e)}"
