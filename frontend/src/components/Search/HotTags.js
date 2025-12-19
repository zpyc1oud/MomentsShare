// frontend/src/components/Search/HotTags.js

import React from 'react';

// 假设这些热门标签数据是从某个API获取或配置的
const popularTags = [
    '旅游',
    '美食探店',
    '日常分享',
    '运动健身',
    '科技前沿',
    '宠物日常'
];

// 热门标签组件，负责点击事件
function HotTags({ onLabelClick }) {
    
    const handleTagClick = (tag) => {
        if (onLabelClick) {
            // 将点击的标签名传递给父组件
            onLabelClick(tag);
        }
    };

    return (
        <div style={styles.container}>
            <h4>热门标签/推荐</h4>
            <div style={styles.tagsArea}>
                {popularTags.map(tag => (
                    <span 
                        key={tag}
                        onClick={() => handleTagClick(tag)}
                        style={styles.tag}
                    >
                        #{tag}
                    </span>
                ))}
            </div>
        </div>
    );
}

const styles = {
    container: {
        padding: '10px 20px',
    },
    tagsArea: {
        display: 'flex',
        flexWrap: 'wrap',
        gap: '10px',
        marginTop: '10px',
    },
    tag: {
        padding: '5px 10px',
        backgroundColor: '#eee',
        borderRadius: '15px',
        cursor: 'pointer',
        fontSize: '14px',
    }
};

export default HotTags;