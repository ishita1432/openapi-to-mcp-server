from src.config import ConfigManager
from src.bootstrap import bootstrap_from_openapi
import argparse
import sys

# Global MCP instance (required for FastMCP discovery)
mcp = None


def main():
    """Main entry point with CLI argument parsing"""
    parser = argparse.ArgumentParser(
        description="Dynamic OpenAPI → FastMCP Server"
    )
    parser.add_argument(
        "--spec",
        help="OpenAPI JSON/YAML file or URL"
    )
    parser.add_argument(
        "--real-api",
        action="store_true",
        help="Use real API calls instead of mocks"
    )
    parser.add_argument(
        "--config",
        help="Path to config file (default: mcp_config.json)"
    )
    
    args = parser.parse_args()

    # Get spec source
    spec_source = args.spec or ConfigManager.get_spec_source(args.config)
    use_real_api = args.real_api or ConfigManager.should_use_real_api(args.config)

    if not spec_source:
        print("\n No OpenAPI spec provided!", file=sys.stderr)
        print("\nUsage examples:", file=sys.stderr)
        print("  python server.py spec.json", file=sys.stderr)
        print("  python server.py --spec spec.yaml --real-api", file=sys.stderr)
        print("  python server.py  # Reads from mcp_config.json", file=sys.stderr)
        print("\nConfig file example (mcp_config.json):", file=sys.stderr)
        print('  {"spec_path": "./specs/pizza_api.json", "use_real_api": false}', file=sys.stderr)
        sys.exit(1)

    # Bootstrap MCP server
    global mcp
    mcp = bootstrap_from_openapi(spec_source, use_real_api)


# Auto-bootstrap for `mcp run` command
spec_source = ConfigManager.get_spec_source()
use_real_api = ConfigManager.should_use_real_api()

if spec_source:
    print(f"Auto-bootstrapping MCP server...", file=sys.stderr)
    mcp = bootstrap_from_openapi(spec_source, use_real_api)


if __name__ == "__main__":
    main()
