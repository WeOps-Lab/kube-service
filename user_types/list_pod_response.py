from langserve import CustomUserType


class PodInfo(CustomUserType):
    name: str
    status: str
