import logging
import os
from typing import Dict, List, Optional

from django.conf import settings
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


class AIOutputSchema(BaseModel):
    polished_content: str = Field(description="润色后的文本内容，更加生动有趣，适合社交媒体发布")
    suggested_tags: List[str] = Field(description="基于内容推荐的3-5个标签，每个标签不超过10个字符")


class AIService:
    """
    Service for AI interactions using LangChain.
    Supports text polishing and tag recommendation in a single pass.
    """

    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.base_url = settings.AI_BASE_URL or None
        self.model_name = settings.AI_MODEL_NAME
        self.proxy_url = settings.AI_PROXY_URL
        self.provider = settings.AI_PROVIDER

        if not self.api_key:
            logger.warning("AI_API_KEY is not set. AI features may fail.")

        # Configure Proxy if needed
        self.openai_proxy = None
        if self.proxy_url:
            self.openai_proxy = self.proxy_url
            # Also set env vars just in case some underlying libs need it
            # os.environ["HTTP_PROXY"] = self.proxy_url
            # os.environ["HTTPS_PROXY"] = self.proxy_url

    def get_llm(self, model_name: str = None) -> Optional[ChatOpenAI]:
        """Initialize and return the LLM client."""
        if not self.api_key:
            return None
        
        # Use provided model_name if available, otherwise fallback to settings
        target_model = model_name or self.model_name

        try:
            # Common arguments for ChatOpenAI
            # Note: For ZhipuAI, use base_url="https://open.bigmodel.cn/api/paas/v4/"
            # and model_name="glm-4" (or similar).
            llm = ChatOpenAI(
                openai_api_key=self.api_key,
                openai_api_base=self.base_url,
                model_name=target_model,
                openai_proxy=self.openai_proxy,
                temperature=0.7,
            )
            return llm
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            return None

    def process_content(self, text: str, model_name: str = None) -> Dict:
        """
        Process user text to generate polished content and tags.
        Returns a dict with 'polished_content' and 'suggested_tags'.
        """
        llm = self.get_llm(model_name=model_name)
        if not llm:
            return self._fallback_response(text)

        try:
            # Define the output parser
            parser = JsonOutputParser(pydantic_object=AIOutputSchema)

            # Define the prompt template
            prompt = PromptTemplate(
                template="你是一个专业的社交媒体运营助手。\n"
                         "请阅读以下用户提供的原始内容，完成两个任务：\n"
                         "1. 润色文案：使其更加生动、有趣、吸引人，适合发朋友圈或社交媒体。\n"
                         "2. 推荐标签：根据内容推荐3-5个相关标签，不要带#号，每个标签简短有力。\n\n"
                         "原始内容：\n{text}\n\n"
                         "请严格按照以下JSON格式输出，不要包含Markdown代码块标记：\n"
                         "{format_instructions}\n",
                input_variables=["text"],
                partial_variables={"format_instructions": parser.get_format_instructions()},
            )

            # Create chain
            chain = prompt | llm | parser

            # Invoke chain
            result = chain.invoke({"text": text})
            return result

        except Exception as e:
            logger.error(f"AI processing failed: {e}")
            return self._fallback_response(text)

    def _fallback_response(self, text: str) -> Dict:
        """Return a safe fallback response when AI fails."""
        return {
            "polished_content": text,  # Return original text as fallback
            "suggested_tags": ["日常", "分享"],
        }
