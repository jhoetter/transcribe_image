from adalace import (
    AutomatedNode,
    NodeConfig,
    NodeIO,
)

class EmptyUploadNode(AutomatedNode[NodeIO, NodeIO]):
    """Node that processes entry documents for ETL pipelines"""

    class Config(NodeConfig):
        name: str = "empty_upload"
        description: str = "Processes entry documents and prepares them for ETL pipeline ingestion"

    class Input(NodeIO):
        pass

    class Output(NodeIO):
        pass

    def process(self, data: Input) -> Output:
        return self.Output()
