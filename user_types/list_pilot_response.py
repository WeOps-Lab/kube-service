from langserve import CustomUserType


class PilotInfo(CustomUserType):
    name: str
    status: str
