import time

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import OperationOrm
from src.operations.schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)

@router.get("/long")
@cache(expire=60)
async def get_long_op():
    time.sleep(2)
    return "Много много данных, которые вычисляются сто лет"

@router.get("/")
async def get_specific_operations(operation_type: str,
                                  page: int = Query(default=1, ge=1),
                                  session: AsyncSession = Depends(get_async_session)):
    size = 50
    
    try:
        # Count the total number of items
        count_stmt = select(func.count()).select_from(OperationOrm).where(OperationOrm.type == operation_type)
        total = await session.scalar(count_stmt)

        # Calculate the number of pages
        max_pages = (total + size - 1) // size  # equivalent to math.ceil(total / size)

        query = (select(OperationOrm)
                 .where(OperationOrm.type == operation_type)
                 .limit(size)
                 .offset((page-1)*size)
                 )
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all(),
            "details": {
                "page": page,
                "size": size,
                "max_pages": max_pages,
                "total_items": total
            }
        }
    except Exception:
        #TODO: Log error to DB
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = OperationOrm(**new_operation.dict())
    session.add_all([stmt])
    await session.flush()
    await session.commit()
    return {"status": "success"}
