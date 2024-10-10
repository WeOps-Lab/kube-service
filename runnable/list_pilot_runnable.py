from typing import List

from langchain_core.runnables import RunnableLambda
from loguru import logger

from user_types.list_pilot_request import ListPilotRequest
from user_types.list_pilot_response import PilotInfo
from utils.kubernetes_client import KubernetesClient


class ListPilotRunnable:
    def __init__(self):
        self.client = KubernetesClient()

    def execute(self, req: ListPilotRequest) -> List[PilotInfo]:
        logger.info(f"列出命名空间'{req.namespace}'中的Pod，标签选择器: {req.label_selector}")

        try:
            pods = self.client.core_api.list_namespaced_pod(namespace=req.namespace, label_selector=req.label_selector)
            pod_list = [PilotInfo(name=pod.metadata.name, status=pod.status.phase) for pod in pods.items if
                        pod.metadata.name.startswith("pilot-")]
            logger.info(f"共找到 {len(pods.items)} 个Pod")
            return pod_list

        except Exception as e:
            logger.error(f"列出命名空间'{req.namespace}'中的Pod失败: {e}")
            return []

    def instance(self):
        runnable = RunnableLambda(self.execute).with_types(
            input_type=ListPilotRequest, output_type=list)
        return runnable
