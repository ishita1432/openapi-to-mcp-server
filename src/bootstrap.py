import sys
from mcp.server.fastmcp import FastMCP
from src.loader import OpenAPILoader
from src.parser import OpenAPIParser
from src.executors import HTTPExecutor, MockExecutor
from src.tool_factory import ToolFactory


def bootstrap_from_openapi(
    spec_source: str, use_real_api: bool = False
) -> FastMCP:
    """Initialize MCP server from OpenAPI spec
    
    Args:
        spec_source: Path or URL to OpenAPI specification
        use_real_api: Whether to use real API calls or mocks
        
    Returns:
        Initialized FastMCP server instance
        
    Raises:
        Exception: If spec loading or parsing fails
    """
    print(f"📋 Loading OpenAPI spec: {spec_source}", file=sys.stderr)

    try:
        # Load and parse spec
        spec = OpenAPILoader.load(spec_source)
        parser = OpenAPIParser(spec)
        
        # Choose executor
        if use_real_api:
            print("🌐 Using REAL API executor", file=sys.stderr)
            executor = HTTPExecutor()
        else:
            print("🎭 Using MOCK executor", file=sys.stderr)
            executor = MockExecutor()

        # Create MCP server
        server_name = parser.server_name()
        mcp = FastMCP(server_name)

        # Register all operations as tools
        operations = parser.operations()
        for op in operations:
            tool = ToolFactory.create_tool(op, executor)
            mcp.add_tool(tool)
            print(f"  ✓ {op.name} ({op.method} {op.path})", file=sys.stderr)

        print(f"\n✅ MCP Server ready: {server_name}", file=sys.stderr)
        print(f"📊 Registered {len(operations)} operations\n", file=sys.stderr)

        return mcp

    except Exception as e:
        print(f"❌ Error bootstrapping MCP: {e}", file=sys.stderr)
        raise

