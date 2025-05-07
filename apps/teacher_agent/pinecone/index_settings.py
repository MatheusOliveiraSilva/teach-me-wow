import os
from dotenv import load_dotenv

load_dotenv()

INDEX_NAME = "teachmewow"
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_REGION = os.getenv("PINECONE_INDEX_REGION")
PINECONE_INDEX_DIMENSIONS = 1536
PINECONE_INDEX_METRIC = "dotproduct"
PINECONE_INDEX_CLOUD = "aws"
