from langchain_core.runnables import RunnableLambda
from loguru import logger

from user_types.stop_pilot_request import StopPilotRequest
from utils.kubernetes_client import KubernetesClient


class StopPilotRunnable:
    def __init__(self):
        self.client = KubernetesClient()

    def execute(self, req: StopPilotRequest) -> bool:
        try:
            self.client.app_api.delete_namespaced_deployment(
                name=f"pilot-{req.bot_id}", namespace=req.namespace
            )
            logger.info(f"停止Pilot[{req.bot_id}]Pod成功")
        except Exception as e:
            logger.error(f"停止Pilot[{req.bot_id}]Pod失败: {e}")

        try:
            self.client.core_api.delete_namespaced_service(
                name=f"pilot-{req.bot_id}-service", namespace=req.namespace
            )
            logger.info(f"停止Pilot[{req.bot_id}]Service成功")
        except Exception as e:
            logger.error(f"停止Pilot[{req.bot_id}]Service失败: {e}")

        try:
            self.client.custom_object_api.delete_namespaced_custom_object(
                group=self.client.traefik_resource_group,
                version="v1alpha1",
                plural="ingressroutes",
                namespace=req.namespace,
                name=f"pilot-{req.bot_id}",
            )
        except Exception as e:
            logger.error(f"停止Pilot[{req.bot_id}]Ingress失败: {e}")

        return True

    def instance(self):
        runnable = RunnableLambda(self.execute).with_types(
            input_type=StopPilotRequest, output_type=bool
        )
        return runnable
