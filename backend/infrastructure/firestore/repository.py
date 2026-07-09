"""Base Firestore Repository."""
from typing import TypeVar, Generic, Type, List, Optional, Any, Dict
from pydantic import BaseModel
from fastapi import Depends
from .client import get_firestore_client
import structlog

logger = structlog.get_logger()

T = TypeVar("T", bound=BaseModel)

class BaseRepository(Generic[T]):
    collection_name: str
    model_class: Type[T]

    def __init__(self, db: Any = Depends(get_firestore_client)):
        self.db = db

    @property
    def collection(self):
        return self.db.collection(self.collection_name)

    async def get_by_id(self, id: str) -> Optional[T]:
        doc_ref = self.collection.document(id)
        doc = await doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            return self.model_class.model_validate(data)
        return None

    async def list_all(self, limit: int = 100, offset: int = 0) -> List[T]:
        docs = await self.collection.limit(limit).offset(offset).get()
        results = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            results.append(self.model_class.model_validate(data))
        return results

    async def query(self, filters: Dict[str, Any], limit: int = 100) -> List[T]:
        query = self.collection
        for field, value in filters.items():
            query = query.where(field, "==", value)
        
        docs = await query.limit(limit).get()
        results = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            results.append(self.model_class.model_validate(data))
        return results

    async def create(self, data: T, id: Optional[str] = None) -> str:
        doc_data = data.model_dump(exclude_unset=True)
        # remove id from document data, it will be the doc key
        doc_data.pop("id", None)
        
        if id:
            await self.collection.document(id).set(doc_data)
            return id
        else:
            _, doc_ref = await self.collection.add(doc_data)
            return doc_ref.id

    async def update(self, id: str, data: Dict[str, Any]) -> None:
        doc_ref = self.collection.document(id)
        await doc_ref.update(data)

    async def delete(self, id: str) -> None:
        await self.collection.document(id).delete()
