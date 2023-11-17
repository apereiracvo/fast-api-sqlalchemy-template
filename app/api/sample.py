from datetime import date
from typing import Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.models.sample_model import SampleModel
from app.schemas.sample_schema import SampleData, SampleDataList


router = APIRouter()

@router.get("/sample", response_model=SampleData)
async def sample_get() -> Any:
    data = SampleModel.all()



@router.post("/sample/", response_model=AccountList)
async def sample_post(sample_data: SampleData) -> Any:
    new_data = SampleModel(**sample_data.dict())
    new_data.save()
    return {
        "success": True
    }
