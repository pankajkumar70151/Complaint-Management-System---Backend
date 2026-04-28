from typing import Optional

from fastapi import APIRouter, Query, status

from app.models.complaint import (
    AllComplaints,
    ComplaintCreate,
    ComplaintInDB,
    ComplaintStatus,
    ComplaintUpdateStatus,
    PaginatedComplaints,
)
from app.services.complaint_service import ComplaintService

router = APIRouter()
service = ComplaintService()


@router.post(
    "/complaints",
    response_model=ComplaintInDB,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new complaint",
    description="Submit a new complaint. Status is automatically set to 'Open'.",
)
async def create_complaint(complaint: ComplaintCreate):
    return await service.create(complaint)


@router.get(
    "/complaints",
    response_model=PaginatedComplaints,
    summary="Get all complaints",
    description="Retrieve complaints with pagination, optional status filter, text search, and sorting.",
)
async def get_complaints(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    status: Optional[ComplaintStatus] = Query(None, description="Filter by complaint status"),
    search: Optional[str] = Query(
        None, description="Search in title and description (case‑insensitive)"
    ),
    sort_by: Optional[str] = Query(
        "created_at", regex="^(created_at|updated_at)$", description="Sort field"
    ),
    order: Optional[str] = Query("desc", regex="^(asc|desc)$", description="Sort order"),
):
    items, total = await service.get_all(
        page=page,
        size=size,
        status_filter=status,
        search=search,
        sort_by=sort_by,
        order=order,
    )
    return PaginatedComplaints(total=total, page=page, size=size, items=items)
    
@router.get(
    "/complaints/all",
    response_model=AllComplaints,
    summary="Get all complaints",
    description="Retrieve all complaints",
)
async def get_all_complaints():
    items, total = await service.get_all_complaints()
    return AllComplaints(total=total, items=items)

@router.get(
    "/complaints/{complaint_id}",
    response_model=ComplaintInDB,
    summary="Get complaint by ID",
    description="Retrieve a single complaint by its UUID.",
)
async def get_complaint(complaint_id: str):
    return await service.get_by_id(complaint_id)


@router.patch(
    "/complaints/{complaint_id}/status",
    response_model=ComplaintInDB,
    summary="Update complaint status",
    description="Change the status of a complaint to 'Open', 'In Progress', or 'Resolved'.",
)
async def update_complaint_status(
    complaint_id: str,
    status_update: ComplaintUpdateStatus,
):
    return await service.update_status(complaint_id, status_update.status)


@router.delete(
    "/complaints/{complaint_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a complaint",
    description="Permanently remove a complaint from the system.",
)
async def delete_complaint(complaint_id: str):
    await service.delete(complaint_id)
    return None