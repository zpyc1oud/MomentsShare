# 拼音搜索功能测试指南

## 方法一：使用 Django 管理命令测试

### 1. 进入后端目录

```bash
cd backend
```

### 2. 运行测试命令

基本语法：
```bash
python manage.py test_pinyin <查询词> <文本>
```

### 测试示例

#### 测试拼音首字母匹配
```bash
# 测试 "tq" 是否能匹配 "天气"
python manage.py test_pinyin tq "今天天气真好"

# 测试 "ms" 是否能匹配 "美食"
python manage.py test_pinyin ms "今天吃了美食"
```

#### 测试拼音全拼匹配
```bash
# 测试 "tianqi" 是否能匹配 "天气"
python manage.py test_pinyin tianqi "今天天气真好"

# 测试 "meishi" 是否能匹配 "美食"
python manage.py test_pinyin meishi "今天吃了美食"
```

#### 测试中文匹配
```bash
# 测试中文直接匹配
python manage.py test_pinyin 天气 "今天天气真好"
```

### 预期输出

如果 pypinyin 已安装：
```
pypinyin可用: True
查询词: tq
文本: 今天天气真好

文本拼音: jintiantianqizhenhao
文本首字母: jttqzh
匹配结果: True
```

如果 pypinyin 未安装：
```
pypinyin可用: False
查询词: tq
文本: 今天天气真好

匹配结果: False
```

---

## 方法二：测试实际的 API 接口

### 1. 启动后端服务

```bash
cd backend
python manage.py runserver
```

### 2. 使用 curl 测试搜索 API

#### 测试拼音搜索
```bash
# 需要先登录获取 token
# 替换 YOUR_TOKEN 为实际的 JWT token

# 测试拼音首字母搜索
curl -X GET "http://localhost:8000/api/v1/moments/search/?keyword=tq" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 测试拼音全拼搜索
curl -X GET "http://localhost:8000/api/v1/moments/search/?keyword=tianqi" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 测试搜索建议 API
```bash
# 测试拼音搜索建议
curl -X GET "http://localhost:8000/api/v1/moments/search/suggestions/?q=tq" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. 使用 Postman 或浏览器测试

1. 访问 Swagger 文档：http://localhost:8000/api/docs/
2. 登录获取 token
3. 在 Swagger 界面中测试搜索接口

---

## 方法三：使用 Python Shell 测试

### 1. 进入 Django Shell

```bash
cd backend
python manage.py shell
```

### 2. 在 Shell 中测试

```python
from moments.utils import match_pinyin, get_pinyin, get_pinyin_initials, PYPINYIN_AVAILABLE

# 检查 pypinyin 是否可用
print(f"pypinyin可用: {PYPINYIN_AVAILABLE}")

# 测试拼音转换
text = "今天天气真好"
print(f"文本: {text}")
print(f"拼音: {get_pinyin(text)}")
print(f"首字母: {get_pinyin_initials(text)}")

# 测试匹配
print(f"'tq' 匹配 '{text}': {match_pinyin('tq', text)}")
print(f"'tianqi' 匹配 '{text}': {match_pinyin('tianqi', text)}")
print(f"'天气' 匹配 '{text}': {match_pinyin('天气', text)}")
```

---

## 方法四：检查 pypinyin 是否安装

### 检查安装状态

```bash
pip list | grep pypinyin
```

或者：

```bash
pip show pypinyin
```

### 如果未安装，安装它

```bash
pip install pypinyin>=0.49.0
```

或者安装所有依赖：

```bash
pip install -r requirements.txt
```

---

## 常见问题排查

### 问题1：命令找不到

**错误**：`Unknown command: test_pinyin`

**解决**：确保在 `backend` 目录下运行命令，并且 `moments/management/commands/` 目录存在

### 问题2：pypinyin 不可用

**错误**：`pypinyin可用: False`

**解决**：
```bash
pip install pypinyin>=0.49.0
```

### 问题3：匹配结果总是 False

**可能原因**：
1. pypinyin 未安装
2. 查询词格式不正确
3. 文本中没有匹配的内容

**排查步骤**：
1. 运行 `python manage.py test_pinyin tq "天气"` 测试简单情况
2. 检查 pypinyin 是否安装
3. 查看输出的拼音转换结果

---

## 快速测试脚本

创建一个测试文件 `test_pinyin_quick.py`：

```python
#!/usr/bin/env python
import os
import sys
import django

# 设置 Django 环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moments_share.settings')
django.setup()

from moments.utils import match_pinyin, get_pinyin, get_pinyin_initials, PYPINYIN_AVAILABLE

def test_cases():
    print(f"pypinyin可用: {PYPINYIN_AVAILABLE}\n")
    
    test_cases = [
        ("tq", "今天天气真好"),
        ("tianqi", "今天天气真好"),
        ("天气", "今天天气真好"),
        ("ms", "今天吃了美食"),
        ("meishi", "今天吃了美食"),
        ("美食", "今天吃了美食"),
    ]
    
    for query, text in test_cases:
        result = match_pinyin(query, text)
        status = "✓" if result else "✗"
        print(f"{status} '{query}' 匹配 '{text}': {result}")
        if PYPINYIN_AVAILABLE:
            print(f"  文本拼音: {get_pinyin(text)}")
            print(f"  文本首字母: {get_pinyin_initials(text)}")
        print()

if __name__ == "__main__":
    test_cases()
```

运行：
```bash
cd backend
python test_pinyin_quick.py
```

