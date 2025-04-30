# Knowledge Graph Component

This component builds a Neo4j-based knowledge graph from World of Warcraft talent tree data, using LLMs to extract relationships between skills, buffs, and other game mechanics.

### Example Graph Structure
<div style="display: flex; justify-content: space-between;">
  <img src="https://github.com/user-attachments/assets/7b5a9924-29a5-4dd0-8021-975a0ef8183b" width="49%" />
  <img src="https://github.com/user-attachments/assets/0bfddaf4-db02-4c75-bc1f-54a44e7c1892" width="49%" />
</div>

## Overview

The Knowledge Graph component parses World of Warcraft talent tree data and uses a Language Model to intelligently extract relationships between different game elements. It then stores these relationships in a Neo4j graph database for further querying and analysis.

## Architecture

### Main Components

- **Graph Builder (`graph_builder.py`)**: Core class that processes WoW talent data, converts it to documents, and uses LLM to extract graph relationships
- **Graph Structure Prompt (`graph_structure_prompt.py`)**: Contains the prompt templates used to instruct the LLM on how to extract graph structure from talent descriptions

### Features

- **Fault Tolerance**: Implements retry mechanism for LLM calls with configurable retry count and delay
- **Checkpointing**: Tracks progress during graph creation to allow resuming after interruptions
- **Structured Knowledge Extraction**: Uses carefully crafted prompts to extract consistent graph relationships

## Graph Structure

The knowledge graph consists of:

### Nodes
- `BUFF`: Represents a buff or effect in the game
- `SKILL`: Represents an active ability or passive skill

### Relationships
- `PROCS`: Connects skills that trigger (proc) buffs
- `BUFFS`: Connects skills that directly apply buffs
- `CDR`: Connects skills that reduce cooldowns of other skills

## Usage

1. Ensure Neo4j is running (see setup instructions below)
2. Run the graph builder:

```python
from graph_builder import DBToGraph

# Initialize the graph builder with path to talent data
builder = DBToGraph(wow_tree_nodes_data_path="path/to/wow_talents_data.json")

# Build the knowledge graph
builder.create_kg()
```

## Setup Requirements

1. Install required Python packages:
```
pip install langchain langchain-neo4j langchain-experimental python-dotenv
```

2. Start Neo4j database:
```
# Run the Neo4j script (mentioned in code comments)
./neo4j.sh
```

3. Configure environment variables:
```
# Create a .env file with your language model API keys
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
# Add Neo4j connection details if needed
```

## Advanced Configuration

### Retry Mechanism

The graph builder includes fault tolerance with configurable retry parameters:

```python
# Configure max retries and delay between retries (in seconds)
builder.create_kg(max_retries=5, retry_delay=10)
```

### Checkpoint Management

The system automatically saves progress to a checkpoint file located next to your data file. If the process is interrupted, it will resume from where it left off when restarted.

## Extending the Graph

To extend the knowledge graph with additional node types or relationships:

1. Modify the `graph_structure_prompt.py` to include new node types or relationships
2. Update the `LLMGraphTransformer` configuration in `graph_builder.py`
