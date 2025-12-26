from typing import Any, Dict
from src.models import OperationMeta
import sys
import random
from datetime import datetime, timedelta

try:
    import httpx
    HTTP_AVAILABLE = True
except ImportError:
    HTTP_AVAILABLE = False


class HTTPExecutor:
    """Execute real HTTP requests based on OpenAPI operations"""
    
    def __init__(self):
        """Initialize HTTP client
        
        Raises:
            ImportError: If httpx is not installed
        """
        if not HTTP_AVAILABLE:
            raise ImportError(
                "Install httpx for HTTP support: pip install httpx"
            )
        self.client = httpx.AsyncClient(timeout=30.0)

    async def call(
        self, op: OperationMeta, args: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute the API call
        
        Args:
            op: Operation metadata
            args: Arguments provided by user
            
        Returns:
            Response dictionary with status, data, and metadata
        """
        try:
            # Build URL with path parameters
            url = self._build_url(op, args)
            
            # Separate parameters by location
            query_params, body_params, headers = self._categorize_params(op, args)

            # Make request
            response = await self._make_request(
                op.method.lower(), url, query_params, body_params, headers
            )
            
            # Parse response
            try:
                response_data = response.json()
            except:
                response_data = {"text": response.text}

            return {
                "success": True,
                "status_code": response.status_code,
                "data": response_data,
                "url": str(response.url)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }

    def _build_url(self, op: OperationMeta, args: Dict[str, Any]) -> str:
        """Build URL with path parameters substituted"""
        url = op.base_url + op.path
        for param in op.path_params:
            if param in args:
                url = url.replace(f"{{{param}}}", str(args[param]))
        return url

    def _categorize_params(
        self, op: OperationMeta, args: Dict[str, Any]
    ) -> tuple[Dict, Dict, Dict]:
        """Separate parameters by location (query, body, header)"""
        query_params = {}
        body_params = {}
        headers = {}

        for key, value in args.items():
            if key in op.parameters:
                param_info = op.parameters[key]
                if param_info["in"] == "query":
                    query_params[key] = value
                elif param_info["in"] == "body":
                    body_params[key] = value
                elif param_info["in"] == "header":
                    headers[key] = value

        return query_params, body_params, headers

    async def _make_request(
        self, method: str, url: str, 
        query_params: Dict, body_params: Dict, headers: Dict
    ):
        """Make HTTP request with appropriate parameters"""
        request_kwargs = {
            "params": query_params if query_params else None,
            "headers": headers if headers else None,
        }

        if body_params:
            request_kwargs["json"] = body_params

        return await self.client.request(method, url, **request_kwargs)


# class MockExecutor:
#     """Mock executor for testing without real API calls"""
    
#     async def call(
#         self, op: OperationMeta, args: Dict[str, Any]
#     ) -> Dict[str, Any]:
#         """Return mock response
        
#         Args:
#             op: Operation metadata
#             args: Arguments provided by user
            
#         Returns:
#             Mock response dictionary
#         """
#         return {
#             "mock": True,
#             "operation": op.name,
#             "method": op.method,
#             "path": op.path,
#             "base_url": op.base_url,
#             "received_arguments": args,
#             "note": "Mock response. Set use_real_api: true in config for real calls."
#         }

class MockExecutor:
    """Mock executor with realistic response data for testing"""
    
    def __init__(self):
        """Initialize mock data generators"""
        self.pizza_menu = self._generate_pizza_menu()
        self.order_counter = 1000
        self.pet_counter = 100
        
    def _generate_pizza_menu(self) -> list:
        """Generate realistic pizza menu"""
        return [
            {
                "id": "pizza_001",
                "name": "Margherita",
                "category": "classic",
                "description": "Fresh mozzarella, tomato sauce, basil",
                "prices": {"small": 8.99, "medium": 11.99, "large": 14.99, "xlarge": 17.99},
                "available": True,
                "toppings": ["mozzarella", "tomato sauce", "basil"]
            },
            {
                "id": "pizza_002",
                "name": "Pepperoni",
                "category": "classic",
                "description": "Pepperoni, mozzarella, tomato sauce",
                "prices": {"small": 9.99, "medium": 12.99, "large": 15.99, "xlarge": 18.99},
                "available": True,
                "toppings": ["pepperoni", "mozzarella", "tomato sauce"]
            },
            {
                "id": "pizza_003",
                "name": "Hawaiian",
                "category": "specialty",
                "description": "Ham, pineapple, mozzarella",
                "prices": {"small": 10.99, "medium": 13.99, "large": 16.99, "xlarge": 19.99},
                "available": True,
                "toppings": ["ham", "pineapple", "mozzarella"]
            },
            {
                "id": "pizza_004",
                "name": "Veggie Supreme",
                "category": "vegetarian",
                "description": "Bell peppers, onions, mushrooms, olives",
                "prices": {"small": 10.99, "medium": 13.99, "large": 16.99, "xlarge": 19.99},
                "available": True,
                "toppings": ["bell peppers", "onions", "mushrooms", "olives", "mozzarella"]
            },
            {
                "id": "pizza_005",
                "name": "Meat Lovers",
                "category": "specialty",
                "description": "Pepperoni, sausage, bacon, ham",
                "prices": {"small": 11.99, "medium": 14.99, "large": 17.99, "xlarge": 20.99},
                "available": True,
                "toppings": ["pepperoni", "sausage", "bacon", "ham", "mozzarella"]
            }
        ]
    
    async def call(
        self, op: OperationMeta, args: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Return realistic mock response based on operation
        
        Args:
            op: Operation metadata
            args: Arguments provided by user
            
        Returns:
            Mock response dictionary with realistic data
        """
        # Generate realistic mock data based on operation
        mock_data = self._generate_mock_data(op, args)
        
        return {
            "success": True,
            "status_code": 200,
            "mock": True,
            "data": mock_data,
            "metadata": {
                "operation": op.name,
                "method": op.method,
                "path": op.path,
                "base_url": op.base_url,
                "received_arguments": args
            },
            "note": "Mock response. Set use_real_api: true in config for real calls."
        }
    
    def _generate_mock_data(self, op: OperationMeta, args: Dict[str, Any]) -> Any:
        """Generate realistic mock data based on operation type"""
        
        # Pizza API mock data
        if "menu" in op.name.lower() or "list" in op.name.lower():
            return self._mock_pizza_menu(args)
        
        if "order" in op.name.lower() and op.method == "POST":
            return self._mock_place_order(args)
        
        if "track" in op.name.lower() or ("order" in op.name.lower() and op.method == "GET"):
            return self._mock_track_order(args)
        
        # Pet Store mock data
        if "pet" in op.name.lower():
            if op.method == "POST":
                return self._mock_add_pet(args)
            elif op.method == "GET":
                return self._mock_get_pet(args)
            elif "status" in op.name.lower():
                return self._mock_find_pets_by_status(args)
        
        # Weather API mock data
        if "weather" in op.name.lower() or "forecast" in op.name.lower():
            return self._mock_weather(args)
        
        # E-commerce mock data
        if "product" in op.name.lower():
            return self._mock_products(args)
        
        if "cart" in op.name.lower():
            return self._mock_cart(args)
        
        # Generic mock response
        return {
            "message": "Operation successful",
            "timestamp": datetime.now().isoformat(),
            "data": args
        }
    
    def _mock_pizza_menu(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Mock pizza menu listing"""
        category = args.get("category")
        menu = self.pizza_menu
        
        if category:
            menu = [p for p in menu if p["category"] == category]
        
        return {
            "pizzas": menu,
            "total": len(menu),
            "timestamp": datetime.now().isoformat()
        }
    
    def _mock_place_order(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Mock pizza order placement"""
        order_id = f"ORD-{self.order_counter}"
        self.order_counter += 1
        
        pizza = next((p for p in self.pizza_menu if p["id"] == args.get("pizza_id")), None)
        size = args.get("size", "medium")
        quantity = args.get("quantity", 1)
        
        price = 0
        if pizza:
            price = pizza["prices"].get(size, 12.99) * quantity
        
        estimated_delivery = datetime.now() + timedelta(minutes=random.randint(25, 45))
        
        return {
            "order_id": order_id,
            "status": "confirmed",
            "pizza": pizza["name"] if pizza else "Unknown",
            "size": size,
            "quantity": quantity,
            "customer_name": args.get("customer_name"),
            "delivery_address": args.get("address"),
            "phone": args.get("phone"),
            "extra_toppings": args.get("extra_toppings", []),
            "total_price": round(price, 2),
            "estimated_delivery": estimated_delivery.strftime("%Y-%m-%d %H:%M:%S"),
            "order_time": datetime.now().isoformat()
        }
    
    def _mock_track_order(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Mock order tracking"""
        order_id = args.get("orderId", "ORD-1000")
        
        statuses = ["preparing", "baking", "quality_check", "out_for_delivery", "delivered"]
        current_status = random.choice(statuses[:4])  # Don't always show delivered
        
        return {
            "order_id": order_id,
            "status": current_status,
            "status_history": [
                {"status": "confirmed", "timestamp": "2024-01-15 18:00:00"},
                {"status": "preparing", "timestamp": "2024-01-15 18:05:00"},
                {"status": "baking", "timestamp": "2024-01-15 18:15:00"}
            ],
            "estimated_delivery": (datetime.now() + timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S"),
            "driver": {"name": "John Doe", "phone": "+1-555-0123"} if current_status == "out_for_delivery" else None
        }
    
    def _mock_add_pet(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Mock adding a pet"""
        pet_id = self.pet_counter
        self.pet_counter += 1
        
        return {
            "id": pet_id,
            "name": args.get("name"),
            "photoUrls": args.get("photoUrls", []),
            "status": args.get("status", "available"),
            "category": {"id": 1, "name": "Dogs"},
            "tags": []
        }
    
    def _mock_get_pet(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Mock getting a pet by ID"""
        pet_id = args.get("petId", 1)
        
        return {
            "id": pet_id,
            "name": f"Pet_{pet_id}",
            "photoUrls": [f"https://example.com/photo{pet_id}.jpg"],
            "status": "available",
            "category": {"id": 1, "name": "Dogs"}
        }
    
    def _mock_find_pets_by_status(self, args: Dict[str, Any]) -> list:
        """Mock finding pets by status"""
        status = args.get("status", "available")
        
        return [
            {"id": 1, "name": "Buddy", "status": status},
            {"id": 2, "name": "Max", "status": status},
            {"id": 3, "name": "Luna", "status": status}
        ]
    
    def _mock_weather(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Mock weather data"""
        location = args.get("location", "Unknown")
        units = args.get("units", "metric")
        
        temp = random.randint(15, 30) if units == "metric" else random.randint(60, 85)
        
        return {
            "location": location,
            "current": {
                "temperature": temp,
                "feels_like": temp + random.randint(-3, 3),
                "humidity": random.randint(40, 80),
                "description": random.choice(["Sunny", "Partly Cloudy", "Cloudy", "Light Rain"]),
                "wind_speed": random.randint(5, 20)
            },
            "units": units,
            "timestamp": datetime.now().isoformat()
        }
    
    def _mock_products(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Mock product listing"""
        products = [
            {"id": "prod_1", "name": "Laptop", "price": 999.99, "category": "electronics"},
            {"id": "prod_2", "name": "Headphones", "price": 79.99, "category": "electronics"},
            {"id": "prod_3", "name": "T-Shirt", "price": 19.99, "category": "clothing"},
            {"id": "prod_4", "name": "Coffee Maker", "price": 49.99, "category": "home"}
        ]
        
        category = args.get("category")
        if category:
            products = [p for p in products if p["category"] == category]
        
        return {
            "products": products,
            "page": args.get("page", 1),
            "limit": args.get("limit", 20),
            "total": len(products)
        }
    
    def _mock_cart(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Mock adding to cart"""
        return {
            "cart_id": "cart_123",
            "items": [
                {
                    "product_id": args.get("product_id"),
                    "quantity": args.get("quantity", 1)
                }
            ],
            "total_items": args.get("quantity", 1),
            "timestamp": datetime.now().isoformat()
        }


