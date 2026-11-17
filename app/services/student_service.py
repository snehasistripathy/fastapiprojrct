
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models.student import Student

from app.schemas.student import (
    StudentCreate,
    StudentUpdate
)


# --------------------------------------------------
# Create Student
# --------------------------------------------------

async def create_student(
    db: AsyncSession,
    student_data: StudentCreate
):
    student = Student(
        **student_data.model_dump()
    )

    try:
        db.add(student)

        await db.commit()
        await db.refresh(student)

        return student

    except IntegrityError:
        await db.rollback()
        raise ValueError("Student email already exists")


# --------------------------------------------------
# Get All Students
# --------------------------------------------------

async def get_all_students(db: AsyncSession):

    query = select(Student).order_by(Student.id)

    result = await db.execute(query)

    return result.scalars().all()


# --------------------------------------------------
# Get Student By ID
# --------------------------------------------------

async def get_student_by_id(
    db: AsyncSession,
    student_id: int
):

    query = select(Student).where(
        Student.id == student_id
    )

    result = await db.execute(query)

    return result.scalar_one_or_none()


# --------------------------------------------------
# Update Student
# --------------------------------------------------

async def update_student(
    db: AsyncSession,
    student_id: int,
    student_data: StudentUpdate
):

    student = await get_student_by_id(
        db,
        student_id
    )

    if not student:
        return None

    update_data = student_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(student, field, value)

    try:
        await db.commit()
        await db.refresh(student)

        return student

    except IntegrityError:
        await db.rollback()
        raise ValueError("Student email already exists")


# --------------------------------------------------
# Delete Student
# --------------------------------------------------

async def delete_student(
    db: AsyncSession,
    student_id: int
):

    student = await get_student_by_id(
        db,
        student_id
    )

    if not student:
        return None

    await db.delete(student)
    await db.commit()

    return student
