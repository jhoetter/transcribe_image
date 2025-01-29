from adalace import (
    InteractiveNode,
    NodeConfig,
    NodeIO,
    InteractionData,
    BaseRuntimeParams,
)
from typing import Optional, Dict, Any, Set, List
from pydantic import Field
import logging


class EvaluateImageRuntimeParams(BaseRuntimeParams):
    are_ok: Optional[bool] = Field(None, description="Are the generated images acceptable?")
    feedback: Optional[str] = Field(None, description="Optional feedback about the images")


class EvaluateImageInteractionData(InteractionData):
    prompts: List[str] = Field(..., description="Original prompts used to generate images")
    image_urls: List[str] = Field(..., description="Generated image URLs to evaluate")


class EvaluateImageNode(InteractiveNode[NodeIO, NodeIO]):
    """Node that evaluates the quality of generated images"""

    class Config(NodeConfig):
        name: str = "evaluate_image"
        description: str = "Evaluates the quality of AI-generated images"

    class Input(NodeIO):
        prompts: List[str] = Field(..., description="Original prompts used to generate images")
        image_urls: List[str] = Field(..., description="Generated image URLs to evaluate")

    class Output(NodeIO):
        are_ok: bool = Field(..., description="Are the generated images acceptable?")
        feedback: Optional[str] = Field(None, description="Optional feedback about the images")

    def process(
        self, data: Input, runtime_params: Optional[Dict[str, Any]] = None
    ) -> Output:

        if isinstance(runtime_params, EvaluateImageRuntimeParams):
            params = runtime_params
        else:
            params = EvaluateImageRuntimeParams(**(runtime_params or {}))

        return self.Output(
            are_ok=params.are_ok,
            feedback=params.feedback
        )

    def get_interaction_data(self, data: Input) -> EvaluateImageInteractionData:
        return EvaluateImageInteractionData(
            prompts=data.prompts,
            image_urls=data.image_urls,
        )
