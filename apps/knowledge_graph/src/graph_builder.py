import os
import sys
import json
from pathlib import Path

# Adicionar o diretório raiz ao Python path
root_dir = str(Path(__file__).parent.parent.parent.parent)
sys.path.append(root_dir)

from dotenv import load_dotenv
from apps.common.llm_config import LLMConfig
from langchain_neo4j import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from graph_structure_prompt import DB_GRAPH_PROMPT

load_dotenv()

class DBToGraph:
    def __init__(self, wow_tree_nodes_data_path: str) -> None:
        self.wow_tree_nodes_data_path = wow_tree_nodes_data_path

        # Modify temperature and model_name experimentally if need some improvements.
        self.llm = LLMConfig(provider="azure", model="gpt-4o").get_llm()

        # To use the neo4j graph, need to run neo4j.sh script. (for more info see README.md)
        self.graph = Neo4jGraph(refresh_schema=True)

        # Initialize the LLMGraphTransformer with the DB_GRAPH_PROMPT and create KB, after this send for Neo4j.
        self.llm_transformer = LLMGraphTransformer(
            llm=self.llm,
            prompt=DB_GRAPH_PROMPT,
            allowed_nodes=["BUFF", "SKILL"],
            allowed_relationships=["PROCS", "CDR", "BUFFS"],
            node_properties=["name", "description"],
            relationship_properties=["description"],
        )

    def parse_json_items_to_langchain_documents(self, json_data):
        # class_documents = []
        # specs_documents = []
        # hero_talents_documents = []

        talents_documents = []

        # Iterate over classes and specs
        for class_name in json_data:
            # For POC, only Shaman is used, uncomment for other classes when needed.    
            if class_name == "Shaman":
                for json_spec_data in json_data[class_name]['specs']:
                    for node in json_spec_data['spec_nodes']:
                        skill = node[0] + f" - {json_spec_data["spec_name"]} specialization talent:"
                        description = node[1]
                        talents_documents.append(Document(page_content=skill + "\n" + description))

                    for node in json_spec_data['hero_talent_nodes']:
                        skill = node[0] + f" - {json_spec_data["spec_name"]} hero talent:"
                        description = node[1]
                        talents_documents.append(Document(page_content=skill + "\n" + description))
            
                for node in json_data[class_name]['class_nodes']:
                    skill = node[0] + f" - {class_name} class talent:"
                    description = node[1]
                    talents_documents.append(Document(page_content=skill + "\n" + description))

            #print(class_documents)
            # print(specs_documents)
            # print(hero_talents_documents)
                        
        return talents_documents

    def create_kg(self):
        with open(self.wow_tree_nodes_data_path, "r") as file:
            wow_tree_nodes_data = json.load(file)

        talents_documents = self.parse_json_items_to_langchain_documents(wow_tree_nodes_data)

        #print(talents_documents[0].page_content)
        for document in talents_documents:
            print("Document: ", document.page_content)
            graph_from_docs = self.llm_transformer.convert_to_graph_documents([document])
            self.graph.add_graph_documents(graph_from_docs, include_source=False)

if __name__ == "__main__":
    
    db_to_graph = DBToGraph(
        wow_tree_nodes_data_path=root_dir + "/apps/etl/data/wow_talents_data.json"
    )

    db_to_graph.create_kg()
    print("Graph created successfully!")