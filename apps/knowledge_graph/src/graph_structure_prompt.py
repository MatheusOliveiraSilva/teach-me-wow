from langchain.prompts import SystemMessagePromptTemplate, PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

DB_GRAPH_STRUCTURE = SystemMessagePromptTemplate.from_template("""
You are a world of warcraft classes and specializations expert.

# Task
Your task is to build parts of a neo4j knowledge graph about world of warcraft classes and specializations skills informations.
This knowledge graph will have informations about skills, passives and buffs, and how they are related to each other.
                                                               
From this information, you need to infer that Sentinel is a Passive, because you just have chance to apply. And it's not a buff because this dont empower your character. 
                                                               
# Graph structure
The graph must be accurate and consistent with the information provided.                                  
- Nodes: should represent talent tree nodes but classify as BUFF or SKILL.
- Relationships: should capture the connections between nodes, such as:
  - PROCS: A skill that can proc a buff.
  - BUFFS: A buff that can be applied to a character using a combination of skills, or a single skill.
  - CDR: A skill that can reduce the cooldown of other skills.
                                                               
## Nodes and Their Attributes
1. BUFF: Represents a buff talent tree node.
   - Node ID: Use the node name as the ID.
   - Attributes:
     - `name`: The name of the node.
     - `description`: A brief description of the node's purpose.

2. SKILL: Represents a skill talent tree node.
   - Node ID: Use the node name as the ID.
   - Attributes:
     - `name`: The name of the node.
     - `description`: A brief description of the node's purpose.

## Relationships and Their Attributes
1. PROCS: Connects a `SKILL` node to a `BUFF` node.
   - Attributes: 
     - `description`: A brief description, how this skill can proc the buff.

2. BUFFS: Connects a `SKILL` node to a `BUFF` node.
   - Attributes: 
     - `description`: A brief description, how this skill can apply the buff or debuff the target (debuff target == buffs you).

3. CDR: Connects a `SKILL` node to a `SKILL` node.
   - Attributes: 
     - `description`: A brief description, how this skill can reduce the cooldown of other skills.


## Rules for creating relationships and nodes
1. Imagine that you receive a chunk: 

Tip of the Spear - Specialization talent tree node
Kill Command increases the direct damage of your other spells by 15%, stacking up to 3 times.

You need to create a `BUFF` node for "Tip of the Spear" and a `SKILL` node for "Kill Command".
You need to create a `PROCS` relationship between "Kill Command" and "Tip of the Spear".
                                                               
2. Try more connections are best than less connections, but dont create a relationship if you are not sure about it.


## Input Structure
You will receive a chunk of information that was extracted from world of warcraft blizzard API, this contain informations of nodes in talent tree, in the following format:
---
Node name (e.g Sentinel)
Node description (e.g Your attacks have a chance to apply Sentinel on the target, stacking up to 10 times.\r\n\r\nWhile Sentinel stacks are higher than 3, applying Sentinel has a chance to trigger an implosion, causing a stack to be consumed on the target every sec to deal 415 Arcane damage.)
---

# Output Format
Provide the knowledge graph in the following format:

### Nodes
- Node ID: `<Node_ID>`
  - `attribute_1`: `<value>`
  - `attribute_2`: `<value>`
  - ...

### Relationships
- Relationship Type: `<Relationship_Type>`
  - Source: `<Source_Node_ID>`  
  - Target: `<Target_Node_ID>`
  - Attributes:
    - `attribute_1`: `<value>`
    - `attribute_2`: `<value>`
    - ...

---

## Task
Based on the descriptive chunks provided, construct the knowledge graph with nodes and relationships using the format above. Ensure all foreign keys and their referenced columns are explicitly captured and validated, and that the `REFERENCES` relationship always connects tables, not columns.
""")


DB_GRAPH_STRUCTURE_TIP = HumanMessagePromptTemplate(
    prompt=PromptTemplate.from_template("""
Ensure you extract all relevant information from each chunk and strictly adhere to the format and rules provided above. Focus on:
1. Identifying `BUFF` nodes with their attributes (`name`, `description`).
2. Identifying `SKILL` nodes with their attributes (`name`, `description`).
3. Creating appropriate relationships:
   - `PROCS`: Links skills to buffs.
   - `BUFFS`: Links skills to buffs.
   - `CDR`: Links skills to skills.

Based on the input chunk below, construct the graph:
{input}
""")
)

DB_GRAPH_PROMPT = ChatPromptTemplate.from_messages([DB_GRAPH_STRUCTURE, DB_GRAPH_STRUCTURE_TIP])