from adalace import (
    AutomatedNode,
    NodeConfig,
    NodeIO,
)
from pydantic import Field
import logging
from PIL import Image
import tempfile
from pathlib import Path

class EntryImageNode(AutomatedNode[NodeIO, NodeIO]):
    """Node that processes image files and extracts metadata"""

    class Config(NodeConfig):
        name: str = "entry_image"
        description: str = "Entry image node"

    class Input(NodeIO):
        pass

    class Output(NodeIO):
        width: int = Field(..., description="Image width in pixels")
        height: int = Field(..., description="Image height in pixels")
        format: str = Field(..., description="Image format (e.g., JPEG, PNG)")
        mode: str = Field(..., description="Image mode (e.g., RGB, RGBA)")
        file_size: int = Field(..., description="File size in bytes")

    def process(self, data: Input) -> Output:
        files = self.get_task_files()
        if not files:
            raise ValueError("No files found in task")

        # Get the first image file
        image_file = files[0]
        
        # Create a temporary file to download the image
        with tempfile.NamedTemporaryFile(suffix=Path(image_file.name).suffix) as tmp_file:
            self.download_task_file(image_file.name, tmp_file.name)
            
            # Open and analyze the image
            with Image.open(tmp_file.name) as img:
                return self.Output(
                    width=img.width,
                    height=img.height,
                    format=img.format,
                    mode=img.mode,
                    file_size=image_file.size
                )
