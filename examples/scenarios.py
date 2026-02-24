"""
memPro 实践示例 - 具体场景演示

本文件展示 memPro 在不同场景下的使用方式。
"""

import asyncio
from mempro import MemoryService, MemoryConfig, MemoryType


async def scenario_personal_assistant():
    """
    场景 1: 个人 AI 助手 - 记住用户偏好
    
    功能演示：
    - 存储用户偏好、事实、目标
    - 检索相关记忆
    - 统计记忆数量
    """
    print("=" * 60)
    print("场景 1: 个人 AI 助手")
    print("=" * 60)
    
    service = MemoryService()
    await service.init()
    
    # 1. 存储用户偏好
    print("\n[存储偏好]")
    result = await service.memorize(
        content="用户喜欢使用深色主题，不喜欢亮色界面",
        type=MemoryType.PREFERENCE,
        entities=["用户", "深色主题", "界面"],
        confidence=0.9,
    )
    print(f"  已记住偏好: {result.semantic_id[:8]}...")
    
    # 2. 存储重要事实
    print("\n[存储事实]")
    facts = [
        ("用户的名字是张三", ["用户", "张三", "名字"]),
        ("用户是软件工程师，主要使用 Python", ["用户", "软件工程师", "Python"]),
        ("用户每周五下午有团队会议", ["用户", "团队会议", "周五"]),
    ]
    
    for content, entities in facts:
        result = await service.memorize(
            content=content,
            type=MemoryType.FACT,
            entities=entities,
            confidence=0.8,
        )
        print(f"  已记住: {content}")
    
    # 3. 存储目标
    print("\n[存储目标]")
    result = await service.memorize(
        content="用户想要学习机器学习和深度学习",
        type=MemoryType.GOAL,
        entities=["用户", "机器学习", "深度学习"],
        confidence=0.7,
    )
    print(f"  已记住目标: 用户想要学习机器学习和深度学习")
    
    # 4. 检索记忆
    print("\n[检索记忆]")
    
    results = await service.retrieve("用户偏好")
    print(f"  偏好相关记忆: {len(results.semantics)} 条")
    for m in results.semantics:
        print(f"    - [{m.type.value}] {m.content}")
    
    results = await service.retrieve("用户工作")
    print(f"  工作相关记忆: {len(results.semantics)} 条")
    for m in results.semantics:
        print(f"    - [{m.type.value}] {m.content}")
    
    # 5. 统计
    print("\n[记忆统计]")
    stats = await service.stats()
    print(f"  总记忆数: {stats.total}")
    print(f"  按层级: {stats.by_level}")
    
    await service.close()


async def scenario_hierarchy_explained():
    """
    场景 2: 四级层级存储详解
    
    层级说明：
    - Original: 原始消息，完整保存用户输入
    - Episode: 对话片段，将连续消息组织成块
    - Semantic: 语义记忆，提取可复用的事实
    - Theme: 主题，组织相关的语义记忆
    """
    print("\n" + "=" * 60)
    print("场景 2: 四级层级存储详解")
    print("=" * 60)
    
    service = MemoryService()
    await service.init()
    
    print("\n[层级结构说明]")
    print("""
    Theme (主题层)
      高层概念，组织相关的语义记忆
      例: "用户偏好"、"项目A"、"Python开发"
    
    Semantic (语义层)
      可复用的事实、偏好、目标、约束
      例: "用户喜欢深色主题" (preference)
          "项目预算50万" (constraint)
    
    Episode (片段层)
      对话片段，按主题或时间组织
      例: "用户询问界面设置，偏好深色主题"
    
    Original (原始层)
      原始消息，完整保存
      例: "我喜欢深色主题，亮色太刺眼了"
    """)
    
    # 存储一条记忆，观察层级创建
    print("\n[存储记忆并观察层级]")
    
    result = await service.memorize(
        content="我喜欢使用 Python 进行数据分析，特别是 pandas 和 numpy",
        type=MemoryType.PREFERENCE,
        entities=["用户", "Python", "数据分析", "pandas", "numpy"],
        confidence=0.9,
    )
    
    print(f"  Original ID: {result.original_id[:8]}...")
    print(f"  Episode ID:  {result.episode_id[:8]}...")
    print(f"  Semantic ID: {result.semantic_id[:8]}...")
    print(f"  Theme ID:    {result.theme_id[:8] if result.theme_id else 'None'}")
    
    # 查看统计
    print("\n[层级统计]")
    stats = await service.stats()
    for level, count in stats.by_level.items():
        print(f"  {level}: {count} 条")
    
    await service.close()


async def scenario_memory_types():
    """
    场景 3: 不同记忆类型的使用
    
    记忆类型：
    - FACT: 事实
    - PREFERENCE: 偏好
    - GOAL: 目标
    - CONSTRAINT: 约束
    - EVENT: 事件
    """
    print("\n" + "=" * 60)
    print("场景 3: 不同记忆类型")
    print("=" * 60)
    
    service = MemoryService()
    await service.init()
    
    # 存储不同类型的记忆
    memories = [
        ("用户的名字是李四", MemoryType.FACT, ["用户", "李四"]),
        ("用户偏好使用 VS Code 编辑器", MemoryType.PREFERENCE, ["用户", "VS Code"]),
        ("用户想要完成一个 Web 应用", MemoryType.GOAL, ["用户", "Web应用"]),
        ("项目必须在月底前完成", MemoryType.CONSTRAINT, ["项目", "截止日期"]),
        ("用户今天参加了产品评审会议", MemoryType.EVENT, ["用户", "会议"]),
    ]
    
    print("\n[存储不同类型记忆]")
    for content, mem_type, entities in memories:
        result = await service.memorize(
            content=content,
            type=mem_type,
            entities=entities,
            confidence=0.8,
        )
        print(f"  [{mem_type.value}] {content}")
    
    # 按类型检索
    print("\n[检索用户相关记忆]")
    results = await service.retrieve("用户")
    for m in results.semantics:
        print(f"  - [{m.type.value}] {m.content} (置信度: {m.confidence})")
    
    await service.close()


async def main():
    """运行所有场景示例"""
    
    await scenario_personal_assistant()
    await scenario_hierarchy_explained()
    await scenario_memory_types()
    
    print("\n" + "=" * 60)
    print("所有场景演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
