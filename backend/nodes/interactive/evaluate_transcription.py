from adalace import (
    InteractiveNode,
    NodeConfig,
    NodeIO,
    InteractionData,
    BaseRuntimeParams,
)
from typing import Optional, Dict, Any, Set, List
from pydantic import Field


class EvaluateTranscriptionRuntimeParams(BaseRuntimeParams):
    are_ok: Optional[bool] = Field(None, description="Are the transcriptions ok?")


class EvaluateTranscriptionInteractionData(InteractionData):
    transcriptions: List[str] = Field(..., description="Transcriptions to evaluate")
    image_urls: List[str] = Field(..., description="Image URLs")


class EvaluateTranscriptionNode(InteractiveNode[NodeIO, NodeIO]):
    """Node that evaluates the transcription"""

    class Config(NodeConfig):
        name: str = "evaluate_transcription"
        description: str = "Evaluates the transcription"

    class Input(NodeIO):
        transcriptions: List[str] = Field(..., description="Transcriptions to evaluate")

    class Output(NodeIO):
        are_ok: bool = Field(..., description="Is the transcription ok?")

    def process(
        self, data: Input, runtime_params: Optional[Dict[str, Any]] = None
    ) -> Output:

        if isinstance(runtime_params, EvaluateTranscriptionRuntimeParams):
            params = runtime_params
        else:
            params = EvaluateTranscriptionRuntimeParams(**(runtime_params or {}))

        return self.Output(are_ok=params.are_ok)

    def get_interaction_data(self, data: Input) -> EvaluateTranscriptionInteractionData:
        files = self.get_task_files()
        # Support common image extensions
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
        image_urls = [file.download_url for file in files if file.name.lower().endswith(image_extensions)]
        return EvaluateTranscriptionInteractionData(
            transcriptions=data.transcriptions,
            image_urls=image_urls,
        )
