import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import List, Dict, Any

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

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DBToGraph:
    def __init__(self, wow_tree_nodes_data_path: str) -> None:
        self.wow_tree_nodes_data_path = wow_tree_nodes_data_path
        self.checkpoint_path = os.path.join(os.path.dirname(wow_tree_nodes_data_path), "kg_checkpoint.json")

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

    def create_kg(self, max_retries: int = 3, retry_delay: int = 5):
        with open(self.wow_tree_nodes_data_path, "r") as file:
            wow_tree_nodes_data = json.load(file)

        talents_documents = self.parse_json_items_to_langchain_documents(wow_tree_nodes_data)
        
        # Load checkpoint if exists
        processed_indices = self._load_checkpoint()
        logger.info(f"Loaded checkpoint: {len(processed_indices)} documents already processed")
        
        for idx, document in enumerate(talents_documents):
            # Skip already processed documents
            if idx in processed_indices:
                logger.info(f"Skipping document {idx} (already processed)")
                continue
                
            logger.info(f"Processing document {idx}/{len(talents_documents)}: {document.page_content[:50]}...")
            
            retry_count = 0
            success = False
            
            while not success and retry_count < max_retries:
                try:
                    print(f"Document {idx}: {document.page_content}")
                    graph_from_docs = self.llm_transformer.convert_to_graph_documents([document])
                    self.graph.add_graph_documents(graph_from_docs, include_source=False)
                    
                    # Mark as processed and save checkpoint
                    processed_indices.append(idx)
                    self._save_checkpoint(processed_indices)
                    
                    success = True
                    
                except Exception as e:
                    retry_count += 1
                    logger.error(f"Error processing document {idx} (attempt {retry_count}/{max_retries}): {str(e)}")
                    
                    if retry_count < max_retries:
                        logger.info(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                    else:
                        logger.error(f"Max retries reached for document {idx}. Moving to next document.")
        
        logger.info(f"Knowledge graph creation completed. Processed {len(processed_indices)}/{len(talents_documents)} documents.")
    
    def _load_checkpoint(self) -> List[int]:
        """Load the checkpoint file containing indices of processed documents"""
        if not os.path.exists(self.checkpoint_path):
            return []
            
        try:
            with open(self.checkpoint_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading checkpoint: {str(e)}")
            return []
    
    def _save_checkpoint(self, processed_indices: List[int]) -> None:
        """Save the current progress to checkpoint file"""
        try:
            with open(self.checkpoint_path, 'w') as f:
                json.dump(processed_indices, f)
        except Exception as e:
            logger.error(f"Error saving checkpoint: {str(e)}")

if __name__ == "__main__":
    
    db_to_graph = DBToGraph(
        wow_tree_nodes_data_path=root_dir + "/apps/etl/data/wow_talents_data.json"
    )

    db_to_graph.create_kg()
    print("Graph created successfully!")