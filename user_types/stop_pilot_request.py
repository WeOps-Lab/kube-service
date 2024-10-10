from langserve import CustomUserType


class StopPilotRequest(CustomUserType):
    namespace: str = "lite"
    bot_id: str
