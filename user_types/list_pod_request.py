from langserve import CustomUserType


class ListPodRequest(CustomUserType):
    namespace: str = "lite"
    label_selector: str = ""
