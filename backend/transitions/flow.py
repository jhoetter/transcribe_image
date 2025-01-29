from adalace.core.transitions import TransitionRule
from nodes.automated.analyze_data import AnalyzeDataNode
from nodes.interactive.evaluate_transcription import EvaluateTranscriptionNode
from nodes.interactive.evaluate_image import EvaluateImageNode
from adalace.core.llm.function import llm
from adalace.core.llm.providers.openai import OpenAIProvider
from adalace.core.llm.providers.langfuse import LangfuseWrapper
from dotenv import load_dotenv
import os

load_dotenv()

openai_provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
langfuse_provider = LangfuseWrapper(
    provider=openai_provider,
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST"),
)


@llm(provider=langfuse_provider)
def has_files(output: AnalyzeDataNode.Output) -> bool:
    f"""
    Determine if there are files present in the analysis output.
    Input number of files: {output.num_files}
    Return true if the number of files is greater than 0.
    """


def are_images(output: AnalyzeDataNode.Output) -> bool:
    return output.are_images


def are_ok(output: EvaluateTranscriptionNode.Output) -> bool:
    return output.are_ok


def are_images_ok(output: EvaluateImageNode.Output) -> bool:
    return output.are_ok


rules = [
    TransitionRule(
        source_nodes={"analyze_data"},
        target_nodes={"entry_image"},
        condition=lambda output: has_files(output),
    ),
    TransitionRule(
        source_nodes={"analyze_data"},
        target_nodes={"empty_upload"},
        condition=lambda output: not has_files(output),
    ),
    TransitionRule(
        source_nodes={"entry_image"},
        target_nodes={"transcribe_image"},
    ),
    TransitionRule(
        source_nodes={"transcribe_image"},
        target_nodes={"summarize_text"},
    ),
    TransitionRule(
        source_nodes={"transcribe_image"},
        target_nodes={"evaluate_transcription"},
    ),
    TransitionRule(
        source_nodes={"evaluate_transcription"},
        target_nodes={"transcribe_image"},
        condition=lambda output: not are_ok(output),
    ),
    TransitionRule(
        source_nodes={"evaluate_transcription"},
        target_nodes={"generate_image"},
        condition=lambda output: are_ok(output),
    ),
    TransitionRule(
        source_nodes={"generate_image"},
        target_nodes={"evaluate_image"},
    ),
    TransitionRule(
        source_nodes={"evaluate_image"},
        target_nodes={"generate_image"},
        condition=lambda output: not are_images_ok(output),
    ),
]
