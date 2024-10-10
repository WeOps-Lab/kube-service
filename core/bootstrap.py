import uvicorn
from langserve import add_routes

from core.server_settings import server_settings
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from starlette.middleware.cors import CORSMiddleware
from typing_extensions import Annotated

from runnable.list_pod_runnable import ListPodRunnable
from runnable.start_pilot_runnable import StartPilotRunnable
from runnable.stop_pilot_runnable import StopPilotRunnable


class Bootstrap:
    async def verify_token(self, x_token: Annotated[str, Header()]) -> None:
        if x_token != server_settings.token:
            raise HTTPException(status_code=400, detail="Token is invalid")

    def __init__(self):
        load_dotenv()

        if server_settings.token == "":
            self.app = FastAPI(title=server_settings.app_name)
        else:
            self.app = FastAPI(title=server_settings.app_name, dependencies=[Depends(self.verify_token)])

    def setup_middlewares(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
        )

    def setup_router(self):
        add_routes(self.app, ListPodRunnable().instance(), path='/list_pod')
        add_routes(self.app, StartPilotRunnable().instance(), path='/start_pilot')
        add_routes(self.app, StopPilotRunnable().instance(), path='/stop_pilot')

    def start(self):
        self.setup_middlewares()
        self.setup_router()
        uvicorn.run(self.app, host=server_settings.app_host, port=server_settings.app_port)
