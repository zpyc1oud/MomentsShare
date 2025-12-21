# AI 服务升级指南 (SiliconFlow + LangChain)

## 1. 概述

本次更新对后端 `ai_service` 进行了重构，从硬编码的 SDK 调用迁移到了 **LangChain** 框架，并接入了 **SiliconFlow (硅基流动)** 聚合 API 平台。

主要改进点：
- **统一架构**: 使用 LangChain `ChatOpenAI` 客户端，兼容 OpenAI、DeepSeek、Zhipu 等多种模型协议。
- **动态模型**: 润色接口支持前端指定模型（如 `DeepSeek-V3`），满足不同场景对智能程度的需求。
- **成本优化**: 标签推荐等简单任务默认使用高性价比模型（如 `Qwen2.5-7B`）。

## 2. 配置说明 (.env)

请确保 `.env` 文件包含以下配置：

```ini
# AI Service Configuration
# -----------------------------------------------------------------------------
AI_PROVIDER=openai
# 硅基流动 API Key
AI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# 硅基流动 Base URL
AI_BASE_URL=https://api.siliconflow.cn/v1

# 默认模型 (用于标签推荐或未指定模型时的润色)
# 推荐: Qwen/Qwen2.5-7B-Instruct (速度快，免费/便宜)
AI_MODEL_NAME=Qwen/Qwen2.5-7B-Instruct

# 代理设置 (硅基流动国内直连，留空即可)
AI_PROXY_URL=
```

## 3. 接口使用指南

### 3.1 文案润色 (Polish)

*   **URL**: `/api/v1/ai/polish/`
*   **Method**: `POST`
*   **Auth**: Bearer Token

#### 场景 A: 使用默认模型 (快速/省钱)
适用于普通用户的日常润色。

```json
{
    "text": "今天天气真好，去公园玩了一圈。"
}
```

#### 场景 B: 指定强力模型 (高质量)
适用于会员或需要深度润色的场景。

```json
{
    "text": "今天天气真好，去公园玩了一圈。",
    "model": "deepseek-ai/DeepSeek-V3" 
}
```
*支持的模型取决于 SiliconFlow 账号权限，常用模型包括 `deepseek-ai/DeepSeek-V3`, `deepseek-ai/DeepSeek-R1`, `Qwen/Qwen2.5-72B-Instruct` 等。*

### 3.2 标签推荐 (Recommend Tags)

*   **URL**: `/api/v1/ai/recommend-tags/`
*   **Method**: `POST`
*   **Auth**: Bearer Token

始终使用后端配置的默认模型（`AI_MODEL_NAME`），确保响应速度。

```json
{
    "text": "新开的咖啡店味道很赞，拿铁拉花很漂亮。"
}
```

## 4. 开发维护

- **代码位置**: `backend/ai_service/services.py` (AIService 类)
- **依赖**: `langchain`, `langchain-openai`, `pydantic`
- **测试**: 可运行 `python verify_ai_service.py` 进行端到端测试。
