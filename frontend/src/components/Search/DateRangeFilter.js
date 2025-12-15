// frontend/src/components/Search/DateRangeFilter.js

import React, { useState, useEffect } from 'react';

// 日期范围选择组件 (对应需求: 筛选面板 - 时间范围选择器)
function DateRangeFilter({ onChange, initialStartDate = '', initialEndDate = '' }) {
    // 内部状态，用于控制输入框的值
    const [startDate, setStartDate] = useState(initialStartDate);
    const [endDate, setEndDate] = useState(initialEndDate);

    // 使用 useEffect 来监听日期变化，并通知父组件
    useEffect(() => {
        // 只有当两个日期都非空，或者两个都清空时，才触发 onChange
        if (startDate || endDate) {
            // 确保日期格式正确 (YYYY-MM-DD)
            onChange(startDate, endDate);
        } else if (!startDate && !endDate) {
            // 允许清空日期
            onChange('', '');
        }
        // 当 startDate 或 endDate 变化时执行
    }, [startDate, endDate, onChange]);

    // 清空日期处理
    const handleClear = () => {
        setStartDate('');
        setEndDate('');
        // onChange('', ''); // useEffect 会自动触发
    };

    return (
        <div style={styles.container}>
            <span style={styles.label}>时间范围:</span>
            
            <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                style={styles.input}
                placeholder="开始日期"
            />
            
            <span style={styles.separator}>至</span>
            
            <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                style={styles.input}
                placeholder="结束日期"
            />
            
            <button onClick={handleClear} style={styles.clearButton} type="button">
                清空
            </button>
        </div>
    );
}

const styles = {
    container: {
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        padding: '5px 0',
        fontSize: '14px',
    },
    label: {
        fontWeight: 'bold',
        minWidth: '70px',
    },
    input: {
        padding: '6px',
        border: '1px solid #ccc',
        borderRadius: '4px',
    },
    separator: {
        color: '#888',
    },
    clearButton: {
        padding: '6px 10px',
        marginLeft: '10px',
        backgroundColor: '#f8f8f8',
        border: '1px solid #ddd',
        borderRadius: '4px',
        cursor: 'pointer',
    }
};

export default DateRangeFilter;