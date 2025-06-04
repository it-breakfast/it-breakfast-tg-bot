from .default import default_router, message_time_router
from .payments import payments_router

from aiogram import Router

routers: list[Router] = [default_router, payments_router, message_time_router]

def register_handlers(main_router: Router) -> None:
    for router in routers:
        main_router.include_router(router)
