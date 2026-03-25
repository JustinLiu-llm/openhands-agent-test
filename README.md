# OpenHands Agent Chat

基于 OpenHands Agent 的 Chatbot 前后端项目，支持多会话持续对话功能。

## 项目结构

```
openhands-agent-chat/
├── frontend/           # 前端页面
│   └── index.html     # Chatbot 界面
└── api-test/          # 后端 API 测试脚本
    └── test_api.py    # Python API 测试
```

## 快速开始

### 1. 启动后端服务

首先需要启动 OpenHands Agent 后端服务：

```bash
# 启动 OpenHands Agent 服务
# 默认端口 8000
docker run -d -p 8000:8000 \
  --name openhands-agent \
  openhands/agent:latest
```

或使用其他启动方式，确保服务运行在 `http://localhost:8000`

### 2. 启动前端

```bash
cd frontend
python3 -m http.server 8080
```

然后在浏览器访问：**http://localhost:8080**

---

## 前端功能说明

### 界面介绍

- **顶部状态指示器**：绿色表示已连接后端，红色表示未连接
- **左侧边栏**：对话列表、新建对话、设置按钮
- **聊天区域**：显示用户和 AI 的对话消息
- **输入框**：支持 Enter 发送消息，Shift+Enter 换行

### 核心功能

| 功能 | 说明 |
|------|------|
| ✅ 自动创建会话 | 页面加载后自动创建新对话 |
| ✅ 会话持续保存 | 消息历史自动保存到 localStorage，刷新不丢失 |
| ✅ 自动恢复会话 | 刷新页面后自动回到之前的对话 |
| ✅ 对话历史持久化 | 关闭浏览器后重新打开，会话仍在 |
| ✅ 多会话支持 | 支持创建、切换、删除多个对话 |
| ✅ 自动生成标题 | 发送第一条消息后，自动用消息内容作为对话标题 |

### 使用流程

1. **首次访问**：页面自动连接后端，创建新对话
2. **发送消息**：在输入框输入内容，按 Enter 发送
3. **查看历史**：点击左侧对话列表，切换到历史对话
4. **新建对话**：点击左侧 "➕" 按钮创建新会话
5. **删除对话**：点击对话右侧 🗑️ 按钮删除

---

## 后端 API 接口

### 基础接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/alive` | GET | 检查服务是否存活 |
| `/health` | GET | 健康检查 |
| `/ready` | GET | 检查服务是否就绪 |

### 对话管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/conversations` | GET | 获取对话列表 |
| `/api/conversations` | POST | 创建新对话 |
| `/api/conversations/{id}` | GET | 获取对话详情 |
| `/api/conversations/{id}` | DELETE | 删除对话 |
| `/api/conversations/{id}/ask_agent` | POST | 向 Agent 发送消息 |
| `/api/conversations/{id}/events` | GET | 获取对话事件/消息 |

### 测试 API

```bash
# 进入测试目录
cd api-test

# 测试服务器状态
python3 test_api.py status

# 测试对话功能
python3 test_api.py conversations

# 测试 Bash 命令
python3 test_api.py bash

# 交互式聊天
python3 test_api.py chat

# 运行所有测试
python3 test_api.py all
```

---

## 配置说明

### 修改后端地址

前端默认连接 `http://localhost:8000`，可在页面设置中修改：

1. 点击右上角 **⚙️ 设置** 按钮
2. 修改 API 地址
3. 点击 **连接**

### 修改前端端口

```bash
# 修改端口
python3 -m http.server 8080  # 默认 8080
python3 -m http.server 3000  # 改为 3000
```

---

## 常见问题

### Q: 页面显示红色状态指示器

**A**: 检查后端服务是否启动，确保 `http://localhost:8000` 可访问

### Q: 刷新页面后消息丢失

**A**: 检查浏览器是否禁用了 localStorage，或尝试清除浏览器缓存

### Q: 无法创建新对话

**A**: 检查浏览器控制台是否有错误，确认后端 API 正常

---

## 技术栈

- **前端**: 原生 HTML + CSS + JavaScript
- **存储**: localStorage 持久化
- **后端**: OpenHands Agent API
- **通信**: REST API + JSON

---

## License

MIT
