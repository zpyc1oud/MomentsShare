# 前端搜索功能调试指南

## 问题描述

终端测试拼音搜索成功，但前端搜索框不能成功。

## 调试步骤

### 1. 打开浏览器开发者工具

1. 按 `F12` 或右键选择"检查"
2. 切换到 **Console（控制台）** 标签
3. 切换到 **Network（网络）** 标签

### 2. 测试搜索功能

1. 在前端搜索框输入 `tq` 或 `tianqi`
2. 观察控制台输出，应该看到：
   ```
   🔍 获取搜索建议，关键词: tq
   📥 搜索建议响应: {...}
   ✅ 建议数量: X 标签数量: Y
   ```

3. 按回车或点击搜索按钮，应该看到：
   ```
   🔍 执行搜索，参数: {keyword: "tq"}
   📥 搜索结果响应: {...}
   📊 结果数量: X
   ✅ 去重后结果数量: X
   ```

### 3. 检查网络请求

在 Network 标签中：

1. 查找 `/api/v1/moments/search/suggestions/` 请求（搜索建议）
2. 查找 `/api/v1/moments/search/` 请求（搜索结果）
3. 点击请求，查看：
   - **Request URL**: 确认参数是否正确
   - **Request Headers**: 确认有 `Authorization: Bearer ...`
   - **Response**: 查看返回的数据

### 4. 常见问题排查

#### 问题1：请求返回 401 Unauthorized

**原因**：未登录或 token 过期

**解决**：
- 检查是否已登录
- 检查 localStorage 中是否有 `access_token`
- 尝试重新登录

#### 问题2：请求返回空结果

**检查**：
- 后端是否有包含"天气"的动态内容
- 在 Network 中查看 Response，确认后端返回了什么
- 在控制台查看日志，确认前端收到了什么数据

#### 问题3：搜索建议不显示

**检查**：
- 控制台是否有错误信息
- 搜索建议 API 是否返回了数据
- `showDropdown` 计算属性是否正确

#### 问题4：拼音搜索不工作

**检查**：
1. 确认后端 pypinyin 已安装（终端测试成功说明已安装）
2. 查看后端日志，确认拼音匹配是否执行
3. 检查前端发送的关键词是否正确

### 5. 手动测试 API

在浏览器控制台中运行：

```javascript
// 测试搜索建议 API
fetch('/api/v1/moments/search/suggestions/?q=tq', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
  }
})
.then(r => r.json())
.then(data => console.log('搜索建议:', data))

// 测试搜索 API
fetch('/api/v1/moments/search/?keyword=tq', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
  }
})
.then(r => r.json())
.then(data => console.log('搜索结果:', data))
```

### 6. 检查后端日志

在 Docker 容器中查看后端日志：

```bash
docker compose logs web -f
```

然后在前端执行搜索，观察后端日志输出。

## 预期行为

### 输入 "tq" 时：

1. **搜索建议**应该显示：
   - 包含"天气"的动态内容片段
   - 匹配的标签（如果有）

2. **搜索结果**应该包含：
   - 所有包含"天气"的动态

### 输入 "tianqi" 时：

应该和输入 "tq" 有相同的结果。

## 如果还是不行

请提供以下信息：

1. 浏览器控制台的完整错误信息
2. Network 标签中搜索请求的详细信息（Request 和 Response）
3. 后端日志中的相关错误信息
4. 具体是什么不工作：
   - 搜索建议不显示？
   - 搜索结果为空？
   - 还是其他问题？

