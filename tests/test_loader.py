import pytest
# from src.loader import OpenAPILoader
from pathlib import Path
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# import sys, os
# sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from src.loader import OpenAPILoader



def test_load_json_spec():
    spec = OpenAPILoader.load("examples/pizza_openapi.json")
    assert "openapi" in spec
    assert spec["info"]["title"] == "Pizza Delivery API"

def test_load_invalid_file():
    with pytest.raises(FileNotFoundError):
        OpenAPILoader.load("nonexistent.json")

@pytest.mark.asyncio
async def test_mock_executor():
    from src.executors import MockExecutor
    from src.models import OperationMeta
    
    executor = MockExecutor()
    op = OperationMeta(
        name="listMenu",
        method="GET",
        path="/menu",
        base_url="https://api.pizza.com",
        description="List pizzas",
        parameters={},
        path_params=[]
    )
    
    result = await executor.call(op, {})
    assert result["success"] == True
    assert "data" in result
