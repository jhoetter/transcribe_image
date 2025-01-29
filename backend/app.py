from adalace import register_pipeline, run_server
from adalace.core.pipeline import Pipeline
from adalace.core.transitions import TransitionEngine
from adalace.workers.task_processor import TaskProcessor
import yaml
from nodes.automated.analyze_data import AnalyzeDataNode
from nodes.automated.entry_image import EntryImageNode
from nodes.automated.transcribe_image import TranscribeImageNode
from nodes.automated.empty_upload import EmptyUploadNode
from nodes.interactive.evaluate_transcription import EvaluateTranscriptionNode
from nodes.automated.generate_image import GenerateImageNode
from nodes.interactive.evaluate_image import EvaluateImageNode
from nodes.automated.summarize_text import SummarizeTextNode
from transitions.flow import rules
import sys


def setup_pipeline():
    """Setup and register the pipeline"""
    # Load pipeline schema
    with open("pipe.yaml") as f:
        big_pipeline_data = yaml.safe_load(f)

    # Load layout data
    with open("pipe.layout.yaml") as f:
        big_layout_data = yaml.safe_load(f)

    # Create and configure transition engine
    transition_engine = TransitionEngine()
    for rule in rules:
        transition_engine.add_rule(rule)

    # Create pipeline with node implementations and transition engine
    big_pipeline = Pipeline(
        big_pipeline_data,
        layout_data=big_layout_data,
        transition_engine=transition_engine,
        analyze_data=AnalyzeDataNode,
        entry_image=EntryImageNode,
        empty_upload=EmptyUploadNode,
        transcribe_image=TranscribeImageNode,
        evaluate_transcription=EvaluateTranscriptionNode,
        generate_image=GenerateImageNode,
        evaluate_image=EvaluateImageNode,
        summarize_text=SummarizeTextNode,
    )

    # Register pipeline for the server
    register_pipeline(big_pipeline.name, big_pipeline)
    return big_pipeline


if __name__ == "__main__":
    pipeline = setup_pipeline()
    
    # Check if we should run as a worker
    if len(sys.argv) > 1 and sys.argv[1] == "worker":
        # Run as worker
        processor = TaskProcessor()
        processor.process_automated_tasks()
    else:
        # Run as server
        run_server()
