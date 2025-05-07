import sys
from pathlib import Path

root_path = Path().resolve().parent.parent.parent
sys.path.append(str(root_path))

from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import StateGraph, START
from apps.teacher_agent.agent.agent_nodes import AgentNodes
from apps.teacher_agent.agent.agent_state import AgentState
from apps.teacher_agent.agent.agent_toolbox import TOOLS

def build_graph() -> StateGraph:
    evaluator_nodes = AgentNodes()

    graph_builder = StateGraph(AgentState)
    graph_builder.add_node("assistant", evaluator_nodes.assistant_node)
    graph_builder.add_node("tools", ToolNode(TOOLS))

    graph_builder.add_edge(START, "assistant")
    graph_builder.add_conditional_edges("assistant", tools_condition)
    graph_builder.add_edge("tools", "assistant")

    return graph_builder.compile()