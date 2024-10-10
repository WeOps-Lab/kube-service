import yaml
from langchain_core.runnables import RunnableLambda
from loguru import logger

from user_types.start_pilot_request import StartPilotRequest
from utils.kubernetes_client import KubernetesClient
from utils.template_loader import core_template


class StartPilotRunnable:
    def __init__(self):
        self.client = KubernetesClient()

    def execute(self, req: StartPilotRequest) -> bool:
        logger.info(f"启动Pilot: {req.pilot_id}")
        dynamic_dict = {
            "bot_id": req.pilot_id,
            "api_key": req.api_key,
            "base_url": req.munchkin_url,
            "rabbitmq_host": req.rabbitmq_host,
            "rabbitmq_port": req.rabbitmq_port,
            "rabbitmq_user": req.rabbitmq_user,
            "rabbitmq_password": req.rabbitmq_password,
            "enable_ssl": req.enable_ssl,
            "bot_domain": req.bot_domain,
            "enable_nodeport": req.enable_node_port,
            "web_nodeport": req.node_port,
        }

        try:
            deployment_template = core_template.get_template("pilot/deployment.yml")
            deployment = deployment_template.render(dynamic_dict)
            self.client.app_api.create_namespaced_deployment(namespace=req.namespace, body=yaml.safe_load(deployment))
            logger.info(f"启动Pilot[{req.id}]Pod成功")
        except Exception as e:
            logger.error(f"启动Pilot[{req.id}]Pod失败: {e}")

        try:
            svc_template = core_template.get_template("pilot/svc.yml")
            svc = svc_template.render(dynamic_dict)
            self.client.core_api.create_namespaced_service(namespace=req.namespace, body=yaml.safe_load(svc))
            logger.info(f"启动Pilot[{req.id}]Service成功")
        except Exception as e:
            logger.error(f"启动Pilot[{req.id}]Service失败: {e}")

        if req.enable_bot_domain:
            try:
                ingress_template = core_template.get_template("pilot/ingress.yml")
                ingress = ingress_template.render(dynamic_dict)
                self.client.custom_object_api.create_namespaced_custom_object(
                    group=self.client.traefik_resource_group,
                    version="v1alpha1",
                    plural="ingressroutes",
                    body=yaml.safe_load(ingress),
                    namespace=self.namespace,
                )
                logger.info(f"启动Pilot[{req.id}]Ingress成功")
            except Exception as e:
                logger.error(f"启动Pilot[{req.id}]Ingress失败: {e}")

    def instance(self):
        runnable = RunnableLambda(self.execute).with_types(
            input_type=StartPilotRequest, output_type=bool)
        return runnable
