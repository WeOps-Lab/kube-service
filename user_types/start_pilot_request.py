from langserve import CustomUserType


class StartPilotRequest(CustomUserType):
    pilot_id: str
    api_key: str
    namespace: str = "lite"
    munchkin_url: str = "http://munchkin"
    rabbitmq_host: str = "rabbitmq-service"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "admin"
    rabbitmq_password: str = ""
    enable_ssl: bool = False
    bot_domain: str = ""
    enable_node_port: bool = False
    node_port: int = 18080
