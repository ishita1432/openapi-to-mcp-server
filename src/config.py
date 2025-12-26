import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
import sys


class ConfigManager:
    """Manages configuration from multiple sources with priority:
    1. CLI arguments
    2. Environment variables
    3. Config file
    """
    
    DEFAULT_CONFIG_FILE = "mcp_config.json"
    
    
    
    @staticmethod
    def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        config_file = Path(__file__).parent.parent / (
            config_path or ConfigManager.DEFAULT_CONFIG_FILE
        )

        try:
            if not config_file.exists():
                return {}

            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config
        except Exception as e:
            print(f" Failed to load config: {e}", file=sys.stderr)
            return {}
        

    @staticmethod
    def get_spec_source(config_path: Optional[str] = None) -> Optional[str]:
        """Get OpenAPI spec source from environment or config file"""
        # Priority 1: Environment variable
        env_spec = os.environ.get("OPENAPI_SPEC")
        if env_spec:
            print(f" Using spec from environment: {env_spec}", file=sys.stderr)
            return env_spec
        
        # Priority 2: Config file
        config = ConfigManager.load_config(config_path)
        spec_path = config.get("spec_path")
        if spec_path:
            print(f" Using spec from config: {spec_path}", file=sys.stderr)
            return spec_path
        
        return None

    @staticmethod
    def should_use_real_api(config_path: Optional[str] = None) -> bool:
        """Determine if real API should be used"""
        # Priority 1: Environment variable
        if os.environ.get("USE_REAL_API", "").lower() in ("true", "1", "yes"):
            return True
        
        # Priority 2: Config file
        config = ConfigManager.load_config(config_path)
        return config.get("use_real_api", False)
