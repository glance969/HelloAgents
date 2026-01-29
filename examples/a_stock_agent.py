"""
股票分析Agent

Agent范式包括：
- SimpleAgent: 基础对话Agent
- ReActAgent: 推理与行动结合的Agent
- ReflectionAgent: 自我反思与迭代优化的Agent
- PlanAndSolveAgent: 分解规划与逐步执行的Agent
自主决定调用哪个工具
三个工具：计算，搜素，mcp
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from hello_agents import (
    HelloAgentsLLM,
    SimpleAgent, ReActAgent, ReflectionAgent, PlanAndSolveAgent,
    ToolRegistry, search, calculate,
    ToolChain, ToolChainManager, AsyncToolExecutor
)

from hello_agents.tools import MCPTool

def demo_react_agent():
    """演示ReActAgent - 推理与行动结合"""
    print("\n" + "="*60)
    print("🔧 ReActAgent 演示 - 推理与行动结合的Agent")
    print("="*60)

    # 创建LLM实例
    llm = HelloAgentsLLM()

    # 创建工具注册表
    tool_registry = ToolRegistry()

    # 注册工具
    tool_registry.register_function(
        name="search",
        description="一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。",
        func=search
    )

    tool_registry.register_function(
        name="calculate",
        description="执行数学计算。支持基本运算、数学函数等。例如：2+3*4, sqrt(16), sin(pi/2)等。",
        func=calculate
    )

    """
		"aktools": {
			"command": "uvx",
			"args": [
				"mcp-aktools"
			],
			"type": "stdio"
		},
    """
    # 创建MCP工具
    mcp_tool = MCPTool(
    name="akshare_mcp",
	description="自定义业务逻辑服务器",
    server_command=["uvx","mcp-aktools"],
    auto_expand=True
    )
    tool_registry.register_tool(mcp_tool)

    # 自定义配置演示 - 研究助手
    print("\n--- 自定义配置：研究助手 ---")
    research_prompt = """
你是一个专业的研究助手，擅长信息收集和分析。

可用工具如下：
{tools}

请按照以下格式进行研究：

Thought: 分析问题，确定需要什么信息，制定研究策略。
Action: 选择合适的工具获取信息，格式为：
- 无参数工具：`tool_name[]`
- 单参数工具：`tool_name[参数值]`
- 多参数工具：`tool_name[{{"param1": "value1", "param2": "value2"}}]`（必须使用JSON格式）
- 完成任务：`Finish[研究结论]`

**重要**：多参数工具必须使用JSON格式，例如：`stock_prices[{{"symbol": "300058", "period": "daily"}}]`

研究问题：{question}
已完成的研究：{history}
"""

    research_agent = ReActAgent(
        name="研究助手",
        llm=llm,
        tool_registry=tool_registry,
        custom_prompt=research_prompt,
        max_steps=30
    )

    task2 = "查询一下蓝色光标最近的股票走势，当前我手头有50万资金，计算一下我最终能够买多少股，最后搜素一下相关的财经新闻，最后给我一个投资建议。"
    print(f"\n🎯 任务: {task2}")
    try:
        response = research_agent.run(task2)
        print(f"\n✅ 研究助手结果: {response}")
    except Exception as e:
        print(f"❌ 错误: {e}")



def main():
    """主函数"""
    print("🚀 HelloAgents 框架完整演示")
    print("基于OpenAI原生API的多智能体框架")
    print("\n🎯 演示内容：")
    print("1. 四种Agent范式的默认配置使用")
    print("2. 自定义配置的高级用法")
    print("3. 默认 vs 自定义配置的对比")
    print("4. 高级功能：工具链和异步执行")
    print("5. 交互式Agent体验")

    try:
        # 2. ReActAgent演示（默认 + 自定义）
        demo_react_agent()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")

if __name__ == "__main__":
    main()
