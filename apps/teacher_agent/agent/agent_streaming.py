import sys
from pathlib import Path
import json
root_path = Path().resolve().parent.parent.parent
sys.path.append(str(root_path))

from apps.teacher_agent.agent.agent_graph import build_graph
from apps.teacher_agent.agent.agent_state import AgentState

class AgentStreaming:
    def __init__(self):
        self.graph = build_graph()

    def stream(self, state: AgentState):
        """
        This function is used to stream the agent's response.

        Args:
            state: The state of the agent.

        Returns:
            The stream chunks of the agent's response.
        """
        for chunk, meta in self.graph.stream(
            state,
            stream_mode="messages"
        ):
            chunk_type = meta.get("langgraph_node", None)

            # If the chunk is empty, skip it, to avoid spending network bandwidth
            if chunk_type == "assistant" and chunk.content == "":
                continue

            response_obj = {
                "content": chunk.content,
                "meta": meta
            }

            yield f"data: {json.dumps(response_obj)} \n\n"
