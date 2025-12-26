import json
from pathlib import Path
from typing import Any, Dict
import sys
import yaml


# Optional dependencies
try:
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    import httpx
    HTTP_AVAILABLE = True
except ImportError:
    HTTP_AVAILABLE = False


class OpenAPILoader:
    """Universal OpenAPI spec loader supporting JSON, YAML, and URLs"""
    
    @staticmethod
    def load(source: str) -> Dict[str, Any]:
        """Load OpenAPI spec from file or URL
        
        Args:
            source: File path or URL to OpenAPI spec
            
        Returns:
            Parsed OpenAPI specification dictionary
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ImportError: If required dependencies are missing
            ValueError: If file format is unsupported
        """
        if source.startswith(("http://", "https://")):
            return OpenAPILoader._load_from_url(source)

        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"OpenAPI spec not found: {source}")

        if path.suffix.lower() == ".json":
            return json.loads(path.read_text(encoding="utf-8"))

        if path.suffix.lower() in {".yaml", ".yml"}:
            if not YAML_AVAILABLE:
                raise ImportError(
                    "Install PyYAML for YAML support: pip install pyyaml"
                )
            return yaml.safe_load(path.read_text(encoding="utf-8"))

        raise ValueError(f"Unsupported file format: {path.suffix}")

    @staticmethod
    def _load_from_url(url: str) -> Dict[str, Any]:
        """Load OpenAPI spec from URL
        
        Args:
            url: HTTP/HTTPS URL to OpenAPI spec
            
        Returns:
            Parsed OpenAPI specification dictionary
            
        Raises:
            ImportError: If httpx is not installed
        """
        if not HTTP_AVAILABLE:
            raise ImportError(
                "Install httpx for URL support: pip install httpx"
            )

        response = httpx.get(url, timeout=30)
        response.raise_for_status()

        content_type = response.headers.get("content-type", "")
        if "yaml" in content_type or url.endswith((".yaml", ".yml")):
            if not YAML_AVAILABLE:
                raise ImportError(
                    "Install PyYAML for YAML support: pip install pyyaml"
                )
            return yaml.safe_load(response.text)

        return response.json()