from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import no_data_in_bd
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.google_constants import TITLE_MESSAGE, SHEETS_SERVICE_URL
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import spreadsheets_create, set_user_permissions, spreadsheets_update_value


router = APIRouter()


@router.post(
    '/',
    response_model=dict[str, str],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    """Только для суперюзеров."""
    projects_report = await charity_project_crud.get_projects_report(
        session
    )
    no_data_in_bd(projects_report)

    # остарю это тут, чтобы можно было просмотреть результат и убедится в правильности работы функции
    # print(*projects_report, sep='\n')

    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(spreadsheet_id,
                                    projects_report,
                                    wrapper_services)
    message = {TITLE_MESSAGE: f'{SHEETS_SERVICE_URL}{spreadsheet_id}'}
    return message
