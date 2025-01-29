from adalace import (
    AutomatedNode,
    NodeConfig,
    NodeIO,
)
from pydantic import Field
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List
import requests
import tempfile

load_dotenv()


class GenerateImageNode(AutomatedNode[NodeIO, NodeIO]):
    """Node that uses DALL-E to generate images from text descriptions"""

    class Config(NodeConfig):
        name: str = "generate_image"
        description: str = "Generates images from text descriptions using DALL-E"

    class Input(NodeIO):
        transcriptions: List[str] = Field(
            ..., description="Transcriptions to generate images from"
        )

    class Output(NodeIO):
        image_urls: List[str] = Field(..., description="Generated image URLs")
        prompts: List[str] = Field(..., description="Prompts used to generate images")

    def process(self, data: Input) -> Output:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        image_urls = []
        uploaded_urls = []

        for idx, transcription in enumerate(data.transcriptions):
            response = client.images.generate(
                model="dall-e-3",
                prompt=transcription,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            dalle_url = response.data[0].url
            image_urls.append(dalle_url)

            # Download the image and upload directly
            img_response = requests.get(dalle_url)
            if img_response.status_code == 200:
                task_file = self.upload_file_from_bytes(
                    img_response.content,
                    f"generated_image_{idx}.png"
                )
                uploaded_urls.append(task_file.download_url)

        return self.Output(image_urls=uploaded_urls, prompts=data.transcriptions)
