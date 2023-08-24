from datetime import datetime, timedelta

from aiogoogle import Aiogoogle
from sqlalchemy.engine.row import Row

from app.core.config import settings
from app.core.google_constants import (
    COLUMN_COUNT,
    DESCTIPTION,
    FORMAT,
    NAME,
    RANGE,
    ROW_COUNT,
    SHEET_ID,
    TIME,
    TITLE,
    TITLE_2
)


async def get_title() -> str:
    '''
    Функция формирует название сотоящее из строки
    и текущего времени
    '''
    now_date_time = datetime.now().strftime(FORMAT)
    return TITLE + now_date_time


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    '''
    Создание гугл таблицы
    Функция возвращает id созданной таблицы
    '''

    service = await wrapper_services.discover('sheets', 'v4')
    title = await get_title()
    spreadsheet_body = {
        'properties': {'title': title,
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': SHEET_ID,
                                   'title': title,
                                   'gridProperties': {'rowCount': ROW_COUNT,
                                                      'columnCount': COLUMN_COUNT}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
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
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects_report: list[Row],
        wrapper_services: Aiogoogle
) -> None:
    '''Обновление данных в гугл таблице'''
    title = await get_title()
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        [title],
        [TITLE_2],
        [NAME, TIME, DESCTIPTION]
    ]
    for project in projects_report:
        new_row = [str(project[0]), str(timedelta(seconds=project[1])), str(project[2])]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=RANGE,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
