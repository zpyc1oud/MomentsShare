# 修复 Docker 容器中的 pypinyin 问题

## 问题说明

Docker 容器中的镜像是在添加 `pypinyin` 依赖之前构建的，所以需要重新构建镜像或安装依赖。

## 解决方案

### 方案1：重新构建 Docker 镜像（推荐）

这会确保所有依赖都正确安装：

```bash
# 停止当前容器
docker compose down

# 重新构建镜像（不使用缓存，确保安装最新依赖）
docker compose build --no-cache

# 启动服务
docker compose up -d

# 验证 pypinyin 是否安装
docker compose exec web python manage.py test_pinyin tq "今天天气真好"
```

### 方案2：在运行的容器中直接安装（快速临时方案）

如果不想重新构建镜像，可以直接在运行的容器中安装：

```bash
# 进入 web 容器
docker compose exec web bash

# 在容器内安装 pypinyin
pip install pypinyin>=0.49.0

# 退出容器
exit

# 测试
docker compose exec web python manage.py test_pinyin tq "今天天气真好"
```

**注意**：这种方法在容器重启后会失效，因为容器内的更改不会持久化。

### 方案3：重新构建并重启（最简单）

```bash
# 一键命令：停止、重建、启动
docker compose down && docker compose build --no-cache && docker compose up -d

# 等待服务启动后测试
docker compose exec web python manage.py test_pinyin tq "今天天气真好"
```

## 验证安装

运行测试命令：

```bash
docker compose exec web python manage.py test_pinyin tq "今天天气真好"
```

应该看到：
```
pypinyin可用: True
查询词: tq
文本: 今天天气真好

文本拼音: jintiantianqizhenhao
文本首字母: jttqzh
匹配结果: True
```

## 如果还是不行

检查 requirements.txt 是否包含 pypinyin：

```bash
docker compose exec web cat requirements.txt | grep pypinyin
```

应该看到：
```
pypinyin>=0.49.0
```

如果看不到，说明 requirements.txt 没有同步到容器中，需要重新构建。

