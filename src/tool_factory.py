import json
from typing import Any, Dict
from src.models import OperationMeta
from mcp.types import TextContent


class ToolFactory:
    """Factory for creating MCP tools from OpenAPI operations"""
    
    @staticmethod
    def create_tool(op: OperationMeta, executor):
        """Create an MCP tool from an OpenAPI operation
        
        Args:
            op: Operation metadata
            executor: Executor instance (HTTPExecutor or MockExecutor)
            
        Returns:
            Async function suitable for MCP tool registration
        """
        async def tool(arguments: Dict[str, Any]):
            """Dynamically generated MCP tool"""
            result = await executor.call(op, arguments)
            
            response = {
                "operation": op.name,
                "method": op.method,
                "path": op.path,
                "description": op.description,
                "response": result,
            }
            
            return [
                TextContent(
                    type="text",
                    text=json.dumps(response, indent=2, ensure_ascii=False),
                )
            ]

        # Set metadata for MCP
        tool.__name__ = op.name
        tool.__doc__ = op.description
        
        return tool

