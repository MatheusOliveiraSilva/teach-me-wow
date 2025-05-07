import sys
from pathlib import Path

root_path = Path().resolve().parent.parent
sys.path.append(str(root_path))
print(root_path)

from apps.teacher_agent.pinecone.index_settings import INDEX_NAME
from apps.common.embedding_config import EmbeddingConfig
from langchain_pinecone import PineconeVectorStore

WOWHEAD_GUIDES_NAMESPACE = "guides-elemental-shaman"
TOP_K = 10

class Retriever:
    def __init__(self, namespace: str = WOWHEAD_GUIDES_NAMESPACE):
        self.embedding_config = EmbeddingConfig(model="text-embedding-3-large")
        self.pinecone_vector_store = PineconeVectorStore(
            index_name=INDEX_NAME, 
            embedding=self.embedding_config.get_embedding(),
            namespace=namespace
        )

    def retrieve(self, query: str):
        return self.pinecone_vector_store.similarity_search(query, k=TOP_K)
    
if __name__ == "__main__":
    retriever = Retriever()
    print(retriever.retrieve("Fale a rotação do shaman elemental!"))