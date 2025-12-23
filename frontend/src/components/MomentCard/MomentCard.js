// frontend/src/components/MomentCard/MomentCard.js

import React from 'react';

// 动态卡片组件（P2 样式复用）
// 假设 moment 对象结构包含了后端 MomentListSerializer 返回的字段
function MomentCard({ moment }) {
    // 假设卡片包含：用户头像、昵称、内容、图片/视频缩略图、发布时间、标签
    
    // 渲染标签
    const renderTags = () => {
        if (moment.tags && moment.tags.length > 0) {
            return (
                <div style={cardStyles.tagsContainer}>
                    {moment.tags.map(tag => (
                        <span key={tag.id} style={cardStyles.tag}>#{tag.name}</span>
                    ))}
                </div>
            );
        }
        return null;
    };

    return (
        <div style={cardStyles.card}>
            {/* 头部：用户信息 */}
            <div style={cardStyles.header}>
                <img src={moment.user.avatar || '/media/default_avatar.png'} alt="Avatar" style={cardStyles.avatar} />
                <span style={cardStyles.username}>{moment.user.username}</span>
                <span style={cardStyles.date}>{moment.created_at.split('T')[0]}</span>
            </div>

            {/* 内容 */}
            <p style={cardStyles.content}>{moment.content.substring(0, 100)}...</p>

            {/* 媒体：显示类型提示 */}
            <div style={cardStyles.mediaPlaceholder}>
                <span style={cardStyles.mediaText}>
                    {moment.type === 'VIDEO' ? '🎥 视频缩略图' : '🖼️ 图片集'}
                </span>
            </div>
            
            {/* 标签 */}
            {renderTags()}

        </div>
    );
}

const cardStyles = {
    card: {
        border: '1px solid #ddd',
        borderRadius: '8px',
        padding: '15px',
        margin: '15px 0',
        backgroundColor: '#fff',
    },
    header: {
        display: 'flex',
        alignItems: 'center',
        marginBottom: '10px',
    },
    avatar: {
        width: '30px',
        height: '30px',
        borderRadius: '50%',
        marginRight: '10px',
    },
    username: {
        fontWeight: 'bold',
        marginRight: 'auto',
    },
    date: {
        fontSize: '12px',
        color: '#888',
    },
    content: {
        fontSize: '14px',
        marginBottom: '10px',
    },
    mediaPlaceholder: {
        height: '100px',
        backgroundColor: '#f5f5f5',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: '4px',
        marginBottom: '10px',
    },
    mediaText: {
        color: '#aaa',
        fontSize: '14px',
    },
    tagsContainer: {
        marginTop: '10px',
    },
    tag: {
        fontSize: '12px',
        color: '#007bff',
        backgroundColor: '#e9f5ff',
        padding: '3px 8px',
        borderRadius: '12px',
        marginRight: '5px',
    }
};

export default MomentCard;