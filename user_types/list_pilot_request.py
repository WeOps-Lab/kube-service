from langserve import CustomUserType


class ListPilotRequest(CustomUserType):
    namespace: str = "lite"
    label_selector: str = ""
