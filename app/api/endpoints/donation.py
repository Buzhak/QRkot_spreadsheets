from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (
    DonationCreate, DonationFullDB, DonationShortDB
)
from app.services.corelogic import investition

router = APIRouter()


@router.post(
    '/',
    response_model=DonationShortDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),

):
    new_donation = await donation_crud.create(
        donation, session, user
    )

    await investition(session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=List[DonationFullDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    '''
    Промотр всех донатов, толькор для суперюзера.
    '''
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=List[DonationShortDB],
    response_model_exclude={'user_id'},
)
async def get_my_reservations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    '''Просмотр своих донатов'''
    my_reservations = await donation_crud.get_by_user(user, session)
    return my_reservations
