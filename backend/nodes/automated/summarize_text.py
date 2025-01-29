from adalace import (
    AutomatedNode,
    NodeConfig,
    NodeIO,
)
from adalace.core.llm.function import llm
from adalace.core.llm.providers.openai import OpenAIProvider
from adalace.core.llm.providers.langfuse import LangfuseWrapper
from pydantic import Field
import os
from dotenv import load_dotenv
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('langfuse').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

class SummarizeTextNode(AutomatedNode[NodeIO, NodeIO]):
    """Node that uses GPT-4 to summarize text"""

    class Config(NodeConfig):
        name: str = "summarize_text"
        description: str = "Summarizes text using GPT-4"

    class Input(NodeIO):
        transcriptions: List[str] = Field(..., description="List of texts to summarize")

    class Output(NodeIO):
        summaries: List[str] = Field(..., description="List of summarized texts")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("Initializing SummarizeTextNode...")
        
        # Log environment variables (without revealing full keys)
        openai_key = os.getenv("OPENAI_API_KEY", "")
        langfuse_secret = os.getenv("LANGFUSE_SECRET_KEY", "")
        langfuse_public = os.getenv("LANGFUSE_PUBLIC_KEY", "")
        langfuse_host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    
        
        # Create base OpenAI provider
        logger.info("Creating OpenAI provider...")
        openai_provider = OpenAIProvider(
            api_key=openai_key,
            model="gpt-4"  # Using GPT-4 for better summarization
        )
        
        # Wrap it with Langfuse logging
        logger.info("Creating Langfuse wrapper...")
        self.provider = LangfuseWrapper(
            provider=openai_provider,
            secret_key=langfuse_secret,
            public_key=langfuse_public,
            host=langfuse_host
        )
        logger.info("SummarizeTextNode initialization complete")

    def process(self, data: Input) -> Output:
        logger.info("Starting text summarization process")
        logger.info(f"Processing {len(data.transcriptions)} transcriptions")
        
        @llm(provider=self.provider, reasoning_first=False)
        def summarize_text(text: str) -> str:
            f"""
            Please provide a concise summary of the following text using only emojis:
            {text}
            """

        try:
            summaries = [ summarize_text(text) for text in data.transcriptions]            
            logger.info(f"Successfully processed {len(summaries)} summaries")
            return self.Output(summaries=summaries)
        except Exception as e:
            logger.error(f"Error summarizing texts: {str(e)}")
            raise
