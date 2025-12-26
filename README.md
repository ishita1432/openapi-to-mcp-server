"""
# Dynamic OpenAPI to FastMCP Server

A universal, modular OpenAPI specification loader that dynamically generates MCP (Model Context Protocol) tools from any OpenAPI spec.

## Features

✅ **Universal OpenAPI Support**
- Supports OpenAPI 3.0+ specifications
- Load from JSON, YAML files, or URLs
- Automatic operation discovery and tool generation

✅ **Multiple Input Sources**
- Direct file paths: `python server.py spec.json`
- Environment variables: `OPENAPI_SPEC=spec.yaml`
- Configuration files: `mcp_config.json`
- Remote URLs: `https://api.example.com/openapi.json`

✅ **Smart Mock Data**
- Realistic mock responses for testing
- Context-aware data generation (pizza orders, weather, pets, etc.)
- No external API calls needed for development

✅ **Real API Support**
- Toggle between mock and real API calls
- Full HTTP support (GET, POST, PUT, PATCH, DELETE)
- Automatic parameter handling (path, query, body, headers)

## Installation

```bash
# Core dependencies
pip install mcp httpx

# Optional dependencies
pip install pyyaml  # For YAML support
```

## Quick Start

### 1. Basic Usage

```bash
# Use default config file (mcp_config.json)
python server.py

# Specify a spec file directly
python server.py specs/pizza_api.json

# Use flags
python server.py --spec specs/weather_api.json --real-api
```

### 2. Configuration File

Create `mcp_config.json`:

```json
{
  "spec_path": "./specs/pizza_api.json",
  "use_real_api": false
}
```

### 3. Environment Variables

```bash
# Linux/Mac
export OPENAPI_SPEC="./specs/petstore_api.json"
export USE_REAL_API="true"
python server.py

# Windows
set OPENAPI_SPEC=./specs/petstore_api.json
set USE_REAL_API=true
python server.py
```

## Project Structure

```
.
├── server.py                # Main entry point
├── mcp_config.json         # Default configuration
├── src/
│   ├── config.py           # Configuration management
│   ├── models.py           # Data structures
│   ├── loader.py           # OpenAPI spec loading
│   ├── parser.py           # OpenAPI spec parsing
│   ├── executors.py        # API execution (real & mock)
│   ├── tool_factory.py     # MCP tool creation
│   └── bootstrap.py        # Server initialization
└── specs/                  # Example OpenAPI specifications
    ├── pizza_api.json
    ├── petstore_api.json
    ├── weather_api.json
    └── ecommerce_api.json
```

## Example OpenAPI Specs

### Pizza Delivery API
Operations: `listMenu`, `placeOrder`, `trackOrder`

```bash
python server.py specs/pizza_api.json
```

### Pet Store API
Operations: `addPet`, `getPetById`, `deletePet`, `findPetsByStatus`

```bash
python server.py specs/petstore_api.json
```

### Weather API
Operations: `getCurrentWeather`, `getForecast`

```bash
python server.py specs/weather_api.json
```

### E-Commerce API
Operations: `listProducts`, `addToCart`, `createOrder`

```bash
python server.py specs/ecommerce_api.json
```

## Mock Data Examples

The MockExecutor provides realistic data for testing:

### Pizza Order Response
```json
{
  "order_id": "ORD-1001",
  "status": "confirmed",
  "pizza": "Margherita",
  "size": "large",
  "quantity": 2,
  "customer_name": "John Doe",
  "total_price": 29.98,
  "estimated_delivery": "2024-01-15 19:30:00"
}
```

### Weather Response
```json
{
  "location": "New York",
  "current": {
    "temperature": 22,
    "feels_like": 20,
    "humidity": 65,
    "description": "Partly Cloudy",
    "wind_speed": 12
  }
}
```

## Creating Your Own OpenAPI Spec

1. Create a JSON or YAML file following OpenAPI 3.0 specification
2. Include at minimum:
   - `openapi` version
   - `info` (title, version)
   - `servers` (base URL)
   - `paths` (operations)

Example minimal spec:

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "My API",
    "version": "1.0.0"
  },
  "servers": [{"url": "https://api.example.com"}],
  "paths": {
    "/items": {
      "get": {
        "operationId": "listItems",
        "summary": "List all items",
        "responses": {"200": {"description": "Success"}}
      }
    }
  }
}
```

3. Load it:

```bash
python server.py my_api.json
```

## Configuration Priority

The server follows this priority order:

1. **CLI Arguments** (highest priority)
   ```bash
   python server.py --spec myspec.json --real-api
   ```

2. **Environment Variables**
   ```bash
   export OPENAPI_SPEC="myspec.json"
   export USE_REAL_API="true"
   ```

3. **Config File** (lowest priority)
   ```json
   {"spec_path": "myspec.json", "use_real_api": true}
   ```

## Advanced Usage

### Custom Config File Location

```bash
python server.py --config custom_config.json
```

### Load from URL

```bash
python server.py https://raw.githubusercontent.com/example/spec.json
```

### Real API with Authentication

Modify `src/executors.py` to add authentication:

```python
class HTTPExecutor:
    def __init__(self, api_key: str = None):
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={"Authorization": f"Bearer {api_key}"} if api_key else {}
        )
```

## Troubleshooting

### "PyYAML not installed"
```bash
pip install pyyaml
```

### "httpx not installed"
```bash
pip install httpx
```

### "No OpenAPI spec provided"
Ensure you've either:
- Created `mcp_config.json` with `spec_path`
- Set `OPENAPI_SPEC` environment variable
- Passed spec as CLI argument

## Contributing

To add support for new features:

1. **New parameter types**: Update `src/parser.py`
2. **New mock data types**: Update `src/executors.py` MockExecutor
3. **New authentication**: Update `src/executors.py` HTTPExecutor
4. **New loaders**: Update `src/loader.py`

## License

MIT License - feel free to use in your projects!
"""