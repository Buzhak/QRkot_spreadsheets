from datetime import datetime, timedelta

from aiogoogle import Aiogoogle
from sqlalchemy.engine.row import Row

from app.core.config import settings
from app.core.google_constants import (
    COLUMN_COUNT,
    DESCTIPTION,
    FORMAT,
    NAME,
    RANGE_END,
    RANGE_START,
    ROW_COUNT,
    SHEET_ID,
    TIME,
    TITLE,
    TITLE_2
)


def get_title() -> str:
    '''
    Функция формирует название сотоящее из строки
    и текущего времени
    '''
    now_date_time = datetime.now().strftime(FORMAT)
    return TITLE + now_date_time


SPREAD_SHEET_BODY = {
    'properties': {
        'title': get_title(),
        'locale': 'ru_RU'
    },
    'sheets': [{'properties': {
        'sheetType': 'GRID',
        'sheetId': SHEET_ID,
        'title': get_title(),
        'gridProperties': {
            'rowCount': ROW_COUNT,
            'columnCount': COLUMN_COUNT
        }
    }}]
}


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    '''
    Создание гугл таблицы
    Функция возвращает id созданной таблицы
    '''

    service = await wrapper_services.discover('sheets', 'v4')
    spread_sheet_body = SPREAD_SHEET_BODY
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spread_sheet_body)
    )
    spread_sheet_id = response['spreadsheetId']
    return spread_sheet_id


async def set_user_permissions(
        spread_sheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    '''
    Функция принимает id таблицы и выдаёт доступ пользоввтелю,
    email которого указан в .env или settings.
    '''
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spread_sheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spread_sheet_id: str,
        projects_report: list[Row],
        wrapper_services: Aiogoogle
) -> None:
    '''Обновление данных в гугл таблице'''
    title = get_title()
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        [title],
        [TITLE_2],
        [NAME, TIME, DESCTIPTION],
        *[
            [
                name, str(timedelta(seconds=date)), description
            ] for name, date, description in projects_report
        ]
    ]

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spread_sheet_id,
            range=f'{RANGE_START}:{RANGE_END}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
