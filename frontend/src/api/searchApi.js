// frontend/src/api/searchApi.js

// 假设基础 URL 是您的后端服务地址，通常在开发环境中通过 Vite/Webpack 代理配置来处理
const API_BASE_URL = ''; 

/**
 * 执行多维度动态内容搜索
 * @param {object} params - 包含 keyword, label, startDate, endDate 的对象
 * @returns {Promise<Array>} 搜索结果列表
 */
export async function searchMoments(params) {
    const queryParams = new URLSearchParams();
    
    // 构造请求参数，匹配后端接口要求
    if (params.keyword) queryParams.append('keyword', params.keyword);
    if (params.label) queryParams.append('label', params.label);
    if (params.startDate) queryParams.append('start_date', params.startDate);
    if (params.endDate) queryParams.append('end_date', params.endDate);
    
    // 接口地址: /moments/search/
    const url = `${API_BASE_URL}/moments/search/?${queryParams.toString()}`;
    
    try {
        const response = await fetch(url);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || '搜索失败，服务器响应错误。');
        }

        return await response.json();
    } catch (error) {
        console.error("API Call Failed:", error);
        throw error;
    }
}