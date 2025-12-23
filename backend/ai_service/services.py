import logging
import os
from typing import Dict, List, Optional

from django.conf import settings
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
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
        logger.info(f"AIService initialized with default model: {self.model_name}")
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

    def get_llm(self, model_name: str = None, image_data: str = None) -> Optional[ChatOpenAI]:
        """Initialize and return the LLM client."""
        if not self.api_key:
            return None
        
        # Use provided model_name if available, otherwise fallback to settings
        target_model = model_name or self.model_name
        
        # Auto-switch to Vision model if image is present but current model is not VLM
        # Note: This is a simple heuristic. Ideally, caller should pass correct model.
        # But for user convenience, we override here if needed.
        if "image_data" in locals() and image_data and "VL" not in target_model and "4.6V" not in target_model:
             # Default fallback vision model - use Qwen/Qwen3-VL-8B-Instruct
             target_model = "Qwen/Qwen3-VL-8B-Instruct"
             logger.info(f"Auto-switching to vision model: {target_model}")

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

    def process_content(self, text: str, image_data: str = None, model_name: str = None) -> Dict:
        """
        Process user text (and optional image) to generate polished content and tags.
        Returns a dict with 'polished_content' and 'suggested_tags'.
        """
        llm = self.get_llm(model_name=model_name, image_data=image_data)
        
        # Log effective model name
        effective_model = model_name or self.model_name
        logger.info(f"Processing content with model: {effective_model}, has_image: {bool(image_data)}")
        
        if not llm:
            logger.error("LLM initialization failed")
            return self._fallback_response(text)

        try:
            # Define the output parser
            parser = JsonOutputParser(pydantic_object=AIOutputSchema)
            format_instructions = parser.get_format_instructions()

            # Construct System Prompt
            system_prompt = (
                "你是一个专业的社交媒体运营助手。\n"
                "请阅读以下用户提供的原始内容（可能包含图片和文字），完成两个任务：\n"
                "1. 润色文案：根据图片内容（如果有）和文字草稿，使其更加生动、有趣、吸引人，适合发朋友圈或社交媒体。\n"
                "2. 推荐标签：根据内容（图片和文字）推荐3-5个相关标签，不要带#号，每个标签简短有力。\n\n"
                "请严格按照以下JSON格式输出，不要包含Markdown代码块标记：\n"
                f"{format_instructions}\n"
            )

            # Construct User Content (Multimodal)
            user_content = []
            if text:
                user_content.append({"type": "text", "text": f"原始内容：\n{text}"})
            
            if image_data:
                # Compatible with OpenAI Vision format (works for SiliconFlow/GLM-4V etc)
                user_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}"
                    }
                })

            if not user_content:
                # Should not happen due to serializer validation, but safe check
                return self._fallback_response(text)

            # Build Messages
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_content)
            ]

            # Invoke LLM
            logger.info(f"Sending request to LLM: model={model_name or self.model_name}, has_image={bool(image_data)}")
            response = llm.invoke(messages)
            logger.info(f"LLM Response: {response.content}")
            
            # Parse result
            content = response.content
            # Cleanup potential markdown formatting if model wraps JSON in ```json ... ```
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[0].strip()
            
            # Special handling for GLM-4/SiliconFlow output artifacts
            if "<|begin_of_box|>" in content:
                content = content.replace("<|begin_of_box|>", "").replace("<|end_of_box|>", "").strip()
            
            # Remove any leading/trailing characters that are not part of JSON object
            content = content.strip()
            if not content.startswith("{") and "{" in content:
                content = content[content.find("{"):]
            if not content.endswith("}") and "}" in content:
                content = content[:content.rfind("}")+1]

            return parser.parse(content)

        except Exception as e:
            logger.error(f"AI processing failed: {e}")
            return self._fallback_response(text)

    def _fallback_response(self, text: str) -> Dict:
        """Return a safe fallback response when AI fails."""
        return {
            "polished_content": text,  # Return original text as fallback
            "suggested_tags": ["日常", "分享"],
        }
