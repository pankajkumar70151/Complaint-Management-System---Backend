import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple
from uuid import uuid4

from fastapi import HTTPException, status

from app.config import settings
from app.models.complaint import ComplaintCreate, ComplaintInDB, ComplaintStatus

class FileStore:
    """Thread-safe async JSON file store."""
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.lock = asyncio.Lock()
        # Ensure the directory and file exist
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._sync_write([])

    def _sync_read(self) -> list:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _sync_write(self, data: list):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

    async def read_all(self) -> list:
        async with self.lock:
            return await asyncio.to_thread(self._sync_read)

    async def write_all(self, data: list):
        async with self.lock:
            await asyncio.to_thread(self._sync_write, data)


class ComplaintService:
    def __init__(self):
        self.store = FileStore(settings.DATA_FILE)

    async def create(self, data: ComplaintCreate) -> ComplaintInDB:
        now = datetime.utcnow()
        complaint = ComplaintInDB(
            id=uuid4(),
            title=data.title,
            description=data.description,
            user_name=data.user_name,
            status=ComplaintStatus.OPEN,
            created_at=now,
            updated_at=now,
        )
        complaints = await self.store.read_all()
        # Convert complaint to dict for JSON storage
        complaints.append(complaint.model_dump(mode="json"))
        await self.store.write_all(complaints)
        return complaint

    async def get_all(
        self,
        page: int = 1,
        size: int = 10,
        status_filter: Optional[ComplaintStatus] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        order: str = "desc",
    ) -> Tuple[List[ComplaintInDB], int]:
        complaints_data = await self.store.read_all()
        complaints = [ComplaintInDB(**c) for c in complaints_data]

        # Filter by status
        if status_filter:
            complaints = [c for c in complaints if c.status == status_filter]

        # Search in title and description
        if search:
            search_lower = search.lower()
            complaints = [
                c for c in complaints
                if search_lower in c.title.lower() or search_lower in c.description.lower()
            ]

        # Sort
        if sort_by not in ("created_at", "updated_at"):
            sort_by = "created_at"
        reverse = order.lower() == "desc"
        complaints.sort(key=lambda c: getattr(c, sort_by), reverse=reverse)

        total = len(complaints)

        # Paginate
        start = (page - 1) * size
        end = start + size
        paged_complaints = complaints[start:end]

        return paged_complaints, total
    
    async def get_all_complaints(self) -> Tuple[List[ComplaintInDB], int]:
        complaints_data = await self.store.read_all()
        complaints = [ComplaintInDB(**c) for c in complaints_data]

        total = len(complaints)
 

        return complaints, total

    async def get_by_id(self, complaint_id: str) -> ComplaintInDB:
        complaints_data = await self.store.read_all()
        for c in complaints_data:
            if c["id"] == complaint_id:
                return ComplaintInDB(**c)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")

    async def update_status(self, complaint_id: str, new_status: ComplaintStatus) -> ComplaintInDB:
        complaints = await self.store.read_all()
        for complaint_dict in complaints:
            if complaint_dict["id"] == complaint_id:
                complaint = ComplaintInDB(**complaint_dict)
                if complaint.status == new_status:
                    return complaint  # nothing to change
                complaint.status = new_status
                complaint.updated_at = datetime.utcnow()
                complaint_dict.update(complaint.model_dump(mode="json"))
                await self.store.write_all(complaints)
                return complaint
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")

    async def delete(self, complaint_id: str) -> None:
        complaints = await self.store.read_all()
        initial_len = len(complaints)
        complaints = [c for c in complaints if c["id"] != complaint_id]
        if len(complaints) == initial_len:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
        await self.store.write_all(complaints)