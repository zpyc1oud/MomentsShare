// frontend/src/components/MomentCard/MomentList.js

import React from 'react';
import MomentCard from './MomentCard'; // 引入卡片组件

/**
 * 动态列表组件，渲染搜索结果
 * @param {Array<Object>} data - Moment 对象的数组
 */
function MomentList({ data }) {
    if (!data || data.length === 0) {
        return null; // 列表为空时不渲染
    }

    return (
        <div style={listStyles.container}>
            {data.map(moment => (
                // 假设后端返回的每个对象都有一个唯一的 id
                <MomentCard key={moment.id} moment={moment} />
            ))}
        </div>
    );
}

const listStyles = {
    container: {
        padding: '0 20px',
    }
};

export default MomentList;