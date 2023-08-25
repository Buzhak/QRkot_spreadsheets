from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_name = await charity_project_crud.get_project_id_by_name(project_name, session)
    if project_name is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    meeting_room = await charity_project_crud.get(project_id, session)
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Благотворительный проект не найден'
        )
    return meeting_room


async def check_amount(obj_db_amount: int, new_amount: int) -> None:
    if obj_db_amount > new_amount:
        raise HTTPException(
            status_code=400,
            detail='Сумма средств должна быть больше изначальной {obj_db_amount}',
        )


async def check_no_delete_invested_projects(obj_db_invested_amount: int) -> None:
    if obj_db_invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


async def check_no_edit_closed_projects(closed: bool) -> None:
    if closed:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!',
        )


async def check_no_delete_closed_projects(closed: bool) -> None:
    if closed:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя удалить!',
        )


async def no_data_in_bd(data: list) -> None:
    if len(data) == 0:
        raise HTTPException(
            status_code=404,
            detail='Данные отсутствуют.',
        )


async def service_is_unavailable() -> None:
    raise HTTPException(
        status_code=503,
        detail='Сервис временно недоступен',
    )
