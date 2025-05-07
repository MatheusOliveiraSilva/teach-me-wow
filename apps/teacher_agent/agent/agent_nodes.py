from apps.common.llm_config import LLMConfig
from apps.teacher_agent.agent.agent_state import AgentState
from langchain_core.messages import SystemMessage
from apps.teacher_agent.agent.prompts.assistant_prompt import ASSISTANT_PROMPT
from apps.teacher_agent.agent.agent_toolbox import TOOLS

class AgentNodes:
    def __init__(self):
        self.system_prompt = ASSISTANT_PROMPT

    def assistant_node(self, state: AgentState) -> AgentState:
        """
        This represents the assistant node that decides which tool will be requestest, or if we will
        just answer the question.
        """

        llm_config = LLMConfig(**state["llm_config"])
        llm = llm_config.get_llm()

        llm_with_tools = llm.bind_tools(TOOLS, parallel_tool_calls=False)

        sys_msg = SystemMessage(content=self.system_prompt)

        return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

