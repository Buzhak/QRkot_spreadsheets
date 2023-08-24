from typing import List, Optional, Union
from sqlalchemy import func, select
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityproject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_projects_report(
            self,
            session: AsyncSession
    ) -> Union[List[Row], None]:
        '''
        Функция отдаёт список объектов БД (проектов) сотоящих из
        (name, time, description)
        в кототорые были закрыты по причине рабора нужной суммы средств
        fully_invested is True
        Столбца time нет в модели он формируется из разницы столбцов
        close_date и create_date
        и представляет из себя int, колчичество секунд.
        Возвращаемый список объектов отсортирован по столбцу time
        в порядке возрастания (от меньшего времени к большему).
        '''
        db_project_report = await session.execute(
            select(
                CharityProject.name,
                (func.strftime(
                    "%s", CharityProject.close_date
                ) - func.strftime(
                    "%s", CharityProject.create_date
                )).label("time"),
                CharityProject.description
            ).where(
                CharityProject.fully_invested == 1
            ).order_by("time")
        )
        db_project_report = db_project_report.all()
        return db_project_report


charity_project_crud = CRUDCharityproject(CharityProject)
