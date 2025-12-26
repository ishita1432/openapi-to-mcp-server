from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class OperationMeta:
    """Metadata for an OpenAPI operation"""
    name: str
    method: str
    path: str
    base_url: str
    description: str
    parameters: Dict[str, Any]
    path_params: List[str]
    
    def __repr__(self) -> str:
        return f"<Operation {self.name}: {self.method} {self.path}>"