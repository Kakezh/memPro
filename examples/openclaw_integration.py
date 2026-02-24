"""
OpenClaw 集成示例 - 可运行的 Python 代码

演示如何在 OpenClaw 中使用 memPro。
"""

import asyncio
from mempro.integrations.openclaw import OpenClawAdapter, create_openclaw_plugin


async def step1_install():
    """第一步：安装说明"""
    print("=" * 60)
    print("第一步：安装 memPro")
    print("=" * 60)
    print("""
# 从 GitHub 安装（推荐）
pip install git+https://github.com/Kakezh/memPro.git

# 或从 PyPI 安装（发布后）
pip install mempro

# 安装可选依赖
pip install mempro[sqlite,openai]
    """)


async def step2_create_adapter():
    """第二步：创建 OpenClaw 适配器"""
    print("\n" + "=" * 60)
    print("第二步：创建 OpenClaw 适配器")
    print("=" * 60)
    
    # 创建插件实例
    adapter = create_openclaw_plugin({
        'workspace_path': '/tmp/openclaw-memory',
        'storage_backend': 'sqlite',
    })
    
    # 初始化
    await adapter.init()
    print("  Memory adapter initialized!")
    
    return adapter


async def step3_get_tools(adapter: OpenClawAdapter):
    """第三步：获取工具定义"""
    print("\n" + "=" * 60)
    print("第三步：获取工具定义（给 AI Agent 使用）")
    print("=" * 60)
    
    tools = adapter.get_tools()
    
    for tool in tools:
        print(f"\n  Tool: {tool['function']['name']}")
        print(f"  Description: {tool['function']['description']}")
        params = tool['function']['parameters']['properties']
        print(f"  Parameters: {list(params.keys())}")


async def step4_remember(adapter: OpenClawAdapter):
    """第四步：存储记忆"""
    print("\n" + "=" * 60)
    print("第四步：存储记忆")
    print("=" * 60)
    
    # 存储不同类型的记忆
    memories = [
        ("用户正在开发一个电商平台项目", "fact", ["用户", "电商平台"]),
        ("用户偏好使用 Python 进行后端开发", "preference", ["用户", "Python"]),
        ("用户想要在月底前完成项目", "goal", ["用户", "项目", "截止日期"]),
        ("项目预算上限为 50 万元", "constraint", ["项目", "预算"]),
    ]
    
    for content, mem_type, entities in memories:
        result = await adapter.remember(
            content=content,
            memory_type=mem_type,
            entities=entities,
            confidence=0.9,
        )
        print(f"  [{mem_type}] {content}")
        print(f"    -> {result['message']}")


async def step5_recall(adapter: OpenClawAdapter):
    """第五步：检索记忆"""
    print("\n" + "=" * 60)
    print("第五步：检索记忆")
    print("=" * 60)
    
    # 检索用户相关记忆
    result = await adapter.recall("用户", top_k=5)
    
    print(f"\n  找到 {len(result['memories'])} 条记忆:")
    for m in result['memories']:
        print(f"    - [{m['type']}] {m['content']}")
    
    print(f"\n  找到 {len(result['themes'])} 个主题:")
    for t in result['themes']:
        print(f"    - {t['name']}")


async def step6_stats(adapter: OpenClawAdapter):
    """第六步：查看统计"""
    print("\n" + "=" * 60)
    print("第六步：查看统计")
    print("=" * 60)
    
    stats = await adapter.stats()
    print(f"  总记忆数: {stats['total']}")
    print(f"  按层级分布: {stats['by_level']}")


async def step7_tool_execution(adapter: OpenClawAdapter):
    """第七步：模拟 AI Agent 工具调用"""
    print("\n" + "=" * 60)
    print("第七步：模拟 AI Agent 工具调用")
    print("=" * 60)
    
    # 模拟 AI Agent 的工具调用
    tool_calls = [
        {
            "name": "memory_remember",
            "params": {
                "content": "用户今天参加了产品评审会议",
                "memory_type": "event",
                "entities": ["用户", "会议"],
            }
        },
        {
            "name": "memory_recall",
            "params": {
                "query": "项目",
                "top_k": 3,
            }
        },
    ]
    
    for call in tool_calls:
        print(f"\n  调用工具: {call['name']}")
        print(f"  参数: {call['params']}")
        
        result = await adapter.execute_tool(call["name"], call["params"])
        
        if "memories" in result:
            print(f"  结果: 找到 {len(result['memories'])} 条记忆")
        else:
            print(f"  结果: {result}")


async def main():
    """运行所有步骤"""
    
    await step1_install()
    
    adapter = await step2_create_adapter()
    
    await step3_get_tools(adapter)
    await step4_remember(adapter)
    await step5_recall(adapter)
    await step6_stats(adapter)
    await step7_tool_execution(adapter)
    
    # 关闭
    await adapter.close()
    
    print("\n" + "=" * 60)
    print("OpenClaw 集成演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
