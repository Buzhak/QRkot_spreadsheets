from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.corelogic import investition
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charityproject import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)

from app.api.validators import (
    check_amount,
    check_charity_project_exists,
    check_name_duplicate,
    check_no_edit_closed_projects,
    check_no_delete_closed_projects,
    check_no_delete_invested_projects,
)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],

)
async def create_new_charity_project(
    new_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(new_project.name, session)
    new_charity_project = await charity_project_crud.create(
        new_project, session
    )
    await investition(session)
    await session.refresh(new_charity_project)
    return new_charity_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(charity_project_id, session)
    await check_no_delete_invested_projects(charity_project.invested_amount)
    await check_no_delete_closed_projects(charity_project.fully_invested)
    charity_project = await charity_project_crud.remove(charity_project, session)
    return charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    await check_no_edit_closed_projects(charity_project.fully_invested)
    if obj_in.full_amount is not None:  # проверяем что новая сумма сборов на проект не меньше предыдущей.
        await check_amount(charity_project.invested_amount, obj_in.full_amount)
        await check_name_duplicate(obj_in.name, session)

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project
