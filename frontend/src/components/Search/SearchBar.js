// frontend/src/components/Search/SearchBar.js

import React, { useState } from 'react';

// 顶部搜索栏组件 (对应需求: 顶部悬浮搜索框)
function SearchBar({ onSearch }) {
    const [keyword, setKeyword] = useState('');

    const handleSubmit = (e) => {
        // 阻止表单默认提交，防止页面刷新
        e.preventDefault(); 
        const trimmedKeyword = keyword.trim();
        
        if (onSearch) {
            // 将关键词传递给父组件处理，对应后端的 keyword 参数
            onSearch(trimmedKeyword);
        }
    };

    return (
        <form onSubmit={handleSubmit} style={styles.container}> 
            <input
                type="text"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                placeholder="请输入搜索关键词..."
                style={styles.input}
            />
            <button type="submit" style={styles.button}>
                搜索
            </button>
        </form>
    );
}

const styles = {
    // 模拟 "顶部悬浮" 样式
    container: {
        position: 'sticky', 
        top: 0,
        zIndex: 10,
        padding: '10px 20px',
        backgroundColor: '#fff',
        borderBottom: '1px solid #eee',
        display: 'flex',
    },
    input: {
        flexGrow: 1,
        padding: '8px',
        marginRight: '10px',
        border: '1px solid #ccc',
        borderRadius: '4px',
    },
    button: {
        padding: '8px 15px',
        border: 'none',
        backgroundColor: '#007bff',
        color: 'white',
        cursor: 'pointer',
        borderRadius: '4px',
    }
};

export default SearchBar;