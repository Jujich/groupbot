from aiogram.types import CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from routers.menu.get_groups import get_channels
from routers.start import start

router = Router()


@router.callback_query(F.data == "cancel")
async def return_to_menu(call: CallbackQuery, state: FSMContext):
    await start(call.message, state, main=False)
    await state.set_state(None)


@router.callback_query(F.data == "cancel_settings")
async def return_to_menu_from_settings(call: CallbackQuery, state: FSMContext):
    await get_channels(call, state)
    await state.update_data(channel_id=None)
    await state.set_state(None)
