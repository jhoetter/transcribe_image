from adalace import (
    AutomatedNode,
    NodeConfig,
    NodeIO,
)
from adalace.core.llm.function import llm
from adalace.core.llm.providers.openai import OpenAIProvider
from adalace.core.llm.providers.langfuse import LangfuseWrapper
from pydantic import Field
import tempfile
from pathlib import Path
import base64
import os
from dotenv import load_dotenv
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class TranscribeImageNode(AutomatedNode[NodeIO, NodeIO]):
    """Node that uses GPT-4 Vision to transcribe text from images"""

    class Config(NodeConfig):
        name: str = "transcribe_image"
        description: str = "Extracts text from images using GPT-4 Vision"

    class Input(NodeIO):
        pass

    class Output(NodeIO):
        transcriptions: List[str] = Field(
            ..., description="Transcribed text from the image"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        openai_key = os.getenv("OPENAI_API_KEY", "")
        langfuse_secret = os.getenv("LANGFUSE_SECRET_KEY", "")
        langfuse_public = os.getenv("LANGFUSE_PUBLIC_KEY", "")
        langfuse_host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

        # Create base OpenAI provider
        openai_provider = OpenAIProvider(api_key=openai_key, model="gpt-4o-mini")

        langfuse_provider = LangfuseWrapper(
            provider=openai_provider,
            secret_key=langfuse_secret,
            public_key=langfuse_public,
            host=langfuse_host,
        )

        self.provider = langfuse_provider

    def _encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def process(self, data: Input) -> Output:
        logger.info("Starting image transcription process")
        files = self.get_task_files()
        if not files:
            logger.error("No files found in task")
            raise ValueError("No files found in task")

        logger.info(f"Found {len(files)} files to process")

        @llm(provider=self.provider, reasoning_first=False)
        def transcribe_image(image_base64: str) -> str:
            """
            Please accurately describe the image in a few sentences.
            !image[{image_base64}]
            """.format(
                image_base64=image_base64
            )

        transcriptions = []
        for idx, image_file in enumerate(files, 1):
            logger.info(f"Processing image {idx}/{len(files)}: {image_file.name}")

            with tempfile.NamedTemporaryFile(
                suffix=Path(image_file.name).suffix, delete=False
            ) as tmp_file:
                logger.debug(f"Created temporary file: {tmp_file.name}")
                self.download_task_file(image_file.name, tmp_file.name)
                tmp_file_path = tmp_file.name

            try:
                logger.debug("Encoding image to base64")
                image_data_url = self._encode_image(tmp_file_path)

                logger.info("Sending image to LLM for transcription")
                transcribed_text = transcribe_image(image_data_url)
                logger.info("Received transcription from LLM")

                transcriptions.append(transcribed_text)

                logger.debug(f"Transcription result: {transcribed_text[:100]}...")
            except Exception as e:
                logger.error(f"Error processing image {image_file.name}: {str(e)}")
                raise
            finally:
                logger.debug(f"Cleaning up temporary file: {tmp_file_path}")
                os.remove(tmp_file_path)

        logger.info(f"Successfully processed {len(transcriptions)} images")
        return self.Output(transcriptions=transcriptions)
