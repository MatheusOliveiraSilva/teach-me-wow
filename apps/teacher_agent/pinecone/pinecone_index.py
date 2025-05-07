from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import apps.teacher_agent.pinecone.index_settings as index_settings

class PineconeIndex:
    """
    Class to manage Pinecone Index Connection
    """
    def __init__(self):
        self.index_name = index_settings.INDEX_NAME
        self.api_key = index_settings.PINECONE_API_KEY
        self.index_region = index_settings.PINECONE_INDEX_REGION
        self.index_dimensions = index_settings.PINECONE_INDEX_DIMENSIONS
        self.index_metric = index_settings.PINECONE_INDEX_METRIC
        self.index_cloud = index_settings.PINECONE_INDEX_CLOUD

        self.pc = self.get_pinecone_client()
        
    def get_pinecone_client(self) -> Pinecone:
        """
        Get pinecone client
        """
        return Pinecone(api_key=self.api_key)
    
    def get_index(self) :
        """
        Check if index exists, if not create it
        """
        # Get the list of index names
        existing_indexes = self.pc.list_indexes()

        for index in existing_indexes:
            if index.name == self.index_name:
                print(f"[Index Exists] Index {self.index_name} already exists.")
                return self.pc.Index(self.index_name)

        print(f"[Creating Index] Index {self.index_name} does not exist, creating it")
        self.pc.create_index(
            name=self.index_name,
            dimension=self.index_dimensions,
            metric=self.index_metric,
            spec=ServerlessSpec(cloud=self.index_cloud, region=self.index_region)
        )
        print(f"[Index Created] Index {self.index_name} created")
        return self.pc.Index(self.index_name)

if __name__ == "__main__":
    pc = PineconeIndex()
    pc.get_index()