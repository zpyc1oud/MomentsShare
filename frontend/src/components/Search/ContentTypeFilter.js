// frontend/src/components/Search/ContentTypeFilter.js

import React from 'react';

const contentTypes = [
    { value: 'all', label: '全部' },
    { value: 'IMAGE', label: '图文' },
    { value: 'VIDEO', label: '视频' },
];

// 内容类型筛选组件 (对应需求: 筛选面板 - 内容类型)
function ContentTypeFilter({ selectedType, onChange }) {
    
    const handleChange = (e) => {
        onChange(e.target.value);
    };

    return (
        <div style={styles.container}>
            <span style={styles.label}>内容类型:</span>
            {contentTypes.map((type) => (
                <label key={type.value} style={styles.radioLabel}>
                    <input
                        type="radio"
                        name="contentType"
                        value={type.value}
                        checked={selectedType === type.value}
                        onChange={handleChange}
                        style={styles.radioInput}
                    />
                    {type.label}
                </label>
            ))}
        </div>
    );
}

const styles = {
    container: {
        display: 'flex',
        alignItems: 'center',
        gap: '15px',
        padding: '5px 0',
    },
    label: {
        fontWeight: 'bold',
        minWidth: '70px',
    },
    radioLabel: {
        display: 'flex',
        alignItems: 'center',
        cursor: 'pointer',
        fontSize: '14px',
    },
    radioInput: {
        marginRight: '5px',
    }
};

export default ContentTypeFilter;