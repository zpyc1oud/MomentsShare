// frontend/src/App.jsx

import React from 'react';
import DiscoveryPage from './pages/DiscoveryPage/DiscoveryPage';

function App() {
  // 实际项目中这里应该使用 React Router 等配置路由
  return (
    <div className="App">
      {/* 暂时直接渲染 P4 页面 */}
      <DiscoveryPage /> 
    </div>
  );
}

export default App;