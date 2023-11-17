from typing import Any

from fastapi import APIRouter

from app.models.sample_model import SampleModel
from app.schemas.sample_schema import SampleData, SampleDataList


router = APIRouter()


@router.get("/sample", response_model=SampleData)
async def sample_get() -> Any:
    data = SampleModel.all()


@router.post("/sample/", response_model=SampleDataList)
async def sample_post(sample_data: SampleData) -> Any:
    new_data = SampleModel(**sample_data.dict())
    await new_data.save()
    return {"success": True}
