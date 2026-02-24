# OpenClaw 集成指南

本指南展示如何在 OpenClaw 中集成和使用 memPro。

---

## 第一步：安装 memPro

### 方式 1: 从 GitHub 安装（推荐）

```bash
pip install git+https://github.com/Kakezh/memPro.git
```

### 方式 2: 从本地安装

```bash
git clone https://github.com/Kakezh/memPro.git
cd memPro
pip install -e .
```

### 方式 3: 从 PyPI 安装（发布后）

```bash
pip install mempro
```

### 安装可选依赖

```bash
pip install mempro[sqlite,openai]  # SQLite 存储 + OpenAI 支持
```

---

## 第二步：创建 OpenClaw 插件

在 OpenClaw 项目中创建记忆插件文件：

```
extensions/memory-plugin/index.ts
```

```typescript
// extensions/memory-plugin/index.ts
import { OpenClawAdapter } from 'mempro/integrations/openclaw';

const memoryAdapter = new OpenClawAdapter({
  workspacePath: './data/memory',
  storageBackend: 'sqlite',  // 或 'memory'
});

// 导出 OpenClaw 插件
export default {
  name: 'memory-plugin',
  
  async init() {
    await memoryAdapter.init();
    console.log('Memory plugin initialized');
  },
  
  // 提供工具给 AI Agent
  getTools() {
    return memoryAdapter.getTools();
  },
  
  // 处理工具调用
  async executeTool(name: string, params: any) {
    return await memoryAdapter.executeTool(name, params);
  },
  
  async close() {
    await memoryAdapter.close();
  },
};
```

---

## 第三步：在 OpenClaw 中注册插件

在 OpenClaw 配置文件中注册插件：

```typescript
// openclaw.config.ts
export default {
  plugins: [
    './extensions/memory-plugin',
    // 其他插件...
  ],
  
  // 其他配置...
};
```

---

## 第四步：使用示例

```python
import asyncio
from mempro.integrations.openclaw import OpenClawAdapter, create_openclaw_plugin


async def main():
    # 1. 创建插件实例
    adapter = create_openclaw_plugin({
        'workspace_path': './memory-data',
        'storage_backend': 'sqlite',
    })
    
    # 2. 初始化
    await adapter.init()
    print("Memory plugin initialized!")
    
    # 3. 获取工具定义（给 AI Agent 使用）
    tools = adapter.get_tools()
    print(f"Available tools: {[t['function']['name'] for t in tools]}")
    
    # 4. 存储记忆
    result = await adapter.remember(
        content="用户正在开发一个电商平台项目",
        memory_type="fact",
        entities=["用户", "电商平台", "项目"],
        confidence=0.9,
    )
    print(f"Remember result: {result}")
    
    # 5. 检索记忆
    result = await adapter.recall("用户项目", top_k=5)
    print(f"Found {len(result['memories'])} memories")
    
    # 6. 关闭
    await adapter.close()


asyncio.run(main())
```

---

## 第五步：AI Agent 工具调用

当 AI Agent 需要使用记忆功能时，会调用以下工具：

### 工具 1: memory_remember

存储信息到长期记忆：

```json
{
  "name": "memory_remember",
  "parameters": {
    "content": "用户偏好使用 Python 进行后端开发",
    "memory_type": "preference",
    "entities": ["用户", "Python", "后端开发"],
    "confidence": 0.9
  }
}
```

### 工具 2: memory_recall

从长期记忆检索信息：

```json
{
  "name": "memory_recall",
  "parameters": {
    "query": "用户偏好",
    "top_k": 5
  }
}
```

---

## 第六步：记忆类型说明

| 类型 | 用途 | 示例 |
|------|------|------|
| `fact` | 客观事实 | "用户名字是张三" |
| `preference` | 用户偏好 | "用户喜欢深色主题" |
| `goal` | 目标 | "用户想学习机器学习" |
| `constraint` | 约束条件 | "项目预算50万" |
| `event` | 事件记录 | "用户参加了会议" |

---

## 第七步：存储后端选择

| 后端 | 用途 | 特点 |
|------|------|------|
| `memory` | 测试/开发 | 快速、无持久化 |
| `sqlite` | 单机部署 | 轻量、文件存储 |
| `postgres` | 生产环境 | 高性能、向量支持 |

---

## 完整示例

运行以下命令查看完整示例：

```bash
cd /home/kakezh/memPro
source .venv/bin/activate
PYTHONPATH=src python3 examples/basic_usage.py
```
