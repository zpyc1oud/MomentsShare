// frontend/src/pages/DiscoveryPage/DiscoveryPage.js

import React, { useState } from 'react';
import SearchBar from '../../components/Search/SearchBar'; 
import HotTags from '../../components/Search/HotTags'; 
import DateRangeFilter from '../../components/Search/DateRangeFilter'; 
import ContentTypeFilter from '../../components/Search/ContentTypeFilter'; 
import MomentList from '../../components/MomentCard/MomentList'; // <-- 新增引入
import { searchMoments } from '../../api/searchApi'; 

function DiscoveryPage() {
    // 状态 1: 存储搜索参数，对应后端的四个参数
    const [searchParams, setSearchParams] = useState({
        keyword: '',   
        label: '',     
        startDate: '', // YYYY-MM-DD
        endDate: '',   // YYYY-MM-DD
    });

    // 状态 2: 存储搜索结果和加载状态
    const [results, setResults] = useState([]); // 原始 API 返回数据
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    
    // 状态 3: 存储前端筛选状态（内容类型）
    const [contentTypeFilter, setContentTypeFilter] = useState('all'); 

    // 核心函数：执行 API 调用
    const fetchResults = async (params) => {
        // 当所有参数都为空时，不触发搜索，清空结果
        if (!params.keyword && !params.label && !params.startDate && !params.endDate) {
            setResults([]);
            return; 
        }

        setIsLoading(true);
        setError(null);
        
        try {
            const data = await searchMoments(params);
            setResults(data); 

        } catch (err) {
            console.error("搜索失败:", err.message);
            setError(err.message);
            setResults([]);
        } finally {
            setIsLoading(false);
        }
    };

    // 处理器 1: 关键词搜索 (由 SearchBar 触发)
    const handleKeywordSearch = (keyword) => {
        const newParams = {
            ...searchParams,
            keyword: keyword, 
            label: '', 
        };
        setSearchParams(newParams);
        fetchResults(newParams); 
    };

    // 处理器 2: 标签点击 (由 HotTags 触发)
    const handleLabelClick = (label) => {
        const newParams = {
            ...searchParams,
            label: label,      
            keyword: '',      
        };
        setSearchParams(newParams);
        fetchResults(newParams); 
    };
    
    // 处理器 3: 日期范围变化 (由 DateRangeFilter 触发)
    const handleDateRangeChange = (startDate, endDate) => {
        const newParams = {
             ...searchParams,
             startDate: startDate, 
             endDate: endDate,     
        };
        setSearchParams(newParams);
        fetchResults(newParams); 
    };

    // 处理器 4: 内容类型变化 (由 ContentTypeFilter 触发)
    const handleContentTypeChange = (type) => {
        // 仅更新前端筛选类型
        setContentTypeFilter(type); 
    };

    // 前端过滤逻辑：根据 ContentTypeFilter 的选择进行过滤
    const filteredResults = results.filter(moment => {
        if (contentTypeFilter === 'all') {
            return true;
        }
        // 假设 moment 对象包含 type 字段 (IMAGE/VIDEO)
        return moment.type === contentTypeFilter;
    });


    // --- 渲染部分 ---
    
    const isInitialState = !searchParams.keyword && !searchParams.label && !searchParams.startDate && !searchParams.endDate && !isLoading;
    const isSearchActive = searchParams.keyword || searchParams.label || searchParams.startDate || searchParams.endDate;

    return (
        <div className="discovery-page" style={styles.pageContainer}>
            <h1>P4: 发现与搜索页</h1>
            
            {/* 1. 顶部搜索栏 */}
            <SearchBar onSearch={handleKeywordSearch} />
            
            {/* 3. 热门标签/推荐 */}
            <HotTags onLabelClick={handleLabelClick} /> 
            
            {/* 2. 筛选面板 */}
            <div style={styles.filterArea}>
                 {/* 时间范围选择器 */}
                 <DateRangeFilter 
                    onChange={handleDateRangeChange}
                    initialStartDate={searchParams.startDate}
                    initialEndDate={searchParams.endDate}
                 /> 
                 
                 {/* 内容类型筛选 */}
                 <ContentTypeFilter 
                    selectedType={contentTypeFilter} 
                    onChange={handleContentTypeChange} 
                 /> 
            </div>
            
            <hr style={styles.divider} />

            {/* 4. 搜索结果展示 */}
            <h3 style={styles.resultsHeader}>
                搜索结果 
                {isLoading && <span> (加载中...)</span>}
                {!isLoading && isSearchActive && <span> 
                    ({filteredResults.length} 条) 
                    {filteredResults.length !== results.length && 
                        <span style={{color: '#888', marginLeft: '5px'}}> (总 {results.length} 条，已过滤)</span>
                    }
                </span>}
            </h3>
            
            {error && <p style={styles.errorMessage}>搜索出错: {error}</p>}
            
            {/* 列表渲染 */}
            {!isLoading && !error && filteredResults.length > 0 && (
                <MomentList data={filteredResults} />
            )}
            
            {/* 结果为空或初始状态的提示 */}
            {!isLoading && !error && filteredResults.length === 0 && (
                <p style={styles.noResults}>
                    {isInitialState 
                        ? "请输入关键词或点击标签开始搜索。" 
                        : (results.length > 0 ? "当前内容类型下没有结果。" : "未找到符合条件的动态。")
                    }
                </p>
            )}
            
        </div>
    );
}

const styles = {
    pageContainer: { padding: '0 0 20px 0', fontFamily: 'Arial, sans-serif' },
    filterArea: { margin: '10px 20px', padding: '15px 0', borderTop: '1px solid #eee' },
    divider: { margin: '20px 20px', border: 'none', borderTop: '1px solid #ddd' },
    resultsHeader: { marginTop: '10px', padding: '0 20px', fontSize: '18px' },
    noResults: { color: '#888', padding: '0 20px', textAlign: 'center' },
    errorMessage: { color: 'red', padding: '0 20px' }
};


export default DiscoveryPage;