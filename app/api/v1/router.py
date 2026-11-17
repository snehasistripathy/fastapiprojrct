
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)

from app.services import student_service


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# CREATE STUDENT
@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_student(
    student_data: StudentCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await student_service.create_student(
            db,
            student_data
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        )


# GET ALL STUDENTS
@router.get(
    "/",
    response_model=list[StudentResponse]
)
async def get_students(
    db: AsyncSession = Depends(get_db)
):
    return await student_service.get_all_students(db)


# GET STUDENT BY ID
@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    student = await student_service.get_student_by_id(
        db,
        student_id
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student


# UPDATE STUDENT
@router.put(
    "/{student_id}",
    response_model=StudentResponse
)
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: AsyncSession = Depends(get_db)
):
    try:
        student = await student_service.update_student(
            db,
            student_id,
            student_data
        )

        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        return student

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        )


# DELETE STUDENT
@router.delete(
    "/{student_id}"
)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    student = await student_service.delete_student(
        db,
        student_id
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return {
        "message": "Student deleted successfully",
        "student_id": student_id
    }
