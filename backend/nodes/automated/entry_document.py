from adalace import (
    AutomatedNode,
    NodeConfig,
    NodeIO,
)
from typing import List
from markitdown import MarkItDown
from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import Field
load_dotenv()
import tempfile
from pathlib import Path

class EntryDocumentNode(AutomatedNode[NodeIO, NodeIO]):
    """Node that processes entry documents for ETL pipelines"""

    class Config(NodeConfig):
        name: str = "entry_document"
        description: str = "Processes entry documents and prepares them for ETL pipeline ingestion"

    class Input(NodeIO):
        pass

    class Output(NodeIO):
        results: List[str] = Field(..., description="Results of the document processing")

    def process(self, data: Input) -> Output:

        files = self.get_task_files()

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        md = MarkItDown(llm_client=client, llm_model="gpt-4o-mini")

        results = []
        for file in files:
            # Create a temporary file to store the content
            with tempfile.NamedTemporaryFile(suffix=Path(file.name).suffix, delete=False) as tmp_file:
                self.download_task_file(file.name, tmp_file.name)
                tmp_file_path = tmp_file.name

            try:
                result = md.convert(tmp_file_path)
                # Extract the string content from the DocumentConverterResult
                result_text = str(result.text_content)
                results.append(result_text)
            finally:
                # Clean up the temporary file
                os.remove(tmp_file_path)

        return self.Output(results=results)
