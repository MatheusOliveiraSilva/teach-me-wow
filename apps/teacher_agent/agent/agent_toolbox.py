from apps.teacher_agent.pinecone.retrieval.retriever import Retriever
from langchain_core.documents import Document
from typing import List

def retrieve_documents(query: str) -> List[Document]:
    """
    This tool is used to retrieve documents from the Pinecone index.

    Args:
        query: The query to search for.

    Returns:
        A list of documents.
    """
    retriever = Retriever()
    return retriever.retrieve(query)

def check_skill_info(skill: str) -> str:
    """
    This tool is used to check the info of a skill.

    Args:
        skill: The skill to check the info for.

    Returns:
        A string with the skill info.
    """

    return "placeholder"

TOOLS = [retrieve_documents, check_skill_info]