import re
from typing import Any, Dict, List
from src.models import OperationMeta


class OpenAPIParser:
    """Parse OpenAPI specifications and extract operation metadata"""
    
    def __init__(self, spec: Dict[str, Any]):
        """Initialize parser with OpenAPI spec
        
        Args:
            spec: OpenAPI specification dictionary
        """
        self.spec = spec

    def server_name(self) -> str:
        """Extract server name from spec title"""
        return self.spec.get("info", {}).get(
            "title", "Dynamic OpenAPI MCP Server"
        )

    def base_url(self) -> str:
        """Extract base URL from servers array"""
        servers = self.spec.get("servers", [])
        if servers and isinstance(servers, list) and len(servers) > 0:
            return servers[0].get("url", "")
        return ""

    def _extract_path_params(self, path: str) -> List[str]:
        """Extract path parameters from path template
        
        Args:
            path: Path template like /users/{id}/posts/{postId}
            
        Returns:
            List of parameter names: ['id', 'postId']
        """
        return re.findall(r'\{([^}]+)\}', path)

    def operations(self) -> List[OperationMeta]:
        """Parse all operations from OpenAPI spec
        
        Returns:
            List of OperationMeta objects for all valid operations
        """
        ops: List[OperationMeta] = []

        for path, methods in self.spec.get("paths", {}).items():
            if not isinstance(methods, dict):
                continue

            for method, op in methods.items():
                if method.lower() not in {"get", "post", "put", "patch", "delete"}:
                    continue

                ops.append(self._parse_operation(path, method, op))

        return ops

    def _parse_operation(
        self, path: str, method: str, op: Dict[str, Any]
    ) -> OperationMeta:
        """Parse a single operation
        
        Args:
            path: API path
            method: HTTP method
            op: Operation object from OpenAPI spec
            
        Returns:
            OperationMeta object
        """
        # Generate operation ID
        op_id = op.get(
            "operationId",
            f"{method}_{path.strip('/').replace('/', '_').replace('{', '').replace('}', '')}",
        )

        # Extract parameters from multiple sources
        params = {}
        
        # 1. Path/query/header parameters
        for p in op.get("parameters", []):
            param_name = p.get("name")
            param_schema = p.get("schema", {})
            params[param_name] = {
                "type": param_schema.get("type", "string"),
                "in": p.get("in", "query"),
                "required": p.get("required", False),
                "description": p.get("description", "")
            }

        # 2. Request body parameters
        request_body = op.get("requestBody", {})
        if request_body:
            params.update(self._extract_body_params(request_body))

        # Extract path parameters
        path_params = self._extract_path_params(path)

        return OperationMeta(
            name=op_id,
            method=method.upper(),
            path=path,
            base_url=self.base_url(),
            description=op.get("summary") or op.get("description", "No description"),
            parameters=params,
            path_params=path_params
        )

    def _extract_body_params(self, request_body: Dict[str, Any]) -> Dict[str, Any]:
        """Extract parameters from request body schema
        
        Args:
            request_body: Request body object from OpenAPI spec
            
        Returns:
            Dictionary of parameter definitions
        """
        params = {}
        content = request_body.get("content", {})
        
        for media_type, media_obj in content.items():
            schema = media_obj.get("schema", {})
            properties = schema.get("properties", {})
            required = schema.get("required", [])
            
            for prop_name, prop_schema in properties.items():
                params[prop_name] = {
                    "type": prop_schema.get("type", "string"),
                    "in": "body",
                    "required": prop_name in required,
                    "description": prop_schema.get("description", "")
                }
        
        return params
