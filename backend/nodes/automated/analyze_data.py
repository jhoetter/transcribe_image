from adalace import (
    AutomatedNode,
    NodeConfig,
    NodeIO,
)
from pydantic import Field
import logging
from pathlib import Path


class AnalyzeDataNode(AutomatedNode[NodeIO, NodeIO]):
    """Node that processes user's name input"""

    class Config(NodeConfig):
        name: str = "analyze_data"
        description: str = "Analyze data node"

    class Input(NodeIO):
        pass

    class Output(NodeIO):
        num_files: int = Field(..., description="Number of files")
        file_extensions: list[str] = Field(
            default_factory=list, description="List of unique file extensions"
        )
        filenames: list[str] = Field(
            default_factory=list, description="List of filenames without extensions"
        )
        are_images: bool = Field(..., description="Whether all files are images")

    def process(self, data: Input) -> Output:
        files = self.get_task_files()

        if len(files) == 0:
            return self.Output(
                num_files=0, file_extensions=[], filenames=[], are_images=False
            )

        # Analyze filenames using pathlib
        file_info = [Path(file.name) for file in files]
        extensions = [f.suffix.lower() for f in file_info if f.suffix]
        names = [f.stem for f in file_info]

        # Define common image extensions
        IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

        # Check if all files are images based on file extensions
        are_images = all(f.suffix.lower() in IMAGE_EXTENSIONS for f in file_info)

        return self.Output(
            num_files=len(files),
            file_extensions=list(set(extensions)),
            filenames=names,
            are_images=are_images,
        )
