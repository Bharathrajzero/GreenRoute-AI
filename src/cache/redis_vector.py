import numpy as np
import redis
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

class SemanticCache:
    def __init__(self, redis_url: str):
        self.client = redis.from_url(redis_url, decode_responses=True)
        self.index_name = "idx:cache"
        self.vector_dim = 384  # Matches all-MiniLM-L6-v2 dimension
        
        try:
            from sentence_transformers import SentenceTransformer
            self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
            self.has_encoder = True
            self._initialize_vector_index()
        except Exception as e:
            print(f"Running in Lightweight Keyword Mode. Encoder init missed: {e}")
            self.has_encoder = False

    def _initialize_vector_index(self):
        """Creates an HNSW Vector Index in Redis Stack if missing."""
        try:
            self.client.ft(self.index_name).info()
        except Exception:
            schema = (
                TextField("prompt"),
                TextField("response"),
                VectorField("prompt_embedding", "HNSW", {
                    "TYPE": "FLOAT32",
                    "DIM": self.vector_dim,
                    "DISTANCE_METRIC": "COSINE"
                })
            )
            self.client.ft(self.index_name).create_index(
                fields=schema,
                definition=IndexDefinition(prefix=["cache:doc encampment:"], index_type=IndexType.HASH)
            )

    def get(self, prompt: str, distance_threshold: float = 0.15) -> str | None:
        if not self.has_encoder:
            return self.client.hget("cache:keywords", prompt)

        try:
            query_vector = self.encoder.encode(prompt).astype(np.float32).tobytes()
            q = Query(f"*=>[KNN 1 @prompt_embedding $vec_param AS vector_distance]").return_fields("response", "vector_distance").dialect(2)
            results = self.client.ft(self.index_name).search(q, query_properties={"vec_param": query_vector})
            
            if results.docs:
                nearest_doc = results.docs[0]
                if float(nearest_doc.vector_distance) <= distance_threshold:
                    return nearest_doc.response
        except Exception as e:
            print(f"Vector Index reading error: {e}")
        return None

    def set(self, prompt: str, response: str):
        if not self.has_encoder:
            self.client.hset("cache:keywords", prompt, response)
            return

        try:
            doc_id = f"cache:doc encampment:{hash(prompt)}"
            embedding = self.encoder.encode(prompt).astype(np.float32).tobytes()
            self.client.hset(doc_id, mapping={
                "prompt": prompt,
                "response": response,
                "prompt_embedding": embedding
            })
        except Exception as e:
            print(f"Vector write failed: {e}")
