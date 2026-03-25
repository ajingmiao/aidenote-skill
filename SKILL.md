---
name: AiDeNote 录音笔记
description: 智能录音笔记管理助手 - AI 自动转写和总结录音，支持知识库管理和语义搜索
version: 1.0.0
author: AiDeNote Team
capabilities:
  - 查询和搜索录音笔记
  - 获取转写文本和 AI 总结
  - 知识库管理和语义检索
  - 文件夹分类和标签管理
---

# AiDeNote 录音笔记 API

## ⚠️ 必读约束

### 🌐 Base URL（重要！所有 API 共用）
```
https://api.aidenote.cn
```
所有 API 请求必须使用此 Base URL。

### 🔑 首次安装配置
⚠️ Agent 必读：每次调用 API 前，先检查 `$AIDENOTE_API_KEY` 是否存在。若不存在，引导用户前往 [API Key 管理页面](https://www.aidenote.cn/apikey) 获取。

**配置步骤：**
1. 访问 https://www.aidenote.cn/apikey
2. 输入密钥名称（如：OpenClaw小龙虾）
3. 点击"生成访问密钥"
4. 复制生成的 API Key（格式：sk-xxxxxxxx...）
5. 在 `~/.openclaw/openclaw.json` 中添加：
```json
{
  "skills": {
    "entries": {
      "aidenote": {
        "apiKey": "sk_你的key",
        "env": {
          "AIDENOTE_BASE_URL": "https://api.aidenote.cn"
        }
      }
    }
  }
}
```

### 🔒 安全规则
- 笔记数据属于用户隐私，不在群聊中主动展示笔记内容
- API Key 长期有效，除非用户手动删除或禁用
- 请求失败时检查 API Key 是否有效

## 认证
请求头：
```
Authorization: Bearer {token}
```

**获取 Token：**
```bash
POST /api/UserapikeyMstr/GetToken
Content-Type: application/json

{
  "apiKey": "sk-xxx..."
}
```

返回：
```json
{
  "code": 200,
  "result": {
    "token": "jwt-token",
    "userId": "user-id"
  }
}
```

后续所有请求使用返回的 `token` 作为 Bearer Token。

## 快速决策

| 用户意图 | 接口 | 关键点 |
|---------|------|--------|
| 「查我的笔记」「最近的录音」 | POST /api/AudiofileMstr/List | 分页查询，支持筛选 |
| 「看这条笔记详情」「转写内容」 | POST /api/AudiofileMstr/Get | 包含完整转写和总结 |
| 「搜索笔记」「找关于XX的」 | POST /api/AudiofileMstr/Search | 全文搜索 |
| 「查文件夹」「笔记分类」 | POST /api/UserfolderMstr/List | 树形结构 |
| 「知识库有什么」 | POST /api/KnowledgeBase/List | 知识库列表 |
| 「在知识库搜XX」 | POST /api/KnowledgeBase/Search | 语义检索 |

## 核心能力

### 📝 录音笔记管理
AiDeNote 是一个智能录音笔记系统，通过 AI 自动转写录音并生成总结。本技能让你通过自然语言快速查找和管理录音笔记。

**核心功能：**
- **查询笔记列表**：按时间、文件夹筛选
- **获取笔记详情**：完整转写文本和 AI 总结
- **全文搜索**：在所有笔记中搜索关键词
- **文件夹管理**：按文件夹组织笔记
- **知识库检索**：语义搜索知识库内容

## API 接口文档

### 笔记列表
```
POST /api/AudiofileMstr/List
Content-Type: application/json
Authorization: Bearer {token}
```

请求体：
```json
{
  "pageIndex": 1,
  "pageSize": 20,
  "audiofileFolderid": 0,
  "audiofileTitle": ""
}
```

参数说明：
- `pageIndex`: 页码，从 1 开始
- `pageSize`: 每页数量，默认 20
- `audiofileFolderid`: 文件夹 ID，0 表示全部
- `audiofileTitle`: 标题关键词筛选

返回：
```json
{
  "code": 200,
  "result": {
    "items": [
      {
        "id": 123,
        "audiofileTitle": "会议录音",
        "audiofileSummary": "AI 生成的摘要",
        "audiofileDuration": 1800,
        "createTime": "2026-03-25T10:00:00"
      }
    ],
    "total": 100
  }
}
```

### 笔记详情
```
POST /api/AudiofileMstr/Get
Content-Type: application/json
Authorization: Bearer {token}
```

请求体：
```json
{
  "id": 123
}
```

返回：
```json
{
  "code": 200,
  "result": {
    "id": 123,
    "audiofileTitle": "会议录音",
    "audiofileSummary": "AI 生成的摘要",
    "audiofileTranscript": "完整的转写文本...",
    "audiofileDuration": 1800,
    "audiofileUrl": "https://...",
    "createTime": "2026-03-25T10:00:00"
  }
}
```

### 搜索笔记
```
POST /api/AudiofileMstr/Search
Content-Type: application/json
Authorization: Bearer {token}
```

请求体：
```json
{
  "keyword": "搜索关键词",
  "pageIndex": 1,
  "pageSize": 20
}
```

### 文件夹列表
```
POST /api/UserfolderMstr/List
Content-Type: application/json
Authorization: Bearer {token}
```

返回树形结构的文件夹列表。

### 知识库搜索
```
POST /api/KnowledgeBase/Search
Content-Type: application/json
Authorization: Bearer {token}
```

请求体：
```json
{
  "query": "搜索内容",
  "topK": 5
}
```

支持语义检索，返回最相关的知识库内容。

## 使用示例

### 查询最近的笔记
```
你：帮我看看最近的录音笔记
小龙虾：好的，我帮你查询最近的笔记...

找到 5 条最近的录音：
1. 【项目会议】- 今天 14:30，时长 45 分钟
2. 【客户访谈】- 昨天 10:00，时长 1 小时
...
```

### 搜索特定内容
```
你：找一下关于"产品需求"的笔记
小龙虾：在你的笔记中搜索"产品需求"...

找到 3 条相关笔记：
1. 【产品需求讨论】- 2026-03-20
   摘要：讨论了新版本的核心功能需求...
```

### 获取笔记详情
```
你：给我看看昨天那条会议录音的详细内容
小龙虾：这是笔记的完整内容：

📝 标题：项目会议
⏱️ 时长：45 分钟
📅 时间：2026-03-24 14:30

💡 AI 总结：
本次会议主要讨论了...

📄 完整转写：
[00:00] 张三：大家好...
```

### 按文件夹查询
```
你：工作文件夹里有哪些笔记？
小龙虾：工作文件夹中有以下笔记...
```

### 知识库检索
```
你：在我的知识库里搜索"API 设计"
小龙虾：在知识库中找到以下相关内容...
```

## 常见问题

### Q: API Key 在哪里获取？
A: 访问 https://www.aidenote.cn/apikey，登录后在"我的" → "API Key"页面创建。

### Q: API Key 会过期吗？
A: API Key 长期有效，除非你手动删除或禁用。

### Q: 可以创建多个 API Key 吗？
A: 可以，你可以为不同的应用创建多个 API Key，每个最多 20 个字符的名称。

### Q: 如何撤销 API Key？
A: 在 API Key 管理页面点击删除按钮即可立即撤销。

### Q: 技能无法访问我的笔记怎么办？
A: 请检查：
1. API Key 是否正确配置
2. API Key 是否已被禁用或删除
3. Token 是否已过期（需重新调用 GetToken）
4. 网络连接是否正常

### Q: 支持哪些类型的录音？
A: 支持即时录音、会议录音、本地音频、内录音频、课堂录音等多种类型。

## 隐私说明

- 本技能仅访问你授权的 AiDeNote 账号数据
- 所有数据传输使用 HTTPS 加密
- API Key 仅用于身份认证，不会被存储或分享
- 你可以随时撤销 API Key 以停止访问
- 笔记内容不会被第三方访问或存储

## 技术支持

- **官网**：https://www.aidenote.cn
- **API Key 管理**：https://www.aidenote.cn/apikey
- **问题反馈**：在 AiDeNote 应用内"意见反馈"提交
- **技能地址**：https://clawhub.ai/aidenote/skill

## 更新日志

### v1.0.0 (2026-03-25)
- 🎉 首次发布
- ✅ 支持笔记查询和搜索
- ✅ 支持知识库语义检索
- ✅ 支持文件夹管理
- ✅ 完整的 API 文档

