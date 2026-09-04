from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.filters import Command

import os, logging
router = Router()

@router.message(Command("id"))
async def get_id(message: Message):
    await message.answer(str(message.chat.id))