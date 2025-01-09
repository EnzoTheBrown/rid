from pydantic import BaseModel, Field
from settings import EMBEDDING_SIZE
from datetime import datetime
from typing import List, Optional
from embeddings import embeddings
from lancedb.pydantic import Vector
import uuid


class Note(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = None
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    vector: Optional[Vector(EMBEDDING_SIZE)] = None
